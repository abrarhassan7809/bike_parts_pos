#show_data_windows/invoice_window.py
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHeaderView,
                               QLineEdit, QHBoxLayout, QSizePolicy, QSpacerItem)
from add_data_windows.add_invoice_window import CreateInvoiceWindow
from db_config.db_operations import get_all_invoices, get_invoice_by_id
from show_data_windows.invoice_detail_window import InvoiceDetailWindow


class InvoicesWindow(QWidget):
    signal_created = Signal()
    def __init__(self, parent=None, tab_manager=None):
        super().__init__(parent)
        self.parent = parent
        self.tab_manager = tab_manager
        self.all_invoices = []
        self.filtered_invoices = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Create a search layout
        search_layout = QHBoxLayout()
        self.search_data = QLineEdit(self)
        self.search_data.setFixedWidth(300)
        self.search_data.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.search_data.setPlaceholderText("Search invoices...")
        self.search_data.textChanged.connect(self.filter_invoices)

        search_layout.addWidget(self.search_data)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        search_layout.addItem(spacer)
        self.layout.addLayout(search_layout)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.load_all_invoices()

    def load_all_invoices(self):
        self.all_invoices = get_all_invoices()
        self.filtered_invoices = self.all_invoices
        self.update_invoice_table(self.filtered_invoices)

    def filter_invoices(self):
        customer_text = self.search_data.text().strip().lower()
        self.filtered_invoices = [invoice for invoice in self.all_invoices
            if (customer_text in invoice.customer_name.lower()) or (customer_text in invoice.current_date)]

        self.update_invoice_table(self.filtered_invoices)

    def update_invoice_table(self, invoices):
        self.table_widget.setRowCount(len(invoices))
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ['Date', 'Customer Name', 'Receiving Amount', 'Remaining Amount', 'Total Amount', 'Details', 'Edit'])

        for row, invoice in enumerate(invoices):
            self.table_widget.setItem(row, 0, QTableWidgetItem(invoice.current_date))
            self.table_widget.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(round(invoice.receiving_amount, 2))))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(round(invoice.remaining_amount, 2))))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(round(invoice.grand_total, 2))))

            # Create a Details button
            details_button = QPushButton("View Details")
            details_button.clicked.connect(lambda _, i_id=invoice.id: self.show_invoice_details(i_id))
            self.table_widget.setCellWidget(row, 5, details_button)

            # Edit button
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, i_id=invoice.id: self.update_invoice_data(i_id))
            self.table_widget.setCellWidget(row, 6, edit_button)

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show_invoice_details(self, invoice_id):
        detail_window = InvoiceDetailWindow(invoice_id, self)
        detail_window.setWindowTitle(f"Invoice Details - {invoice_id}")
        detail_window.resize(600, 400)
        detail_window.exec()
        self.signal_created.emit()

    def create_invoice_tab(self, invoice=None):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Create Invoice":
                self.tab_manager.setCurrentIndex(index)
                return

        invoice_widget = CreateInvoiceWindow(invoice=invoice, parent=self)
        invoice_widget.signal_created.connect(self.load_all_invoices)
        tab_title = "Edit Invoice" if invoice else "Create Invoice"
        self.tab_manager.add_new_tab(tab_title, invoice_widget)

    def update_invoice_data(self, invoice_id):
        invoice = get_invoice_by_id(invoice_id)
        if invoice:
            self.create_invoice_tab(invoice=invoice)
