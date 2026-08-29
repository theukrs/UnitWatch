from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget,QFormLayout,QLineEdit, QPushButton, QMessageBox
from datetime import date
import duckdb
green_btn_style = """
QPushButton { background-color: #27ae60;font-size: 15pt;border-radius: 8px;padding:5px; }
QPushButton:hover { background-color: #219150; }
QPushButton:pressed { background-color: #1e8449; }
"""
red_btn_style = """
QPushButton {background-color: #e74c3c; color: white;font-size: 15pt; border-radius: 8px; padding: 5px;} 
QPushButton:hover { background-color: #c0392b;}
QPushButton:pressed { background-color: #a93226; }
"""
QUERY = """
SELECT reading_date, units FROM readings WHERE reading_date = ?
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
        except ValueError:
            self.throw_error('Kindly enter a valid integer.')
            return
        with duckdb.connect('data.duckdb') as conn:
            latest_units = int(conn.execute('SELECT units FROM readings ORDER BY reading_date DESC LIMIT 1').fetchone()[0])
        if readings <= latest_units:
            self.throw_error(f"The number must be greater than {latest_units}")
            return
        r_date = date.today()
        with duckdb.connect('data.duckdb') as conn:
            conn.execute("INSERT INTO readings (reading_date, units) VALUES (?,?)",(r_date,readings))
            self.input_box.clear()
            self.submitted.emit()

    def disable_options(self,units):
        self.input_box.setText(f'{str(units)} [ALREADY SUBMITTED]')
        self.input_box.setReadOnly(True)
        self.submit_btn.setDisabled(True)

    def confirm_submission(self):
        with duckdb.connect('data.duckdb') as conn:
            results = conn.execute(QUERY,[date.today()]).fetchone()
        if results:
            self.disable_options(results[1])

    def throw_error(self,msg):
        QMessageBox.warning(self,'Input Error', msg)