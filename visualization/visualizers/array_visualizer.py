from visualization.array_node import ArrayNode
from visualization.graphics_scene import GraphicsScene
from PyQt5.QtCore import Qt, QPointF, QTimer
from PyQt5.QtGui import QFontMetrics

class ArrayVisualizer:

    BOX_WIDTH = 140
    BOX_HEIGHT = 90
    START_X = 80
    START_Y = 150
    SPACING = 1

    def __init__(self, scene: GraphicsScene):
        self.scene = scene

        self.selected_index = -1

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

        # self.create_temp_box()
            
        for index, song in enumerate(array.get_all()):
            

            node = ArrayNode(
                song,
                index,
                index == self.selected_index
            )

            position = self.get_box_position(index)

            node.setPos(position)

            self.scene.addItem(node)

            self.items.append(node)

        self.update_scene_rect()
    
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

            if animation.get("opacity"):
                opacity = start + (end - start) * progress

                for item in animation["item"]:
                    item.setOpacity(opacity)

            else:

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

    # ======== SWAPPING FUNCTIONS ==================

    def animate_swap(self, first, second, finished=None):

            if self.animating:
                return

            self.create_temp_box()

            self.animating = True

            self.swap_finished = finished

            self.animate_to_temp(
                first, second
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

        self.animate_temp_fade(
            finished=self.finish_swap_animation
        )

    def finish_swap_animation(self):

        finished = self.swap_finished
        self.swap_finished = None

        self.finish_animation(finished)

    #==================================================

    #==============INSERTION FUNCTIONS================

    def add_empty_node(self):

        node = ArrayNode(
            None,
            len(self.items),
            empty=True
        )

        node.setPos(
            self.get_box_position(
                len(self.items)
            )
        )

        self.scene.addItem(node)
        self.items.append(node)

    def animate_insert(self, index, song_title, finished=None, started=None):

        if self.animating:
            return

        self.animating = True

        self.create_temp_box()

        self.add_empty_node()

        if started:
            started()

        self.show_temp(song_title, index)

        self.animate_shift_chain(
            insert_index=index,
            current_index=len(self.items) - 2,
            finished=lambda:
                self.animate_temp_to_array(
                    index,
                    finished
                )
        )

    def animate_temp_to_array(self, index, finished=None):

        self.items[index].hide_text()

        floating = self.create_floating_text(self.temp_text)
        self.temp_text.hide()

        destination = self.items[
            index
        ].get_text_scene_position()

        self.animate_text(
            floating,
            destination,
            finished=lambda:
                self.finish_insert(
                    index,
                    floating,
                    finished
                )
        )

    def finish_insert(self, index, floating, finished=None):

        destination = self.items[index]

        destination.set_title(floating.toPlainText())

        destination.show_text()

        self.scene.removeItem(floating)

        self.animate_temp_fade(
            finished=lambda:
                self.finish_animation(finished)
        )

    def animate_shift_chain(self, insert_index, current_index, finished=None):

        if current_index < insert_index:
            if finished:
                finished()
            return
        else:
            self.animate_shift(
                current_index,
                finished=lambda:
                self.animate_shift_chain(
                    insert_index,
                    current_index - 1,
                    finished
                )
            )

    def animate_shift(self, from_index, finished=None):

        node = self.items[from_index]

        floating = self.create_floating_text(node.text)

        node.hide_text()

       

        destination_node = self.items[from_index+1]

        self.animate_text(
            floating,
            destination_node.get_text_scene_position(),
            finished=lambda:
                self.finish_shift(
                    node,
                    destination_node,
                    floating,
                    finished
                )
        )

    def finish_shift(self, source_node,destination_node, floating, finished):

        destination_node.set_title(
            source_node.song.title
        )

        destination_node.show_text()

        self.scene.removeItem(floating)

        if finished:
            finished()

    #=============================================================

    #============= DELETION ANIMATION ===========================


    def animate_delete(self, index, finished=None):

        if self.animating:
            return

        self.animating = True

        self.create_temp_box()

        node = self.items[index]

        self.show_temp("", index)

        floating = self.create_floating_text(
            node.text
        )

        node.hide_text()

        temp = self.get_temp_position(index)

        rect = floating.boundingRect()

        destination = QPointF(
            temp.x() + (self.BOX_WIDTH - rect.width()) / 2,
            temp.y() + (self.BOX_HEIGHT - rect.height()) /2
        )


        self.animate_text(
            floating,
            destination,
            finished=lambda:    
                self.finish_delete_to_temp(
                    node,
                    floating,
                    index,
                    finished
                )
        )

    def finish_delete_to_temp(self, node, floating, index, finished=None):

        self.scene.removeItem(floating)

        self.show_temp(
            node.song.title, index
        )

        self.animate_shift_left_chain(
            current_index=index + 1,
            finished=lambda:
                self.finish_delete(finished)
        )

    def animate_shift_left(self, from_index, finished=None):
    
        node = self.items[from_index]

        destination_node = self.items[from_index - 1]
    
        floating = self.create_floating_text(node.text)
    
        node.hide_text()
              
        self.animate_text(
            floating,
            destination_node.get_text_scene_position(),
            finished=lambda:
                self.finish_shift(  # reused from insertion
                    node,
                    destination_node,
                    floating,
                    finished
                )
        )

    def animate_shift_left_chain(self, current_index, finished=None):

        if current_index >= len(self.items):
            if finished:
                finished()
            return

        self.animate_shift_left(
            current_index,
            finished=lambda:
                self.animate_shift_left_chain(
                    current_index + 1,
                    finished
                )
        )

    def finish_delete(self, finished=None):

        last = self.items.pop()

        self.scene.removeItem(last)

        self.animate_temp_fade(
            finished=lambda:
                self.finish_animation(
                    finished
                )
        )

    #===========================================================

    def animate_temp_fade(self, finished=None):
    
        animation = {
            "item" : [
                self.temp_box,
                self.temp_text,
                self.temp_label
            ],

            "start": 1.0,

            "end": 0.0,

            "elapsed": 0,

            "duration": 250,

            "finished": finished,

            "opacity": True
        }

        self.animations.append(animation)

        if not self.timer.isActive():
            self.timer.start(16)

    def finish_animation(self, finished=None):
    
        self.remove_temp()

        self.update_scene_rect()

        self.animating = False

        if finished:
                finished()

    def update_scene_rect(self):

        rect = self.scene.itemsBoundingRect()

        rect.adjust(
            -80, -10, self.BOX_WIDTH + 80, 10
        )

        self.scene.setSceneRect(rect)

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
            box.y() - 130
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

    def show_temp(self, song_name, index):

        metrics = QFontMetrics(self.temp_text.font())

        display = metrics.elidedText(
            song_name,
            Qt.ElideRight,
            self.BOX_WIDTH - 20
        )

        self.temp_text.setPlainText(display)

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

        self.temp_text.setToolTip(song_name)

        self.temp_box.show()
        self.temp_text.show()
        self.temp_label.show()

    def remove_temp(self):

        self.scene.removeItem(self.temp_box)
        self.scene.removeItem(self.temp_text)
        self.scene.removeItem(self.temp_label)

        self.temp_box = None
        self.temp_text = None
        self.temp_label = None

    def set_selected_index(self, index):

        self.selected_index = index

        self._redraw()

    def _redraw(self):
        if self.current_array is not None:
            self.visualize(self.current_array)

    def get_item_count(self):
        return len(self.items)