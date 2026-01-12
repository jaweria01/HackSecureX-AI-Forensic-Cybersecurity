
import sys
import os

# Absolute path to integrity folder
INTEGRITY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "integrity"
)

sys.path.insert(0, INTEGRITY_PATH)

from integrity_manager import IntegrityManager

# Initialize integrity manager
manager = IntegrityManager()

# Path to sample log file
file_path = "data/sample_logs.txt"

print("🔒 Locking evidence...")
original_hash = manager.lock_evidence(file_path)
print(f"Original Hash: {original_hash}\n")

print("🔍 Verifying integrity (before any change)...")
status, message = manager.verify_integrity(file_path)
print(message, "\n")

print("⚠️ Simulating tampering (modifying the file)...")
with open(file_path, "a") as f:
    f.write("\n2026-01-10 04:00:00 ERROR Unauthorized access detected")

print("🔍 Verifying integrity (after tampering)...")
status, message = manager.verify_integrity(file_path)
print(message)
