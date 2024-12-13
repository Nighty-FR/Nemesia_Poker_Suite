import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRect, QTimer
import pyautogui
from database_cd import DatabaseManager


class CardDetectorOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Obtenir la taille de l'écran
        screen = app.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        # Configuration de la fenêtre
        self.setWindowTitle("Overlay Transparent - Détection des cartes")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        # Initialisation de la base de données
        self.db_manager = DatabaseManager()

        # Charger les rectangles depuis la base de données
        loaded_rectangles = self.db_manager.load_rectangles()
        self.rectangles = [
            {"rect": QRect(x, y, width, height), "label": label}
            for label, x, y, width, height in loaded_rectangles
        ]

        # Ajouter des rectangles par défaut si aucun n'est présent
        if not self.rectangles:
            self.rectangles = [
                {"rect": QRect(200, 100, 150, 100), "label": "Flop"},
                {"rect": QRect(100, 300, 150, 100), "label": "Joueur 1"},
                {"rect": QRect(300, 300, 150, 100), "label": "Joueur 2"},
                {"rect": QRect(500, 300, 150, 100), "label": "Joueur 3"},
                {"rect": QRect(700, 300, 150, 100), "label": "Joueur 4"},
                {"rect": QRect(900, 300, 150, 100), "label": "Joueur 5"},
            ]

        # Rectangle actif (pour drag ou resize)
        self.active_rectangle = None
        self.dragging = False
        self.resizing = False
        self.start_pos = None

        # Timer pour capture des zones
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_zones)
        self.captures_enabled = True  # Contrôle des captures
        self.timer.start(1000)  # Capture toutes les secondes

    def paintEvent(self, event):
        # Dessiner les rectangles et leurs labels
        painter = QPainter(self)
        pen = QPen(Qt.red, 2)
        brush = QBrush(QColor(255, 0, 0, 50))  # Fond semi-transparent
        painter.setPen(pen)
        painter.setBrush(brush)

        for item in self.rectangles:
            rect = item["rect"]
            label = item["label"]

            # Dessiner le rectangle
            painter.drawRect(rect)

            # Ajouter le texte en dehors, en haut à gauche du rectangle
            painter.setPen(Qt.yellow)  # Couleur du texte
            font = painter.font()
            font.setBold(True)
            painter.setFont(font)
            text_x = rect.x() - 10  # Légèrement à gauche du rectangle
            text_y = rect.y() - 10  # Au-dessus du rectangle
            painter.drawText(text_x, text_y, label)

    def mousePressEvent(self, event):
        for item in self.rectangles:
            rect = item["rect"]
            if rect.contains(event.pos()):
                self.active_rectangle = rect
                self.start_pos = event.pos()
                if event.button() == Qt.LeftButton:
                    self.dragging = True
                elif event.button() == Qt.RightButton:
                    self.resizing = True
                self.captures_enabled = False  # Désactiver les captures pendant l'interaction
                break

    def mouseMoveEvent(self, event):
        if self.active_rectangle:
            dx = event.pos().x() - self.start_pos.x()
            dy = event.pos().y() - self.start_pos.y()

            if self.dragging:
                # Déplacer le rectangle sans dépasser les limites de l'écran
                new_x = max(0, min(self.active_rectangle.x() + dx, self.screen_width - self.active_rectangle.width()))
                new_y = max(0, min(self.active_rectangle.y() + dy, self.screen_height - self.active_rectangle.height()))
                self.active_rectangle.moveTo(new_x, new_y)

            elif self.resizing:
                # Redimensionner sans dépasser les limites de l'écran
                new_width = max(30, min(self.active_rectangle.width() + dx, self.screen_width - self.active_rectangle.x()))
                new_height = max(30, min(self.active_rectangle.height() + dy, self.screen_height - self.active_rectangle.y()))
                self.active_rectangle.setWidth(new_width)
                self.active_rectangle.setHeight(new_height)

            self.start_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.active_rectangle:
            # Sauvegarder le rectangle modifié dans la base de données
            for item in self.rectangles:
                if item["rect"] == self.active_rectangle:
                    rect = item["rect"]
                    self.db_manager.save_rectangle(
                        item["label"], rect.x(), rect.y(), rect.width(), rect.height()
                    )
        self.dragging = False
        self.resizing = False
        self.active_rectangle = None
        self.captures_enabled = True  # Réactiver les captures après l'interaction

    def capture_zones(self):
        if not self.captures_enabled:
            return  # Ne rien faire si les captures sont désactivées

        # Capture l'écran
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)

        # Extraire les zones définies par les rectangles
        for i, item in enumerate(self.rectangles):
            rect = item["rect"]
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            cropped_zone = screenshot_np[y:y+h, x:x+w]

            # Sauvegarder ou traiter les zones capturées
            cv2.imwrite(f"zone_{item['label']}.png", cv2.cvtColor(cropped_zone, cv2.COLOR_RGB2BGR))
            print(f"Zone {item['label']} capturée et sauvegardée.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = CardDetectorOverlay()
    overlay.show()
    sys.exit(app.exec_())
