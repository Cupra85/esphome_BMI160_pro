import esphome.codegen as cg
import esphome.config_validation as cv

from esphome.components import i2c, sensor
from esphome.const import (
    CONF_ID,
    CONF_ADDRESS,
    CONF_UPDATE_INTERVAL,
    UNIT_METER_PER_SECOND_SQUARED,
    UNIT_DEGREE,
    UNIT_CELSIUS,
    ICON_ACCELERATION,
    ICON_THERMOMETER,
    ICON_ROTATE_3D,
    STATE_CLASS_MEASUREMENT,
)

# ----- Metadaten für ESPHome -----
# Mehrere Instanzen erlaubt
MULTI_CONF = True

# Wir benötigen den I2C-Bus
DEPENDENCIES = ["i2c"]

# Namespace und C++-Klasse
bmi160_pro_ns = cg.esphome_ns.namespace("bmi160_pro")
BMI160Pro = bmi160_pro_ns.class_("BMI160Pro", cg.PollingComponent, i2c.I2CDevice)

# ---- eigene Konfig-Keys ----
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

CONF_TILT_THRESHOLD = "tilt_threshold_deg"
CONF_MOTION_THRESHOLD = "motion_threshold_ms2"
CONF_VIBRATION_THRESHOLD = "vibration_threshold_ms2"

# ----- Sensor-Schemata -----
accel_schema = sensor.sensor_schema(
    unit_of_measurement=UNIT_METER_PER_SECOND_SQUARED,
    icon=ICON_ACCELERATION,
    accuracy_decimals=3,
    state_class=STATE_CLASS_MEASUREMENT,
)

gyro_schema = sensor.sensor_schema(
    unit_of_measurement=UNIT_DEGREE + "/s",
    icon=ICON_ROTATE_3D,
    accuracy_decimals=3,
    state_class=STATE_CLASS_MEASUREMENT,
)

angle_schema = sensor.sensor_schema(
    unit_of_measurement=UNIT_DEGREE,
    icon=ICON_ROTATE_3D,
    accuracy_decimals=1,
    state_class=STATE_CLASS_MEASUREMENT,
)

temp_schema = sensor.sensor_schema(
    unit_of_measurement=UNIT_CELSIUS,
    icon=ICON_THERMOMETER,
    accuracy_decimals=1,
    state_class=STATE_CLASS_MEASUREMENT,
)

vibration_schema = sensor.sensor_schema(
    unit_of_measurement=UNIT_METER_PER_SECOND_SQUARED,
    icon=ICON_ACCELERATION,
    accuracy_decimals=3,
    state_class=STATE_CLASS_MEASUREMENT,
)

# ----- CONFIG_SCHEMA -----
CONFIG_SCHEMA = (
    cv.Schema(
        {
            cv.GenerateID(CONF_ID): cv.declare_id(BMI160Pro),

            # optionale Outputs
            cv.Optional(CONF_ACCEL_X): accel_schema,
            cv.Optional(CONF_ACCEL_Y): accel_schema,
            cv.Optional(CONF_ACCEL_Z): accel_schema,

            cv.Optional(CONF_GYRO_X): gyro_schema,
            cv.Optional(CONF_GYRO_Y): gyro_schema,
            cv.Optional(CONF_GYRO_Z): gyro_schema,

            cv.Optional(CONF_PITCH): angle_schema,
            cv.Optional(CONF_ROLL): angle_schema,
            cv.Optional(CONF_INCLINATION): angle_schema,

            cv.Optional(CONF_TEMPERATURE): temp_schema,
            cv.Optional(CONF_VIBRATION): vibration_schema,

            # Zusatz-Parameter für C++ (Schwellenwerte)
            cv.Optional(CONF_TILT_THRESHOLD, default=15.0): cv.float_range(
                min=0.0, max=90.0
            ),
            cv.Optional(CONF_MOTION_THRESHOLD, default=0.3): cv.float_range(
                min=0.0, max=10.0
            ),
            cv.Optional(CONF_VIBRATION_THRESHOLD, default=0.5): cv.float_range(
                min=0.0, max=50.0
            ),
        }
    )
    # Standard I2C-Schema inkl. address / i2c_id
    .extend(i2c.i2c_device_schema(0x68))
    # Polling-Intervall (update_interval)
    .extend(cv.polling_component_schema("5s"))
)

# ----- Code-Generierung -----
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])

    # als Komponente und I2C-Device registrieren
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    # Schwellenwerte ins C++ Objekt schreiben
    cg.add(var.set_tilt_threshold_deg(config[CONF_TILT_THRESHOLD]))
    cg.add(var.set_motion_threshold_ms2(config[CONF_MOTION_THRESHOLD]))
    cg.add(var.set_vibration_threshold_ms2(config[CONF_VIBRATION_THRESHOLD]))

    # Sensor-Instanzen an das C++ Objekt durchreichen
    if CONF_ACCEL_X in config:
        sens = await sensor.new_sensor(config[CONF_ACCEL_X])
        cg.add(var.set_accel_x_sensor(sens))

    if CONF_ACCEL_Y in config:
        sens = await sensor.new_sensor(config[CONF_ACCEL_Y])
        cg.add(var.set_accel_y_sensor(sens))

    if CONF_ACCEL_Z in config:
        sens = await sensor.new_sensor(config[CONF_ACCEL_Z])
        cg.add(var.set_accel_z_sensor(sens))

    if CONF_GYRO_X in config:
        sens = await sensor.new_sensor(config[CONF_GYRO_X])
        cg.add(var.set_gyro_x_sensor(sens))

    if CONF_GYRO_Y in config:
        sens = await sensor.new_sensor(config[CONF_GYRO_Y])
        cg.add(var.set_gyro_y_sensor(sens))

    if CONF_GYRO_Z in config:
        sens = await sensor.new_sensor(config[CONF_GYRO_Z])
        cg.add(var.set_gyro_z_sensor(sens))

    if CONF_PITCH in config:
        sens = await sensor.new_sensor(config[CONF_PITCH])
        cg.add(var.set_pitch_sensor(sens))

    if CONF_ROLL in config:
        sens = await sensor.new_sensor(config[CONF_ROLL])
        cg.add(var.set_roll_sensor(sens))

    if CONF_INCLINATION in config:
        sens = await sensor.new_sensor(config[CONF_INCLINATION])
        cg.add(var.set_inclination_sensor(sens))

    if CONF_TEMPERATURE in config:
        sens = await sensor.new_sensor(config[CONF_TEMPERATURE])
        cg.add(var.set_temperature_sensor(sens))

    if CONF_VIBRATION in config:
        sens = await sensor.new_sensor(config[CONF_VIBRATION])
        cg.add(var.set_vibration_sensor(sens))
