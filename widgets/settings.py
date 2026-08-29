from PyQt6.QtWidgets import QDialog, QFormLayout, QSpinBox, QPushButton
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
        self.units_limit = QSpinBox()
        self.units_limit.setRange(200,1000)

        self.reading_day = QSpinBox()
        self.reading_day.setRange(1,28)

        self.save_btn = QPushButton('Save')
        self.save_btn.setStyleSheet(green_btn_style)
        self.save_btn.setMinimumWidth(100)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(red_btn_style)
        self.cancel_btn.setMinimumWidth(100)

    def create_grid(self):
        layout = QFormLayout()
        layout.addRow('Units:',self.units_limit)
        layout.addRow('Reading Date:',self.reading_day)
        layout.addRow(self.save_btn,self.cancel_btn)
        self.setLayout(layout)

    def setup_window(self):
        self.setWindowTitle('Settings')
        self.setFixedSize(300,160)

    def create_link(self):
        self.save_btn.clicked.connect(self.submit_values)
        self.cancel_btn.clicked.connect(self.reject)

    def setup_values(self):
        with duckdb.connect('data.duckdb') as conn:
            reading_day = conn.execute("SELECT value FROM settings WHERE name = 'reading_day'").fetchone()[0]
            units_limit = conn.execute("SELECT value FROM settings WHERE name = 'units_limit'").fetchone()[0]
            self.reading_day.setValue(int(reading_day))
            self.units_limit.setValue(int(units_limit))

    def submit_values(self):
        with duckdb.connect('data.duckdb') as conn:
            reading_day = self.reading_day.value()
            units_limit = self.units_limit.value()
            conn.execute("UPDATE settings SET value = ? WHERE name = 'reading_day'",[reading_day])
            conn.execute("UPDATE settings SET value = ? WHERE name = 'units_limit'",[units_limit])
            self.accept()
