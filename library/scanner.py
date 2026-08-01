import os

from applications.music_player.song import Song

class Scanner:

    SUPPORTED_EXTENSIONS = (
        ".mp3", ".wav", ".flac", ".ogg", ".m4a"
    )

    UNKNOWN_ARTIST = "Unknown"
    UNKNOWN_ALBUM = "Unknown"

    def scan(self, folder_path):

        songs = []

        for root, _, files in os.walk(folder_path):

            for file in files:

                if file.lower().endswith(self.SUPPORTED_EXTENSIONS):

                    file_path = os.path.join(root, file)

                    title = os.path.splitext(file)[0]

                    song = Song(
                        title = title,
                        artist=self.UNKNOWN_ARTIST,
                        album = self.UNKNOWN_ALBUM,
                        duration= None,
                        path = file_path
                    )

                    songs.append(song)

        return songs