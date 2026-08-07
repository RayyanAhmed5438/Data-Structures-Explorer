import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

from structures.linked_list.singly_linked_list import SinglyLinkedList

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    ll = SinglyLinkedList()

    # Only node
    ll.insert("A")
    print(ll.remove(0))
    print(ll.get_all())

    # Head
    ll.insert("A")
    ll.insert("B")
    ll.insert("C")
    print(ll.remove(0))
    print(ll.get_all())

    # Middle
    ll.clear()
    ll.insert("A")
    ll.insert("B")
    ll.insert("C")
    ll.insert("D")
    print(ll.remove(2))
    print(ll.get_all())

    # Tail
    ll.clear()
    ll.insert("A")
    ll.insert("B")
    ll.insert("C")
    print(ll.remove(2))
    print(ll.get_all())

    main()

