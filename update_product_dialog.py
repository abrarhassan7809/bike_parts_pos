from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QDoubleSpinBox, QSpinBox, QLabel, QPushButton,
                               QMessageBox, QHBoxLayout)
from db_operations import get_product_by_barcode


class UpdateProductDialog(QDialog):
    def __init__(self, parent=None, barcode=None):
        super().__init__(parent)
        self.setWindowTitle("Edit Product")
        self.setFixedSize(350, 500)

        # Create layout
        main_layout = QVBoxLayout(self)

        # Create input fields
        self.barcode_input = QLineEdit(self)
        self.barcode_input.setFixedHeight(30)
        self.name_input = QLineEdit(self)
        self.name_input.setFixedHeight(30)
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
        main_layout.addWidget(QLabel("Purchase Price:"))
        main_layout.addWidget(self.pur_price_input)
        main_layout.addWidget(QLabel("Selling Price:"))
        main_layout.addWidget(self.sel_price_input)
        main_layout.addWidget(QLabel("Quantity:"))
        main_layout.addWidget(self.quantity_input)

        # Add fetch button to get product details by barcode
        self.fetch_button = QPushButton("Fetch Product", self)
        self.fetch_button.setFixedSize(150, 40)
        self.fetch_button.clicked.connect(self.fetch_product_data)

        # Add submit button for updating the product
        self.submit_button = QPushButton("Update", self)
        self.submit_button.setFixedSize(150, 40)

        # Create a horizontal layout to center the button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.fetch_button)
        button_layout.addStretch()

        # Add button layout to the main layout
        main_layout.addLayout(button_layout)

        # Connect the submit button to dialog accept
        self.submit_button.clicked.connect(self.accept)

        # If barcode is provided, automatically populate fields
        if barcode:
            self.barcode_input.setText(barcode)
            self.fetch_product_data()

    def fetch_product_data(self):
        barcode = self.barcode_input.text()
        if not barcode:
            # Using a custom message box with set size
            QMessageBox.warning(self, "Error", "Please enter a valid barcode.")
            return

        # Fetch the product from the database (get_product_by_barcode should be defined in db_operations)
        product_data = get_product_by_barcode(barcode)
        if product_data:
            self.name_input.setText(product_data.name)
            self.pur_price_input.setValue(product_data.pur_price)
            self.sel_price_input.setValue(product_data.sel_price)
            self.quantity_input.setValue(product_data.quantity)
        else:
            # Using a custom message box with set size
            QMessageBox.warning(self, "Error", "No product found with the provided barcode.")

    def get_product_data(self):
        return {
            'name': self.name_input.text(),
            'barcode': self.barcode_input.text(),
            'pur_price': self.pur_price_input.value(),
            'sel_price': self.sel_price_input.value(),
            'quantity': self.quantity_input.value()
        }
