import os
import torch
from torchvision import transforms
from torchvision.models import resnet18, ResNet18_Weights
from PIL import Image
from matplotlib import pyplot as plt
import csv

# Configuration
MODEL_PATH = r"C:\Users\conta\Documents\python\model.pth"  # Chemin du modèle sauvegardé
TEST_IMAGE_DIR = r"C:\Users\conta\Desktop\test image"  # Remplacez par le bon chemin

OUTPUT_REPORT = r"C:\Users\conta\Documents\python\test_report.csv"  # Chemin pour sauvegarder le rapport
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Classes du modèle
CLASSES = [
    "2H", "2D", "2C", "2S", "3H", "3D", "3C", "3S",
    "4H", "4D", "4C", "4S", "5H", "5D", "5C", "5S",
    "6H", "6D", "6C", "6S", "7H", "7D", "7C", "7S",
    "8H", "8D", "8C", "8S", "9H", "9D", "9C", "9S",
    "10H", "10D", "10C", "10S", "JH", "JD", "JC", "JS",
    "QH", "QD", "QC", "QS", "KH", "KD", "KC", "KS",
    "AH", "AD", "AC", "AS", "cartes_retournees",
    "non_cartes", "cartes_combinees", "cartes_combinees_retournees"
]

# Transformation des images
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Charger le modèle
def load_model(model_path, num_classes):
    model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
    model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
    model.load_state_dict(torch.load(model_path, map_location=DEVICE), strict=True)
    model = model.to(DEVICE)
    model.eval()
    return model

# Faire une prédiction sur une image
def predict_image(model, image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        image_tensor = transform(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            outputs = model(image_tensor)
            _, predicted_idx = torch.max(outputs, 1)

        return CLASSES[predicted_idx.item()]
    except Exception as e:
        print(f"Erreur lors de la prédiction pour {image_path} : {e}")
        return None

# Afficher une image avec sa prédiction
def predict_and_display(model, image_path):
    prediction = predict_image(model, image_path)
    image = Image.open(image_path)
    plt.imshow(image)
    plt.title(f"Prédiction : {prediction}")
    plt.axis("off")
    plt.show()
    return prediction

# Tester toutes les images d'un dossier et générer un rapport
def test_images(model, test_image_dir, output_report):
    results = []
    print(f"Test des images dans le dossier : {test_image_dir}\n")

    for file_name in os.listdir(test_image_dir):
        file_path = os.path.join(test_image_dir, file_name)
        if file_name.lower().endswith(('png', 'jpg', 'jpeg')):
            prediction = predict_and_display(model, file_path)
            print(f"Image : {file_name}, Prédiction : {prediction}")
            results.append((file_name, prediction))
        else:
            print(f"Fichier ignoré (format non supporté) : {file_name}")

    # Sauvegarder les résultats dans un fichier CSV
    with open(output_report, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Nom de l'image", "Classe prédite"])
        writer.writerows(results)
    print(f"Rapport des prédictions sauvegardé dans : {output_report}")

if __name__ == "__main__":
    # Charger le modèle
    model = load_model(MODEL_PATH, len(CLASSES))
    print(f"Modèle chargé depuis : {MODEL_PATH}\n")

    # Tester les images
    if os.path.exists(TEST_IMAGE_DIR):
        test_images(model, TEST_IMAGE_DIR, OUTPUT_REPORT)
    else:
        print(f"Le dossier de test n'existe pas : {TEST_IMAGE_DIR}")
