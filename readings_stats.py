from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QGridLayout, QPushButton
import duckdb
from datetime import date
import calendar
STYLE = """
    QLineEdit:focus { border: 1px solid #c0392b;}
    QLabel { font-size:15px; font-weight: bold; qproperty-alignment: AlignCenter;}
    QPushButton {background-color: #666666;font-size: 15pt;padding:5px;font-weight:bold;margin-bottom:10px;}
    QPushButton:hover {background-color: #3D3D3D;}
"""
QUERY = """
    WITH units_usage AS (
        SELECT units, units - LAG(units) OVER(ORDER BY reading_date) AS usage
        FROM readings WHERE reading_date > ?
    )
    SELECT AVG(usage) FROM units_usage
"""
class ReadingStats(QWidget):
    def __init__(self):
        super().__init__()
        self.remaining_days = None
        self.create_widgets()
        self.create_grid()
        self.link_widgets()
        self.setStyleSheet(STYLE)

    def create_widgets(self):
        self.settings_btn = QPushButton('Settings')

        self.days_left_label = QLabel('Days Left:')
        self.days_left = QLineEdit()
        self.days_left.setReadOnly(True)

        self.units_used_label = QLabel('Units Used:')
        self.units_used = QLineEdit()
        self.units_used.setReadOnly(True)

        self.units_left_label = QLabel('Units Left:')
        self.units_left = QLineEdit()
        self.units_left.setReadOnly(True)

        self.avg_units_label = QLabel('Average Daily:')
        self.avg_units = QLineEdit()
        self.avg_units.setReadOnly(True)

        self.projected_usage_label = QLabel('Projected Usage:')
        self.projected_usage = QLineEdit()
        self.projected_usage.setReadOnly(True)

    def create_grid(self):
        grid = QGridLayout()
        grid.setVerticalSpacing(0)
        grid.setHorizontalSpacing(0)
        grid.addWidget(self.settings_btn,0,0)
        grid.addWidget(self.days_left_label,1,0)
        grid.addWidget(self.days_left,2,0)
        grid.addWidget(self.units_used_label,3,0)
        grid.addWidget(self.units_used,4,0)
        grid.addWidget(self.units_left_label,5,0)
        grid.addWidget(self.units_left,6,0)
        grid.addWidget(self.avg_units_label,7,0)
        grid.addWidget(self.avg_units,8,0)
        grid.addWidget(self.projected_usage_label,9,0)
        grid.addWidget(self.projected_usage,10,0)

        self.setLayout(grid)

    def link_widgets(self):
        self.set_days_left()
        self.set_units_stats()

    def set_days_left(self):
        with duckdb.connect('data.duckdb') as conn:
            next_reading_date = int(conn.execute("SELECT value FROM settings WHERE name = 'reading_day'").fetchone()[0])
            cd = date.today()
            self.remaining_days = next_reading_date - cd.day
            if self.remaining_days < 0:
                year, month = (cd.year + 1, 1) if cd.month == 12 else (cd.year, cd.month + 1)
                day = min(next_reading_date,calendar.monthrange(year,month)[1]) 
                target = date(year, month, day)
                result = (target - cd).days
                self.days_left.setText(str(result))
            else:
                self.days_left.setText(str(self.remaining_days))

    def set_units_stats(self):
        with duckdb.connect('data.duckdb') as conn:
            reading_day = int(conn.execute("SELECT value FROM settings where name = 'reading_day'").fetchone()[0])
            units_limit = int(conn.execute("SELECT value FROM settings WHERE name = 'units_limit'").fetchone()[0])
            latest_reading_date = conn.execute("SELECT reading_date FROM readings ORDER BY reading_date DESC LIMIT 1").fetchone()[0]
            cd = date.today()
            year,month = (cd.year - 1, 12) if cd.month == 1 else (cd.year, cd.month - 1)
            self.last_reading_date = date(year,month,reading_day)
            last_read_units = int(conn.execute("SELECT units FROM readings WHERE reading_date = ?",[self.last_reading_date]).fetchone()[0])
            latest_units = int(conn.execute("SELECT units FROM readings ORDER BY reading_date DESC LIMIT 1").fetchone()[0])
            units_used = latest_units - last_read_units
            units_left = units_limit - units_used
            total_days = (latest_reading_date - self.last_reading_date).days
            avg_units_per_day = units_used / total_days
            projected_usage = float(avg_units_per_day) * self.remaining_days
            self.avg_units.setText(f"{avg_units_per_day:.2f}")
            self.projected_usage.setText(str(int(projected_usage + units_used)))
            self.units_used.setText(str(units_used))
            self.units_left.setText(str(units_left))
