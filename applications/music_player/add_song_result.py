from enum import Enum

class AddSongResult(Enum):
    SUCCESS = 1
    ALREADY_IN_LIBRARY = 2
    DUPLICATE_NAME = 3