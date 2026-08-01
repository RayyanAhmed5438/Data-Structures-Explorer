from applications.music_player.music_player_app import MusicPlayerApplication

class ApplicationManager:

    def __init__(self):

        self._applications = [

            MusicPlayerApplication()

        ]

    def get_applications(self):
        return self._applications