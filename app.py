# ===============================
# 1. IMPORTS (TOP OF FILE)
# ===============================
import streamlit as st
import os
import json
from datetime import datetime

from integrity.integrity_manager import IntegrityManager
from ml.forensic_analyzer import ForensicAnalyzer
# ===============================
# 2. CLOUD-SAFE DIRECTORIES
# ===============================
# Ensure required directories exist (Cloud-safe)
os.makedirs("integrity", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ===============================
# 3. PAGE CONFIG (BEFORE UI)
# ===============================
# Page config
st.set_page_config(
    page_title="CyberTrust – AI Forensic Cybersecurity System",
    page_icon="🛡️",
    layout="wide"
)
# ===============================
# 4. SIDEBAR (STATE FIRST)
# ===============================
# Sidebar
st.sidebar.header("🔧 Control Panel")
demo_mode = st.sidebar.toggle("🎭 Demo Mode", value=True)

uploaded_file = st.sidebar.file_uploader(
    "Upload Log Evidence",
    type=["txt", "log"]
)
#
lock_btn = st.sidebar.button("🔒 Lock Evidence")
analyze_btn = st.sidebar.button("🤖 Run AI Analysis")
verify_btn = st.sidebar.button("🔍 Verify Integrity")
view_custody_btn = st.sidebar.button("📜 View Chain of Custody")
download_report_btn = st.sidebar.button("📄 Download Forensic Report")

# ===============================
# 5. INITIALIZE MANAGERS
# ===============================
# Initialize managers
integrity = IntegrityManager()
analyzer = ForensicAnalyzer()

# ===============================
# 6. DEMO MODE RESET (RUN ONCE)
# ===============================
# Demo Mode: reset chain of custody for clean runs
if demo_mode and "demo_reset_done" not in st.session_state:
    custody_file = os.path.join("integrity", "chain_of_custody.json")
    if os.path.exists(custody_file):
        os.remove(custody_file)
    st.session_state.demo_reset_done = True

# ===============================
# 7. TITLE + MODE INDICATOR
# ===============================
# Title
st.title("🛡️ CyberTrust – AI Forensic Cybersecurity System")
if demo_mode:
    st.info("🎭 Demo Mode is ON — clean forensic session")
else:
    st.warning("🔍 Forensic Mode is ON — custody history preserved")
st.markdown(
    """
    <h3 style="margin-bottom: 0;">
        Nexora Hacks 2026 Hackathon
    </h3>
    <p style="font-size: 18px; margin-top: 4px;">
        <em>AI-driven cyber forensics with legally defensible evidence handling</em>
        <em>AI-powered digital forensics with evidence integrity and chain-of-custody</em>
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ===============================
# 8. FILE UPLOAD HANDLING
# ===============================
# Session state
if "file_path" not in st.session_state:
    st.session_state.file_path = None
if uploaded_file:
    save_path = os.path.join("data", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.session_state.file_path = save_path
    st.success("📁 Evidence file uploaded successfully.")

# Lock evidence
# ===============================
# 9. LOCK EVIDENCE
# ===============================
if lock_btn and st.session_state.file_path:
    file_hash = integrity.lock_evidence(st.session_state.file_path)
    st.success("🔒 Evidence locked successfully.")
    st.code(file_hash, language="text")

# AI analysis
# ===============================
# 10. AI FORENSIC ANALYSIS
# ===============================
if analyze_btn and st.session_state.file_path:
    st.info("🤖 Running AI forensic analysis...")
    df = analyzer.parse_logs(st.session_state.file_path)
    df = analyzer.detect_anomalies(df)
    timeline = analyzer.reconstruct_timeline(df)

    # Convert anomaly values to readable labels
    timeline["Anomaly Status"] = timeline["anomaly"].apply(
        lambda x: "🔴 Suspicious" if x == -1 else "🟢 Normal"
    )

    st.subheader("📊 Forensic Timeline")
    st.dataframe(
        timeline[["timestamp", "level", "Anomaly Status"]],
        width="stretch"
    )

    integrity.log_event(
        os.path.basename(st.session_state.file_path),
        integrity.generate_hash(st.session_state.file_path),
        "AI_ANALYSIS_PERFORMED"
    )

# Verify integrity
# ===============================
# 11. VERIFY INTEGRITY
# ===============================
if verify_btn and st.session_state.file_path:
    status, message = integrity.verify_integrity(st.session_state.file_path)
    if status:
        st.success(f"✅ {message}")
    else:
        st.error(f"❌ {message}")

st.divider()

import json

# ------------------------------
# 12. Chain of Custody Viewer
# ------------------------------
if view_custody_btn:
    custody_file = os.path.join("integrity", "chain_of_custody.json")

    st.subheader("📜 Chain of Custody Log")

    if os.path.exists(custody_file):
        with open(custody_file, "r") as f:
            custody_data = json.load(f)

        if custody_data:
            custody_df = st.dataframe(
                custody_data,
                width="stretch"
            )
        else:
            st.info("No custody records found yet.")
    else:
        st.warning("Chain of custody file not found.")

# ===============================
# 13. DOWNLOAD FORENSIC REPORT
# ===============================

# Download Forensic Report
if download_report_btn and st.session_state.file_path:
    report_lines = []

    report_lines.append("AI FORENSIC EVIDENCE REPORT")
    report_lines.append("=" * 40)
    report_lines.append(f"Generated on: {datetime.utcnow().isoformat()} UTC\n")

    report_lines.append(f"Evidence File: {os.path.basename(st.session_state.file_path)}")
    report_lines.append(f"Evidence Hash: {integrity.generate_hash(st.session_state.file_path)}\n")

    status, message = integrity.verify_integrity(st.session_state.file_path)
    report_lines.append(f"Integrity Check Result: {message}\n")

    report_lines.append("AI FORENSIC SUMMARY:")
    report_lines.append("- AI-assisted log analysis performed")
    report_lines.append("- Anomalous events detected and flagged")
    report_lines.append("- Forensic timeline reconstructed\n")

    report_lines.append("NOTE:")
    report_lines.append(
        "This report was generated by an AI-assisted forensic system "
        "with enforced chain-of-custody for legal integrity."
    )

    report_content = "\n".join(report_lines)

    st.download_button(
        label="⬇️ Download Report (.txt)",
        data=report_content,
        file_name="forensic_report.txt",
        mime="text/plain"
    )

# Explanation section
with st.expander("ℹ️ How this system works"):
    st.markdown(
        """
        - **Evidence is locked** using cryptographic hashing before analysis  
        - **AI detects anomalies** and reconstructs attack timelines  
        - **Chain-of-custody is enforced** before and after AI access  
        - **Integrity verification** ensures legal admissibility of evidence  
        """
    )

with st.expander("🌍 Why this matters in the real world"):
    st.markdown(
        """
        Traditional AI-based security tools focus on detecting attacks but often overlook legal and evidentiary requirements.
        This project bridges that critical gap by combining AI-driven forensic analysis with cryptographic evidence integrity.

        **Who benefits from this system:**
        - Cybersecurity teams investigating security breaches and incidents  
        - Digital forensic analysts handling sensitive and legally significant evidence  
        - Organizations facing regulatory, audit, or cyber law compliance requirements  
        - Researchers exploring trustworthy and responsible AI in cybersecurity  

        By enforcing chain-of-custody across AI workflows, the system ensures that AI-generated insights remain
        transparent, auditable, and legally defensible in real-world cyber investigations.
        """
    )

