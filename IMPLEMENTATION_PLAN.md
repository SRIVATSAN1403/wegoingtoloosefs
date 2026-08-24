## Phase 1 & 2: Edge Hardware and Data Pipeline
* Flash the ESP32-C3 Super Mini with C++ firmware so it actively generates live sensor telemetry, specifically capturing Fan RPM, Temperature, and CPU Load[cite: 1].
* Establish the local USB connection targeting COM15 to ensure completely offline, cloud-free data transmission[cite: 1].
* Implement the Python PySerial ingestion script to seamlessly read raw bytes into a rolling 60-second Pandas dataframe, keeping memory usage stable during spikes[cite: 1].

## Phase 3: AI Detection and Causal Engine
* Integrate scikit-learn's Isolation Forest algorithm to continuously scan the rolling dataframe buffer, flagging anomalies instantly as they occur[cite: 1].
* Develop the custom Python causal engine to execute lagged correlation and threshold-sequence tracking backward through the data[cite: 1].
* Rigorously test the engine's capability to pinpoint the exact root cause of hardware failures rather than simply triggering an alert storm[cite: 1].

## Phase 4: Dashboard Visualization
* Build the fully offline presentation layer using Streamlit and Plotly to guarantee zero cloud dependency[cite: 1].
* Design the dark-themed UI to render live data feeds, highlight instant alerts, and clearly map out the automated root-cause chain for the user[cite: 1].

## Phase 5: Final Polish and Pitch Preparation
* Finalize the "NEURAL X PPT PRESENTATION.pptx" slide deck, maintaining the exact template constraints with no extra slides added[cite: 1].
* Verify that all team branding, including the "Build Beyond Boundaries" tagline, is properly aligned for the judges[cite: 1].
* To visually demonstrate the physical hardware layer to the judges, create a 3D model of the ESP32-C3 setup with moveable components in Tinkercad, utilizing the same workflow designed for the dual-axis solar panel client presentation.