from structures.linked_list.linked_list import LinkedList
from structures.linked_list.linked_list_node import LinkedListNode


class SinglyLinkedList(LinkedList):

    def __init__(self):
        super().__init__()

    def insert(self, item):

        node = LinkedListNode(item)

        if self.head is None:

            self.head = node
            self.tail = node

        else:

            self.tail.next = node
            self.tail = node

        self._size += 1

    def get_all(self):

        items = []

        current = self.head

        while current is not None:

            items.append(current.data)

            current = current.next

        return items

    def get(self, index):

        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        current = self.head

        for _ in range(index):
            current = current.next

        return current.data

    def remove(self, index):

        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        if self.head == self.tail:
            value = self.head.data
            self.head = None
            self.tail = None

        elif index == 0:
            value = self.head.data
            self.head = self.head.next

        else:
            current = self.head

            for _ in range(index - 1):
                current = current.next

            value = current.next.data

            if current.next == self.tail:
                current.next = None
                self.tail = current
            else:
                current.next = current.next.next

        self._size -= 1
        return value
           

    def update(self, index, item):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")

        current = self.head

        for _ in range(index):
            current = current.next

        current.data = item

    def search(self, value):

        current = self.head
        index = 0

        while current is not None:

            if current.data == value:
                return index

            current = current.next
            index += 1

        return -1