from PyQt5.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QFileDialog
)
from config.settings import SettingsManager
from ui.pages.home_page import HomePage
from ui.pages.workspace_page import WorkspacePage
from core.application_manager import ApplicationManager


#OOGA BOOGA CLASS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QMainWindow{
                background-color: #2B2D31;
            }

            QWidget{
                background-color: #2B2D31;
                color: #E8E8E8;
                font-family: "Segoe UI";
                font-size: 10pt;
            }

            QMenuBar {
                background-color: #232428;
                color: white;
                spacing: 8px;
                padding: 6px;
                border-bottom: 1px solid #3A3A3A;
            }

            QMenuBar::item {
                padding: 6px 12px;
                border-radius: 6px;
            }

            QMenuBar::item:selected {
                background: #3A3D42;
            }

            QMenu {
                background-color: #2D2F34;
                border: 1px solid #454545;
            }

            QMenu::item:selected {
                background: #404249;
            }
        """)

        self.settings = SettingsManager()
        

        self.setWindowTitle("Data Structure Explorer")
        self.resize(1200, 700)
        

        self.application_manager = ApplicationManager()
        self.current_application = None

        
        self.create_menu()
        self.create_pages()

        self.connect_signals()

        self.show_home()


    def connect_signals(self):
        self.home_page.openRequested.connect(self.open_application)
        self.workspace_page.backRequested.connect(self.show_home)

        self.workspace_page.chooseLibraryRequested.connect(
            self.choose_library
        )

        self.workspace_page.nextRequested.connect(self.next_song)
        self.workspace_page.previousRequested.connect(self.previous_song)
        self.workspace_page.stopRequested.connect(self.toggle_song_playback)
        self.workspace_page.songSelected.connect(self.play_song)

    def open_application(self, application):
        self.current_application = application

        self.workspace_page.set_application(application)

        library_path = self.settings.get("library_path")

        if library_path:
            application.load_library(library_path)

            self.refresh_workspace()

        self.show_workspace()

    def choose_library(self):


        folder = QFileDialog.getExistingDirectory(
            self, "Select your folder"
        )

        if folder and self.current_application:
            self.current_application.load_library(folder)

            self.settings.set("library_path", folder)

            self.refresh_workspace()

    def refresh_workspace(self):
        self.workspace_page.set_library(
            self.settings.get("library_path")
        )

        self.workspace_page.visualize_array(
            self.current_application.get_structure()
        )

        self.workspace_page.load_songs(
            self.current_application.get_songs()
        )
            
    def create_menu(self):
        menu = self.menuBar()

        menu.addMenu("File")
        menu.addMenu("Application")
        menu.addMenu("Data Structure")
        menu.addMenu("Help")

    
    def create_pages(self):
        self.stack = QStackedWidget()

        self.home_page = HomePage(
            self.application_manager.get_applications()
        )

        self.workspace_page = WorkspacePage()

        self.stack.addWidget(self.home_page)
        self.stack.addWidget(self.workspace_page)

        self.setCentralWidget(self.stack)


    def show_home(self):
        self.stack.setCurrentWidget(self.home_page)

    def show_workspace(self):
        self.stack.setCurrentWidget(self.workspace_page)

    def next_song(self):
        if self.current_application:

            self.update_playback_ui(
                self.current_application.next()
            )

    def previous_song(self):
        if self.current_application:


            self.update_playback_ui(
                self.current_application.previous()
            )

    def toggle_song_playback(self):
        if self.current_application:
            self.current_application.toggle_playback()
            self.workspace_page.set_playing(
                self.current_application.is_playing()
            )

    def play_song(self, index):
        if self.current_application:

            self.update_playback_ui(
                self.current_application.play_song(index)
            )


    def update_playback_ui(self, result):
        if not result:
            return

        song, previous_enabled, next_enabled = result

        self.workspace_page.set_song(song.title)
        self.workspace_page.set_navigation(previous_enabled, next_enabled)

        self.workspace_page.set_current_song(
            self.current_application.current_index  # for highlight (UI)
        )

        self.workspace_page.set_playing(
            self.current_application.is_playing()
        )