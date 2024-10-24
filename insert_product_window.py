# insert_product_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QDoubleSpinBox, QSpinBox, QLabel, QPushButton,
                               QHBoxLayout)


class InsertProductDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Product")
        self.setFixedSize(350, 600)

        # Create layout
        main_layout = QVBoxLayout(self)

        # Input fields
        self.name_input = QLineEdit(self)
        self.name_input.setFixedHeight(30)
        self.barcode_input = QLineEdit(self)
        self.barcode_input.setFixedHeight(30)
        self.brand_input = QLineEdit(self)
        self.brand_input.setFixedHeight(30)
        self.company_input = QLineEdit(self)
        self.company_input.setFixedHeight(30)
        self.rank_num_input = QLineEdit(self)
        self.rank_num_input.setFixedHeight(30)
        self.pur_price_input = QDoubleSpinBox(self)
        self.pur_price_input.setFixedHeight(30)
        self.pur_price_input.setRange(0, 999999)
        self.pur_price_input.setFixedHeight(30)
        self.sel_price_input = QDoubleSpinBox(self)
        self.sel_price_input.setFixedHeight(30)
        self.sel_price_input.setRange(0, 999999)
        self.quantity_input = QSpinBox(self)
        self.quantity_input.setFixedHeight(30)
        self.quantity_input.setRange(0, 9999)

        # Add labels and fields to layout
        main_layout.addWidget(QLabel("Product Name:"))
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(QLabel("Barcode:"))
        main_layout.addWidget(self.barcode_input)
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

        self.submit_button = QPushButton("Insert", self)
        self.submit_button.setFixedSize(150, 40)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
        self.submit_button.clicked.connect(self.accept)

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
