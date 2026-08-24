# Walkthrough — `neuralX`: ESP32-C3 & Enterprise AI Root-Cause Intelligence Platform

We have built **`neuralX`**, an end-to-end AI system created for problem **AI-04: AI Anomaly Root-Cause Analyzer**.

---

## 🏆 Key Features & Value Proposition

1. **Live Sensor Monitoring via ESP32-C3 (RPM, Temperature, CPU Load)**:
   - Tracks `esp32_cpu_load_pct`, `chip_temperature_c`, `motor_rpm_sensor`, `gpio_interrupt_lag_ms`, and `sensor_bus_voltage_v`.
   - Includes Arduino C++ firmware sketch (`esp32_c3_firmware.ino`) and Python serial bridge (`src/hardware/esp32_bridge.py`).

2. **Real-Time Anomaly Detection using Isolation Forest**:
   - Ensembles Isolation Forest, PCA Reconstruction Error, and Rolling Z-Score bounds to isolate normal baseline vs anomaly state in real time.

3. **Automated Root-Cause Chain Tracing (Not Just Alerts)**:
   - Constructs a Directed Acyclic Graph (DAG) using Granger causality & Time-Lagged Cross-Correlation to map out the exact propagation chain ($A \rightarrow B \rightarrow C$).

4. **Actionable Recommendations Alongside Diagnosis**:
   - Generates plain-English XAI summaries, prescriptive action steps, and copyable bash/kubectl/SQL CLI runbook commands.

5. **Fully Offline, On-Premises Dashboard (Streamlit + Plotly)**:
   - Running locally at `http://127.0.0.1:8501`. Zero cloud calls, zero external API keys needed, 100% on-premises secure.

---

## 🛠️ Codebase Structure

```
neuralX/
├── app.py                            # Streamlit Interactive Web Application
├── requirements.txt                  # Dependencies configuration
├── WALKTHROUGH.md                    # System Walkthrough & Feature Guide
├── IMPLEMENTATION_PLAN.md            # Technical Architecture Plan
├── src/
│   ├── __init__.py
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── anomaly_detector.py       # Isolation Forest + PCA SVD + Z-Score Anomaly Detector
│   │   ├── causal_analyzer.py        # TLCC + Granger OLS Causality + Feature Attribution
│   │   ├── data_loader.py            # Telemetry Ingestion & Preprocessing Manager
│   │   ├── explanation_generator.py  # XAI Natural Language & Remediation Runbook Generator
│   │   ├── root_cause_ranker.py      # Causal DAG Builder & Root Cause vs Symptom Ranker
│   │   └── synthetic_generator.py    # ESP32-C3 & Enterprise Telemetry Generator
│   └── hardware/
│       └── esp32_bridge.py           # ESP32-C3 Live Serial Bridge & Firmware Sketch
└── tests/
    └── test_engine.py                # Automated Unit & Integration Test Suite
```

---

## 🧪 Automated Test Verification

All 6 unit and integration tests pass cleanly with **100% success**:

```bash
python -m pytest tests/test_engine.py
```

```text
============================= test session starts =============================
platform win32 -- Python 3.14.6, pytest-9.1.1
collected 6 items

tests\test_engine.py ......                                              [100%]

============================== 6 passed in 4.72s ==============================
```

---

## 🌐 Live Web Application

- **Primary URL (IPv4):** [http://127.0.0.1:8501](http://127.0.0.1:8501)
- **Alternative URL:** [http://localhost:8501](http://localhost:8501)
