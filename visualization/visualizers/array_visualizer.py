from visualization.graphics_scene import GraphicsScene
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

BOX_WIDTH = 140
BOX_HEIGHT = 90

START_X = 80
START_Y = 150

SPACING = 1

class ArrayVisualizer:

    def __init__(self, scene: GraphicsScene):
        self.scene = scene

        self.selected_index = -1

        self.marker_text = None
        self.marker_index = -1

        
    def visualize(self, array):

        self.current_array = array

        self.scene.clear_scene()

        for index, song in enumerate(array.get_all()):

            x = START_X + index * (BOX_WIDTH + SPACING)
            y = START_Y

            if index == self.selected_index:
                box = self.scene.draw_box(
                    x, y,
                    BOX_WIDTH, BOX_HEIGHT,
                    fill_color = QColor("#3E6AE1")
                )
            else:

                box = self.scene.draw_box(
                    x, y, BOX_WIDTH, BOX_HEIGHT
                )


            text = self.scene.draw_text(
                song.title,0, 0
            )
            rect = text.boundingRect()

            text_x = x + (BOX_WIDTH - rect.width()) / 2
            text_y = y + (BOX_HEIGHT - rect.height()) / 2

            text.setPos(text_x, text_y)


            if index == self.selected_index:
                text.setDefaultTextColor(Qt.white)


            index_text = self.scene.draw_text(
                str(index),
                x + 60, y + BOX_HEIGHT + 12
            )
            
            index_text.setFont(QFont("Segoe UI", 9))
            index_text.setDefaultTextColor(QColor(170, 170, 170))


            if index == self.marker_index:


                marker = self.scene.draw_text(
                    self.marker_text, 0, 0
                )

                marker_rect = marker.boundingRect()

                marker.setPos(
                    x + (BOX_WIDTH - marker_rect.width()) / 2,
                    y + BOX_HEIGHT + 55
                )

                marker.setDefaultTextColor(QColor(220, 220, 220))
                marker.setFont(QFont("Segoe UI", 9))


            self.scene.items_map[index] = {
                "box": box,
                "text": text,
                "index": index_text
            }



        self.scene.fit_with_margin(30)

    def set_selected_index(self, index):

        self.selected_index = index

        self._redraw()

    def set_marker(self, index, text):

        self.marker_index = index
        self.marker_text = text
        self._redraw()

    def _redraw(self):
        if self.current_array is not None:
            self.visualize(self.current_array)