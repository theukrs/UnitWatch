from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QListWidget, QPushButton, QFormLayout
import duckdb
from datetime import date
green_btn_style = """
QPushButton {background-color: #27ae60;font-size: 15pt;border-radius: 8px;padding:5px;}
QPushButton:hover {background-color: #219150;}
"""
red_btn_style = """
QPushButton {background-color: #e74c3c; color: white;font-size: 15pt; border-radius: 8px; padding: 5px;} 
QPushButton:hover { background-color: #c0392b;}
"""

class EditReadings(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.create_widgets()
        self.create_grid()
        self.create_link()
        self.setup_window()

    def create_widgets(self):
        self.input_box = QLineEdit()
        self.input_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.reading_days = QListWidget()
        self.add_dates_in_list_widget()

        self.save_btn = QPushButton('Save')
        self.save_btn.setStyleSheet(green_btn_style)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(red_btn_style)

    def create_grid(self):
        layout = QFormLayout()
        layout.addRow('Units: ', self.input_box)
        layout.addRow('Reading Day:', self.reading_days)
        layout.addRow(self.save_btn, self.cancel_btn)
        self.setLayout(layout)

    def create_link(self):
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def setup_window(self):
        self.setWindowTitle('Edit Settings')
        self.setFixedSize(300,200)

    def add_dates_in_list_widget(self):
        with duckdb.connect('data.duckdb') as conn:
            day = int(conn.execute("SELECT value FROM settings WHERE name = 'reading_day'").fetchone()[0])
        last_reading_date = self.get_last_reading_date(day)
        print(last_reading_date)
        
    def get_last_reading_date(self,day):
        cd = date.today()
        year,month = (cd.year - 1, 12) if cd.month == 1 else (cd.year, cd.month - 1)
        last_reading_date = date(year,month,day)
        return last_reading_date
