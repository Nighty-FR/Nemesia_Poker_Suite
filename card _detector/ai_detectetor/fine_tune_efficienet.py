import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models

# Chemins
DATASET_DIR = r"C:\Users\conta\Desktop\dataset"
MODEL_PATH = r"C:\Users\conta\Documents\python\model_efficientnet.pth"
SAVE_PATH = r"C:\Users\conta\Documents\python\model_efficientnet_finetuned.pth"

# Hyperparamètres
NUM_CLASSES = 56  # Nombre de classes
BATCH_SIZE = 32
NUM_EPOCHS = 5
LEARNING_RATE = 0.001
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Transformations des données
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Chargement du dataset
train_dataset = datasets.ImageFolder(root=DATASET_DIR, transform=transform)
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Chargement du modèle EfficientNet
print("Chargement du modèle EfficientNet...")
model = models.efficientnet_b0(weights=None)  # Charger un modèle sans poids

# Charger les poids en ignorant la dernière couche de classification
state_dict = torch.load(MODEL_PATH)
filtered_state_dict = {k: v for k, v in state_dict.items() if "classifier" not in k}
model.load_state_dict(filtered_state_dict, strict=False)

# Remplacer la dernière couche pour correspondre au nombre de classes
model.classifier[1] = nn.Linear(model.classifier[1].in_features, NUM_CLASSES)
model = model.to(DEVICE)

# Optimiseur et fonction de perte
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

# Entraînement
print("Début du Fine-Tuning...")
for epoch in range(NUM_EPOCHS):
    model.train()
    running_loss = 0.0
    for inputs, labels in train_loader:
        inputs, labels = inputs.to(DEVICE), labels.to(DEVICE)

        # Forward + Backpropagation
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

    print(f"Époque {epoch + 1}/{NUM_EPOCHS}, Perte : {running_loss / len(train_loader):.4f}")

# Sauvegarde du modèle
torch.save(model.state_dict(), SAVE_PATH)
print(f"Modèle fine-tuné sauvegardé à : {SAVE_PATH}")
