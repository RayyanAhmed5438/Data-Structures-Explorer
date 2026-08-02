import os
import shutil

from applications.music_player.add_song_result import AddSongResult
from applications.music_player.scanner import Scanner

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

    def delete_song(self, song):

        os.remove(song.path)

        self.songs.remove(song)

    def add_song(self, source_path):

        destination = os.path.join(
            self.library_path,
            os.path.basename(source_path)
        )

        if os.path.samefile(source_path, destination):
            return AddSongResult.ALREADY_IN_LIBRARY

        if os.path.exists(destination):
            return AddSongResult.DUPLICATE_NAME

        shutil.copy2(
            source_path, destination
        )

        song = self.scanner.create_song(destination)

        self.songs.append(song)

        return AddSongResult.SUCCESS