"""
neuralX — Enterprise AI Root-Cause Intelligence & On-Premises Hardware Telemetry Platform
Supports Live ESP32-C3 Sensor Monitoring (RPM, Temp, CPU Load), Isolation Forest, Causal Graph Tracing, and Offline Dashboard.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
import json
import os
import time
import streamlit.components.v1 as components
from pyvis.network import Network

from src.engine.data_loader import DataLoader
from src.engine.anomaly_detector import AnomalyDetector
from src.engine.causal_analyzer import CausalAnalyzer
from src.engine.root_cause_ranker import RootCauseRanker
from src.engine.explanation_generator import IncidentExplanationGenerator
from src.hardware.esp32_bridge import ESP32HardwareBridge

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="neuralX | ESP32-C3 & Enterprise RCA Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }

    .saas-top-bar {
        background: #111827;
        border-bottom: 1px solid #1f2937;
        padding: 0.8rem 1.5rem;
        margin: -4rem -4rem 1.5rem -4rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .brand-logo {
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .org-badge {
        background: #1e293b;
        border: 1px solid #334155;
        color: #94a3b8;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 500;
    }

    .status-offline-secure {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        color: #34d399;
        padding: 4px 12px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 700;
    }

    .datadog-card {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 10px;
        padding: 1.1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        transition: border-color 0.2s ease;
    }

    .datadog-card-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.06em;
    }

    .datadog-card-value {
        font-size: 1.7rem;
        font-weight: 800;
        margin-top: 0.3rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .feature-chip {
        background: #1e293b;
        color: #38bdf8;
        border: 1px solid #334155;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 600;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Top SaaS Navigation Bar
# ---------------------------------------------------------
st.markdown("""
<div class="saas-top-bar">
    <div style="display: flex; align-items: center; gap: 15px;">
        <span class="brand-logo">⚡ neuralX</span>
        <span class="org-badge">📡 Hardware: ESP32-C3 Microcontroller</span>
        <span class="org-badge">🔒 Architecture: 100% Offline / On-Premises</span>
    </div>
    <div>
        <span class="status-offline-secure">🛡️ ZERO CLOUD DEPENDENCY (OFFLINE SECURE)</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Controls & Data Mode
# ---------------------------------------------------------
st.sidebar.markdown("### ⚙️ Hardware & Telemetry Mode")

data_mode = st.sidebar.radio(
    "Data Source Mode",
    ["📡 ESP32-C3 Live Hardware Sensor (RPM, Temp, CPU Load)", "🖥️ Production APM Infrastructure Benchmark", "📂 Upload Custom Telemetry CSV"],
    index=0
)

data_loader = DataLoader()
df = None
time_col = None
feature_cols = []
scenario_name = "ESP32-C3 Sensor Stream"

if data_mode == "📡 ESP32-C3 Live Hardware Sensor (RPM, Temp, CPU Load)":
    scenario_key = "esp32_c3_sensor"
    scenario_name = "ESP32-C3 Microcontroller Sensor Mesh"
    df_raw = data_loader.get_preset_scenario(scenario_key, length=400)
    df, time_col, feature_cols = data_loader.process_dataframe(df_raw, "timestamp")

elif data_mode == "🖥️ Production APM Infrastructure Benchmark":
    scenario_choice = st.sidebar.selectbox(
        "Select Enterprise Scenario",
        [
            "☸️ AWS EKS Kubernetes Cluster (Pod Memory Leak ➔ Service Timeout ➔ 5xx)",
            "🐘 PostgreSQL Enterprise DB (Active Conn Saturation ➔ Lock Wait ➔ 504)",
            "📦 Apache Kafka Event Stream (Broker Disk I/O Saturation ➔ Lag Spike ➔ DLQ)"
        ]
    )
    if "Kubernetes" in scenario_choice:
        scenario_key = "k8s_mesh"
        scenario_name = "AWS EKS Kubernetes Cluster"
    elif "PostgreSQL" in scenario_choice:
        scenario_key = "postgres_db"
        scenario_name = "PostgreSQL Enterprise Database"
    else:
        scenario_key = "kafka_pipeline"
        scenario_name = "Apache Kafka Pipeline"

    df_raw = data_loader.get_preset_scenario(scenario_key, length=400)
    df, time_col, feature_cols = data_loader.process_dataframe(df_raw, "timestamp")

