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

    # Each arrow component is faded separately before moving to the next.
    DELETE_LINE_FADE_DURATION_MS = 320
    DELETE_LINE_PAUSE_MS = 100
    DELETE_FADE_DURATION_MS = 700

    def __init__(self, scene):

        self.scene = scene

        self.items = []
        self.arrows = []

        self.selected_index = -1

        self.animating = False
        self._active_delete_animation = None

        self.null_endpoint = None
        

    def visualize(self, linked_list):

        self.scene.clear()

        self.items.clear()
        self.arrows.clear()

        self.null_endpoint = None

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
            node.address_label = address_text

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
            self.create_null_endpoint(self.items[-1])

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
            SinglyLinkedListNodeItem.DATA_WIDTH
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

    def add_insert_arrow(self, source, target):

        # Start from the right side of PREVIOUS
        start_x = (
            source.x() +
            SinglyLinkedListNodeItem.WIDTH
        )

        start_y = (
            source.y() +
            SinglyLinkedListNodeItem.HEIGHT / 2
        )

        # Go horizontally right until directly below
        # the DATA/NEXT divider of NEW
        turn_x = (
            target.x() +
            SinglyLinkedListNodeItem.DATA_WIDTH - 40
        )

        # Enter NEW from its bottom
        end_y = (
            target.y() +
            SinglyLinkedListNodeItem.HEIGHT
        )

        # -----------------------------
        # _
        # -----------------------------

        horizontal = QGraphicsLineItem(
            start_x,
            start_y,
            turn_x,
            start_y
        )

        horizontal.setPen(
            QPen(Qt.white, 2)
        )

        self.scene.addItem(horizontal)

        # -----------------------------
        # |
        # -----------------------------

        vertical = QGraphicsLineItem(
            turn_x,
            start_y,
            turn_x,
            end_y
        )

        vertical.setPen(
            QPen(Qt.white, 2)
        )

        self.scene.addItem(vertical)

        # Arrow points UP into NEW
        arrow_head = self.create_arrow_head(
            turn_x,
            end_y,
            turn_x,
            start_y
        )

        arrow = {
            "source": source,
            "target": target,
            "type": "insert",
            "items": (
                horizontal,
                vertical,
                arrow_head
            )
        }

        self.arrows.append(arrow)

        return arrow

    def add_straight_down_arrow(
        self,
        source,
        target
    ):

        x = (
            source.x() +
            SinglyLinkedListNodeItem.DATA_WIDTH
        )

        start_y = (
            source.y() +
            SinglyLinkedListNodeItem.HEIGHT
        )

        end_y = target.y()

        line = QGraphicsLineItem(
            x,
            start_y,
            x,
            end_y
        )

        line.setPen(
            QPen(Qt.white, 2)
        )

        self.scene.addItem(line)

        arrow_head = self.create_arrow_head(
            x,
            end_y,
            x,
            start_y
        )

        arrow = {
            "source": source,
            "target": target,
            "type": "insert_down",
            "items": (
                line,
                arrow_head
            )
        }

        self.arrows.append(arrow)

        return arrow

    def add_straight_null_arrow(self, node):

        # The DATA/NEXT divider of NEW
        x = (
            node.x() +
            SinglyLinkedListNodeItem.DATA_WIDTH
        )

        start_y = (
            node.y() +
            SinglyLinkedListNodeItem.HEIGHT
        )

        # Same point used by the existing NULL arrow
        end_y = (
            self.null_endpoint.y() - 10
        )

        line = QGraphicsLineItem(
            x,
            start_y,
            x,
            end_y
        )

        line.setPen(
            QPen(Qt.white, 2)
        )

        self.scene.addItem(line)

        arrow_head = self.create_arrow_head(
            x,
            end_y,
            x,
            start_y
        )

        arrow = {
            "source": node,
            "target": "NULL",
            "type": "insert_null_down",
            "items": (
                line,
                arrow_head
            )
        }

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

    def create_null_endpoint(self, node):

        if self.null_endpoint is not None:
            return

        self.null_endpoint = QGraphicsTextItem("NULL")

        self.null_endpoint.setDefaultTextColor(Qt.white)

        self.null_endpoint.setFont(
            QFont(
                "Segoe UI",
                10,
                QFont.Bold
            )
        )

        x = (
            node.x()
            + SinglyLinkedListNodeItem.WIDTH
            + 80
        )

        y = (
            node.y()
            + SinglyLinkedListNodeItem.HEIGHT / 2
            + 90
        )

        self.null_endpoint.setPos(
            x - 20,
            y + 10
        )

        self.scene.addItem(self.null_endpoint)

  
    def create_null_arrow(self, node):

        if self.null_endpoint is None:
            self.create_null_endpoint(
                self.items[-1]
            )

        start_x = (
            node.x()
            + SinglyLinkedListNodeItem.WIDTH
        )

        start_y = (
            node.y()
            + SinglyLinkedListNodeItem.HEIGHT / 2
        )

        end_x = self.null_endpoint.x() + 20
        end_y = self.null_endpoint.y() - 10

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

        arrow_head = self.create_arrow_head(
            end_x,
            end_y,
            end_x,
            start_y
        )

        return {
            "source": node,
            "target": "NULL",
            "type": "null",
            "items": (
                horizontal,
                vertical,
                arrow_head
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

                self.remove_null_arrow(second)

                first.set_next_address("NULL")

                
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

    def animate_swap_right(self, index, finished = None):

        if self.animating:
            return

        if index < 0 or index >= len(self.items) - 1:
            if finished:
                finished()
            return

        self.animating = True

        first = self.items[index]
        second = self.items[index + 1]

        previous = (
            self.items[index - 1]
            if index > 0
            else None
        )

        after = (
            self.items[index + 2]
            if index + 2 < len(self.items)
            else None
        )

        def finish_swap():
            self.animating = False

            if finished:
                finished()

        def step_three():

            if after is not None:

                self.remove_arrow(
                    second, after
                )

            else:
                self.remove_null_arrow(second)

            second.set_next_address(first.address)

            self.add_reverse_arrow(
                second, first
            )

            QTimer.singleShot(
                1000, finish_swap
            )

        def step_two():

            self.remove_arrow(
                first, second
            )

            if after is not None:

                first.set_next_address(after.address)

                self.add_arrow(first, after)

            else:

                self.remove_null_arrow(second)

                first.set_next_address("NULL")

                self.add_null_arrow(first)

            QTimer.singleShot(
                1000, step_three
            )
        def step_one():

            if previous is not None:

                self.remove_arrow(
                    previous, first
                )

                previous.set_next_address(
                    second.address
                )

                self.add_arrow(previous, second)

            QTimer.singleShot(
                1000, step_two
            )

        step_one()

    def animate_delete(self, index, finished=None):
        """
        Animate removal of a node without mutating the underlying linked list.

        Existing pointer components disappear one at a time. Once the old
        arrows have been removed, the surviving pointer is created (if needed)
        and the target node fades out. The application performs the actual
        deletion in the finished callback and then refreshes the visualization.
        """
        if self.animating:
            return

        if index < 0 or index >= len(self.items):
            if finished:
                finished()
            return

        self.animating = True

        node = self.items[index]
        previous = self.items[index - 1] if index > 0 else None
        next_node = (
            self.items[index + 1]
            if index + 1 < len(self.items)
            else None
        )

        # CASE 1: Delete the first node (or the only node).
        if previous is None:
            if next_node is not None:
                arrows_to_remove = [
                    self._take_arrow_for_animation(node, next_node)
                ]
            else:
                arrows_to_remove = [
                    self._take_arrow_for_animation(
                        node, "NULL", arrow_type="null"
                    )
                ]

            def finish_first_pointer_changes():
                # An empty list should not leave a detached NULL label behind.
                if next_node is None and self.null_endpoint is not None:
                    self.scene.removeItem(self.null_endpoint)
                    self.null_endpoint = None

                self._fade_deleted_node(node, finished)

            self._animate_remove_arrows(
                arrows_to_remove,
                finish_first_pointer_changes
            )
            return

        # CASE 2: Delete the last node. Remove both old connections in sequence,
        # then redirect the previous node to NULL before fading the old tail.
        if next_node is None:
            arrows_to_remove = [
                self._take_arrow_for_animation(previous, node),
                self._take_arrow_for_animation(
                    node, "NULL", arrow_type="null"
                )
            ]

            def finish_last_pointer_changes():
                previous.set_next_address("NULL")
                self.reposition_null_endpoint(previous)
                self.add_null_arrow(previous)
                self._fade_deleted_node(node, finished)

            self._animate_remove_arrows(
                arrows_to_remove,
                finish_last_pointer_changes
            )
            return

        # CASE 3: Delete a middle node. Remove its incoming and outgoing arrows
        # component-by-component, then create the predecessor -> successor arrow.
        arrows_to_remove = [
            self._take_arrow_for_animation(previous, node),
            self._take_arrow_for_animation(node, next_node)
        ]

        def finish_middle_pointer_changes():
            previous.set_next_address(next_node.address)
            self.add_arrow(previous, next_node)
            self._fade_deleted_node(node, finished)

        self._animate_remove_arrows(
            arrows_to_remove,
            finish_middle_pointer_changes
        )

    def _take_arrow_for_animation(
        self,
        source,
        target,
        arrow_type=None
    ):
        """Detach an arrow record so it can be removed visually in stages."""
        for index, arrow in enumerate(self.arrows):
            if (
                arrow.get("source") is source
                and arrow.get("target") is target
                and (
                    arrow_type is None
                    or arrow.get("type") == arrow_type
                )
            ):
                return self.arrows.pop(index)

        return None

    def _animate_remove_arrows(self, arrows, finished):
        """
        Fade arrowheads and line segments one at a time, retracting each arrow
        from its target back toward its source.
        """
        components = []

        for arrow in arrows:
            if arrow is None:
                continue

            # create_arrow/create_null_arrow store horizontal, vertical, head.
            # Reverse this so each connection retracts from its arrowhead first.
            components.extend(
                item for item in reversed(arrow["items"])
                if item is not None
            )

        def remove_next_component():
            if not components:
                finished()
                return

            item = components.pop(0)
            animation = QVariantAnimation(self.scene)
            animation.setDuration(self.DELETE_LINE_FADE_DURATION_MS)
            animation.setStartValue(1.0)
            animation.setEndValue(0.0)
            animation.valueChanged.connect(
                lambda value, graphic_item=item:
                    graphic_item.setOpacity(float(value))
            )

            def component_faded():
                item.setOpacity(0.0)

                if item.scene() is self.scene:
                    self.scene.removeItem(item)

                if self._active_delete_animation is animation:
                    self._active_delete_animation = None

                animation.deleteLater()

                # This short gap makes the sequential removals visually distinct.
                QTimer.singleShot(
                    self.DELETE_LINE_PAUSE_MS,
                    remove_next_component
                )

            animation.finished.connect(component_faded)
            self._active_delete_animation = animation
            animation.start()

        remove_next_component()

    def _fade_deleted_node(self, node, finished=None):
        """Fade the deleted node and its separately rendered address label."""
        address_label = getattr(node, "address_label", None)

        animation = QVariantAnimation(self.scene)
        animation.setDuration(self.DELETE_FADE_DURATION_MS)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)

        def update_opacity(value):
            opacity = float(value)
            node.setOpacity(opacity)

            if address_label is not None:
                address_label.setOpacity(opacity)

        animation.valueChanged.connect(update_opacity)

        def complete():
            node.setOpacity(0.0)

            if address_label is not None:
                address_label.setOpacity(0.0)

            self.animating = False
            if self._active_delete_animation is animation:
                self._active_delete_animation = None

            animation.deleteLater()

            # MainWindow handles the model deletion and refresh in this callback.
            if finished:
                finished()

        animation.finished.connect(complete)
        self._active_delete_animation = animation
        animation.start()

    def reposition_null_endpoint(self, node):
    
        x = (
            node.x()
            + SinglyLinkedListNodeItem.WIDTH
            + 80
        )

        y = (
            node.y()
            + SinglyLinkedListNodeItem.HEIGHT / 2
            + 90
        )

        self.null_endpoint.setPos(
            x - 20,
            y + 10
        )


    def animate_insert(
        self,
        index,
        song_name,
        finished=None,
        started=None
    ):

        if self.animating:
            return

        if index < 0 or index > len(self.items):

            if finished:
                finished()

            return

        self.temp_address_text = None

        self.animating = True

        # -----------------------------------------
        # Existing nodes
        # -----------------------------------------

        previous = (
            self.items[index - 1]
            if index > 0
            else None
        )

        next_node = (
            self.items[index]
            if index < len(self.items)
            else None
        )

        # -----------------------------------------
        # New node position
        # -----------------------------------------

        if previous is None and next_node is not None:

            # =====================================
            # INSERT AT BEGINNING
            #
            # Put NEW directly before FIRST.
            # =====================================

            new_x = (
                next_node.x()
                - SinglyLinkedListNodeItem.WIDTH
                - self.NODE_GAP_X
            )

            new_y = (
                next_node.y()
                - self.NODE_GAP_Y
            )


        elif previous is not None:

            # =====================================
            # MIDDLE AND END USE THE SAME DESIGN
            #
            # Put NEW directly above:
            # - NEXT, or
            # - the existing NULL endpoint
            # =====================================

            if next_node is not None:

                # Directly above NEXT
                new_x = next_node.x()

                new_y = (
                    min(
                        previous.y(),
                        next_node.y()
                    )
                    - 180
                )

            else:

                # Directly above the existing NULL.
                # Align NEW's DATA/NEXT divider with
                # the existing NULL arrow endpoint.
                null_arrow_x = (
                    self.null_endpoint.x() + 20
                )

                new_x = (
                    null_arrow_x
                    - SinglyLinkedListNodeItem.DATA_WIDTH
                )

                new_y = (
                    min(
                        previous.y(),
                        self.null_endpoint.y()
                    )
                    - 180
                )


        else:

            # =====================================
            # EMPTY LIST
            # =====================================

            new_x = self.START_X
            new_y = self.START_Y

        # -----------------------------------------
        # Determine the temporary NEXT address
        # -----------------------------------------

        if next_node is not None:

            next_address = next_node.address

        else:

            next_address = "NULL"

        # -----------------------------------------
        # Create the new visual node
        # -----------------------------------------

        new_node = SinglyLinkedListNodeItem(
            song_name,
            "NEW",
            next_address
        )

        new_node.setPos(
            new_x,
            new_y
        )

        self.scene.addItem(new_node)

        # Keep it available during animation
        self.items.insert(
            index,
            new_node
        )

        # -----------------------------------------
        # Address label
        # -----------------------------------------

        address_text = QGraphicsTextItem(
            "NEW"
        )

        address_text.setDefaultTextColor(
            Qt.white
        )

        address_text.setFont(
            QFont(
                "Segoe UI",
                9
            )
        )

        address_width = (
            address_text.boundingRect().width()
        )

        address_text.setPos(
            new_x +
            (
                SinglyLinkedListNodeItem.WIDTH -
                address_width
            ) / 2,

            new_y +
            SinglyLinkedListNodeItem.HEIGHT +
            12
        )

        self.scene.addItem(
            address_text
        )

        self.temp_address_text = address_text

        # -----------------------------------------
        # Selection
        # -----------------------------------------

        new_node.set_selected(False)

        # -----------------------------------------
        # If something actually started the
        # insertion animation
        # -----------------------------------------

        if started:
            started()

        # -----------------------------------------
        # STEP 1
        #
        # previous -> next
        # becomes
        # previous -> NEW
        # -----------------------------------------

        def step_one():

            # =====================================
            # INSERT AT BEGINNING
            # =====================================

            if previous is None:

                # There is no old pointer to remove.
                # Just show NEW -> FIRST.
                QTimer.singleShot(
                    1000,
                    step_two
                )

                return


            # =====================================
            # MIDDLE OR END
            # =====================================

            if next_node is not None:

                # Remove:
                # PREVIOUS -> NEXT

                self.remove_arrow(
                    previous,
                    next_node
                )

            else:

                # Remove:
                # PREVIOUS -> NULL

                self.remove_null_arrow(
                    previous
                )


            # Update visible NEXT value
            previous.set_next_address(
                "NEW"
            )

            # Add:
            #
            # PREVIOUS ----|
            #              ↑
            #             NEW

            self.add_insert_arrow(
                previous,
                new_node
            )

            QTimer.singleShot(
                1200,
                step_two
            )

        # -----------------------------------------
        # STEP 2
        #
        # NEW -> next
        # -----------------------------------------

        def step_two():

            # =====================================
            # NEW -> NEXT
            # =====================================

            if next_node is not None:

                new_node.set_next_address(
                    next_node.address
                )

                # Beginning:
                # NEW is before FIRST.
                #
                # Middle:
                # NEW is directly above NEXT.
                #
                # The same normal method can handle
                # beginning, while the vertical method
                # is used for the middle layout.

                if previous is None:

                    self.add_arrow(
                        new_node,
                        next_node
                    )

                else:

                    self.add_straight_down_arrow(
                        new_node,
                        next_node
                    )


            # =====================================
            # NEW -> NULL
            # =====================================

            else:

                new_node.set_next_address(
                    "NULL"
                )

                self.add_straight_null_arrow(
                    new_node
                )


            QTimer.singleShot(
                1200,
                move_nodes
            )
        
        def move_nodes():

            

            rebuild_visualization()
        

        # -----------------------------------------
        # STEP 4
        #
        # Rebuild arrows at their final positions.
        # -----------------------------------------

        
        def rebuild_visualization():

            # Remove temporary NEW address label
            if self.temp_address_text is not None:

                self.scene.removeItem(
                    self.temp_address_text
                )

                self.temp_address_text = None

            # Remove every existing arrow
            for arrow in self.arrows:

                for item in arrow["items"]:

                    self.scene.removeItem(
                        item
                    )

            self.arrows.clear()

            # Reposition every node exactly
            for i, node in enumerate(self.items):

                x = (
                    self.START_X +
                    i * (
                        SinglyLinkedListNodeItem.WIDTH +
                        self.NODE_GAP_X
                    )
                )

                y = (
                    self.START_Y +
                    i * self.NODE_GAP_Y
                )

                node.setPos(
                    x,
                    y
                )

            # Recreate normal arrows
            for i in range(
                len(self.items) - 1
            ):

                self.add_arrow(
                    self.items[i],
                    self.items[i + 1]
                )

            # Recreate NULL arrow
            if self.items:

                self.reposition_null_endpoint(
                    self.items[-1]
                )

                self.add_null_arrow(
                    self.items[-1]
                )

            self.scene.fit_with_margin(
                400
            )

            self.animating = False

            if finished:
                finished()

        QTimer.singleShot(
            1000, step_one
        )


