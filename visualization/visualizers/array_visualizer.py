from visualization.graphics_scene import GraphicsScene
from PyQt5.QtGui import QFont, QColor

BOX_WIDTH = 140
BOX_HEIGHT = 90

START_X = 80
START_Y = 150

SPACING = 1

class ArrayVisualizer:

    def __init__(self, scene: GraphicsScene):
        self.scene = scene

        
    def visualize(self, array):

        print("called visualize")
        print(array.get_all())
        print(len(array.get_all()))

        self.scene.clear_scene()

        for index, song in enumerate(array.get_all()):

            x = START_X + index * (BOX_WIDTH + SPACING)

            y = START_Y

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


            index_text = self.scene.draw_text(
                str(index),
                x + 60, y + BOX_HEIGHT + 12
            )
            
            index_text.setFont(QFont("Segoe UI", 9))
            index_text.setDefaultTextColor(QColor(170, 170, 170))

            self.scene.items_map[index] = {
                "box": box,
                "text": text,
                "index": index_text
            }

        self.scene.fit_with_margin(30)