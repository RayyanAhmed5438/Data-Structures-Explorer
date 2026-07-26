from PyQt5.QtWidgets import (
    QMainWindow,
    QStackedWidget,
    QFileDialog
)
from config.settings import SettingsManager
from ui.pages.home_page import HomePage
from ui.pages.workspace_page import WorkspacePage
from core.application_manager import ApplicationManager
from library.library_manager import LibraryManager

from structures.array_ds import ArrayDS

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.settings = SettingsManager()
        

        self.setWindowTitle("Data Structure Explorer")
        self.resize(1200, 700)
        

        self.application_manager = ApplicationManager()
        self.current_application = None

        self.library_manager = LibraryManager()


        self.create_menu()
        self.create_statusbar()
        self.create_pages()

        library_path = self.settings.get("library_path")
        if library_path:
            self.library_manager.load_library(library_path)
            self.workspace_page.control_panel.set_library(library_path)

            array = ArrayDS()

            for song in self.library_manager.get_songs():
                array.insert(song)

            self.workspace_page.visualize_array(array)


        self.connect_signals()

        self.show_home()


    def connect_signals(self):
        self.home_page.openRequested.connect(self.open_application)
        self.workspace_page.backRequested.connect(self.show_home)

        self.workspace_page.chooseLibraryRequested.connect(
            self.choose_library
        )

    def open_application(self, application):
        self.current_application = application
        self.workspace_page.set_application(application)
        self.show_workspace()

    def choose_library(self):


        folder = QFileDialog.getExistingDirectory(
            self, "Select your music folder"
        )

        if folder:
            self.library_manager.load_library(folder)

            self.settings.set("library_path", folder)
            self.workspace_page.control_panel.set_library(folder)

            array = ArrayDS()

            for song in self.library_manager.get_songs():
                array.insert(song)

            self.workspace_page.visualize_array(array)
            


    def create_menu(self):
        menu = self.menuBar()

        menu.addMenu("File")
        menu.addMenu("Application")
        menu.addMenu("Data Structure")
        menu.addMenu("Help")

    def create_statusbar(self):
        self.statusBar().showMessage("Ready")

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

