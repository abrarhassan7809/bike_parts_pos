#main_window.py
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMainWindow, QToolBar, QComboBox, QInputDialog, QMessageBox
from tab_manager import TabManager
from db_operations import insert_product, update_product, delete_product, get_all_products


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

        # Add buttons to the toolbar
        new_tab_action = QAction("New Tab", self)
        new_tab_action.triggered.connect(lambda: self.tab_manager.add_new_tab("Empty Tab"))
        toolbar.addAction(new_tab_action)

        # Add dropdown menu
        dropdown = QComboBox(self)
        dropdown.addItems(["", "Insert", "Update", "Delete", "Fetch"])
        dropdown.currentIndexChanged.connect(self.on_dropdown_change)
        toolbar.addWidget(dropdown)

        return toolbar

    def on_dropdown_change(self, index):
        if index == 0:
            self.show_insert_tab()
        elif index == 1:
            self.show_update_tab()
        elif index == 2:
            self.show_delete_tab()
        elif index == 3:
            self.show_fetch_tab()

    def show_insert_tab(self):
        name = QInputDialog.getText(self, 'Insert Product', 'Enter product name:')
        price = QInputDialog.getDouble(self, 'Insert Product', 'Enter product price:')
        quantity = QInputDialog.getInt(self, 'Insert Product', 'Enter product quantity:')
        if name and price and quantity:
            insert_product(name, price, quantity)
            QMessageBox.information(self, "Success", "Product inserted successfully!")
            self.tab_manager.add_new_tab("Insert Tab", f"Inserted: {name}, Price: {price}, Quantity: {quantity}")

    def show_update_tab(self):
        product_id = QInputDialog.getInt(self, 'Update Product', 'Enter product ID to update:')
        if product_id:
            name, ok1 = QInputDialog.getText(self, 'Update Product', 'Enter new product name (leave blank to skip):')
            price, ok2 = QInputDialog.getDouble(self, 'Update Product', 'Enter new product price (leave blank to skip):', 0, -9999, 9999, 2)
            quantity, ok3 = QInputDialog.getInt(self, 'Update Product', 'Enter new quantity (leave blank to skip):', 0, 0, 9999)
            update_product(product_id, name=name, price=price if ok2 else None, quantity=quantity if ok3 else None)
            QMessageBox.information(self, "Success", "Product updated successfully!")
            self.tab_manager.add_new_tab("Update Tab", f"Updated Product ID: {product_id}")

    def show_delete_tab(self):
        product_id = QInputDialog.getInt(self, 'Delete Product', 'Enter product ID to delete:')
        if product_id:
            delete_product(product_id)
            QMessageBox.information(self, "Success", "Product deleted successfully!")
            self.tab_manager.add_new_tab("Delete Tab", f"Deleted Product ID: {product_id}")

    def show_fetch_tab(self):
        products = get_all_products()
        product_list = "\n".join([f"{p.id}: {p.name}, Price: {p.price}, Quantity: {p.quantity}" for p in products])
        self.tab_manager.add_new_tab("Fetch Tab", product_list if product_list else "No products found")
