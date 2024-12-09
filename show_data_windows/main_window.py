#show_data_windows/main_window.py
import os.path
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QMainWindow, QToolBar, QComboBox, QMessageBox, QDialog, QPushButton)
from add_data_windows.add_customer_window import InsertCustomerDialog
from add_data_windows.add_supplier_window import InsertSupplierDialog
from show_data_windows.products_window import AllProductWindow
from add_data_windows.add_product_window import InsertProductDialog
from add_data_windows.add_invoice_window import CreateInvoiceWindow
from show_data_windows.customers_window import CustomerWindow
from show_data_windows.dashboard_window import DashboardWindow
from show_data_windows.invoices_window import InvoicesWindow
from add_data_windows.update_product_window import UpdateProductDialog
from show_data_windows.inventories_window import ShowInventoryWindow
from show_data_windows.create_multi_invoice_tabs import CreateMultiInvoiceTabs
from show_data_windows.suppliers_window import SupplierWindow
from tab_manager import TabManager
from db_config.db_operations import (update_product, get_all_products, get_invoice_by_id, insert_supplier,
                                     insert_customer, insert_or_update_product)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atoms POS System")
        # self.setGeometry(200, 200, 1024, 768)
        self.setWindowIcon(QIcon(os.path.abspath("atom_icon_1.ico")))
        self.button_style = "min-width: 100px; min-height: 35px;"

        self.tab_manager = TabManager(self)
        self.setCentralWidget(self.tab_manager)

        self.toolbar = self.create_toolbar()
        self.all_products = []
        self.load_dashboard_tab()

    def create_toolbar(self):
        toolbar = QToolBar("Operations")
        self.addToolBar(toolbar)

        dashboard_button = QPushButton("Dashboard", self)
        dashboard_button.setStyleSheet(self.button_style)
        dashboard_button.clicked.connect(self.load_dashboard_tab)
        toolbar.addWidget(dashboard_button)

        # Add dropdown menu
        tab_dropdown = QComboBox(self)
        tab_dropdown.addItems(["Select Window", "Show Products", "Show Customers", "Show Suppliers", "Show Invoices",
                               "Show Inventory"])
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

        return toolbar

    def load_dashboard_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Dashboard":
                self.tab_manager.setCurrentIndex(index)
                return

        dashboard_tab = DashboardWindow(self)
        self.tab_manager.add_new_tab("Dashboard", dashboard_tab)

    def load_all_products(self):
        self.all_products = get_all_products()
        self.show_all_products_tab()

    def select_dropdown_window(self, index):
        if index == 0:
            return
        elif index == 1:
            self.load_all_products()
        elif index == 2:
            self.show_customer_tab()
        elif index == 3:
            self.show_supplier_tab()
        elif index == 4:
            self.show_invoices_tab()
        elif index == 5:
            self.show_inventory_tab()

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
            if self.tab_manager.tabText(index) == "Products":
                self.tab_manager.setCurrentIndex(index)
                return

        products_tab = AllProductWindow(self)
        products_tab.signal_created.connect(self.refresh_all_tabs)
        self.tab_manager.add_new_tab("Products", products_tab)

    def show_invoices_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Invoices":
                self.tab_manager.setCurrentIndex(index)
                return

        invoices_tab = InvoicesWindow(self, self.tab_manager)
        invoices_tab.signal_created.connect(self.refresh_all_tabs)
        self.tab_manager.add_new_tab("Invoices", invoices_tab)

    def create_invoice_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Create Invoice":
                self.tab_manager.setCurrentIndex(index)
                return

        invoice_widget = CreateMultiInvoiceTabs(invoice=None, parent=self)
        invoice_widget.signal_created.connect(self.refresh_all_tabs)
        self.tab_manager.add_new_tab("Create Invoice", invoice_widget)

    def show_inventory_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Inventory":
                self.tab_manager.setCurrentIndex(index)
                return

        inventory_widget = ShowInventoryWindow(self)
        inventory_widget.signal_created.connect(self.refresh_all_tabs)
        self.tab_manager.add_new_tab("Inventory", inventory_widget)

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
        dialog.signal_created.connect(self.refresh_all_tabs)
        if dialog.exec() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            if product_data:
                message = insert_or_update_product(product_data)
                QMessageBox.information(self, "Success", f"{message}")
                self.refresh_all_tabs()

                for index in range(self.tab_manager.count()):
                    widget = self.tab_manager.widget(index)
                    if isinstance(widget, AllProductWindow) and self.tab_manager.tabText(index) == "Products":
                        widget.load_all_products()
                        break
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def show_update_tab(self, p_id=None):
        dialog = UpdateProductDialog(self, p_id)
        if dialog.exec() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            if product_data:
                update_product(product_data['p_id'], product_data['name'], product_data['company'],
                               product_data['rank_number'], product_data['pur_price'], product_data['sel_price'],
                               product_data['quantity'])
                QMessageBox.information(self, "Success", "Product updated successfully!")
                self.refresh_all_tabs()

                for index in range(self.tab_manager.count()):
                    print('index is: ', index)
                    widget = self.tab_manager.widget(index)
                    if isinstance(widget, AllProductWindow) and self.tab_manager.tabText(index) == "Products":
                        widget.load_all_products()
                        break
            else:
                QMessageBox.warning(self, "Error", "No product found with the provided barcode.")

    def add_supplier_dialog(self):
        dialog = InsertSupplierDialog(self)
        if dialog.exec() == QDialog.Accepted:
            supplier_data = dialog.get_supplier_data()
            if all(supplier_data.values()):
                insert_supplier(**supplier_data)
                QMessageBox.information(self, "Success", "Supplier added successfully!")
                self.refresh_all_tabs()

                for index in range(self.tab_manager.count()):
                    widget = self.tab_manager.widget(index)
                    if isinstance(widget, SupplierWindow) and self.tab_manager.tabText(index) == "Supplier":
                        widget.load_all_supplier()
                        break
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def show_supplier_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Supplier":
                self.tab_manager.setCurrentIndex(index)
                return

        supplier_tab = SupplierWindow(self)
        supplier_tab.signal_created.connect(self.refresh_all_tabs)
        self.tab_manager.add_new_tab("Supplier", supplier_tab)

    def add_customer_dialog(self):
        dialog = InsertCustomerDialog(self)
        if dialog.exec() == QDialog.Accepted:
            customer_data = dialog.get_customer_data()
            if all(customer_data.values()):
                insert_customer(**customer_data)
                QMessageBox.information(self, "Success", "Customer added successfully!")
                self.refresh_all_tabs()

                for index in range(self.tab_manager.count()):
                    widget = self.tab_manager.widget(index)
                    if isinstance(widget, CustomerWindow) and self.tab_manager.tabText(index) == "Customer":
                        widget.load_all_customer()
                        break
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def show_customer_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "Customer":
                self.tab_manager.setCurrentIndex(index)
                return

        customer_tab = CustomerWindow(self)
        customer_tab.signal_created.connect(self.refresh_all_tabs)
        self.tab_manager.add_new_tab("Customer", customer_tab)

    def refresh_all_tabs(self):
        for index in range(self.tab_manager.count()):
            widget = self.tab_manager.widget(index)
            tab_name = self.tab_manager.tabText(index)
            if tab_name == "Dashboard" and isinstance(widget, DashboardWindow):
                widget.load_data()

            elif tab_name == "Products" and isinstance(widget, AllProductWindow):
                widget.load_all_products()

            elif tab_name == "Supplier" and isinstance(widget, SupplierWindow):
                widget.load_all_supplier()

            elif tab_name == "Customer" and isinstance(widget, CustomerWindow):
                widget.load_all_customer()

            elif tab_name == "Invoices" and isinstance(widget, InvoicesWindow):
                widget.load_all_invoices()

            elif tab_name == "Inventory" and isinstance(widget, ShowInventoryWindow):
                widget.load_all_inventory()
