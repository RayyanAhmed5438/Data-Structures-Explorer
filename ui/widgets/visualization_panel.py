from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation
from visualization.graphics_scene import GraphicsScene
from visualization.visualizers.array_visualizer import ArrayVisualizer
from visualization.visualizers.singly_linked_list_visualizer import (
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
        

        self.view.setBackgroundBrush(Qt.black)
        self.view.setFrameShape(QFrame.NoFrame)

        self.visualization_mode = VisualizationMode.ARRAY
        
        self.view.setStyleSheet("""
        QGraphicsView {
            border:1px solid #444;
    
            background:#17181C;
            border-radius: 10px;
        }
        """)

        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.scroll_animation = QPropertyAnimation(
            self.view.horizontalScrollBar(), b"value"
        )
        self.scroll_animation.setDuration(400)

        self.array_visualizer = ArrayVisualizer(self.scene)

        self.singly_linked_list_visualizer = SinglyLinkedListVisualizer(self.scene)


        layout.addWidget(self.view)

        self.setLayout(layout)

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

        self.view.centerOn(x, y)

    def smooth_scroll_to_swap(self, first, second):

        middle = (first + second) / 2

        scene_x = (
            self.array_visualizer.START_X +
            middle * (
                self.array_visualizer.BOX_WIDTH +
                self.array_visualizer.SPACING
            )+
            self.array_visualizer.BOX_WIDTH / 2
        )

        self.smooth_scroll_to(scene_x)

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

        self.array_visualizer.animate_insert(
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

        viewport_width = self.view.viewport().width()

        target = int(
            scene_x -
            viewport_width / 2
        )

        target = max(
            self.view.horizontalScrollBar().minimum(),
            min(
                target,
                self.view.horizontalScrollBar().maximum()
            )
        )

        self.scroll_animation.stop()

        current = self.scroll_animation.currentValue()

        if current is None:
            current = self.view.horizontalScrollBar().value()

        self.scroll_animation.setStartValue(
            current
        )

        self.scroll_animation.setEndValue(target)

        self.scroll_animation.start()


    def is_animating(self):
        return self.array_visualizer.animating

    def set_visualization_mode(self, mode):

        self.visualization_mode = mode