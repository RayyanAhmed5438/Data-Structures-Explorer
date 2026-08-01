class Song:
    def __init__(
        self,
        title,
        artist,
        album,
        duration,
        path
    ):
        self.title = title
        self.artist = artist
        self.album = album
        self.duration = duration
        self.path = path

    def __repr__(self):
        return f"Song({self.title}, {self.artist})"