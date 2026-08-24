"""
PyroTrace Anomaly Detection Module
Scikit-Learn Isolation Forest implementation for real-time sensor anomaly detection.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import logging

logger = logging.getLogger("PyroTrace.AnomalyDetector")


class AnomalyDetector:
    """
    Scikit-Learn Isolation Forest Anomaly Detector.
    Scans the 60-second rolling telemetry buffer to identify hardware anomalies.
    """

    def __init__(self, contamination: float = 0.08, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.feature_cols = ["temp", "rpm", "cpu_load"]
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=self.random_state,
            n_estimators=100
        )
        self._is_fitted = False

    def fit_predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Fits the Isolation Forest on available telemetry buffer data and predicts anomaly scores.
        
        Returns:
            DataFrame with added columns:
            - 'anomaly_score': float (negative = anomalous, positive = normal)
            - 'is_anomaly': bool (True if anomalous, False if normal)
        """
        if df.empty or len(df) < 5:
            # Not enough data points yet for reliable fit
            df_result = df.copy()
            df_result["anomaly_score"] = 0.0
            df_result["is_anomaly"] = False
            return df_result

        df_result = df.copy()
        
        # Ensure target features exist
        valid_cols = [c for c in self.feature_cols if c in df_result.columns]
        if len(valid_cols) < len(self.feature_cols):
            df_result["anomaly_score"] = 0.0
            df_result["is_anomaly"] = False
            return df_result

        X = df_result[valid_cols].values

        try:
            # Fit and predict
            predictions = self.model.fit_predict(X)
            scores = self.model.decision_function(X)

            df_result["anomaly_score"] = scores
            # predictions: -1 for outlier/anomaly, 1 for normal
            df_result["is_anomaly"] = predictions == -1

            # Rule-based threshold safety override for physical sensor bounds
            latest = df_result.iloc[-1]
            if latest["temp"] > 80.0 or latest["rpm"] < 800 or latest["cpu_load"] > 95.0:
                df_result.loc[df_result.index[-1], "is_anomaly"] = True

        except Exception as e:
            logger.error(f"Error during anomaly detection fit_predict: {e}")
            df_result["anomaly_score"] = 0.0
            df_result["is_anomaly"] = False

        return df_result


# Quick module verification
if __name__ == "__main__":
    print("Testing PyroTrace Anomaly Detector...")
    sample_data = {
        "timestamp": list(range(10)),
        "temp": [35.0, 35.2, 35.1, 35.3, 35.0, 35.4, 75.0, 88.0, 92.0, 95.0],
        "rpm": [3200, 3190, 3210, 3205, 3195, 3200, 1200, 800, 500, 400],
        "cpu_load": [25.0, 24.8, 25.2, 25.1, 25.0, 25.3, 90.0, 98.0, 99.0, 100.0]
    }
    df = pd.DataFrame(sample_data)
    detector = AnomalyDetector()
    res = detector.fit_predict(df)
    print(res[["temp", "rpm", "cpu_load", "anomaly_score", "is_anomaly"]])
