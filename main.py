from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QGridLayout, QPushButton
from add_readings import AddReadings
from show_readings import ShowReadings
from readings_stats import ReadingStats
import duckdb
STYLE = """
    QWidget {color: white;}
    QLineEdit {background-color:#222; border: 1px solid #555; padding: 10px; font-size: 11pt;qproperty-alignment: AlignCenter;}
    QLineEdit:focus { border: 1px solid #27ae60; }
    QLabel { font-size:15px; font-weight: bold;}
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
TABLE_STYLE = """
QTableWidget {
    background-color: #222;
    color: white;
    border: 1px solid #555;
    gridline-color: #444;
    selection-background-color: #27ae60;
    selection-color: white;
    alternate-background-color: #2a2a2a;
}

QTableWidget::item {
    padding: 5px;
}

QTableWidget::item:selected {
    background-color: #27ae60;
    color: white;
}

QHeaderView::section {
    background-color: #222;
    color: white;
    padding: 5px;
    border: 1px solid #555;
    font-size: 9pt;
    font-weight: bold;
}

QTableWidget QScrollBar:vertical {
    background-color: #222;
    width: 12px;
    margin: 0px;
}

QTableWidget QScrollBar::handle:vertical {
    background-color: #555;
    min-height: 30px;
    border-radius: 5px;
}

QTableWidget QScrollBar::handle:vertical:hover {
    background-color: #27ae60;
}

QTableWidget QScrollBar::add-line:vertical,
QTableWidget QScrollBar::sub-line:vertical {
    height: 0px;
}

QTableWidget QScrollBar:horizontal {
    background-color: #222;
    height: 12px;
    margin: 0px;
}

QTableWidget QScrollBar::handle:horizontal {
    background-color: #555;
    min-width: 30px;
    border-radius: 5px;
}

QTableWidget QScrollBar::handle:horizontal:hover {
    background-color: #27ae60;
}

QTableWidget QScrollBar::add-line:horizontal,
QTableWidget QScrollBar::sub-line:horizontal {
    width: 0px;
}
"""
blue_btn_style = """
QPushButton {background-color: #2980b9;font-size: 20pt;border-radius: 8px;padding:5px;}
QPushButton:hover {background-color: #3498db;}"""

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

    def create_widgets(self):
        self.add_readings = AddReadings()
        self.add_readings.hide()

        self.add_btn = QPushButton("Add reading")
        self.add_btn.setStyleSheet(blue_btn_style)

        self.show_readings = ShowReadings()

        self.reading_stats = ReadingStats()


    def create_grid(self):
        widget = QWidget()
        grid = QGridLayout()
        grid.addWidget(self.add_readings,0,0)
        grid.addWidget(self.add_btn,0,0)
        grid.addWidget(self.reading_stats,0,2,2,1)
        grid.addWidget(self.show_readings,1,0)
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 0)
        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def setup_window(self):
        self.setWindowTitle('UnitWatch')
        self.setStyleSheet(STYLE + TABLE_STYLE)
        self.setFixedSize(536,426)

    def create_link(self):
        self.add_btn.clicked.connect(self.toggle_add_mode)
        self.add_readings.submitted.connect(self.reading_submitted)

    def toggle_add_mode(self):
        visible = self.add_readings.isVisible()
        self.add_readings.setVisible(not visible)
        self.add_btn.setVisible(visible)

    def reading_submitted(self):
        self.toggle_add_mode()
        self.show_readings.load_tables()
        self.reading_stats.link_widgets()
        self.add_readings.confirm_submission()


app = QApplication([])
app.setWindowIcon(QIcon('assets/icon.png'))
window = MainWindow()
window.show()
app.exec()
