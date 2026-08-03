import json
import os

class PlaylistManager:

    FILE_NAME = ".dse_playlist.json"

    def __init__(self):
        self.playlist_path = None

    def set_library(self, library_path):

        self.playlist_path = os.path.join(
            library_path,
            self.FILE_NAME
        )

    def load(self):

        if not os.path.exists(self.playlist_path):
            return []

        with open(self.playlist_path, "r") as file:
            return json.load(file)

    def save(self, filenames):

        with open(self.playlist_path, "w") as file:
            json.dump(
                filenames,
                file,
                indent=4
            )