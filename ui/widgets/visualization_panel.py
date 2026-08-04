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
            padding:20px;
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

        x = self.array_visualizer.START_X + index * (self.array_visualizer.BOX_WIDTH + self.array_visualizer.SPACING)

        self.view.centerOn(
            x + self.array_visualizer.BOX_WIDTH / 2,
            self.array_visualizer.START_Y
        )