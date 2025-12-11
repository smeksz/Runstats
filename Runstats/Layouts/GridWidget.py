from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QImage
from PySide6.QtCore import Qt


class GridWidget(QWidget):
    def __init__(self, grid, parent=None):
        super().__init__(parent)
        self.grid = grid

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform, False)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        qimg = self.grid.to_qimage()

        # Determine square size to maintain aspect ratio
        w = self.width()
        h = self.height()
        side = min(w, h)  # keep it perfectly square

        # Center the square inside the widget
        x = (w - side) // 2
        y = (h - side) // 2

        painter.drawImage(
            Qt.Rect(x, y, side, side),
            qimg
        )
