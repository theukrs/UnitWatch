from PyQt6.QtWidgets import QDialog

class AboutMe(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.create_widgets()
        self.create_grid()
        self.setup_window()

    def create_widgets(self):
        pass

    def create_grid(self):
        pass

    def setup_window(self):
        self.setWindowTitle('About me!')