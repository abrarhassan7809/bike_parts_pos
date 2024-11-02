from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QHBoxLayout, QLineEdit,
                               QPushButton, QSpacerItem, QSizePolicy, QHeaderView)
from db_config.db_operations import get_all_products


class ShowInventoryWindow(QWidget):
    signal_created = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.main_layout = QVBoxLayout(self)

        btn_layout = QHBoxLayout()
        self.print_btn = QPushButton("Print", self)
        self.print_btn.clicked.connect(self.print_inventory)

        btn_layout.addWidget(self.print_btn)

        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        btn_layout.addItem(spacer)
        self.main_layout.addLayout(btn_layout)

        self.table_widget = QTableWidget(self)
        self.main_layout.addWidget(self.table_widget)

        self.load_all_inventory()

    def load_all_inventory(self):
        self.all_products = get_all_products()
        self.update_inventory_table(self.all_products)

    def update_inventory_table(self, all_products):
        self.table_widget.clearContents()
        self.table_widget.setRowCount(len(all_products))
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Company', 'Quantity'])

        for row, customer in enumerate(all_products):
            self.table_widget.setItem(row, 0, QTableWidgetItem(customer.name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(customer.company))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(customer.quantity)))

        self.table_widget.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def print_inventory(self):
        print("invoice printed!")
