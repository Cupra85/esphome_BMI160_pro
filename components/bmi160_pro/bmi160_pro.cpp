#include "bmi160_pro.h"
#include "esphome/core/log.h"

namespace esphome {
namespace bmi160_pro {

static const char *const TAG = "bmi160_pro";

void BMI160Pro::setup() {
  ESP_LOGCONFIG(TAG, "Setting up BMI160...");

  // Soft reset
  this->write_byte(0x7E, 0xB6);
  delay(100);

  // Configure accelerometer to ±2g, normalized mode
  this->write_byte(0x40, 0x28);
  // Configure gyro to 2000°/s
  this->write_byte(0x42, 0x26);

  // Setup complete
  ESP_LOGI(TAG, "BMI160 setup done");
}

void BMI160Pro::update() {
  // ----- ACCEL + GYRO READ -----
  uint8_t data[12];  // 6*2 bytes
  if (!this->read_bytes(0x12, data, 12)) {
    ESP_LOGW(TAG, "BMI160 read failed!");
    return;
  }

  // Convert raw 16-bit values
  int16_t ax = (int16_t)((data[1] << 8) | data[0]);
  int16_t ay = (int16_t)((data[3] << 8) | data[2]);
  int16_t az = (int16_t)((data[5] << 8) | data[4]);
  int16_t gx = (int16_t)((data[7] << 8) | data[6]);
  int16_t gy = (int16_t)((data[9] << 8) | data[8]);
  int16_t gz = (int16_t)((data[11] << 8) | data[10]);

  // ----- SCALE TO SI UNITS -----
  const float accel_scale = 9.80665f / 16384.0f;  // LSB per g
  const float gyro_scale = 2000.0f / 32768.0f;    // deg/s

  float ax_ms2 = ax * accel_scale;
  float ay_ms2 = ay * accel_scale;
  float az_ms2 = az * accel_scale;

  float gx_deg = gx * gyro_scale;
  float gy_deg = gy * gyro_scale;
  float gz_deg = gz * gyro_scale;

  // ----- ANGLES -----
  // Simple estimate (replace later with complementary filter)
  float pitch = atan2f(ay_ms2, sqrtf(ax_ms2 * ax_ms2 + az_ms2 * az_ms2)) * 180.0f / PI;
  float roll  = atan2f(-ax_ms2, az_ms2) * 180.0f / PI;
  float incl  = sqrtf(pitch * pitch + roll * roll);

  // ----- TEMPERATURE READ -----
  uint8_t temp_raw;
  if (this->read_byte(0x20, &temp_raw)) {
    temperature_ = (float)temp_raw * 0.5f + 23.0f;  // basic conversion
  }

  // ----- VIBRATION ESTIMATE -----
  float vibration = fabsf(ax_ms2) + fabsf(ay_ms2) + fabsf(az_ms2);
  vibration -= 9.80665f;  // subtract gravity contribution

  // ----- PUBLISH SENSOR VALUES -----
  if (accel_x_sensor_) accel_x_sensor_->publish_state(ax_ms2);
  if (accel_y_sensor_) accel_y_sensor_->publish_state(ay_ms2);
  if (accel_z_sensor_) accel_z_sensor_->publish_state(az_ms2);

  if (gyro_x_sensor_) gyro_x_sensor_->publish_state(gx_deg);
  if (gyro_y_sensor_) gyro_y_sensor_->publish_state(gy_deg);
  if (gyro_z_sensor_) gyro_z_sensor_->publish_state(gz_deg);

  if (pitch_sensor_) pitch_sensor_->publish_state(pitch);
  if (roll_sensor_)  roll_sensor_->publish_state(roll);
  if (inclination_sensor_) inclination_sensor_->publish_state(incl);

  if (temperature_sensor_) temperature_sensor_->publish_state(temperature_);
  if (vibration_sensor_) vibration_sensor_->publish_state(vibration);

  // optional thresholds, not published as binary sensors here
  if (fabsf(pitch) > tilt_threshold_deg_ || fabsf(roll) > tilt_threshold_deg_) {
    ESP_LOGD(TAG, "Tilt threshold exceeded");
  }
  if (vibration > vibration_threshold_ms2_) {
    ESP_LOGD(TAG, "Vibration threshold exceeded");
  }
  if (fabsf(ax_ms2) > motion_threshold_ms2_ ||
      fabsf(ay_ms2) > motion_threshold_ms2_ ||
      fabsf(az_ms2) > motion_threshold_ms2_) {
    ESP_LOGD(TAG, "Motion threshold exceeded");
  }
}

}  // namespace bmi160_pro
}  // namespace esphome
