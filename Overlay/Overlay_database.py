import os
import sqlite3

BASE_DIR = os.path.expanduser("~\\Documents\\Némésia Poker Suite")
DB_PATH = os.path.join(BASE_DIR, "poker_bot.db")


def ensure_directory_exists():
    """Vérifie que le dossier 'Némésia Poker Suite' existe."""
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)


def reset_overlay_table():
    """Réinitialise proprement la table overlay."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS overlay")  # Suppression sécurisée
        cursor.execute('''
            CREATE TABLE overlay (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                site TEXT DEFAULT "Winamax",
                style TEXT DEFAULT "Heads Up",
                nombre_tables INTEGER DEFAULT 1,
                niveau_aide INTEGER DEFAULT 0
            )
        ''')
        cursor.execute("INSERT INTO overlay (id) VALUES (1)")
        conn.commit()
        print("Table 'overlay' recréée avec succès.")


def get_user_preferences():
    """Récupère les préférences utilisateur."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT site, style, nombre_tables, niveau_aide FROM overlay WHERE id=1 LIMIT 1")
        return cursor.fetchone()


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


if __name__ == "__main__":
    ensure_directory_exists()
    reset_overlay_table()
    print("Base de données prête avec la table 'overlay'.")
