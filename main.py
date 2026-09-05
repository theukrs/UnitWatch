from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QPushButton, QDialog, QVBoxLayout
from widgets.add_readings import AddReadings
from widgets.show_readings import ShowReadings
from widgets.readings_stats import ReadingStats
from widgets.settings import Settings
from widgets.startup import Startup
from widgets.edit_readings import EditReadings
import duckdb
STYLE = """
    QWidget {color: white;}
    QLineEdit {background-color:#222; border: 1px solid #555; padding: 10px; font-size: 11pt;qproperty-alignment: AlignCenter;}
    QLineEdit:focus { border: 1px solid #27ae60; }
    QSpinBox {background-color:#222; border: 1px solid #555; padding: 6px 35px; font-size: 11pt;qproperty-alignment: AlignCenter;}
    QSpinBox:focus { border: 1px solid #27ae60; }
    QSpinBox:up-button {width:20px; subcontrol-origin: padding; border; subcontrol-position: left;}
    QSpinBox:down-button {width:20px; subcontrol-origin: padding; subcontrol-position: right;}
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {background-color: #333;}
    QLabel { font-size:15px; font-weight: bold;}
"""
blue_btn_style = """
QPushButton {background-color: #3498db;font-size: 20pt;border-radius: 8px;padding: 5px; font-weight: bold;}
QPushButton:hover {background-color: #2980b9;}"""
green_btn_style = """
QPushButton {background-color: #27ae60;font-size: 20pt;border-radius: 8px;padding: 5px; font-weight: bold;} 
QPushButton:hover { background-color: #219150;}
"""
purple_btn_style = """
QPushButton {background-color: #8e44ad;font-size: 20pt;border-radius: 8px;padding: 5px; font-weight: bold;} 
QPushButton:hover { background-color: #9b59b6;}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.create_sql()
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()

    def create_sql(self):
        with duckdb.connect('data.duckdb') as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS readings (reading_date DATE, units INTEGER)')
            conn.execute('CREATE TABLE IF NOT EXISTS settings (name VARCHAR PRIMARY KEY, value VARCHAR)')
            settings = conn.execute("SELECT name FROM settings WHERE name IN ('reading_day', 'units_limit')").fetchall()
        if len(settings) < 2:
            dialog = Startup(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                pass


    def create_widgets(self):
        self.add_readings = AddReadings()
        self.add_readings.hide()
        self.add_readings.setMinimumWidth(400)

        self.add_btn = QPushButton("Add reading")
        self.add_btn.setStyleSheet(blue_btn_style)
        self.add_btn.setMinimumWidth(160)

        self.edit_btn = QPushButton("Edit reading")
        self.edit_btn.setStyleSheet(green_btn_style)
        self.edit_btn.setMinimumWidth(160)

        self.settings_btn = QPushButton('Settings')
        self.settings_btn.setStyleSheet(purple_btn_style)
        self.settings_btn.setFixedWidth(150)

        self.show_readings = ShowReadings()

        self.reading_stats = ReadingStats()
        self.reading_stats.setFixedWidth(150)


    def create_grid(self):
        widget = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.add_readings,0,0,1,2)
        grid.addWidget(self.add_btn,0,0)
        grid.addWidget(self.edit_btn,0,1)
        grid.addWidget(self.show_readings,1,0,1,2)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)

        right_layout.addWidget(self.settings_btn)
        right_layout.addWidget(self.reading_stats)
        right_layout.addStretch()
        
        grid.addWidget(right_widget,0,2,2,1)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def setup_window(self):
        self.setWindowTitle('UnitWatch')
        self.setStyleSheet(STYLE)
        self.setFixedSize(580,426)

    def create_link(self):
        self.add_btn.clicked.connect(self.toggle_add_mode)
        self.add_readings.submitted.connect(self.reading_submitted)
        self.settings_btn.clicked.connect(self.open_settings)
        self.edit_btn.clicked.connect(self.open_edit_readings)

    def toggle_add_mode(self):
        visible = self.add_readings.isVisible()
        self.add_readings.setVisible(not visible)
        self.add_btn.setVisible(visible)
        self.edit_btn.setVisible(visible)
        if visible:
            self.add_btn.setFocus()
        else:
            self.add_readings.setFocus()

    def refresh_data(self):
        self.show_readings.load_tables()
        self.reading_stats.link_widgets()

    def reading_submitted(self):
        self.add_readings.confirm_submission()
        self.toggle_add_mode()
        self.refresh_data()

    def open_settings(self):
        dialog = Settings(self)
        dialog.exec()
        self.refresh_data()

    def open_edit_readings(self):
        dialog = EditReadings(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_data()
            

app = QApplication([])
app.setWindowIcon(QIcon('assets/unitwatch.png'))
window = MainWindow()
window.show()
app.exec()
