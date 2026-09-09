from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout
STYLE = "border: 2px dashed;"

class AboutMe(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.create_widgets()
        self.create_grid()
        self.setup_window()

    def create_widgets(self):
        self.title = QLabel('UnitWatch\nElectricity Tracker')
        self.title.setStyleSheet('font-size:25px; font-weight: bolder; qproperty-alignment: AlignCenter;')

        self.about_me = QLabel('About Me')
        self.about_me.setStyleSheet('font-size:15px; font-style: italic; qproperty-alignment: AlignCenter;')

        self.name = QLabel('Usama Khan')
        self.name.setStyleSheet('font-size:25px; font-weight: bold italic; qproperty-alignment: AlignCenter;')


    def create_grid(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(15)

        layout.addWidget(self.title)

        layout.addWidget(self.about_me)
        layout.addWidget(self.name)

        self.setLayout(layout)

    def setup_window(self):
        self.setWindowTitle('About me!')
        self.setFixedSize(400,500)
        self.setStyleSheet(STYLE)



# ┌─────────────────────────────────────────┐
# │                                         │
# │                 UnitWatch               │
# │           Electricity Tracker           │
# │                                         │
# │              About Me                   │
# │                                         │
# │          [ Your Name ]                  │
# │       Developer & Creator               │
# │                                         │
# │   I built UnitWatch to make tracking    │
# │   electricity usage simple and useful.  │
# │                                         │
# │              Built With                 │
# │                                         │
# │    Python   PyQt6   DuckDB   Pandas     │
# │                                         │
# │          [ GitHub ] [ LinkedIn ]        │
# │                                         │
# │             Version 1.0.0               │
# │                                         │
# └─────────────────────────────────────────┘