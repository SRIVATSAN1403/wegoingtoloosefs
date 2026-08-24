# PyroTrace: System Architecture

## Overview
PyroTrace is an edge-native, locally-processed AI diagnostic system designed to trace physical hardware failures back to their root cause in real time. It operates entirely offline without cloud dependencies, bridging the gap between IT monitoring and Operational Technology (OT) telemetry.

---

## System Components

### 1. Hardware & Edge Layer
*   **Microcontroller:** ESP32-C3 Super Mini[cite: 1].
*   **Function:** Generates and collects live sensor telemetry, including Fan RPM, Temperature, and CPU Load[cite: 1].
*   **Firmware:** Written in C++ to package telemetry data into JSON format and stream it directly over a local USB connection[cite: 1].

### 2. Data Ingestion Layer
*   **Connection Protocol:** Serial communication via USB (Targeting COM15)[cite: 1].
*   **Processor:** Python `PySerial` library reads the raw byte stream[cite: 1].
*   **Memory Management:** Data is fed into a rolling 60-second `Pandas` dataframe buffer[cite: 1]. This keeps memory utilization flat and prevents lag or system crashes during high-frequency data spikes.

### 3. AI & Analytics Layer
*   **Anomaly Detection:** Utilizes the `Isolation Forest` algorithm via `scikit-learn`[cite: 1]. It continuously scans the 60-second rolling buffer in real time to instantly flag hardware deviations[cite: 1].
*   **Causal Tracing Engine:** A custom Python logic sequence utilizing time-lagged correlation and threshold-sequence tracking[cite: 1]. Instead of just outputting an alert, it steps backward through the time-series data to link cascading failures back to the initial trigger event[cite: 1].

### 4. Presentation & Visualization Layer
*   **Framework:** Streamlit[cite: 1].
*   **Visualization:** Plotly integration for live-updating, interactive charts[cite: 1].
*   **UI/UX:** A dark-themed, locally-hosted dashboard that renders live data, anomaly alerts, and the final automated root-cause diagnostic chain[cite: 1].

---

## Architecture Flow Diagram

```mermaid
graph TD
    subgraph Hardware Layer
        A[ESP32-C3 Super Mini] -->|Sensors: Temp, RPM, CPU| B(JSON over USB)
    end

    subgraph Data Ingestion Layer
        B -->|COM15| C(Python: PySerial)
        C --> D[(Rolling 60s Pandas Dataframe)]
    end

    subgraph AI & Causal Engine
        D --> E{Scikit-learn: Isolation Forest}
        E -->|Anomalies Detected| F[Custom Causal Engine]
        F -->|Lagged Correlation Tracing| G[Root Cause Identified]
    end

    subgraph Presentation Layer
        G --> H[Streamlit + Plotly Dashboard]
        D -->|Live Data Feed| H
    end