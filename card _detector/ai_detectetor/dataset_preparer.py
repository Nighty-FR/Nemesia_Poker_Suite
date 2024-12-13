import os
import cv2
import logging
from datetime import datetime

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("dataset_preparer.log"), logging.StreamHandler()]
)

# Liste complète des cartes (valeurs et symboles)
CARDS = [
    f"{value}{suit}" for value in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    for suit in ["H", "D", "C", "S"]  # H = ♥, D = ♦, C = ♣, S = ♠
]

# Répertoire de base pour le dataset
BASE_DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")

class DatasetPreparer:
    def __init__(self):
        """Initialisation de l'organisateur du dataset."""
        self.create_dataset_structure()

    def create_dataset_structure(self):
        """Crée la structure du dataset avec des sous-dossiers pour chaque carte."""
        if not os.path.exists(BASE_DATASET_DIR):
            os.makedirs(BASE_DATASET_DIR)
            logging.info(f"Dossier dataset créé : {BASE_DATASET_DIR}")

        for card in CARDS:
            card_dir = os.path.join(BASE_DATASET_DIR, card)
            if not os.path.exists(card_dir):
                os.makedirs(card_dir)
                logging.info(f"Dossier créé pour la classe : {card}")

    def save_image(self, image, card_label):
        """
        Sauvegarde une image dans le dossier correspondant à la classe (label).
        Args:
            image (numpy.ndarray): Image à sauvegarder.
            card_label (str): Label de la carte (par ex. "2H" pour 2 de cœur).
        """
        if card_label not in CARDS:
            logging.error(f"Label invalide : {card_label}")
            return

        card_dir = os.path.join(BASE_DATASET_DIR, card_label)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_path = os.path.join(card_dir, f"{timestamp}.png")

        cv2.imwrite(file_path, image)
        logging.info(f"Image sauvegardée pour la classe {card_label} : {file_path}")

    def display_dataset_status(self):
        """Affiche le nombre d'images dans chaque classe."""
        logging.info("Statut actuel du dataset :")
        for card in CARDS:
            card_dir = os.path.join(BASE_DATASET_DIR, card)
            image_count = len([f for f in os.listdir(card_dir) if f.endswith(('.png', '.jpg', '.jpeg'))])
            logging.info(f"Classe {card} : {image_count} images")

# Exemple d'utilisation
if __name__ == "__main__":
    dataset_preparer = DatasetPreparer()

    # Exemple : Afficher le statut du dataset
    dataset_preparer.display_dataset_status()

    # Simulation : Sauvegarder une image pour une classe
    # Charger une image factice pour l'exemple
    example_image = 255 * (cv2.getStructuringElement(cv2.MORPH_RECT, (100, 150)).astype("uint8"))  # Rectangle blanc
    dataset_preparer.save_image(example_image, "2H")  # Sauvegarde pour "2♥"
