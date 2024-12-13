import os
import sqlite3
import logging

# Chemins constants
BASE_DIR = os.path.join(os.path.expanduser("~"), "Documents", "Némésia Poker Suite")
DB_PATH = os.path.join(BASE_DIR, "poker_bot.db")

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("database_cd.log"), logging.StreamHandler()]
)


class DatabaseManager:
    def __init__(self):
        # Vérification du dossier et de la base de données
        self.ensure_directory_exists()
        self.ensure_database_exists()
        self.ensure_table_exists()

    def ensure_directory_exists(self):
        """Vérifie que le dossier existe, sinon le crée."""
        if not os.path.exists(BASE_DIR):
            os.makedirs(BASE_DIR)
            logging.info(f"Dossier créé : {BASE_DIR}")
        else:
            logging.info(f"Dossier déjà existant : {BASE_DIR}")

    def ensure_database_exists(self):
        """Vérifie que la base de données existe, sinon la crée."""
        if not os.path.exists(DB_PATH):
            logging.info(f"Base de données non trouvée. Création de {DB_PATH}...")
            conn = sqlite3.connect(DB_PATH)
            conn.close()
        else:
            logging.info(f"Base de données existante : {DB_PATH}")

    def ensure_table_exists(self):
        """Vérifie que la table CD_Rectangle existe, sinon la crée."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS CD_Rectangle (
                label TEXT PRIMARY KEY,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        logging.info("Table CD_Rectangle vérifiée/créée.")

    def save_rectangle(self, label, x, y, width, height):
        """Enregistre ou met à jour un rectangle dans la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CD_Rectangle (label, x, y, width, height)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(label) DO UPDATE SET
            x = excluded.x,
            y = excluded.y,
            width = excluded.width,
            height = excluded.height
        """, (label, x, y, width, height))
        conn.commit()
        conn.close()
        logging.info(f"Rectangle enregistré : {label} (x={x}, y={y}, w={width}, h={height})")

    def load_rectangles(self):
        """Charge les rectangles depuis la base de données."""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT label, x, y, width, height FROM CD_Rectangle")
        rows = cursor.fetchall()
        conn.close()
        logging.info("Rectangles chargés depuis la base de données.")
        return rows
