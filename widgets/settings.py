from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QFormLayout, QSpinBox, QPushButton, QHBoxLayout, QSizePolicy
import duckdb
green_btn_style = """
QPushButton {background-color: #27ae60;font-size: 15pt;border-radius: 2px;padding:5px;}
QPushButton:hover {background-color: #219150;}
"""
red_btn_style = """
QPushButton {background-color: #e74c3c; font-size: 15pt; border-radius: 2px; padding: 5px;} 
QPushButton:hover { background-color: #c0392b;}
"""
blue_btn_style = """
QPushButton {background-color: #1f4e6e;font-size: 11pt;border-radius: 12px;padding: 5px; }
QPushButton:hover {background-color: #286486;}"""
purple_btn_style = """
QPushButton {background-color: #176b5b;font-size: 11pt;border-radius: 12px;padding: 5px; } 
QPushButton:hover { background-color: #20816e;}
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

        self.import_btn = QPushButton('Import')
        self.import_btn.setStyleSheet(blue_btn_style)
        self.import_btn.se

        self.export_btn = QPushButton('Export')
        self.export_btn.setStyleSheet(purple_btn_style)

        self.save_btn = QPushButton('Save')
        self.save_btn.setStyleSheet(green_btn_style)

        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet(red_btn_style)

        for btn in (self.import_btn, self.export_btn):
            btn.setSizePolicy(QSizePolicy.Policy.Fixed,QSizePolicy.Policy.Fixed)

    def create_grid(self):
        layout = QFormLayout()

        layout.setVerticalSpacing(15)
        layout.setHorizontalSpacing(20)

        layout.addRow('Units:', self.units_limit)
        layout.addRow('Reading Date:',self.reading_day)
        layout.addRow('Import Readings:',self.import_btn)
        layout.addRow('Export Readings:',self.export_btn)

        buttons = QHBoxLayout()
        buttons.addWidget(self.save_btn)
        buttons.addWidget(self.cancel_btn)

        layout.addRow('',buttons)

        self.setLayout(layout)

    def setup_window(self):
        self.setWindowTitle('Settings')
        self.setFixedSize(370,250)

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
