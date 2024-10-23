#splash_scree.py
from PySide6.QtWidgets import QSplashScreen
from PySide6.QtGui import QPixmap
import time

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap("assets/images/splash_image.png")  # Path to your splash image
        self.setPixmap(pixmap)

    def show(self):
        super().show()
        time.sleep(2)  # Simulate some loading time
