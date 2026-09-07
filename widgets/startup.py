from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QFormLayout, QLabel, QSpinBox, QPushButton
import duckdb
from datetime import date
STYLE = """
    QSpinBox {background-color:#222; border: 1px solid #555; padding: 6px 35px; font-size: 11pt;qproperty-alignment: AlignCenter;}
    QSpinBox:focus { border: 1px solid #27ae60; }
    QSpinBox:up-button {width:18px; subcontrol-origin: padding; border; subcontrol-position: left;}
    QSpinBox:down-button {width:18px; subcontrol-origin: padding; subcontrol-position: right;}
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
        self.header_label = QLabel('Kindly enter the limits for Units,\nYour Meter Reading day and\nYour Last Meter Bill reading')
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet('font-size:18px;')

        self.units_limit = QSpinBox()
        self.units_limit.setRange(200,1000)

        self.reading_day = QSpinBox()
        self.reading_day.setRange(1,28)
        self.reading_day.setValue(28)

        self.last_read_units = QSpinBox()
        self.last_read_units.setRange(1,999999)
        self.last_read_units.setValue(2000)

        self.submit_btn = QPushButton('Submit')
        self.submit_btn.setStyleSheet(green_btn_style)

    def create_grid(self):
        layout = QFormLayout()
        layout.setVerticalSpacing(15)
        layout.setHorizontalSpacing(20)

        layout.addRow(self.header_label)
        layout.addRow('Units:',self.units_limit)
        layout.addRow('Reading day:',self.reading_day)
        layout.addRow('Last read units:',self.last_read_units)
        layout.addRow(self.submit_btn)

        self.setLayout(layout)

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
            last_read_units = self.last_read_units.value()
            r_date = self.get_reading_day()
            conn.execute("INSERT INTO settings (name, value) VALUES (?,?)",['reading_day',reading_day])
            conn.execute("INSERT INTO settings (name, value) VALUES (?,?)",['units_limit',units_limit])
            conn.execute("INSERT INTO readings (reading_date, units) VALUES (?,?)",[r_date,last_read_units])
        self.accept()

    def get_reading_day(self):
        cd = date.today()
        reading_day = self.reading_day.value()
        if  reading_day >= cd.day:
            year, month = (cd.year - 1, 12) if cd.month == 1 else (cd.year, cd.month - 1)
        else:
            year, month = cd.year, cd.month
        last_reading_date = date(year, month,reading_day)
        return last_reading_date