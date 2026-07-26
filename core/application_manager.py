from core.application import Application


class ApplicationManager:

    def __init__(self):

        self._applications = [

            Application(
                "music",
                "Music Playlist",
                "Learn data structures through a playlist."
            )

        ]

    def get_applications(self):
        return self._applications