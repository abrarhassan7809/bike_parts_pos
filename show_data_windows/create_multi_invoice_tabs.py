from PySide6.QtCore import Signal
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QPushButton, QMessageBox, QHBoxLayout)
from add_data_windows.add_invoice_window import CreateInvoiceWindow


class CreateMultiInvoiceTabs(QWidget):
    signal_created = Signal()

    def __init__(self, invoice=None, parent=None):
        super().__init__(parent)
        self.invoice = invoice
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        # Add a button to create new invoice tabs
        self.create_invoice_tab_btn = QPushButton("Create New Invoice", self)
        self.create_invoice_tab_btn.clicked.connect(self.add_new_tab)
        button_layout.addWidget(self.create_invoice_tab_btn)

        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)  # Make tabs closable
        self.tab_widget.tabCloseRequested.connect(self.close_tab)  # Connect to close event

        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.tab_widget)

        self.add_new_tab()

    def add_new_tab(self):
        new_invoice = CreateInvoiceWindow(self.invoice, self)
        tab_index = self.tab_widget.addTab(new_invoice, f"Invoice {self.tab_widget.count() + 1}")
        self.tab_widget.setCurrentIndex(tab_index)

        new_invoice.signal_created.connect(lambda: self.close_tab(tab_index))

    def close_tab(self, index):
        reply = QMessageBox.question(
            self, "Close Tab", "Do you want to close this tab?", QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.tab_widget.removeTab(index)
