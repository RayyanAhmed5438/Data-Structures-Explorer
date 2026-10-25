from pathlib import Path

from PyQt5.QtCore import Qt, QTimer, QRectF
from PyQt5.QtGui import (
    QColor,
    QFont,
    QFontMetricsF,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QRadialGradient
)
from PyQt5.QtWidgets import QWidget


class SpinningCDWidget(QWidget):
    """Draws a rotating CD image with the current song title over its center."""

    DIAMETER = 180
    TIMER_INTERVAL_MS = 30
    ROTATION_STEP_DEGREES = 2.0

    def __init__(self, assets_dir, parent=None):
        super().__init__(parent)

        self.assets_dir = Path(assets_dir)
        self._title = "No Song Playing"
        self._angle = 0.0
        self._spinning = False

        self._pixmap = self._load_cd_image()

        self._rotation_timer = QTimer(self)
        self._rotation_timer.setInterval(self.TIMER_INTERVAL_MS)
        self._rotation_timer.timeout.connect(self._advance_rotation)

        self.setFixedSize(self.DIAMETER, self.DIAMETER)
        self.setAccessibleName("Spinning CD")
        self.setToolTip(self._title)

    def _load_cd_image(self):
        """Find a file named CD regardless of extension or letter casing."""
        try:
            candidates = sorted(
                (
                    path for path in self.assets_dir.iterdir()
                    if path.is_file() and path.stem.casefold() == "cd"
                ),
                key=lambda path: path.name.casefold()
            )
        except OSError:
            candidates = []

        for path in candidates:
            pixmap = QPixmap(str(path))
            if not pixmap.isNull():
                return pixmap

        # The widget has a drawn-disc fallback if the image is not present.
        return QPixmap()

    def setText(self, title):
        """Keep a QLabel-like setter so existing panel code stays compatible."""
        self._title = str(title) if title else "No Song Playing"
        self.setToolTip(self._title)
        self.update()

    def set_spinning(self, spinning):
        self._spinning = bool(spinning)

        if self._spinning:
            if not self._rotation_timer.isActive():
                self._rotation_timer.start()
        else:
            self._rotation_timer.stop()

    def _advance_rotation(self):
        self._angle = (
            self._angle + self.ROTATION_STEP_DEGREES
        ) % 360.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        center_x = self.width() / 2.0
        center_y = self.height() / 2.0
        diameter = min(self.width(), self.height()) - 8.0

        # Rotate only the CD artwork. The title is drawn afterwards so it stays
        # level and readable while the disc turns beneath it.
        painter.save()
        painter.translate(center_x, center_y)
        painter.rotate(self._angle)

        disc_rect = QRectF(
            -diameter / 2.0,
            -diameter / 2.0,
            diameter,
            diameter
        )

        if not self._pixmap.isNull():
            painter.drawPixmap(
                disc_rect,
                self._pixmap,
                QRectF(self._pixmap.rect())
            )
        else:
            self._draw_fallback_disc(painter, diameter)

        painter.restore()

        self._draw_outlined_title(painter, diameter)

    def _draw_fallback_disc(self, painter, diameter):
        """Render a simple silver CD if the local artwork has not been copied."""
        radius = diameter / 2.0

        gradient = QRadialGradient(0.0, 0.0, radius)
        gradient.setColorAt(0.0, QColor("#F1F2F3"))
        gradient.setColorAt(0.28, QColor("#AEB3BA"))
        gradient.setColorAt(0.55, QColor("#E0E2E5"))
        gradient.setColorAt(0.78, QColor("#8C929A"))
        gradient.setColorAt(1.0, QColor("#D5D8DD"))

        painter.setPen(QPen(QColor("#737982"), 1.2))
        painter.setBrush(gradient)
        painter.drawEllipse(QRectF(-radius, -radius, diameter, diameter))

        painter.setBrush(Qt.NoBrush)
        for fraction in (0.35, 0.55, 0.72, 0.9):
            ring_radius = radius * fraction
            painter.setPen(QPen(QColor(90, 96, 104, 110), 1.0))
            painter.drawEllipse(
                QRectF(
                    -ring_radius,
                    -ring_radius,
                    ring_radius * 2,
                    ring_radius * 2
                )
            )

        hole_radius = radius * 0.105
        painter.setPen(QPen(QColor("#6D737B"), 1.0))
        painter.setBrush(QColor("#2D2F34"))
        painter.drawEllipse(
            QRectF(
                -hole_radius,
                -hole_radius,
                hole_radius * 2,
                hole_radius * 2
            )
        )

    def _draw_outlined_title(self, painter, diameter):
        font = QFont("Segoe UI", 10, QFont.Bold)
        metrics = QFontMetricsF(font)

        # Keep the title inside the inner label area and elide long names.
        max_text_width = diameter * 0.68
        display_title = metrics.elidedText(
            self._title,
            Qt.ElideMiddle,
            max_text_width
        )

        text_path = QPainterPath()
        text_path.addText(0.0, 0.0, font, display_title)
        bounds = text_path.boundingRect()

        text_path.translate(
            (self.width() - bounds.width()) / 2.0 - bounds.left(),
            (self.height() - bounds.height()) / 2.0 - bounds.top()
        )

        # White fill with a grey stroke creates the requested outlined text.
        outline = QPen(QColor("#777D85"), 1.6)
        outline.setJoinStyle(Qt.RoundJoin)

        painter.setPen(outline)
        painter.setBrush(QColor("#F7F7F7"))
        painter.drawPath(text_path)
