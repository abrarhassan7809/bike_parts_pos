# main_window.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QToolBar, QComboBox, QMessageBox, QDialog, QTableWidget,
                               QTableWidgetItem, QHeaderView, QPushButton, QLineEdit, QWidget, QSizePolicy)
from all_product_window import AllProductWindow
from insert_product_window import InsertProductDialog
from create_invoice_window import CreateInvoiceWindow
from invoices_window import InvoicesWindow
from update_product_window import UpdateProductDialog
from tab_manager import TabManager
from db_operations import (insert_product, update_product, delete_product, get_all_products, get_product_by_barcode,
                           get_all_invoices, get_invoice_by_id)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atoms POS System")
        self.setGeometry(200, 200, 1024, 768)
        self.button_style = "min-width: 100px; min-height: 35px;"

        self.tab_manager = TabManager(self)
        self.setCentralWidget(self.tab_manager)

        self.toolbar = self.create_toolbar()
        self.all_products = []
        self.all_invoices = []
        self.load_all_products()

    def create_toolbar(self):
        toolbar = QToolBar("Operations")
        self.addToolBar(toolbar)

        # Add dropdown menu
        dropdown = QComboBox(self)
        dropdown.addItems(["Select Options", "All Products", "Incoices"])
        dropdown.setStyleSheet(self.button_style)
        dropdown.setItemData(0, False, Qt.UserRole - 1)
        dropdown.currentIndexChanged.connect(self.on_dropdown_change)
        toolbar.addWidget(dropdown)

        add_product_window = QPushButton("Add Product", self)
        add_product_window.setStyleSheet(self.button_style)
        add_product_window.clicked.connect(lambda: self.show_insert_tab())
        toolbar.addWidget(add_product_window)

        update_product_window = QPushButton("Update Product", self)
        update_product_window.setStyleSheet(self.button_style)
        update_product_window.clicked.connect(lambda: self.show_update_tab())
        toolbar.addWidget(update_product_window)

        invoice_button = QPushButton("Create Invoice", self)
        invoice_button.setStyleSheet(self.button_style)
        invoice_button.clicked.connect(lambda: self.create_invoice_tab())
        toolbar.addWidget(invoice_button)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        self.search_bar = QLineEdit(self)
        self.search_bar.setFixedWidth(300)
        self.search_bar.setPlaceholderText("Search Product...")
        self.search_bar.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.search_bar.textChanged.connect(self.filter_products)
        toolbar.addWidget(self.search_bar)

        return toolbar

    def load_all_products(self):
        self.all_products = get_all_products()
        self.update_product_table(self.all_products)
        self.show_all_products_tab()

    def load_all_invoices(self):
        self.all_invoices = get_all_invoices()
        self.show_invoices_tab()

    def on_dropdown_change(self, index):
        if index == 0:
            return
        elif index == 1:
            self.show_all_products_tab()
        elif index == 2:
            self.show_invoices_tab()

    def show_all_products_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "All Products":
                self.tab_manager.setCurrentIndex(index)
                self.update_product_table(self.all_products)
                return

        products_tab = AllProductWindow(self)
        self.tab_manager.add_new_tab("All Products", products_tab)
        self.update_product_table(self.all_products)

    def show_invoices_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Invoices":
                self.tab_manager.setCurrentIndex(index)
                return

        invoices_tab = InvoicesWindow(self)
        self.tab_manager.add_new_tab("Invoices", invoices_tab)

    def create_invoice_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Create Invoice":
                self.tab_manager.setCurrentIndex(index)
                return

        invoice_widget = CreateInvoiceWindow(self)
        self.tab_manager.add_new_tab("Create Invoice", invoice_widget)

    def update_product_table(self, products):
        all_products_tab = self.findChild(AllProductWindow)
        if all_products_tab:
            table_widget = all_products_tab.table_widget
            table_widget.setRowCount(len(products))
            table_widget.setColumnCount(7)
            table_widget.setHorizontalHeaderLabels(
                ['Name', 'Barcode', 'Purchase Price', 'Sell Price', 'Quantity', 'Update', 'Remove'])

            for row, product in enumerate(products):
                table_widget.setItem(row, 0, QTableWidgetItem(product.name))
                table_widget.setItem(row, 1, QTableWidgetItem(product.barcode))
                table_widget.setItem(row, 2, QTableWidgetItem(str(product.pur_price)))
                table_widget.setItem(row, 3, QTableWidgetItem(str(product.sel_price)))
                table_widget.setItem(row, 4, QTableWidgetItem(str(product.quantity)))

                # Create Edit button
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda _, b=product.barcode: self.show_update_tab(b))
                table_widget.setCellWidget(row, 5, edit_button)

                # Create Delete button
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, p_id=product.id: self.delete_product(p_id))
                table_widget.setCellWidget(row, 6, delete_button)

            table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            table_widget.horizontalHeader().setStretchLastSection(True)
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_invoice_table(self, invoices):
        invoices_tab = self.findChild(InvoicesWindow)
        if invoices_tab:
            invoice_table = invoices_tab.invoice_table
            invoice_table.setRowCount(len(invoices))
            invoice_table.setColumnCount(5)
            invoice_table.setHorizontalHeaderLabels(
                ['Invoice ID', 'Customer Name', 'Date', 'Total Amount', 'Details'])

            for row, invoice in enumerate(invoices):
                invoice_table.setItem(row, 0, QTableWidgetItem(str(invoice.id)))
                invoice_table.setItem(row, 1, QTableWidgetItem(invoice.customer_name))
                invoice_table.setItem(row, 2, QTableWidgetItem(invoice.date))
                invoice_table.setItem(row, 3, QTableWidgetItem(str(invoice.total_amount)))

                # Create a Details button
                details_button = QPushButton("View Details")
                details_button.clicked.connect(lambda _, i_id=invoice.id: self.show_invoice_details(i_id))
                invoice_table.setCellWidget(row, 4, details_button)

            invoice_table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            invoice_table.horizontalHeader().setStretchLastSection(True)
            invoice_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def filter_products(self):
        search_text = self.search_bar.text().strip()
        filtered_products = []
        if search_text:
            filtered_products = [product for product in self.all_products if
                                 search_text in product.barcode or search_text.lower() in product.name.lower()]
        else:
            filtered_products = self.all_products

        self.update_product_table(filtered_products)

    def show_invoice_details(self, invoice_id):
        invoice = get_invoice_by_id(invoice_id)
        if invoice:
            details_message = f"Invoice ID: {invoice.id}\nCustomer Name: {invoice.customer_name}\nDate: {invoice.date}\nTotal Amount: {invoice.total_amount}\nItems:\n"
            for item in invoice.items:
                details_message += f"{item.product_name} - Quantity: {item.quantity}, Price: {item.price}\n"

            QMessageBox.information(self, "Invoice Details", details_message)
        else:
            QMessageBox.warning(self, "Error", "Invoice details not found.")

    def show_insert_tab(self):
        dialog = InsertProductDialog(self)
        if dialog.exec() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            name, barcode, pur_price, sel_price, quantity = (
                product_data['name'],
                product_data['barcode'],
                product_data['pur_price_input'],
                product_data['sel_price_input'],
                product_data['quantity']
            )
            if name and barcode and pur_price and sel_price and quantity:
                insert_product(name, barcode, pur_price, sel_price, quantity)
                QMessageBox.information(self, "Success", "Product inserted successfully!")

                self.load_all_products()  # Reload products
                self.update_product_table(self.all_products)  # Refresh table
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def show_update_tab(self, barcode=None):
        dialog = UpdateProductDialog(self, barcode)
        if dialog.exec() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            barcode, name, pur_price, sel_price, quantity = (
                product_data['barcode'],
                product_data['name'],
                product_data['pur_price'],
                product_data['sel_price'],
                product_data['quantity']
            )
            if barcode and name and pur_price and sel_price and quantity:
                existing_product = get_product_by_barcode(barcode)
                if existing_product:
                    update_product(existing_product.id, name, barcode, pur_price, sel_price, quantity)
                    QMessageBox.information(self, "Success", "Product updated successfully!")

                    self.load_all_products()
                    self.update_product_table(self.all_products)
                else:
                    QMessageBox.warning(self, "Error", "No product found with the provided barcode.")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def delete_product(self, product_id):
        response = QMessageBox.question(self, "Confirm Delete",
                                         f"Are you sure you want to delete product ID {product_id}?",
                                         QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            delete_product(product_id)
            self.load_all_products()
