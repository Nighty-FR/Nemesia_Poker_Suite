import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QSlider
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt

class NemesiaPokerSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Némésia Poker Suite")
        self.setFixedWidth(1000)
        self.setStyleSheet(self.load_stylesheet())
        self.selected_site = None
        self.selected_style = None

        # Styles par site et niveaux d'aide
        self.styles_by_site = {
            "Winamax": ["Heads Up", "5 Max", "6 Max", "9 Max", "Escape", "Tournoi"],
            "PokerStars": ["Heads Up", "5 Max", "6 Max", "9 Max", "Zoom", "Tournoi"],
            "Unibet": ["Heads Up", "5 Max", "6 Max", "9 Max", "Tournoi"]
        }
        self.aide_levels = ["Préflop Assisté", "GTO Avancée", "Autopilotage"]

        # Police personnalisée
        font_path = os.path.abspath("Trajan Pro Regular.ttf")
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0] if self.font_id != -1 else "Arial"

        self.initUI()

    def initUI(self):
        # Widget principal
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(20)

        # Titre
        self.title_label = QLabel("NÉMÉSIA POKER SUITE")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont(self.font_family, 36, QFont.Bold))
        self.title_label.setStyleSheet("color: #4ABFF7;")
        self.main_layout.addWidget(self.title_label)

        # Curseurs
        self.slider_container = QHBoxLayout()
        self.add_slider_section("Nombre de tables", ["1", "2", "4", "6"], "tables")
        self.add_slider_section("Niveau d'aide", self.aide_levels, "aide")

        self.main_layout.addLayout(self.slider_container)
        self.setCentralWidget(self.main_widget)

    def add_slider_section(self, label_text, values, slider_name):
        """Ajoute un curseur avec ses labels alignés."""
        container = QVBoxLayout()

        # Titre du curseur
        title_label = QLabel(label_text)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont(self.font_family, 12, QFont.Bold))
        title_label.setStyleSheet("color: #4ABFF7;")
        container.addWidget(title_label)

        # Curseur
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(len(values) - 1)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksAbove)
        slider.setStyleSheet(self.get_slider_style())
        slider.setFixedWidth(400)
        container.addWidget(slider)

        # Labels en dessous du curseur avec décalage
        labels_layout = QHBoxLayout()
        labels_layout.setContentsMargins(-10, 0, 0, 0)  # Décalage de 10px vers la gauche

        for value in values:
            lbl = QLabel(value)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont(self.font_family, 8))  # Taille de police réduite
            lbl.setStyleSheet("color: #4ABFF7;")
            labels_layout.addWidget(lbl)

        container.addLayout(labels_layout)
        self.slider_container.addLayout(container)

    def get_slider_style(self):
        """Style personnalisé pour les curseurs."""
        return """
            QSlider::groove:horizontal {
                background: #4ABFF7;
                height: 10px;
                border-radius: 5px;
            }
            QSlider::handle:horizontal {
                background: #4ABFF7;
                border: 2px solid #FFFFFF;
                width: 20px;
                height: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
        """

    def load_stylesheet(self):
        """Styles généraux pour la fenêtre."""
        return """
            QMainWindow {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1, 
                           stop:0 #101820, stop:1 #1B2838);
            }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NemesiaPokerSuite()
    window.show()
    sys.exit(app.exec_())
