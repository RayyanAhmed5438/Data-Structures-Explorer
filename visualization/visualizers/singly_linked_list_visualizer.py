from PyQt5.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsLineItem,
    QGraphicsPolygonItem
)
from PyQt5.QtGui import (
    QColor,
    QPen,
    QBrush,
    QFont,
    QFontMetrics,
    QPolygonF
)
from PyQt5.QtCore import (
    QTimer,
    Qt,
    QPointF,
    QParallelAnimationGroup,
    QPropertyAnimation,
    QVariantAnimation
)


class SinglyLinkedListNodeItem(QGraphicsRectItem):

    WIDTH = 280
    HEIGHT = 80

    DATA_WIDTH = 110
    NEXT_WIDTH = 170

    def __init__(self, song, address, next_address):

        super().__init__(
            0,
            0,
            self.WIDTH,
            self.HEIGHT
        )

        self.song = song
        self.next_address = next_address
        self.address = address

        self.setPen(
            QPen(Qt.white, 2)
        )

        self.setBrush(
            QBrush(QColor(55, 55, 55))
        )

        # -----------------------------------------
        # Vertical divider between DATA and NEXT
        # -----------------------------------------

        self.divider = QGraphicsLineItem(
            self.DATA_WIDTH ,
            0,
            self.DATA_WIDTH ,
            self.HEIGHT,
            self
        )

        self.divider.setPen(
            QPen(Qt.white, 2)
        )

        # -----------------------------------------
        # DATA label
        # -----------------------------------------

        self.data_label = QGraphicsTextItem(
            "DATA",
            self
        )

        self.data_label.setDefaultTextColor(
            Qt.white
        )

        self.data_label.setFont(
            QFont("Segoe UI", 9, QFont.Bold)
        )

        self.data_label.setPos(
            8,
            5
        )

        # -----------------------------------------
        # NEXT label
        # -----------------------------------------

        self.next_label = QGraphicsTextItem(
            "NEXT",
            self
        )

        self.next_label.setDefaultTextColor(
            Qt.white
        )

        self.next_label.setFont(
            QFont("Segoe UI", 9, QFont.Bold)
        )

        self.next_label.setPos(
            self.DATA_WIDTH  + 8,
            5
        )

        # -----------------------------------------
        # Song title
        # -----------------------------------------

        self.data_text = QGraphicsTextItem(
            self.elide_text(song.title, self.DATA_WIDTH - 16),
            self
        )

        self.data_text.setDefaultTextColor(
            Qt.white
        )

        self.data_text.setFont(
            QFont("Segoe UI", 9)
        )

        self.data_text.setPos(
            8,
            35
        )

        # -----------------------------------------
        # Next address
        # -----------------------------------------

        self.next_text = QGraphicsTextItem(
            next_address,
            self
        )

        self.next_text.setDefaultTextColor(
            Qt.white
        )

        self.next_text.setFont(
            QFont("Segoe UI", 9)
        )

        self.next_text.setPos(
            self.DATA_WIDTH  + 8,
            35
        )

    @staticmethod
    def elide_text(text, width):

        font = QFont("Segoe UI", 9)

        metrics = QFontMetrics(font)

        return metrics.elidedText(
            str(text),
            Qt.ElideRight,
            width
        )

    def set_next_address(self, address):

        self.next_address = address
        self.next_text.setPlainText(address)

    def set_selected(self, selected):

        if selected:
            self.setBrush(
                QBrush(QColor("#3E6AE1"))
            )
        else:
            self.setBrush(
                QBrush(QColor(55, 55, 55))
            )


