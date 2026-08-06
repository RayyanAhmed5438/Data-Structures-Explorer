from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGraphicsView, QFrame
from PyQt5.QtCore import Qt
from visualization.graphics_scene import GraphicsScene
from visualization.visualizers.array_visualizer import ArrayVisualizer


class VisualizationPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.scene = GraphicsScene()

        self.view = QGraphicsView()


        self.view.setScene(self.scene)
        

        self.view.setBackgroundBrush(Qt.black)
        self.view.setFrameShape(QFrame.NoFrame)

        
        self.view.setStyleSheet("""
        QGraphicsView {
            border:1px solid #444;
    
            background:#17181C;
            border-radius: 10px;
        }
        """)

        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)


        self.array_visualizer = ArrayVisualizer(self.scene)


        layout.addWidget(self.view)

        self.setLayout(layout)

    def visualize_array(self, array):
        self.array_visualizer.visualize(array)

    def set_selected_index(self, index):
        self.array_visualizer.set_selected_index(index)

    def set_marker(self, index, text):
        self.array_visualizer.set_marker(index, text)

    def center_on_index(self, index):

        x = self.array_visualizer.START_X + index * (
            self.array_visualizer.BOX_WIDTH + 
            self.array_visualizer.SPACING
            )

        self.view.centerOn(
            x + self.array_visualizer.BOX_WIDTH / 2,
            self.array_visualizer.START_Y
        )

    def center_on_insert(self):

        self.center_on_index(
            self.array_visualizer.get_item_count() - 1
        )

    def center_on_swap(self, first, second):

        middle = (first + second) / 2

        x = (
            self.array_visualizer.START_X +
            middle * (
                self.array_visualizer.BOX_WIDTH +
                self.array_visualizer.SPACING
            )
        )

        self.view.centerOn(
            x + self.array_visualizer.BOX_WIDTH / 2,
            self.array_visualizer.START_Y
        )

    def animate_swap(self, first, second, finished=None):

        self.array_visualizer.animate_swap(
            first,
            second,
            finished,
        )

    def animate_insert(self, index, song_name, finished=None, started=None):

        self.array_visualizer.animate_insert(
            index,
            song_name,
            finished=finished,
            started=started
        )

    def animate_delete(self, index, finished=None):

        self.array_visualizer.animate_delete(
            index, finished
        )


    def is_animating(self):
        return self.array_visualizer.animating