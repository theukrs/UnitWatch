from PyQt6.QtWidgets import QDialog, QLabel, QGridLayout, QSpinBox, QPushButton
import duckdb

green_btn_style = """
QPushButton {background-color: #27ae60;font-size: 15pt;border-radius: 8px;padding:5px;}
QPushButton:hover {background-color: #219150;}
"""
red_btn_style = """
QPushButton {background-color: #e74c3c; color: white;font-size: 15pt; border-radius: 8px; padding: 5px;} 
QPushButton:hover { background-color: #c0392b;}
"""
class Settings(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()
        self.setup_values()

    def create_widgets(self):
        self.units_limit_label = QLabel('Units:')
        self.units_limit = QSpinBox()
        self.units_limit.setRange(200,1000)

        self.reading_day_label = QLabel('Reading Date:')
        self.reading_day = QSpinBox()
        self.reading_day.setRange(1,28)

        self.save_btn = QPushButton('Save')
        self.save_btn.setStyleSheet(green_btn_style)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(red_btn_style)

    def create_grid(self):
        grid = QGridLayout()
        grid.addWidget(self.units_limit_label,0,0)
        grid.addWidget(self.units_limit,0,1)
        grid.addWidget(self.reading_day_label,1,0)
        grid.addWidget(self.reading_day,1,1)
        grid.addWidget(self.save_btn,2,0)
        grid.addWidget(self.cancel_btn,2,1)
        self.setLayout(grid)

    def setup_window(self):
        self.setWindowTitle('Settings')
        self.setFixedSize(300,200)

    def create_link(self):
        self.save_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

    def setup_values(self):
        with duckdb.connect('data.duckdb') as conn:
            reading_day = conn.execute("SELECT value FROM settings WHERE name = 'reading_day'").fetchone()[0]
            units_limit = conn.execute("SELECT value FROM settings WHERE name = 'reading_day'").fetchone()[0]
            self.reading_day.setValue(int(reading_day))
            self.units_limit.setValue(int(units_limit))
