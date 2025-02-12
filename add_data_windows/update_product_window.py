#add_data_windows/update_product_window.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QDoubleSpinBox, QSpinBox, QLabel, QPushButton,
                               QMessageBox, QHBoxLayout)
from db_config.db_operations import get_product_by_id, get_product_by_name


class UpdateProductDialog(QDialog):
    def __init__(self, parent=None, p_id=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Product")
        self.setFixedSize(350, 600)
        self.is_product = None
        self.p_id = p_id
        if self.p_id is not None:
            self.is_product = get_product_by_id(self.p_id)

        # Create layout
        main_layout = QVBoxLayout(self)

        # Create input fields
        self.name_input = QLineEdit(self)
        self.name_input.setFixedHeight(30)
        self.company_input = QLineEdit(self)
        self.company_input.setFixedHeight(30)
        self.rank_num_input = QLineEdit(self)
        self.rank_num_input.setFixedHeight(30)
        self.pur_price_input = QDoubleSpinBox(self)
        self.pur_price_input.setFixedHeight(30)
        self.pur_price_input.setRange(1, 999999)
        self.sel_price_input = QDoubleSpinBox(self)
        self.sel_price_input.setFixedHeight(30)
        self.sel_price_input.setRange(2, 999999)
        self.quantity_input = QSpinBox(self)
        self.quantity_input.setFixedHeight(30)
        self.quantity_input.setRange(1, 9999)

        # Add labels and fields to layout
        main_layout.addWidget(QLabel("Product Name:"))
        main_layout.addWidget(self.name_input)
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

        self.submit_button = QPushButton("Update", self)
        self.submit_button.setFixedSize(150, 40)

        self.fetch_button = QPushButton("Get Product", self)
        self.fetch_button.setFixedSize(150, 40)
        self.fetch_button.clicked.connect(self.fetch_product_data)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.fetch_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
        self.submit_button.clicked.connect(self.validate_fields)

        if self.is_product:
            self.name_input.setText(self.is_product.name)
            self.fetch_product_data()

    def fetch_product_data(self):
        p_name = self.name_input.text()
        if not p_name:
            QMessageBox.warning(self, "Error", "Please enter a valid name.")
            return

        product_data = get_product_by_name(p_name)
        if product_data:
            self.p_id = product_data.id
            self.name_input.setText(product_data.name)
            self.company_input.setText(product_data.company)
            self.rank_num_input.setText(product_data.rank_number)
            self.pur_price_input.setValue(product_data.pur_price)
            self.sel_price_input.setValue(product_data.sel_price)
            self.quantity_input.setValue(product_data.quantity)
        else:
            QMessageBox.warning(self, "Error", "No product found with the provided name.")

    def get_product_data(self):
        return {
            'p_id': self.p_id,
            'name': self.name_input.text(),
            'company': self.company_input.text(),
            'rank_number': self.rank_num_input.text(),
            'pur_price': self.pur_price_input.value(),
            'sel_price': self.sel_price_input.value(),
            'quantity': self.quantity_input.value(),
        }

    def validate_fields(self):
        name = self.name_input.text().strip()
        company = self.company_input.text().strip()
        pur_price = self.pur_price_input.value()
        sel_price = self.sel_price_input.value()
        quantity = self.quantity_input.value()

        if not name or not sel_price or not company:
            QMessageBox.warning(self, "Validation Error", "All fields required.")
            return

        if pur_price <= 0 or sel_price <= 0 or quantity <= 0:
            QMessageBox.warning(self, "Validation Error", "Price and quantity must be greater than zero.")
            return

        if pur_price > sel_price:
            QMessageBox.warning(self, "Validation Error", "Sell Price must be greater than purchase price.")
            return

        self.accept()
