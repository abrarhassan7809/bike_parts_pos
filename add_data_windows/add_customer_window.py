#add_data_windows/insert_customer_window.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QHBoxLayout, QMessageBox


class InsertCustomerDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Customer")
        self.setFixedSize(350, 450)

        main_layout = QVBoxLayout(self)

        self.name_input = QLineEdit(self)
        self.name_input.setFixedHeight(30)
        self.company_input = QLineEdit(self)
        self.company_input.setFixedHeight(30)
        self.phone_input = QLineEdit(self)
        self.phone_input.setFixedHeight(30)
        self.email_input = QLineEdit(self)
        self.email_input.setFixedHeight(30)
        self.city_input = QLineEdit(self)
        self.city_input.setFixedHeight(30)
        self.address_input = QLineEdit(self)
        self.address_input.setFixedHeight(30)

        main_layout.addWidget(QLabel("Name:"))
        main_layout.addWidget(self.name_input)
        main_layout.addWidget(QLabel("Company:"))
        main_layout.addWidget(self.company_input)
        main_layout.addWidget(QLabel("Phone Number:"))
        main_layout.addWidget(self.phone_input)
        main_layout.addWidget(QLabel("Email:"))
        main_layout.addWidget(self.email_input)
        main_layout.addWidget(QLabel("City:"))
        main_layout.addWidget(self.city_input)
        main_layout.addWidget(QLabel("Address:"))
        main_layout.addWidget(self.address_input)

        submit_button = QPushButton("Add Customer")
        submit_button.setFixedSize(150, 40)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(submit_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)
        submit_button.clicked.connect(self.validate_fields)

    def get_customer_data(self):
        return {
            "name": self.name_input.text(),
            "company": self.company_input.text(),
            "phone_num": self.phone_input.text(),
            "email": self.email_input.text(),
            "city": self.city_input.text(),
            "address": self.address_input.text()
        }

    def validate_fields(self):
        if not self.name_input.text().strip() or not self.phone_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Customer name and Number fields required.")
        else:
            self.accept()
