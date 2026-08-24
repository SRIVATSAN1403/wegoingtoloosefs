PYROTRACE (formerly neuralx)
"The AI that finds the frayed wire, not just the fire."

what??
Most AI acts like a smoke detector. It looks at historical data, notices a spike or a drop, and says "Hey, something is wrong!" (This is Anomaly Detection). But a smoke detector doesn't tell you how the fire started.

Our system is the fire investigator. When an anomaly happens, it looks at all the surrounding data and works backward to figure out the chain of events.

The Symptom: The server crashed (the smoke).
The Root Cause Chain: A new code update went live -> It caused a memory leak -> RAM usage hit 100% -> The server crashed (the frayed wire that started the fire).

The system looks at a mess of data and draws that exact arrow-by-arrow map, proving the actual root cause instead of just flagging the symptom.

HOW IT ACTUALLY TRACES THE CHAIN (the mechanism, not just the story)
This is a lightweight causal engine built from lagged correlation + domain rules -- not full Bayesian causal inference (that's Phase 3, see below). Two techniques:
- Time-lagged cross-correlation: for each anomaly, scan backward through the rolling 60-second buffer and rank which prior metric deviations precede it most consistently, and with the tightest lag.
- Threshold-crossing sequence detection: if Temperature crosses its z-score threshold 8 seconds before RPM does, Temperature is upstream in the causal chain.
Being upfront that this is simplified-but-legitimate (vs. "true" causal AI) is a feature, not a weakness -- it's honest about what's achievable at this scale today, with a clear upgrade path.

who??
IT & DevOps / Site Reliability Engineers: a website goes down. Instead of 5 engineers spending 4 hours digging through server logs, the AI instantly points to a faulty database query.

sell points:
* Reduces MTTR (Mean Time to Resolution): 80% of incident time is spent finding the problem, 20% fixing it. This eliminates the 80% search time.
* Turns Junior Staff into Experts: normally only a senior engineer with 10 years of experience can trace a complex failure. This gives every junior engineer the diagnostic power of an expert.
* Actionable, not just diagnostic: alongside the root-cause trace, output a simple rule-based recommendation (e.g. "Root cause: fan RPM drop -> Recommended action: check fan bearing/power connector"). Small build lift, big credibility boost -- turns "we found it" into "here's what to do."

flow
+--------------------------+
|  ESP32-C3 Super Mini     |  (Outputs JSON via Serial)
+------------+-------------+
             | USB Cable
             v
+------------+-------------+
|  COM15 Port               |
+------------+-------------+
             |
             v
+------------+-------------+
|  PySerial (Background)   |  (Reads raw bytes into Dataframe)
+------------+-------------+
             |
             v
+------------+-------------+
|  Streamlit App (Frontend) |  (Renders UI + Runs AI RCA Engine)
+--------------------------+

what are we going to build:
Python + Streamlit + Dark Theme CSS for maximum speed and lowest risk. Looks like professional industrial software (think SpaceX/Datadog control panel).

competitive landscape (one line each):
1. Dynatrace (Davis AI) -- cloud-scale vs. our edge-scale. Dynatrace maps dependencies across massive cloud architectures (Kubernetes, AWS) and costs millions; we're lightweight and localized for Edge hardware/IoT.
2. Datadog (Watchdog AI) -- cloud-dependent vs. our air-gapped. Datadog sends data to a centralized cloud; we run entirely locally, keeping sensitive telemetry (factory machine metrics) on-premises.
3. BigPanda -- software ticketing (ITSM) vs. our physical hardware. BigPanda correlates alert floods for IT service tickets; we do real-time physical machine diagnostics.

[NOTE: verify the "costs millions" / competitor pricing claims against a public source (e.g. G2, Gartner) before using in a pitch -- soften to "industry reports suggest" if no direct citation.]

what is the innovation:
1. "Edge-Native" Processing (Zero Cloud Required)
   Status Quo: Datadog and Dynatrace require uploading terabytes of sensitive machine data to external cloud servers.
   Innovation: Runs entirely locally. ESP32-C3 streams data directly over COM15 to a local machine. For highly secure environments (government data centers, defense, power plants), data never leaves the building -- maximum security, zero latency.

2. Bridging IT to OT (Operational Technology)
   Status Quo: Existing tools monitor software (Kubernetes, AWS, API calls, code errors).
   Innovation: Monitoring physical physics (motors, temperature, voltages) -- bringing enterprise-grade causal AI to the factory floor. Not just why a website crashed, but why a physical machine is about to fail.

3. The Ultra-Low-Cost Diagnostic Engine
   Status Quo: Enterprise observability tools cost hundreds of thousands per year and need dedicated engineering teams.
   Innovation: An ESP32-C3 microcontroller and a lightweight Python dashboard give any small-to-medium factory an automated "AI Investigator" for pennies.

tech stack:
1. Hardware & Edge Layer
   - Microcontroller: ESP32-C3 Super Mini
   - Firmware: C++ generating simulated sensor telemetry (Fan RPM, Temperature, CPU Load)
   - Payload Format: Lightweight JSON string transmission

2. Data Ingestion (The Pipeline)
   - Transport: Direct USB connection via COM15, zero-latency offline data transfer
   - Buffer Engine: Python pyserial + pandas managing a rolling 60-second time-series dataframe

3. AI & Analytics Engine
   - Anomaly Detection (The Alarm): scikit-learn Isolation Forest for real-time threshold breaches
   - Root Cause Tracer (The Investigator): custom Python causal logic (lagged cross-correlation + threshold-sequence detection) analyzing the time-lagged buffer to pinpoint the originating failure event

4. Frontend Dashboard
   - Framework: Streamlit (100% Python UI, no separate frontend/API layer)
   - Visualizations: Plotly, dark-themed, live-updating

demo plan (lead with this, not the slides):
1. Show the live dashboard in normal operating state.
2. Physically induce a fault (block the fan, heat the sensor) -- trigger a real anomaly, not simulated data.
3. Watch the RCA engine trace it backward on screen in real time, ending in a recommended action.
Live hardware + live fault is rare at this level and is the single most persuasive part of the pitch -- open with it.

future scope and impact:
1. Real-World Impact
   - Reduces MTTR by up to 80% (industry estimate -- cite source, e.g. downtime-cost studies from Uptime Institute/Gartner, if used in a pitch)
   - Downtime in data centers/manufacturing can cost well into six figures per hour; catching a fan failure 15 seconds before thermal shutdown saves real money
   - 100% on-premises data security -- compliant with strict industrial/defense standards
   - Zero cloud overhead -- no monthly observability subscription

2. Future Scope
   Phase 1: Wireless Sensor Mesh (LoRaWAN / ESP-NOW) -- expand from one ESP32 node to a decentralized mesh across a factory floor or data center row.
   Phase 2: Closed-Loop Automated Remediation -- move from passive reporting to active intervention (auto-engage backup cooling, throttle server power) before hardware fails.
   Phase 3: Causal Knowledge Graphs -- upgrade the RCA engine with Bayesian Causal Networks to learn complex multi-variable dependencies across thousands of nodes without manual rule configuration.

conclusion:
1. The Problem: hardware downtime costs industrial and data center sectors billions annually. Existing tools only alert you after the fire starts.
2. The Solution: an Edge-Native, AI-powered Root Cause Analysis engine, built on an ultra-low-cost ESP32 microcontroller and a lightweight Python/Streamlit architecture.
3. The Value: Speed (up to 80% MTTR reduction), Security (100% localized processing, zero cloud upload), Accessibility (enterprise-level diagnostic AI on the factory floor at a fraction of the cost).