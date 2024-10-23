#main.py
from PySide6.QtWidgets import QApplication
from splash_screen import SplashScreen
from main_window import MainWindow
from db import engine, Base
import sys

def main():
    app = QApplication(sys.argv)

    # Show splash screen
    splash = SplashScreen()
    splash.show()

    # Initialize main window after splash screen
    window = MainWindow()
    window.show()

    # Close splash screen once main window is ready
    splash.finish(window)

    sys.exit(app.exec())

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    main()
