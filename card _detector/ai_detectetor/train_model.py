import os
import torch
from torchvision import datasets, transforms, models
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import logging

# Configurer le chemin des données et du modèle
DATASET_DIR = r"C:\Users\conta\Desktop\dataset"  # Chemin vers votre dataset
MODEL_SAVE_PATH = r"C:\Users\conta\Documents\python\model_resnet50.pth"

# Configurer les logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Configuration des hyperparamètres
BATCH_SIZE = 32
EPOCHS = 15
LEARNING_RATE = 0.0001
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Transformation des données
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Charger le dataset
dataset = datasets.ImageFolder(root=DATASET_DIR, transform=transform)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

# Charger ResNet50 préentraîné
logging.info("Chargement du modèle ResNet50...")
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V1)
model.fc = nn.Linear(model.fc.in_features, len(dataset.classes))  # Adapter la dernière couche
model = model.to(DEVICE)

# Définir la perte et l'optimiseur
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Fonction d'entraînement
def train(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        # Forward
        outputs = model(images)
        loss = criterion(outputs, labels)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    return running_loss / len(loader)

# Fonction de validation
def validate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)

            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item()

            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = correct / total
    return running_loss / len(loader), accuracy

# Boucle d'entraînement
logging.info("Début de l'entraînement...")
for epoch in range(EPOCHS):
    train_loss = train(model, train_loader, criterion, optimizer, DEVICE)
    val_loss, val_accuracy = validate(model, val_loader, criterion, DEVICE)

    logging.info(f"Époque {epoch+1}/{EPOCHS}, "
                 f"Perte d'entraînement : {train_loss:.4f}, "
                 f"Perte de validation : {val_loss:.4f}, "
                 f"Précision de validation : {val_accuracy:.4f}")

# Sauvegarder le modèle
torch.save(model.state_dict(), MODEL_SAVE_PATH)
logging.info(f"Modèle sauvegardé à : {MODEL_SAVE_PATH}")
