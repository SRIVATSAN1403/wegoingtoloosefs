"""
PyroTrace Streamlit Dashboard
"The AI that finds the frayed wire, not just the fire."
Designed according to the Steep Editorial Light Design System (design.md).
"""

import sys
import os
import time
import pandas as pd
import streamlit as st

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.ingestion import SerialIngestor
from src.anomaly_detection import AnomalyDetector
from src.causal_tracing import CausalEngine
from dashboard.visualizations import (
    create_telemetry_chart,
    create_gauge_chart,
    create_causal_flow_chart
)

# Page Setup - Light Theme Editorial Layout
st.set_page_config(
    page_title="PyroTrace | Edge AI Investigator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Steep Editorial Design Tokens & Styling
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;1,8..60,400&family=Inter:wght@400;450;500;600&display=swap');

        /* Steep Color Tokens */
        :root {
            --color-ink-black: #17191c;
            --color-paper-white: #ffffff;
            --color-mist-gray: #f2f2f3;
            --color-slate-gray: #777b86;
            --color-ash-gray: #979799;
            --color-blush-peach: #fbe1d1;
            --color-sienna-brown: #5d2a1a;
            --color-hairline: #ececec;
        }

        /* Page Canvas */
        .stApp {
            background-color: #ffffff !important;
            color: #17191c !important;
            font-family: 'Inter', sans-serif !important;
        }

        /* Headers - Serif Signifier Style */
        h1, h2, h3, .serif-heading {
            font-family: 'Source Serif 4', Georgia, serif !important;
            font-weight: 400 !important;
            color: #17191c !important;
            letter-spacing: -0.66px !important;
        }

        /* Subhead Muted Text */
        .subhead-text {
            color: #777b86;
            font-size: 17px;
            font-weight: 400;
            line-height: 1.4;
            margin-bottom: 24px;
        }

        /* Metric Cards - Floating White Artifacts */
        div[data-testid="metric-container"] {
            background-color: #ffffff !important;
            border: 1px solid #ececec !important;
            border-radius: 20px !important;
            padding: 16px 20px !important;
            box-shadow: 0 0 0 1px rgba(4, 23, 43, 0.05), 0 20px 25px -5px rgba(0, 0, 0, 0.06) !important;
        }
        div[data-testid="metric-container"] label {
            color: #979799 !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #17191c !important;
            font-size: 24px !important;
            font-weight: 500 !important;
        }

        /* Neutral Mist Gray Card */
        .neutral-card {
            background-color: #f2f2f3;
            border-radius: 24px;
            padding: 24px;
            margin-bottom: 20px;
        }

        /* Accent Blush Peach Card */
        .accent-peach-card {
            background-color: #fbe1d1;
            color: #5d2a1a !important;
            border-radius: 24px;
            padding: 28px;
            margin-bottom: 20px;
        }
        .accent-peach-card h3, .accent-peach-card h4 {
            color: #5d2a1a !important;
            font-family: 'Source Serif 4', Georgia, serif !important;
            font-weight: 400 !important;
            margin-top: 0;
        }

        /* Floating Product Artifact Surface */
        .artifact-card {
            background-color: #ffffff;
            border-radius: 24px;
            border: 1px solid #ececec;
            box-shadow: 0 0 0 1px rgba(4,23,43,0.05), 0 20px 25px -5px rgba(0,0,0,0.08), 0 8px 10px -6px rgba(0,0,0,0.04);
            padding: 24px;
            margin-bottom: 20px;
        }

        /* Category Label */
        .category-tag {
            color: #979799;
            font-size: 14px;
            font-weight: 400;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
        }

        /* Pill Buttons */
        .pill-badge {
            background-color: #17191c;
            color: #ffffff !important;
            border-radius: 9999px;
            padding: 6px 16px;
            font-size: 13px;
            font-weight: 400;
            display: inline-block;
        }
        .pill-badge-ghost {
            background-color: transparent;
            color: #17191c !important;
            border: 1px solid #17191c;
            border-radius: 9999px;
            padding: 6px 16px;
            font-size: 13px;
            font-weight: 400;
            display: inline-block;
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {
            background-color: #fafafb !important;
            border-right: 1px solid #ececec !important;
        }
    </style>
""", unsafe_allow_html=True)


# Initialize Ingestion & AI Engine Services
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
    st.markdown('<div class="category-tag">SYSTEM SETUP</div>', unsafe_allow_html=True)
    st.title("PyroTrace")
    st.caption("Edge-Native AI Investigator")
    st.markdown("---")

    # Connection Status Pill Badges
    hw_connected = ingestor.is_hardware_connected()
    if hw_connected:
        st.markdown('<span class="pill-badge">COM15 Hardware Live</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="pill-badge-ghost">Edge Simulation Active</span>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="category-tag">SIMULATION & DEMO</div>', unsafe_allow_html=True)
    st.write("Inject simulated physical fault vectors to test real-time causal tracing:")

    fault_option = st.radio(
        "Select Operational Mode:",
        options=[
            "0: Normal Baseline",
            "1: Thermal Spike (Heatsink Detachment)",
            "2: Fan Bearing Failure (RPM Drop)",
            "3: Runaway CPU Load Surge"
        ],
        index=0
    )

    selected_mode = int(fault_option.split(":")[0])
    ingestor.set_fault_mode(selected_mode)

    st.markdown("---")
    auto_refresh = st.checkbox("Auto-Refresh (1s)", value=True)
    if st.button("Refresh Stream"):
        st.rerun()

    st.markdown("---")
    st.caption("Steep Editorial Design System | Neural X")


# Hero Header Section
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.markdown('<div class="category-tag">HARDWARE TELEMETRY & CAUSAL INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown("<h1>PyroTrace Edge Investigator</h1>", unsafe_allow_html=True)
    st.markdown('<div class="subhead-text">The AI that finds the frayed wire, not just the fire. Operating 100% offline over USB COM15.</div>', unsafe_allow_html=True)

with col_head2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<span class="pill-badge">Air-Gapped Processing</span>', unsafe_allow_html=True)
    st.markdown('<span class="pill-badge-ghost">60s Rolling Window</span>', unsafe_allow_html=True)


# Fetch Data & Run AI Engine
df_buffer = ingestor.get_buffer()
detector = st.session_state["detector"]
df_analyzed = detector.fit_predict(df_buffer)

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
            <div style="background-color:#fbe1d1; border-radius:20px; padding:14px 18px; text-align:center;">
                <span style="color:#5d2a1a; font-weight:600; font-size:12px; text-transform:uppercase;">Anomaly Flagged</span><br>
                <span style="color:#5d2a1a; font-size:20px; font-weight:600; font-family:'Source Serif 4', Georgia, serif;">{causal_result["root_cause_metric"].upper() if causal_result["root_cause_metric"] else "ALERT"}</span>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('''
            <div style="background-color:#f2f2f3; border-radius:20px; padding:14px 18px; text-align:center;">
                <span style="color:#979799; font-weight:600; font-size:12px; text-transform:uppercase;">Status</span><br>
                <span style="color:#17191c; font-size:20px; font-weight:500;">Nominal Baseline</span>
            </div>
        ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# Main Grid Layout (2 Columns)
col_left, col_right = st.columns([1.5, 1.0])

with col_left:
    st.markdown('<div class="artifact-card">', unsafe_allow_html=True)
    st.markdown('<div class="category-tag">REAL-TIME FEEDS</div>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top:0;">Live Telemetry & Outlier Overlays</h3>', unsafe_allow_html=True)
    fig_telemetry = create_telemetry_chart(df_analyzed)
    st.plotly_chart(fig_telemetry, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    if causal_result["has_anomaly"]:
        st.markdown(f'''
            <div class="accent-peach-card">
                <div style="color:#5d2a1a; font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">ROOT CAUSE DIAGNOSTIC</div>
                <h3 style="margin-top:4px; margin-bottom:8px; color:#5d2a1a;">{causal_result["root_cause_title"]}</h3>
                <p style="color:#5d2a1a; font-size:14px; margin-bottom:16px;">Confidence: <b>{causal_result["confidence"]*100:.1f}%</b></p>
                <hr style="border-color:rgba(93,42,26,0.2);">
                <p style="font-weight:500; color:#5d2a1a;">Cascading Propagation Sequence:</p>
            </div>
        ''', unsafe_allow_html=True)

        # Horizontal Causal Chain Graph
        st.markdown('<div class="artifact-card">', unsafe_allow_html=True)
        fig_causal = create_causal_flow_chart(causal_result["propagation_chain"])
        st.plotly_chart(fig_causal, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Prescriptive Recommendation Card
        st.markdown(f'''
            <div class="neutral-card">
                <div class="category-tag">RECOMMENDED ACTION</div>
                <p style="color:#17191c; font-size:15px; line-height:1.5;">
                    <b>{causal_result["recommended_action"]}</b>
                </p>
            </div>
        ''', unsafe_allow_html=True)

    else:
        st.markdown('''
            <div class="neutral-card">
                <div class="category-tag">DIAGNOSTIC ANALYSIS</div>
                <h3 style="margin-top:4px;">All Systems Nominal</h3>
                <p style="color:#777b86; font-size:15px; line-height:1.5;">
                    Sensors are within baseline bounds. Continuous Isolation Forest scoring confirms balanced thermal dissipation and steady fan tachometer readings.
                </p>
            </div>
        ''', unsafe_allow_html=True)

        # Nominal Indicator Gauges
        st.markdown('<div class="artifact-card">', unsafe_allow_html=True)
        st.markdown('<div class="category-tag">HARDWARE GAUGES</div>', unsafe_allow_html=True)
        g_col1, g_col2, g_col3 = st.columns(3)
        with g_col1:
            st.plotly_chart(create_gauge_chart(temp_val, 20, 100, "Temperature", "°C", "#5d2a1a"), use_container_width=True)
        with g_col2:
            st.plotly_chart(create_gauge_chart(rpm_val, 0, 5000, "Fan Speed", "RPM", "#17191c"), use_container_width=True)
        with g_col3:
            st.plotly_chart(create_gauge_chart(cpu_val, 0, 100, "CPU Load", "%", "#777b86"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# Auto-refresh loop
if auto_refresh:
    time.sleep(1.0)
    st.rerun()
