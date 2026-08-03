from PyQt5.QtWidgets import (
    QGraphicsScene,
    QGraphicsRectItem,
    QGraphicsTextItem,
    QGraphicsLineItem
)

from PyQt5.QtGui import QColor, QBrush, QFontMetrics, QPen, QFont
from PyQt5.QtCore import Qt


class GraphicsScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)

        

        self.items_map = {}

    def draw_box(self, x, y, width, height,
                  fill_color = QColor(55, 55, 55), 
                  border_color = QColor(180, 180, 180)
    ):

        rect = self.addRect(
            x, y, width, height,
            QPen(border_color, 2),
            QBrush(fill_color)
        )

        return rect

    def draw_text(self, text, x, y, max_width=None):
        font = QFont("Segoe UI", 11)
        font.setBold(True)

        if max_width is not None:
            metrics = QFontMetrics(font)
            text = metrics.elidedText(
                text,
                Qt.ElideRight,
                max_width
            )

        text_item = self.addText(text)

        text_item.setDefaultTextColor(Qt.white)
        text_item.setFont(font)
        text_item.setPos(x, y)

        return text_item

    def clear_scene(self):
        self.clear()
        self.items_map.clear()

    def draw_line(self, x1, y1, x2, y2):

        line = self.addLine(
            x1, y1, x2, y2, QPen(Qt.white)
        )

        return line

    def animate_move(self):
        pass

    def animate_insert(self):
        pass

    def animate_delete(self):
        pass

    def animate_highlight(self):
        pass

    def fit_with_margin(self, margin):
        
        rect = self.itemsBoundingRect()

        self.setSceneRect(
            rect.left() - margin,
            rect.top() - margin,
            rect.width() + margin * 2,
            rect.height() + margin * 2
        )