# PDF & Graphs Generator (Clean Version)
import io
import json
import matplotlib.pyplot as plt
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(analysis_result, output_path=None):
    """
    Clean DFIR PDF report generator.
    - No raw JSON
    - No parsed dictionaries
    - Only Summary + Graphs
    - Graph placeholders if no graphs produced
    """

    # -----------------------------------------
    # 1. Unique Filename Generation
    # -----------------------------------------
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"CipherAI_Report_{timestamp}.pdf"

    # -----------------------------------------
    # 2. Extract meaningful summary text ONLY
    # -----------------------------------------
    summary_text = analysis_result.get("summary", None)

    # Fallback (if no summary key)
    if not summary_text:
        summary_text = analysis_result.get("output", "No summary available")
    
    summary_text = summary_text.replace("\n", "<br/>")

    # -----------------------------------------
    # 3. Prepare Graph Data
    # -----------------------------------------
    parsed = analysis_result.get("parsed", {})
    ips = parsed.get("ips", [])
    ports = parsed.get("ports", {})

    images = []

    # ------ Graph 1: IP Count Bar Chart ------
    if ips:
        plt.figure(figsize=(6, 3))
        plt.title("Detected IPs")
        plt.bar(range(len(ips)), [1] * len(ips))
        plt.xticks(range(len(ips)), ips, rotation=45, ha="right")
        plt.tight_layout()

        buf = io.BytesIO()
        plt.savefig(buf, format="png", dpi=200)
        buf.seek(0)
        images.append(buf)
        plt.close()

    # ------ Graph 2: Ports Histogram ------
    if ports:
        plt.figure(figsize=(6, 3))
        plt.title("Port Frequency")
        plt.bar(list(ports.keys()), list(ports.values()))
        plt.tight_layout()

        buf2 = io.BytesIO()
        plt.savefig(buf2, format="png", dpi=200)
        buf2.seek(0)
        images.append(buf2)
        plt.close()

    # -----------------------------------------
    # 4. Build PDF Document
    # -----------------------------------------
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>CipherAI Digital Forensics Report</b>", styles["Title"]))
    story.append(Spacer(1, 14))

    story.append(Paragraph("Incident Summary:", styles["Heading2"]))
    story.append(Paragraph(summary_text, styles["BodyText"]))
    story.append(Spacer(1, 16))

    # ---- If no graphs available ----
    if len(images) == 0:
        story.append(Paragraph(
            "<i>No graph could be generated for this dataset (no numeric distributions found).</i>",
            styles["Italic"]
        ))
        story.append(Spacer(1, 16))

    # ---- Add charts to PDF ----
    for img in images:
        story.append(Image(img, width=400, height=240))
        story.append(Spacer(1, 20))

    # Final build
    doc.build(story)

    return output_path