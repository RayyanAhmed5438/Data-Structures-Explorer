from PyQt5.QtCore import pyqtSignal, Qt

from PyQt5.QtGui import QFont

from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)


class ApplicationCard(QFrame):

    openRequested = pyqtSignal(object)

    def __init__(self, application):
        super().__init__()

        self.application = application

        self.setup_ui()

    def setup_ui(self):

        self.setCursor(Qt.PointingHandCursor)

        self.setStyleSheet("""
            ApplicationCard {
                border: 1px solid #3A3B42;
                border-radius: 14px;
                background-color: #25262B;
            }

            ApplicationCard:hover {
                background-color: #2D2F36;
                border: 1px solid #50525C;
            }
        """)

        layout = QHBoxLayout()

        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(8)

        title = QLabel(self.application.name)
        title.setFont(QFont("Segoe UI", 14, QFont.Bold))

        title.setStyleSheet("color: #FFFFFF; background-color: transparent; font-size: 28px")

        description = QLabel(self.application.description)

        description.setWordWrap(True)

        description.setStyleSheet("""
            color: #A7A9B1;
            font-size: 11pt;
            background-color: transparent;
        """)

        

        layout.addWidget(title)
        layout.addWidget(description)
        self.setLayout(layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.openRequested.emit(self.application)

        super().mousePressEvent(event)
