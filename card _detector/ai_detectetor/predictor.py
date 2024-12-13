import os
import cv2
import numpy as np
import logging
from tensorflow.keras.models import load_model

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

MODEL_PATH = os.path.join(os.getcwd(), "ai_detector", "card_model.h5")

def predict_image(image_path):
    """
    Prédit la classe d'une carte à partir de son image.
    """
    model = load_model(MODEL_PATH)
    logging.info(f"Modèle chargé : {MODEL_PATH}")

    # Charger et prétraiter l'image
    image = cv2.imread(image_path)
    image = cv2.resize(image, (128, 128))
    image = np.expand_dims(image, axis=0) / 255.0

    prediction = model.predict(image)
    predicted_class = np.argmax(prediction)
    confidence = np.max(prediction)

    logging.info(f"Classe prédite : {predicted_class}, Confiance : {confidence:.2f}")
    return predicted_class, confidence
