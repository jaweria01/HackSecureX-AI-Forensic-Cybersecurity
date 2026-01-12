from forensic_pipeline import ForensicPipeline

pipeline = ForensicPipeline()
file_path = "data/sample_logs.txt"

timeline, status, message = pipeline.analyze_evidence(file_path)

print("\n📊 Final Forensic Timeline:")
print(timeline[["timestamp", "level", "anomaly"]])

print("\n🔐 Integrity Check Result:")
print(message)
