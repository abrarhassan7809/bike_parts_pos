#main.py
from PySide6.QtWidgets import QApplication
from show_data_windows.main_window import MainWindow
from db_config.db import engine, Base
import sys


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    main()
