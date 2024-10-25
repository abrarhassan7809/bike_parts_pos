# show_data_windows/customer_window.py
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QHBoxLayout, QLineEdit, \
    QSpacerItem, QSizePolicy, QPushButton, QMessageBox
from db_config.db_operations import get_all_customers, delete_customer


class CustomerWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.all_customer = []
        self.filtered_customer = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Create a search layout
        search_layout = QHBoxLayout()
        self.search_data = QLineEdit(self)
        self.search_data.setFixedWidth(300)
        self.search_data.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.search_data.setPlaceholderText("Search customers...")
        self.search_data.textChanged.connect(self.filter_customer)

        search_layout.addWidget(self.search_data)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        search_layout.addItem(spacer)
        self.layout.addLayout(search_layout)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.load_all_customer()

    def load_all_customer(self):
        self.all_customer = get_all_customers()
        self.filtered_customer = self.all_customer
        self.update_customer_table(self.filtered_customer)

    def filter_customer(self):
        customer_text = self.search_data.text().strip().lower()

        self.filtered_customer = [
            customer for customer in self.all_customer
            if (customer_text in customer.name.lower() if customer.name else False) or
               (customer_text in customer.company.lower() if customer.company else False) or
               (customer_text in customer.phone_num.lower() if customer.phone_num else False) or
               (customer_text in customer.city.lower() if customer.city else False)
        ]

        self.update_customer_table(self.filtered_customer)

    def update_customer_table(self, customers):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(customers))
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Company', 'Contact', 'Email', 'City', 'Address', 'Action'])

        for row, customer in enumerate(customers):
            self.table_widget.setItem(row, 0, QTableWidgetItem(customer.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(customer.company))
            self.table_widget.setItem(row, 2, QTableWidgetItem(customer.phone_num))
            self.table_widget.setItem(row, 3, QTableWidgetItem(customer.email))
            self.table_widget.setItem(row, 4, QTableWidgetItem(customer.city))
            self.table_widget.setItem(row, 5, QTableWidgetItem(customer.address))

            # Create Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, p_id=customer.id: self.delete_product(p_id))
            self.table_widget.setCellWidget(row, 6, delete_button)

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def delete_product(self, product_id):
        response = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            delete_customer(product_id)
            self.load_all_customer()
