#main_window.py
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QMainWindow, QToolBar, QComboBox, QMessageBox, QDialog, QTableWidget, QTableWidgetItem,
                               QHeaderView, QPushButton, QLineEdit, QWidget, QSizePolicy)
from insert_product_dialog import InsertProductDialog
from update_product_dialog import UpdateProductDialog
from tab_manager import TabManager
from db_operations import insert_product, update_product, delete_product, get_all_products, get_product_by_barcode


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS System")
        self.setGeometry(200, 200, 1024, 768)

        # Initialize tab manager first
        self.tab_manager = TabManager(self)

        # Initialize toolbar
        self.toolbar = self.create_toolbar()

        # Set central widget as the tab manager
        self.setCentralWidget(self.tab_manager)

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
        self.search_bar.returnPressed.connect(self.search_product)
        toolbar.addWidget(self.search_bar)

        return toolbar

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

        # Fetch the latest products from the database
        products = get_all_products()

        if not products:
            QMessageBox.warning(self, "No Products", "No products found in the database.")
            return

        # Create a table widget to display product data
        table_widget = QTableWidget()
        table_widget.setRowCount(len(products))
        table_widget.setColumnCount(7)
        table_widget.setHorizontalHeaderLabels(
            ['Name', 'Barcode', 'Purchase Price', 'Sell Price', 'Quantity', 'Update', 'Remove'])

        # Populate the table with product data
        for row, product in enumerate(products):
            table_widget.setItem(row, 0, QTableWidgetItem(product.name))
            table_widget.setItem(row, 1, QTableWidgetItem(product.barcode))
            table_widget.setItem(row, 2, QTableWidgetItem(str(product.pur_price)))
            table_widget.setItem(row, 3, QTableWidgetItem(str(product.sel_price)))
            table_widget.setItem(row, 4, QTableWidgetItem(str(product.quantity)))

            # Create Edit button
            def create_edit_button(barcode):
                edit_button = QPushButton("Edit")
                edit_button.clicked.connect(lambda: self.show_update_tab(barcode))
                return edit_button

            edit_button = create_edit_button(product.barcode)
            table_widget.setCellWidget(row, 5, edit_button)

            # Create Delete button
            def create_delete_button(product_id):
                delete_button = QPushButton("Delete")
                delete_button.clicked.connect(lambda: self.delete_product(product_id, table_widget))
                return delete_button

            delete_button = create_delete_button(product.id)
            table_widget.setCellWidget(row, 6, delete_button)

        # Set the table widget to stretch to fit the entire width
        table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        table_widget.horizontalHeader().setStretchLastSection(True)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add the QTableWidget directly to a new tab
        self.tab_manager.add_new_tab("All Products", table_widget)

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
                self.show_all_products_tab()
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
                # Update the product based on the barcode
                existing_product = get_product_by_barcode(barcode)
                if existing_product:
                    update_product(existing_product.id, name, barcode, pur_price, sel_price, quantity)
                    QMessageBox.information(self, "Success", "Product updated successfully!")
                    self.show_all_products_tab()
                else:
                    QMessageBox.warning(self, "Error", "No product found with the provided barcode.")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")

    def delete_product(self, product_id, table_widget):
        response = QMessageBox.question(self, "Confirm Delete",
                                        f"Are you sure you want to delete product ID {product_id}?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            delete_product(product_id)
            self.show_all_products_tab()

    def search_product(self):
        barcode = self.search_bar.text().strip()
        if barcode:
            product_data = get_product_by_barcode(barcode)
            if product_data:
                self.display_product_details(product_data)
            else:
                QMessageBox.warning(self, "Not Found", "No product found with the provided barcode.")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a valid barcode.")

    def display_product_details(self, product_data):
        table_widget = QTableWidget()
        table_widget.setRowCount(1)
        table_widget.setColumnCount(5)  # Only show relevant columns
        table_widget.setHorizontalHeaderLabels(['Name', 'Barcode', 'Purchase Price', 'Sell Price', 'Quantity'])

        # Populate the table with product data
        table_widget.setItem(0, 0, QTableWidgetItem(product_data.name))
        table_widget.setItem(0, 1, QTableWidgetItem(product_data.barcode))
        table_widget.setItem(0, 2, QTableWidgetItem(str(product_data.pur_price)))
        table_widget.setItem(0, 3, QTableWidgetItem(str(product_data.sel_price)))
        table_widget.setItem(0, 4, QTableWidgetItem(str(product_data.quantity)))

        table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        table_widget.horizontalHeader().setStretchLastSection(True)
        table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # Add the QTableWidget directly to a new tab
        self.tab_manager.add_new_tab(f"Search Result - {product_data.name}", table_widget)



