import sys
import os
import cv2
import time
import json
import numpy as np
import pyautogui
from threading import Thread
from skimage.metrics import structural_similarity as ssim
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRect, QTimer

# Configuration générale
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")
DATASET_DIR = r"C:\Users\conta\Desktop\Images_Captured"
SIMILARITY_THRESHOLD = 0.97  # Seuil de similarité (97%)

os.makedirs(DATASET_DIR, exist_ok=True)  # Crée le dossier s'il n'existe pas


class CardCaptureOverlay(QMainWindow):
    def __init__(self):
        super().__init__()
        screen = QApplication.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()

        # Fenêtre transparente
        self.setWindowTitle("Overlay Transparent - Capture Dataset")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        # Charger les rectangles depuis config.json
        self.rectangles = self.load_config()
        self.dragging_rectangle = None
        self.start_pos = None

        # Timer pour capture automatique
        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.capture_rectangles)
        self.capture_timer.start(2000)  # Capture toutes les 2 secondes

    def load_config(self):
        """Charge les positions et dimensions des rectangles depuis config.json."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                return [QRect(*rect) for rect in json.load(file)]
        else:
            print("Fichier de configuration non trouvé. Vérifiez config.json.")
            return []

    def save_config(self):
        """Sauvegarde les positions et dimensions des rectangles dans config.json."""
        with open(CONFIG_FILE, "w") as file:
            json.dump([[r.x(), r.y(), r.width(), r.height()] for r in self.rectangles], file, indent=4)

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
        """Détecte le clic pour déplacer ou redimensionner les rectangles."""
        for rect in self.rectangles:
            if rect.contains(event.pos()):
                self.dragging_rectangle = rect
                self.start_pos = event.pos()
                break

    def mouseMoveEvent(self, event):
        """Déplace le rectangle sélectionné."""
        if self.dragging_rectangle and self.start_pos:
            dx = event.pos().x() - self.start_pos.x()
            dy = event.pos().y() - self.start_pos.y()
            self.dragging_rectangle.translate(dx, dy)
            self.start_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """Termine le déplacement du rectangle."""
        if self.dragging_rectangle:
            self.dragging_rectangle = None
            self.save_config()

    def capture_rectangles(self):
        """Capture les zones définies par les rectangles."""
        screenshot = pyautogui.screenshot()
        screenshot_np = np.array(screenshot)
        for i, rect in enumerate(self.rectangles):
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            if w > 0 and h > 0:
                cropped = screenshot_np[y:y+h, x:x+w]
                filename = os.path.join(DATASET_DIR, f"capture_{int(time.time())}_{i}.jpeg")
                cv2.imwrite(filename, cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])
                print(f"Image sauvegardée : {filename}")


def find_and_remove_duplicates():
    """Surveille le dossier et supprime les doublons toutes les 15 secondes."""
    while True:
        files = [f for f in os.listdir(DATASET_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        for i, file in enumerate(files):
            file_path = os.path.join(DATASET_DIR, file)
            current_image = cv2.imread(file_path, cv2.IMREAD_COLOR)
            if current_image is None:
                continue
            for other_file in files:
                if file == other_file:
                    continue
                other_file_path = os.path.join(DATASET_DIR, other_file)
                other_image = cv2.imread(other_file_path, cv2.IMREAD_COLOR)
                if other_image is None:
                    continue
                similarity = compare_images(current_image, other_image)
                if similarity > SIMILARITY_THRESHOLD:
                    print(f"Doublon détecté : {file}. Suppression...")
                    os.remove(file_path)
                    break
        time.sleep(15)


def main():
    """Lance l'interface graphique pour les rectangles et le tri des doublons."""
    app = QApplication(sys.argv)
    overlay = CardCaptureOverlay()
    overlay.show()

    # Lancer le tri des doublons dans un thread séparé
    deduplicate_thread = Thread(target=find_and_remove_duplicates, daemon=True)
    deduplicate_thread.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
