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

        self.animations = []

        self.swap_finished = None
        self.animating = False

        
    def visualize(self, array):

        self.current_array = array

        self.create_items(array)

        self.refresh_scene()

    def refresh_scene(self):

        rebuild = False

        for node, song in zip(
            self.items,
            self.current_array.get_all()
        ):
            if node.song is not song:
                rebuild = True
                break

        if rebuild:
            self.create_items(self.current_array)
            return

        for index, node in enumerate(self.items):
            node.set_selected(index == self.selected_index)

    def create_items(self, array):

        self.scene.clear_scene()
        self.items.clear()

        self.create_temp_box()

        print("Rebuilding:")
            
        for index, song in enumerate(array.get_all()):
            print(song.title)

            node = ArrayNode(
                song,
                index,
                index == self.selected_index
            )

            position = self.get_box_position(index)

            node.setPos(position)

            self.scene.addItem(node)

            self.items.append(node)

        self.scene.fit_with_margin(30)

    
    def create_floating_text(self, text_item):

        floating = self.scene.draw_text(
            text_item.toPlainText(),
            0,
            0,
            self.BOX_WIDTH - 20
        )

        floating.setPos(
            text_item.scenePos()
        )

        return floating

    def animate_text(self,floating,end_pos,finished=None):

        animation = {
            "item": floating,

            "start": floating.scenePos(),

            "end": end_pos,

            "elapsed": 0,

            "duration": 600,

            "finished": finished
        }

        self.animations.append(animation)

        if not self.timer.isActive():
            self.timer.start(16)


    def update_animation(self):

        if not self.animations:
            self.timer.stop()
            return

        finished = []

        for animation in self.animations:

            animation["elapsed"] += 16

            progress = (
                animation["elapsed"] /
                animation["duration"]
            )

            if progress >= 1:

                progress = 1

            start = animation["start"]
            end = animation["end"]

            x = start.x() + (end.x() - start.x()) * progress
            y = start.y() + (end.y() - start.y()) * progress

            animation["item"].setPos(x, y)

            if progress == 1:
                finished.append(animation)

        for animation in finished:

            callback = animation["finished"]

            self.animations.remove(animation)

            if callback:
                callback()

        if not self.animations:
            self.timer.stop()

    def animate_swap(self, first, second, finished=None):

            if self.animating:
                return

            self.animating = True

            self.swap_finished = finished

            self.animate_to_temp(
                first, second
            )

    def animate_b_to_a(self, first, second):

        first_node = self.items[first]
        second_node = self.items[second]

        floating = self.create_floating_text(
            second_node.text
        )

        second_node.hide_text()

        destination = first_node.get_text_scene_position()

        self.animate_text(
            floating,
            destination,
            finished=lambda:
                self.finish_b_to_a(
                    first_node,
                    second_node,
                    floating
                )
        )

    def finish_b_to_a(self, first_node, second_node, floating):

        first_node.set_title(
            second_node.song.title
        )

        first_node.show_text()

        self.scene.removeItem(floating)

        floating = self.create_floating_text(
            self.temp_text
        )

        self.temp_text.hide()

        destination = second_node.get_text_scene_position()

        self.animate_text(
            floating,
            destination,
            finished=lambda:
                self.finish_temp_to_b(
                    second_node,
                    floating
                )
        )

    def finish_temp_to_b(self, second_node, floating):

        second_node.set_title(
            self.temp_text.toPlainText()
        )
        
        second_node.show_text()

        self.scene.removeItem(floating)

        self.hide_temp()

        self.animating = False

        if self.swap_finished:
            self.swap_finished()
            self.swap_finished = None

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
    
    def get_temp_position(self,index):

        box = self.get_box_position(index)
    
        return QPointF(
            box.x(),
            box.y() - 170
        )

    def animate_to_temp(self, first, second):

        node = self.items[first]


        self.show_temp("", first)

        floating = self.create_floating_text(
            node.text
        )

        node.hide_text()

        temp = self.get_temp_position(first)

        rect = floating.boundingRect()

        destination = QPointF(
            temp.x() + (self.BOX_WIDTH - rect.width()) / 2,
            temp.y() + (self.BOX_HEIGHT - rect.height()) / 2
        )

        self.animate_text(
            floating,
            destination,
            finished=lambda: self.finish_a_to_temp(
            node,
            floating,
            first,
            second
        )
        )

    def finish_a_to_temp(self, node, floating, first, second):

        self.scene.removeItem(floating)

        self.show_temp(
            node.song.title, first
        )

        self.animate_b_to_a(
            first,
            second
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

    def show_temp(self, song_name, index):

        self.temp_text.setPlainText(song_name)

        temp = self.get_temp_position(index)

        self.temp_box.setPos(temp)

        self.temp_label.setPos(
            temp.x() + 45,
            temp.y() - 35
        )

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

    