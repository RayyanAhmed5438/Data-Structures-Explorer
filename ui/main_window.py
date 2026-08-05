import os

from PyQt5.QtWidgets import (
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QStackedWidget,
    QFileDialog
)
from applications.music_player.add_song_result import AddSongResult
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
        self.workspace_page.deleteRequested.connect(self.delete_song)
        self.workspace_page.addSongRequested.connect(self.add_song)
        self.workspace_page.moveDownRequested.connect(self.move_down)
        self.workspace_page.moveUpRequested.connect(self.move_up)


    def open_application(self, application):
        self.current_application = application

        self.workspace_page.set_application(application)

        self.current_application.on_error = self.show_playback_error

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

        print("Refreshing workspace")

        self.current_application.refresh_structure()

        self.workspace_page.set_library(
            self.settings.get("library_path")
        )


        self.workspace_page.visualize_array(
            self.current_application.get_structure()
        )


        self.workspace_page.load_songs(
            self.current_application.get_songs()
        )

        state = self.current_application.get_visualization_state()

        if state.selected_index is not None:
            self.workspace_page.set_current_song(state.selected_index)
            self.workspace_page.set_selected_index(state.selected_index)

        if state.marker is not None:
            index, text = state.marker
            self.workspace_page.set_marker(index, text)

        self.workspace_page.set_playing(
            self.current_application.is_playing()
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

        if self.workspace_page.visualization_panel.is_animating():
            return

        if self.current_application:

            self.update_playback_ui(
                self.current_application.next()
            )

    def previous_song(self):
        if self.workspace_page.visualization_panel.is_animating():
            return


        if self.current_application:


            self.update_playback_ui(
                self.current_application.previous()
            )

    def toggle_song_playback(self):
        if self.workspace_page.visualization_panel.is_animating():
            return

        if self.current_application:
            self.current_application.toggle_playback()
            self.workspace_page.set_playing(
                self.current_application.is_playing()
            )

    def show_playback_error(self, error):

            if not error:
                error = (
                    f"Unable to play this audio file.\n\n"
                    "The file may ise an unsupported codec or may be corrupted."
                )
        
            QMessageBox.warning(
                self, 
                "Playback Error",
                error
            )

            self.update_playback_ui(
                self.current_application.get_playback_state()
            )
            

    def play_song(self, index):

        if self.workspace_page.visualization_panel.is_animating():
            return

        if not self.current_application:
            return

        result = self.current_application.play_song(index)

        self.update_playback_ui(
            result
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

        state = self.current_application.get_visualization_state()

        if state.selected_index is not None:
            self.workspace_page.set_selected_index(
                state.selected_index
            )

        if state.marker is not None:
            index, text = state.marker

            self.workspace_page.set_marker(
                index,
                text
            )

    def delete_song(self, index):

        if self.workspace_page.visualization_panel.is_animating():
            return

        if not self.current_application:
            return

        song = self.current_application.get_songs()[index]

        reply = QMessageBox.question(
            self,
            "Delete Song",
            f"Delete '{song.title}' from the library?\n\nThis will permanently delete the file.",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            self.current_application.delete_song(index)

            self.refresh_workspace()

    def add_song(self):

        if self.workspace_page.visualization_panel.is_animating():
            return

        if not self.current_application:
            return

        file, _ = QFileDialog.getOpenFileName(
            self, "Select Song",
            "",
            "Audio Files (*.mp3 *.wav *.ogg *.flac *.m4a)"
        )
        if not file:
            return

        songs = self.current_application.get_songs()

        position, ok = QInputDialog.getInt(
            self,
            "Insert Song",
            f"Insert at position (1-{len(songs)+1}):",
            len(songs) + 1,
            1,
            len(songs) + 1
        )

        if not ok:
            return

        index = position - 1
        song_name = os.path.splitext(
            os.path.basename(file)
        )[0]

        self.workspace_page.visualization_panel.animate_insert(
            index,
            song_name,
            finished=lambda:
                self.finish_add_song(file, index)
            
        )
    def finish_add_song(self, file, index):

        result = self.current_application.add_song(file, index)

        if result == AddSongResult.SUCCESS:
            self.refresh_workspace()

        elif result == AddSongResult.ALREADY_IN_LIBRARY:

            QMessageBox.information(
                self,
                "Song Exists",
                "This song is already in the selected library."
            )

        elif result == AddSongResult.DUPLICATE_NAME:

            QMessageBox.warning(
                self,
                "Duplicate Song",
                "A file with this name already exists in the library."
            )

    def move_up(self, index):

        if self.workspace_page.visualization_panel.is_animating():
            return

        if index <= 0:
            return

        self.workspace_page.visualization_panel.center_on_swap(
            index, index-1
        )

        self.workspace_page.visualization_panel.animate_swap(
            index,
            index-1,
            finished=lambda:self.finish_move_up(index)
        )

    def finish_move_up(self, index):

        if self.current_application:

            self.current_application.move_up(index)

            self.refresh_workspace()

    def move_down(self, index):

        if self.workspace_page.visualization_panel.is_animating():
            return

        if index >= len(self.current_application.get_songs()) -1:
            return

        self.workspace_page.visualization_panel.center_on_swap(
            index,
            index + 1
        )

        self.workspace_page.visualization_panel.animate_swap(
            index,
            index+1,
            finished=lambda:self.finish_move_down(index)
        )

    def finish_move_down(self, index):

        if self.current_application:
            self.current_application.move_down(index)

            self.refresh_workspace()