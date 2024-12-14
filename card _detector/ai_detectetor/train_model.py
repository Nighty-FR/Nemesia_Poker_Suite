import os
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torchvision.models import resnet18, ResNet18_Weights

# Configuration
DATASET_DIR = r"C:\Users\conta\Desktop\dataset"  # Dossier contenant les images
MODEL_SAVE_PATH = r"C:\Users\conta\Documents\python\model.pth"  # Chemin pour sauvegarder le modèle
NUM_CLASSES = 56  # 52 cartes standards + cartes retournées + non-cartes + cartes combinées
BATCH_SIZE = 32
EPOCHS = 10
LEARNING_RATE = 0.001
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Vérification du GPU
print(f"Entraînement sur : {DEVICE}")

# Transformation des données
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Chargement des données
dataset = datasets.ImageFolder(root=DATASET_DIR, transform=transform)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

# Charger un modèle pré-entraîné
model = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)  # Adapter pour 56 classes
model = model.to(DEVICE)

# Définir la fonction de perte et l'optimiseur
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Entraînement
print("Début de l'entraînement...")
for epoch in range(EPOCHS):
    model.train()
    running_loss = 0.0
    for inputs, labels in dataloader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        # Réinitialiser les gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass et optimisation
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    # Afficher la perte moyenne pour l'époque
    print(f"Époque {epoch + 1}/{EPOCHS}, Perte : {running_loss / len(dataloader):.4f}")

# Sauvegarder le modèle
torch.save(model.state_dict(), MODEL_SAVE_PATH)
print(f"Modèle sauvegardé à : {MODEL_SAVE_PATH}")
