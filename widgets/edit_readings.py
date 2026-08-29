from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox, QPushButton, QFormLayout
import duckdb
from datetime import date
COMBO_STYLE = """
QComboBox {
    background-color: #222;
    border: 1px solid #555;
    border-radius: 4px;
    padding: 8px 35px 8px 10px;
    font-size: 11pt;
    color: white;
}

QComboBox:focus {
    border: 1px solid #27ae60;
}

QComboBox:hover {
    border: 1px solid #777;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #555;
    background-color: #333;
}

QComboBox::drop-down:hover {
    background-color: #27ae60;
}

QComboBox QAbstractItemView {
    background-color: #222;
    color: white;
    border: 1px solid #555;
    selection-background-color: #27ae60;
    selection-color: white;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px;
    text-align: center;
}

QComboBox QAbstractItemView::item:hover {
    background-color: #333;
}
"""
green_btn_style = """
QPushButton {background-color: #27ae60;font-size: 15pt;border-radius: 8px;padding:8px;}
QPushButton:hover {background-color: #219150;}
"""
red_btn_style = """
QPushButton {background-color: #e74c3c; color: white;font-size: 15pt; border-radius: 8px; padding: 8px;} 
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

        self.reading_days = QComboBox()
        self.add_dates_in_list_widget()

        self.save_btn = QPushButton('Save')
        self.save_btn.setStyleSheet(green_btn_style)
        self.save_btn.setMinimumWidth(100)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(red_btn_style)
        self.cancel_btn.setMinimumWidth(100)

    def create_grid(self):
        layout = QFormLayout()
        layout.addRow('Units: ', self.input_box)
        layout.addRow('Reading Day:', self.reading_days)
        layout.addRow(self.save_btn, self.cancel_btn)
        self.setLayout(layout)

    def create_link(self):
        self.save_btn.clicked.connect(self.submit_values)
        self.cancel_btn.clicked.connect(self.reject)
        self.reading_days.currentIndexChanged.connect(self.update_value)

    def setup_window(self):
        self.setWindowTitle('Edit Settings')
        self.setFixedSize(300,160)
        self.setStyleSheet(COMBO_STYLE)

    def add_dates_in_list_widget(self):
        with duckdb.connect('data.duckdb') as conn:
            day = int(conn.execute("SELECT value FROM settings WHERE name = 'reading_day'").fetchone()[0])
            last_reading_date = self.get_last_reading_date(day)
            get_reading_days = conn.execute("SELECT reading_date, units FROM readings WHERE reading_date > ? ORDER BY reading_date DESC",[last_reading_date]).fetchall()
            for row in get_reading_days:
                self.reading_days.addItem(row[0].strftime("%d-%m-%Y"),row)
        self.update_value()
        
    def get_last_reading_date(self,day):
        cd = date.today()
        year,month = (cd.year - 1, 12) if cd.month == 1 else (cd.year, cd.month - 1)
        last_reading_date = date(year,month,day)
        return last_reading_date

    def update_value(self):
        self.input_box.setText(str(self.reading_days.currentData()[1]))

    def submit_values(self):
        with duckdb.connect('data.duckdb') as conn:
            day = self.reading_days.currentData()[0]
            new_units = int(self.input_box.text())
            conn.execute("UPDATE readings SET units = ? WHERE reading_date = ?",[new_units,day])
        self.accept()