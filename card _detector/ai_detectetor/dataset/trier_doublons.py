import os
import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

# Dossier contenant les images à analyser
IMAGE_DIR = r"C:\Users\conta\Desktop\Images_Captured"

def load_images_from_folder(folder):
    """Charge toutes les images d'un dossier."""
    images = []
    filenames = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            if img is not None:
                images.append(img)
                filenames.append(img_path)
    return images, filenames

def compare_images(image1, image2):
    """Compare deux images à l'aide de SSIM."""
    # Redimensionner pour correspondre aux dimensions
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray1, gray2, full=True)
    return score

def find_and_remove_duplicates(images, filenames, similarity_threshold=0.97):
    """Trouve et supprime les doublons."""
    duplicates = set()
    num_images = len(images)

    for i in range(num_images):
        if i in duplicates:
            continue
        for j in range(i + 1, num_images):
            if j in duplicates:
                continue
            similarity = compare_images(images[i], images[j])
            if similarity > similarity_threshold:
                print(f"Doublon trouvé : {filenames[j]} (similarité : {similarity:.2f})")
                duplicates.add(j)

    # Supprimer les fichiers doublons
    for index in duplicates:
        os.remove(filenames[index])
        print(f"Image supprimée : {filenames[index]}")

def main():
    images, filenames = load_images_from_folder(IMAGE_DIR)
    if not images:
        print("Aucune image trouvée dans le dossier.")
        return

    print(f"{len(images)} images chargées depuis {IMAGE_DIR}.")
    find_and_remove_duplicates(images, filenames)

if __name__ == "__main__":
    main()
