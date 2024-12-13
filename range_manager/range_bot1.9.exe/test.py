import os
import sqlite3

# Chemin vers le dossier et la base de données
documents_path = os.path.expanduser("~/Documents")
nemesia_folder = os.path.join(documents_path, "Némésia Poker Suite")
db_path = os.path.join(nemesia_folder, "poker_bot.db")

def create_nemesia_folder_and_db():
    """
    Crée le dossier `Némésia Poker Suite` et la base de données `poker_bot.db` si nécessaire.
    """
    try:
        # Vérifier si le dossier existe
        if not os.path.exists(nemesia_folder):
            os.makedirs(nemesia_folder)
            print(f"Dossier créé : {nemesia_folder}")

        # Vérifier si la base de données existe
        if not os.path.exists(db_path):
            # Création d'une base de données vide
            conn = sqlite3.connect(db_path)
            conn.close()
            print(f"Base de données créée : {db_path}")
        else:
            print(f"Base de données existante trouvée : {db_path}")
    except Exception as e:
        print(f"Erreur lors de la création du dossier ou de la base de données : {e}")

if __name__ == "__main__":
    # Appeler la fonction pour vérifier et/ou créer le dossier et la base de données
    create_nemesia_folder_and_db()
