import sqlite3
import config  # Importer la variable globale pour le chemin de la base de données


def create_table():
    """
    Crée la table `ranges` si elle n'existe pas déjà.
    """
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranges (
                position TEXT NOT NULL,
                range_type TEXT NOT NULL,
                hands TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (position, range_type)
            )
        """)
        conn.commit()
        print("Table `ranges` vérifiée ou créée avec succès.")
    except sqlite3.Error as e:
        print(f"Erreur lors de la création de la table : {e}")
    finally:
        conn.close()


def save_range(position, range_type, hands):
    """
    Enregistre ou met à jour un range dans la base de données.

    Args:
        position (str): La position (ex: UTG, CO, BTN).
        range_type (str): Le type de range (ex: Open, 3-Bet).
        hands (list): Liste des mains sélectionnées.
    """
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT hands FROM ranges WHERE position = ? AND range_type = ?
        """, (position, range_type))
        result = cursor.fetchone()

        if result:
            cursor.execute("""
                UPDATE ranges
                SET hands = ?, updated_at = CURRENT_TIMESTAMP
                WHERE position = ? AND range_type = ?
            """, (",".join(hands), position, range_type))
            print(f"Range mis à jour pour {position} ({range_type}).")
        else:
            cursor.execute("""
                INSERT INTO ranges (position, range_type, hands)
                VALUES (?, ?, ?)
            """, (position, range_type, ",".join(hands)))
            print(f"Range ajouté pour {position} ({range_type}).")

        conn.commit()
    except sqlite3.Error as e:
        print(f"Erreur lors de la sauvegarde dans la base de données : {e}")
    finally:
        conn.close()


def load_range(position, range_type):
    """
    Charge un range depuis la base de données.

    Args:
        position (str): La position (ex: UTG, CO, BTN).
        range_type (str): Le type de range (ex: Open, 3-Bet).

    Returns:
        list: Liste des mains pour ce range.
    """
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT hands FROM ranges WHERE position = ? AND range_type = ?
        """, (position, range_type))
        result = cursor.fetchone()

        conn.close()
        if result:
            return result[0].split(",")  # Retourne une liste des mains
    except sqlite3.Error as e:
        print(f"Erreur lors du chargement des ranges : {e}")
    return []


def load_all_ranges():
    """
    Charge tous les ranges de la base de données.

    Returns:
        list: Liste de tuples (position, range_type, hands).
    """
    try:
        conn = sqlite3.connect(config.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT position, range_type, hands FROM ranges
        """)
        results = cursor.fetchall()

        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"Erreur lors du chargement de tous les ranges : {e}")
        return []
