from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame
)


class ApplicationCard(QFrame):

    openRequested = pyqtSignal(object)

    def __init__(self, application):
        super().__init__()

        self.application = application

        self.setup_ui()

    def setup_ui(self):

        layout = QVBoxLayout()

        title = QLabel(self.application.name)

        description = QLabel(self.application.description)

        open_button = QPushButton("Open")

        open_button.clicked.connect(self.open_application)

        layout.addWidget(title)
        layout.addWidget(description)
        layout.addWidget(open_button)

        self.setLayout(layout)

    def open_application(self):

        self.openRequested.emit(self.application)