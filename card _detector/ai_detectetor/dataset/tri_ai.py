import os
import shutil
import torch
from torchvision import transforms, models
from PIL import Image

# Configuration des chemins
SOURCE_DIR = r"C:\Users\conta\Desktop\tentative_tri_ai\Images_Captured - Copie"
DATASET_DIR = r"C:\Users\conta\Desktop\tentative_tri_ai\dataset"
MODEL_PATH = r"C:\Users\conta\Documents\python\model_efficientnet.pth"

# Liste des classes (doit correspondre aux sous-dossiers dans DATASET_DIR)
CLASSES = ["10C", "10D", "10H", "10S", "2C", "2D", "2H", "2S", "3C", "3D", "3H", "3S",
           "4C", "4D", "4H", "4S", "5C", "5D", "5H", "5S", "6C", "6D", "6H", "6S",
           "7C", "7D", "7H", "7S", "8C", "8D", "8H", "8S", "9C", "9D", "9H", "9S",
           "AC", "AD", "AH", "AS", "cartes_combinees", "cartes_combinees_retournees", "cartes_retournees",
           "JC", "JD", "JH", "JS", "KC", "KD", "KH", "KS", "non_cartes", "QC", "QD", "QH", "QS"]

# Transformation des images
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Chargement du modèle
print("Chargement du modèle EfficientNet...")
model = models.efficientnet_b0(pretrained=False)
model.classifier[1] = torch.nn.Linear(model.classifier[1].in_features, len(CLASSES))
model.load_state_dict(torch.load(MODEL_PATH, map_location="cuda" if torch.cuda.is_available() else "cpu"))
model.eval()
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(DEVICE)

# Fonction pour prédire la classe d'une image
def predict(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        image = transform(image).unsqueeze(0).to(DEVICE)
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)
            return CLASSES[predicted.item()]
    except Exception as e:
        print(f"Erreur lors de la prédiction pour {image_path}: {e}")
        return None

# Traitement des images
if __name__ == "__main__":
    if not os.path.exists(SOURCE_DIR):
        print(f"Le dossier source n'existe pas : {SOURCE_DIR}")
        exit(1)

    if not os.path.exists(DATASET_DIR):
        print(f"Le dossier dataset n'existe pas : {DATASET_DIR}")
        exit(1)

    for image_name in os.listdir(SOURCE_DIR):
        image_path = os.path.join(SOURCE_DIR, image_name)

        if not os.path.isfile(image_path):
            continue

        print(f"Traitement de l'image : {image_name}")
        prediction = predict(image_path)

        if prediction and prediction in CLASSES:
            destination_dir = os.path.join(DATASET_DIR, prediction)
            os.makedirs(destination_dir, exist_ok=True)
            shutil.move(image_path, os.path.join(destination_dir, image_name))
            print(f"Image déplacée dans : {destination_dir}")
        else:
            print(f"Impossible de classer l'image : {image_name}")

    print("Tri terminé.")
