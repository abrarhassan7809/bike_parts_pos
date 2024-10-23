#tab_manager.py
from PySide6.QtWidgets import QWidget, QTabWidget, QLabel, QVBoxLayout


class TabManager(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def add_new_tab(self, title="New Tab", content=""):
        widget = QWidget()
        layout = QVBoxLayout()

        # Create a label to display content
        content_label = QLabel(content)
        layout.addWidget(content_label)

        widget.setLayout(layout)
        self.addTab(widget, title)

    def close_tab(self, index):
        self.removeTab(index)
