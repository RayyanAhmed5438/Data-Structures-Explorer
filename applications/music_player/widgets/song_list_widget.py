from PyQt5.QtWidgets import QListWidget
from PyQt5.QtCore import Qt


class SongListWidget(QListWidget):

    def mousePressEvent(self, event):

        if event.button() == Qt.RightButton:
            event.accept()
            return

        super().mousePressEvent(event)