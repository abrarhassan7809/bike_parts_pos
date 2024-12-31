#add_data_windows/insert_product_dialog.py
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QDoubleSpinBox, QSpinBox, QLabel, QPushButton,
                               QHBoxLayout, QMessageBox, QFileDialog)
from datetime import datetime
from add_data_windows.import_product_dialog import ImportProductDialog


class InsertProductDialog(QDialog):
    signal_created = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Product")
        self.setFixedSize(350, 600)
        self.date_time = datetime.today().strftime('%Y-%m-%d')

        # Create layout
        main_layout = QVBoxLayout(self)

        # Input fields
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

        self.submit_button = QPushButton("Add Product", self)
        self.submit_button.setFixedSize(150, 40)
        self.submit_button.clicked.connect(self.validate_fields)

        self.import_button = QPushButton("Import File", self)
        self.import_button.setFixedSize(150, 40)
        self.import_button.clicked.connect(self.open_import_dialog)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def get_product_data(self):
        return {
            'name': self.name_input.text(),
            'company': self.company_input.text(),
            'rank_number': self.rank_num_input.text(),
            'pur_price': self.pur_price_input.value(),
            'sel_price': self.sel_price_input.value(),
            'quantity': self.quantity_input.value(),
            'current_date': self.date_time,
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

    def open_import_dialog(self):
        dialog = ImportProductDialog(self)
        if dialog.exec() == QDialog.Accepted:
            QMessageBox.information(self, "Import", "Products imported successfully.")
            self.signal_created.emit()
