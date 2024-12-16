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

        # Dictionnaire des styles de jeu par site
        self.styles_by_site = {
            "Winamax": ["Heads Up", "5 Max", "6 Max", "9 Max", "Escape", "Tournoi"],
            "PokerStars": ["Heads Up", "5 Max", "6 Max", "9 Max", "Zoom", "Tournoi"],
            "Unibet": ["Heads Up", "5 Max", "6 Max", "9 Max", "Tournoi"]
        }

        # Texte pour le niveau d'aide
        self.aide_levels = ["Préflop Assisté", "GTO Avancée", "Autopilotage"]

        # Charger la police personnalisée
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

        # SECTION : Choix des sites
        self.site_layout = QHBoxLayout()
        self.site_buttons = {}
        for site in ["Winamax", "PokerStars", "Unibet"]:
            btn = self.create_glow_button(site, small=True)
            btn.clicked.connect(lambda _, s=site: self.on_site_selected(s))
            self.site_buttons[site] = btn
            self.site_layout.addWidget(btn)

        # SECTION : Styles de jeu
        self.style_layout = QHBoxLayout()
        self.style_buttons = []

        # SECTION : Curseurs (Nombre de tables et Niveau d'aide)
        self.slider_container = QHBoxLayout()
        self.add_slider_section("Nombre de tables", ["1", "2", "4", "6"], adjust_cursor=True)
        self.add_slider_section("Niveau d'aide", self.aide_levels)

        # Ajout des widgets au layout principal
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.site_layout)
        self.main_layout.addLayout(self.style_layout)
        self.main_layout.addLayout(self.slider_container)
        self.setCentralWidget(self.main_widget)

    def add_slider_section(self, label_text, values, adjust_cursor=False):
        """Ajoute une section avec un curseur aligné."""
        container = QVBoxLayout()

        # Titre du curseur
        title_label = QLabel(label_text)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont(self.font_family, 12, QFont.Bold))
        title_label.setStyleSheet("color: #4ABFF7;")
        container.addWidget(title_label)

        # Curseur
        slider_layout = QHBoxLayout()
        if adjust_cursor:
            slider_layout.setContentsMargins(10, 0, 0, 0)  # Décalage de 10 pixels vers la droite

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(len(values) - 1)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksAbove)
        slider.setStyleSheet(self.get_slider_style())
        slider.setFixedWidth(400)
        slider_layout.addWidget(slider)
        container.addLayout(slider_layout)

        # Labels sous le curseur
        value_labels = QHBoxLayout()
        for value in values:
            lbl = QLabel(value)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont(self.font_family, 10))
            lbl.setStyleSheet("color: #4ABFF7;")
            lbl.setFixedWidth(100)
            value_labels.addWidget(lbl)

        container.addLayout(value_labels)
        self.slider_container.addLayout(container)

    def on_site_selected(self, site_name):
        """Affiche les styles de jeu en fonction du site sélectionné."""
        self.clear_style_buttons()
        self.selected_site = site_name
        for style in self.styles_by_site[site_name]:
            btn = self.create_glow_button(style, smaller=True)
            btn.clicked.connect(lambda _, s=style: self.on_style_selected(s))
            self.style_buttons.append(btn)
            self.style_layout.addWidget(btn)

    def on_style_selected(self, style_name):
        """Sélectionne un style de jeu."""
        self.selected_style = style_name

    def clear_style_buttons(self):
        """Supprime les styles existants."""
        for btn in self.style_buttons:
            btn.deleteLater()
        self.style_buttons = []

    def create_glow_button(self, text, small=False, smaller=False):
        """Crée un bouton stylisé."""
        button = QPushButton(text)
        button.setFixedSize(150, 50 if not smaller else 40)
        button.setStyleSheet("""
            QPushButton {
                background-color: #101820;
                color: #4ABFF7;
                border: 2px solid #4ABFF7;
                border-radius: 15px;
            }
            QPushButton:hover {
                background-color: #4ABFF7;
                color: #101820;
            }
        """)
        return button

    def get_slider_style(self):
        """Style du curseur."""
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
        """Style général."""
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
