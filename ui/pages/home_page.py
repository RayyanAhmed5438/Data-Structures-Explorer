from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame
)

from ui.widgets.application_card import ApplicationCard

class HomePage(QWidget):

    openRequested = pyqtSignal(object)

    def __init__(self, applications):
        super().__init__()

        self.applications = applications

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Data Structure Explorer")
        title.setStyleSheet("font-size:28px;font-weight:bold;")

        subtitle = QLabel("Choose an application")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        
        for application in self.applications:
            card = ApplicationCard(application)

            card.openRequested.connect(
                self.openRequested.emit
            )

            layout.addWidget(card)
        
           
        layout.addStretch()

        self.setLayout(layout)
