from applications.music_player.add_song_result import AddSongResult
from applications.music_player.library_manager import LibraryManager
from core.application import Application
from structures.array_ds import ArrayDS
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from core.visualization_state import VisualizationState

class MusicPlayerApplication(Application):


    def __init__(self):
        super().__init__(
            "music_player",
            "Music Player",
            "Demonstrate data structures using a music playlist"
        )
        self.library_manager = LibraryManager()
        self.current_structure = None

        self.player = QMediaPlayer()
        self.player.setVolume(100)

        self.current_index = -1
        self.current_song = None

        self.on_error = None

        self.player.error.connect(self.on_player_error)
        

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

    def play_song(self, index):

    
        if not(0 <= index < len(self.get_songs())):
            return None

            
        self.current_index = index
        previous = index > 0
        next = index < len(self.get_songs()) - 1
    
        song = self.get_songs()[index]

        if song == self.current_song:
            if not self.is_playing():
                self.player.play()
            return song, previous, next

            
        self.current_song = song

        url = QUrl.fromLocalFile(song.path)

        media = QMediaContent(url)


        self.player.setMedia(media)

        self.player.play()
    
        return song, previous, next

    def get_playback_state(self):

        if self.current_song is None:
            return None

        previous = self.current_index > 0
        next = self.current_index < len(self.get_songs()) - 1

        return (
            self.current_song,
            previous,
            next
        )

    def on_player_error(self):
        
        if self.on_error:
            self.on_error(
                "Unable to play this audio file.\n\n"
                "The file may use an unsupported codec or is corrupted."
            )
        
    def update_current_index(self):

        if self.current_song is None:
            return

        try:
            self.current_index = self.get_songs().index(
                self.current_song
            )
        except ValueError:

            self.player.stop()

            self.current_song = None
            self.current_index = -1
    
    def next(self):

        
        if self.current_index == -1:
            return None
    
        return self.play_song(self.current_index + 1)
    

    def previous(self):
        

        if self.current_index == -1:
            return None

        return self.play_song(self.current_index - 1)

    def toggle_playback(self):

        if self.is_playing():
            self.player.pause()

        elif self.current_index != -1:
            self.player.play()

    def is_playing(self):
        return self.player.state() == QMediaPlayer.PlayingState

    def get_visualization_state(self):

        if self.current_index == -1:
            return VisualizationState()

        return VisualizationState(
            selected_index=self.current_index,
        )

    def delete_song(self, index):

        song = self.get_songs()[index]

        self.library_manager.delete_song(song)

        self.update_current_index()

        

    def add_song(self, file_path, index):

        result = self.library_manager.add_song(file_path, index)

        if result == AddSongResult.SUCCESS:
            
            self.update_current_index()

        return result

    def validate_add_song(self, file):

        return self.library_manager.validate_add_song(file)

    def move_up(self, index):


        self.library_manager.move_up(index)
        self.update_current_index()

        

    def move_down(self, index):

        self.library_manager.move_down(index)
        self.update_current_index()

    def get_current_song_title(self):
    
        if self.current_song is None:
            return "No song playing"

        return self.current_song.title    