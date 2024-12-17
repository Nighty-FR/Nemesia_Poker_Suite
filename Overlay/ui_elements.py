import os
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QMessageBox
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from styles import load_stylesheet, get_slider_style, get_selected_button_style, get_unselected_button_style


class NemesiaPokerSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Némésia Poker Suite")
        self.setFixedWidth(1000)
        self.setStyleSheet(load_stylesheet())
        self.selected_site = None
        self.selected_style = None

        # Styles par site
        self.styles_by_site = {
            "Winamax": ["Heads Up", "5 Max", "6 Max", "9 Max", "Escape", "Tournoi"],
            "PokerStars": ["Heads Up", "5 Max", "6 Max", "9 Max", "Zoom", "Tournoi"],
            "Unibet": ["Heads Up", "5 Max", "6 Max", "9 Max", "Tournoi"]
        }

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

        # Sites
        self.site_layout = QHBoxLayout()
        self.site_buttons = {}
        for site in ["Winamax", "PokerStars", "Unibet"]:
            btn = self.create_button(site)
            btn.clicked.connect(lambda _, s=site: self.on_site_selected(s))
            self.site_buttons[site] = btn
            self.site_layout.addWidget(btn)
        self.main_layout.addLayout(self.site_layout)

        # Styles de jeu
        self.style_layout = QHBoxLayout()
        self.style_buttons = {}
        self.main_layout.addLayout(self.style_layout)

        # Curseurs
        self.slider_container = QHBoxLayout()
        self.add_slider_section("Nombre de tables", ["1", "2", "4", "6"], adjust_cursor=True)
        self.add_slider_section("Niveau d'aide", ["Préflop Assisté", "GTO Avancée", "Autopilotage"])
        self.main_layout.addLayout(self.slider_container)

        # Boutons principaux
        self.add_main_buttons()

        self.setCentralWidget(self.main_widget)

    def add_main_buttons(self):
        """Ajoute les boutons principaux en bas de l'interface."""
        button_layout = QHBoxLayout()

        # Espacement fixe entre les boutons
        button_spacing = 25

        # Bouton "Range Manager"
        self.range_manager_button = QPushButton("Range Manager")
        self.range_manager_button.setStyleSheet(get_unselected_button_style())
        self.range_manager_button.setFixedSize(200, 50)
        self.range_manager_button.clicked.connect(self.launch_range_manager)
        button_layout.addWidget(self.range_manager_button, alignment=Qt.AlignLeft)
        button_layout.addSpacing(button_spacing)  # Espacement entre Range Manager et Overlay

        # Espace flexible pour centrer le bouton "Lancer l'Overlay"
        button_layout.addStretch(1)
        self.launch_overlay_button = QPushButton("Lancer l'Overlay")
        self.launch_overlay_button.setStyleSheet(get_selected_button_style())
        self.launch_overlay_button.setFixedSize(200, 50)
        self.launch_overlay_button.clicked.connect(self.launch_overlay)
        button_layout.addWidget(self.launch_overlay_button, alignment=Qt.AlignCenter)
        button_layout.addStretch(1)

        # Espacement fixe entre Overlay et Tracker
        button_layout.addSpacing(button_spacing)
        self.tracker_button = QPushButton("Tracker")
        self.tracker_button.setStyleSheet(get_unselected_button_style())
        self.tracker_button.setFixedSize(200, 50)
        self.tracker_button.clicked.connect(self.launch_tracker)
        button_layout.addWidget(self.tracker_button, alignment=Qt.AlignRight)

        self.main_layout.addLayout(button_layout)

    def launch_overlay(self):
        """Action pour le bouton Lancer Overlay."""
        QMessageBox.information(self, "Lancer Overlay", "L'Overlay sera ajouté ici dans une future mise à jour.")

    def launch_range_manager(self):
        """Action pour le bouton Range Manager."""
        QMessageBox.information(self, "Range Manager", "Lancement du Range Manager...")

    def launch_tracker(self):
        """Action pour le bouton Tracker."""
        QMessageBox.information(self, "Tracker", "Lancement du Tracker...")

    def add_slider_section(self, label_text, values, adjust_cursor=False):
        """Ajoute une section avec un curseur."""
        container = QVBoxLayout()

        # Titre
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont(self.font_family, 12, QFont.Bold))
        label.setStyleSheet("color: #4ABFF7;")
        container.addWidget(label)

        # Curseur
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(len(values) - 1)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.TicksAbove)
        slider.setStyleSheet(get_slider_style())
        slider.setFixedWidth(400)

        # Décalage
        slider_layout = QHBoxLayout()
        if adjust_cursor:
            slider_layout.setContentsMargins(10, 0, 0, 0)
        slider_layout.addWidget(slider)
        container.addLayout(slider_layout)

        # Labels sous le curseur
        value_labels = QHBoxLayout()
        for value in values:
            lbl = QLabel(value)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont(self.font_family, 8))
            lbl.setStyleSheet("color: #4ABFF7;")
            lbl.setFixedWidth(100)
            value_labels.addWidget(lbl)

        container.addLayout(value_labels)
        self.slider_container.addLayout(container)

    def on_site_selected(self, site_name):
        """Met en surbrillance le site sélectionné et affiche les styles correspondants."""
        self.selected_site = site_name

        # Mettre à jour le style des boutons de sites
        for site, btn in self.site_buttons.items():
            btn.setStyleSheet(get_selected_button_style() if site == site_name else get_unselected_button_style())

        # Mettre à jour les styles de jeu
        self.clear_style_buttons()
        for style in self.styles_by_site[site_name]:
            btn = self.create_button(style, smaller=True)
            btn.clicked.connect(lambda _, s=style: self.on_style_selected(s))
            self.style_buttons[style] = btn
            self.style_layout.addWidget(btn)

    def on_style_selected(self, style_name):
        """Met en surbrillance le style sélectionné."""
        self.selected_style = style_name
        for style, btn in self.style_buttons.items():
            btn.setStyleSheet(get_selected_button_style() if style == style_name else get_unselected_button_style())

    def clear_style_buttons(self):
        """Supprime les styles de jeu affichés."""
        for btn in self.style_buttons.values():
            btn.deleteLater()
        self.style_buttons = {}

    def create_button(self, text, smaller=False):
        """Crée un bouton stylisé."""
        button = QPushButton(text)
        button.setFixedSize(150, 40 if smaller else 50)
        button.setStyleSheet(get_unselected_button_style())
        return button
