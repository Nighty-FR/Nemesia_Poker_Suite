import sys
import os
import json
import cv2
import numpy as np
import pyautogui
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRect, QTimer

# Fichier de configuration pour sauvegarder les positions et dimensions
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
# Dossier où les captures seront enregistrées
DATASET_DIR = r"C:\Users\conta\Desktop\Images_Captured"
os.makedirs(DATASET_DIR, exist_ok=True)  # Crée le dossier s'il n'existe pas

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

        # Timer pour captures automatiques
        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.capture_rectangles)
        self.capture_timer.start(2000)  # Capture toutes les 2 secondes

        # Timer pour le clic simulé
        self.click_timer = QTimer(self)
        self.click_timer.timeout.connect(self.simulate_mouse_click)
        self.click_timer.start(180000)  # Clic toutes les 3 minutes (180 000 ms)

    def load_config(self):
        """Charge les positions et dimensions des rectangles depuis config.json."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                data = json.load(file)
                return [QRect(*rect) for rect in data]
        else:
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

    def capture_rectangles(self):
        """Capture les zones définies par les rectangles."""
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)

        for i, rect in enumerate(self.rectangles):
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            print(f"Rectangle {i}: x={x}, y={y}, width={w}, height={h}")

            if w <= 0 or h <= 0:
                print(f"Rectangle {i} ignoré (dimensions invalides : width={w}, height={h})")
                continue

            cropped = screenshot_np[y:y+h, x:x+w]

            # Sauvegarder l'image directement dans le dossier
            filename = os.path.join(DATASET_DIR, f"capture_{int(time.time())}_{i}.jpeg")
            cv2.imwrite(filename, cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])
            print(f"Image sauvegardée : {filename}")

    def simulate_mouse_click(self):
        """Simule un clic gauche au milieu de l'écran."""
        x = self.screen_width // 2
        y = self.screen_height // 2
        pyautogui.click(x, y)
        print("Clic gauche simulé au centre de l'écran pour éviter la déconnexion.")

    def add_rectangle(self):
        """Ajoute un nouveau rectangle au centre de l'écran."""
        default_width, default_height = 100, 100
        x = (self.screen_width - default_width) // 2
        y = (self.screen_height - default_height) // 2
        new_rect = QRect(x, y, default_width, default_height)
        self.rectangles.append(new_rect)
        self.save_config()
        self.update()

    def remove_rectangle(self):
        """Supprime le dernier rectangle ajouté."""
        if self.rectangles:
            self.rectangles.pop()
            self.save_config()
            self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = CardCaptureOverlay()
    overlay.show()
    sys.exit(app.exec_())
