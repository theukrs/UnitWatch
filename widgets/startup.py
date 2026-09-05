from PyQt6.QtWidgets import QDialog, QFormLayout, QSpinBox, QPushButton, QHBoxLayout
import duckdb
green_btn_style = """
QPushButton {background-color: #27ae60;font-size: 15pt;border-radius: 2px;padding:5px;}
QPushButton:hover {background-color: #219150;}
"""
red_btn_style = """
QPushButton {background-color: #e74c3c; font-size: 15pt; border-radius: 2px; padding: 5px;} 
QPushButton:hover { background-color: #c0392b;}
"""


class Startup(QDialog):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()

    def create_widgets(self):
        self.units_limit = QSpinBox()
        self.units_limit.setRange(200,1000)

        self.reading_day = QSpinBox()
        self.reading_day.setRange(1,28)

        self.save_btn = QPushButton('Save')
        self.save_btn.setStyleSheet(green_btn_style)

        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(red_btn_style)

    def create_grid(self):
        layout = QFormLayout()
        layout.setVerticalSpacing(15)
        layout.setHorizontalSpacing(20)

        layout.addRow('Units:', self.units_limit)
        layout.addRow('Reading Date:',self.reading_day)

        buttons = QHBoxLayout()
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)

        layout.addRow('',buttons)

        self.setLayout(layout)

    def setup_window(self):
        self.setWindowTitle('Setup Window')
        self.setFixedSize(370,250)

    def create_link(self):
        self.save_btn.clicked.connect(self.submit_values)
        self.cancel_btn.clicked.connect(self.reject)

    def submit_values(self):
        with duckdb.connect('data.duckdb') as conn:
            reading_day = self.reading_day.value()
            units_limit = self.units_limit.value()
            conn.execute("UPDATE settings SET value = ? WHERE name = 'reading_day'",[reading_day])
            conn.execute("UPDATE settings SET value = ? WHERE name = 'units_limit'",[units_limit])
        self.accept()