from core.data_structure import DataStructure

class ArrayDS(DataStructure):

    def __init__(self):

        self.items = []

    def insert(self, item):
        self.items.append(item)

    def remove(self, index):

        if 0 <= index < len(self.items):
            return self.items.pop(index)

        return None

    def get(self, index):

        if 0 <= index < len(self.items):
            return self.items[index]

        return None

    def update(self, index, item):

        if 0<= index < len(self.items):
            self.items[index] = item

    def search(self, value):
        for item in self.items:
            if item ==value:
                return item

        return None

    def clear(self):
        self.items.clear()

    def size(self):
        return len(self.items)

    def get_all(self):
        return self.items