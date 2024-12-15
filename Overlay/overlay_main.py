import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget,
    QPushButton, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor, QFontDatabase
from PyQt5.QtCore import Qt

class NemesiaPokerSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Némésia Poker Suite")
        self.setFixedWidth(1000)  # Fixe la largeur à 1000px
        self.setStyleSheet(self.load_stylesheet())
        self.selected_site = None

        # Dictionnaire des styles de jeu par site
        self.styles_by_site = {
            "Winamax": ["Heads Up", "5 Max", "6 Max", "9 Max", "Escape", "Tournoi"],
            "PokerStars": ["Heads Up", "5 Max", "6 Max", "9 Max", "Zoom", "Tournoi"],
            "Unibet": ["Heads Up", "5 Max", "6 Max", "9 Max", "Tournoi"]
        }

        # Charger la police personnalisée
        font_path = os.path.abspath("Trajan Pro Regular.ttf")
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        if self.font_id == -1:
            print("Erreur : Impossible de charger la police. Utilisation de la police par défaut.")
            self.font_family = "Times"
        else:
            self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0]
            print(f"Police chargée avec succès : {self.font_family}")

        self.initUI()

    def initUI(self):
        # Widget principal
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(20)

        # Appliquer une transparence de 20% à la fenêtre
        self.setWindowOpacity(0.8)

        # Titre
        self.title_label = QLabel("NÉMÉSIA POKER SUITE")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont(self.font_family, 36, QFont.Bold))
        self.title_label.setObjectName("neonTitle")

        # SECTION : Choix des sites
        self.site_layout = QHBoxLayout()
        self.site_buttons = {}
        for site in ["Winamax", "PokerStars", "Unibet"]:
            btn = self.create_glow_button(site, small=True)
            btn.clicked.connect(lambda _, s=site: self.on_site_selected(s))
            self.site_buttons[site] = btn
            self.site_layout.addWidget(btn)

        # SECTION : Styles de jeu (initialement cachée)
        self.style_layout = QHBoxLayout()
        self.style_buttons = []

        # Ajout des sections au layout principal
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.site_layout)
        self.main_layout.addLayout(self.style_layout)
        self.setCentralWidget(self.main_widget)

    def on_site_selected(self, site_name):
        """Action lorsqu'un site est sélectionné ou désélectionné."""
        if self.selected_site == site_name:  # Désélectionner le site
            self.selected_site = None
            for btn in self.site_buttons.values():
                btn.setStyleSheet(self.get_unselected_button_style())
            self.clear_style_buttons()
        else:  # Sélectionner un site
            self.selected_site = site_name
            for site, btn in self.site_buttons.items():
                if site == site_name:
                    btn.setStyleSheet(self.get_selected_button_style())
                else:
                    btn.setStyleSheet(self.get_unselected_button_style())
            self.update_style_buttons(site_name)

    def update_style_buttons(self, site_name):
        """Mettre à jour les boutons des styles de jeu."""
        self.clear_style_buttons()
        for style in self.styles_by_site[site_name]:
            btn = self.create_glow_button(style, smaller=True)
            self.style_buttons.append(btn)
            self.style_layout.addWidget(btn)

    def clear_style_buttons(self):
        """Supprimer les boutons des styles de jeu."""
        for btn in self.style_buttons:
            btn.deleteLater()
        self.style_buttons = []

    def create_glow_button(self, text, small=False, smaller=False):
        """Créer un bouton lumineux."""
        button = QPushButton(text)
        button.setObjectName("glowButton")
        button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        button.setFixedSize(150, 50 if small else (40 if smaller else 60))
        button.setFont(QFont("Arial", 12 if small else 10, QFont.Bold))
        button.setStyleSheet(self.get_unselected_button_style())
        return button

    def get_selected_button_style(self):
        """Style pour le bouton sélectionné."""
        return """
            QPushButton {
                background-color: #4ABFF7;
                color: #101820;
                border: 2px solid #FFFFFF;
                border-radius: 15px;
                font-weight: bold;
            }
        """

    def get_unselected_button_style(self):
        """Style pour les boutons non sélectionnés."""
        return """
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
        """

    def load_stylesheet(self):
        """Styles CSS."""
        return """
            QMainWindow {
                background: qradialgradient(cx:0.5, cy:0.5, radius:1, 
                           stop:0 #101820, stop:1 #1B2838);
            }
            QLabel#neonTitle {
                color: #4ABFF7;
                font-size: 40px;
                letter-spacing: 2px;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NemesiaPokerSuite()
    window.show()
    sys.exit(app.exec_())
