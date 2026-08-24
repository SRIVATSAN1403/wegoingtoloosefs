# PyroTrace Project Folder Structure

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
│   ├── app.py                  # Streamlit application file (dark-themed UI)
│   ├── visualizations.py       # Plotly charts for live data and causal chain rendering
│   └── assets/                 # Custom CSS, logos, or icons
│       └── style.css
│
├── docs/                       # Project documentation
│   ├── architecture.md         # System flow and component breakdown
│   └── folder_structure.md     # Directory specifications
│
├── work_logs/                  # Completed phase reports
│   └── PHASE_1_AND_2_COMPLETION.md
│
├── .gitignore                  # Ignores virtual environments, cache, and local logs
├── requirements.txt            # Python dependencies
└── README.md                   # Setup instructions and project overview
```
