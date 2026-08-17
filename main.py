from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout
from add_readings import AddReadings
STYLE = """
    QWidget {background-color: #2c3e50;color: white;}
    QPushButton {background-color: #27ae60;font-size: 20pt;border-radius: 8px;padding:5px;}
    QPushButton:hover {background-color: #219150;}
    QLineEdit {background-color:#222; border: 1px solid #555; padding: 10px; font-size: 11pt;}
    QLineEdit:focus { border: 1px solid #27ae60;}
    QLabel { font-size:20px; font-weight: bold;}
    QDateEdit {
        background-color: #222;
        border: 1px solid #555;
        border-radius: 4px;
        padding: 8px 10px;
        font-size: 11pt;
        color: white;
    }
    QDateEdit:focus {
        border: 1px solid #27ae60;
    }
    QDateEdit::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 25px;
        border-left-width: 1px;
        border-left-color: #555;
        border-left-style: solid;
        border-top-right-radius: 3px;
        border-bottom-right-radius: 3px;
        background-color: #333;
    }
    QDateEdit::drop-down:hover {
        background-color: #27ae60;
    }
"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()

    def create_widgets(self):
        self.add_readings = AddReadings()

    def create_grid(self):
        widget = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.add_readings,0,0)

        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def setup_window(self):
        self.setWindowTitle('UnitWatch')
        self.setStyleSheet(STYLE)
        self.setFixedWidth(300)

    def create_link(self):
        pass

app = QApplication([])
window = MainWindow()
window.show()
app.exec()
