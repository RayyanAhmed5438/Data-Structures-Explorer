import os

from applications.music_player.song import Song

class Scanner:

    SUPPORTED_EXTENSIONS = (
        ".mp3", ".wav", ".flac", ".ogg", ".m4a"
    )

    UNKNOWN_ARTIST = "Unknown"
    UNKNOWN_ALBUM = "Unknown"

    def create_song(self, file_path):

        title = os.path.splitext(
            os.path.basename(file_path)
        )[0]

        return Song(
            title=title,
            artist=self.UNKNOWN_ARTIST,
            album=self.UNKNOWN_ALBUM,
            duration=None,
            path=file_path
        )

    def scan(self, folder_path):

        songs = []

        for root, _, files in os.walk(folder_path):

            for file in files:

                if file.lower().endswith(self.SUPPORTED_EXTENSIONS):

                    file_path = os.path.join(root, file)

                    songs.append(self.create_song(file_path))

        return songs