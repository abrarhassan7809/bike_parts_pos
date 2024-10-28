#show_data_windows/all_product_window.py
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHeaderView,
                               QLineEdit, QHBoxLayout, QSpacerItem, QSizePolicy)
from db_config.db_operations import get_all_products, delete_product, update_product, get_product_by_id
from add_data_windows.update_product_window import UpdateProductDialog
from PySide6.QtWidgets import QMessageBox


class AllProductWindow(QWidget):
    signal_created = Signal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.all_products = []
        self.filtered_products = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        search_layout = QHBoxLayout()
        self.search_data = QLineEdit(self)
        self.search_data.setFixedWidth(300)
        self.search_data.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.search_data.setPlaceholderText("Search Product...")
        self.search_data.textChanged.connect(self.filter_products)

        search_layout.addWidget(self.search_data)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        search_layout.addItem(spacer)
        self.layout.addLayout(search_layout)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.load_all_products()

    def load_all_products(self):
        self.all_products = get_all_products()
        self.update_product_table(self.all_products)

    def filter_products(self):
        search_text = self.search_data.text().strip()

        if search_text:
            self.filtered_products = [
                product for product in self.all_products
                if search_text in product.barcode or search_text.lower() in product.name.lower()
            ]
        else:
            self.filtered_products = self.all_products

        self.update_product_table(self.filtered_products)

    def update_product_table(self, products):
        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(8)
        self.table_widget.setHorizontalHeaderLabels(
            ['Name', 'Company', 'Rack Number', 'Purchase Price', 'Sell Price', 'Quantity', 'Update', 'Remove'])

        for row, product in enumerate(products):
            self.table_widget.setItem(row, 0, QTableWidgetItem(product.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(product.company))
            self.table_widget.setItem(row, 2, QTableWidgetItem(product.rank_number))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(product.pur_price)))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(product.sel_price)))
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(product.quantity)))

            # Create Edit button
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, p_id=product.id: self.show_update_tab(p_id))
            self.table_widget.setCellWidget(row, 6, edit_button)

            # Create Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, p_id=product.id: self.delete_product(p_id))
            self.table_widget.setCellWidget(row, 7, delete_button)

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def delete_product(self, product_id):
        response = QMessageBox.question(self, "Confirm Delete", f"You want to delete product?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            delete_product(product_id)
            self.load_all_products()
            self.signal_created.emit()

    def show_update_tab(self, p_id=None):
        dialog = UpdateProductDialog(self, p_id)
        if dialog.exec() == QMessageBox.Accepted:
            product_data = dialog.get_product_data()
            p_id, name, company, rank_number, pur_price, sel_price, quantity = (
                product_data['p_id'],
                product_data['name'],
                product_data['company'],
                product_data['rank_number'],
                product_data['pur_price'],
                product_data['sel_price'],
                product_data['quantity']
            )
            if company and name and pur_price and sel_price and quantity:
                existing_product = get_product_by_id(p_id)
                if existing_product:
                    update_product(p_id, name, company, rank_number, pur_price, sel_price, quantity)
                    QMessageBox.information(self, "Success", "Product updated successfully!")
                    self.load_all_products()
                else:
                    QMessageBox.warning(self, "Error", "No product found with the provided barcode.")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")
