import os
import torch
from torchvision import transforms, models
from PIL import Image
import matplotlib.pyplot as plt
import logging

# Configuration
MODEL_PATH = r"C:\Users\conta\Documents\python\model_resnet50.pth"  # Chemin vers le modèle entraîné
TEST_IMAGES_DIR = r"C:\Users\conta\Desktop\test image"  # Chemin vers les images de test
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Configurer les logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Charger le modèle
logging.info("Chargement du modèle ResNet50...")
model = models.resnet50(weights=None)
model.fc = torch.nn.Linear(model.fc.in_features, 56)  # Adapter au nombre de classes (56 ici)
model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE), strict=True)
model = model.to(DEVICE)
model.eval()
logging.info(f"Modèle chargé depuis : {MODEL_PATH}")

# Transformation pour les images de test
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Obtenir les noms des classes
CLASS_NAMES = [
    "2H", "2D", "2C", "2S", "3H", "3D", "3C", "3S",
    "4H", "4D", "4C", "4S", "5H", "5D", "5C", "5S",
    "6H", "6D", "6C", "6S", "7H", "7D", "7C", "7S",
    "8H", "8D", "8C", "8S", "9H", "9D", "9C", "9S",
    "10H", "10D", "10C", "10S", "JH", "JD", "JC", "JS",
    "QH", "QD", "QC", "QS", "KH", "KD", "KC", "KS",
    "AH", "AD", "AC", "AS",
    "cartes_combinees", "cartes_combinees_retournees",
    "cartes_retournees", "non_cartes"
]

# Fonction pour effectuer une prédiction sur une image
def predict_image(image_path, model, transform, class_names):
    try:
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0).to(DEVICE)

        with torch.no_grad():
            outputs = model(input_tensor)
            _, predicted = torch.max(outputs, 1)

        return class_names[predicted.item()]
    except Exception as e:
        logging.error(f"Erreur lors de la prédiction pour {image_path} : {e}")
        return None

# Tester et afficher les images avec leurs prédictions
def test_and_preview_images(test_dir, model, transform, class_names):
    if not os.path.exists(test_dir):
        logging.error(f"Le dossier de test n'existe pas : {test_dir}")
        return

    logging.info(f"Test des images dans le dossier : {test_dir}")
    for image_file in os.listdir(test_dir):
        image_path = os.path.join(test_dir, image_file)
        if image_file.lower().endswith(('png', 'jpg', 'jpeg')):
            prediction = predict_image(image_path, model, transform, class_names)
            if prediction:
                logging.info(f"Image : {image_file}, Prédiction : {prediction}")
                display_image_with_prediction(image_path, prediction)

# Afficher une image avec sa prédiction
def display_image_with_prediction(image_path, prediction):
    image = Image.open(image_path).convert("RGB")
    plt.imshow(image)
    plt.title(f"Prédiction : {prediction}", fontsize=14, color="blue")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    test_and_preview_images(TEST_IMAGES_DIR, model, transform, CLASS_NAMES)
