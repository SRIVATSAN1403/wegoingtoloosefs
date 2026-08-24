# PyroTrace: Project Folder Structure

This document outlines the directory structure for the PyroTrace project, separating the hardware firmware from the local Python backend and dashboard.

```text
pyrotrace/
│
├── firmware/                   # Code for the hardware layer
│   └── esp32_telemetry/
│       ├── esp32_telemetry.ino # C++ firmware for ESP32-C3 Super Mini
│       └── config.h            # Pin configurations and sensor setup
│
├── src/                        # Main Python backend and AI logic
│   ├── __init__.py
│   ├── ingestion.py            # Reads COM15 via PySerial and manages the 60s Pandas buffer
│   ├── anomaly_detection.py    # Scikit-learn Isolation Forest implementation
│   └── causal_tracing.py       # Custom Python logic for lagged correlation and root-cause tracing
│
├── dashboard/                  # Frontend UI layer
│   ├── app.py                  # Streamlit application file (dark-themed UI)[cite: 1]
│   ├── visualizations.py       # Plotly charts for live data and causal chain rendering[cite: 1]
│   └── assets/                 # Custom CSS, logos, or icons
│
├── docs/                       # Project documentation
│   ├── architecture.md         # System flow and component breakdown
│   ├── folder_structure.md     # This file
│   └── NEURAL_X_PPT.pptx       # Presentation slides[cite: 1]
│
├── .gitignore                  # Ignores virtual environments, cache, and local logs
├── requirements.txt            # Python dependencies (pandas, pyserial, scikit-learn, streamlit, plotly)
└── README.md                   # Setup instructions and project overview