# Implementation Plan - AI-04: AI Anomaly Root-Cause Analyzer

Develop an end-to-end AI system (`neuralX`) that detects abnormal events from historical multivariate telemetry/time-series data, investigates variable relationships via causal discovery and explainable AI (XAI), and builds a probable root-cause chain distinguishing upstream root causes from downstream symptoms.

## Core Capabilities & Architecture

1. **Live Sensor Monitoring via ESP32-C3**: Supports physical ESP32-C3 hardware telemetry (RPM, Temperature, CPU Load, Voltage, Interrupt Lag).
2. **Real-time Anomaly Detection using Isolation Forest**: Multi-algorithm detector combining Isolation Forest, PCA Reconstruction Error, and Z-Score bounds.
3. **Automated Root-Cause Chain Tracing**: Builds Directed Acyclic Graphs (DAG) via Granger causality and Time-Lagged Cross Correlation.
4. **Actionable Recommendations**: Prescriptive remediation action steps and copyable CLI runbook commands (`kubectl`, `psql`, `kafka-consumer-groups.sh`).
5. **Fully Offline, On-Premises Dashboard**: Streamlit + Plotly interactive UI running on `http://127.0.0.1:8501` with zero cloud dependency.
