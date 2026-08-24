# PyroTrace — Walkthrough & Implementation Progress

PyroTrace is an edge-native, locally-processed AI diagnostic system designed to trace physical hardware failures back to their root cause in real time, operating entirely offline without cloud dependencies.

---

## 🏆 Completed Phases (All Phases 1 - 5 Complete)

### Phase 1: Edge Hardware & Microcontroller Firmware (`firmware/esp32_telemetry/`)
- **Target:** ESP32-C3 Super Mini
- **C++ Firmware:** [`firmware/esp32_telemetry/esp32_telemetry.ino`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/firmware/esp32_telemetry/esp32_telemetry.ino) & [`config.h`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/firmware/esp32_telemetry/config.h)
- **JSON Telemetry Stream:** Outputs `timestamp`, `temp` (°C), `rpm` (RPM), `cpu_load` (%), and `fault_mode` over USB Serial (`COM15`, 115200 baud).

### Phase 2: PySerial Data Ingestion Pipeline & Buffer (`src/ingestion.py`)
- **Ingestion Engine:** Reads raw telemetry from COM15 with PySerial and maintains a rolling 60-second Pandas DataFrame buffer.
- **Hardware/Simulation Fallback:** Automatically engages local synthetic sensor stream when physical COM15 port is disconnected.

### Phase 3: AI Detection & Causal Engine (`src/anomaly_detection.py`, `src/causal_tracing.py`)
- **Isolation Forest Anomaly Detector:** Scans rolling 60-second buffer data to detect hardware threshold breaches and statistical outliers.
- **Time-Lagged Causal Tracing Engine:** Analyzes time lags and sequence ordering to map the root cause ($A \rightarrow B \rightarrow C$) and output prescriptive remediation instructions.

### Phase 4: Streamlit & Plotly Presentation Layer (`dashboard/app.py`, `dashboard/visualizations.py`)
- **Interactive Dark Dashboard:** Live telemetry feeds, status badges, KPI metric cards, Plotly multi-axis line graphs, gauge meters, horizontal causal chain diagrams, and physical fault injection controls.

### Phase 5: Final Polish & Pitch Presentation (`docs/NEURAL_X_PPT.pptx`)
- **Pitch Deck:** Created slide presentation at [`docs/NEURAL_X_PPT.pptx`](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/docs/NEURAL_X_PPT.pptx) highlighting problem statement, causal engine solution, competitive analysis, and value metrics.
- **Tagline Branding:** Aligned *"Build Beyond Boundaries"* across pitch materials and panel headers.

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
│   ├── ingestion.py                   # Ingestor & 60s Pandas Buffer
│   ├── anomaly_detection.py           # Isolation Forest Anomaly Detector
│   └── causal_tracing.py              # Time-Lagged Causal Root Cause Engine
├── dashboard/
│   ├── __init__.py
│   ├── app.py                         # Streamlit Interactive Dashboard
│   ├── visualizations.py              # Plotly Visualizations & Causal Graphs
│   └── assets/
│       └── style.css                  # Custom CSS Stylesheet
├── docs/
│   ├── architecture.md                # System Flow
│   ├── folder_structure.md            # File Specs
│   └── NEURAL_X_PPT.pptx              # Pitch Slides
├── work_logs/
│   ├── PHASE_1_AND_2_COMPLETION.md    # Work Log for Phase 1 & 2
│   ├── PHASE_3_AND_4_COMPLETION.md    # Work Log for Phase 3 & 4
│   └── PHASE_5_COMPLETION.md          # Work Log for Phase 5
├── Arctricute.md                      # System Architecture
├── FILE_STRUCTURE.md                  # Detailed Folder Structure Specs
├── IMPLEMENTATION_PLAN.md             # Master Roadmap
├── requirements.txt                   # Project Dependencies
└── WALKTHROUGH.md                     # System Progress Walkthrough
```

---

## 📝 Work Log Artifacts

- [Phase 1 & 2 Completion Report](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/work_logs/PHASE_1_AND_2_COMPLETION.md)
- [Phase 3 & 4 Completion Report](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/work_logs/PHASE_3_AND_4_COMPLETION.md)
- [Phase 5 Completion Report](file:///c:/aa/wearegoingtoloose/wegoingtoloosefs/work_logs/PHASE_5_COMPLETION.md)

---

## 🚀 Running the Application

To launch the dashboard locally:
```bash
streamlit run dashboard/app.py
```
Open your browser at `http://localhost:8501`.
