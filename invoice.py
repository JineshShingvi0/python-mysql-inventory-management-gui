from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(
    TTFont(
        "DejaVuSans",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    )
)
pdfmetrics.registerFont(
    TTFont(
        "DejaVuSans-Bold",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    )
)

import os

from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image
)

# ==========================================================
# BUSINESS DETAILS
# ==========================================================

BUSINESS_NAME = "Shingvi Supermart"
BUSINESS_ADDRESS = "Market Yard, Pune"
BUSINESS_PHONE = "9881353330"
GST_NUMBER = "27ABCDE1234F1Z5"

LOGO_PATH = "assets/logo.png"
QR_PATH = "assets/UPI Qr.png"

styles = getSampleStyleSheet()

def generate_invoice(
    sale_id,
    customer_name,
    phone,
    payment_method,
    cart,
    subtotal,
    gst,
    discount,
    grand_total
):
    invoice_number = f"INV-{sale_id:05d}"

    today = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    invoice_path = f"invoices/{invoice_number}.pdf"

    doc = SimpleDocTemplate(
            invoice_path,
        rightMargin=18,
        leftMargin=18,
        topMargin=18,
        bottomMargin=18
    )

    story = []

        # Logo
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=35*mm, height=35*mm)
        story.append(logo)

    story.append(
        Paragraph(
            "<b><font size=18 color='#065F46'>SHINGVI SUPERMART</font></b>",
            styles["Title"]
        )
    )

    story.append(Paragraph(BUSINESS_ADDRESS, styles["Normal"]))
    story.append(Paragraph(f"Phone : {BUSINESS_PHONE}", styles["Normal"]))
    story.append(Paragraph(f"GSTIN : {GST_NUMBER}", styles["Normal"]))

    story.append(Spacer(1,10))

    customer_data = [
        ["Invoice No.", invoice_number],
        ["Date", today],
        ["Customer", customer_name],
        ["Phone", phone],
        ["Payment", payment_method]
    ]

    customer_table = Table(customer_data, colWidths=[100,250])

    customer_table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),
        ("BACKGROUND",(0,0),(0,-1),colors.HexColor("#D1FAE5")),
        ("TEXTCOLOR",(0,0),(0,-1),colors.HexColor("#065F46")),
        ("FONTNAME",(0,0),(-1,-1),"DejaVuSans-Bold"),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
    ]))

    story.append(customer_table)
    story.append(Spacer(1,12))

    table_data = [
        ["Product","Qty","Price","Subtotal"]
    ]

    for item in cart:

        table_data.append([
            item["name"],
            item["quantity"],
            f"₹ {item['price']:.2f}",
            f"₹ {item['subtotal']:.2f}"
        ])

    product_table = Table(
        table_data,
        colWidths=[190,55,90,90]
    )

    product_table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#065F46")),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),

        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        # Header font
        ("FONTNAME",(0,0),(-1,0),"DejaVuSans-Bold"),

        # Body font (THIS FIXES ₹)
        ("FONTNAME",(0,1),(-1,-1),"DejaVuSans"),

        ("ALIGN",(1,1),(-1,-1),"CENTER"),
        ("BOTTOMPADDING",(0,0),(-1,0),10),

        ("BACKGROUND",(0,1),(-1,-1),colors.white)
    ]))

    story.append(product_table)
    story.append(Spacer(1,12))

    summary_data = [
        ["Subtotal", f"₹ {subtotal:.2f}"],
        ["Discount", f"₹ {discount:.2f}"],
        ["GST (18%)", f"₹ {gst:.2f}"],
        ["Grand Total", f"₹ {grand_total:.2f}"]
    ]

    summary_table = Table(summary_data, colWidths=[250,175])

    summary_table.setStyle(TableStyle([
        ("GRID",(0,0),(-1,-1),0.5,colors.grey),

        ("BACKGROUND",(0,3),(-1,3),colors.HexColor("#DCFCE7")),

        ("TEXTCOLOR",(0,3),(-1,3),colors.HexColor("#14532D")),

        ("FONTNAME",(0,0),(-1,-1),"DejaVuSans"),
        ("ALIGN",(1,0),(1,-1),"RIGHT")
    ]))

    story.append(summary_table)
    story.append(Spacer(1,18))

    story.append(
        Paragraph(
            "<b>Scan to Pay</b>",
            styles["Heading3"]
        )
    )

    if os.path.exists(QR_PATH):

        qr = Image(QR_PATH, width=42*mm, height=42*mm)
        story.append(qr)

    story.append(Spacer(1,12))


    story.append(
        Paragraph(
            "<font color='#065F46'><b>Thank you for shopping with Shingvi Supermart!</b></font>",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            "Visit Again • Quality Products • Best Prices",
            styles["Normal"]
        )
    )

    story.append(Spacer(1,8))

    story.append(
        Paragraph(
            f"Generated At : {today}",
            styles["Italic"]
        )
    )

    doc.build(story)

    return invoice_path
