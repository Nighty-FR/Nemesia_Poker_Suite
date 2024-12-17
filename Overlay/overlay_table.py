import os
from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QSlider, QApplication
)
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtCore import Qt, QPoint
from styles import get_selected_button_style, get_unselected_button_style


class OverlayTable(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Némésia Poker Suite - Overlay Table")
        self.setFixedWidth(450)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.5)  # Transparence de 50%

        # Police personnalisée
        font_path = os.path.abspath("Trajan Pro Regular.ttf")
        self.font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(self.font_id)[0] if self.font_id != -1 else "Arial"

        self.old_pos = None  # Pour le repositionnement
        self.is_playing = False  # État Play/Pause
        self.initUI()

    def initUI(self):
        self.main_widget = QWidget(self)
        self.main_widget.setStyleSheet("""
            QWidget {
                background-color: #1B2838;
                border: 3px solid #101820;
                border-radius: 15px;
            }
        """)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_layout.setContentsMargins(10, 5, 10, 15)
        self.main_layout.setSpacing(10)

        # Titre
        self.title_label = QLabel("NÉMÉSIA POKER SUITE")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont(self.font_family, 12, QFont.Bold))
        self.title_label.setStyleSheet("color: #4ABFF7; border: none;")
        self.main_layout.addWidget(self.title_label)

        # Curseur avec labels
        self.add_slider_section("Niveau d'aide", ["Préflop Assisté", "GTO Avancée", "Autopilotage"])

        # Boutons
        self.add_control_buttons()
        self.setCentralWidget(self.main_widget)

    def add_control_buttons(self):
        button_layout = QHBoxLayout()

        # Play/Pause
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet(get_selected_button_style())
        self.play_button.setFixedSize(100, 40)
        self.play_button.clicked.connect(self.toggle_play_pause)
        button_layout.addWidget(self.play_button)

        # Stop
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(get_unselected_button_style())
        self.stop_button.setFixedSize(100, 40)
        self.stop_button.clicked.connect(self.stop_overlay)
        button_layout.addWidget(self.stop_button)

        # Config
        self.config_button = QPushButton("Config")
        self.config_button.setStyleSheet(get_unselected_button_style())
        self.config_button.setFixedSize(100, 40)
        button_layout.addWidget(self.config_button)

        self.main_layout.addLayout(button_layout)

    def add_slider_section(self, label_text, values):
        container = QVBoxLayout()
        label = QLabel(label_text)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont(self.font_family, 6, QFont.Bold))
        label.setStyleSheet("color: #FFFFFF; border: none;")
        container.addWidget(label)

        slider_layout = QHBoxLayout()
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(0)
        slider.setMaximum(len(values) - 1)
        slider.setTickInterval(1)
        slider.setTickPosition(QSlider.NoTicks)
        slider.setStyleSheet("""
            QSlider::groove:horizontal {
                background: #4ABFF7;
                height: 10px;
                border-radius: 5px;
                border: none;
            }
            QSlider::handle:horizontal {
                background: #4ABFF7;
                border: 2px solid #FFFFFF;
                width: 20px;
                height: 20px;
                margin: -5px 0;
                border-radius: 10px;
            }
        """)
        slider.setFixedWidth(350)
        slider_layout.addWidget(slider)
        container.addLayout(slider_layout)

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
        """Gère l'état Play/Pause."""
        if self.is_playing:
            self.play_button.setText("Play")
            self.play_button.setStyleSheet(get_selected_button_style())
            self.is_playing = False
        else:
            self.play_button.setText("Pause")
            self.play_button.setStyleSheet(get_unselected_button_style())
            self.is_playing = True

    def stop_overlay(self):
        """Arrête le programme."""
        QApplication.quit()

    # Gestion du déplacement avec clic droit
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
    import sys
    app = QApplication(sys.argv)
    window = OverlayTable()
    window.show()
    sys.exit(app.exec_())
