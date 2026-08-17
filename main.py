from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QApplication, QWidget, QDateEdit, QMainWindow, QGridLayout, QLabel, QLineEdit, QPushButton,QMessageBox
import duckdb
# con = duckdb.connect('database.db')
# con.execute("""CREATE OR REPLACE TABLE readings (
#         id INTEGER DEFAULT,
#         reading_date DATE,
#         units INTEGER
#     )
# """)

STYLE = """
    QWidget {background-color: #2c3e50;color: white;}
    QPushButton {background-color: #27ae60;font-size: 20pt;border-radius: 8px;padding:5px;}
    QPushButton:hover {background-color: #219150;}
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

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fullscreen = False
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()

    def create_widgets(self):
        self.header_label = QLabel('Enter the reading!')
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_box = QLineEdit()
        self.input_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.input_box.setValidator(QIntValidator(1,9999))
        self.input_box.setPlaceholderText('Enter the numbers')

        self.reading_date = QDateEdit()
        self.reading_date.setDate(QDate.currentDate())
        self.reading_date.setCalendarPopup(True)
        self.reading_date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.submit_btn = QPushButton('Submit')

    def create_grid(self):
        widget = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.header_label,0,0)
        grid.addWidget(self.input_box,1,0)
        grid.addWidget(self.reading_date,2,0)
        grid.addWidget(self.submit_btn,3,0)

        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def setup_window(self):
        self.setWindowTitle('UnitWatch')
        self.setStyleSheet(STYLE)
        self.setFixedWidth(300)

    def create_link(self):
        self.submit_btn.clicked.connect(self.readings_submit)
    
    def readings_submit(self):
        try:
            readings = self.input_box.text()
            date = self.reading_date.date().toString("yyyy-MM-dd")
            print(f"Readings for {date}: {readings}")
        except ValueError:
            QMessageBox.warning(self,'Input Error','Kindly enter valid numbers only.\nNumber and Rows must be integers.\nThe number must be 1-9999')

app = QApplication([])
window = MainWindow()
window.show()
app.exec()