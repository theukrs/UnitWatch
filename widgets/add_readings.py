from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget,QFormLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QMessageBox
from datetime import date
import duckdb
green_btn_style = """
QPushButton {background-color: #27ae60;font-size: 15pt;border-radius: 8px;padding:5px;}
QPushButton:hover {background-color: #219150;}
"""
red_btn_style = """
QPushButton {background-color: #e74c3c; color: white;font-size: 15pt; border-radius: 8px; padding: 5px;} 
QPushButton:hover { background-color: #c0392b;}
"""
QUERY = f"""
SELECT reading_date, units FROM readings WHERE reading_date = '{date.today()}'
"""

class AddReadings(QWidget):
    submitted = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.create_grid()
        self.create_link()
        self.confirm_submission()

    def create_widgets(self):
        self.input_box = QLineEdit()
        self.input_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_box.setValidator(QIntValidator(1,9999))
        self.input_box.setPlaceholderText('Enter the numbers')

        self.r_date = QLineEdit()
        self.r_date.setReadOnly(True)
        self.r_date.setText(str(date.today().strftime("%d-%m-%Y")))

        # self.r_date = QDateEdit()
        # self.r_date.setDate(QDate.currentDate())
        # self.r_date.setCalendarPopup(True)
        # self.r_date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.submit_btn = QPushButton('Submit')
        self.submit_btn.setStyleSheet(green_btn_style)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(red_btn_style)

    def create_grid(self):
        layout = QFormLayout()
        layout.addRow("Units:", self.input_box)
        layout.addRow("Date:", self.r_date)
        layout.addRow(self.cancel_btn,self.submit_btn)
        self.setLayout(layout)

    def create_link(self):
        self.submit_btn.clicked.connect(self.readings_submit)
        self.cancel_btn.clicked.connect(self.submitted.emit)

    def readings_submit(self):
        try:
            readings = int(self.input_box.text())
            with duckdb.connect('data.duckdb') as conn:
                latest_units_readings = int(conn.execute('SELECT units FROM readings ORDER BY reading_date DESC LIMIT 1').fetchone()[0])
            if not latest_units_readings < readings <= 9999:
                raise ValueError
            r_date = date.today()
            self.input_box.clear()
            with duckdb.connect('data.duckdb') as conn:
                conn.execute("INSERT INTO readings (reading_date, units) VALUES (?,?)",(r_date,readings))
                self.submitted.emit()
        except ValueError:
            QMessageBox.warning(self,'Input Error',f'Kindly enter valid numbers only.\nNumber and Rows must be integers.\nThe number must be {latest_units_readings}-9999')

    def disable_options(self,units):
        self.input_box.setText(f'{str(units)} [ALREADY SUBMITTED]')
        self.input_box.setReadOnly(True)
        self.submit_btn.setDisabled(True)
        self.r_date.setReadOnly(True)

    def confirm_submission(self):
        with duckdb.connect('data.duckdb') as conn:
            results = conn.execute(QUERY).fetchall()
        if (len(results) > 0):
            self.disable_options(results[0][1])
