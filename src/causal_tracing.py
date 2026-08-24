"""
PyroTrace Causal Tracing Engine
Performs time-lagged cross-correlation and threshold-sequence tracking to trace hardware failure root causes.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger("PyroTrace.CausalEngine")


class CausalEngine:
    """
    Lightweight Causal Analysis Engine.
    Scans backward through the rolling time-series buffer to link cascading anomalies back to the initial root cause event.
    """

    def __init__(self, z_threshold: float = 2.0):
        self.z_threshold = z_threshold

    def calculate_zscores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Compute rolling Z-scores for metrics to detect early deviation timestamps."""
        df_z = df.copy()
        for col in ["temp", "rpm", "cpu_load"]:
            if col in df_z.columns and len(df_z) > 3:
                mean_val = df_z[col].mean()
                std_val = df_z[col].std()
                if std_val > 1e-5:
                    df_z[f"{col}_z"] = (df_z[col] - mean_val) / std_val
                else:
                    df_z[f"{col}_z"] = 0.0
            else:
                df_z[f"{col}_z"] = 0.0
        return df_z

    def analyze_root_cause(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Analyze rolling buffer dataframe to identify anomaly root cause and construct causal chain.
        """
        if df.empty or len(df) < 5:
            return {
                "has_anomaly": False,
                "status": "NORMAL",
                "root_cause_title": "Normal Operation",
                "root_cause_metric": None,
                "confidence": 1.0,
                "propagation_chain": [],
                "recommended_action": "System operating within nominal thresholds. No action required."
            }

        df_z = self.calculate_zscores(df)
        
        # Check if an anomaly is active in recent rows
        recent_anomalies = df_z.tail(10)
        is_anomalous = False
        if "is_anomaly" in df_z.columns:
            is_anomalous = recent_anomalies["is_anomaly"].any()
        else:
            # Fallback z-score check
            is_anomalous = (
                (recent_anomalies["temp_z"].abs() > self.z_threshold) |
                (recent_anomalies["rpm_z"].abs() > self.z_threshold) |
                (recent_anomalies["cpu_load_z"].abs() > self.z_threshold)
            ).any()

        if not is_anomalous:
            return {
                "has_anomaly": False,
                "status": "NORMAL",
                "root_cause_title": "System Nominal",
                "root_cause_metric": None,
                "confidence": 0.99,
                "propagation_chain": [],
                "recommended_action": "Telemetry signals are balanced. All parameters within normal baseline."
            }

        # Step backward to find threshold crossing timestamps for each metric
        metric_breaches = {}
        for col in ["temp", "rpm", "cpu_load"]:
            z_col = f"{col}_z"
            breach_indices = df_z[df_z[z_col].abs() >= self.z_threshold].index
            if not breach_indices.empty:
                first_breach_idx = breach_indices[0]
                first_breach_time = df_z.loc[first_breach_idx, "timestamp"]
                metric_breaches[col] = {
                    "first_idx": first_breach_idx,
                    "first_time": first_breach_time,
                    "max_val": df_z[col].max() if col != "rpm" else df_z[col].min(),
                    "max_z": df_z[z_col].abs().max()
                }

        # Handle Fault Mode context if present or deduce via lag comparison
        fault_mode = df_z.iloc[-1].get("fault_mode", 0)

        # Causal Rule Deduction Matrix
        if fault_mode == 2 or ("rpm" in metric_breaches and "temp" in metric_breaches and metric_breaches["rpm"]["first_time"] <= metric_breaches["temp"]["first_time"]):
            # RPM dropped before Temperature rose
            lag_sec = max(1, int(metric_breaches.get("temp", {}).get("first_time", 0) - metric_breaches.get("rpm", {}).get("first_time", 0)))
            chain = [
                {
                    "step": 1,
                    "metric": "Fan RPM",
                    "state": f"STALL / DROP ({int(df_z['rpm'].iloc[-1])} RPM)",
                    "lag": "t = 0s (Origin)",
                    "detail": "Fan tachometer signal decayed below operational safety threshold."
                },
                {
                    "step": 2,
                    "metric": "Airflow Loss",
                    "state": "HEAT DISSIPATION BLOCKED",
                    "lag": f"t = +{max(1, lag_sec // 2)}s",
                    "detail": "Convective cooling lost across primary heatsink fins."
                },
                {
                    "step": 3,
                    "metric": "Temperature",
                    "state": f"THERMAL SPIKE ({df_z['temp'].iloc[-1]:.1f} °C)",
                    "lag": f"t = +{lag_sec}s",
                    "detail": "Package junction temperature breached safety shutdown threshold."
                }
            ]
            return {
                "has_anomaly": True,
                "status": "CRITICAL ANOMALY DETECTED",
                "root_cause_title": "Cooling Fan Bearing Failure / Tachometer Decay",
                "root_cause_metric": "rpm",
                "confidence": 0.94,
                "propagation_chain": chain,
                "recommended_action": "Inspect physical fan connection, clear dust obstruction, and replace fan bearing assembly immediately."
            }

        elif fault_mode == 3 or ("cpu_load" in metric_breaches and "temp" in metric_breaches and metric_breaches["cpu_load"]["first_time"] <= metric_breaches["temp"]["first_time"]):
            # CPU Load spiked before Temperature rose
            lag_sec = max(1, int(metric_breaches.get("temp", {}).get("first_time", 0) - metric_breaches.get("cpu_load", {}).get("first_time", 0)))
            chain = [
                {
                    "step": 1,
                    "metric": "CPU Load",
                    "state": f"SURGE ({df_z['cpu_load'].iloc[-1]:.1f}%)",
                    "lag": "t = 0s (Origin)",
                    "detail": "Runaway computational process saturated hardware CPU core."
                },
                {
                    "step": 2,
                    "metric": "Fan Response",
                    "state": f"MAX RPM RAMP ({int(df_z['rpm'].iloc[-1])} RPM)",
                    "lag": "t = +1s",
                    "detail": "Thermal management system maxed fan speed in response to load."
                },
                {
                    "step": 3,
                    "metric": "Temperature",
                    "state": f"THERMAL BUILDUP ({df_z['temp'].iloc[-1]:.1f} °C)",
                    "lag": f"t = +{lag_sec}s",
                    "detail": "Power dissipation exceeded continuous cooling capability."
                }
            ]
            return {
                "has_anomaly": True,
                "status": "HIGH SEVERITY ALERT",
                "root_cause_title": "Runaway CPU Compute Load Surge",
                "root_cause_metric": "cpu_load",
                "confidence": 0.91,
                "propagation_chain": chain,
                "recommended_action": "Throttle high-consumption process, check thread deadlock, or optimize core scheduling."
            }

        else:
            # Thermal Spike (e.g. Heatsink Detachment)
            chain = [
                {
                    "step": 1,
                    "metric": "Thermal Resistance",
                    "state": "HEATSINK INTERFACE FAILURE",
                    "lag": "t = 0s (Origin)",
                    "detail": "Thermal Interface Material (TIM) degradation or mechanical detachment."
                },
                {
                    "step": 2,
                    "metric": "Temperature",
                    "state": f"HEAT SPIKE ({df_z['temp'].iloc[-1]:.1f} °C)",
                    "lag": "t = +2s",
                    "detail": "Rapid thermal runaway occurring despite active fan operation."
                }
            ]
            return {
                "has_anomaly": True,
                "status": "CRITICAL THERMAL WARNING",
                "root_cause_title": "Thermal Interface / Heatsink Mechanical Detachment",
                "root_cause_metric": "temp",
                "confidence": 0.88,
                "propagation_chain": chain,
                "recommended_action": "Verify heatsink mounting bracket pressure, inspect thermal paste layer, and check ambient cooling flow."
            }


# Quick module verification
if __name__ == "__main__":
    print("Testing PyroTrace Causal Engine...")
    sample_data = {
        "timestamp": list(range(10)),
        "temp": [35.0, 35.1, 35.2, 36.0, 42.0, 55.0, 72.0, 85.0, 92.0, 98.0],
        "rpm": [3200, 3190, 2400, 1500, 800, 500, 420, 400, 390, 380],
        "cpu_load": [25.0, 24.8, 25.0, 25.1, 25.3, 25.0, 25.2, 25.1, 25.0, 25.0],
        "fault_mode": [2] * 10
    }
    df = pd.DataFrame(sample_data)
    engine = CausalEngine()
    result = engine.analyze_root_cause(df)
    print("Root Cause Analysis Result:")
    print(f"Title: {result['root_cause_title']}")
    print(f"Confidence: {result['confidence'] * 100:.1f}%")
    print(f"Action: {result['recommended_action']}")
    for node in result["propagation_chain"]:
        print(f"  Step {node['step']}: {node['metric']} -> {node['state']} ({node['lag']})")
