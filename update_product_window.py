from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QDoubleSpinBox, QSpinBox, QLabel, QPushButton,
                               QMessageBox, QHBoxLayout)
from db_operations import get_product_by_barcode


class UpdateProductDialog(QDialog):
    def __init__(self, parent=None, barcode=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Product")
        self.setFixedSize(350, 600)

        # Create layout
        main_layout = QVBoxLayout(self)

        # Create input fields
        self.barcode_input = QLineEdit(self)
        self.barcode_input.setFixedHeight(30)
        self.name_input = QLineEdit(self)
        self.name_input.setFixedHeight(30)
        self.brand_input = QLineEdit(self)
        self.brand_input.setFixedHeight(30)
        self.company_input = QLineEdit(self)
        self.company_input.setFixedHeight(30)
        self.rank_num_input = QLineEdit(self)
        self.rank_num_input.setFixedHeight(30)
        self.pur_price_input = QDoubleSpinBox(self)
        self.pur_price_input.setFixedHeight(30)
        self.pur_price_input.setRange(0, 999999)
        self.sel_price_input = QDoubleSpinBox(self)
        self.sel_price_input.setFixedHeight(30)
        self.sel_price_input.setRange(0, 999999)
        self.quantity_input = QSpinBox(self)
        self.quantity_input.setFixedHeight(30)
        self.quantity_input.setRange(0, 9999)

        # Add labels and fields to layout
        main_layout.addWidget(QLabel("Barcode:"))
        main_layout.addWidget(self.barcode_input)
        main_layout.addWidget(QLabel("Product Name:"))
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(QLabel("Brand:"))
        main_layout.addWidget(self.brand_input)
        main_layout.addWidget(QLabel("Company:"))
        main_layout.addWidget(self.company_input)
        main_layout.addWidget(QLabel("Rank Number:"))
        main_layout.addWidget(self.rank_num_input)
        main_layout.addWidget(QLabel("Purchase Price:"))
        main_layout.addWidget(self.pur_price_input)
        main_layout.addWidget(QLabel("Selling Price:"))
        main_layout.addWidget(self.sel_price_input)
        main_layout.addWidget(QLabel("Quantity:"))
        main_layout.addWidget(self.quantity_input)

        self.fetch_button = QPushButton("Fetch Product", self)
        self.fetch_button.setFixedSize(150, 40)
        self.fetch_button.clicked.connect(self.fetch_product_data)

        self.submit_button = QPushButton("Update", self)
        self.submit_button.setFixedSize(150, 40)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.fetch_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
        self.submit_button.clicked.connect(self.accept)

        if barcode:
            self.barcode_input.setText(barcode)
            self.fetch_product_data()

    def fetch_product_data(self):
        barcode = self.barcode_input.text()
        if not barcode:
            QMessageBox.warning(self, "Error", "Please enter a valid barcode.")
            return

        product_data = get_product_by_barcode(barcode)
        if product_data:
            self.name_input.setText(product_data.name)
            self.brand_input.setText(product_data.brand)
            self.company_input.setText(product_data.company)
            self.rank_num_input.setText(product_data.rank_number)
            self.pur_price_input.setValue(product_data.pur_price)
            self.sel_price_input.setValue(product_data.sel_price)
            self.quantity_input.setValue(product_data.quantity)
        else:
            QMessageBox.warning(self, "Error", "No product found with the provided barcode.")

    def get_product_data(self):
        return {
            'name': self.name_input.text(),
            'barcode': self.barcode_input.text(),
            'brand': self.brand_input.text(),
            'company': self.company_input.text(),
            'rank_number': self.rank_num_input.text(),
            'pur_price_input': self.pur_price_input.value(),
            'sel_price_input': self.sel_price_input.value(),
            'quantity': self.quantity_input.value(),
        }
