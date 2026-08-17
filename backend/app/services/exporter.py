import pandas as pd
import io
from typing import List
from app.models import ProductItem
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def export_to_excel(products: List[ProductItem], keyword: str, time_range: str) -> bytes:
    data = []
    for item in products:
        data.append({
            "Rank": item.rank,
            "Platform": item.platform.upper(),
            "Nama Produk": item.name,
            "Harga": item.price_formatted,
            "Penjualan": item.sales_volume_formatted,
            "Rating": item.rating,
            "Jumlah Ulasan": item.reviews_count,
            "Nama Toko": item.shop_name,
            "Link Produk": item.product_url
        })
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Top Products')
    return output.getvalue()

def export_to_pdf(products: List[ProductItem], keyword: str, time_range: str) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
    styles = getSampleStyleSheet()
    story = []

    title_style = styles["Heading1"]
    story.append(Paragraph(f"Laporan Analisis Pasar: {keyword.capitalize()} ({time_range.capitalize()})", title_style))
    story.append(Spacer(1, 12))

    table_data = [["Rank", "Platform", "Nama Produk", "Harga", "Penjualan", "Rating", "Toko"]]
    for item in products:
        short_name = (item.name[:45] + '...') if len(item.name) > 45 else item.name
        table_data.append([
            str(item.rank),
            item.platform.upper(),
            short_name,
            item.price_formatted,
            item.sales_volume_formatted,
            f"{item.rating} ★",
            item.shop_name
        ])

    table = Table(table_data, colWidths=[40, 60, 260, 90, 80, 50, 140])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E293B')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F8FAFC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    story.append(table)
    doc.build(story)
    return buffer.getvalue()
