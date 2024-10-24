# all_product_window.py
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QHeaderView
from db_operations import get_all_products, delete_product, update_product, get_product_by_barcode
from update_product_window import UpdateProductDialog
from PySide6.QtWidgets import QMessageBox


class AllProductWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.all_products = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)
        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.load_all_products()

    def load_all_products(self):
        self.all_products = get_all_products()
        self.update_product_table(self.all_products)

    def update_product_table(self, products):
        self.table_widget.setRowCount(len(products))
        self.table_widget.setColumnCount(7)
        self.table_widget.setHorizontalHeaderLabels(
            ['Name', 'Brand', 'Company', 'Rank Number', 'Barcode', 'Purchase Price', 'Sell Price', 'Quantity', 'Update', 'Remove'])

        for row, product in enumerate(products):
            self.table_widget.setItem(row, 0, QTableWidgetItem(product.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(product.brand))
            self.table_widget.setItem(row, 2, QTableWidgetItem(product.company))
            self.table_widget.setItem(row, 3, QTableWidgetItem(product.rank_number))
            self.table_widget.setItem(row, 4, QTableWidgetItem(product.barcode))
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(product.pur_price)))
            self.table_widget.setItem(row, 6, QTableWidgetItem(str(product.sel_price)))
            self.table_widget.setItem(row, 7, QTableWidgetItem(str(product.quantity)))

            # Create Edit button
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda _, b=product.barcode: self.show_update_tab(b))
            self.table_widget.setCellWidget(row, 8, edit_button)

            # Create Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, p_id=product.id: self.delete_product(p_id))
            self.table_widget.setCellWidget(row, 9, delete_button)

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def delete_product(self, product_id):
        response = QMessageBox.question(self, "Confirm Delete",
                                        f"Are you sure you want to delete product ID {product_id}?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            delete_product(product_id)
            self.load_all_products()

    def show_update_tab(self, barcode=None):
        dialog = UpdateProductDialog(self, barcode)
        if dialog.exec() == QMessageBox.Accepted:
            product_data = dialog.get_product_data()
            name, barcode, brand, company, rank_number, pur_price, sel_price, quantity = (
                product_data['name'],
                product_data['barcode'],
                product_data['brand'],
                product_data['company'],
                product_data['rank_number'],
                product_data['pur_price_input'],
                product_data['sel_price_input'],
                product_data['quantity']
            )
            if barcode and name and pur_price and sel_price and quantity:
                existing_product = get_product_by_barcode(barcode)
                if existing_product:
                    update_product(existing_product.id, name, barcode, pur_price, sel_price, quantity)
                    QMessageBox.information(self, "Success", "Product updated successfully!")
                    self.load_all_products()
                else:
                    QMessageBox.warning(self, "Error", "No product found with the provided barcode.")
            else:
                QMessageBox.warning(self, "Error", "Please fill in all fields.")
