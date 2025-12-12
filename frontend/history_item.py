from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from utils.image_utils import pil_image_to_qt_pixmap
from backend.qrgenerator import QRGenerator


class HistoryItem(QWidget):
    def __init__(self, entry, delete_callback, view_callback):
        super().__init__()

        self.entry = entry
        self.delete_callback = delete_callback
        self.view_callback = view_callback

        # Gerar miniatura
        generator = QRGenerator()
        img = generator.generate(entry["text"], entry["qr_color"], entry["bg_color"])
        pix = pil_image_to_qt_pixmap(img, max_size=70)

        qr_label = QLabel()
        qr_label.setPixmap(pix)
        qr_label.setFixedSize(80, 80)
        qr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Texto principal
        txt = QLabel(f"<b>{entry['text']}</b>")
        txt.setWordWrap(True)
        txt.setStyleSheet("font-size: 14px;")

        # Timestamp
        timestamp = QLabel(entry["timestamp"])
        timestamp.setStyleSheet("color: #666; font-size: 12px;")

        # NOVO TEXT_LAYOUT SEM BOLINHAS
        text_layout = QVBoxLayout()
        text_layout.addWidget(txt)
        text_layout.addWidget(timestamp)
        text_layout.setSpacing(5)

        # Botão "Ver"
        view_btn = QPushButton("Ver")
        view_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #2E86C1; }
        """)
        view_btn.clicked.connect(self.on_view_clicked)

        # Botão "Excluir"
        delete_btn = QPushButton("Excluir")
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                color: white;
                border-radius: 8px;
                padding: 8px;
                font-size: 13px;
            }
            QPushButton:hover { background-color: #C0392B; }
        """)
        delete_btn.clicked.connect(lambda: self.delete_callback(entry["id"]))

        # Layout final do card
        layout = QHBoxLayout()
        layout.addWidget(qr_label)
        layout.addLayout(text_layout)
        layout.addWidget(view_btn)
        layout.addWidget(delete_btn)
        layout.setSpacing(20)

        self.setLayout(layout)
        self.setMinimumHeight(110)

        self.setStyleSheet("""
            QWidget {
                background: white;
                border-radius: 10px;
                border: 1px solid #E0E0E0;
            }
        """)

    def on_view_clicked(self):
        self.view_callback(self.entry)
