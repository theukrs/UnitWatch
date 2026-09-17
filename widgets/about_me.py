from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QHBoxLayout


STYLE = """
    QDialog {background-color: #2c3e50;}
    QLabel {color: white;}
    #title {font-size: 25px;font-weight: bold;}
    #subtitle {font-size: 15px;color: #bdc3c7;}
    #section {font-size: 15px;font-weight: bold;}
    #name {font-size: 22px;font-weight: bold;}
    #role {font-size: 13px;color: #27ae60;}

    #description {
        font-size: 13px;
        color: #ecf0f1;
    }

    #tech {
        font-size: 13px;
        color: #bdc3c7;
    }

    #links {
        font-size: 13px;
        color: #27ae60;
    }

    #version {
        font-size: 11px;
        color: #7f8c8d;
    }
"""


class AboutMe(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.create_widgets()
        self.create_grid()
        self.setup_window()

    def create_widgets(self):

        self.title = QLabel('UnitWatch')
        self.title.setObjectName('title')
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.subtitle = QLabel('Electricity Tracker')
        self.subtitle.setObjectName('subtitle')
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.about_me = QLabel('About Me')
        self.about_me.setObjectName('section')
        self.about_me.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.name = QLabel('Usama Khan')
        self.name.setObjectName('name')
        self.name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.role = QLabel('Data Engineer')
        self.role.setObjectName('role')
        self.role.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.description = QLabel(
            'I built UnitWatch to make tracking electricity '
            'usage simple, clear, and useful.'
        )
        self.description.setObjectName('description')
        self.description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.description.setWordWrap(True)

        self.built_with = QLabel('Built With')
        self.built_with.setObjectName('section')
        self.built_with.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.tech = QLabel('Python  •  PyQt6  •  DuckDB  •  Pandas')
        self.tech.setObjectName('tech')
        self.tech.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.links = QLabel('GitHub  •  LinkedIn')
        self.links.setObjectName('links')
        self.links.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.version = QLabel('Version 1.0.0')
        self.version.setObjectName('version')
        self.version.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def create_grid(self):

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(35, 30, 35, 25)
        layout.setSpacing(8)

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

        layout.addSpacing(25)

        layout.addWidget(self.about_me)

        layout.addSpacing(5)

        layout.addWidget(self.name)
        layout.addWidget(self.role)

        layout.addSpacing(10)

        layout.addWidget(self.description)

        layout.addSpacing(25)

        layout.addWidget(self.built_with)

        layout.addSpacing(5)

        layout.addWidget(self.tech)

        layout.addSpacing(20)

        layout.addWidget(self.links)

        layout.addSpacing(25)

        layout.addWidget(self.version)

        self.setLayout(layout)

    def setup_window(self):

        self.setWindowTitle('About UnitWatch')
        self.setFixedSize(400, 500)
        self.setStyleSheet(STYLE)

