from visualization.array_node import ArrayNode
from visualization.graphics_scene import GraphicsScene
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, QPointF, QTimer

class ArrayVisualizer:

    BOX_WIDTH = 140
    BOX_HEIGHT = 90
    START_X = 80
    START_Y = 150
    SPACING = 1

    ANIMATION_DURATION = 1000
    FRAME_TIME = 16

    def __init__(self, scene: GraphicsScene):
        self.scene = scene

        self.selected_index = -1

        self.marker_text = None
        self.marker_index = -1

        self.items = []
        self.current_array = None

        self.temp_box = None
        self.temp_text = None
        self.temp_label = None

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_animation
        )

        self.animation = None

        
    def visualize(self, array):

        self.current_array = array

        if len(self.items) != len(array.get_all()):
            self.create_items(array)
            return

        self.refresh_scene()

    def refresh_scene(self):
        pass

    def create_items(self, array):

        self.scene.clear_scene()
        self.items.clear()

        self.create_temp_box()
            
        for index, song in enumerate(array.get_all()):

            node = ArrayNode(
                song,
                index,
                index == self.selected_index
            )

            position = self.get_box_position(index)

            node.setPos(position)

            self.scene.addItem(node)

            self.items.append({
                "song": song,
                "node": node
            })

        self.scene.fit_with_margin(30)
    

    def animate_item(self, visual_item, end_pos, finished=None):

        self.animation = {
            "item": visual_item,

            "start": visual_item["node"].pos(),

            "end": end_pos,

            "duration": self.ANIMATION_DURATION,

            "elapsed": 0,

            "finished": finished
        }

        self.timer.start(self.FRAME_TIME)

    def update_animation(self):

        if self.animation is None:
            return

        self.animation["elapsed"] += self.FRAME_TIME

        progress = (
            self.animation["elapsed"] / self.animation["duration"]
        )

        if progress >= 1:

            progress = 1

            self.timer.stop()
            callback = self.animation["finished"]
            self.animation = None

            if callback:
                callback()

            return

        start = self.animation["start"]
        end = self.animation["end"]

        x = start.x() + (end.x() - start.x()) * progress
        y = start.y() + (end.y() - start.y()) * progress

        self.animation["item"]["node"].setPos(x, y)


    def animate_to_temp(self, index):

        item = self.items[index]

        self.show_temp(
            ""
        )


        # temp = self.get_temp_position()

        # self.center_text(
        #     self.temp_text,
        #     temp.x(),
        #     temp.y()
        # )

        print("BOX POS :", item["node"].pos())

        print("TEMP POS :", self.temp_box.pos())
        print("TEMP RECT:", self.temp_box.rect())

        self.animate_item(
            item, self.get_temp_position()
        )


    def animate_swap(self, first, second):
            pass

    def center_text(self, text_item, x, y):

        rect = text_item.boundingRect()

        text_item.setPos(
            x + (self.BOX_WIDTH - rect.width()) / 2,
            y + (self.BOX_HEIGHT - rect.height()) / 2
        )


    def get_box_position(self, index):
    
            return QPointF(
                self.START_X + index * (self.BOX_WIDTH + self.SPACING),
                self.START_Y
            )
    
    def get_temp_position(self):
    
        return QPointF(
            self.START_X,
            self.START_Y - 170
        )


    def create_temp_box(self):

        x = self.START_X
        y = self.START_Y - 170

        self.temp_box = self.scene.draw_box(
            x, y, self.BOX_WIDTH, self.BOX_HEIGHT
        )

        self.temp_text = self.scene.draw_text(
            "", 0, 0, self.BOX_WIDTH - 20
        )

        self.temp_label = self.scene.draw_text(
            "temp", x + 45, y - 35
        )


        self.hide_temp()

    def show_temp(self, song_name):

        self.temp_text.setPlainText(song_name)

        temp = self.get_temp_position()

        self.center_text(
            self.temp_text,
            temp.x(),
            temp.y()
        )

        self.temp_box.show()
        self.temp_text.show()
        self.temp_label.show()

    def hide_temp(self):

        self.temp_box.hide()
        self.temp_text.hide()
        self.temp_label.hide()

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