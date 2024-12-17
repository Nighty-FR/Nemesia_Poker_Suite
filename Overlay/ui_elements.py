import os
import subprocess
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QMessageBox, QSpacerItem, QSizePolicy,
    QMenuBar, QMenu
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
        self.selected_site = "Winamax"
        self.selected_style = None
        self.font_family = self.load_font()

        self.styles_by_site = {
            "Winamax": ["Heads Up", "5 Max", "6 Max", "9 Max", "Escape", "Tournoi"],
            "PokerStars": ["Heads Up", "5 Max", "6 Max", "9 Max", "Zoom", "Tournoi"],
            "Unibet": ["Heads Up", "5 Max", "6 Max", "9 Max", "Tournoi"]
        }
        self.style_buttons = {}
        self.initUI()

    def load_font(self):
        font_path = os.path.abspath("Trajan Pro Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        return QFontDatabase.applicationFontFamilies(font_id)[0] if font_id != -1 else "Arial"

    def initUI(self):
        self.add_menu_bar()

        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(20)

        # Titre principal
        self.title_label = QLabel("NÉMÉSIA POKER SUITE")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont(self.font_family, 36, QFont.Bold))
        self.title_label.setStyleSheet("color: #4ABFF7;")
        self.main_layout.addWidget(self.title_label)

        # Boutons des sites
        self.site_layout = QHBoxLayout()
        self.site_buttons = {}
        for site in self.styles_by_site.keys():
            btn = self.create_button(site)
            btn.clicked.connect(lambda _, s=site: self.on_site_selected(s))
            self.site_buttons[site] = btn
            self.site_layout.addWidget(btn)
        self.main_layout.addLayout(self.site_layout)

        # Boutons des styles de jeu
        self.style_layout = QHBoxLayout()
        self.main_layout.addLayout(self.style_layout)

        # Curseurs
        self.slider_container = QHBoxLayout()
        self.add_slider_section("Nombre de tables", ["1", "2", "4", "6"], adjust_cursor=True)
        self.add_slider_section("Niveau d'aide", ["Préflop Assisté", "GTO Avancée", "Autopilotage"])
        self.main_layout.addLayout(self.slider_container)

        # Espacement
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addSpacerItem(spacer)

        # Boutons principaux
        self.add_main_buttons()

        # Sélection par défaut
        self.on_site_selected("Winamax")

        self.setCentralWidget(self.main_widget)

    def add_menu_bar(self):
        """Ajoute une barre de menu complète."""
        menu_bar = QMenuBar(self)

        # Menu File
        file_menu = menu_bar.addMenu("File")
        file_menu.addAction("Open", self.placeholder_action)
        file_menu.addAction("Exit", self.close)

        # Menu Edit
        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction("Preferences", self.placeholder_action)

        # Menu Connect
        connect_menu = menu_bar.addMenu("Connect")
        connect_menu.addAction("Connect to Server", self.placeholder_action)

        # Menu À propos
        about_menu = menu_bar.addMenu("À propos")
        about_menu.addAction("About", self.show_about)

        self.setMenuBar(menu_bar)

    def show_about(self):
        QMessageBox.about(self, "À propos", "Némésia Poker Suite\nVersion 1.0\n© 2024 Némésia. Tous droits réservés.")

    def placeholder_action(self):
        QMessageBox.information(self, "Action", "Cette action sera ajoutée prochainement.")

    def add_main_buttons(self):
        button_layout = QHBoxLayout()

        # Bouton Range Manager
        self.range_manager_button = QPushButton("Range Manager")
        self.range_manager_button.setStyleSheet(get_unselected_button_style())
        self.range_manager_button.setFixedSize(200, 50)
        self.range_manager_button.clicked.connect(self.launch_range_manager)
        button_layout.addWidget(self.range_manager_button, alignment=Qt.AlignLeft)

        # Lancer Overlay
        self.launch_overlay_button = QPushButton("Lancer Overlay")
        self.launch_overlay_button.setStyleSheet(get_selected_button_style())
        self.launch_overlay_button.setFixedSize(200, 50)
        self.launch_overlay_button.clicked.connect(self.launch_overlay)
        button_layout.addWidget(self.launch_overlay_button, alignment=Qt.AlignCenter)

        # Bouton Tracker
        self.tracker_button = QPushButton("Tracker")
        self.tracker_button.setStyleSheet(get_unselected_button_style())
        self.tracker_button.setFixedSize(200, 50)
        self.tracker_button.clicked.connect(self.launch_tracker)
        button_layout.addWidget(self.tracker_button, alignment=Qt.AlignRight)

        self.main_layout.addLayout(button_layout)

    def launch_overlay(self):
        """Ferme la fenêtre principale et lance overlay_table.py."""
        self.close()  # Ferme la fenêtre principale
        subprocess.Popen(["python", "overlay_table.py"])

    def launch_range_manager(self):
        try:
            executable_path = r"C:\Users\conta\Desktop\Némésia Poker Suite\NPS - Range Manager.exe"
            if os.path.exists(executable_path):
                subprocess.Popen(executable_path, shell=True)
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de trouver 'NPS - Range Manager.exe'.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Une erreur est survenue : {e}")

    def launch_tracker(self):
        QMessageBox.information(self, "Fonctionnalité à venir", "Cette fonctionnalité sera ajoutée prochainement.")

    def add_slider_section(self, label_text, values, adjust_cursor=False):
        container = QVBoxLayout()

        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont(self.font_family, 12, QFont.Bold))
        label.setStyleSheet("color: #4ABFF7;")
        container.addWidget(label)

        slider_layout = QHBoxLayout()
        if adjust_cursor and label_text == "Nombre de tables":
            slider_layout.setContentsMargins(5, 0, 0, 0)  # Décale de 5 pixels

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(len(values) - 1)
        slider.setStyleSheet(get_slider_style())
        slider.setFixedWidth(400)
        slider_layout.addWidget(slider)
        container.addLayout(slider_layout)

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
        self.selected_site = site_name
        for site, btn in self.site_buttons.items():
            btn.setStyleSheet(get_selected_button_style() if site == site_name else get_unselected_button_style())
        self.clear_style_buttons()
        for style in self.styles_by_site[site_name]:
            btn = self.create_button(style, smaller=True)
            btn.clicked.connect(lambda _, s=style: self.on_style_selected(s))
            self.style_buttons[style] = btn
            self.style_layout.addWidget(btn)

    def on_style_selected(self, style_name):
        self.selected_style = style_name
        for style, btn in self.style_buttons.items():
            btn.setStyleSheet(get_selected_button_style() if style == style_name else get_unselected_button_style())

    def clear_style_buttons(self):
        for btn in self.style_buttons.values():
            btn.deleteLater()
        self.style_buttons = {}

    def create_button(self, text, smaller=False):
        button = QPushButton(text)
        button.setFixedSize(150, 40 if smaller else 50)
        button.setStyleSheet(get_unselected_button_style())
        return button


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    window = NemesiaPokerSuite()
    window.show()
    sys.exit(app.exec_())
