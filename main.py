from PyQt6.QtWidgets import QApplication, QMainWindow
# import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.width = 500
        self.height = 500
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
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

    def create_link(self):
        pass

app = QApplication([])
window = MainWindow()
window.show()
app.exec()