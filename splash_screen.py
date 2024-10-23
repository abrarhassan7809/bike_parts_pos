# splash_screen.py
from PySide6.QtWidgets import QSplashScreen
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap("assets/images/splash_img1.png")  # Path to your splash image
        self.setPixmap(pixmap)

    def show(self):
        super().show()

    def start_main_window(self, window):
        # Close splash screen and open main window after delay
        self.finish(window)
