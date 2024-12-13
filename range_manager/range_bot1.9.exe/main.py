import sys
import os
import shutil
import sqlite3
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QMovie
from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QWidget, QMessageBox, QFileDialog
)
from gui_range import RangeSelector
import config  # Importer le module pour la variable globale
import logging

# Set up logging
LOG_DIR = os.path.expanduser("~/Documents/Némésia Poker Suite/Log")
LOG_FILE = os.path.join(LOG_DIR, "range_manager.log")

def setup_logging():
    """Sets up logging for the application."""
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )

setup_logging()

def verify_or_create_nemesia_folder():
    """
    Vérifie ou crée le dossier `Némésia Poker Suite`.
    """
    documents_path = os.path.expanduser("~/Documents")
    nemesia_folder = os.path.join(documents_path, "Némésia Poker Suite")

    if not os.path.exists(nemesia_folder):
        os.makedirs(nemesia_folder)
        logging.info(f"Dossier créé : {nemesia_folder}")

    return nemesia_folder

def verify_or_create_db(nemesia_folder):
    """
    Vérifie si la base de données existe dans le dossier donné. Si elle n'existe pas,
    retourne None pour permettre à l'utilisateur de choisir.
    """
    db_path = os.path.join(nemesia_folder, "poker_bot.db")

    if not os.path.exists(db_path):
        logging.warning("Base de données introuvable, elle sera créée.")
        return None
    logging.info(f"Base de données existante trouvée : {db_path}")
    return db_path

class SplashScreen(QWidget):
    def __init__(self, nemesia_folder):
        super().__init__()
        self.setWindowTitle("Némésia Poker Suite - Loading")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(900, 1000)
        self.setStyleSheet("background-color: #1B2838;")

        self.nemesia_folder = nemesia_folder
        self.db_path = None

        # Layout principal
        layout = QVBoxLayout(self)

        # Espacement supplémentaire en haut
        top_spacer = QLabel("")
        top_spacer.setFixedHeight(50)  # Ajustez cette valeur pour augmenter ou réduire l'espace
        layout.addWidget(top_spacer)

        # Logo
        self.logo_label = QLabel(self)
        pixmap = QPixmap(r"/poker bot/Ref_png/némésia_poker_suite.webp")
        self.logo_label.setPixmap(pixmap.scaled(800, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.logo_label)

        # Animation circulaire
        self.loading_label = QLabel(self)
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("background: transparent;")
        self.movie = QMovie(r"C:\\Users\\conta\\Documents\\python\\pythonProject\\poker bot\\Ref_png\\loading_spinner.gif")

        if self.movie.isValid():
            self.loading_label.setMovie(self.movie)
            self.movie.start()
        layout.addWidget(self.loading_label)

        # Texte
        self.search_label = QLabel("Chargement de la base de données...", self)
        self.search_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        self.search_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.search_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_db_status)
        self.timer.start(2000)  # Temps fixe de 2 secondes

    def check_db_status(self):
        """Vérifie l'état de la base de données après le splash screen."""
        self.timer.stop()
        self.db_path = verify_or_create_db(self.nemesia_folder)

        if not self.db_path:
            self.show_db_choice_dialog()
        else:
            config.DB_PATH = self.db_path  # Met à jour la variable globale
            logging.info("Base de données trouvée, lancement de l'application principale.")
            self.show_main_window()

    def show_db_choice_dialog(self):
        """Affiche une boîte de dialogue pour créer ou sélectionner une base de données."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Base de données introuvable")
        msg_box.setText("Aucune base de données trouvée. Que voulez-vous faire ?")
        msg_box.setIcon(QMessageBox.Question)

        # Ajouter les boutons sans personnalisation de style
        create_button = msg_box.addButton("Créer une nouvelle DB", QMessageBox.AcceptRole)
        select_button = msg_box.addButton("Sélectionner un fichier", QMessageBox.ActionRole)
        close_button = msg_box.addButton("Fermer", QMessageBox.RejectRole)

        msg_box.exec_()

        # Actions selon le bouton sélectionné
        if msg_box.clickedButton() == create_button:
            self.create_new_db()
        elif msg_box.clickedButton() == select_button:
            self.select_existing_db()
        else:
            logging.error("Aucune base de données sélectionnée. Fermeture de l'application.")
            self.close_application()

    def create_new_db(self):
        """Crée une nouvelle base de données vierge."""
        db_path = os.path.join(self.nemesia_folder, "poker_bot.db")
        conn = sqlite3.connect(db_path)
        conn.close()
        logging.info(f"Base de données créée : {db_path}")
        config.DB_PATH = db_path  # Met à jour la variable globale
        self.show_main_window()

    def select_existing_db(self):
        """Permet à l'utilisateur de sélectionner une base de données existante."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        selected_path, _ = QFileDialog.getOpenFileName(self, "Sélectionner une base de données", "", "SQLite Files (*.db);;All Files (*)", options=options)

        if selected_path:
            new_path = os.path.join(self.nemesia_folder, "poker_bot.db")
            shutil.copy(selected_path, new_path)
            logging.info(f"Base de données déplacée et renommée : {new_path}")
            config.DB_PATH = new_path  # Met à jour la variable globale
            self.show_main_window()
        else:
            logging.warning("Aucun fichier sélectionné. Fermeture de l'application.")
            self.close_application()

    def show_main_window(self):
        """Affiche la fenêtre principale avec le chemin de la base de données."""
        logging.debug("Affichage de la fenêtre principale.")
        self.main_window = RangeSelector()
        self.main_window.db_path = config.DB_PATH
        self.main_window.show()
        self.close()

    def close_application(self):
        """Ferme complètement l'application."""
        logging.info("Fermeture de l'application...")
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Vérification ou création du dossier
    nemesia_folder = verify_or_create_nemesia_folder()

    # Splash screen
    splash = SplashScreen(nemesia_folder)
    splash.show()

    sys.exit(app.exec_())
