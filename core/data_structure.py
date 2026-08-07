from abc import ABC, abstractmethod


class DataStructure(ABC):

    @abstractmethod
    def insert(self, item):
        pass

    @abstractmethod
    def remove(self, index):
        pass

    @abstractmethod
    def get(self, index):
        pass

    @abstractmethod
    def update(self, index, item):
        pass

    @abstractmethod
    def search(self, value):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def get_all(self):
        pass

    def __iter__(self):
        pass