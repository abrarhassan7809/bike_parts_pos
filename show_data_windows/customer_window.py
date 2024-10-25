# show_data_windows/customer_window.py
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from db_config.db_operations import get_all_customers


class CustomerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())

        self.table_widget = QTableWidget()
        self.layout().addWidget(self.table_widget)

        self.load_customers()

    def load_customers(self):
        customers = get_all_customers()
        self.table_widget.setRowCount(len(customers))
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Company', 'Contact', 'Email', 'City', 'Address'])

        for row, customer in enumerate(customers):
            self.table_widget.setItem(row, 0, QTableWidgetItem(customer.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(customer.company))
            self.table_widget.setItem(row, 2, QTableWidgetItem(customer.phone_num))
            self.table_widget.setItem(row, 3, QTableWidgetItem(customer.email))
            self.table_widget.setItem(row, 4, QTableWidgetItem(customer.city))
            self.table_widget.setItem(row, 5, QTableWidgetItem(customer.address))

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
