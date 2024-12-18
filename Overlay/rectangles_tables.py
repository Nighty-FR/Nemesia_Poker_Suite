import sqlite3
import os
import random

# Chemin vers la base de données
BASE_DIR = os.path.expanduser("~\\Documents\\Némésia Poker Suite")
DB_PATH = os.path.join(BASE_DIR, "poker_bot.db")

# Données par défaut pour les rectangles
RECTANGLE_CATEGORIES = ["pseudo", "carte", "action", "BB", "flop_turn_river"]
DEFAULT_PARENT_WIDTH = 800
DEFAULT_PARENT_HEIGHT = 600
DEFAULT_CHILD_SIZES = {
    "pseudo": (150, 50),
    "carte": (100, 150),
    "action": (100, 50),
    "BB": (80, 40),
    "flop_turn_river": (100, 100),
}

# Fonctions pour gérer les rectangles
def create_overlay_table():
    """Crée la table overlay_table pour stocker les rectangles."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS overlay_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_id INTEGER NOT NULL,
                site TEXT NOT NULL,
                style TEXT NOT NULL,
                label TEXT NOT NULL,
                x INTEGER NOT NULL,
                y INTEGER NOT NULL,
                width INTEGER NOT NULL,
                height INTEGER NOT NULL
            )
        ''')
        conn.commit()
        print("Table 'overlay_table' créée ou existante.")

def initialize_default_rectangles():
    """Initialise les rectangles avec des valeurs par défaut aléatoires."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Nettoyer les rectangles existants pour recommencer à zéro
        cursor.execute("DELETE FROM overlay_table")

        for site in ["Winamax", "PokerStars", "Unibet"]:
            for style in ["Heads-Up", "5-Max", "6-Max", "9-Max", "Tournoi"]:
                for table_id in range(1, 7):
                    # Rectangle parent "table"
                    parent_x = random.randint(0, 300)
                    parent_y = random.randint(0, 300)
                    cursor.execute('''
                        INSERT INTO overlay_table (table_id, site, style, label, x, y, width, height)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (table_id, site, style, "table", parent_x, parent_y, DEFAULT_PARENT_WIDTH, DEFAULT_PARENT_HEIGHT))

                    # Rectangles enfants
                    for category in RECTANGLE_CATEGORIES:
                        count = 2 if category != "flop_turn_river" else 5
                        for i in range(count):
                            rel_x = random.randint(10, 100)
                            rel_y = random.randint(10, 100)
                            width, height = DEFAULT_CHILD_SIZES[category]
                            x = parent_x + rel_x
                            y = parent_y + rel_y
                            label = f"{category}_{i+1}"

                            cursor.execute('''
                                INSERT INTO overlay_table (table_id, site, style, label, x, y, width, height)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (table_id, site, style, label, x, y, width, height))

        conn.commit()
        print("Rectangles initiaux insérés avec succès.")

if __name__ == "__main__":
    create_overlay_table()
    initialize_default_rectangles()
