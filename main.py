from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QPushButton
from widgets.add_readings import AddReadings
from widgets.show_readings import ShowReadings
from widgets.readings_stats import ReadingStats
from widgets.settings import Settings
import duckdb
STYLE = """
    QWidget {color: white;}
    QLineEdit {background-color:#222; border: 1px solid #555; padding: 10px; font-size: 11pt;qproperty-alignment: AlignCenter;}
    QLineEdit:focus { border: 1px solid #27ae60; }
    QSpinBox {background-color:#222; border: 1px solid #555; padding: 10px; font-size: 11pt;qproperty-alignment: AlignCenter;}
    QSpinBox:focus { border: 1px solid #27ae60; }
    QLabel { font-size:15px; font-weight: bold;}
"""
DATE_STYLE = """
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
blue_btn_style = """
QPushButton {background-color: #2980b9;font-size: 20pt;border-radius: 8px;padding: 5px; font-weight: bold;}
QPushButton:hover {background-color: #3498db;}"""
red_btn_style = """
QPushButton {background-color: #e74c3c;font-size: 20pt;border-radius: 8px;padding: 5px; font-weight: bold;} 
QPushButton:hover { background-color: #c0392b;}
"""

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.add_mode = False
        self.create_sql()
        self.create_widgets()
        self.create_grid()
        self.setup_window()
        self.create_link()

    def create_sql(self):
        with duckdb.connect('data.duckdb') as conn:
            conn.execute('CREATE TABLE IF NOT EXISTS readings (reading_date DATE, units INTEGER)')
            conn.execute('CREATE TABLE IF NOT EXISTS settings (name VARCHAR PRIMARY KEY, value VARCHAR)')
            lists = conn.execute('SELECT * FROM settings').fetchall()
            print(lists)

    def create_widgets(self):
        self.add_readings = AddReadings()
        self.add_readings.hide()

        self.add_btn = QPushButton("Add reading")
        self.add_btn.setStyleSheet(blue_btn_style)
        self.add_btn.setMinimumWidth(200)

        self.settings_btn = QPushButton('Settings')
        self.settings_btn.setStyleSheet(red_btn_style)
        self.settings_btn.setMinimumWidth(200)

        self.show_readings = ShowReadings()

        self.reading_stats = ReadingStats()


    def create_grid(self):
        widget = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.add_readings,0,0)
        grid.addWidget(self.add_btn,0,0)
        grid.addWidget(self.settings_btn,0,1)
        grid.addWidget(self.reading_stats,0,2,2,1)
        grid.addWidget(self.show_readings,1,0,1,2)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 0)
        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def setup_window(self):
        self.setWindowTitle('UnitWatch')
        self.setStyleSheet(STYLE)
        self.setFixedSize(560,426)

    def create_link(self):
        self.add_btn.clicked.connect(self.toggle_add_mode)
        self.add_readings.submitted.connect(self.reading_submitted)
        self.settings_btn.clicked.connect(self.open_settings)

    def toggle_add_mode(self):
        visible = self.add_readings.isVisible()
        self.add_readings.setVisible(not visible)
        self.add_btn.setVisible(visible)
        self.settings_btn.setVisible(visible)

    def reading_submitted(self):
        self.toggle_add_mode()
        self.show_readings.load_tables()
        self.reading_stats.link_widgets()
        self.add_readings.confirm_submission()

    def open_settings(self):
        dialog = Settings(self)
        dialog.exec()

app = QApplication([])
app.setWindowIcon(QIcon('assets/icon.png'))
window = MainWindow()
window.show()
app.exec()
