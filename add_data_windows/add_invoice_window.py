#show_data_windows/add_invoice_window.py
import os
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, QTableWidget, QPushButton, QMessageBox,
                               QTableWidgetItem, QGridLayout, QHBoxLayout, QHeaderView, QDateEdit)
from add_data_windows.save_invoice_pdf import save_invoice_as_pdf
from db_config.db_operations import (insert_invoice, get_product_by_name, get_total_counts, update_invoice)
from datetime import datetime
from add_data_windows.product_selection_dialog import ProductSelectionDialog


class CreateInvoiceWindow(QWidget):
    signal_created = Signal()

    def __init__(self, invoice=None, parent=None):
        super().__init__(parent)
        self.invoice = invoice
        self.init_ui()
        self.load_data()

        if self.invoice is not None:
            self.load_invoice_data()

        self.product_selection_dialog = ProductSelectionDialog(self)
        self.product_selection_dialog.product_selected.connect(self.fill_product_fields)

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        grid_layout = QGridLayout()

        # Add form fields for customer and invoice details
        self.select_product_btn = QPushButton("Select Product", self)
        self.select_product_btn.clicked.connect(self.open_product_selection_dialog)

        self.product_name_input = QLineEdit(self)
        self.product_name_input.setPlaceholderText("Product Name")
        self.product_name_input.textChanged.connect(self.fill_product_data_by_name)

        self.company_input = QLineEdit(self)
        self.company_input.setPlaceholderText("Company")

        self.quantity_input = QLineEdit(self)
        self.quantity_input.setPlaceholderText("Quantity")
        self.quantity_input.textChanged.connect(self.update_total_price)

        self.customer_name_input = QLineEdit(self)
        self.customer_name_input.setPlaceholderText("Select Customer")

        self.price_input = QLineEdit(self)
        self.price_input.setPlaceholderText("Product Price")
        self.price_input.textChanged.connect(self.update_total_price)

        self.total_input = QLineEdit(self)
        self.total_input.setPlaceholderText("Total")
        self.total_input.setReadOnly(True)

        self.discount_input = QLineEdit(self)
        self.discount_input.setPlaceholderText("Discount")
        self.discount_input.textChanged.connect(self.update_remaining_amount)

        self.current_date_input = QDateEdit(self)
        self.current_date_input.setCalendarPopup(True)
        self.current_date_input.setDate(datetime.today())

        self.receiving_amount_input = QLineEdit(self)
        self.receiving_amount_input.setPlaceholderText("Receiving Amount")
        self.receiving_amount_input.textChanged.connect(self.update_remaining_amount)

        self.remaining_amount_input = QLineEdit(self)
        self.remaining_amount_input.setPlaceholderText("Remaining Amount")
        self.remaining_amount_input.setReadOnly(True)

        self.grand_total_input = QLineEdit(self)
        self.grand_total_input.setPlaceholderText("Grand Total")
        self.grand_total_input.setReadOnly(True)

        self.total_products_input = QLineEdit(self)
        self.total_products_input.setPlaceholderText("Total Products")
        self.total_products_input.setReadOnly(True)

        self.total_customers_input = QLineEdit(self)
        self.total_customers_input.setPlaceholderText("Total Customers")
        self.total_customers_input.setReadOnly(True)

        self.total_invoices_input = QLineEdit(self)
        self.total_invoices_input.setPlaceholderText("Total Invoices")
        self.total_invoices_input.setReadOnly(True)

        # Buttons for adding items and creating invoice
        self.add_item_btn = QPushButton("Add Item", self)
        self.add_item_btn.clicked.connect(self.add_item)

        self.create_btn = QPushButton("Create Invoice", self)

        if self.invoice is not None:
            self.create_btn.setText("Update Invoice")
            self.create_btn.clicked.connect(self.update_invoice)
        else:
            self.create_btn.setText("Create Invoice")
            self.create_btn.clicked.connect(self.save_invoice)

        # Add Clear button
        self.clear_btn = QPushButton("Clear", self)
        self.clear_btn.clicked.connect(self.clear_invoice)

        # Add a table for product selection
        self.products_input = QTableWidget(self)
        self.products_input.setColumnCount(6)
        self.products_input.setHorizontalHeaderLabels(['Product', 'Company', 'Quantity', 'Price', 'Total', 'Remove'])

        # Stretch columns evenly across the table width
        header = self.products_input.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        # Arrange inputs in a grid layout
        grid_layout.addWidget(QLabel("Product:"), 0, 0)
        grid_layout.addWidget(self.select_product_btn, 0, 1)

        grid_layout.addWidget(QLabel("Product Name:"), 1, 0)
        grid_layout.addWidget(self.product_name_input, 1, 1)

        grid_layout.addWidget(QLabel("Company:"), 2, 0)
        grid_layout.addWidget(self.company_input, 2, 1)

        grid_layout.addWidget(QLabel("Quantity:"), 3, 0)
        grid_layout.addWidget(self.quantity_input, 3, 1)

        grid_layout.addWidget(QLabel("Customer:"), 0, 2)
        grid_layout.addWidget(self.customer_name_input, 0, 3)

        grid_layout.addWidget(QLabel("Product Price:"), 1, 2)
        grid_layout.addWidget(self.price_input, 1, 3)

        grid_layout.addWidget(QLabel("Total:"), 2, 2)
        grid_layout.addWidget(self.total_input, 2, 3)

        grid_layout.addWidget(QLabel("Discount:"), 3, 2)
        grid_layout.addWidget(self.discount_input, 3, 3)

        grid_layout.addWidget(QLabel("Select Date:"), 0, 4)
        grid_layout.addWidget(self.current_date_input, 0, 5)

        grid_layout.addWidget(QLabel("Receiving Amount:"), 1, 4)
        grid_layout.addWidget(self.receiving_amount_input, 1, 5)

        grid_layout.addWidget(QLabel("Remaining Amount:"), 2, 4)
        grid_layout.addWidget(self.remaining_amount_input, 2, 5)

        grid_layout.addWidget(QLabel("Grand Total:"), 3, 4)
        grid_layout.addWidget(self.grand_total_input, 3, 5)

        grid_layout.addWidget(QLabel("Total Pro/Qty:"), 1, 6)
        grid_layout.addWidget(self.total_products_input, 1, 7)

        grid_layout.addWidget(QLabel("Total Customers:"), 2, 6)
        grid_layout.addWidget(self.total_customers_input, 2, 7)

        grid_layout.addWidget(QLabel("Total Invoices:"), 3, 6)
        grid_layout.addWidget(self.total_invoices_input, 3, 7)

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

    def load_data(self):
        totals = get_total_counts()
        self.total_products_input.setText(str(totals['total_products']))
        self.total_customers_input.setText(str(totals['total_customers']))
        self.total_invoices_input.setText(str(totals['total_invoices']))

    def open_product_selection_dialog(self):
        self.product_selection_dialog.load_products()
        self.product_selection_dialog.exec_()

    def fill_product_fields(self, product_data):
        self.product_name_input.setText(product_data['name'])
        self.company_input.setText(product_data['company'])
        self.price_input.setText(str(product_data['price']))
        self.quantity_input.setText("1")
        self.update_total_price()

        self.total_products_input.setText(str(product_data['quantity']))
        self.update_total_price()

    def fill_product_data_by_name(self):
        product_name = self.product_name_input.text().strip()
        if product_name:
            product = get_product_by_name(product_name)
            if product:
                self.product_name_input.setText(product.name)
                self.company_input.setText(product.company)
                self.price_input.setText(str(product.sel_price))
                self.quantity_input.setText("1")
                self.update_total_price()

    def add_item(self):
        if not self.product_name_input.text() or not self.company_input.text():
            QMessageBox.warning(self, "Error", "Please fill in the product name or company.")
            return

        quantity = int(self.quantity_input.text())
        total_quantity = int(self.total_products_input.text())

        if quantity > total_quantity:
            QMessageBox.warning(self, "Error", "Quantity Not available in stock.")
            return

        available_stock = total_quantity - quantity
        self.total_products_input.setText(str(available_stock))

        price = float(self.price_input.text() or 0)
        total = price * quantity
        row_position = self.products_input.rowCount()
        self.products_input.insertRow(row_position)

        self.products_input.setItem(row_position, 0, QTableWidgetItem(self.product_name_input.text()))
        self.products_input.setItem(row_position, 1, QTableWidgetItem(self.company_input.text()))
        self.products_input.setItem(row_position, 2, QTableWidgetItem(str(quantity)))
        self.products_input.setItem(row_position, 3, QTableWidgetItem(str(price)))
        self.products_input.setItem(row_position, 4, QTableWidgetItem(str(total)))

        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(lambda: self.remove_item(row_position))
        self.products_input.setCellWidget(row_position, 5, remove_btn)

        self.update_grand_total()

    def update_total_price(self):
        price = float(self.price_input.text() or 0)
        quantity = int(self.quantity_input.text() or 1)
        total = round(price * quantity, 2)
        self.total_input.setText(f"{total:.2f}")

    def update_grand_total(self):
        grand_total = 0.0
        for row in range(self.products_input.rowCount()):
            grand_total += float(self.products_input.item(row, 4).text())

        grand_total = round(grand_total, 2)
        self.grand_total_input.setText(f"{grand_total:.2f}")
        self.update_remaining_amount()

    def update_remaining_amount(self):
        grand_total = float(self.grand_total_input.text() or 0)
        discount = float(self.discount_input.text() or 0)
        receiving_amount = float(self.receiving_amount_input.text() or 0)
        remaining_amount = round(grand_total - discount - receiving_amount, 2)
        self.remaining_amount_input.setText(f"{remaining_amount:.2f}")

    def remove_item(self, row):
        self.products_input.removeRow(row)
        self.update_grand_total()

    def clear_invoice(self):
        self.customer_name_input.clear()
        self.product_name_input.clear()
        self.company_input.clear()
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
            company = self.products_input.item(row, 1).text()
            quantity = int(self.products_input.item(row, 2).text())
            price = float(self.products_input.item(row, 3).text())
            total = float(self.products_input.item(row, 4).text())
            invoice_items.append({'product_name': product_name, 'company': company, 'quantity': quantity,
                                  'sell_price': round(price, 2), 'total_price': round(total, 2)})

        customer_name = self.customer_name_input.text() if self.customer_name_input.text() else 'N/N'
        invoice_date = self.current_date_input.date().toString("yyyy-MM-dd")
        grand_total = float(self.grand_total_input.text())
        discount = float(self.discount_input.text()) if self.discount_input.text() else 0.0
        receiving_amount = float(self.receiving_amount_input.text()) if self.receiving_amount_input.text() else 0.0
        remaining_amount = grand_total - discount - receiving_amount

        # Check if all required fields are filled
        if grand_total and invoice_items:
            invoice_data = {'customer_name': customer_name, 'current_date': invoice_date,
                            'grand_total': round(grand_total, 2), 'discount': round(discount, 2),
                            'receiving_amount': round(receiving_amount, 2),
                            'remaining_amount': round(remaining_amount, 2), 'items': invoice_items
            }
            reply = QMessageBox.question(self, "Save Invoice", "Want to create invoice!",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                insert_invoice(invoice_data)
                self.save_invoice_pdf(invoice_data)
                self.clear_invoice()
                self.signal_created.emit()
            else:
                return
        else:
            QMessageBox.warning(self, "Error", "Please fill in all fields and try again.")

    def save_invoice_pdf(self, invoice_data):
        output_dir = "pdf_invoices"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        reply = QMessageBox.question(self, "Save PDF", "Do you want to save this invoice as a PDF?",
                                     QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            save_invoice_as_pdf(invoice_data, output_dir)
            QMessageBox.information(self, "PDF Saved", "Invoice saved as PDF successfully.")

    def load_invoice_data(self):
        self.customer_name_input.setText(str(self.invoice.customer_name))
        if isinstance(self.invoice.current_date, str):
            invoice_date = datetime.strptime(self.invoice.current_date, "%Y-%m-%d").date()
            self.current_date_input.setDate(invoice_date)
        elif isinstance(self.invoice.current_date, datetime):
            self.current_date_input.setDate(self.invoice.current_date.date())
        self.discount_input.setText(str(self.invoice.discount))
        self.receiving_amount_input.setText(str(self.invoice.receiving_amount))
        self.grand_total_input.setText(str(self.invoice.grand_total))
        self.remaining_amount_input.setText(str(self.invoice.remaining_amount))

        # Populate the product table
        self.products_input.setRowCount(0)
        for item in self.invoice.invoice_with_item:
            row_position = self.products_input.rowCount()
            self.products_input.insertRow(row_position)
            self.products_input.setItem(row_position, 0, QTableWidgetItem(item.product_name))
            self.products_input.setItem(row_position, 1, QTableWidgetItem(item.company))
            self.products_input.setItem(row_position, 2, QTableWidgetItem(str(item.quantity)))
            self.products_input.setItem(row_position, 3, QTableWidgetItem(str(item.sell_price)))
            self.products_input.setItem(row_position, 4, QTableWidgetItem(str(item.total_price)))

            remove_btn = QPushButton("Remove")
            remove_btn.clicked.connect(lambda _, r=row_position: self.remove_item(r))
            self.products_input.setCellWidget(row_position, 5, remove_btn)

        self.update_grand_total()

    def update_invoice(self):
        invoice_items = []
        for row in range(self.products_input.rowCount()):
            product_name = self.products_input.item(row, 0).text()
            company = self.products_input.item(row, 1).text()
            quantity = int(self.products_input.item(row, 2).text())
            price = float(self.products_input.item(row, 3).text())
            total = float(self.products_input.item(row, 4).text())
            invoice_items.append({'product_name': product_name, 'company': company, 'quantity': quantity,
                                  'sell_price': round(price, 2), 'total_price': round(total, 2)})

        customer_name = self.customer_name_input.text() if self.customer_name_input.text() else 'N/N'
        invoice_date_qdate = self.current_date_input.date()
        invoice_date = invoice_date_qdate.toString("yyyy-MM-dd")
        grand_total = float(self.grand_total_input.text())
        discount = float(self.discount_input.text()) if self.discount_input.text() else 0.0
        receiving_amount = float(self.receiving_amount_input.text()) if self.receiving_amount_input.text() else 0.0
        remaining_amount = grand_total - discount - receiving_amount

        # Create the updated invoice data structure
        updated_invoice_data = {'id': self.invoice.id, 'customer_name': customer_name, 'current_date': invoice_date,
                                'grand_total': round(grand_total, 2), 'discount': round(discount, 2),
                                'receiving_amount': round(receiving_amount, 2),
                                'remaining_amount': round(remaining_amount, 2), 'items': invoice_items}

        reply = QMessageBox.question(self, "Update Invoice", "You want to update this invoice?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            update_invoice(updated_invoice_data)
            self.save_invoice_pdf(updated_invoice_data)
            self.signal_created.emit()
            self.clear_invoice()
        else:
            return