else:
    uploaded_file = st.sidebar.file_uploader("Upload Telemetry CSV", type=["csv"])
    if uploaded_file is not None:
        df, time_col, feature_cols = data_loader.load_from_csv(uploaded_file)
        scenario_name = uploaded_file.name
    else:
        st.warning("⚠️ Please upload a CSV file or select ESP32-C3 Sensor mode.")
        st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎛️ Isolation Forest Tuning")
contamination = st.sidebar.slider("Isolation Forest Contamination Rate", 0.05, 0.40, 0.25, 0.01)
corr_thresh = st.sidebar.slider("Causal Correlation Threshold", 0.10, 0.80, 0.35, 0.05)

# ---------------------------------------------------------
# Core Analytics Pipeline
# ---------------------------------------------------------
detector = AnomalyDetector(contamination=contamination)
causal_analyzer = CausalAnalyzer(max_lag=12)
ranker = RootCauseRanker(p_val_threshold=0.05, corr_threshold=corr_thresh)
explanation_gen = IncidentExplanationGenerator()

anomaly_results = detector.detect_anomalies(df, time_col, feature_cols)
is_anomaly = anomaly_results["is_anomaly"]
onset_timestamp = anomaly_results["onset_timestamp"]

tlcc_results = causal_analyzer.compute_tlcc(df, feature_cols, max_lag=12)
granger_p_matrix = causal_analyzer.compute_granger_causality(df, feature_cols, max_lag=3)
feature_importances = causal_analyzer.compute_feature_attribution(df, feature_cols, is_anomaly)

G_causal, dag_meta = ranker.build_causal_dag(
    feature_cols,
    granger_p_matrix,
    tlcc_results,
    anomaly_results["feature_onsets"]
)

df_rankings = ranker.rank_root_causes(
    G_causal,
    feature_cols,
    anomaly_results["feature_onsets"],
    feature_importances
)

causal_chain = ranker.extract_root_cause_chain(G_causal, df_rankings)

incident_report = explanation_gen.generate_incident_report(
    scenario_name,
    onset_timestamp,
    df_rankings,
    causal_chain,
    anomaly_results
)

