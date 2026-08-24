"""
PyroTrace Plotly Visualizations
Generates charts for live telemetry feeds, indicator gauges, and causal propagation graphs.
"""

from typing import List, Dict, Any
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Dark Theme Color Palette
COLOR_BG = "#0e1117"
COLOR_CARD = "#161b22"
COLOR_TEXT = "#f0f6fc"
COLOR_TEXT_MUTED = "#8b949e"
COLOR_TEMP = "#ff7b72"     # Coral/Red
COLOR_RPM = "#58a6ff"      # Cyan/Blue
COLOR_CPU = "#d2a8ff"      # Purple/Violet
COLOR_ANOMALY = "#f85149"  # Crimson Highlight


def create_gauge_chart(value: float, min_val: float, max_val: float, title: str, unit: str, color: str) -> go.Figure:
    """Create a dark-themed sleek Plotly indicator gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': f" {unit}", 'font': {'size': 24, 'color': COLOR_TEXT, 'family': "sans-serif"}},
        title={'text': title, 'font': {'size': 15, 'color': COLOR_TEXT_MUTED}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': COLOR_TEXT_MUTED},
            'bar': {'color': color, 'thickness': 0.3},
            'bgcolor': COLOR_CARD,
            'bordercolor': "#30363d",
            'steps': [
                {'range': [min_val, max_val], 'color': "#21262d"}
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=30, b=20),
        height=140
    )
    return fig


def create_telemetry_chart(df: pd.DataFrame) -> go.Figure:
    """Create multi-axis live line chart for Temperature, Fan RPM, and CPU Load with anomaly markers."""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Temperature (°C)", "Fan Speed (RPM)", "CPU Load (%)")
    )

    if df.empty:
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor=COLOR_CARD,
            font=dict(color=COLOR_TEXT)
        )
        return fig

    # X-axis time representation
    x_data = df["datetime"] if "datetime" in df.columns else df["timestamp"]

    # 1. Temperature Subplot
    fig.add_trace(
        go.Scatter(
            x=x_data, y=df["temp"],
            mode="lines",
            name="Temperature (°C)",
            line=dict(color=COLOR_TEMP, width=2.5),
            hovertemplate="%{y:.1f} °C"
        ),
        row=1, col=1
    )

    # 2. Fan RPM Subplot
    fig.add_trace(
        go.Scatter(
            x=x_data, y=df["rpm"],
            mode="lines",
            name="Fan RPM",
            line=dict(color=COLOR_RPM, width=2.5),
            hovertemplate="%{y} RPM"
        ),
        row=2, col=1
    )

    # 3. CPU Load Subplot
    fig.add_trace(
        go.Scatter(
            x=x_data, y=df["cpu_load"],
            mode="lines",
            name="CPU Load (%)",
            line=dict(color=COLOR_CPU, width=2.5),
            hovertemplate="%{y:.1f} %"
        ),
        row=3, col=1
    )

    # Highlight Anomalies
    if "is_anomaly" in df.columns and df["is_anomaly"].any():
        anom_df = df[df["is_anomaly"]]
        anom_x = anom_df["datetime"] if "datetime" in anom_df.columns else anom_df["timestamp"]

        fig.add_trace(
            go.Scatter(
                x=anom_x, y=anom_df["temp"],
                mode="markers",
                name="Anomaly Detected",
                marker=dict(color=COLOR_ANOMALY, size=10, symbol="x"),
                showlegend=True
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=anom_x, y=anom_df["rpm"],
                mode="markers",
                name="Anomaly Detected",
                marker=dict(color=COLOR_ANOMALY, size=10, symbol="x"),
                showlegend=False
            ),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=anom_x, y=anom_df["cpu_load"],
                mode="markers",
                name="Anomaly Detected",
                marker=dict(color=COLOR_ANOMALY, size=10, symbol="x"),
                showlegend=False
            ),
            row=3, col=1
        )

    # Layout Styling
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=COLOR_CARD,
        font=dict(color=COLOR_TEXT, family="sans-serif"),
        height=480,
        margin=dict(l=40, r=40, t=40, b=30),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Gridlines and styling
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#21262d", row=1, col=1)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#21262d", row=2, col=1)
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor="#21262d", row=3, col=1)

    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#21262d", row=1, col=1)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#21262d", row=2, col=1)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor="#21262d", row=3, col=1)

    return fig


def create_causal_flow_chart(chain: List[Dict[str, Any]]) -> go.Figure:
    """Create a horizontal step flow visualization for the root cause propagation chain."""
    fig = go.Figure()

    if not chain:
        fig.add_annotation(
            text="No active causal chain. System in nominal state.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color=COLOR_TEXT_MUTED)
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor=COLOR_CARD,
            height=150
        )
        return fig

    n_nodes = len(chain)
    x_coords = list(range(n_nodes))
    y_coords = [0] * n_nodes

    # Node Labels & Colors
    node_text = []
    node_hover = []
    node_colors = []

    for i, node in enumerate(chain):
        label = f"<b>Step {node['step']}</b><br>{node['metric']}<br><i>({node['lag']})</i>"
        node_text.append(label)
        node_hover.append(f"{node['metric']}: {node['state']}<br>{node['detail']}")
        
        # Color root vs intermediate vs final
        if i == 0:
            node_colors.append("#ff7b72") # Origin (Red)
        elif i == n_nodes - 1:
            node_colors.append("#f85149") # Impact (Crimson)
        else:
            node_colors.append("#d2a8ff") # Propagation (Purple)

    # Add connect lines (arrows)
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode="lines",
        line=dict(color="#58a6ff", width=3, dash="solid"),
        hoverinfo="none",
        showlegend=False
    ))

    # Add Node markers
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode="markers+text",
        marker=dict(size=44, color=node_colors, line=dict(color=COLOR_TEXT, width=2)),
        text=[f"S{node['step']}" for node in chain],
        textposition="middle center",
        textfont=dict(color="#ffffff", size=14, family="sans-serif"),
        hoverinfo="text",
        hovertext=node_hover,
        showlegend=False
    ))

    # Add text annotations below nodes
    for i, node in enumerate(chain):
        fig.add_annotation(
            x=i, y=-0.35,
            text=f"<b>{node['metric']}</b><br><span style='color:#8b949e'>{node['state']}</span>",
            showarrow=False,
            font=dict(size=12, color=COLOR_TEXT)
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, n_nodes - 0.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.8, 0.5]),
        margin=dict(l=20, r=20, t=20, b=20),
        height=180
    )

    return fig
