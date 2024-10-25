#add_data_windows/invoice_detail_window.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel
from db_config.db_operations import get_invoice_by_id


class InvoiceDetailWindow(QDialog):
    def __init__(self, invoice_id, parent=None):
        super().__init__(parent)
        self.invoice_id = invoice_id
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Invoice Details")
        layout = QVBoxLayout(self)

        # Create a table widget to display invoice items
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # Load invoice details
        self.load_invoice_details()

    def load_invoice_details(self):
        invoice = get_invoice_by_id(self.invoice_id)
        if invoice:
            # Set up the table for displaying invoice items
            self.table_widget.setRowCount(len(invoice.invoice_with_item))
            self.table_widget.setColumnCount(6)
            self.table_widget.setHorizontalHeaderLabels(['Product Name', 'Brand', 'Company', 'Quantity', 'Sell Price', 'Total Price'])

            for row, item in enumerate(invoice.invoice_with_item):
                self.table_widget.setItem(row, 0, QTableWidgetItem(item.product_name))
                self.table_widget.setItem(row, 1, QTableWidgetItem(item.brand))
                self.table_widget.setItem(row, 2, QTableWidgetItem(item.company))
                self.table_widget.setItem(row, 3, QTableWidgetItem(str(item.quantity)))
                self.table_widget.setItem(row, 4, QTableWidgetItem(str(item.sell_price)))
                self.table_widget.setItem(row, 5, QTableWidgetItem(str(item.total_price)))

            self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            self.table_widget.horizontalHeader().setStretchLastSection(True)
        else:
            self.table_widget.setRowCount(0)
            label = QLabel("Invoice not found.")
            self.table_widget.setCellWidget(0, 0, label)
