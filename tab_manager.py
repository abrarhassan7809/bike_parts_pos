#tab_manager.py
from PySide6.QtWidgets import QTabWidget, QWidget, QVBoxLayout, QLabel

class TabManager(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

    def add_new_tab(self, title="New Tab", widget=None):
        if widget is None or isinstance(widget, str):
            widget_container = QWidget()
            layout = QVBoxLayout(widget_container)
            layout.addWidget(QLabel(str(widget)))
            self.addTab(widget_container, title)
        else:
            self.addTab(widget, title)

    def close_tab(self, index):
        self.removeTab(index)
