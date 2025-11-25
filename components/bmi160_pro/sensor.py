import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, binary_sensor
from esphome.const import CONF_ID

bmi160_pro_ns = cg.esphome_ns.namespace("bmi160_pro")
BMI160Pro = bmi160_pro_ns.class_("BMI160Pro", cg.PollingComponent)

CONF_ACCEL_X = "accel_x"
CONF_ACCEL_Y = "accel_y"
CONF_ACCEL_Z = "accel_z"
CONF_GYRO_X = "gyro_x"
CONF_GYRO_Y = "gyro_y"
CONF_GYRO_Z = "gyro_z"
CONF_PITCH = "pitch"
CONF_ROLL = "roll"
CONF_INCLINATION = "inclination"
CONF_TEMPERATURE = "temperature"
CONF_VIBRATION = "vibration"
CONF_TILT_ALERT = "tilt_alert"
CONF_MOTION_ALERT = "motion_alert"
CONF_TILT_THRESHOLD = "tilt_threshold_deg"
CONF_MOTION_THRESHOLD = "motion_threshold_ms2"

CONFIG_SCHEMA = cv.Schema(
    {
        cv.GenerateID(): cv.declare_id(BMI160Pro),

        cv.Optional(CONF_TILT_THRESHOLD, default=10.0): cv.float_,
        cv.Optional(CONF_MOTION_THRESHOLD, default=1.0): cv.float_,

        cv.Optional(CONF_ACCEL_X): sensor.sensor_schema(),
        cv.Optional(CONF_ACCEL_Y): sensor.sensor_schema(),
        cv.Optional(CONF_ACCEL_Z): sensor.sensor_schema(),
        cv.Optional(CONF_GYRO_X): sensor.sensor_schema(),
        cv.Optional(CONF_GYRO_Y): sensor.sensor_schema(),
        cv.Optional(CONF_GYRO_Z): sensor.sensor_schema(),
        cv.Optional(CONF_PITCH): sensor.sensor_schema(),
        cv.Optional(CONF_ROLL): sensor.sensor_schema(),
        cv.Optional(CONF_INCLINATION): sensor.sensor_schema(),
        cv.Optional(CONF_TEMPERATURE): sensor.sensor_schema(),
        cv.Optional(CONF_VIBRATION): sensor.sensor_schema(),

        cv.Optional(CONF_TILT_ALERT): binary_sensor.binary_sensor_schema(),
        cv.Optional(CONF_MOTION_ALERT): binary_sensor.binary_sensor_schema(),
    }
).extend(cv.COMPONENT_SCHEMA)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    if CONF_TILT_THRESHOLD in config:
        cg.add(var.tilt_threshold_deg = config[CONF_TILT_THRESHOLD])
    if CONF_MOTION_THRESHOLD in config:
        cg.add(var.motion_threshold_ms2 = config[CONF_MOTION_THRESHOLD])

    if CONF_ACCEL_X in config:
        sens = await sensor.new_sensor(config[CONF_ACCEL_X])
        cg.add(var.accel_x = sens)
    if CONF_ACCEL_Y in config:
        sens = await sensor.new_sensor(config[CONF_ACCEL_Y])
        cg.add(var.accel_y = sens)
    if CONF_ACCEL_Z in config:
        sens = await sensor.new_sensor(config[CONF_ACCEL_Z])
        cg.add(var.accel_z = sens)

    if CONF_GYRO_X in config:
        sens = await sensor.new_sensor(config[CONF_GYRO_X])
        cg.add(var.gyro_x = sens)
    if CONF_GYRO_Y in config:
        sens = await sensor.new_sensor(config[CONF_GYRO_Y])
        cg.add(var.gyro_y = sens)
    if CONF_GYRO_Z in config:
        sens = await sensor.new_sensor(config[CONF_GYRO_Z])
        cg.add(var.gyro_z = sens)

    if CONF_PITCH in config:
        sens = await sensor.new_sensor(config[CONF_PITCH])
        cg.add(var.pitch = sens)
    if CONF_ROLL in config:
        sens = await sensor.new_sensor(config[CONF_ROLL])
        cg.add(var.roll = sens)
    if CONF_INCLINATION in config:
        sens = await sensor.new_sensor(config[CONF_INCLINATION])
        cg.add(var.incl = sens)

    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.temperature = sens)
    if CONF_VIBRATION in config:
        sens = await sensor.new_sensor(config[CONF_VIBRATION])
        cg.add(var.vibration = sens)

    if CONF_TILT_ALERT in config:
        bs = await binary_sensor.new_binary_sensor(config[CONF_TILT_ALERT])
        cg.add(var.tilt_alert = bs)
    if CONF_MOTION_ALERT in config:
        bs = await binary_sensor.new_binary_sensor(config[CONF_MOTION_ALERT])
        cg.add(var.motion_alert = bs)
