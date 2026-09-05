from PyQt6.QtWidgets import QDialog, QGridLayout, QLabel, QSpinBox, QPushButton
import duckdb
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
        self.units_limit_label = QLabel('Units:')

        self.units_limit = QSpinBox()
        self.units_limit.setRange(200,1000)

        self.reading_day_label = QLabel('Reading Date:')

        self.reading_day = QSpinBox()
        self.reading_day.setRange(1,28)


        self.submit_btn = QPushButton('Submit')
        self.submit_btn.setStyleSheet(green_btn_style)

    def create_grid(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(15)
        grid.setHorizontalSpacing(20)

        grid.addWidget(self.units_limit_label,0,0)
        grid.addWidget(self.units_limit,0,1)
        grid.addWidget(self.reading_day_label,1,0)
        grid.addWidget(self.reading_day,1,1)
        grid.addWidget(self.submit_btn,2,0,2,1)

        self.setLayout(grid)

    def setup_window(self):
        self.setWindowTitle('Setup Window')
        self.setFixedSize(370,250)

    def create_link(self):
        self.submit_btn.clicked.connect(self.submit_values)

    def submit_values(self):
        with duckdb.connect('data.duckdb') as conn:
            reading_day = self.reading_day.value()
            units_limit = self.units_limit.value()
            conn.execute("INSERT INTO settings (reading_day, units_limit) VALUES (?,?)",[reading_day,units_limit])
        self.accept()