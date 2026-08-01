from library.scanner import Scanner

class LibraryManager:

    def __init__(self):
        self.library_path = None
        self.songs = []
        self.scanner = Scanner()

    def load_library(self, folder_path):
        self.library_path = folder_path
        self.songs = self.scanner.scan(folder_path)

    def get_songs(self):
        return self.songs

    def get_library_path(self):
        return self.library_path

    def clear(self):
        self.library_path = None
        self.songs = []