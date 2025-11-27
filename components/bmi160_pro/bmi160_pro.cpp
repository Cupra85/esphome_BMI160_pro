#include "bmi160_pro.h"
#include "esphome/core/log.h"
#include <cmath>

namespace esphome {
namespace bmi160_pro {

static const char *const TAG = "bmi160_pro";

void BMI160Pro::setup() {
  ESP_LOGCONFIG(TAG, "Setting up BMI160...");

  // Soft reset
  this->write_byte(0x7E, 0xB6);
  delay(100);

  // Configure accelerometer: +-2g, normal mode (0x28)
  this->write_byte(0x40, 0x28);

  // Configure gyro: 2000 °/s (0x26)
  this->write_byte(0x42, 0x26);

  ESP_LOGI(TAG, "BMI160 setup done");
}

void BMI160Pro::update() {
  // ----- ACCEL + GYRO READ -----
  uint8_t data[12];
  if (!this->read_bytes(0x12, data, 12)) {
    ESP_LOGW(TAG, "BMI160 read failed");
    return;
  }

  // 16-bit conversion
  int16_t ax = (data[1] << 8) | data[0];
  int16_t ay = (data[3] << 8) | data[2];
  int16_t az = (data[5] << 8) | data[4];
  int16_t gx = (data[7] << 8) | data[6];
  int16_t gy = (data[9] << 8) | data[8];
  int16_t gz = (data[11] << 8) | data[10];

  // ----- SCALE TO SI UNITS -----
  const float a = 9.80665f / 16384.0f;  // accel: g → m/s²
  const float g = 2000.0f / 32768.0f;   // gyro: LSB → °/s

  float axm = ax * a;
  float aym = ay * a;
  float azm = az * a;

  float gxm = gx * g;
  float gym = gy * g;
  float gzm = gz * g;

  // ----- ANGLES -----
  float pitch = atan2f(aym, sqrtf(axm * axm + azm * azm)) * 180.0f / M_PI;
  float roll  = atan2f(-axm, azm) * 180.0f / M_PI;
  float incl  = sqrtf(pitch * pitch + roll * roll);

  // ----- TEMPERATURE -----
  uint8_t tmp;
  if (this->read_byte(0x20, &tmp)) {
    temperature_ = tmp * 0.5f + 23.0f;
  }

  // ----- VIBRATION -----
  float vibe = fabsf(axm) + fabsf(aym) + fabsf(azm) - 9.80665f;

  // ----- PUBLISH SENSOR VALUES -----
  if (accel_x_sensor_) accel_x_sensor_->publish_state(axm);
  if (accel_y_sensor_) accel_y_sensor_->publish_state(aym);
  if (accel_z_sensor_) accel_z_sensor_->publish_state(azm);

  if (gyro_x_sensor_) gyro_x_sensor_->publish_state(gxm);
  if (gyro_y_sensor_) gyro_y_sensor_->publish_state(gym);
  if (gyro_z_sensor_) gyro_z_sensor_->publish_state(gzm);

  if (pitch_sensor_) pitch_sensor_->publish_state(pitch);
  if (roll_sensor_) roll_sensor_->publish_state(roll);
  if (inclination_sensor_) inclination_sensor_->publish_state(incl);

  if (temperature_sensor_) temperature_sensor_->publish_state(temperature_);
  if (vibration_sensor_) vibration_sensor_->publish_state(vibe);

  // ----- ALERTS -----
  if (tilt_alert_) {
    bool tilted = fabsf(pitch) > tilt_threshold_deg_ || fabsf(roll) > tilt_threshold_deg_;
    tilt_alert_->publish_state(tilted);
  }

  if (motion_alert_) {
    bool moved =
      fabsf(axm) > motion_threshold_ms2_ ||
      fabsf(aym) > motion_threshold_ms2_ ||
      fabsf(azm) > motion_threshold_ms2_;
    motion_alert_->publish_state(moved);
  }
}

}  // namespace bmi160_pro
}  // namespace esphome
