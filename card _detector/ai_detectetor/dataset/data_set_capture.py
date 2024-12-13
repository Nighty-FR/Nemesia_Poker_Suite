import sys
import os
import json
import cv2
import numpy as np
import pyautogui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRect

# Fichier de configuration pour sauvegarder les positions et dimensions
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

class CardCaptureOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        screen = app.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        self.setWindowTitle("Overlay Transparent - Capture Dataset")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        # Chargement des rectangles depuis le fichier de configuration
        self.rectangles = self.load_config()

        # Rectangle actif
        self.active_rectangle = None
        self.dragging = False
        self.resizing = False
        self.start_pos = None

        # Ajouter les boutons "+" et "-"
        self.add_button = QPushButton("+", self)
        self.add_button.setGeometry(10, 10, 40, 40)
        self.add_button.clicked.connect(self.add_rectangle)

        self.remove_button = QPushButton("-", self)
        self.remove_button.setGeometry(60, 10, 40, 40)
        self.remove_button.clicked.connect(self.remove_rectangle)

        # Rendre les boutons repositionnables
        self.dragging_button = None

    def load_config(self):
        """Charge les positions et dimensions des rectangles depuis config.json."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                data = json.load(file)
                return [QRect(*rect) for rect in data]
        else:
            # Si aucun fichier de config, initialiser une liste vide
            return []

    def save_config(self):
        """Sauvegarde les positions et dimensions des rectangles dans config.json."""
        data = [[rect.x(), rect.y(), rect.width(), rect.height()] for rect in self.rectangles]
        with open(CONFIG_FILE, "w") as file:
            json.dump(data, file, indent=4)

    def paintEvent(self, event):
        """Dessine les rectangles sur l'overlay."""
        painter = QPainter(self)
        pen = QPen(Qt.red, 2)
        brush = QBrush(QColor(255, 0, 0, 50))  # Fond semi-transparent
        painter.setPen(pen)
        painter.setBrush(brush)

        for rect in self.rectangles:
            painter.drawRect(rect)

    def mousePressEvent(self, event):
        """Détecte si un rectangle ou bouton est cliqué pour drag ou resize."""
        for rect in self.rectangles:
            if rect.contains(event.pos()):
                self.active_rectangle = rect
                self.start_pos = event.pos()
                if event.button() == Qt.LeftButton:
                    self.dragging = True
                elif event.button() == Qt.RightButton:
                    self.resizing = True
                return

        # Vérifier si un bouton est cliqué pour le repositionner
        if self.add_button.geometry().contains(event.pos()):
            self.dragging_button = self.add_button
            self.start_pos = event.pos()
        elif self.remove_button.geometry().contains(event.pos()):
            self.dragging_button = self.remove_button
            self.start_pos = event.pos()

    def mouseMoveEvent(self, event):
        """Permet de déplacer ou redimensionner un rectangle ou repositionner un bouton."""
        if self.active_rectangle:
            dx = event.pos().x() - self.start_pos.x()
            dy = event.pos().y() - self.start_pos.y()

            if self.dragging:
                # Déplacer le rectangle
                new_x = max(0, min(self.active_rectangle.x() + dx, self.screen_width - self.active_rectangle.width()))
                new_y = max(0, min(self.active_rectangle.y() + dy, self.screen_height - self.active_rectangle.height()))
                self.active_rectangle.moveTo(new_x, new_y)
            elif self.resizing:
                # Redimensionner le rectangle
                new_width = max(30, self.active_rectangle.width() + dx)
                new_height = max(30, self.active_rectangle.height() + dy)
                self.active_rectangle.setWidth(new_width)
                self.active_rectangle.setHeight(new_height)

            self.start_pos = event.pos()
            self.update()
        elif self.dragging_button:
            # Déplacer un bouton
            dx = event.pos().x() - self.start_pos.x()
            dy = event.pos().y() - self.start_pos.y()
            new_pos = self.dragging_button.geometry().adjusted(dx, dy, dx, dy)
            self.dragging_button.setGeometry(new_pos)
            self.start_pos = event.pos()

    def mouseReleaseEvent(self, event):
        """Réinitialise les états après une interaction."""
        self.dragging = False
        self.resizing = False
        self.dragging_button = None
        self.active_rectangle = None
        # Sauvegarder les rectangles après chaque modification
        self.save_config()

    def add_rectangle(self):
        """Ajoute un nouveau rectangle au centre de l'écran."""
        default_width, default_height = 100, 100
        x = (self.screen_width - default_width) // 2
        y = (self.screen_height - default_height) // 2
        new_rect = QRect(x, y, default_width, default_height)
        self.rectangles.append(new_rect)
        self.save_config()
        self.update()
        print(f"Rectangle ajouté : x={x}, y={y}, width={default_width}, height={default_height}")

    def remove_rectangle(self):
        """Supprime le dernier rectangle ajouté."""
        if self.rectangles:
            removed_rect = self.rectangles.pop()
            self.save_config()
            self.update()
            print(f"Rectangle supprimé : {removed_rect}")

    def capture_rectangles(self):
        """Capture les zones définies par les rectangles."""
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)

        for i, rect in enumerate(self.rectangles):
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            cropped = screenshot_np[y:y+h, x:x+w]
            filename = f"capture_{i}.png"
            cv2.imwrite(filename, cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR))
            print(f"Rectangle {i} capturé et sauvegardé sous : {filename}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = CardCaptureOverlay()
    overlay.show()
    sys.exit(app.exec_())
