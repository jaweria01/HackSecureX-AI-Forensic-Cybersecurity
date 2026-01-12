import pandas as pd
from datetime import datetime
from sklearn.ensemble import IsolationForest


class ForensicAnalyzer:
    def __init__(self):
        # ML model for anomaly detection
        self.model = IsolationForest(
            n_estimators=100,
            contamination=0.1,
            random_state=42
        )

    def parse_logs(self, file_path):
        """
        Parses log file into structured events
        """
        records = []

        with open(file_path, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 3)
                if len(parts) < 4:
                    continue

                date, time, level, message = parts
                timestamp = datetime.strptime(
                    f"{date} {time}", "%Y-%m-%d %H:%M:%S"
                )

                records.append({
                    "timestamp": timestamp,
                    "level": level,
                    "message_length": len(message)
                })

        return pd.DataFrame(records)

    def detect_anomalies(self, df):
        """
        Detects anomalous log events using ML
        """
        # Convert severity to numeric
        severity_map = {"INFO": 0, "WARNING": 1, "ERROR": 2}
        df["severity"] = df["level"].map(severity_map)

        features = df[["severity", "message_length"]]

        df["anomaly"] = self.model.fit_predict(features)

        return df

    def reconstruct_timeline(self, df):
        """
        Returns sorted forensic timeline
        """
        return df.sort_values("timestamp")
