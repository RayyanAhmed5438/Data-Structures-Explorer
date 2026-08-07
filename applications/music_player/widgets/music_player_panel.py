from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMenu
)
from PyQt5.QtCore import Qt, pyqtSignal
from applications.music_player.widgets.song_list_widget import SongListWidget
from core.enums.visualization_mode import VisualizationMode

class MusicPlayerPanel(QWidget):

    previousRequested = pyqtSignal()
    nextRequested = pyqtSignal()
    stopRequested = pyqtSignal()
    songSelected = pyqtSignal(int)

    deleteRequested = pyqtSignal(int)

    moveUpRequested = pyqtSignal(int)
    moveDownRequested = pyqtSignal(int)

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

            font-size:17px;
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
        QPushButton#operations{

            min-width:150px;
            max-width:180px;

            min-height:40px;
            max-height:40px;

            border-radius:8px;
        }
    """)

        layout = QVBoxLayout(self)

        title = QLabel("🎵 Music Player")
        title.setObjectName("title")

        layout.addWidget(title)

        card = QFrame()

        card_layout = QVBoxLayout(card)

        now = QLabel("Now Playing:-")

        self.song_title = QLabel("No Song Playing")
        self.song_title.setObjectName("songTitle")
        self.song_title.setAlignment(Qt.AlignCenter)

        controls = QHBoxLayout()

        self.previous_button = QPushButton("⏮")
        self.toggle_button = QPushButton("⏹")
        self.next_button = QPushButton("⏭")
        
        self.set_navigation(False, False)
        self.next_button.setEnabled(False)

        controls.addStretch()
        controls.addWidget(self.previous_button)
        controls.addWidget(self.toggle_button)
        controls.addWidget(self.next_button)
        controls.addStretch()

        card_layout.addWidget(now)
        card_layout.addSpacing(6)
        card_layout.addWidget(self.song_title)
        card_layout.addSpacing(10)
        card_layout.addLayout(controls)

        layout.addWidget(card)

        self.section_title = QLabel("Library")
        self.section_title.setObjectName("title")

        layout.addWidget(self.section_title)

        self.song_list = SongListWidget()

        self.song_list.setContextMenuPolicy(Qt.CustomContextMenu)

        self.song_list.customContextMenuRequested.connect(
            self.show_context_menu
        )

        layout.addWidget(self.song_list, 1)

        #=============== LINKED LIST ===================

        self.operations_widget = QWidget()

        operations_layout = QVBoxLayout(self.operations_widget)

        self.swap_left_button = QPushButton("⬅ Swap Left")

        self.delete_current_button = QPushButton("🗑 Delete")

        self.swap_right_button = QPushButton("Swap Right ➡")

        for button in (
            self.swap_left_button,
            self.delete_current_button,
            self.swap_right_button,
        ):
            button.setObjectName("operations")

        operations_layout.addStretch()

        operations_layout.addWidget(self.swap_left_button, alignment=Qt.AlignCenter)
        operations_layout.addSpacing(10)

        operations_layout.addWidget(self.delete_current_button, alignment=Qt.AlignCenter)
        operations_layout.addSpacing(10)

        operations_layout.addWidget(self.swap_right_button, alignment=Qt.AlignCenter)

        operations_layout.addStretch()

        self.operations_widget.hide()

        layout.addWidget(self.operations_widget)

        #=================================================

        layout.addStretch()

        self.previous_button.clicked.connect(
            self.previousRequested.emit
        )

        self.toggle_button.clicked.connect(
            self.stopRequested.emit
        )

        self.next_button.clicked.connect(
            self.nextRequested.emit
        )

        self.song_list.itemClicked.connect(
            self.item_clicked
        )

    def item_clicked(self, item):
        index = self.song_list.row(item)
        self.songSelected.emit(index)

    def show_context_menu(self, pos):

        item = self.song_list.itemAt(pos)

        if item is None:
            return

        index = self.song_list.row(item)

        menu = QMenu(self)

        move_up = menu.addAction("Move Up")
        move_down = menu.addAction("Move Down")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")

        move_up.setEnabled(index > 0)

        move_down.setEnabled(index < self.song_list.count() - 1) 

        action = menu.exec_(
            self.song_list.mapToGlobal(pos)
        )

        if action == move_up:
            self.moveUpRequested.emit(index)

        elif action == move_down:
            self.moveDownRequested.emit(index)

        elif action == delete_action:
            self.deleteRequested.emit(index)

    def set_song(self, title):
        self.song_title.setText(title)

    def load_songs(self, songs):

        self.song_list.blockSignals(True)

        self.song_list.clear()

        

        for song in songs:
            
            QListWidgetItem(song.title, self.song_list)

        self.song_list.setCurrentRow(-1)

        self.song_list.blockSignals(False)

    def set_navigation(self, previous_enabled, next_enabled):
        self.previous_button.setEnabled(previous_enabled)
        self.next_button.setEnabled(next_enabled)

    def set_current_song(self, index):  # for highlight (UI)

        self.song_list.blockSignals(True)

        self.song_list.setCurrentRow(index)

        self.song_list.blockSignals(False)

    def set_playing(self, playing):  # for button (UI)

        if playing:
            self.toggle_button.setText("⏸")
        else:
            self.toggle_button.setText("▶")

    def set_visualization_mode(self, mode):

        if mode == VisualizationMode.ARRAY:

            self.section_title.setText("Library")

            self.song_list.show()

        elif mode == VisualizationMode.LINKED_LIST:

            self.section_title.setText("Linked List Operations")

            self.song_list.hide()
            self.operations_widget.show()