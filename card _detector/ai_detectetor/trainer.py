import os
import logging
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from model_builder import build_model

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

DATASET_DIR = os.path.join(os.getcwd(), "ai_detector", "dataset")
MODEL_SAVE_PATH = os.path.join(os.getcwd(), "ai_detector", "card_model.h5")

def train_model():
    """
    Entraîne le modèle CNN avec le dataset.
    """
    logging.info("Chargement des données...")
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

    train_data = datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(128, 128),
        batch_size=32,
        class_mode='sparse',
        subset='training'
    )

    val_data = datagen.flow_from_directory(
        DATASET_DIR,
        target_size=(128, 128),
        batch_size=32,
        class_mode='sparse',
        subset='validation'
    )

    model = build_model(input_shape=(128, 128, 3), num_classes=len(train_data.class_indices))
    logging.info("Entraînement du modèle...")
    model.fit(train_data, validation_data=val_data, epochs=10)

    logging.info(f"Sauvegarde du modèle dans : {MODEL_SAVE_PATH}")
    model.save(MODEL_SAVE_PATH)

if __name__ == "__main__":
    train_model()
