from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox, QPushButton, QFormLayout, QMessageBox
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
        self.input_box.setValidator(QIntValidator(1,9999))

        self.reading_days = QComboBox()
        self.load_reading_days()

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

    def load_reading_days(self):
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
        return date(year,month,day)

    def update_value(self):
        data = self.reading_days.currentData()
        if data:
            self.input_box.setText(str(data[1]))

    def submit_values(self):
        reading_date = self.reading_days.currentData()[0]
        new_units = int(self.input_box.text())
        with duckdb.connect('data.duckdb') as conn:
            previous_date_units = int(conn.execute('SELECT units FROM readings WHERE reading_date < ? ORDER BY reading_date DESC LIMIT 1',[reading_date]).fetchone()[0])
            next_date_units = conn.execute('SELECT units FROM readings WHERE reading_date > ? ORDER BY reading_date LIMIT 1',[reading_date]).fetchone()
            if new_units <= previous_date_units:
                QMessageBox.warning(self,'Input Error', f"The number must be greater than {previous_date_units}")
                return
            if next_date_units and next_date_units[0] >= new_units:
                QMessageBox.warning(self,'Input Error', f"The number must be lower than {next_date_units}")
                return
            conn.execute("UPDATE readings SET units = ? WHERE reading_date = ?",[new_units,reading_date])
        self.accept()