# show_data_windows/supplier_window.py
from PySide6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QHeaderView
from db_config.db_operations import get_all_suppliers


class SupplierWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QVBoxLayout())

        self.table_widget = QTableWidget()
        self.layout().addWidget(self.table_widget)

        self.load_suppliers()

    def load_suppliers(self):
        suppliers = get_all_suppliers()
        self.table_widget.setRowCount(len(suppliers))
        self.table_widget.setColumnCount(4)
        self.table_widget.setHorizontalHeaderLabels(['ID', 'Name', 'Contact', 'Email'])

        for row, supplier in enumerate(suppliers):
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(supplier.id)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(supplier.name))
            self.table_widget.setItem(row, 2, QTableWidgetItem(supplier.company))
            self.table_widget.setItem(row, 3, QTableWidgetItem(supplier.phon_num))
            self.table_widget.setItem(row, 3, QTableWidgetItem(supplier.email))
            self.table_widget.setItem(row, 3, QTableWidgetItem(supplier.address))

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
