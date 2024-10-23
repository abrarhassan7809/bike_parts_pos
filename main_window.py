# main_window.py
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QMainWindow, QToolBar, QComboBox, QMessageBox, QDialog, QTableWidget,
                               QTableWidgetItem, QHeaderView, QPushButton, QLineEdit, QWidget, QSizePolicy)
from insert_product_dialog import InsertProductDialog
from update_product_dialog import UpdateProductDialog
from tab_manager import TabManager
from db_operations import insert_product, update_product, delete_product, get_all_products, get_product_by_barcode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Atoms POS System")
        self.setGeometry(200, 200, 1024, 768)

        # Initialize tab manager first
        self.tab_manager = TabManager(self)

        # Set central widget as the tab manager
        self.setCentralWidget(self.tab_manager)

        # Initialize toolbar
        self.toolbar = self.create_toolbar()

        # Store all products data for filtering
        self.all_products = []

        # Load all products from the database once at startup
        self.load_all_products()

    def create_toolbar(self):
        toolbar = QToolBar("Operations")
        self.addToolBar(toolbar)

        # Add dropdown menu
        dropdown = QComboBox(self)
        dropdown.addItems(["Select Options", "All Products"])
        dropdown.setItemData(0, False, Qt.UserRole - 1)
        dropdown.currentIndexChanged.connect(self.on_dropdown_change)
        toolbar.addWidget(dropdown)

        add_product_window = QPushButton("Add Product", self)
        add_product_window.clicked.connect(lambda: self.show_insert_tab())
        toolbar.addWidget(add_product_window)

        update_product_window = QPushButton("Update Product", self)
        update_product_window.clicked.connect(lambda: self.show_update_tab())
        toolbar.addWidget(update_product_window)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)

        # Add a search bar for barcode search
        self.search_bar = QLineEdit(self)
        self.search_bar.setFixedWidth(300)
        self.search_bar.setPlaceholderText("Search Product...")
        self.search_bar.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.search_bar.textChanged.connect(self.filter_products)  # Connect textChanged signal
        toolbar.addWidget(self.search_bar)

        return toolbar

    def load_all_products(self):
        self.all_products = get_all_products()  # Load all products once
        self.show_all_products_tab()  # Display products

    def on_dropdown_change(self, index):
        if index == 0:
            return
        elif index == 1:
            self.show_all_products_tab()

    def show_all_products_tab(self):
        for index in range(self.tab_manager.count()):
            if self.tab_manager.tabText(index) == "All Products":
                self.tab_manager.removeTab(index)
                break

        # Create a table widget to display product data
        self.table_widget = QTableWidget()
        self.update_product_table(self.all_products)  # Initial load with all products

        # Add the QTableWidget directly to a new tab
        self.tab_manager.add_new_tab("All Products", self.table_widget)

    def update_product_table(self, products):
        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ['Name', 'Barcode', 'Purchase Price', 'Sell Price', 'Quantity', 'Update', 'Remove'])

        for row, product in enumerate(products):
            self.table_widget.setItem(row, 0, QTableWidgetItem(product.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(product.barcode))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(product.pur_price)))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(product.sel_price)))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(product.quantity)))

            # Create Edit button
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, b=product.barcode: self.show_update_tab(b))
            self.table_widget.setCellWidget(row, 5, edit_button)

            # Create Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, p_id=product.id: self.delete_product(p_id))
            self.table_widget.setCellWidget(row, 6, delete_button)

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def filter_products(self):
        search_text = self.search_bar.text().strip()
        filtered_products = []

        if search_text:
            filtered_products = [product for product in self.all_products if search_text in product.barcode]
        else:
            filtered_products = self.all_products  # Show all if search bar is empty

        self.update_product_table(filtered_products)

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
                self.load_all_products()  # Refresh the product list
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
                    self.load_all_products()  # Refresh the product list
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
            self.load_all_products()  # Refresh the product list after deletion
