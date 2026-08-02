from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QFrame
)
from PyQt5.QtCore import pyqtSignal

class MusicPlayerPanel(QWidget):

    previousRequested = pyqtSignal()
    nextRequested = pyqtSignal()
    stopRequested = pyqtSignal()
    songSelected = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setupUI()

    def setupUI(self):

        self.setStyleSheet("""
            QWidget{
            background:#2D2F34;
            color:white;
        }

        QLabel#title{
            font-size:15px;
            font-weight:600;
            color:white;
        }

        QFrame{
            background:#25272C;
            border:1px solid #404040;
            border-radius:10px;
        }

        QLabel#songTitle{
            font-size:16px;
            font-weight:600;
            color:#EAEAEA;
        }

        QPushButton{

            background:#3A3D42;
            border:1px solid #555;
            border-radius:18px;

            min-width:36px;
            max-width:36px;

            min-height:36px;
            max-height:36px;
        }

        QPushButton:hover{
            background:#4A4E56;
        }

        QPushButton:disabled{
            background:#2A2A2A;
            color:#777;
        }

        QListWidget{

            background:#25272C;
            border:none;
            outline:none;

            font-size:13px;
        }

        QListWidget::item{

            padding:10px 8px;
            border-radius:6px;
        }

        QListWidget::item:hover{

            background:#3C4047;
        }

        QListWidget::item:selected{

            background:#3E6AE1;
            color:white;
        }
    """)

        layout = QVBoxLayout(self)

        title = QLabel("🎵 Music Player")
        title.setObjectName("title")

        layout.addWidget(title)

        card = QFrame()

        card_layout = QVBoxLayout(card)

        now = QLabel("Now Playing")

        self.song_title = QLabel("No Song Playing")
        self.song_title.setObjectName("songTitle")

        controls = QHBoxLayout()

        self.previous_button = QPushButton("⏮")
        self.stop_button = QPushButton("⏹")
        self.next_button = QPushButton("⏭")

        controls.addStretch()
        controls.addWidget(self.previous_button)
        controls.addWidget(self.stop_button)
        controls.addWidget(self.next_button)
        controls.addStretch()

        card_layout.addWidget(now)
        card_layout.addSpacing(6)
        card_layout.addWidget(self.song_title)
        card_layout.addSpacing(10)
        card_layout.addLayout(controls)

        layout.addWidget(card)

        library = QLabel("Library")
        library.setObjectName("title")

        layout.addWidget(library)

        self.song_list = QListWidget()

        layout.addWidget(self.song_list)

        layout.addStretch()

        self.previous_button.clicked.connect(
            self.previousRequested.emit
        )

        self.stop_button.clicked.connect(
            self.stopRequested.emit
        )

        self.next_button.clicked.connect(
            self.nextRequested.emit
        )

        self.song_list.currentRowChanged.connect(
            lambda row: self.songSelected.emit(row)
        )

    def set_song(self, title):
        self.song_title.setText(title)

    def load_songs(self, songs):

        self.song_list.clear()

        for song in songs:
            QListWidgetItem(song.title, self.song_list)

    def set_navigation(self, previous_enabled, next_enabled):
        self.previous_button.setEnabled(previous_enabled)
        self.next_button.setEnabled(next_enabled)