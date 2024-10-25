#show_data_windows/invoice_window.py
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHeaderView
from db_config.db_operations import get_all_invoices
from add_data_windows.invoice_detail_window import InvoiceDetailWindow


class InvoicesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.all_invoices = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.invoice_table = QTableWidget(self)
        self.layout.addWidget(self.invoice_table)

        self.load_all_invoices()

    def load_all_invoices(self):
        self.all_invoices = get_all_invoices()
        self.update_invoice_table(self.all_invoices)

    def update_invoice_table(self, invoices):
        self.invoice_table.setRowCount(len(invoices))
        self.invoice_table.setColumnCount(6)
        self.invoice_table.setHorizontalHeaderLabels(
            ['Date', 'Customer Name', 'Receiving Amount', 'Remaining Amount', 'Total Amount', 'Details'])

        for row, invoice in enumerate(invoices):
            self.invoice_table.setItem(row, 0, QTableWidgetItem(invoice.current_date))
            self.invoice_table.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
            self.invoice_table.setItem(row, 2, QTableWidgetItem(str(invoice.receiving_amount)))
            self.invoice_table.setItem(row, 3, QTableWidgetItem(str(invoice.remaining_amount)))
            self.invoice_table.setItem(row, 4, QTableWidgetItem(str(invoice.grand_total)))

            # Create a Details button
            details_button = QPushButton("View Details")
            details_button.clicked.connect(lambda _, i_id=invoice.id: self.show_invoice_details(i_id))
            self.invoice_table.setCellWidget(row, 5, details_button)

        self.invoice_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.invoice_table.horizontalHeader().setStretchLastSection(True)
        self.invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_invoice_details(self, invoice_id):
        detail_window = InvoiceDetailWindow(invoice_id, self)
        detail_window.setWindowTitle(f"Invoice Details - {invoice_id}")
        detail_window.resize(600, 400)
        detail_window.exec()