# ---------------------------------------------------------
# High-Impact Value Proposition Banner
# ---------------------------------------------------------
st.markdown("""
<div style="background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 0.9rem 1.2rem; margin-bottom: 1.2rem;">
    <span class="feature-chip">⚡ Live ESP32-C3 Monitoring (RPM, Temp, CPU)</span>
    <span class="feature-chip">🌲 Real-Time Isolation Forest Anomaly Detection</span>
    <span class="feature-chip">🔗 Automated Causal DAG Chain Tracing</span>
    <span class="feature-chip">💡 Actionable Diagnostic Recommendations</span>
    <span class="feature-chip">🛡️ 100% Offline On-Premises Streamlit + Plotly</span>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# KPI Metric Cards
# ---------------------------------------------------------
top_cause_row = df_rankings.iloc[0] if not df_rankings.empty else None
top_cause_name = top_cause_row["metric"] if top_cause_row is not None else "N/A"
confidence_score = top_cause_row["root_cause_score"] if top_cause_row is not None else 0
n_symptoms = len(df_rankings[df_rankings["category"] == "DOWNSTREAM SYMPTOM"])

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="datadog-card" style="border-top: 3px solid #ef4444;">
        <div class="datadog-card-title">PRIMARY ROOT CAUSE</div>
        <div class="datadog-card-value" style="color: #ef4444;">{top_cause_name}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="datadog-card" style="border-top: 3px solid #38bdf8;">
        <div class="datadog-card-title">RCA CONFIDENCE SCORE</div>
        <div class="datadog-card-value" style="color: #38bdf8;">{confidence_score}%</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="datadog-card" style="border-top: 3px solid #fbbf24;">
        <div class="datadog-card-title">ANOMALY ONSET TIME</div>
        <div class="datadog-card-value" style="color: #fbbf24; font-size: 1.3rem;">{onset_timestamp}</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="datadog-card" style="border-top: 3px solid #a78bfa;">
        <div class="datadog-card-title">CASCADING SYMPTOMS</div>
        <div class="datadog-card-value" style="color: #a78bfa;">{n_symptoms} Metrics</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Enterprise Dashboard Tabs
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📡 Live Sensor Telemetry (RPM/Temp/CPU)",
    "🕸️ Automated Causal Chain Tracing (DAG)",
    "💡 Actionable Diagnosis & Remediation",
    "⚖️ Root Cause Ranking Matrix",
    "🔌 ESP32-C3 Firmware & Serial Bridge"
])

# ---------------------------------------------------------
# TAB 1: Live Sensor Telemetry
# ---------------------------------------------------------
with tab1:
    st.markdown("### 📊 Real-Time Telemetry Stream (ESP32-C3 Sensor Metrics)")
    
    selected_metrics = st.multiselect(
        "Select Telemetry Overlay Metrics",
        options=feature_cols,
        default=feature_cols[:min(4, len(feature_cols))]
    )

    fig_timeline = go.Figure()

    anomaly_indices = np.where(is_anomaly)[0]
    if len(anomaly_indices) > 0:
        anom_start = df[time_col].iloc[anomaly_indices[0]]
        anom_end = df[time_col].iloc[anomaly_indices[-1]]
        fig_timeline.add_vrect(
            x0=anom_start, x1=anom_end,
            fillcolor="rgba(239, 68, 68, 0.15)",
            layer="below", line_width=0,
            annotation_text="ISOLATION FOREST ANOMALY WINDOW", annotation_position="top left",
            annotation_font=dict(color="#ef4444", size=11)
        )

    for metric in selected_metrics:
        vals = df[metric].values
        vals_norm = (vals - vals.min()) / (vals.max() - vals.min() + 1e-8)
        
        is_root = (metric == top_cause_name)
        line_color = "#ef4444" if is_root else None
        line_width = 3.2 if is_root else 1.8
        name_label = f"🔴 {metric} (ROOT CAUSE)" if is_root else metric

        fig_timeline.add_trace(go.Scatter(
            x=df[time_col],
            y=vals_norm,
            mode="lines",
            name=name_label,
            line=dict(width=line_width, color=line_color)
        ))

    fig_timeline.add_vline(
        x=onset_timestamp, line_dash="dash", line_color="#fbbf24",
        annotation_text=f"Onset T_onset: {onset_timestamp}", annotation_position="top right"
    )

    fig_timeline.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#0f172a",
        xaxis_title="Time Sequence",
        yaxis_title="Normalized Scale (0 - 1)",
        height=480,
        margin=dict(l=20, r=20, t=30, b=20)
    )

    st.plotly_chart(fig_timeline, width='stretch')

# ---------------------------------------------------------
# TAB 2: Automated Causal Chain Tracing
# ---------------------------------------------------------
with tab2:
    st.markdown("### 🕸️ Automated Root-Cause Chain Tracing (DAG Flow Map)")
    st.markdown("Traces directional fault propagation from the **Upstream Root Cause** down through **Intermediate Relays** to **Downstream Symptoms**.")

    g_col1, g_col2 = st.columns([3, 1])

    with g_col1:
        net = Network(height="540px", width="100%", bgcolor="#0f172a", font_color="#f8fafc", directed=True)
        
        for col in feature_cols:
            cat_row = df_rankings[df_rankings["metric"] == col]
            cat = cat_row.iloc[0]["category"] if not cat_row.empty else "DOWNSTREAM SYMPTOM"
            score = cat_row.iloc[0]["root_cause_score"] if not cat_row.empty else 0

            if cat == "CRITICAL ROOT CAUSE":
                color = "#ef4444"
                size = 38
                label = f"🔴 {col}\n({score}%)"
            elif cat == "INTERMEDIATE PROPAGATOR":
                color = "#f59e0b"
                size = 26
                label = f"🟠 {col}\n({score}%)"
            else:
                color = "#3b82f6"
                size = 20
                label = f"🔵 {col}\n({score}%)"

            net.add_node(col, label=label, color=color, size=size, title=f"Metric: {col}\nClass: {cat}\nScore: {score}%")

        for u, v, data in G_causal.edges(data=True):
            weight = data.get("weight", 1.0)
            lag = data.get("lag", 0)
            net.add_edge(u, v, value=max(1.5, weight*3), title=f"Directional Lag: +{lag}s\nCorrelation: {data.get('correlation', 0):.2f}")

        net.set_options("""
        var options = {
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -4500,
              "centralGravity": 0.3,
              "springLength": 130
            }
          }
        }
        """)

        os.makedirs("scratch", exist_ok=True)
        html_path = "scratch/causal_network.html"
        net.save_graph(html_path)

        with open(html_path, "r", encoding="utf-8") as f:
            html_content = f.read()
        components.html(html_content, height=560)

    with g_col2:
        st.markdown("#### 🔑 Node Tag Legend")
        st.markdown("""
        - 🔴 **CRITICAL ROOT CAUSE:** Upstream Failure Origin
        - 🟠 **PROPAGATOR:** Cascading Subsystem
        - 🔵 **SYMPTOM:** Downstream Telemetry Effect
        """)
        st.markdown("---")
        st.markdown("#### 🔗 Identified Causal Chain")
        for idx, node in enumerate(causal_chain):
            if idx == 0:
                st.markdown(f"**Step 1:** 🔴 `{node}` *(ROOT)*")
            else:
                st.markdown(f"**Step {idx+1}:** ➔ `{node}`")

# ---------------------------------------------------------
# TAB 3: Actionable Diagnosis & Remediation
# ---------------------------------------------------------
with tab3:
    st.markdown("### 💡 Actionable Recommendations Alongside Each Diagnosis")
    st.markdown("Gives junior engineers senior-level diagnostic power out of the box with prescriptive action plans.")

    st.markdown(f"#### {incident_report['headline']}")
    st.info(incident_report["summary"])

    st.markdown(incident_report["narrative"])

    st.markdown("### 🛠️ Prescriptive Action Checklist")
    for idx, act in enumerate(incident_report["action_plan"], 1):
        st.markdown(f"**Step {idx}:** {act}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 💻 Automated Remediation CLI Runbook")
    for item in incident_report.get("cli_runbook", []):
        st.markdown(f"#### 🔧 {item['title']}")
        st.code(item["command"], language="bash")

# ---------------------------------------------------------
# TAB 4: Root Cause Ranking Matrix
# ---------------------------------------------------------
with tab4:
    st.markdown("### ⚖️ Root Cause Ranking & SHAP Attribution Matrix")
    
    st.dataframe(
        df_rankings[[
            "metric", "root_cause_score", "category", "onset_time",
            "out_degree", "in_degree", "max_z_score"
        ]],
        width='stretch',
        column_config={
            "metric": "Telemetry Metric",
            "root_cause_score": st.column_config.ProgressColumn("Root Cause Score (%)", min_value=0, max_value=100, format="%.1f%%"),
            "category": "Classification",
            "onset_time": "Earliest Onset Time",
            "out_degree": "Out-Degree (Causes)",
            "in_degree": "In-Degree (Caused By)",
            "max_z_score": "Max Z-Score"
        }
    )

    st.markdown("<br>", unsafe_allow_html=True)

    fig_bar = px.bar(
        df_rankings, x="root_cause_score", y="metric", orientation="h",
        color="category",
        color_discrete_map={
            "CRITICAL ROOT CAUSE": "#ef4444",
            "INTERMEDIATE PROPAGATOR": "#f59e0b",
            "DOWNSTREAM SYMPTOM": "#3b82f6"
        },
        title="Root-Cause Probability Score Ranking"
    )
    fig_bar.update_layout(template="plotly_dark", height=380, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_bar, width='stretch')

# ---------------------------------------------------------
# TAB 5: ESP32-C3 Hardware Firmware & Serial Bridge
# ---------------------------------------------------------
with tab5:
    st.markdown("### 🔌 ESP32-C3 Hardware Firmware & Serial Bridge")
    st.markdown("Connect physical ESP32-C3 microcontrollers over USB Serial or local offline WiFi.")

    bridge = ESP32HardwareBridge()
    firmware_code = bridge.generate_esp32_c3_firmware_code()

    st.markdown("#### 📄 ESP32-C3 Arduino C++ Firmware Sketch (`esp32_c3_firmware.ino`)")
    st.code(firmware_code, language="cpp")

    st.markdown("#### 🐍 Python ESP32 Serial Reader (`src/hardware/esp32_bridge.py`)")
    st.code("""
from src.hardware.esp32_bridge import ESP32HardwareBridge

bridge = ESP32HardwareBridge(port="COM3", baudrate=115200)
sample = bridge.read_live_sample()
print("Live ESP32-C3 Telemetry Sample:", sample)
""", language="python")