class SinglyLinkedListVisualizer:

    START_X = 60
    START_Y = 100

    NODE_GAP_X = 80
    NODE_GAP_Y = 120

    def __init__(self, scene):

        self.scene = scene

        self.items = []
        self.arrows = []

        self.selected_index = -1

        self.animating = False

        

    def visualize(self, linked_list):

        self.scene.clear()

        self.items.clear()
        self.arrows.clear()

        if linked_list is None:
            return

        current = linked_list.head

        index = 0

        # -----------------------------------------
        # First create all nodes
        # -----------------------------------------

        while current is not None:

            next_node = current.next

            if next_node is None:
                next_address = "NULL"
            else:
                next_address = self.format_address(
                    id(next_node)
                )

            node = SinglyLinkedListNodeItem(
                current.data,
                self.format_address(id(current)),
                next_address
            )

            x = (
                self.START_X +
                index * (
                    SinglyLinkedListNodeItem.WIDTH +
                    self.NODE_GAP_X
                )
            )

            y = (
                self.START_Y +
                index * self.NODE_GAP_Y
            )

            node.setPos(x, y)

            self.scene.addItem(node)

            self.items.append(node)

            address_text = QGraphicsTextItem(
                self.format_address(id(current))
            )

            address_text.setDefaultTextColor(Qt.white)
            address_text.setFont(
                QFont("Segoe UI", 9)
            )

            address_width = address_text.boundingRect().width()

            address_text.setPos(
                x + (
                    SinglyLinkedListNodeItem.WIDTH - address_width
                ) / 2,
                y + SinglyLinkedListNodeItem.HEIGHT + 12
            )

            self.scene.addItem(address_text)

            current = current.next
            index += 1

        # -----------------------------------------
        # Then create the arrows
        # -----------------------------------------

        for index, node in enumerate(self.items):
            node.set_selected(
                index == self.selected_index
            )

        for index in range(len(self.items) - 1):

            self.add_arrow(
                self.items[index], self.items[index+1]
            )
        # -----------------------------------------
        # Final NULL arrow
        # -----------------------------------------

        if self.items:
            self.add_null_arrow(self.items[-1])

        # Update scene bounds    

        self.scene.fit_with_margin(400)

        

    def format_address(self, address):

        return hex(address)

    def create_arrow(self, current_node, next_node):

        # Start from the right-middle of the current node
        start_x = (
            current_node.x() +
            SinglyLinkedListNodeItem.WIDTH
        )

        start_y = (
            current_node.y() +
            SinglyLinkedListNodeItem.HEIGHT / 2
        )

        # Target = top-center of next node
        end_x = (
            next_node.x() +
            SinglyLinkedListNodeItem.WIDTH / 2
        )

        end_y = next_node.y()

        # -----------------------------------------
        # Horizontal segment
        # -----------------------------------------

        horizontal = QGraphicsLineItem(
            start_x,
            start_y,
            end_x,
            start_y
        )

        horizontal.setPen(
            QPen(Qt.white, 2)
        )

        self.scene.addItem(horizontal)

        # -----------------------------------------
        # Vertical segment
        # -----------------------------------------

        vertical = QGraphicsLineItem(
            end_x,
            start_y,
            end_x,
            end_y
        )

        vertical.setPen(
            QPen(Qt.white, 2)
        )

        self.scene.addItem(vertical)

        # -----------------------------------------
        # Arrow head
        # -----------------------------------------

        arrow_head = self.create_arrow_head(
            end_x,
            end_y,
            end_x,
            start_y
        )

        # -----------------------------------------
        # Store relationship
        # -----------------------------------------

        return {
            "source": current_node,
            "target": next_node,
            "items": (
                horizontal,
                vertical,
                arrow_head
            )
        }

    def add_arrow(self, source, target):

        arrow = self.create_arrow(
            source,
            target
        )

        self.arrows.append(arrow)

        return arrow

    def add_null_arrow(self, node):

        arrow = self.create_null_arrow(node)

        self.arrows.append(arrow)

        return arrow


    def add_reverse_arrow(self, source, target):

        arrow = self.create_reverse_arrow(
            source,
            target
        )

        self.arrows.append(arrow)

        return arrow

    def create_reverse_arrow(self, source, target):

        # Start at bottom-center of source
        start_x = (
            source.x() + SinglyLinkedListNodeItem.WIDTH / 2
        )

        start_y = (
            source.y() + SinglyLinkedListNodeItem.HEIGHT 
        )

        end_x = (
            target.x() + SinglyLinkedListNodeItem.WIDTH / 2
        )

        end_y = (
            target.y() + SinglyLinkedListNodeItem.HEIGHT 
        )

        # Route below the source, then left
        # then upward into the target

        route_y = start_y + 90

        vertical_down = QGraphicsLineItem(
            start_x, start_y, start_x, route_y
        )

        horizontal = QGraphicsLineItem(
            start_x, route_y, end_x, route_y
        )

        vertical_up = QGraphicsLineItem(
            end_x, route_y, end_x, end_y
        )

        for line in (vertical_down, horizontal, vertical_up):

            line.setPen(
                QPen(Qt.white, 2)
            )

            self.scene.addItem(line)

        arrow_head = self.create_arrow_head(
            end_x, end_y, end_x, route_y
        )

        return{
            "source": source,
            "target" : target,
            "items": (
                vertical_down,
                horizontal,
                vertical_up,
                arrow_head
            )
        }

    def remove_arrow(self, source, target):

        for arrow in self.arrows:

            if (
                arrow["source"] is source
                and arrow["target"] is target
            ):

                for item in arrow["items"]:
                    self.scene.removeItem(item)

                self.arrows.remove(arrow)

                return

    def remove_null_arrow(self, node):

        for arrow in self.arrows:

            if (
                arrow.get("type") == "null"
                and arrow["source"] is node
            ):

                for item in arrow["items"]:
                    self.scene.removeItem(item)

                self.arrows.remove(arrow)

                return

    def create_null_arrow(self, node):

        # Start from the right-middle of the NEXT box
        start_x = (
            node.x() +
            SinglyLinkedListNodeItem.WIDTH
        )

        start_y = (
            node.y() +
            SinglyLinkedListNodeItem.HEIGHT / 2
        )

        # Go right, then down
        end_x = start_x + 100
        end_y = start_y + 80

        # -----------------------------------------
        # Horizontal segment
        # -----------------------------------------

        horizontal = QGraphicsLineItem(
            start_x,
            start_y,
            end_x,
            start_y
        )

        horizontal.setPen(
            QPen(Qt.white, 2)
        )

        self.scene.addItem(horizontal)

        # -----------------------------------------
        # Vertical segment
        # -----------------------------------------

        vertical = QGraphicsLineItem(
            end_x,
            start_y,
            end_x,
            end_y
        )

        vertical.setPen(
            QPen(Qt.white, 2)
        )

        self.scene.addItem(vertical)

        # -----------------------------------------
        # Arrow head
        # -----------------------------------------

        arrow_head = self.create_arrow_head(
            end_x,
            end_y,
            end_x,
            start_y
        )

        # -----------------------------------------
        # NULL label
        # -----------------------------------------

        null_text = QGraphicsTextItem("NULL")

        null_text.setDefaultTextColor(Qt.white)

        null_text.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Bold
            )
        )

        null_text.setPos(
            end_x - 20,
            end_y + 10
        )

        self.scene.addItem(null_text)

        # -----------------------------------------
        # Store NULL arrow
        # -----------------------------------------

        return {
            "source": node,
            "target": None,
            "type": "null",
            "items": (
                horizontal,
                vertical,
                arrow_head,
                null_text
            )
        }

    def create_arrow_head(
        self,
        end_x,
        end_y,
        start_x,
        start_y
    ):

        # Direction of the arrow

        dx = end_x - start_x
        dy = end_y - start_y

        length = (
            dx * dx +
            dy * dy
        ) ** 0.5

        if length == 0:
            return

        dx /= length
        dy /= length

        # Perpendicular vector

        px = -dy
        py = dx

        size = 10

        tip = QPointF(
            end_x,
            end_y
        )

        left = QPointF(
            end_x -
            dx * size +
            px * size / 2,

            end_y -
            dy * size +
            py * size / 2
        )

        right = QPointF(
            end_x -
            dx * size -
            px * size / 2,

            end_y -
            dy * size -
            py * size / 2
        )

        arrow_head = QGraphicsPolygonItem()

        arrow_head.setPolygon(
            QPolygonF([
            tip,
            left,
            right
            ])
        )

        arrow_head.setBrush(
            QBrush(Qt.white)
        )

        arrow_head.setPen(
            QPen(Qt.white)
        )

        self.scene.addItem(
            arrow_head
        )

        return arrow_head

    def set_selected_index(self, index):

        self.selected_index = index

        for i, node in enumerate(self.items):
            node.set_selected(
                i == self.selected_index
            )

    def is_animating(self):

        return self.animating

    def get_swap_center(self, first, second):

        first_node = self.items[first]
        second_node = self.items[second]

        center_x = (
            (first_node.x() + second_node.x()) / 2
            + SinglyLinkedListNodeItem.WIDTH / 2
        )

        center_y = (
            (first_node.y() + second_node.y()) / 2
            + SinglyLinkedListNodeItem.HEIGHT / 2
        )

        return center_x, center_y

    def animate_swap(self, first, second, finished=None):

        if self.animating:
            return

        if not (
            0 <= first < len(self.items)
            and 0 <= second < len(self.items)
        ):
            if finished:
                finished()
            return

        self.animating = True

        first_item = self.items[first]
        second_item = self.items[second]

        first_pos = first_item.pos()
        second_pos = second_item.pos()

        # Hide all arrows while nodes are moving
        for arrow in self.arrows:
            for item in arrow["items"]:
                item.hide()

        animation = QVariantAnimation()
        animation.setDuration(500)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)

        def update(value):

            progress = float(value)

            first_x = (
                first_pos.x() +
                (second_pos.x() - first_pos.x()) * progress
            )

            first_y = (
                first_pos.y() +
                (second_pos.y() - first_pos.y()) * progress
            )

            second_x = (
                second_pos.x() +
                (first_pos.x() - second_pos.x()) * progress
            )

            second_y = (
                second_pos.y() +
                (first_pos.y() - second_pos.y()) * progress
            )

            first_item.setPos(first_x, first_y)
            second_item.setPos(second_x, second_y)

        def finish():

            self.animating = False

            # Put them exactly at their destinations
            first_item.setPos(second_pos)
            second_item.setPos(first_pos)

            if finished:
                finished()

            self.swap_animation = None

        animation.valueChanged.connect(update)
        animation.finished.connect(finish)

        self.swap_animation = animation
        animation.start()

    def animate_swap_left(self, index, finished=None):

        if self.animating:
            return

        if index <= 0 or index >= len(self.items):
            if finished:
                finished()
            return

        self.animating = True

        first = self.items[index - 1]
        second = self.items[index]

        previous = (
            self.items[index - 2]
            if index >= 2
            else None
        )

        after = (
            self.items[index + 1]
            if index + 1 < len(self.items)
            else None
        )

        def step_one():

            # previous -> first
            # becomes
            # previous -> second

            if previous is not None:

                self.remove_arrow(
                    previous,
                    first
                )

                previous.set_next_address(
                    second.address
                )

                self.add_arrow(
                    previous,
                    second
                )

            QTimer.singleShot(
                1000,
                step_two
            )

        def step_two():

            # first -> second
            # becomes
            # first -> after

            self.remove_arrow(
                first,
                second
            )

            if after is not None:

                first.set_next_address(
                    after.address
                )

                self.add_arrow(
                    first,
                    after
                )

            else:

                first.set_next_address("NULL")

                self.remove_null_arrow(second)

                self.add_null_arrow(first)

            QTimer.singleShot(
                1000,
                step_three
            )

        def finish_swap():

            self.animating = False

            if finished:
                finished()

        def step_three():

            # second -> after
            # becomes
            # second -> first

            if after is not None:

                self.remove_arrow(
                    second,
                    after
                )

            second.set_next_address(
                first.address
            )

            self.add_reverse_arrow(
                second,
                first
            )

            # IMPORTANT:
            # Keep the third arrow visible BEFORE
            # allowing the actual node swap to happen.
            QTimer.singleShot(
                1000,
                finish_swap
            )
        step_one()