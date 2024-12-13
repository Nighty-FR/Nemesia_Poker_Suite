import os
import logging
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models, optimizers
from tensorflow.keras.applications import MobileNet

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("train_model.log"), logging.StreamHandler()]
)

# Paramètres
BASE_DATASET_DIR = os.path.join(os.path.dirname(__file__), "dataset")
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), "mobilenet_cards_model.h5")
IMAGE_SIZE = (128, 128)
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 52  # Les 52 cartes

def prepare_data():
    """
    Prépare les données à partir du dataset en utilisant l'augmentation d'image.
    Returns:
        train_generator, val_generator: Générateurs pour l'entraînement et la validation.
    """
    # Générateur de données avec augmentation
    data_gen = ImageDataGenerator(
        rescale=1.0 / 255,  # Normalisation
        validation_split=0.2,  # Fraction des données pour la validation
        rotation_range=15,  # Rotation aléatoire
        width_shift_range=0.1,  # Translation horizontale
        height_shift_range=0.1,  # Translation verticale
        shear_range=0.1,  # Distorsion
        zoom_range=0.1,  # Zoom
        horizontal_flip=True,  # Miroir horizontal
        fill_mode="nearest"  # Remplissage des pixels manquants
    )

    # Générateur d'entraînement
    train_generator = data_gen.flow_from_directory(
        BASE_DATASET_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="training"
    )

    # Générateur de validation
    val_generator = data_gen.flow_from_directory(
        BASE_DATASET_DIR,
        target_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE,
        class_mode="categorical",
        subset="validation"
    )

    return train_generator, val_generator

def build_model():
    """
    Construit le modèle MobileNet avec fine-tuning.
    Returns:
        model: Le modèle compilé.
    """
    # Charger MobileNet pré-entraîné
    base_model = MobileNet(weights="imagenet", include_top=False, input_shape=(*IMAGE_SIZE, 3))

    # Geler les couches du modèle de base
    for layer in base_model.layers:
        layer.trainable = False

    # Ajouter des couches personnalisées pour la classification des cartes
    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation="relu"),
        layers.Dropout(0.5),
        layers.Dense(NUM_CLASSES, activation="softmax")
    ])

    # Compiler le modèle
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    logging.info("Modèle MobileNet construit avec succès.")
    return model

def train_model():
    """
    Entraîne le modèle MobileNet sur le dataset des cartes.
    """
    # Préparer les données
    train_generator, val_generator = prepare_data()

    # Construire le modèle
    model = build_model()

    # Entraîner le modèle
    logging.info("Début de l'entraînement du modèle.")
    history = model.fit(
        train_generator,
        epochs=EPOCHS,
        validation_data=val_generator,
        verbose=1
    )

    # Sauvegarder le modèle entraîné
    model.save(MODEL_SAVE_PATH)
    logging.info(f"Modèle entraîné et sauvegardé dans : {MODEL_SAVE_PATH}")

    # Résultats
    logging.info(f"Précision finale sur l'ensemble de validation : {history.history['val_accuracy'][-1]:.4f}")

if __name__ == "__main__":
    train_model()
