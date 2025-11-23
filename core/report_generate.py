# report_generate.py
import io
import json
import time
import matplotlib.pyplot as plt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(analysis_result, output_path=None):
    """
    Generates a PROFESSIONAL DFIR PDF report.
    No raw JSON or parsed output is included.
    Only clean summaries + charts.
    """

    # Timestamp-based filename
    if output_path is None:
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        output_path = f"CipherAI_Report_{timestamp}.pdf"

    # Extract data safely
    parsed = analysis_result.get("parsed", {})
    ips = parsed.get("ips", [])
    ports = parsed.get("ports", {})
    events = parsed.get("parsed_events", [])

    # ----------- CHART GENERATION -----------
    images = []

    # IP Chart
    if ips:
        plt.figure(figsize=(6, 3))
        plt.title("Detected IP Addresses")
        plt.bar(range(len(ips)), [1] * len(ips))
        plt.xticks(range(len(ips)), ips, rotation=45, ha="right")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        images.append(buf)
        plt.close()

    # Port Chart
    if ports:
        plt.figure(figsize=(6, 3))
        plt.title("Port Activity Frequency")
        plt.bar(list(ports.keys()), list(ports.values()))
        plt.tight_layout()

        buf2 = io.BytesIO()
        plt.savefig(buf2, format="png")
        buf2.seek(0)
        images.append(buf2)
        plt.close()

    # ------------------------------------------------------
    #                PDF CONTENT (CLEAN DFIR REPORT)
    # ------------------------------------------------------

    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>CipherAI Digital Forensics Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # Executive Summary
    story.append(Paragraph("<b>1. Executive Summary</b>", styles["Heading2"]))
    summary_text = """
    This report presents the results of an automated DFIR (Digital Forensics & Incident Response)
    analysis conducted using CipherAI. The analysis includes log inspection, PCAP network evaluation,
    and memory forensic assessment to identify suspicious activity, potential Indicators of Compromise (IOCs),
    and anomalies in system behavior.
    """
    story.append(Paragraph(summary_text, styles["BodyText"]))
    story.append(Spacer(1, 12))

    # Indicators of Compromise
    story.append(Paragraph("<b>2. Indicators of Compromise (IOCs)</b>", styles["Heading2"]))

    if ips:
        story.append(Paragraph("<b>Suspicious IPs Detected:</b>", styles["BodyText"]))
        for ip in ips:
            story.append(Paragraph(f"• {ip}", styles["BodyText"]))
    else:
        story.append(Paragraph("No suspicious IP addresses detected.", styles["BodyText"]))

    story.append(Spacer(1, 12))

    if ports:
        story.append(Paragraph("<b>Suspicious or Unusual Ports:</b>", styles["BodyText"]))
        for port, count in ports.items():
            story.append(Paragraph(f"• Port {port}: {count} events", styles["BodyText"]))
    else:
        story.append(Paragraph("No unusual port activity detected.", styles["BodyText"]))

    story.append(Spacer(1, 12))

    # Memory Events
    story.append(Paragraph("<b>3. Memory Forensics Findings</b>", styles["Heading2"]))

    suspicious_events = [e for e in events if "process" in str(e).lower() or "injection" in str(e).lower()]

    if suspicious_events:
        for ev in suspicious_events:
            story.append(Paragraph(f"• {ev}", styles["BodyText"]))
    else:
        story.append(Paragraph("No suspicious memory events detected.", styles["BodyText"]))

    story.append(Spacer(1, 20))

    # Include charts
    story.append(Paragraph("<b>4. Visual Summary</b>", styles["Heading2"]))
    story.append(Spacer(1, 12))

    for img in images:
        story.append(Image(img, width=400, height=240))
        story.append(Spacer(1, 16))

    # Build final PDF
    doc.build(story)

    return output_path