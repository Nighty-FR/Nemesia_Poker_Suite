import os
import time
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
from scipy.spatial.distance import cosine

# Configuration générale
IMAGE_DIR = r"C:\Users\conta\Desktop\Images_Captured"
SIMILARITY_THRESHOLD = 0.03  # Distance cosinus (1 - 0.97)
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Créer le dossier si nécessaire
os.makedirs(IMAGE_DIR, exist_ok=True)

# Charger le modèle ResNet18 pré-entraîné
model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
model = torch.nn.Sequential(*list(model.children())[:-1])  # Retirer la dernière couche
model.eval().to(DEVICE)

# Transformation des images
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def extract_feature_vector(image_path):
    """Extrait un vecteur de caractéristiques pour une image donnée."""
    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            feature_vector = model(image).flatten()
        return feature_vector
    except Exception as e:
        print(f"Erreur lors de l'extraction du vecteur pour {image_path}: {e}")
        return None

def find_and_remove_duplicates():
    """Détecte et supprime les doublons en utilisant des vecteurs de caractéristiques."""
    vectors = {}  # Stocke les vecteurs des images

    while True:
        files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for file in files:
            file_path = os.path.join(IMAGE_DIR, file)

            # Si le fichier est déjà analysé, on passe
            if file_path in vectors:
                continue

            # Extraire le vecteur de l'image
            feature_vector = extract_feature_vector(file_path)
            if feature_vector is None:
                continue

            # Comparer avec les vecteurs existants
            is_duplicate = False
            for other_path, other_vector in vectors.items():
                distance = cosine(feature_vector.cpu(), other_vector.cpu())
                if distance < SIMILARITY_THRESHOLD:
                    print(f"Doublon détecté : {file_path} (distance cosinus : {distance:.4f}). Suppression...")
                    os.remove(file_path)
                    is_duplicate = True
                    break

            # Ajouter le vecteur si ce n'est pas un doublon
            if not is_duplicate:
                vectors[file_path] = feature_vector

        time.sleep(15)  # Vérification toutes les 15 secondes

if __name__ == "__main__":
    if not os.path.exists(IMAGE_DIR):
        print(f"Le dossier {IMAGE_DIR} n'existe pas.")
    else:
        print(f"Surveillance du dossier : {IMAGE_DIR}")
        print(f"Utilisation du périphérique : {DEVICE}")
        find_and_remove_duplicates()
