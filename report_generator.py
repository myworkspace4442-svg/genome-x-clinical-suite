import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_clinical_pdf(filename, dna_seq, gc_ratio, security_status, mutations="0"):
    # ၁။ PDF စာရွက် အရွယ်အစား သတ်မှတ်ခြင်း
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40,
                            leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()

    # ၂။ ကိုယ်ပိုင် စာလုံးဒီဇိုင်း (Styles) များ ဖန်တီးခြင်း
    title_style = ParagraphStyle(
        'MainTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor("#1A365D"),  # Navy Blue ရောင်
        spaceAfter=15
    )

    meta_style = ParagraphStyle(
        'Meta', parent=styles['Normal'], fontSize=10, leading=14)
    seq_style = ParagraphStyle(
        'Sequence', parent=styles['Normal'], fontName='Courier', fontSize=10, leading=14)

    # ၃။ ခေါင်းစဉ်ပိုင်း ထည့်သွင်းခြင်း
    story.append(
        Paragraph("🧬 Genome-X Clinical Diagnostic Report", title_style))
    story.append(Paragraph(
        f"Report Generated On: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", meta_style))
    story.append(Spacer(1, 15))

    # ၄။ ရလဒ်များကို Table (ဇယား) ပုံစံဖြင့် စနစ်တကျ စီခြင်း
    # Threat ရှိရင် အနီ၊ စိတ်ချရရင် အစိမ်း
    status_color = "#E53E3E" if "Threat" in security_status else "#38A169"

    table_data = [
        [Paragraph("<b>Metric / Parameter</b>", meta_style),
         Paragraph("<b>Diagnostic Result</b>", meta_style)],
        [Paragraph("Analysis Type", meta_style), Paragraph(
            "Automated DNA Sequencing", meta_style)],
        [Paragraph("GC Content Ratio", meta_style),
         Paragraph(f"<b>{gc_ratio}</b>", meta_style)],
        [Paragraph("Bio-Security Status", meta_style), Paragraph(
            f"<font color='{status_color}'><b>{security_status}</b></font>", meta_style)],
        [Paragraph("Detected Mutations", meta_style), Paragraph(
            f"{mutations} mutations found", meta_style)]
    ]

    # ဇယားကို ဒီဇိုင်းဆွဲခြင်း (Border, Background color)
    report_table = Table(table_data, colWidths=[200, 300])
    report_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (1, 0), colors.HexColor(
            "#2B6CB0")),  # Header ကို ပြာရောင်ပေးမယ်
        ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        # Data Row တွေကို မီးခိုးနုရောင်ပေးမယ်
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))

    story.append(report_table)
    story.append(Spacer(1, 20))

    # ၅။ စစ်ဆေးခဲ့သည့် မူရင်း DNA Sequence အား အောက်ခြေတွင် ပြသခြင်း
    story.append(
        Paragraph("<b>Analyzed Primary DNA Sequence:</b>", styles['Heading3']))
    story.append(Spacer(1, 5))
    story.append(Paragraph(dna_seq, seq_style))

    # PDF ဖိုင်အဖြစ် တည်ဆောက်ထုတ်လုပ်လိုက်ခြင်း
    doc.build(story)
