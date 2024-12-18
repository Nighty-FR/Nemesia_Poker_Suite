import os
import sqlite3

# Chemin vers la base de données
BASE_DIR = os.path.expanduser("~\\Documents\\Némésia Poker Suite")
DB_PATH = os.path.join(BASE_DIR, "poker_bot.db")

def ensure_directory_exists():
    """Vérifie que le dossier 'Némésia Poker Suite' existe."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

def ensure_database_exists():
    """Vérifie que la base de données existe."""
    if not os.path.exists(DB_PATH):
        with sqlite3.connect(DB_PATH) as conn:
            print(f"Base de données créée : {DB_PATH}")
    else:
        print(f"Base de données existante : {DB_PATH}")

def get_user_preferences():
    """Récupère les préférences utilisateur."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT site, style, nombre_tables, niveau_aide
            FROM overlay
            WHERE id = 1
            LIMIT 1
        ''')
        row = cursor.fetchone()
        if row:
            return row
        else:
            # Valeurs par défaut si aucun enregistrement
            cursor.execute("INSERT INTO overlay (id) VALUES (1)")
            conn.commit()
            return "Winamax", "Heads-Up", 1, 0

def update_user_preferences(site, style, nombre_tables, niveau_aide):
    """Met à jour les préférences utilisateur."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE overlay
            SET site = ?, style = ?, nombre_tables = ?, niveau_aide = ?
            WHERE id = 1
        ''', (site, style, nombre_tables, niveau_aide))
        conn.commit()

def fetch_overlay_table_data(site, style, table_id):
    """Récupère les rectangles associés à un site, style et table donnés."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT label, x, y, width, height
            FROM overlay_table
            WHERE site = ? AND style = ? AND table_id = ?
        ''', (site, style, table_id))
        rows = cursor.fetchall()
        return rows

def save_rectangle_position(table_id, label, x, y, width, height):
    """Met à jour la position d'un rectangle dans la table."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE overlay_table
            SET x = ?, y = ?, width = ?, height = ?
            WHERE table_id = ? AND label = ?
        ''', (x, y, width, height, table_id, label))
        conn.commit()
        print(f"Rectangle '{label}' de table {table_id} mis à jour.")

if __name__ == "__main__":
    ensure_directory_exists()
    ensure_database_exists()
    print("Fonctions principales vérifiées.")
