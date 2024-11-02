# add_data_windows/save_invoice_pdf.py
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
import re

from db_config.db_operations import generate_unique_invoice_code


def save_invoice_as_pdf(invoice_data, output_dir):
    safe_customer_name = re.sub(r'[\\/*?:"<>|]', "_", invoice_data['customer_name'])
    safe_date = re.sub(r'[\\/*?:"<>|]', "_", invoice_data['current_date'])

    # Check and create the directory if it doesn't exist
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Directory '{output_dir}' created successfully.")
        except Exception as e:
            print(f"Failed to create directory '{output_dir}': {e}")
            return

    # Create the file path with safe characters
    invoice_code = generate_unique_invoice_code()
    file_path = os.path.join(output_dir, f"Invoice_{invoice_code}_{safe_date}.pdf")

    # Prepare the PDF structure
    pdf = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    normal_style = styles["Normal"]

    # Add company title and details
    title = Paragraph("Atoms Company", title_style)
    elements.append(title)

    elements.append(Paragraph(f"Customer Name: {invoice_data['customer_name']}", normal_style))
    elements.append(Paragraph(f"Invoice Date: {invoice_data['current_date']}", normal_style))
    elements.append(Paragraph(f"Grand Total: {invoice_data['grand_total']}", normal_style))
    elements.append(Paragraph(f"Discount: {invoice_data['discount']}", normal_style))
    elements.append(Paragraph(f"Receiving Amount: {invoice_data['receiving_amount']}", normal_style))
    elements.append(Paragraph(f"Remaining Amount: {invoice_data['remaining_amount']}", normal_style))
    elements.append(Paragraph(" ", normal_style))  # Space

    # Prepare table data
    table_data = [["Product", "Company", "Quantity", "Price", "Total"]]
    for item in invoice_data['items']:
        table_data.append([
            item['product_name'],
            item['company'],
            str(item['quantity']),
            f"{item['sell_price']:.2f}",
            f"{item['total_price']:.2f}"
        ])

    # Create table with styles
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(table)

    # Attempt to build and save the PDF
    try:
        pdf.build(elements)
        print(f"Invoice PDF saved successfully at: {file_path}")
    except Exception as e:
        print(f"Failed to save invoice PDF: {e}")
