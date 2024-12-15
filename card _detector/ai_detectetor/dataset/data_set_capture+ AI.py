import sys
import os
import json
import cv2
import numpy as np
import time
import torch
import torchvision.models as models
from PIL import ImageGrab
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QRect, QTimer

# Chemin du modèle
MODEL_PATH = r"C:\Users\conta\Documents\python\model_efficientnet_finetuned.pth"

# Dossier de captures sur le bureau
BASE_DIR = os.path.expanduser(r"~/Desktop/capture")
os.makedirs(BASE_DIR, exist_ok=True)

# Dossier de dataset final
DATASET_DIR = r"C:\Users\conta\Desktop\dataset - Copie"

# Fichier de configuration pour les rectangles
CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")


class CardCaptureOverlay(QMainWindow):
    def __init__(self):
        super().__init__()

        # Chargement du modèle CNN
        self.model = self.load_model()
        self.model.eval()

        # Configuration de la fenêtre
        screen = app.primaryScreen().geometry()
        self.screen_width = screen.width()
        self.screen_height = screen.height()
        self.setWindowTitle("Overlay Transparent - Capture Dataset")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, self.screen_width, self.screen_height)

        # Chargement des rectangles
        self.rectangles = self.load_config()

        # Timers
        self.capture_timer = QTimer(self)
        self.capture_timer.timeout.connect(self.capture_rectangles)

        # Boutons Play/Pause
        self.play_button = QPushButton("Play", self)
        self.play_button.setGeometry(10, 60, 60, 40)
        self.play_button.clicked.connect(self.toggle_capture)

        # Bouton pour ajouter un rectangle
        self.add_button = QPushButton("+", self)
        self.add_button.setGeometry(10, 10, 40, 40)
        self.add_button.clicked.connect(self.add_rectangle)

        # Indicateur d'état
        self.recording_label = QLabel("En pause", self)
        self.recording_label.setGeometry(80, 60, 100, 40)
        self.recording_label.setStyleSheet("color: red; font-weight: bold;")

        # Variables
        self.is_recording = False

    def load_model(self):
        """Reconstruit l'architecture du modèle et charge les poids."""
        model = models.efficientnet_b0(weights=None)
        num_features = model.classifier[1].in_features
        state_dict = torch.load(
            MODEL_PATH,
            map_location=torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )
        num_classes = state_dict["classifier.1.weight"].size(0)
        model.classifier[1] = torch.nn.Linear(num_features, num_classes)
        model.load_state_dict(state_dict)
        return model

    def load_config(self):
        """Charge les rectangles depuis config.json."""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as file:
                data = json.load(file)
                print(f"Rectangles chargés : {data}")  # Log pour vérifier les données
                return [QRect(*rect) for rect in data]
        else:
            print("Fichier config.json non trouvé, création d'une configuration vide.")
            return []

    def save_config(self):
        """Sauvegarde les rectangles dans config.json."""
        data = [[rect.x(), rect.y(), rect.width(), rect.height()] for rect in self.rectangles]
        with open(CONFIG_FILE, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Configuration sauvegardée : {data}")  # Log

    def toggle_capture(self):
        """Démarre ou arrête la capture."""
        if self.is_recording:
            self.capture_timer.stop()
            self.is_recording = False
            self.recording_label.setText("En pause")
            self.recording_label.setStyleSheet("color: red; font-weight: bold;")
            self.play_button.setText("Play")
        else:
            self.capture_timer.start(1000)
            self.is_recording = True
            self.recording_label.setText("En cours")
            self.recording_label.setStyleSheet("color: green; font-weight: bold;")
            self.play_button.setText("Pause")

    def paintEvent(self, event):
        """Dessine les rectangles."""
        painter = QPainter(self)
        pen = QPen(Qt.red, 2)
        brush = QBrush(QColor(255, 0, 0, 50))  # Fond semi-transparent
        painter.setPen(pen)
        painter.setBrush(brush)

        if not self.rectangles:
            print("Aucun rectangle à dessiner.")  # Log si aucun rectangle n'est chargé

        for rect in self.rectangles:
            print(f"Dessin du rectangle : x={rect.x()}, y={rect.y()}, width={rect.width()}, height={rect.height()}")  # Log
            painter.drawRect(rect)

    def add_rectangle(self):
        """Ajoute un rectangle par défaut pour tester."""
        default_width, default_height = 100, 100
        x = (self.screen_width - default_width) // 2
        y = (self.screen_height - default_height) // 2
        new_rect = QRect(x, y, default_width, default_height)
        self.rectangles.append(new_rect)
        self.save_config()  # Met à jour config.json
        self.update()  # Redessine la fenêtre
        print(f"Rectangle ajouté : {new_rect}")

    def capture_rectangles(self):
        """Capture les rectangles définis."""
        screenshot = ImageGrab.grab()
        screenshot_np = np.array(screenshot)

        for i, rect in enumerate(self.rectangles):
            x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
            if w <= 0 or h <= 0:
                continue

            cropped = screenshot_np[y:y + h, x:x + w]
            temp_filename = os.path.join(BASE_DIR, f"capture_{time.time():.6f}.jpeg")
            cv2.imwrite(temp_filename, cv2.cvtColor(cropped, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])

    def process_captures(self):
        """Traite les captures en fonction des prédictions."""
        for file in os.listdir(BASE_DIR):
            file_path = os.path.join(BASE_DIR, file)

            # Vérifier que c'est bien un fichier d'image
            if not file.lower().endswith(".jpeg"):
                continue

            # Analyse avec le modèle
            prediction = self.predict_image(file_path)

            if prediction in ["cartes_retournees", "cartes_combinees_retournees", "non_cartes"]:
                os.remove(file_path)  # Supprime les fichiers ignorés
            else:
                # Déplace vers le dossier correspondant
                target_dir = os.path.join(DATASET_DIR, prediction)
                os.makedirs(target_dir, exist_ok=True)
                new_filename = os.path.join(target_dir, f"{file}")
                os.rename(file_path, new_filename)

    def predict_image(self, image_path):
        """Effectue une prédiction sur l'image."""
        image = cv2.imread(image_path)
        if image is None:
            print(f"Impossible de lire l'image : {image_path}")
            return "non_cartes"  # Classe par défaut pour éviter les erreurs

        image = cv2.resize(image, (224, 224))  # Assurez-vous que la taille est correcte pour le modèle
        image = np.transpose(image, (2, 0, 1))  # CHW format
        image = torch.tensor(image, dtype=torch.float32).unsqueeze(0) / 255.0
        if torch.cuda.is_available():
            image = image.cuda()
            self.model = self.model.cuda()
        with torch.no_grad():
            outputs = self.model(image)
            _, predicted = torch.max(outputs, 1)
        return str(predicted.item())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = CardCaptureOverlay()
    overlay.show()
    sys.exit(app.exec_())
