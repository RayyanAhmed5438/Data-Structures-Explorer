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
from pathlib import Path

from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from applications.music_player.widgets.song_list_widget import SongListWidget
from applications.music_player.widgets.spinning_cd_widget import SpinningCDWidget
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

        self.selected_index = -1

        # Resolve assets relative to the project root rather than the
        # terminal's current working directory.
        project_root = Path(__file__).resolve().parents[3]
        self.button_assets_dir = (
            project_root / "assets" / "music_player_buttons"
        )
        self.button_icon_paths = {
            "play": self.button_assets_dir / "play_button.png",
            "stop": self.button_assets_dir / "stop_button.png",
            "previous": self.button_assets_dir / "previous_button.png",
            "next": self.button_assets_dir / "next_button.png",
        }

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
            border-radius: 30px;

            min-width:35px;
            max-width:35px;

            min-height:42px;
            max-height:42px;
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

        self.song_title = SpinningCDWidget(self.button_assets_dir)

        controls = QHBoxLayout()

        self.previous_button = QPushButton()
        self.toggle_button = QPushButton()
        self.next_button = QPushButton()

        for x in (self.previous_button, self.toggle_button, self.next_button):
            x.setObjectName("controls")
            x.setCursor(Qt.PointingHandCursor)

        self._set_button_icon(
            self.previous_button, "previous", "⏮", "Previous song"
        )
        self._set_button_icon(
            self.next_button, "next", "⏭", "Next song"
        )
        self.toggle_button.setIconSize(QSize(24, 24))
        self.toggle_button.setFixedSize(42, 42)
        self.toggle_button.setToolTip("Play or pause playback")
        self.toggle_button.setAccessibleName("Play or pause playback")
        self.set_playing(False)

        self.set_navigation(False, False)
        self.next_button.setEnabled(False)

        controls.addStretch()
        controls.setSpacing(20)
        controls.addWidget(self.previous_button)
        controls.addWidget(self.toggle_button)
        controls.addWidget(self.next_button)
        controls.addStretch()

        card_layout.addWidget(now)
        card_layout.addSpacing(4)

        # Do not pass AlignCenter here: an alignment flag prevents the
        # expanding CD widget from filling the card's available width.
        # The disc itself is centered inside the widget by its paintEvent,
        # while the title can use the full player-panel width.
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

        self.delete_current_button.clicked.connect(
            lambda: self._delete_current()
        )

        self.swap_left_button.clicked.connect(
            lambda: self._swap_left()
        )

        self.swap_right_button.clicked.connect(
            lambda: self._swap_right()
        )

        self.song_list.itemClicked.connect(
            self.item_clicked
        )

    def _delete_current(self):

        index = self.get_selected_index()

        if index is not None:
            self.deleteRequested.emit(index)


    def _swap_left(self):
        index = self.get_selected_index()

        if index is not None:
            self.moveUpRequested.emit(index)


    def _swap_right(self):
        index = self.get_selected_index()

        if index is not None:
            self.moveDownRequested.emit(index)

    def get_selected_index(self):

        if self.selected_index < 0:
            return None

        return self.selected_index

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

        self.selected_index = index

        self.song_list.blockSignals(True)

        self.song_list.setCurrentRow(index)

        self.song_list.blockSignals(False)

    def _set_button_icon(self, button, icon_name, fallback_text, tooltip):
        """Load a project-local PNG icon, falling back to a text symbol."""
        icon_path = self.button_icon_paths[icon_name]

        if icon_path.is_file():
            icon = QIcon(str(icon_path))
            if not icon.isNull():
                button.setIcon(icon)
                button.setIconSize(QSize(24, 24))
                button.setText("")
                button.setToolTip(tooltip)
                button.setAccessibleName(tooltip)
                return True

        # Keep the controls usable if assets have not been copied to this
        # checkout or the image cannot be loaded.
        button.setIcon(QIcon())
        button.setText(fallback_text)
        button.setToolTip(tooltip)
        button.setAccessibleName(tooltip)
        return False

    def set_playing(self, playing):  # for button (UI)

        icon_name = "stop" if playing else "play"
        fallback = "⏸" if playing else "▶"
        tooltip = "Pause playback" if playing else "Play or resume playback"

        self._set_button_icon(
            self.toggle_button,
            icon_name,
            fallback,
            tooltip
        )

        self.song_title.set_spinning(playing)

    def set_previous_enabled(self, enabled):
        self.previous_button.setEnabled(enabled)

    def set_visualization_mode(self, mode):

        if mode == VisualizationMode.ARRAY:

            self.section_title.setText("Library")

            self.song_list.show()
            self.operations_widget.hide()

        elif mode == VisualizationMode.LINKED_LIST:

            self.section_title.setText("Linked List Operations")

            self.song_list.hide()
            self.operations_widget.show()