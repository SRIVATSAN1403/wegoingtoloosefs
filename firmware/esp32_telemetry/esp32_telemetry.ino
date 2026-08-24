/*
 * PyroTrace - Edge Telemetry Firmware
 * Target Microcontroller: ESP32-C3 Super Mini
 * Output: Serial JSON Stream over USB (Targeting COM15)
 * Telemetry Fields: timestamp (seconds), temp (°C), rpm (RPM), cpu_load (%)
 */

#include <Arduino.h>
#include "config.h"

// Track operational state
unsigned long lastTelemetryTime = 0;
unsigned long secondsCounter = 0;
int currentFaultMode = 0; // 0: Normal, 1: Thermal Spike, 2: Fan Bearing Failure, 3: CPU Load Surge

void setup() {
  // Initialize Serial interface
  Serial.begin(SERIAL_BAUD);

  // Initialize hardware pins
  pinMode(PIN_LED_STATUS, OUTPUT);
  digitalWrite(PIN_LED_STATUS, HIGH); // Active low or high indicator

#if defined(PIN_TEMP_SENSOR)
  analogReadResolution(12);
#endif

  // Brief delay for serial stabilization
  delay(1000);
}

void loop() {
  unsigned long currentMillis = millis();

  // Handle incoming serial commands for manual fault injection during physical/demo tests
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == '0') currentFaultMode = 0; // Reset Normal
    if (cmd == '1') currentFaultMode = 1; // Thermal Spike
    if (cmd == '2') currentFaultMode = 2; // Fan Failure
    if (cmd == '3') currentFaultMode = 3; // CPU Load Surge
  }

  // Periodic Telemetry Dispatch
  if (currentMillis - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = currentMillis;
    secondsCounter++;

    float temp = TEMP_BASE_C;
    float rpm = RPM_BASE_VAL;
    float cpuLoad = CPU_LOAD_BASE;

    // Apply baseline natural noise
    temp += random(-10, 10) / 10.0f;
    rpm += random(-35, 35);
    cpuLoad += random(-20, 20) / 10.0f;

    // Dynamic Fault Simulation Curves based on currentFaultMode
    switch (currentFaultMode) {
      case 1: // Thermal Spike (e.g. Heatsink detachment)
        temp += min(45.0f, (float)(secondsCounter % 60) * 1.8f);
        cpuLoad += 15.0f;
        break;
      case 2: // Fan Bearing Failure (RPM drops -> Temperature rises after lag)
        rpm = max(400.0f, RPM_BASE_VAL - ((secondsCounter % 60) * 80.0f));
        if (rpm < 1200.0f) {
          temp += (1200.0f - rpm) * 0.03f;
        }
        break;
      case 3: // CPU Load Spike (CPU hits 100% -> Temperature increases)
        cpuLoad = min(100.0f, 85.0f + random(0, 15));
        temp += 20.0f + random(-5, 5) / 10.0f;
        rpm += 600; // Fan ramps up in response
        break;
      default:
        // Normal baseline fluctuation
        break;
    }

    // Bound values within realistic hardware limits
    temp = constrain(temp, 20.0f, 105.0f);
    rpm = constrain(rpm, 0.0f, 5500.0f);
    cpuLoad = constrain(cpuLoad, 0.0f, 100.0f);

    // Format telemetry as clean JSON object
    // Example: {"timestamp": 123, "temp": 38.5, "rpm": 3180, "cpu_load": 27.2, "fault_mode": 0}
    Serial.print("{\"timestamp\":");
    Serial.print(secondsCounter);
    Serial.print(",\"temp\":");
    Serial.print(temp, 1);
    Serial.print(",\"rpm\":");
    Serial.print((int)rpm);
    Serial.print(",\"cpu_load\":");
    Serial.print(cpuLoad, 1);
    Serial.print(",\"fault_mode\":");
    Serial.print(currentFaultMode);
    Serial.println("}");

    // Toggle onboard LED to visually signal active serial transmission
    digitalWrite(PIN_LED_STATUS, !digitalRead(PIN_LED_STATUS));
  }
}
