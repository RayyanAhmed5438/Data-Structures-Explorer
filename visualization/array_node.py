from PyQt5.QtWidgets import (
    QGraphicsItemGroup,
    QGraphicsRectItem,
    QGraphicsTextItem
)

from PyQt5.QtGui import (
    QColor,
    QBrush,
    QPen,
    QFont,
    QFontMetrics
)

from PyQt5.QtCore import Qt


class ArrayNode(QGraphicsItemGroup):

    BOX_WIDTH = 140
    BOX_HEIGHT = 90

    def __init__(
        self,
        song,
        index,
        selected=False
    ):
        super().__init__()

        self.song = song
        self.index = index

        fill = QColor("#3E6AE1") if selected else QColor(55, 55, 55)

        self.box = QGraphicsRectItem(
            0,
            0,
            self.BOX_WIDTH,
            self.BOX_HEIGHT
        )

        self.box.setBrush(QBrush(fill))
        self.box.setPen(
            QPen(QColor(180, 180, 180), 2)
        )

        self.addToGroup(self.box)

        self.text = QGraphicsTextItem()

        font = QFont("Segoe UI", 11)
        font.setBold(True)

        metrics = QFontMetrics(font)

        self.text.setPlainText(
            metrics.elidedText(
                song.title,
                Qt.ElideRight,
                self.BOX_WIDTH - 20
            )
        )

        self.text.setFont(font)

        self.text.setDefaultTextColor(
            Qt.white
        )

        rect = self.text.boundingRect()

        self.text.setPos(
            (self.BOX_WIDTH - rect.width()) / 2,
            (self.BOX_HEIGHT - rect.height()) / 2
        )

        self.text.setToolTip(song.title)

        self.addToGroup(self.text)

        self.index_text = QGraphicsTextItem(
            str(index)
        )

        self.index_text.setFont(
            QFont("Segoe UI", 9)
        )

        self.index_text.setDefaultTextColor(
            QColor(170,170,170)
        )

        self.index_text.setPos(
            60,
            self.BOX_HEIGHT + 12
        )

        self.addToGroup(
            self.index_text
        )

    def hide_text(self):
        self.text.hide()

    def show_text(self):
        self.text.show()

    def get_text_scene_position(self):
        return self.text.scenePos()

    def set_title(self, title):

        print("SET TTITLE:", id(self.song), self.song.title, "->", title)

        font = self.text.font()

        metrics = QFontMetrics(font)

        display = metrics.elidedText(
            title,
            Qt.ElideRight,
            self.BOX_WIDTH - 20
        )

        self.text.setPlainText(display)

        rect = self.text.boundingRect()

        self.text.setPos(
            (self.BOX_WIDTH - rect.width()) / 2,
            (self.BOX_HEIGHT - rect.height()) / 2
        )

        self.text.setToolTip(title)


    def set_selected(self, selected):

        fill = QColor("#3E6AE1") if selected else QColor(55, 55, 55)

        self.box.setBrush(QBrush(fill))

    def fade_text(self):
            self.text.setOpacity(0)
    
    def restore_text(self):
        self.text.setOpacity(1)