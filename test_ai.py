import sys
import os

# Add ML path
ML_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "ml"
)
sys.path.insert(0, ML_PATH)

from forensic_analyzer import ForensicAnalyzer

file_path = "data/sample_logs.txt"

analyzer = ForensicAnalyzer()

df = analyzer.parse_logs(file_path)
df = analyzer.detect_anomalies(df)
timeline = analyzer.reconstruct_timeline(df)

print("\n🔍 Forensic Timeline:")
print(timeline[["timestamp", "level", "anomaly"]])
