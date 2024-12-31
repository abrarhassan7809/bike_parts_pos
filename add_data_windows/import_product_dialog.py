# add_data_windows/import_product_dialog.py
import time
from datetime import datetime

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QFileDialog, \
    QMessageBox, QHBoxLayout, QProgressDialog
from db_config.db_operations import insert_product
import pandas as pd


class ImportProductDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import Products from CSV/Excel")
        self.setFixedSize(600, 400)

        # Main layout
        main_layout = QVBoxLayout(self)

        # Table for data preview
        self.table = QTableWidget()
        self.table.setStyleSheet("background-color: #9eb2c0")
        main_layout.addWidget(self.table)

        self.load_button = QPushButton("Load File")
        self.load_button.setFixedSize(150, 40)
        self.load_button.clicked.connect(self.load_file)

        self.add_button = QPushButton("Add Products")
        self.add_button.setFixedSize(150, 40)
        self.add_button.clicked.connect(self.add_to_database)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.add_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "CSV Files (*.csv);;Excel Files (*.xlsx)")
        if file_path:
            try:
                if file_path.endswith(".csv"):
                    data = pd.read_csv(file_path)
                else:
                    data = pd.read_excel(file_path)

                self.display_data(data)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load file: {str(e)}")

    def display_data(self, data):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))
        self.table.setHorizontalHeaderLabels(data.columns)

        for row in data.itertuples():
            for col_index, value in enumerate(row[1:], start=0):
                self.table.setItem(row.Index, col_index, QTableWidgetItem(str(value)))

    def add_to_database(self):
        products = []
        for row in range(self.table.rowCount()):
            try:
                quantity_text = self.table.item(row, 5).text()
                quantity = int(''.join(filter(str.isdigit, quantity_text)))

                product_data = {
                    'name': self.table.item(row, 0).text(),
                    'company': self.table.item(row, 1).text(),
                    'rank_number': self.table.item(row, 2).text(),
                    'pur_price': float(self.table.item(row, 3).text()),
                    'sel_price': float(self.table.item(row, 4).text()),
                    'quantity': quantity,
                    'current_date': datetime.today().strftime('%Y-%m-%d'),
                }
                products.append(product_data)
            except ValueError as e:
                QMessageBox.warning(self, "Data Error", f"Invalid data in row {row + 1}: {str(e)}")
                return

        # Create progress dialog
        progress_dialog = QProgressDialog("Adding products to the database...", "Cancel", 0, len(products), self)
        progress_dialog.setWindowTitle("Processing")
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)

        # Insert products into the database
        for i, product in enumerate(products):
            if progress_dialog.wasCanceled():
                break
            insert_product(**product)
            progress_dialog.setValue(i + 1)
            time.sleep(0.05)

        progress_dialog.close()
        self.accept()
