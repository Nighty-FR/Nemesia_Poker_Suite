import os
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt
from styles import load_stylesheet, get_slider_style, get_selected_button_style, get_unselected_button_style


class OverlayTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Némésia Poker Suite - Overlay Table")
        self.setFixedWidth(400)
        self.setStyleSheet(load_stylesheet())

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
        self.title_label = QLabel("OVERLAY TABLE")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont(self.font_family, 24, QFont.Bold))
        self.title_label.setStyleSheet("color: #4ABFF7;")
        self.main_layout.addWidget(self.title_label)

        # Curseur d'aide
        self.add_slider_section("Niveau d'aide", ["Préflop Assisté", "GTO Avancée", "Autopilotage"])

        # Boutons Play/Pause, Stop, Config
        self.add_control_buttons()

        # Espacement pour bien aligner les éléments
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addSpacerItem(spacer)

        self.setCentralWidget(self.main_widget)

    def add_control_buttons(self):
        """Ajoute les boutons Play/Pause, Stop et Config."""
        button_layout = QHBoxLayout()

        # Bouton Play/Pause
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet(get_selected_button_style())
        self.play_button.setFixedSize(100, 40)
        self.play_button.clicked.connect(self.toggle_play_pause)
        button_layout.addWidget(self.play_button)

        # Bouton Stop
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(get_unselected_button_style())
        self.stop_button.setFixedSize(100, 40)
        self.stop_button.clicked.connect(self.stop_overlay)
        button_layout.addWidget(self.stop_button)

        # Bouton Config
        self.config_button = QPushButton("Config")
        self.config_button.setStyleSheet(get_unselected_button_style())
        self.config_button.setFixedSize(100, 40)
        button_layout.addWidget(self.config_button)

        self.main_layout.addLayout(button_layout)

    def add_slider_section(self, label_text, values):
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
        slider.setFixedWidth(300)
        container.addWidget(slider)

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
        self.main_layout.addLayout(container)

    def toggle_play_pause(self):
        """Bascule entre Play et Pause."""
        if self.play_button.text() == "Play":
            self.play_button.setText("Pause")
            self.play_button.setStyleSheet(get_selected_button_style())
        else:
            self.play_button.setText("Play")
            self.play_button.setStyleSheet(get_unselected_button_style())

    def stop_overlay(self):
        """Ferme l'overlay."""
        self.close()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = OverlayTable()
    window.show()
    sys.exit(app.exec_())
