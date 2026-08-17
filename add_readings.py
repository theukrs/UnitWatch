from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget,QFormLayout, QLabel, QLineEdit, QPushButton, QDateEdit, QMessageBox
import duckdb
green_btn_style = """QPushButton {background-color: #27ae60;font-size: 20pt;border-radius: 8px;padding:5px;}QPushButton:hover {background-color: #219150;}"""
red_btn_style = """QPushButton {background-color: #e74c3c; color: white;font-size: 20pt; border-radius: 8px; padding: 5px;} 
QPushButton:hover { background-color: #c0392b;}"""
class AddReadings(QWidget):
    submitted = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.create_grid()
        self.create_link()

    def create_widgets(self):
        self.header_label = QLabel('Enter the reading!')
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_box = QLineEdit()
        self.input_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_box.setValidator(QIntValidator(1,9999))
        self.input_box.setPlaceholderText('Enter the numbers')

        self.r_date = QDateEdit()
        self.r_date.setDate(QDate.currentDate())
        self.r_date.setCalendarPopup(True)
        self.r_date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.submit_btn = QPushButton('Submit')
        self.submit_btn.setStyleSheet(green_btn_style)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(red_btn_style)

    def create_grid(self):
        # grid = QGridLayout()
        # grid.addWidget(self.header_label,0,0)
        # grid.addWidget(self.input_box,1,0)
        # grid.addWidget(self.reading_date,2,0)
        # grid.addWidget(self.submit_btn,3,0)
        # self.setLayout(grid)
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
            date = self.r_date.date().toString("yyyy-MM-dd")
            print(f"Readings for {date}: {readings}")
            self.submitted.emit()
            self.input_box.clear()
            self.r_date.setDate(QDate.currentDate())
            with duckdb.connect('data.duckdb') as con:
                con.execute("CREATE TABLE IF NOT EXISTS readings (reading_date DATE, units INTEGER)")
                con.execute("INSERT INTO readings (reading_date, units) VALUES (?,?)",(date,readings))
                print(con.execute('SELECT * FROM readings').fetchall())
        except ValueError:
            QMessageBox.warning(self,'Input Error','Kindly enter valid numbers only.\nNumber and Rows must be integers.\nThe number must be 1-9999')