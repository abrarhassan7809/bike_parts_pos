#show_data_windows/main_window.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QMainWindow, QToolBar, QComboBox, QMessageBox, QDialog, QTableWidget,
                               QTableWidgetItem, QHeaderView, QPushButton, QLineEdit, QWidget, QSizePolicy)
from add_data_windows.insert_customer_window import InsertCustomerDialog
from add_data_windows.insert_supplier_window import InsertSupplierDialog
from show_data_windows.all_product_window import AllProductWindow
from add_data_windows.insert_product_window import InsertProductDialog
from show_data_windows.create_invoice_window import CreateInvoiceWindow
from show_data_windows.customer_window import CustomerWindow
from show_data_windows.invoices_window import InvoicesWindow
from add_data_windows.update_product_window import UpdateProductDialog
from show_data_windows.supplier_window import SupplierWindow
from tab_manager import TabManager
from db_config.db_operations import (update_product, delete_product, get_all_products, get_product_by_barcode,
                                     get_all_invoices, get_invoice_by_id, insert_supplier, insert_customer,
                                     insert_or_update_product)


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
        tab_dropdown = QComboBox(self)
        tab_dropdown.addItems(["Select Window", "Show Products", "Show Customers", "Show Suppliers", "Show Invoices",])
        tab_dropdown.setStyleSheet(self.button_style)
        tab_dropdown.setItemData(0, False, Qt.UserRole - 1)
        tab_dropdown.currentIndexChanged.connect(self.select_dropdown_window)
        toolbar.addWidget(tab_dropdown)

        tab_dropdown = QComboBox(self)
        tab_dropdown.addItems(["Select Operations", "Add Product", "Add Customer", "Add Supplier",])
        tab_dropdown.setStyleSheet(self.button_style)
        tab_dropdown.setItemData(0, False, Qt.UserRole - 1)
        tab_dropdown.currentIndexChanged.connect(self.select_dropdown_operation)
        toolbar.addWidget(tab_dropdown)

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

    def select_dropdown_window(self, index):
        if index == 0:
            return
        elif index == 1:
            self.show_all_products_tab()
        elif index == 2:
            self.show_customer_tab()
        elif index == 3:
            self.show_supplier_tab()
        elif index == 4:
            self.show_invoices_tab()

        sender = self.sender()
        if isinstance(sender, QComboBox):
            sender.setCurrentIndex(0)

    def select_dropdown_operation(self, index):
        if index == 0:
            return
        elif index == 1:
            self.add_product_dialog()
        elif index == 2:
            self.add_customer_dialog()
        elif index == 3:
            self.add_supplier_dialog()

        sender = self.sender()
        if isinstance(sender, QComboBox):
            sender.setCurrentIndex(0)

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
            table_widget.setColumnCount(10)
            table_widget.setHorizontalHeaderLabels(
                ['Name', 'Brand', 'Company', 'Rank Number', 'Barcode', 'Purchase Price', 'Sell Price', 'Quantity', 'Update', 'Remove'])

            for row, product in enumerate(products):
                table_widget.setItem(row, 0, QTableWidgetItem(product.name))
                table_widget.setItem(row, 1, QTableWidgetItem(product.brand))
                table_widget.setItem(row, 2, QTableWidgetItem(product.company))
                table_widget.setItem(row, 3, QTableWidgetItem(product.rank_number))
                table_widget.setItem(row, 4, QTableWidgetItem(product.barcode))
                table_widget.setItem(row, 5, QTableWidgetItem(str(product.pur_price)))
                table_widget.setItem(row, 6, QTableWidgetItem(str(product.sel_price)))
                table_widget.setItem(row, 7, QTableWidgetItem(str(product.quantity)))

                # Create Edit button
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda _, b=product.barcode: self.show_update_tab(b))
                table_widget.setCellWidget(row, 8, edit_button)

                # Create Delete button
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda _, p_id=product.id: self.delete_product(p_id))
                table_widget.setCellWidget(row, 9, delete_button)

            table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
            table_widget.horizontalHeader().setStretchLastSection(True)
            table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

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

    def add_product_dialog(self):
        dialog = InsertProductDialog(self)
        if dialog.exec() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            if product_data:
                message = insert_or_update_product(product_data)
                QMessageBox.information(self, "Success", f"{message}")

                self.load_all_products()
                self.update_product_table(self.all_products)
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def show_update_tab(self, barcode=None):
        dialog = UpdateProductDialog(self, barcode)
        if dialog.exec() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            if product_data:
                existing_product = get_product_by_barcode(barcode)
                if existing_product:
                    update_product(**product_data)
                    QMessageBox.information(self, "Success", "Product updated successfully!")

                    self.load_all_products()
                    self.update_product_table(self.all_products)
                else:
                    QMessageBox.warning(self, "Error", "No product found with the provided barcode.")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def add_supplier_dialog(self):
        dialog = InsertSupplierDialog(self)
        if dialog.exec() == QDialog.Accepted:
            supplier_data = dialog.get_supplier_data()
            if all(supplier_data.values()):
                insert_supplier(**supplier_data)
                QMessageBox.information(self, "Success", "Supplier added successfully!")

                for index in range(self.tab_manager.count()):
                    widget = self.tab_manager.widget(index)
                    if isinstance(widget, SupplierWindow) and self.tab_manager.tabText(index) == "Supplier":
                        widget.load_suppliers()
                        break
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def show_supplier_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Supplier":
                self.tab_manager.setCurrentIndex(index)
                return

        supplier_tab = SupplierWindow(self)
        self.tab_manager.add_new_tab("Supplier", supplier_tab)

    def add_customer_dialog(self):
        dialog = InsertCustomerDialog(self)
        if dialog.exec() == QDialog.Accepted:
            customer_data = dialog.get_customer_data()
            if all(customer_data.values()):
                insert_customer(**customer_data)
                QMessageBox.information(self, "Success", "Customer added successfully!")

                for index in range(self.tab_manager.count()):
                    widget = self.tab_manager.widget(index)
                    if isinstance(widget, CustomerWindow) and self.tab_manager.tabText(index) == "Customer":
                        widget.load_customers()
                        break
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def show_customer_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Customer":
                self.tab_manager.setCurrentIndex(index)
                return

        customer_tab = CustomerWindow(self)
        self.tab_manager.add_new_tab("Customer", customer_tab)

    def delete_product(self, product_id):
        response = QMessageBox.question(self, "Confirm Delete",
                                         f"Are you sure you want to delete product ID {product_id}?",
                                         QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            delete_product(product_id)
            self.load_all_products()
