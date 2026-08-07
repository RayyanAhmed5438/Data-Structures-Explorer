from core.data_structure import DataStructure

class LinkedList(DataStructure):

    def __init__(self):

        self.head = None
        self.tail = None
        self._size = 0

    def size(self):
        return self._size

    def clear(self):

        self.head = None
        self.tail = None
        self._size = 0