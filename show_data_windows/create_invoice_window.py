#show_data_windows/create_invoice_window.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QTableWidget, QPushButton,
                               QMessageBox, QTableWidgetItem, QGridLayout, QHBoxLayout, QHeaderView, QComboBox)
from db_config.db_operations import insert_invoice, get_product_by_barcode, get_product_by_name, get_all_customers
from datetime import datetime


class CreateInvoiceWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()
        self.load_customers()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        grid_layout = QGridLayout()

        # Add form fields for customer and invoice details
        self.customer_name_input = QComboBox(self)
        self.customer_name_input.setPlaceholderText("Select Customer")

        self.product_name_input = QLineEdit(self)
        self.product_name_input.setPlaceholderText("Product Name")
        self.product_name_input.textChanged.connect(self.auto_fill_product_data_by_name_real_time)

        self.grand_total_input = QLineEdit(self)
        self.grand_total_input.setPlaceholderText("Grand Total")
        self.grand_total_input.setReadOnly(True)

        self.barcode_input = QLineEdit(self)
        self.barcode_input.setPlaceholderText("Product Barcode")
        self.barcode_input.textChanged.connect(self.auto_fill_product_data_by_barcode_real_time)

        self.company_input = QLineEdit(self)
        self.company_input.setPlaceholderText("Company")

        self.discount_input = QLineEdit(self)
        self.discount_input.setPlaceholderText("Discount")
        self.discount_input.textChanged.connect(self.update_remaining_amount)

        self.brand_input = QLineEdit(self)
        self.brand_input.setPlaceholderText("Brand")

        self.quantity_input = QLineEdit(self)
        self.quantity_input.setPlaceholderText("Quantity")
        self.quantity_input.textChanged.connect(self.update_total_price)

        self.receiving_amount_input = QLineEdit(self)
        self.receiving_amount_input.setPlaceholderText("Receiving Amount")
        self.receiving_amount_input.textChanged.connect(self.update_remaining_amount)

        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText("Product Price")
        self.price_input.textChanged.connect(self.update_total_price)

        self.total_input = QLineEdit(self)
        self.total_input.setPlaceholderText("Total")
        self.total_input.setReadOnly(True)

        self.remaining_amount_input = QLineEdit(self)
        self.remaining_amount_input.setPlaceholderText("Remaining Amount")
        self.remaining_amount_input.setReadOnly(True)

        # Add a table for product selection
        self.products_input = QTableWidget(self)
        self.products_input.setColumnCount(7)
        self.products_input.setHorizontalHeaderLabels(['Product', 'Brand', 'Company', 'Quantity', 'Price', 'Total', 'Remove'])

        # Stretch columns evenly across the table width
        header = self.products_input.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Buttons for adding items and creating invoice
        self.add_item_btn = QPushButton("Add Item", self)
        self.add_item_btn.clicked.connect(self.add_item)

        self.create_btn = QPushButton("Create Invoice", self)
        self.create_btn.clicked.connect(self.save_invoice)

        # Add Clear button
        self.clear_btn = QPushButton("Clear", self)
        self.clear_btn.clicked.connect(self.clear_invoice)

        # Arrange inputs in a grid layout
        grid_layout.addWidget(QLabel("Customer Name:"), 0, 0)
        grid_layout.addWidget(self.customer_name_input, 0, 1)

        grid_layout.addWidget(QLabel("Product Name:"), 0, 2)
        grid_layout.addWidget(self.product_name_input, 0, 3)

        grid_layout.addWidget(QLabel("Grand Total:"), 0, 4)
        grid_layout.addWidget(self.grand_total_input, 0, 5)

        grid_layout.addWidget(QLabel("Barcode:"), 1, 0)
        grid_layout.addWidget(self.barcode_input, 1, 1)

        grid_layout.addWidget(QLabel("Company:"), 1, 2)
        grid_layout.addWidget(self.company_input, 1, 3)

        grid_layout.addWidget(QLabel("Discount:"), 1, 4)
        grid_layout.addWidget(self.discount_input, 1, 5)

        grid_layout.addWidget(QLabel("Brand:"), 2, 0)
        grid_layout.addWidget(self.brand_input, 2, 1)

        grid_layout.addWidget(QLabel("Quantity:"), 2, 2)
        grid_layout.addWidget(self.quantity_input, 2, 3)

        grid_layout.addWidget(QLabel("Receiving Amount:"), 2, 4)
        grid_layout.addWidget(self.receiving_amount_input, 2, 5)

        grid_layout.addWidget(QLabel("Product Price:"), 3, 0)
        grid_layout.addWidget(self.price_input, 3, 1)

        grid_layout.addWidget(QLabel("Total:"), 3, 2)
        grid_layout.addWidget(self.total_input, 3, 3)

        grid_layout.addWidget(QLabel("Remaining Amount:"), 3, 4)
        grid_layout.addWidget(self.remaining_amount_input, 3, 5)

        # Add inputs to the main layout
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(QLabel("Products:"))
        main_layout.addWidget(self.products_input)

        # Create a horizontal layout for buttons and add buttons to it
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.add_item_btn)
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.clear_btn)

        # Add button layout to the main layout
        main_layout.addLayout(button_layout)

    def load_customers(self):
        customers = get_all_customers()
        self.customer_name_input.clear()
        for customer in customers:
            self.customer_name_input.addItem(customer.name, customer)

    def auto_fill_product_data_by_barcode_real_time(self):
        barcode = self.barcode_input.text().strip()
        if barcode:
            product = get_product_by_barcode(barcode)
            if product:
                self.product_name_input.setText(product.name)
                self.brand_input.setText(product.brand)
                self.company_input.setText(product.company)
                self.price_input.setText(str(product.sel_price))
                self.quantity_input.setText("1")
                self.update_total_price()

    def auto_fill_product_data_by_name_real_time(self):
        product_name = self.product_name_input.text().strip()
        if product_name:
            product = get_product_by_name(product_name)
            if product:
                self.product_name_input.setText(product.name)
                self.brand_input.setText(product.brand)
                self.company_input.setText(product.company)
                self.price_input.setText(str(product.sel_price))
                self.barcode_input.setText(product.barcode)
                self.quantity_input.setText("1")
                self.update_total_price()

    def add_item(self):
        if not self.product_name_input.text() or not self.barcode_input.text():
            QMessageBox.warning(self, "Error", "Please fill in the product name or barcode.")
            return

        row_position = self.products_input.rowCount()
        self.products_input.insertRow(row_position)

        # Calculate total based on price and quantity inputs
        price = float(self.price_input.text() or 0)
        quantity = int(self.quantity_input.text() or 0)
        total = price * quantity
        self.products_input.setItem(row_position, 0, QTableWidgetItem(self.product_name_input.text()))
        self.products_input.setItem(row_position, 1, QTableWidgetItem(self.brand_input.text()))
        self.products_input.setItem(row_position, 2, QTableWidgetItem(self.company_input.text()))
        self.products_input.setItem(row_position, 3, QTableWidgetItem(str(quantity)))
        self.products_input.setItem(row_position, 4, QTableWidgetItem(str(price)))
        self.products_input.setItem(row_position, 5, QTableWidgetItem(str(total)))

        # Create "Remove" button for each row
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.remove_item(row_position))
        self.products_input.setCellWidget(row_position, 6, remove_btn)

        # Update the grand total after adding the item
        self.update_grand_total()

    def update_total_price(self):
        price = float(self.price_input.text() or 0)
        quantity = int(self.quantity_input.text() or 1)
        total = price * quantity
        self.total_input.setText(str(total))

    def update_grand_total(self):
        grand_total = 0.0
        for row in range(self.products_input.rowCount()):
            grand_total += float(self.products_input.item(row, 5).text())

        self.grand_total_input.setText(str(grand_total))

        # Automatically update remaining amount
        self.update_remaining_amount()

    def update_remaining_amount(self):
        grand_total = float(self.grand_total_input.text() or 0)
        discount = float(self.discount_input.text() or 0)
        receiving_amount = float(self.receiving_amount_input.text() or 0)
        remaining_amount = grand_total - discount - receiving_amount

        self.remaining_amount_input.setText(str(remaining_amount))

    def remove_item(self, row):
        self.products_input.removeRow(row)
        self.update_grand_total()

    def clear_invoice(self):
        self.customer_name_input.clear()
        self.product_name_input.clear()
        self.brand_input.clear()
        self.company_input.clear()
        self.barcode_input.clear()
        self.price_input.clear()
        self.quantity_input.clear()
        self.total_input.clear()
        self.discount_input.clear()
        self.receiving_amount_input.clear()
        self.grand_total_input.clear()
        self.remaining_amount_input.clear()

        # Clear the product table
        self.products_input.setRowCount(0)

    def save_invoice(self):
        invoice_items = []
        for row in range(self.products_input.rowCount()):
            product_name = self.products_input.item(row, 0).text()
            brand = self.products_input.item(row, 1).text()
            company = self.products_input.item(row, 2).text()
            quantity = int(self.products_input.item(row, 3).text())
            price = float(self.products_input.item(row, 4).text())
            total = float(self.products_input.item(row, 5).text())
            invoice_items.append({
                'product_name': product_name,
                'brand': brand,
                'company': company,
                'quantity': quantity,
                'sell_price': price,
                'total_price': total
            })

        customer_name = self.customer_name_input.currentText()
        invoice_date = datetime.today().strftime('%Y-%m-%d')
        grand_total = float(self.grand_total_input.text())
        discount = float(self.discount_input.text()) if self.discount_input.text() else 0.0
        receiving_amount = float(self.receiving_amount_input.text()) if self.receiving_amount_input.text() else 0.0
        remaining_amount = grand_total - discount - receiving_amount

        # Check if all required fields are filled
        if customer_name and invoice_items:
            invoice_data = {
                'customer_name': customer_name,
                'current_date': invoice_date,
                'grand_total': grand_total,
                'discount': discount,
                'receiving_amount': receiving_amount,
                'remaining_amount': remaining_amount,
                'items': invoice_items
            }
            insert_invoice(invoice_data)
            QMessageBox.information(self, "Success", "Invoice created successfully!")
            self.clear_invoice()
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields and try again.")
