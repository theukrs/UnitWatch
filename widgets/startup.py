from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox, QPushButton, QLineEdit
import duckdb
STYLE = """
    QLineEdit {background-color:#222; border: 1px solid #555; padding: 10px; font-size: 11pt;qproperty-alignment: AlignCenter;}
    QLineEdit:focus { border: 1px solid #27ae60; }
    QSpinBox {background-color:#222; border: 1px solid #555; padding: 6px 35px; font-size: 11pt;qproperty-alignment: AlignCenter;}
    QSpinBox:focus { border: 1px solid #27ae60; }
    QSpinBox:up-button {width:20px; subcontrol-origin: padding; border; subcontrol-position: left;}
    QSpinBox:down-button {width:20px; subcontrol-origin: padding; subcontrol-position: right;}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {background-color: #333;}
    QLabel { font-size:15px; font-weight: bold;}
    QPushButton { font-size:15px; font-weight: bold; }
"""
green_btn_style = """
QPushButton {background-color: #27ae60;font-size: 15pt;border-radius: 2px;padding:5px;}
QPushButton:hover {background-color: #219150;}
"""
class Startup(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()

    def create_widgets(self):
        self.header_label = QLabel('Kindly enter the limits for Units,\nYour Meter Reading day,\nYour Last Meter Bill readings')
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet('font-size:18px;')

        self.units_limit_label = QLabel('Units:')
        self.units_limit = QSpinBox()
        self.units_limit.setRange(200,1000)

        self.reading_day_label = QLabel('Reading Date:')
        self.reading_day = QSpinBox()
        self.reading_day.setRange(1,28)

        self.last_reading_label = QLabel('Last Reading:')
        self.last_reading = QLineEdit()
        self.last_reading.setPlaceholderText('Enter units')

        self.submit_btn = QPushButton('Submit')
        self.submit_btn.setStyleSheet(green_btn_style)

    def create_grid(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)

        grid.addWidget(self.header_label,0,0,1,2)
        grid.addWidget(self.units_limit_label,1,0)
        grid.addWidget(self.units_limit,1,1)
        grid.addWidget(self.reading_day_label,2,0)
        grid.addWidget(self.reading_day,2,1)
        grid.addWidget(self.last_reading_label,3,0)
        grid.addWidget(self.last_reading,3,1)
        grid.addWidget(self.submit_btn,4,0,1,2)

        self.setLayout(grid)

    def setup_window(self):
        self.setWindowTitle('Setup Window')
        # self.setFixedSize(350,350)
        self.setStyleSheet(STYLE)

    def create_link(self):
        self.submit_btn.clicked.connect(self.submit_values)

    def submit_values(self):
        with duckdb.connect('data.duckdb') as conn:
            reading_day = self.reading_day.value()
            units_limit = self.units_limit.value()
            conn.execute("INSERT INTO settings (name, value) VALUES (?,?)",['reading_day',reading_day])
            conn.execute("INSERT INTO settings (name, value) VALUES (?,?)",['units_limit',units_limit])
            conn.execute("INSERT INTO readings (reading_date, units) VALUES (?,?)",(r_date,readings))
        self.accept()