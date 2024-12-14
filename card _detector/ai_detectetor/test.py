import os

DATASET_DIR = r"C:\Users\conta\Desktop\dataset"

for class_folder in os.listdir(DATASET_DIR):
    class_path = os.path.join(DATASET_DIR, class_folder)
    if os.path.isdir(class_path):
        files = os.listdir(class_path)
        print(f"{class_folder} contient {len(files)} fichiers.")
