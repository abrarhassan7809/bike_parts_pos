# product_selection_dialog.py
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHeaderView,
                               QLineEdit, QLabel, QHBoxLayout)
from db_config.db_operations import get_all_products


class ProductSelectionDialog(QDialog):
    product_selected = Signal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Product")
        self.setMinimumSize(600, 400)
        self.init_ui()
        self.all_products = []
        self.load_products()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Search Layout
        search_layout = QVBoxLayout()
        self.search_data = QLineEdit(self)
        self.search_data.setFixedWidth(300)
        self.search_data.setFixedWidth(300)
        self.search_data.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.search_data.setPlaceholderText("Search product...")
        self.search_data.textChanged.connect(self.filter_products)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_data)

        layout.addLayout(search_layout)

        # Product Table
        self.product_table = QTableWidget(self)
        self.product_table.setColumnCount(4)
        self.product_table.setHorizontalHeaderLabels(['Name', 'Company', 'Qty', 'Price'])
        self.product_table.setSelectionBehavior(QTableWidget.SelectRows)
        layout.addWidget(self.product_table)

        # Make columns stretchable
        header = self.product_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        select_button = QPushButton("Select Product")
        select_button.clicked.connect(self.select_product)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(select_button)

        layout.addLayout(button_layout)

    def load_products(self):
        self.all_products = get_all_products()
        self.display_products(self.all_products)

    def display_products(self, products):
        self.product_table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.product_table.setItem(row, 0, QTableWidgetItem(product.name))
            self.product_table.setItem(row, 1, QTableWidgetItem(product.company))
            self.product_table.setItem(row, 2, QTableWidgetItem(str(product.quantity)))
            self.product_table.setItem(row, 3, QTableWidgetItem(str(product.sel_price)))

    def filter_products(self):
        filter_text = self.search_data.text().strip().lower()
        filtered_products = [
            product for product in self.all_products
            if filter_text in product.name.lower() or
               filter_text in product.company.lower()
        ]
        self.display_products(filtered_products)

    def select_product(self):
        selected_row = self.product_table.currentRow()
        if selected_row >= 0:
            product_data = {
                'name': self.product_table.item(selected_row, 0).text(),
                'company': self.product_table.item(selected_row, 1).text(),
                'quantity': self.product_table.item(selected_row, 2).text(),
                'price': float(self.product_table.item(selected_row, 3).text()),
            }
            self.product_selected.emit(product_data)
            self.accept()
