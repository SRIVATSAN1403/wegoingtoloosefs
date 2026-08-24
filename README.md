# PyroTrace

**"The AI that finds the frayed wire, not just the fire."**

PyroTrace is an edge-native, locally-processed AI diagnostic system designed to trace physical hardware failures back to their root cause in real time. It operates entirely offline without cloud dependencies, bridging the gap between IT monitoring and Operational Technology (OT) telemetry.

---

## Key Features

- **Edge-Native Processing**: 100% offline, zero cloud overhead, target COM15 serial streaming from an ESP32-C3 Super Mini.
- **Real-Time Data Pipeline**: PySerial ingestion with a 60-second rolling Pandas DataFrame buffer.
- **AI Failure Investigation**: Isolation Forest anomaly detection + time-lagged causal tracing engine.
- **Dark-Themed Dashboard**: Built with Streamlit and Plotly for real-time diagnostic visualization.

---

## Directory Overview

```text
pyrotrace/
├── firmware/         # C++ Firmware for ESP32-C3 Super Mini
├── src/              # PySerial ingestion, Isolation Forest, and Causal Engine
├── dashboard/        # Streamlit + Plotly frontend dashboard
├── docs/             # Architecture and folder specs
├── work_logs/        # Completed milestone reports
└── requirements.txt  # Project dependencies
```

---

## Getting Started

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Test data ingestion**:
   ```bash
   python src/ingestion.py
   ```

3. **Launch Streamlit Dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```
