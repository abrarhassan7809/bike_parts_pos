from PySide2.QtWidgets import QToolBar, QAction, QMenu

class HeaderBar(QToolBar):
    def __init__(self, parent, tab_widget):
        super().__init__(parent)
        self.tab_widget = tab_widget

        self.add_tab_action = QAction("Add Tab", self)
        self.add_tab_action.triggered.connect(self.tab_widget.add_new_tab)
        self.addAction(self.add_tab_action)

        self.dropdown_menu = QMenu("Options", self)
        self.dropdown_action = self.dropdown_menu.addAction("Open New Tab")
        self.dropdown_action.triggered.connect(self.tab_widget.add_new_tab)
        self.addAction(self.dropdown_menu.menuAction())
