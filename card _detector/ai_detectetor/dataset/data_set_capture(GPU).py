import os
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
from PIL import Image
from torch.nn.functional import cosine_similarity

# Configuration
IMAGE_DIR = r"C:\Users\conta\Desktop\Images_Captured"
SIMILARITY_THRESHOLD = 0.03
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Modèle pré-entraîné
model = resnet18(pretrained=True)
model = torch.nn.Sequential(*list(model.children())[:-1])  # Retirer la dernière couche
model.eval()
model.to(DEVICE)

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def extract_feature_vector(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0).to(DEVICE)
    with torch.no_grad():
        feature_vector = model(image).flatten()
    return feature_vector

def find_and_remove_duplicates():
    vectors = {}
    files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for file in files:
        file_path = os.path.join(IMAGE_DIR, file)
        if file_path in vectors:
            continue
        try:
            current_vector = extract_feature_vector(file_path)
            is_duplicate = False
            for other_path, other_vector in vectors.items():
                distance = 1 - cosine_similarity(current_vector.unsqueeze(0), other_vector.unsqueeze(0)).item()
                if distance < SIMILARITY_THRESHOLD:
                    print(f"Doublon détecté : {file_path}. Suppression...")
                    os.remove(file_path)
                    is_duplicate = True
                    break
            if not is_duplicate:
                vectors[file_path] = current_vector
        except Exception as e:
            print(f"Erreur lors du traitement de {file}: {e}")

if __name__ == "__main__":
    print(f"Utilisation du périphérique : {DEVICE}")
    find_and_remove_duplicates()
