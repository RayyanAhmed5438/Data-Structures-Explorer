from applications.music_player.library_manager import LibraryManager
from core.application import Application
from structures.array_ds import ArrayDS

class MusicPlayerApplication(Application):

    def __init__(self):
        super().__init__(
            "music_player",
            "Music Player",
            "Demonstrate data structures using a music playlist"
        )
        self.library_manager = LibraryManager()
        self.current_structure = None

    def load_library(self, folder):
        self.library_manager.load_library(folder)
        self.refresh_structure()

    def refresh_structure(self):
        self.current_structure = ArrayDS()

        for song in self.library_manager.get_songs():
            self.current_structure.insert(song)

    def get_structure(self):
        return self.current_structure

    def get_songs(self):
        return self.library_manager.get_songs()