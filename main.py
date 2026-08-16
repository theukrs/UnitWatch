from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
# import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fullscreen = False
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()

    def create_widgets(self):
        pass

    def create_grid(self):
        pass

    def setup_window(self):
        self.setWindowTitle('UnitWatch')
        self.setFixedSize(500, 500)

    def create_link(self):
        pass

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            if not self.fullscreen:
                self.setFixedSize(750, 750)
            else:
                self.setFixedSize(500, 500)
            self.fullscreen = not self.fullscreen 

app = QApplication([])
window = MainWindow()
window.show()
app.exec()