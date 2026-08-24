# Phase 1 & Phase 2 Completion Report: Edge Hardware & Data Pipeline

**Project:** PyroTrace  
**Date:** August 24, 2026  
**Status:** Completed  

---

## Executive Summary

Phase 1 (Edge Hardware & Microcontroller Firmware) and Phase 2 (Data Ingestion Pipeline & Rolling Memory Buffer) have been fully designed, implemented, and verified. The system establishes an offline, zero-cloud data pipeline streaming real-time sensor telemetry from an ESP32-C3 Super Mini over USB serial (COM15) into a rolling 60-second Pandas DataFrame buffer.

---

## 1. Phase 1: Edge Hardware & Firmware Implementation

### Component Overview
* **Microcontroller Target:** ESP32-C3 Super Mini
* **Communication Protocol:** JSON payload over Serial USB (Targeting `COM15`, Baud rate `115200`)
* **Files Created:**
  * [`firmware/esp32_telemetry/config.h`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/firmware/esp32_telemetry/config.h) - Pin assignments, baseline sensor constants, and hardware thresholds.
  * [`firmware/esp32_telemetry/esp32_telemetry.ino`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/firmware/esp32_telemetry/esp32_telemetry.ino) - Main Arduino C++ firmware logic.

### Key Features
1. **Telemetry JSON Schema:** Generates continuous 1 Hz telemetry in JSON format:
   ```json
   {
     "timestamp": 124,
     "temp": 36.2,
     "rpm": 3210,
     "cpu_load": 25.4,
     "fault_mode": 0
   }
   ```
2. **Dynamic Fault Simulation Engine:** Supports physical sensor readings as well as live hardware demo fault modes triggered via serial input:
   * Mode `0`: Normal operating state.
   * Mode `1`: Thermal Spike (simulates heatsink detachment / cooling breakdown).
   * Mode `2`: Fan Bearing Failure (simulates RPM decay followed by delayed thermal buildup).
   * Mode `3`: CPU Load Surge (simulates 100% CPU utilization leading to elevated temperatures).
3. **Status Heartbeat:** Toggles onboard LED to provide immediate visual indication of serial transmission.

---

## 2. Phase 2: Offline PySerial Data Ingestion Pipeline

### Component Overview
* **Target Transport:** Local USB Serial (`COM15` default)
* **Data Processor:** Python PySerial + Pandas
* **Files Created:**
  * [`src/__init__.py`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/src/__init__.py) - Package initialization.
  * [`src/ingestion.py`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/src/ingestion.py) - `SerialIngestor` class for thread-safe data stream ingestion and buffer management.
  * [`requirements.txt`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/requirements.txt) - Python dependency declarations (`pandas`, `pyserial`, `scikit-learn`, `streamlit`, `plotly`, `numpy`).

### Key Features
1. **Thread-Safe Ingestion Pipeline:** Runs ingestion in a dedicated background thread, ensuring zero frame dropping or dashboard UI blocking.
2. **60-Second Rolling Window Buffer:** Maintains an in-memory Pandas DataFrame containing strictly the last 60 seconds of telemetry data (`timestamp`, `temp`, `rpm`, `cpu_load`, `fault_mode`, `datetime`).
3. **Flat Memory Utilization:** Automatically prunes old data outside the rolling window and caps buffer size to guarantee stable memory consumption during data spikes.
4. **Seamless Hardware/Simulation Fallback:**
   * If an ESP32-C3 Super Mini is plugged into `COM15`, the engine reads live hardware serial bytes.
   * If hardware is disconnected or testing on a machine without `COM15`, the engine automatically engages a high-fidelity sensor simulator so development and AI modeling continue uninterrupted.

---

## 3. Directory Structure

```text
wegoingtoloosefs/
├── firmware/
│   └── esp32_telemetry/
│       ├── esp32_telemetry.ino    # Arduino C++ Firmware
│       └── config.h               # Hardware Pin and Threshold Config
├── src/
│   ├── __init__.py                # Source package init
│   └── ingestion.py               # Serial Ingestion & 60s Rolling Buffer
├── work_logs/
│   └── PHASE_1_AND_2_COMPLETION.md # This completion report
├── requirements.txt               # Dependencies
├── Arctricute.md                  # System Architecture
├── FILE_STRUCTURE.md              # Folder Structure Specs
└── IMPLEMENTATION_PLAN.md         # Master Implementation Plan
```

---

## 4. Next Steps

With Phase 1 & 2 complete, the project is ready for:
* **Phase 3:** AI Detection & Causal Engine implementation (`src/anomaly_detection.py` using Isolation Forest and `src/causal_tracing.py` for time-lagged cross-correlation).
* **Phase 4:** Streamlit & Plotly Dashboard visualization (`dashboard/app.py`).
