import os
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPoint
from styles import get_selected_button_style, get_unselected_button_style


class OverlayTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Némésia Poker Suite - Overlay Table")
        self.setFixedWidth(450)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Fenêtre sans bordure
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Police personnalisée
        font_path = os.path.abspath("Trajan Pro Regular.ttf")
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0] if self.font_id != -1 else "Arial"

        # Déplacement avec clic droit
        self.old_pos = None

        self.initUI()

    def initUI(self):
        # Fond principal
        self.main_widget = QWidget(self)
        self.main_widget.setStyleSheet("""
            QWidget {
                background-color: #1B2838;   /* Fond bleu foncé */
                border: 3px solid #101820;   /* Bordure sombre */
                border-radius: 15px;
            }
        """)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setSpacing(20)

        # Titre
        self.title_label = QLabel("NÉMÉSIA POKER SUITE")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont(self.font_family, 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #4ABFF7; border: none;")
        self.main_layout.addWidget(self.title_label)

        # Curseur d'aide
        self.add_slider_section("Niveau d'aide", ["Préflop Assisté", "GTO Avancée", "Autopilotage"])

        # Boutons Play/Pause, Stop, Config
        self.add_control_buttons()

        # Espacement
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.main_layout.addSpacerItem(spacer)

        self.setCentralWidget(self.main_widget)

    def add_control_buttons(self):
        button_layout = QHBoxLayout()

        # Play
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet(get_selected_button_style())
        self.play_button.setFixedSize(100, 40)
        self.play_button.clicked.connect(self.toggle_play_pause)
        button_layout.addWidget(self.play_button)

        # Stop
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(get_unselected_button_style())
        self.stop_button.setFixedSize(100, 40)
        button_layout.addWidget(self.stop_button)

        # Config
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
        label.setFont(QFont(self.font_family, 6, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF; border: none;")
        container.addWidget(label)

        # Curseur
        slider_layout = QHBoxLayout()
        slider_layout.setContentsMargins(-5, 0, 0, 0)  # Décalage de 5 pixels vers la gauche
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(len(values) - 1)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.NoTicks)  # Pas de ticks
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #4ABFF7;        /* Barre en bleu clair */
                height: 10px;
                border-radius: 5px;
                border: none;               /* Suppression du contour noir */
            }
            QSlider::handle:horizontal {
                background: #4ABFF7;        /* Poignée bleu clair */
                border: 2px solid #FFFFFF;  /* Trait blanc autour de la poignée */
                width: 20px;
                height: 20px;
                margin: -5px 0;             /* Alignement vertical */
                border-radius: 10px;        /* Poignée arrondie */
            }
        """)

        slider.setFixedWidth(350)
        slider_layout.addWidget(slider)
        container.addLayout(slider_layout)

        # Labels sous le curseur
        value_labels = QHBoxLayout()
        for value in values:
            lbl = QLabel(value)
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(QFont(self.font_family, 6))
            lbl.setStyleSheet("color: #B0C4DE; border: none;")
            lbl.setFixedWidth(100)
            value_labels.addWidget(lbl)

        container.addLayout(value_labels)
        self.main_layout.addLayout(container)

    def toggle_play_pause(self):
        if self.play_button.text() == "Play":
            self.play_button.setText("Pause")
            self.play_button.setStyleSheet(get_selected_button_style())
        else:
            self.play_button.setText("Play")
            self.play_button.setStyleSheet(get_unselected_button_style())

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.old_pos = event.pos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.pos() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            self.old_pos = None


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    window = OverlayTable()
    window.show()
    sys.exit(app.exec_())
