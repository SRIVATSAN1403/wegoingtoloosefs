# PyroTrace — Walkthrough & Implementation Progress

PyroTrace is an edge-native, locally-processed AI diagnostic system designed to trace physical hardware failures back to their root cause in real time, operating entirely offline without cloud dependencies.

---

## 🏆 Current Progress: Phase 1 & Phase 2 Complete

### Phase 1: Edge Hardware & Microcontroller Firmware (`firmware/esp32_telemetry/`)
- **Microcontroller Target:** ESP32-C3 Super Mini
- **C++ Firmware:** [`firmware/esp32_telemetry/esp32_telemetry.ino`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/firmware/esp32_telemetry/esp32_telemetry.ino) & [`config.h`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/firmware/esp32_telemetry/config.h)
- **JSON Telemetry Stream:** Outputs `timestamp`, `temp` (°C), `rpm` (RPM), `cpu_load` (%), and `fault_mode` over USB Serial (`COM15`, 115200 baud).
- **Interactive Fault Ingestion:** Includes live triggers for Normal, Thermal Spike, Fan Failure, and CPU Load Surge.

### Phase 2: PySerial Data Ingestion Pipeline & Buffer (`src/ingestion.py`)
- **Serial Connection:** Reads raw JSON telemetry from COM15 with PySerial.
- **Hardware/Simulation Fallback:** Seamlessly switches to local synthetic sensor stream when COM15 hardware is disconnected.
- **Rolling 60-Second Buffer:** Maintains a memory-stable Pandas DataFrame keeping strictly the last 60 seconds of telemetry data.
- **Flat Memory Profile:** Prevents memory leaks and handles data rate spikes smoothly.

---

## 📁 Project Directory Structure

```text
wegoingtoloosefs/
├── firmware/
│   └── esp32_telemetry/
│       ├── esp32_telemetry.ino        # C++ firmware sketch for ESP32-C3
│       └── config.h                   # Pin definitions and thresholds
├── src/
│   ├── __init__.py                    # Source package initialization
│   └── ingestion.py                   # Serial Ingestor & 60s Pandas Buffer Manager
├── work_logs/
│   └── PHASE_1_AND_2_COMPLETION.md    # Dedicated completion log for Phase 1 & 2
├── Arctricute.md                      # System Architecture
├── FILE_STRUCTURE.md                  # Detailed Folder Structure Specs
├── IMPLEMENTATION_PLAN.md             # Master Roadmap (Phases 1-5)
├── requirements.txt                   # Project Dependencies
└── WALKTHROUGH.md                     # System Progress Walkthrough
```

---

## 📝 Work Log Artifacts

All finished milestones are logged in the dedicated work log directory:
- [Phase 1 & 2 Completion Report](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/work_logs/PHASE_1_AND_2_COMPLETION.md)
