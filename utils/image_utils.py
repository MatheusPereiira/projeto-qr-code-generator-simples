from io import BytesIO
from PIL import Image

def pil_image_to_qt_pixmap(pil_img, max_size=300):
    from PyQt6.QtGui import QPixmap
    from PyQt6.QtCore import Qt
    buf=BytesIO()
    pil_img.save(buf, format="PNG")
    data=buf.getvalue()
    pix=QPixmap()
    pix.loadFromData(data)
    if max_size:
        pix=pix.scaled(max_size, max_size, Qt.AspectRatioMode.KeepAspectRatio)
    return pix
