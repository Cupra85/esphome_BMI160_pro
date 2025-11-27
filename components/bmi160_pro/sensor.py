import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor, binary_sensor
from esphome.const import CONF_ID

bmi160_pro_ns = cg.esphome_ns.namespace("bmi160_pro")
BMI160Pro = bmi160_pro_ns.class_("BMI160Pro", cg.PollingComponent, i2c.I2CDevice)

SIMPLE_SENSOR = sensor.sensor_schema()
SIMPLE_BINARY = binary_sensor.binary_sensor_schema()

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_ID): cv.declare_id(BMI160Pro),

            # Sensor outputs
            cv.Optional("accel_x"): SIMPLE_SENSOR,
            cv.Optional("accel_y"): SIMPLE_SENSOR,
            cv.Optional("accel_z"): SIMPLE_SENSOR,
            cv.Optional("gyro_x"): SIMPLE_SENSOR,
            cv.Optional("gyro_y"): SIMPLE_SENSOR,
            cv.Optional("gyro_z"): SIMPLE_SENSOR,
            cv.Optional("pitch"): SIMPLE_SENSOR,
            cv.Optional("roll"): SIMPLE_SENSOR,
            cv.Optional("inclination"): SIMPLE_SENSOR,
            cv.Optional("temperature"): SIMPLE_SENSOR,
            cv.Optional("vibration"): SIMPLE_SENSOR,

            # Binary Alert outputs
            cv.Optional("tilt_alert"): SIMPLE_BINARY,
            cv.Optional("motion_alert"): SIMPLE_BINARY,

            # Thresholds
            cv.Optional("tilt_threshold_deg", default=15.0): cv.float_,
            cv.Optional("motion_threshold_ms2", default=0.3): cv.float_,
            cv.Optional("vibration_threshold_ms2", default=0.5): cv.float_,
        }
    )
    .extend(i2c.i2c_device_schema(0x68))
    .extend(cv.polling_component_schema("5s"))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    # Thresholds setzen
    cg.add(var.set_tilt_threshold_deg(config["tilt_threshold_deg"]))
    cg.add(var.set_motion_threshold_ms2(config["motion_threshold_ms2"]))
    cg.add(var.set_vibration_threshold_ms2(config["vibration_threshold_ms2"]))

    # Normal sensors
    for key in config:
        if key in ["id", "tilt_threshold_deg", "motion_threshold_ms2", "vibration_threshold_ms2"]:
            continue
        if key in ["tilt_alert", "motion_alert"]:
            continue
        sens = await sensor.new_sensor(config[key])
        cg.add(getattr(var, f"set_{key}_sensor")(sens))

    # Binary sensor setup
    if "tilt_alert" in config:
        b = await binary_sensor.new_binary_sensor(config["tilt_alert"])
        cg.add(var.set_tilt_alert(b))

    if "motion_alert" in config:
        b = await binary_sensor.new_binary_sensor(config["motion_alert"])
        cg.add(var.set_motion_alert(b))
