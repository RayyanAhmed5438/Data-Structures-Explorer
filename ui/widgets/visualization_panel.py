from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGraphicsView, 
    QFrame,
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, QPointF
from visualization.graphics_scene import GraphicsScene
from visualization.visualizers.array_visualizer import ArrayVisualizer
from visualization.visualizers.singly_linked_list_visualizer import (
    SinglyLinkedListNodeItem,
    SinglyLinkedListVisualizer
)
from core.enums.visualization_mode import VisualizationMode


class VisualizationPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.scene = GraphicsScene()

        self.view = QGraphicsView()


        self.view.setScene(self.scene)

        self.zoom_factor = 1.0

        self.view.setBackgroundBrush(Qt.black)
        self.view.setFrameShape(QFrame.NoFrame)

        self.view.setDragMode(QGraphicsView.ScrollHandDrag)

        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scrollbars_visible = False

        self.visualization_mode = VisualizationMode.ARRAY
        
        self.view.setStyleSheet("""
        QGraphicsView {
            border:1px solid #444;
    
            background:#17181C;
            border-radius: 10px;
        }
        """)

        
        self.scroll_animation = QPropertyAnimation(
            self.view.horizontalScrollBar(), b"value"
        )
        self.vertical_scroll_animation = QPropertyAnimation(
            self.view.verticalScrollBar(), b"value"
        )

        # Use the same duration and easing for both axes so the view moves
        # diagonally as a single smooth camera motion.
        for animation in (
            self.scroll_animation,
            self.vertical_scroll_animation
        ):
            animation.setDuration(550)
            animation.setEasingCurve(QEasingCurve.InOutCubic)

        self.array_visualizer = ArrayVisualizer(self.scene)

        self.singly_linked_list_visualizer = SinglyLinkedListVisualizer(self.scene)

              
        layout.addWidget(self.view)

        self.setLayout(layout)

    def toggle_scrollbars(self):

        self.scrollbars_visible = (
            not self.scrollbars_visible
        )

        if self.scrollbars_visible:

            self.view.setHorizontalScrollBarPolicy(
                Qt.ScrollBarAsNeeded
            )

            self.view.setVerticalScrollBarPolicy(
                Qt.ScrollBarAsNeeded
            )

        else:

            self.view.setHorizontalScrollBarPolicy(
                Qt.ScrollBarAlwaysOff
            )

            self.view.setVerticalScrollBarPolicy(
                Qt.ScrollBarAlwaysOff
            )

    def visualize_array(self, array):
        self.array_visualizer.visualize(array)

    def visualize(self, structure):

        if self.visualization_mode == VisualizationMode.ARRAY:

            self.array_visualizer.visualize(structure)

        elif self.visualization_mode == VisualizationMode.LINKED_LIST:

            self.singly_linked_list_visualizer.visualize(structure)

    def set_selected_index(self, index):

        self.array_visualizer.selected_index = index

        self.singly_linked_list_visualizer.selected_index = index

        if self.visualization_mode == VisualizationMode.ARRAY:
            self.array_visualizer.set_selected_index(index)

        elif self.visualization_mode == VisualizationMode.LINKED_LIST:

            self.singly_linked_list_visualizer.set_selected_index(index)

    def smooth_scroll_to_index(self, index):

        scene_x = (
            self.array_visualizer.START_X +
            index * (
                self.array_visualizer.BOX_WIDTH + 
                self.array_visualizer.SPACING
            )+
            self.array_visualizer.BOX_WIDTH / 2
        )

        self.smooth_scroll_to(scene_x)

    def center_on_linked_swap(self, first, second):

        x, y = self.singly_linked_list_visualizer.get_swap_center(
            first,
            second
        )

        self.smooth_center_on(x, y)

    def center_on_linked_node(self, index):

        if (
            index < 0 or
            index >= len(self.singly_linked_list_visualizer.items)
        ):
            return

        node = self.singly_linked_list_visualizer.items[index]

        center_x = (
            node.x() + SinglyLinkedListNodeItem.WIDTH / 2
        )
        center_y = (
            node.y() + SinglyLinkedListNodeItem.HEIGHT / 2
        )

        self.smooth_center_on(center_x, center_y)

    def center_on_linked_insert(self, index):
        # Keep the existing insertion API; centering now scrolls smoothly.
        self.center_on_linked_node(index)

    def smooth_scroll_to_swap(self, first, second):

        middle = (first + second) / 2

        scene_x = (
            self.array_visualizer.START_X +
            middle * (
                self.array_visualizer.BOX_WIDTH +
                self.array_visualizer.SPACING
            ) +
            self.array_visualizer.BOX_WIDTH / 2
        )

        self.smooth_scroll_to(scene_x)

    def smooth_center_on(self, scene_x, scene_y):
        """Smoothly center a scene point using both scrollbars."""

        # Stop any previous camera motion before computing the new target.
        self.scroll_animation.stop()
        self.vertical_scroll_animation.stop()

        scene_point = QPointF(scene_x, scene_y)
        viewport_point = self.view.mapFromScene(scene_point)
        viewport = self.view.viewport()

        horizontal = self.view.horizontalScrollBar()
        vertical = self.view.verticalScrollBar()

        target_horizontal = int(
            horizontal.value()
            + viewport_point.x()
            - viewport.width() / 2
        )
        target_vertical = int(
            vertical.value()
            + viewport_point.y()
            - viewport.height() / 2
        )

        target_horizontal = max(
            horizontal.minimum(),
            min(target_horizontal, horizontal.maximum())
        )
        target_vertical = max(
            vertical.minimum(),
            min(target_vertical, vertical.maximum())
        )

        self.scroll_animation.setStartValue(horizontal.value())
        self.scroll_animation.setEndValue(target_horizontal)

        self.vertical_scroll_animation.setStartValue(vertical.value())
        self.vertical_scroll_animation.setEndValue(target_vertical)

        self.scroll_animation.start()
        self.vertical_scroll_animation.start()

    def animate_swap(self, first, second, finished=None):

        if self.visualization_mode == VisualizationMode.ARRAY:

            self.array_visualizer.animate_swap(
                first,
                second,
                finished,
            )

        elif self.visualization_mode == VisualizationMode.LINKED_LIST:

            
            if second == first - 1:

                self.singly_linked_list_visualizer.animate_swap_left(
                    first, finished
                )

            elif second == first + 1:

                self.singly_linked_list_visualizer.animate_swap_right(
                    first, finished
                )

    def animate_insert(self, index, song_name, finished=None, started=None):

        if self.visualization_mode == VisualizationMode.ARRAY:

            self.array_visualizer.animate_insert(
                index,
                song_name,
                finished=finished,
                started=started
            )

        elif self.visualization_mode == VisualizationMode.LINKED_LIST:

            self.singly_linked_list_visualizer.animate_insert(
                index,
                song_name,
                finished=finished,
                started=started
            )

    

    def animate_delete(self, index, finished=None):

        if self.visualization_mode ==  VisualizationMode.ARRAY:
            
            self.array_visualizer.animate_delete(
                index, finished
            )

        elif self.visualization_mode == VisualizationMode.LINKED_LIST:

            self.singly_linked_list_visualizer.animate_delete(
                index, finished
            )

    def smooth_scroll_to(self, scene_x):

        # Array visualizations are horizontal, so only the horizontal camera
        # position changes. Stop any old vertical movement first.
        self.scroll_animation.stop()
        self.vertical_scroll_animation.stop()

        viewport_width = self.view.viewport().width()
        horizontal = self.view.horizontalScrollBar()

        target = int(scene_x - viewport_width / 2)
        target = max(
            horizontal.minimum(),
            min(target, horizontal.maximum())
        )

        self.scroll_animation.setStartValue(horizontal.value())
        self.scroll_animation.setEndValue(target)
        self.scroll_animation.start()

    def zoom_in(self):

        if self.zoom_factor >= 2.5:
            return

        self.view.scale(
            1.15,
            1.15
        )

        self.zoom_factor *= 1.15


    def zoom_out(self):

        if self.zoom_factor <= 0.4:
            return

        self.view.scale(
            1 / 1.15,
            1 / 1.15
        )

        self.zoom_factor /= 1.15

    def is_animating(self):
        return self.array_visualizer.animating or self.singly_linked_list_visualizer.animating

    def set_visualization_mode(self, mode):

        self.visualization_mode = mode