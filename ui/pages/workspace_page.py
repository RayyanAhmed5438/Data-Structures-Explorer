from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton,
    QVBoxLayout,
    QSplitter,
    QLabel,
    QHBoxLayout
)
from applications.music_player.widgets.music_player_panel import MusicPlayerPanel
from ui.widgets.visualization_panel import VisualizationPanel
import os
from core.enums.visualization_mode import VisualizationMode

class WorkspacePage(QWidget):

    backRequested = pyqtSignal()
    chooseLibraryRequested = pyqtSignal()

    previousRequested = pyqtSignal()
    nextRequested = pyqtSignal()
    stopRequested = pyqtSignal()
    songSelected = pyqtSignal(int)

    deleteRequested = pyqtSignal(int)
    addSongRequested = pyqtSignal()

    moveUpRequested = pyqtSignal(int)
    moveDownRequested = pyqtSignal(int)

    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
        
                QPushButton {
        
                    background-color: #32353B;
                    border: 1px solid #4B4E55;
                    border-radius: 8px;
        
                    padding: 8px 16px;
        
                    color: white;
        
                }
        
                QPushButton:hover {
        
                    background-color: #3C4047;
        
                }
        
                QPushButton:pressed {
        
                    background-color: #2A2C31;
        
                }
                
                QLabel{
                    font-size: 15px;
                    font-weight: 600;
                    color: #C7C7C7;
                }
        
             """)

        self.application = None

        self.setup_ui()

    def set_application(self, application):

        self.application = application

    def setup_ui(self):

        self.visualization_panel = VisualizationPanel()

        main_layout = QVBoxLayout()

        self.back_button = QPushButton("←")

        library_title = QLabel("Library: ")
        self.library_label = QLabel("No Library selected")

        self.choose_button = QPushButton("Choose Library")

        self.add_song_button = QPushButton("Add a Song")

        self.array_button = QPushButton("Array")
        self.linked_list_button = QPushButton("Linked List")

        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(10, 10, 10, 10)
        toolbar.setSpacing(8)

        toolbar.addWidget(self.back_button)
        toolbar.addSpacing(12)

        toolbar.addWidget(library_title)
        toolbar.addWidget(self.library_label)

        toolbar.addSpacing(20)

        toolbar.addWidget(self.choose_button)
        toolbar.addSpacing(15)

        toolbar.addWidget(self.add_song_button)
        toolbar.addSpacing(20)

        toolbar.addWidget(self.array_button)
        toolbar.addWidget(self.linked_list_button)

        toolbar.addStretch()

        self.zoom_in_button = QPushButton("+")
        self.zoom_out_button = QPushButton("-")

        self.zoom_in_button.setFixedSize(55, 30)
        self.zoom_out_button.setFixedSize(55, 30)

        self.zoom_in_button.clicked.connect(
            self.visualization_panel.zoom_in
        )

        self.zoom_out_button.clicked.connect(
            self.visualization_panel.zoom_out
        )

        toolbar.addWidget(self.zoom_in_button)
        toolbar.addSpacing(10)
        toolbar.addWidget(self.zoom_out_button)

        self.back_button.clicked.connect(self.backRequested.emit)

        splitter = QSplitter()


        #=======================================

        self.sidebar = MusicPlayerPanel()

        self.sidebar.previousRequested.connect(
            self.previousRequested.emit
        )

        self.sidebar.nextRequested.connect(
            self.nextRequested.emit
        )

        self.sidebar.stopRequested.connect(
            self.stopRequested.emit
        )

        self.sidebar.songSelected.connect(
            self.songSelected.emit
        )

        self.sidebar.deleteRequested.connect(
            self.deleteRequested.emit
        )

        self.sidebar.moveUpRequested.connect(
            self.moveUpRequested.emit
        )

        self.sidebar.moveDownRequested.connect(
            self.moveDownRequested.emit
        )

        #=======================================
        
        

        self.choose_button.clicked.connect(
             self.chooseLibraryRequested.emit
        )

        self.add_song_button.clicked.connect(
            self.addSongRequested.emit
        )

        self.array_button.clicked.connect(
            lambda: self.set_visualization_mode(
                VisualizationMode.ARRAY
            )
        )

        self.linked_list_button.clicked.connect(
            lambda: self.set_visualization_mode(
                VisualizationMode.LINKED_LIST
            )
        )
        
        splitter.addWidget(self.sidebar)
        splitter.addWidget(self.visualization_panel)

        splitter.setSizes([500, 500])

        splitter.setChildrenCollapsible(False)

        main_layout.addLayout(toolbar)
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

    def visualize_array(self, array):
        self.visualization_panel.visualize_array(array)

    def set_library(self, path):
            self.library_label.setText(os.path.basename(path))
            self.library_label.setToolTip(path)

    def set_song(self, title):
        self.sidebar.set_song(title)

    def load_songs(self, songs):
        self.sidebar.load_songs(songs)

    def set_navigation(self, previous, next):
        self.sidebar.set_navigation(previous, next)

    def set_current_song(self, index):  # for highlight (UI)
        self.sidebar.set_current_song(index)

    def set_playing(self, playing):  # for button (UI)

        self.sidebar.set_playing(playing)


    def set_selected_index(self, index):  # for visualization
        self.visualization_panel.set_selected_index(index)

    def set_visualization_mode(self, mode):

        self.application.set_visualization_mode(mode)

        self.application.refresh_structure()

        self.sidebar.set_visualization_mode(mode)
        self.visualization_panel.set_visualization_mode(mode)

        self.visualization_panel.visualize(
            self.application.get_structure()
        )

        if mode == VisualizationMode.LINKED_LIST:

            self.sidebar.set_previous_enabled(False)

        elif mode == VisualizationMode.ARRAY:

            index = self.application.current_index

            self.sidebar.set_previous_enabled(index > 0)

    def visualize(self, structure):

        self.visualization_panel.visualize(structure)

    def set_visualization_ui_mode(self, mode):
    
            self.sidebar.set_visualization_mode(mode)
            self.visualization_panel.set_visualization_mode(mode)

            self.visualization_panel.visualize(
                self.application.get_structure()
            )

            self.visualization_panel.set_selected_index(
                self.application.current_index
            )

        