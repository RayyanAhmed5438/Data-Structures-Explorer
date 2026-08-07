from structures.linked_list.linked_list_node import LinkedListNode

class DoublyLinkedListNode(LinkedListNode):

    def __init__(self, data):

        super().__init__(data)

        self.previous = None