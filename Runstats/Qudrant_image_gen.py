from PIL import Image
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtCore import QObject, Signal, Slot

class QudrantGridWorker(QObject):
    data_ready = Signal(object)
    """
    Creating a 65x65 image to represent 4 quadrants in the nether
    uses x and y in cartesian plane and px and py for the image
    py=32 and px=32 are reserved for divider lines
    """
    def __init__(self, size=65, divider_color=(180,180,180)):
        super().__init__()
        self.running = True
        self.size = size
        self.center = size // 2  # 32
        self.divider_color = divider_color

    @Slot()
    def stop(self):
        print("Stopping quadrant grid worker")
        self.running = False
    @Slot()
    def run(self):
        self.img = Image.new("RGB", (self.size, self.size))
        self.px = self.img.load()
        self.init_default_colors()
        self.data_ready.emit(self.to_qpixmap())
        self.save("grid.png")

    def render_scaled(self, zoom=20):
        large = self.img.resize((self.size * zoom, self.size * zoom), Image.NEAREST)
        return large


    def coord_to_pixel(self, x, y):
        if not (-32 <= x <= 32 and -32 <= y <= 32):
            raise ValueError("Coordinates must between -32..32.")
        px = x + self.center          # -32 -> 0, 32 -> 64
        py = self.center - y          # 32 -> 0, -32 -> 64
        return px, py

    def init_default_colors(self):
        for y in range(-32, 33):
            for x in range(-32, 33):
                px, py = self.coord_to_pixel(x, y)
                if x == 0 or y == 0:
                    self.px[px, py] = self.divider_color
                    continue
                if x < 0 and y > 0:      # Q2
                    color = (255,200,200)
                elif x > 0 and y > 0:    # Q1
                    color = (200,255,200)
                elif x < 0 and y < 0:    # Q3
                    color = (200,200,255)
                else:                    # Q4
                    color = (255,255,200)
                self.px[px, py] = color

    def set(self, x, y, color):
        if x == 0 or y == 0:
            raise ValueError("Cannot color divider axes (x=0 or y=0) — they are divider pixels.")
        px, py = self.coord_to_pixel(x, y)
        self.px[px, py] = color

    def get(self, x, y):
        px, py = self.coord_to_pixel(x, y)
        return self.px[px, py]

    def to_pil(self):
        return self.img

    def save(self, path):
        self.img.save(path)

    def to_qimage(self):
        big_img = self.render_scaled()
        data = big_img.tobytes("raw", "RGB")
        return QImage(
            data,
            big_img.width,
            big_img.height,
            QImage.Format.Format_RGB888
        )

    def to_qpixmap(self):
        return QPixmap.fromImage(self.to_qimage())

"""grid = Grid()

for y in range(-32,32):
    if y >= 0:
        y += 1
    grid.set(-15,y,(255,255,255))

# Save result
grid.save("grid.png")"""