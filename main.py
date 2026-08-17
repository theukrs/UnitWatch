from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QPushButton
from add_readings import AddReadings
STYLE = """
    QWidget {background-color: #2c3e50;color: white;}
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
blue_btn_style = """QPushButton {background-color: #2980b9;font-size: 20pt;border-radius: 8px;padding:5px;}
QPushButton:hover {background-color: #3498db;}"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_mode = False
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()

    def create_widgets(self):
        self.add_readings = AddReadings()
        self.add_readings.hide()

        self.add_btn = QPushButton("Add reading")
        self.add_btn.setStyleSheet(blue_btn_style)

    def create_grid(self):
        widget = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.add_readings,0,0)
        grid.addWidget(self.add_btn,0,0)

        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def setup_window(self):
        self.setWindowTitle('UnitWatch')
        self.setStyleSheet(STYLE)
        self.setFixedWidth(400)

    def create_link(self):
        self.add_btn.clicked.connect(self.toggle_add_mode)
        self.add_readings.submitted.connect(self.toggle_add_mode)

    def toggle_add_mode(self):
        visible = self.add_readings.isVisible()
        self.add_readings.setVisible(not visible)
        self.add_btn.setVisible(visible)


app = QApplication([])
window = MainWindow()
window.show()
app.exec()
