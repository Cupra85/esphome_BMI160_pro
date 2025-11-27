import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor, binary_sensor
from esphome.const import CONF_ID

bmi160_pro_ns = cg.esphome_ns.namespace("bmi160_pro")
BMI160Pro = bmi160_pro_ns.class_("BMI160Pro", cg.PollingComponent, i2c.I2CDevice)

S_SIMPLE = sensor.sensor_schema()
B_SIMPLE = binary_sensor.binary_sensor_schema()

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_ID): cv.declare_id(BMI160Pro),

            # Sensor outputs
            cv.Optional("accel_x"): S_SIMPLE,
            cv.Optional("accel_y"): S_SIMPLE,
            cv.Optional("accel_z"): S_SIMPLE,
            cv.Optional("gyro_x"): S_SIMPLE,
            cv.Optional("gyro_y"): S_SIMPLE,
            cv.Optional("gyro_z"): S_SIMPLE,
            cv.Optional("pitch"): S_SIMPLE,
            cv.Optional("roll"): S_SIMPLE,
            cv.Optional("inclination"): S_SIMPLE,
            cv.Optional("temperature"): S_SIMPLE,
            cv.Optional("vibration"): S_SIMPLE,

            # Binary alert outputs
            cv.Optional("tilt_alert"): B_SIMPLE,
            cv.Optional("motion_alert"): B_SIMPLE,

            # Thresholds
            cv.Optional("tilt_threshold_deg", default=15.0): cv.float_,
            cv.Optional("motion_threshold_ms2", default=0.3): cv.float_,
            cv.Optional("vibration_threshold_ms2", default=0.5): cv.float_,

            # Complementary Filter Parameter
            cv.Optional("filter_alpha", default=0.98): cv.float_range(min=0.80, max=0.999),
        }
    )
    .extend(i2c.i2c_device_schema(0x68))
    .extend(cv.polling_component_schema("5s"))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    # Thresholds
    cg.add(var.set_tilt_threshold_deg(config["tilt_threshold_deg"]))
    cg.add(var.set_motion_threshold_ms2(config["motion_threshold_ms2"]))
    cg.add(var.set_vibration_threshold_ms2(config["vibration_threshold_ms2"]))
    cg.add(var.set_filter_alpha(config["filter_alpha"]))

    # Normal sensor assignment + automatic ID fix
    for key in config:
        if key in ["id", "tilt_threshold_deg", "motion_threshold_ms2", "vibration_threshold_ms2", "filter_alpha"]:
            continue
        if key in ["tilt_alert", "motion_alert"]:
            continue

        value = config[key]

        # If user only writes a string → make it a dict
        if isinstance(value, str):
            value = {"name": value}

        # If the user provides a dict without id → auto generate
        if "id" not in value:
            value["id"] = f"{config[CONF_ID]}_{key}"

        sens = await sensor.new_sensor(value)
        cg.add(getattr(var, f"set_{key}_sensor")(sens))

    # Binary sensors
    if "tilt_alert" in config:
        b = await binary_sensor.new_binary_sensor(config["tilt_alert"])
        cg.add(var.set_tilt_alert(b))

    if "motion_alert" in config:
        b = await binary_sensor.new_binary_sensor(config["motion_alert"])
        cg.add(var.set_motion_alert(b))
