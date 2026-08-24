"""
PyroTrace Visualizations
Implements Steep Editorial Light Design System Plotly Charts
"""

from typing import List, Dict, Any
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Steep Tokens — Light Theme Palette
COLOR_INK_BLACK = "#17191c"
COLOR_PAPER_WHITE = "#ffffff"
COLOR_MIST_GRAY = "#f2f2f3"
COLOR_SLATE_GRAY = "#777b86"
COLOR_ASH_GRAY = "#979799"
COLOR_BLUSH_PEACH = "#fbe1d1"
COLOR_SIENNA_BROWN = "#5d2a1a"
COLOR_HAIRLINE = "#ececec"


def create_gauge_chart(value: float, min_val: float, max_val: float, title: str, unit: str, stroke_color: str = COLOR_INK_BLACK) -> go.Figure:
    """Create a minimal Steep editorial indicator gauge chart."""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={'suffix': f" {unit}", 'font': {'size': 22, 'color': COLOR_INK_BLACK, 'family': "'Inter', sans-serif"}},
        title={'text': title, 'font': {'size': 13, 'color': COLOR_SLATE_GRAY, 'family': "'Inter', sans-serif"}},
        gauge={
            'axis': {'range': [min_val, max_val], 'tickwidth': 1, 'tickcolor': COLOR_ASH_GRAY},
            'bar': {'color': stroke_color, 'thickness': 0.35},
            'bgcolor': COLOR_MIST_GRAY,
            'bordercolor': COLOR_HAIRLINE,
            'steps': [
                {'range': [min_val, max_val], 'color': COLOR_MIST_GRAY}
            ],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=15, r=15, t=25, b=15),
        height=130
    )
    return fig


def create_telemetry_chart(df: pd.DataFrame) -> go.Figure:
    """Create multi-axis live line chart for Temperature, Fan RPM, and CPU Load matching Steep design tokens."""
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        subplot_titles=("Temperature (°C)", "Fan Speed (RPM)", "CPU Load (%)")
    )

    if df.empty:
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor=COLOR_PAPER_WHITE,
            font=dict(color=COLOR_INK_BLACK)
        )
        return fig

    x_data = df["datetime"] if "datetime" in df.columns else df["timestamp"]

    # 1. Temperature Subplot (Sienna Brown)
    fig.add_trace(
        go.Scatter(
            x=x_data, y=df["temp"],
            mode="lines",
            name="Temperature (°C)",
            line=dict(color=COLOR_SIENNA_BROWN, width=2.2),
            hovertemplate="%{y:.1f} °C"
        ),
        row=1, col=1
    )

    # 2. Fan RPM Subplot (Ink Black)
    fig.add_trace(
        go.Scatter(
            x=x_data, y=df["rpm"],
            mode="lines",
            name="Fan RPM",
            line=dict(color=COLOR_INK_BLACK, width=2.2),
            hovertemplate="%{y} RPM"
        ),
        row=2, col=1
    )

    # 3. CPU Load Subplot (Slate Gray)
    fig.add_trace(
        go.Scatter(
            x=x_data, y=df["cpu_load"],
            mode="lines",
            name="CPU Load (%)",
            line=dict(color=COLOR_SLATE_GRAY, width=2.2),
            hovertemplate="%{y:.1f} %"
        ),
        row=3, col=1
    )

    # Highlight Anomalies with Blush Peach / Sienna markers
    if "is_anomaly" in df.columns and df["is_anomaly"].any():
        anom_df = df[df["is_anomaly"]]
        anom_x = anom_df["datetime"] if "datetime" in anom_df.columns else anom_df["timestamp"]

        fig.add_trace(
            go.Scatter(
                x=anom_x, y=anom_df["temp"],
                mode="markers",
                name="Anomaly Breach",
                marker=dict(color=COLOR_SIENNA_BROWN, size=9, symbol="diamond", line=dict(color=COLOR_BLUSH_PEACH, width=2)),
                showlegend=True
            ),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=anom_x, y=anom_df["rpm"],
                mode="markers",
                name="Anomaly Breach",
                marker=dict(color=COLOR_SIENNA_BROWN, size=9, symbol="diamond", line=dict(color=COLOR_BLUSH_PEACH, width=2)),
                showlegend=False
            ),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(
                x=anom_x, y=anom_df["cpu_load"],
                mode="markers",
                name="Anomaly Breach",
                marker=dict(color=COLOR_SIENNA_BROWN, size=9, symbol="diamond", line=dict(color=COLOR_BLUSH_PEACH, width=2)),
                showlegend=False
            ),
            row=3, col=1
        )

    # Layout Styling - Light Paper Canvas
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=COLOR_PAPER_WHITE,
        font=dict(color=COLOR_INK_BLACK, family="'Inter', sans-serif"),
        height=480,
        margin=dict(l=35, r=35, t=35, b=25),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.03,
            xanchor="right",
            x=1
        )
    )

    # Subtle Gridlines
    for r in [1, 2, 3]:
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_MIST_GRAY, row=r, col=1)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor=COLOR_MIST_GRAY, row=r, col=1)

    return fig


def create_causal_flow_chart(chain: List[Dict[str, Any]]) -> go.Figure:
    """Create a horizontal step flow visualization matching Steep editorial card aesthetics."""
    fig = go.Figure()

    if not chain:
        fig.add_annotation(
            text="No active causal chain. System operating in nominal baseline state.",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14, color=COLOR_SLATE_GRAY, family="'Inter', sans-serif")
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=140
        )
        return fig

    n_nodes = len(chain)
    x_coords = list(range(n_nodes))
    y_coords = [0] * n_nodes

    node_colors = []
    node_hover = []

    for i, node in enumerate(chain):
        node_hover.append(f"{node['metric']}: {node['state']}<br>{node['detail']}")
        if i == 0:
            node_colors.append(COLOR_SIENNA_BROWN)  # Origin (Sienna Brown)
        else:
            node_colors.append(COLOR_INK_BLACK)     # Propagation (Ink Black)

    # Connect lines
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode="lines",
        line=dict(color=COLOR_ASH_GRAY, width=2, dash="dot"),
        hoverinfo="none",
        showlegend=False
    ))

    # Node pill markers
    fig.add_trace(go.Scatter(
        x=x_coords, y=y_coords,
        mode="markers+text",
        marker=dict(size=38, color=node_colors, line=dict(color=COLOR_PAPER_WHITE, width=2)),
        text=[f"S{node['step']}" for node in chain],
        textposition="middle center",
        textfont=dict(color=COLOR_PAPER_WHITE, size=13, family="'Inter', sans-serif", weight=500),
        hoverinfo="text",
        hovertext=node_hover,
        showlegend=False
    ))

    # Text annotations below nodes
    for i, node in enumerate(chain):
        fig.add_annotation(
            x=i, y=-0.35,
            text=f"<b>{node['metric']}</b><br><span style='color:#777b86'>{node['state']}</span>",
            showarrow=False,
            font=dict(size=12, color=COLOR_INK_BLACK, family="'Inter', sans-serif")
        )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.5, n_nodes - 0.5]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.8, 0.5]),
        margin=dict(l=15, r=15, t=15, b=15),
        height=170
    )

    return fig
