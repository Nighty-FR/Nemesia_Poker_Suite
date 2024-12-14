import os

# Chemin du dataset sur le bureau
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
dataset_path = os.path.join(desktop_path, "dataset")

# Noms des classes (52 cartes standards + catégories supplémentaires)
classes = [
    # Cartes standards
    "2H", "2D", "2C", "2S",
    "3H", "3D", "3C", "3S",
    "4H", "4D", "4C", "4S",
    "5H", "5D", "5C", "5S",
    "6H", "6D", "6C", "6S",
    "7H", "7D", "7C", "7S",
    "8H", "8D", "8C", "8S",
    "9H", "9D", "9C", "9S",
    "10H", "10D", "10C", "10S",
    "JH", "JD", "JC", "JS",
    "QH", "QD", "QC", "QS",
    "KH", "KD", "KC", "KS",
    "AH", "AD", "AC", "AS",

    # Catégories supplémentaires
    "cartes_retournees",                # Cartes retournées
    "non_cartes",                       # Zones sans cartes
    "cartes_combinees",                 # Cartes combinées visibles
    "cartes_combinees_retournees"       # Cartes combinées retournées
]

# Créer le dossier dataset
if not os.path.exists(dataset_path):
    os.makedirs(dataset_path)
    print(f"Dossier principal créé : {dataset_path}")

# Créer les sous-dossiers pour chaque classe
for class_name in classes:
    class_path = os.path.join(dataset_path, class_name)
    if not os.path.exists(class_path):
        os.makedirs(class_path)
        print(f"Dossier créé pour la classe : {class_name}")

print("Structure du dataset créée avec succès.")
