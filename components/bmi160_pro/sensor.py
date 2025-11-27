import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import CONF_ID

# Namespace für C++
bmi160_pro_ns = cg.esphome_ns.namespace("bmi160_pro")
BMI160Pro = bmi160_pro_ns.class_("BMI160Pro", cg.PollingComponent, i2c.I2CDevice)

# Standard-Schema (kompatibel mit allen ESPHome-Versionen)
SIMPLE = sensor.sensor_schema()

CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_ID): cv.declare_id(BMI160Pro),

            cv.Optional("accel_x"): SIMPLE,
            cv.Optional("accel_y"): SIMPLE,
            cv.Optional("accel_z"): SIMPLE,

            cv.Optional("gyro_x"): SIMPLE,
            cv.Optional("gyro_y"): SIMPLE,
            cv.Optional("gyro_z"): SIMPLE,

            cv.Optional("pitch"): SIMPLE,
            cv.Optional("roll"): SIMPLE,
            cv.Optional("inclination"): SIMPLE,

            cv.Optional("temperature"): SIMPLE,
            cv.Optional("vibration"): SIMPLE,

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

    # Thresholds an Objekt schreiben
    cg.add(var.set_tilt_threshold_deg(config["tilt_threshold_deg"]))
    cg.add(var.set_motion_threshold_ms2(config["motion_threshold_ms2"]))
    cg.add(var.set_vibration_threshold_ms2(config["vibration_threshold_ms2"]))

    # Sensor-Objekte binden
    for key in config:
        if key not in ["id", "tilt_threshold_deg", "motion_threshold_ms2", "vibration_threshold_ms2"]:
            sens = await sensor.new_sensor(config[key])
            cg.add(getattr(var, f"set_{key}_sensor")(sens))
