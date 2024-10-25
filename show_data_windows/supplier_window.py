#show_data_windows/supplier_window.py
from PySide6.QtWidgets import (QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView, QHBoxLayout,
                               QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QMessageBox)
from db_config.db_operations import get_all_suppliers, delete_supplier


class SupplierWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.all_supplier = []
        self.filtered_supplier = []
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout(self)

        # Create a search layout
        search_layout = QHBoxLayout()
        self.search_data = QLineEdit(self)
        self.search_data.setFixedWidth(300)
        self.search_data.setStyleSheet("background-color: #f0f0f0; color: #333;")
        self.search_data.setPlaceholderText("Search supplier...")
        self.search_data.textChanged.connect(self.filter_supplier)

        search_layout.addWidget(self.search_data)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        search_layout.addItem(spacer)
        self.layout.addLayout(search_layout)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.load_all_supplier()

    def load_all_supplier(self):
        self.all_supplier = get_all_suppliers()
        self.filtered_supplier = self.all_supplier
        self.update_supplier_table(self.filtered_supplier)

    def filter_supplier(self):
        supplier_text = self.search_data.text().strip().lower()

        self.filtered_supplier = [
            customer for customer in self.all_supplier
            if (supplier_text in customer.name.lower() if customer.name else False) or
               (supplier_text in customer.company.lower() if customer.company else False) or
               (supplier_text in customer.phon_num.lower() if customer.phon_num else False) or
               (supplier_text in customer.address.lower() if customer.address else False)
        ]

        self.update_supplier_table(self.filtered_supplier)

    def update_supplier_table(self, suppliers):
        self.table_widget.setRowCount(len(suppliers))
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Company', 'Contact', 'Email', 'Address', 'Action'])

        for row, supplier in enumerate(suppliers):
            self.table_widget.setItem(row, 0, QTableWidgetItem(supplier.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(supplier.company))
            self.table_widget.setItem(row, 2, QTableWidgetItem(supplier.phon_num))
            self.table_widget.setItem(row, 3, QTableWidgetItem(supplier.email))
            self.table_widget.setItem(row, 4, QTableWidgetItem(supplier.address))

            # Create Delete button
            delete_button = QPushButton("Delete")
            delete_button.clicked.connect(lambda _, p_id=supplier.id: self.delete_supplier(p_id))
            self.table_widget.setCellWidget(row, 5, delete_button)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def delete_supplier(self, supplier_id):
        response = QMessageBox.question(self, "Confirm Delete", f"Are you sure you want to delete?",
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.Yes:
            delete_supplier(supplier_id)
            self.load_all_supplier()
