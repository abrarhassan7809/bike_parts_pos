from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit,
                               QPushButton, QSpacerItem, QSizePolicy, QHeaderView, QMessageBox)
from db_config.db_operations import get_all_products, generate_unique_invoice_code
import os


class ShowInventoryWindow(QWidget):
    signal_created = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.all_inventory = []
        self.filtered_inventory = []
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)
        btn_layout = QHBoxLayout()
        self.search_data = QLineEdit(self)
        self.search_data.setFixedWidth(300)
        self.search_data.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.search_data.setPlaceholderText("Search invoices...")
        self.search_data.textChanged.connect(self.filter_inventory)
        self.print_btn = QPushButton("Print", self)
        self.print_btn.clicked.connect(self.save_inventory_pdf)

        btn_layout.addWidget(self.search_data)
        btn_layout.addWidget(self.print_btn)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        btn_layout.addItem(spacer)
        self.main_layout.addLayout(btn_layout)

        self.table_widget = QTableWidget(self)
        self.main_layout.addWidget(self.table_widget)

        self.load_all_inventory()

    def load_all_inventory(self):
        self.all_products = get_all_products()
        self.filtered_inventory = self.all_products
        self.update_inventory_table(self.filtered_inventory)

    def filter_inventory(self):
        search_text = self.search_data.text().strip().lower()
        self.filtered_inventory = [inventory for inventory in self.all_products
                                   if (search_text in inventory.company.lower()) or (
                                               search_text in inventory.name.lower())]

        self.update_inventory_table(self.filtered_inventory)

    def update_inventory_table(self, all_products):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(all_products))
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Company', 'Quantity'])

        for row, product in enumerate(all_products):
            self.table_widget.setItem(row, 0, QTableWidgetItem(product.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(product.company))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(product.quantity)))

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def save_inventory_pdf(self):
        output_dir = "pdf_inventory"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        reply = QMessageBox.question(self, "Save PDF", "Do you want to save this inventory as a PDF?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.print_inventory(output_dir)
                QMessageBox.information(self, "PDF Saved", "Inventory saved as PDF successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save PDF: {e}")

    def print_inventory(self, output_dir):
        inventory_code = generate_unique_invoice_code()
        pdf_filename = os.path.join(output_dir, f"inventory_report_{inventory_code}.pdf")

        pdf = canvas.Canvas(pdf_filename, pagesize=A4)
        width, height = A4
        y_position = height - 40

        # Table title
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(200, y_position, "Inventory Report")
        y_position -= 40  # Move down for the next content

        # Prepare data for the table
        data = [["Name", "Company", "Quantity"]]
        for product in self.filtered_inventory:
            data.append([product.name, product.company, str(product.quantity)])

        # Create Table object
        table = Table(data, colWidths=[200, 200, 100])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])
        table.setStyle(style)

        # Loop through rows and print
        row_height = 18
        max_rows_per_page = int((height - 100) / row_height)
        rows_printed = 0

        # Draw table rows, and handle page overflow
        for i in range(0, len(data), max_rows_per_page):
            page_data = data[i:i + max_rows_per_page]
            table = Table(page_data, colWidths=[200, 200, 100])
            table.setStyle(style)
            table.wrapOn(pdf, width, height)
            table.drawOn(pdf, 40, y_position - (len(page_data) * row_height))

            rows_printed += len(page_data)
            y_position -= len(page_data) * row_height

            # Check if we need a new page
            if rows_printed < len(data):
                pdf.showPage()
                y_position = height - 40

        # Save the PDF
        pdf.save()
