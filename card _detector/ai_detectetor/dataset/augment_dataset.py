import os
from PIL import Image
import torchvision.transforms as transforms
import random
import logging

# Configurer le chemin d'accès au dataset
DATASET_DIR = r"C:\Users\conta\Desktop\dataset"  # Remplacez par le chemin vers votre dataset
OUTPUT_DIR = r"C:\Users\conta\Desktop\dataset_augmented"  # Dossier pour le dataset augmenté

# Configurer les logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Transformations d'augmentation
augmentation_transforms = transforms.Compose([
    transforms.RandomRotation(15),  # Rotation aléatoire (-15° à 15°)
    transforms.RandomHorizontalFlip(p=0.5),  # Flip horizontal
    transforms.RandomVerticalFlip(p=0.3),  # Flip vertical
    transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),  # Variations de couleur
    transforms.RandomResizedCrop(size=(224, 224), scale=(0.8, 1.0)),  # Recadrage aléatoire
])

# Vérifiez et créez le dossier de sortie
os.makedirs(OUTPUT_DIR, exist_ok=True)


# Fonction pour augmenter une image
def augment_image(image_path, output_dir, augmentations=5):
    try:
        image = Image.open(image_path).convert("RGB")
        base_name = os.path.splitext(os.path.basename(image_path))[0]

        # Générer plusieurs augmentations pour chaque image
        for i in range(augmentations):
            augmented_image = augmentation_transforms(image)
            augmented_image_path = os.path.join(output_dir, f"{base_name}_aug_{i}.jpg")
            augmented_image.save(augmented_image_path)
        logging.info(f"Augmentations créées pour {image_path}")
    except Exception as e:
        logging.error(f"Erreur avec l'image {image_path}: {e}")


# Parcourir les dossiers et augmenter les données
def augment_dataset(dataset_dir, output_dir, augmentations=5):
    for class_dir in os.listdir(dataset_dir):
        class_path = os.path.join(dataset_dir, class_dir)
        output_class_dir = os.path.join(output_dir, class_dir)
        os.makedirs(output_class_dir, exist_ok=True)

        if os.path.isdir(class_path):
            for image_file in os.listdir(class_path):
                image_path = os.path.join(class_path, image_file)
                if image_file.lower().endswith(('png', 'jpg', 'jpeg')):
                    augment_image(image_path, output_class_dir, augmentations)


if __name__ == "__main__":
    logging.info("Début de l'augmentation du dataset...")
    augment_dataset(DATASET_DIR, OUTPUT_DIR, augmentations=5)
    logging.info("Augmentation du dataset terminée.")
