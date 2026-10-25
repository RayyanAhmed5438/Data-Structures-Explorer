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

    @staticmethod
    def _wrap_title(title, metrics, max_width):
        """
        Wrap all title characters into lines without eliding any part.

        Ordinary titles wrap at spaces. A single long filename token is split
        into character chunks so it cannot extend beyond the CD label area.
        """
        words = str(title).split()
        if not words:
            return [""]

        lines = []
        current_line = ""

        for word in words:
            # Break an unusually long word into width-safe chunks first.
            if metrics.horizontalAdvance(word) > max_width:
                if current_line:
                    lines.append(current_line)
                    current_line = ""

                chunks = []
                chunk = ""

                for character in word:
                    candidate = chunk + character
                    if (
                        chunk
                        and metrics.horizontalAdvance(candidate) > max_width
                    ):
                        chunks.append(chunk)
                        chunk = character
                    else:
                        chunk = candidate

                if chunk:
                    chunks.append(chunk)

                # All complete chunks become their own lines; the final
                # chunk can still share a line with the next word.
                if len(chunks) > 1:
                    lines.extend(chunks[:-1])

                current_line = chunks[-1] if chunks else ""
                continue

            candidate = (
                f"{current_line} {word}"
                if current_line
                else word
            )

            if metrics.horizontalAdvance(candidate) <= max_width:
                current_line = candidate
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines or [""]

    def _draw_outlined_title(self, painter, diameter):
        # Use multiple lines and progressively smaller text when needed.
        # Nothing is elided: the complete song name is drawn on the CD.
        max_text_width = diameter * 0.72
        max_text_height = diameter * 0.62

        chosen_font = None
        chosen_metrics = None
        chosen_lines = None

        for point_size in range(11, 3, -1):
            font = QFont("Segoe UI", point_size, QFont.Bold)
            metrics = QFontMetricsF(font)
            lines = self._wrap_title(
                self._title,
                metrics,
                max_text_width
            )
            text_height = metrics.height() * len(lines)

            chosen_font = font
            chosen_metrics = metrics
            chosen_lines = lines

            if text_height <= max_text_height:
                break

        text_path = QPainterPath()
        line_height = chosen_metrics.height()

        for line_index, line in enumerate(chosen_lines):
            # addText expects a baseline position.
            baseline_y = (
                line_index * line_height
                + chosen_metrics.ascent()
            )
            text_path.addText(
                0.0,
                baseline_y,
                chosen_font,
                line
            )

        bounds = text_path.boundingRect()

        if bounds.isEmpty():
            return

        # Center the complete multi-line title on the disc.
        text_path.translate(
            (self.width() - bounds.width()) / 2.0 - bounds.left(),
            (self.height() - bounds.height()) / 2.0 - bounds.top()
        )

        # White fill with a yellow outline, as requested.
        outline_width = max(0.9, chosen_font.pointSizeF() * 0.13)
        outline = QPen(QColor("#FFD700"), outline_width)
        outline.setJoinStyle(Qt.RoundJoin)

        painter.setPen(outline)
        painter.setBrush(QColor("#F7F7F7"))
        painter.drawPath(text_path)
