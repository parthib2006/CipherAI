import streamlit as st
import os
import json
import requests
import asyncio
import time


from dotenv import load_dotenv
load_dotenv()

from core.utils import combine_inputs, normalize_analysis_result
from core.orchastrator import run_cipher_ai_async
from core.report_generate import generate_pdf_report

def generate_timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S")

# ============================================================
# API KEY + MODEL
# ============================================================
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = "gemini-2.5-flash-lite"

TEST_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# ============================================================
# Streamlit UI
# ============================================================

st.set_page_config(page_title="CipherAI", page_icon="🔐")
st.title("🔐 CipherAI — Digital Forensics Incident Analyzer")

st.markdown("""
<style>
body, .stApp {
    background-color: #AA336A;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# DOWNLOAD BUTTON AT TOP (Disabled Initially)
# ============================================================

st.subheader("📄 Download DFIR Report")

download_placeholder = st.empty()
pdf_ready = False
pdf_path = f"CipherAI_Report_{generate_timestamp()}.pdf"

download_placeholder.download_button(
    "⬇ Download PDF Report (Not Ready Yet)",
    data=b"PDF not ready",
    file_name="CipherAI_Report.pdf",
    disabled=True
)

# ============================================================
# API KEY TEST
# ============================================================

st.subheader("API Key Status")

if st.button("Test API Connection"):
    payload = {"contents": [{"parts": [{"text": "Hello"}]}]}
    resp = requests.post(TEST_URL, json=payload)

    if resp.status_code == 200:
        st.success("API Connected Successfully!")
        st.json(resp.json())
    else:
        st.error(f"API Error {resp.status_code}")
        st.code(resp.text)

# ============================================================
# FILE UPLOAD
# ============================================================

st.subheader("Upload Artefacts")

log_file = st.file_uploader("System Log File (.log/.txt)", type=["log","txt"])
pcap_file = st.file_uploader("PCAP (.json/.pcap)", type=["json","pcap"])
mem_file = st.file_uploader("Memory Artefact (.txt/.log)", type=["txt","log"])

log_text = log_file.read().decode() if log_file else None

# PCAP JSON only, .pcap not parsed yet
pcap_json = None
if pcap_file:
    if pcap_file.type == "application/json":
        pcap_json = json.load(pcap_file)
    else:
        st.warning("⚠ .pcap uploaded — raw PCAP parsing not yet implemented")

mem_text = mem_file.read().decode() if mem_file else None

# ============================================================
# RUN ANALYSIS
# ============================================================

if st.button("Run DFIR Analysis"):
    if not API_KEY:
        st.error("Missing API key in .env")
    else:
        with st.spinner("Running CipherAI Agents..."):
            analysis_result = asyncio.run(
                run_cipher_ai_async(log_text, pcap_json, mem_text)
            )

            analysis_result = normalize_analysis_result(analysis_result)

        st.success("Analysis Complete!")

        st.subheader("Parsed Summary (Cleaned)")
        st.json(analysis_result["parsed"])

        # Generate PDF
        pdf_path = generate_pdf_report(analysis_result)

        # Enable download button
        with open(pdf_path, "rb") as f:
            download_placeholder.download_button(
                "⬇ Download PDF Report",
                data=f,
                file_name="CipherAI_Report.pdf",
                mime="application/pdf",
                disabled=False
            )

        st.success("PDF Generated Successfully!")