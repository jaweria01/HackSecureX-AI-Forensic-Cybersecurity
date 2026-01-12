import os
import sys

# Add integrity and ml paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, "integrity"))
sys.path.insert(0, os.path.join(BASE_DIR, "ml"))

from integrity_manager import IntegrityManager
from forensic_analyzer import ForensicAnalyzer


class ForensicPipeline:
    def __init__(self):
        self.integrity = IntegrityManager()
        self.analyzer = ForensicAnalyzer()

    def analyze_evidence(self, file_path):
        print("🔒 Locking evidence...")
        original_hash = self.integrity.lock_evidence(file_path)

        print("🤖 Running AI forensic analysis...")
        df = self.analyzer.parse_logs(file_path)
        df = self.analyzer.detect_anomalies(df)
        timeline = self.analyzer.reconstruct_timeline(df)

        # Log AI analysis event
        self.integrity.log_event(
            os.path.basename(file_path),
            original_hash,
            "AI_ANALYSIS_PERFORMED"
        )

        print("🔍 Verifying evidence integrity after AI analysis...")
        status, message = self.integrity.verify_integrity(file_path)

        return timeline, status, message
