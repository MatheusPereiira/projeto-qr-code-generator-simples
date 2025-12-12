import sys
from PyQt6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QColorDialog, QVBoxLayout,
    QHBoxLayout, QFileDialog, QMessageBox, QFrame, QTabWidget, QListWidget,
    QListWidgetItem
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from backend.qrgenerator import QRGenerator
from backend.database import JSONDatabase
from utils.image_utils import pil_image_to_qt_pixmap
from frontend.viewer import QRViewer


class QRAppUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QR Code Generator")
        self.resize(520, 720)

        self.generator = QRGenerator()
        self.db = JSONDatabase()

        # Mantém janelas abertas
        self.viewer_windows = []

        self.qr_color = "#000000"
        self.bg_color = "#ffffff"
        self.current_img = None

        self.tabs = QTabWidget()
        self.tab_generate = QWidget()
        self.tab_history = QWidget()

        self.tabs.addTab(self.tab_generate, "Gerar QR")
        self.tabs.addTab(self.tab_history, "Histórico")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

        self.build_tab_generate()
        self.build_tab_history()
        self.apply_styles()

    # --------------------------------------------------------------
    # TAB GERAR QR
    # --------------------------------------------------------------
    def build_tab_generate(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Gerador de QR Code")
        title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # =======================================================
        # 🔥 AQUI ESTÁ A ALTERAÇÃO QUE VOCÊ PEDIU 🔥
        # Campo "Digite o link ou texto..." com MESMO estilo da busca
        # =======================================================
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Digite o link ou texto...")
        self.url_input.setFixedHeight(40)
        self.url_input.setStyleSheet("""
            QLineEdit {
                padding-left: 12px;
                font-size: 15px;
                border-radius: 8px;
                border: 1px solid #CCC;
                background:white;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
        """)

        # BOTÕES DE COR
        color_buttons = QHBoxLayout()
        self.btn_qr_color = QPushButton("Cor do QR")
        self.btn_bg_color = QPushButton("Cor do fundo")
        color_buttons.addWidget(self.btn_qr_color)
        color_buttons.addWidget(self.btn_bg_color)

        self.btn_generate = QPushButton("Gerar QR")
        self.btn_generate.setFixedHeight(40)

        # PREVIEW
        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview.setFixedSize(340, 340)

        frame = QFrame()
        frame.setFixedSize(360, 360)
        frame.setStyleSheet("background: white; border-radius: 12px; border: 1px solid #CCC;")

        f_layout = QVBoxLayout()
        f_layout.addWidget(self.preview)
        frame.setLayout(f_layout)

        # BOTÕES DE SALVAR
        self.btn_save_png = QPushButton("Salvar PNG")
        self.btn_save_svg = QPushButton("Salvar SVG")

        layout.addWidget(title)
        layout.addWidget(self.url_input)
        layout.addLayout(color_buttons)
        layout.addWidget(self.btn_generate)
        layout.addWidget(frame, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.btn_save_png)
        layout.addWidget(self.btn_save_svg)

        self.tab_generate.setLayout(layout)

        # EVENTOS
        self.btn_qr_color.clicked.connect(self.choose_qr_color)
        self.btn_bg_color.clicked.connect(self.choose_bg_color)
        self.btn_generate.clicked.connect(self.on_generate)
        self.btn_save_png.clicked.connect(self.on_save_png)
        self.btn_save_svg.clicked.connect(self.on_save_svg)

    # --------------------------------------------------------------
    # TAB HISTÓRICO
    # --------------------------------------------------------------
    def build_tab_history(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Histórico de QR Codes")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por texto ou link...")
        self.search_input.setFixedHeight(35)
        self.search_input.setStyleSheet("""
            QLineEdit {
                padding-left: 12px;
                font-size: 15px;
                border-radius: 8px;
                border: 1px solid #CCC;
                background:white;
            }
            QLineEdit:focus {
                border: 1px solid #4A90E2;
            }
        """)
        self.search_input.textChanged.connect(self.filter_history)

        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                background: #F0F0F0;
                border: none;
                padding: 10px;
            }
        """)

        layout.addWidget(title)
        layout.addWidget(self.search_input)
        layout.addWidget(self.history_list)

        self.tab_history.setLayout(layout)

        self.load_history_items()

    # --------------------------------------------------------------
    # HISTÓRICO
    # --------------------------------------------------------------
    def add_history_card(self, entry):
        from frontend.history_item import HistoryItem

        item_widget = HistoryItem(
            entry,
            delete_callback=self.delete_entry,
            view_callback=self.open_viewer
        )

        list_item = QListWidgetItem(self.history_list)
        list_item.setSizeHint(item_widget.sizeHint())

        self.history_list.addItem(list_item)
        self.history_list.setItemWidget(list_item, item_widget)

    def load_history_items(self):
        self.history_list.clear()
        history = self.db.load()["history"]

        for entry in history:
            self.add_history_card(entry)

    def filter_history(self):
        text = self.search_input.text().lower()
        self.history_list.clear()

        for entry in self.db.load()["history"]:
            if text in entry["text"].lower():
                self.add_history_card(entry)

    def delete_entry(self, entry_id):
        self.db.delete_entry(entry_id)
        self.load_history_items()
        QMessageBox.information(self, "Excluído", "Item removido!")

    # --------------------------------------------------------------
    # VIEWER
    # --------------------------------------------------------------
    def open_viewer(self, entry):
        viewer = QRViewer(
            entry["text"],
            entry["qr_color"],
            entry["bg_color"]
        )
        self.viewer_windows.append(viewer)
        viewer.show()
        viewer.raise_()

    # --------------------------------------------------------------
    # FUNÇÕES DO QR
    # --------------------------------------------------------------
    def choose_qr_color(self):
        c = QColorDialog.getColor()
        if c.isValid():
            self.qr_color = c.name()

    def choose_bg_color(self):
        c = QColorDialog.getColor()
        if c.isValid():
            self.bg_color = c.name()

    def on_generate(self):
        data = self.url_input.text().strip()
        if not data:
            QMessageBox.warning(self, "Erro", "Digite um texto válido.")
            return

        self.current_img = self.generator.generate(data, self.qr_color, self.bg_color)
        pix = pil_image_to_qt_pixmap(self.current_img, 330)
        self.preview.setPixmap(pix)

        self.db.add_entry(data, self.qr_color, self.bg_color)
        self.load_history_items()

    def on_save_png(self):
        if self.current_img is None:
            QMessageBox.warning(self, "Erro", "Gere um QR antes.")
            return

        path, _ = QFileDialog.getSaveFileName(self, "Salvar PNG", "qrcode.png", "PNG (*.png)")
        if path:
            self.current_img.save(path)

    def on_save_svg(self):
        text = self.url_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Erro", "Gere um QR antes!")
            return

        svg_bytes = self.generator.generate_svg(text, self.qr_color, self.bg_color)
        path, _ = QFileDialog.getSaveFileName(self, "Salvar SVG", "qrcode.svg", "SVG (*.svg)")

        if path:
            with open(path, "wb") as f:
                f.write(svg_bytes)

    # --------------------------------------------------------------
    def apply_styles(self):
        self.setStyleSheet("""
            QWidget { background-color: #F5F5F5; }
            QPushButton {
                background-color: #4A90E2;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 16px;
            }
            QPushButton:hover { background-color: #357ABD; }
        """)
