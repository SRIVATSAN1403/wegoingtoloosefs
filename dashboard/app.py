"""
PyroTrace Streamlit Dashboard Application
"The AI that finds the frayed wire, not just the fire."
Edge-Native Anomaly Detection & Causal Root Cause Analyzer.
"""

import sys
import os
import time
import pandas as pd
import streamlit as st

# Add project root directory to path to enable package imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion import SerialIngestor
from src.anomaly_detection import AnomalyDetector
from src.causal_tracing import CausalEngine
from dashboard.visualizations import (
    create_telemetry_chart,
    create_gauge_chart,
    create_causal_flow_chart
)

# Page Setup
st.set_page_config(
    page_title="PyroTrace | Edge AI Root Cause Analyzer",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Dark Theme Styling
st.markdown("""
    <style>
        /* Base Canvas & Fonts */
        .stApp {
            background-color: #0e1117;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }

        /* Metric Cards */
        div[data-testid="metric-container"] {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 14px 18px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        div[data-testid="metric-container"] label {
            color: #8b949e !important;
            font-size: 14px !important;
            font-weight: 500;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #f0f6fc !important;
            font-size: 26px !important;
            font-weight: 600;
        }

        /* Diagnostic Panel Card */
        .diag-card {
            background-color: #161b22;
            border: 1px solid #30363d;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .diag-card-critical {
            background-color: #1c1214;
            border: 1px solid #f85149;
            border-radius: 14px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .status-badge-ok {
            background-color: rgba(46, 160, 67, 0.2);
            color: #3fb950;
            border: 1px solid #2ea043;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 13px;
        }
        .status-badge-alert {
            background-color: rgba(248, 81, 73, 0.2);
            color: #f85149;
            border: 1px solid #f85149;
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 13px;
        }
        
        /* Action Box */
        .action-box {
            background-color: #1f242c;
            border-left: 4px solid #58a6ff;
            border-radius: 6px;
            padding: 12px 16px;
            margin-top: 10px;
            color: #e6edf3;
            font-size: 14px;
        }

        /* Sidebar Customization */
        section[data-testid="stSidebar"] {
            background-color: #161b22;
            border-right: 1px solid #30363d;
        }
    </style>
""", unsafe_allow_html=True)


# Initialize Session State & Background Services
if "ingestor" not in st.session_state:
    ingestor = SerialIngestor(port="COM15", window_seconds=60)
    ingestor.start()
    st.session_state["ingestor"] = ingestor
else:
    ingestor = st.session_state["ingestor"]

if "detector" not in st.session_state:
    st.session_state["detector"] = AnomalyDetector(contamination=0.08)

if "causal_engine" not in st.session_state:
    st.session_state["causal_engine"] = CausalEngine()


# Sidebar Controls
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/fire-element.png", width=60)
    st.title("PyroTrace Control")
    st.caption("Edge-Native AI Investigator")
    st.markdown("---")

    # Connection Status Indicator
    hw_connected = ingestor.is_hardware_connected()
    if hw_connected:
        st.markdown('<span class="status-badge-ok">🟢 COM15 HARDWARE CONNECTED</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge-ok">⚡ EDGE SIMULATION FALLBACK</span>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Physical / Synthetic Demo Controls")
    st.write("Inject simulated hardware faults to test the AI Causal Engine in real time:")

    fault_option = st.radio(
        "Select Hardware Operational State:",
        options=[
            "0: Normal Baseline",
            "1: Thermal Spike (Heatsink Detachment)",
            "2: Fan Bearing Failure (RPM Drop)",
            "3: Runaway CPU Load Surge"
        ],
        index=0
    )

    # Update fault mode
    selected_mode = int(fault_option.split(":")[0])
    ingestor.set_fault_mode(selected_mode)

    st.markdown("---")
    auto_refresh = st.checkbox("Auto-Refresh Dashboard (1s)", value=True)
    if st.button("Refresh Stream Manual"):
        st.rerun()

    st.markdown("---")
    st.caption("Neural X | Build Beyond Boundaries")


# Top Header Banner
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("PyroTrace Diagnostic Panel")
    st.markdown("*\"The AI that finds the frayed wire, not just the fire.\"*")

with col_head2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Target Transport: **USB COM15 (115200 Baud)**")
    st.caption("Buffer Window: **60s Rolling Memory**")


# Fetch Latest Telemetry Buffer & Process AI Analytics
df_buffer = ingestor.get_buffer()

# Run Anomaly Detection (Isolation Forest)
detector = st.session_state["detector"]
df_analyzed = detector.fit_predict(df_buffer)

# Run Causal Engine Analysis
causal_engine = st.session_state["causal_engine"]
causal_result = causal_engine.analyze_root_cause(df_analyzed)

# Metric KPI Cards Row
latest_sample = ingestor.get_latest_sample()
temp_val = latest_sample.get("temp", 35.0) if latest_sample else 35.0
rpm_val = latest_sample.get("rpm", 3200) if latest_sample else 3200
cpu_val = latest_sample.get("cpu_load", 25.0) if latest_sample else 25.0

col_m1, col_m2, col_m3, col_m4 = st.columns(4)
with col_m1:
    st.metric("Temperature", f"{temp_val:.1f} °C", delta=f"{temp_val - 35.0:.1f} °C" if abs(temp_val - 35.0) > 0.5 else None)
with col_m2:
    st.metric("Fan Speed", f"{int(rpm_val)} RPM", delta=f"{int(rpm_val - 3200)} RPM" if abs(rpm_val - 3200) > 50 else None)
with col_m3:
    st.metric("CPU Load", f"{cpu_val:.1f} %", delta=f"{cpu_val - 25.0:.1f} %" if abs(cpu_val - 25.0) > 2.0 else None)
with col_m4:
    if causal_result["has_anomaly"]:
        st.markdown(f'''
            <div style="background-color:#2c1517; border:1px solid #f85149; border-radius:12px; padding:12px; text-align:center;">
                <span style="color:#f85149; font-weight:bold; font-size:14px;">⚠️ SYSTEM ANOMALY</span><br>
                <span style="color:#ffffff; font-size:18px; font-weight:600;">{causal_result["root_cause_metric"].upper() if causal_result["root_cause_metric"] else "FAULT"}</span>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div style="background-color:#13231b; border:1px solid #2ea043; border-radius:12px; padding:12px; text-align:center;">
                <span style="color:#3fb950; font-weight:bold; font-size:14px;">STATUS NOMINAL</span><br>
                <span style="color:#ffffff; font-size:18px; font-weight:600;">ALL SYSTEMS OK</span>
            </div>
        ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# Main Content Layout: 2 Columns (Telemetry Feeds vs Root Cause Diagnostics)
col_left, col_right = st.columns([1.5, 1.0])

with col_left:
    st.subheader("📈 Live Sensor Telemetry (Rolling 60s)")
    fig_telemetry = create_telemetry_chart(df_analyzed)
    st.plotly_chart(fig_telemetry, use_container_width=True)

with col_right:
    st.subheader("🔍 AI Root Cause Diagnostics")
    
    if causal_result["has_anomaly"]:
        st.markdown(f'''
            <div class="diag-card-critical">
                <h4 style="color:#f85149; margin-top:0;">🚨 {causal_result["root_cause_title"]}</h4>
                <p style="color:#8b949e; font-size:13px;">Diagnostic Confidence: <b>{causal_result["confidence"]*100:.1f}%</b></p>
                <hr style="border-color:#30363d;">
                <p><b>Propagated Failure Sequence:</b></p>
            </div>
        ''', unsafe_allow_html=True)

        # Causal Chain Visualization
        fig_causal = create_causal_flow_chart(causal_result["propagation_chain"])
        st.plotly_chart(fig_causal, use_container_width=True)

        # Prescriptive Recommendation
        st.markdown(f'''
            <div class="action-box">
                <b>🛠️ Prescriptive Recommendation:</b><br>
                {causal_result["recommended_action"]}
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div class="diag-card">
                <h4 style="color:#3fb950; margin-top:0;">✅ All Systems Nominal</h4>
                <p style="color:#8b949e; font-size:13px;">Isolation Forest score stable | Zero threshold breaches</p>
                <p style="font-size:14px; color:#c9d1d9;">
                    The telemetry stream is balanced. Microcontroller inputs, fan speed tachometer, and thermal dissipation levels are operating within continuous baseline limits.
                </p>
            </div>
        ''', unsafe_allow_html=True)

        # Render nominal gauges
        g_col1, g_col2, g_col3 = st.columns(3)
        with g_col1:
            st.plotly_chart(create_gauge_chart(temp_val, 20, 100, "Temp", "°C", "#ff7b72"), use_container_width=True)
        with g_col2:
            st.plotly_chart(create_gauge_chart(rpm_val, 0, 5000, "Fan Speed", "RPM", "#58a6ff"), use_container_width=True)
        with g_col3:
            st.plotly_chart(create_gauge_chart(cpu_val, 0, 100, "CPU Load", "%", "#d2a8ff"), use_container_width=True)


# Auto-refresh loop
if auto_refresh:
    time.sleep(1.0)
    st.rerun()
