from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget,QTableWidgetItem, QAbstractItemView
import duckdb
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
QUERY = """
    SELECT 
        reading_date, 
        units, units - 
        LAG(units) OVER(order by reading_date) AS usage
    FROM readings 
    ORDER BY reading_date DESC 
    LIMIT 30
"""

class ShowReadings(QWidget):
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.create_grid()
        self.setStyleSheet(TABLE_STYLE)

    def create_widgets(self):
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Date','Reading','Usage'])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.load_tables()        

    def create_grid(self):
        grid = QGridLayout()
        grid.addWidget(self.table,0,0)
        self.setLayout(grid)

    def load_tables(self):
        with duckdb.connect('data.duckdb') as conn:
            table_rows = conn.execute(QUERY).fetchall()
        self.table.setRowCount(len(table_rows))
        for i,data in enumerate(table_rows):
            item1, item2 = QTableWidgetItem(data[0].strftime("%d-%m-%Y")),QTableWidgetItem(str(data[1]))
            usage = '-' if data[2] is None else str(data[2])
            item3 = QTableWidgetItem(usage)
            item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i,0,item1)
            self.table.setItem(i,1,item2)
            self.table.setItem(i,2,item3)