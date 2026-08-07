import os
import shutil

from core.enums.add_song_result import AddSongResult
from applications.music_player.playlist_manager import PlaylistManager
from applications.music_player.scanner import Scanner

class LibraryManager:

    def __init__(self):
        self.library_path = None
        self.songs = []
        self.scanner = Scanner()
        self.playlist_manager = PlaylistManager()

    def load_library(self, folder_path):
        self.library_path = folder_path
        self.playlist_manager.set_library(folder_path)
        self.songs = self.scanner.scan(folder_path)

        order = self.playlist_manager.load()

        if order == []:
            order = [
                {"file":os.path.basename(song.path)}
                for song in self.songs
            ]

            self.playlist_manager.save(order)

        song_map = {
            os.path.basename(song.path) : song for song in self.songs
        }

        ordered = []

        for item in order:
            filename = item["file"]

            if filename in song_map:
                ordered.append(song_map.pop(filename))

        ordered.extend(song_map.values())

        order = [
            {"file": os.path.basename(song.path)}
            for song in ordered
        ]

        self.playlist_manager.save(order)

        self.songs = ordered

    def save_playlist(self):

        order = [
            {"file": os.path.basename(song.path)}
            for song in self.songs
        ]

        self.playlist_manager.save(order)

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

        self.save_playlist()

    def add_song(self, source_path, index):

        result = self.validate_add_song(source_path)

        if result != AddSongResult.SUCCESS:
            return result

        destination = os.path.join(
            self.library_path,
            os.path.basename(source_path)
        )

        shutil.copy2(
            source_path, destination
        )

        song = self.scanner.create_song(destination)

        self.songs.insert(index,song)

        self.save_playlist()

        return AddSongResult.SUCCESS

    def validate_add_song(self, source_path):

        destination = os.path.join(
            self.library_path,
            os.path.basename(source_path)
        )

        if os.path.abspath(source_path) == os.path.abspath(destination):
            return AddSongResult.ALREADY_IN_LIBRARY

        if os.path.exists(destination):
            return AddSongResult.DUPLICATE_NAME

        return AddSongResult.SUCCESS

    def move_up(self, index):

        if index == 0:
            return

        self.songs[index], self.songs[index-1] = (
            self.songs[index-1], self.songs[index]
        )

        self.save_playlist()

    def move_down(self, index):

        if index >= len(self.songs) -1:
            return

        
        self.songs[index], self.songs[index+1] = (
            self.songs[index+1], self.songs[index]
        )

        self.save_playlist()

        