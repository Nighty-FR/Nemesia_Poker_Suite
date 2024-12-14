import torch
from torch import nn, optim
from torchvision import datasets, transforms, models
import os

# Configuration
DATASET_DIR = r"C:\Users\conta\Desktop\dataset"
MODEL_PATH = r"C:\Users\conta\Documents\python\model_efficientnet.pth"
WEIGHTS_PATH = r"C:\Users\conta\Documents\python\efficientnet_b0_rwightman-7f5810bc.pth"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
NUM_CLASSES = 56  # Nombre de classes dans votre dataset

# Transformation des données
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.3, contrast=0.3),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Chargement des données
dataset = datasets.ImageFolder(root=DATASET_DIR, transform=transform)
dataloader = torch.utils.data.DataLoader(dataset, batch_size=32, shuffle=True)

# Chargement du modèle EfficientNet avec des poids locaux
print("Chargement du modèle EfficientNet avec des poids locaux...")
model = models.efficientnet_b0(weights=None)  # Pas de téléchargement
state_dict = torch.load(WEIGHTS_PATH)
model.load_state_dict(state_dict)

# Ajustement de la dernière couche pour le nombre de classes
model.classifier[1] = nn.Linear(model.classifier[1].in_features, NUM_CLASSES)
model = model.to(DEVICE)

# Configuration de l'entraînement
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# Entraînement
num_epochs = 10
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for inputs, labels in dataloader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    scheduler.step()
    print(f"Époque {epoch + 1}/{num_epochs}, Perte : {running_loss / len(dataloader):.4f}")

# Sauvegarde du modèle
torch.save(model.state_dict(), MODEL_PATH)
print(f"Modèle sauvegardé à : {MODEL_PATH}")
