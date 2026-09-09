from PyQt6.QtWidgets import QDialog, QLabel

class AboutMe(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.create_widgets()
        self.create_grid()
        self.setup_window()

    def create_widgets(self):
        self.program_name = QLabel('UnitWatch\nElectricity Tracker')
        self.about_me = QLabel('About Me')
        self.name = QLabel('Usama Khan')

    def create_grid(self):
        pass

    def setup_window(self):
        self.setWindowTitle('About me!')



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