#ifndef CONFIG_H
#define CONFIG_H

// ==========================================
// PyroTrace ESP32-C3 Firmware Configuration
// Target Hardware: ESP32-C3 Super Mini
// ==========================================

#define SERIAL_BAUD 115200
#define TELEMETRY_INTERVAL_MS 1000 // Send telemetry every 1000ms (1 second)

// Pin Definitions for Physical Hardware Sensors (ESP32-C3 Super Mini)
#define PIN_TEMP_SENSOR 0   // ADC Pin for Analog Temperature Sensor (e.g., LM35/NTC)
#define PIN_FAN_TACH    1   // GPIO Interrupt Pin for Fan Tachometer (RPM reading)
#define PIN_FAN_PWM     2   // PWM Output Pin for Fan Speed Control
#define PIN_LED_STATUS  8   // Onboard status LED (ESP32-C3 Super Mini default LED)

// Operational Threshold Constants for Telemetry Calibration
#define TEMP_BASE_C       35.0  // Baseline temperature in Celsius
#define TEMP_MAX_LIMIT_C  95.0  // Upper safety limit in Celsius

#define RPM_BASE_VAL      3200  // Baseline Fan RPM
#define RPM_MIN_LIMIT     500   // Minimum fan stall threshold RPM

#define CPU_LOAD_BASE     25.0  // Baseline CPU load percentage (%)
#define CPU_LOAD_MAX      100.0 // Max CPU load percentage (%)

// Simulation / Fault Injection Modes (0 = Hardware/Live, 1 = Thermal Spike, 2 = Fan Failure, 3 = High Load Spike)
extern int currentFaultMode;

#endif // CONFIG_H
