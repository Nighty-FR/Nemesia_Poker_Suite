import os
import cv2
from skimage.metrics import structural_similarity as ssim
import time

# Dossier contenant les images à analyser
IMAGE_DIR = r"C:\Users\conta\Desktop\Images_Captured"
SIMILARITY_THRESHOLD = 0.97  # Seuil de similarité (97%)


def compare_images(image1, image2):
    """Compare deux images à l'aide de SSIM."""
    # Redimensionner pour correspondre aux dimensions
    image1 = cv2.resize(image1, (image2.shape[1], image2.shape[0]))
    gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
    score, _ = ssim(gray1, gray2, full=True)
    return score


def find_and_remove_duplicates():
    """Surveille le dossier et supprime les doublons dès qu'ils sont détectés."""
    processed_files = set()  # Stocke les fichiers déjà analysés

    while True:
        # Charger tous les fichiers du dossier
        files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for file in files:
            file_path = os.path.join(IMAGE_DIR, file)

            if file_path in processed_files:
                continue  # Ignorer les fichiers déjà traités

            try:
                # Charger l'image actuelle
                current_image = cv2.imread(file_path, cv2.IMREAD_COLOR)

                # Comparer avec les autres fichiers du dossier
                for other_file in files:
                    if file == other_file:
                        continue  # Ne pas se comparer avec soi-même

                    other_file_path = os.path.join(IMAGE_DIR, other_file)
                    other_image = cv2.imread(other_file_path, cv2.IMREAD_COLOR)

                    if other_image is None:
                        continue

                    similarity = compare_images(current_image, other_image)

                    if similarity > SIMILARITY_THRESHOLD:
                        print(f"Doublon détecté : {file} (similarité : {similarity:.2f}). Suppression...")
                        os.remove(file_path)
                        break

                # Ajouter le fichier traité à la liste des fichiers analysés
                processed_files.add(file_path)

            except Exception as e:
                print(f"Erreur lors du traitement de {file}: {e}")

        # Pause pour éviter de monopoliser les ressources système
        time.sleep(2)


if __name__ == "__main__":
    if not os.path.exists(IMAGE_DIR):
        print(f"Le dossier {IMAGE_DIR} n'existe pas.")
    else:
        print(f"Surveillance du dossier : {IMAGE_DIR}")
        find_and_remove_duplicates()
