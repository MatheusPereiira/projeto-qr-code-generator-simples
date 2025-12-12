from io import BytesIO
from typing import Optional
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.image.svg import SvgImage
from PIL import Image, ImageColor

class QRGenerator:
    def __init__(self, box_size=10, border=4, error_correction=ERROR_CORRECT_H):
        self.box_size = box_size
        self.border = border
        self.error_correction = error_correction

    def _normalize_color(self, color: Optional[str]) -> str:
        if not color:
            return "black"
        try:
            ImageColor.getrgb(color)
            return color
        except Exception:
            return "black"

    def generate(self, data, fill_color="black", back_color="white", fit=True):
        fill_color = self._normalize_color(fill_color)
        back_color = self._normalize_color(back_color)

        qr = qrcode.QRCode(
            version=None,
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=fit)

        return qr.make_image(fill_color=fill_color, back_color=back_color).convert("RGB")

    def generate_svg(self, data, fill_color="black", back_color="white"):
        qr = qrcode.QRCode(
            error_correction=self.error_correction,
            box_size=self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(image_factory=SvgImage, fill=fill_color, back_color=back_color)

        buf = BytesIO()
        img.save(buf)
        return buf.getvalue()
