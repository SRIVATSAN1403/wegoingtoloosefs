# PyroTrace System Architecture

PyroTrace is an edge-native, locally-processed AI diagnostic system designed to trace physical hardware failures back to their root cause in real time.

## Architectural Layers

1. **Hardware & Edge Layer (`firmware/`)**
   - Microcontroller: ESP32-C3 Super Mini
   - JSON Telemetry streaming over USB Serial (COM15 at 115200 baud).

2. **Data Ingestion Layer (`src/ingestion.py`)**
   - PySerial data pipeline managing a 60-second rolling Pandas DataFrame buffer.
   - Hardware serial reading with automatic local simulation fallback.

3. **AI & Causal Engine (`src/`)**
   - Isolation Forest real-time anomaly detection.
   - Time-lagged cross-correlation and threshold-sequence root cause identification.

4. **Presentation Layer (`dashboard/`)**
   - Streamlit & Plotly dark-themed interactive visualization UI.
