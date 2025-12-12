from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from utils.image_utils import pil_image_to_qt_pixmap
from backend.qrgenerator import QRGenerator


class QRViewer(QWidget):
    def __init__(self, text, qr_color, bg_color):
        super().__init__()

        self.setWindowTitle("QR Code Ampliado")
        self.resize(450, 450)

        generator = QRGenerator()
        img = generator.generate(text, qr_color, bg_color)
        pix = pil_image_to_qt_pixmap(img, max_size=420)

        label = QLabel()
        label.setPixmap(pix)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)
