import os
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image
from collections import defaultdict

# Chemins
MODEL_PATH = "C:\\Users\\conta\\Documents\\python\\model_efficientnet_finetuned.pth"
TEST_PATH = "C:\\Users\\conta\\Desktop\\test_ai"

# Définition des classes
CLASSES = [
    "10C", "10D", "10H", "10S", "2C", "2D", "2H", "2S", "3C", "3D", "3H", "3S",
    "4C", "4D", "4H", "4S", "5C", "5D", "5H", "5S", "6C", "6D", "6H", "6S",
    "7C", "7D", "7H", "7S", "8C", "8D", "8H", "8S", "9C", "9D", "9H", "9S",
    "AC", "AD", "AH", "AS", "JC", "JD", "JH", "JS", "KC", "KD", "KH", "KS",
    "QC", "QD", "QH", "QS", "cartes_combinees", "cartes_combinees_retournees",
    "cartes_retournees", "non_cartes"
]

# Préparer les transformations
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Charger le modèle
print("Chargement du modèle EfficientNet...")
model = models.efficientnet_b0(weights=None)
model.classifier[1] = torch.nn.Linear(in_features=1280, out_features=len(CLASSES))
model.load_state_dict(torch.load(MODEL_PATH))
model.eval()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
model.to(DEVICE)
print("Modèle chargé et prêt à l'utilisation.")

# Fonction pour renommer les fichiers avec les prédictions
def rename_with_prediction(folder_path, model, transform):
    count_dict = defaultdict(int)  # Pour éviter les noms en double

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        try:
            # Ouvrir et transformer l'image
            image = Image.open(file_path).convert("RGB")
            input_tensor = transform(image).unsqueeze(0).to(DEVICE)

            # Prédiction
            with torch.no_grad():
                output = model(input_tensor)
                _, predicted_idx = torch.max(output, 1)
                predicted_label = CLASSES[predicted_idx.item()]

            # Renommer l'image
            count_dict[predicted_label] += 1
            new_file_name = f"{predicted_label}_{count_dict[predicted_label]}.jpg"
            new_file_path = os.path.join(folder_path, new_file_name)

            os.rename(file_path, new_file_path)
            print(f"Image renommée : {file_name} -> {new_file_name}")

        except Exception as e:
            print(f"Erreur lors du traitement de {file_name}: {e}")

# Exécuter le tri et le renommage
print(f"Test des images dans le dossier : {TEST_PATH}")
rename_with_prediction(TEST_PATH, model, transform)
print("Tri et renommage terminés.")
