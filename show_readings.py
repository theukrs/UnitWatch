from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QTableWidget,QTableWidgetItem, QAbstractItemView
import duckdb



class ShowReadings(QWidget):
    conn = duckdb.connect('data.duckdb')
    def __init__(self):
        super().__init__()
        self.create_widgets()
        self.create_grid()

    def create_widgets(self):
        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['Date','Reading','Usage'])
        self.load_tables()        

    def create_grid(self):
        grid = QGridLayout()
        grid.addWidget(self.table,0,0)
        self.setLayout(grid)

    def load_tables(self):
        QUERY = """
        SELECT reading_date, units, units - LAG(units) OVER(order by reading_date) AS usage
        FROM readings ORDER BY reading_date DESC LIMIT 15
        """
        table_rows = self.conn.execute(QUERY).fetchall()
        self.table.setRowCount(len(table_rows))
        for i,data in enumerate(table_rows):
            item1, item2 = QTableWidgetItem(data[0].strftime("%d-%m-%Y")),QTableWidgetItem(str(data[1]))
            item3 = QTableWidgetItem(str(data[2]))
            item1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item3.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.table.setItem(i,0,item1)
            self.table.setItem(i,1,item2)
            self.table.setItem(i,2,item3)
