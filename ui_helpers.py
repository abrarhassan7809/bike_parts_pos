#ui_helpers.py
from PySide6.QtWidgets import QPushButton, QComboBox

def create_button(text, callback):
    button = QPushButton(text)
    button.clicked.connect(callback)
    return button

def create_dropdown(options, callback):
    dropdown = QComboBox()
    dropdown.addItems(options)
    dropdown.currentIndexChanged.connect(callback)
    return dropdown
