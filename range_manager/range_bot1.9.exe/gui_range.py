import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGridLayout, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QLineEdit, QComboBox, QPushButton
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QIcon
from range_calculator import get_hands_for_percentage, calculate_percentage
from database_range import save_range, load_range, create_table


class RangeSelector(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Némésia Poker Suite - Ranges Manager")
        self.setWindowIcon(QIcon(r"/poker bot/Ref_png/némésia_poker_suite.ico"))

        # Permettre le redimensionnement
        self.setMinimumSize(900, 1000)

        # Variables
        self.range = set()
        self.hands_grid = self.generate_hands_grid()
        self.positions = ["UTG", "UTG+1", "UTG+2", "LJ", "HJ", "CO", "BTN", "SB", "BB"]
        self.range_types = ["Open", "3-Bet", "4-Bet", "Call 3-Bet"]

        # Interface utilisateur
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout(self.central_widget)
        self.info_layout = QHBoxLayout()
        self.grid_layout = QGridLayout()
        self.setCentralWidget(self.central_widget)

        self.init_ui()
        self.apply_styles()

        # Crée la table dans la base de données
        create_table()

        # Charge le range initial pour la position et le type sélectionnés
        self.load_range()

    def generate_hands_grid(self):
        """Génère une structure organisée des mains."""
        ranks = "AKQJT98765432"
        grid = []
        for i, rank1 in enumerate(ranks):
            row = []
            for j, rank2 in enumerate(ranks):
                if i == j:
                    row.append(f"{rank1}{rank2}")  # Paires
                elif i < j:
                    row.append(f"{rank1}{rank2}s")  # Suited
                else:
                    row.append(f"{rank2}{rank1}o")  # Offsuit
            grid.append(row)
        return grid

    def init_ui(self):
        # Affichage du pourcentage des mains jouées
        self.percentage_label = QLabel("Pourcentage des mains jouées : 0.00%", self)

        # Champ de saisie pourcentage
        self.percentage_input = QLineEdit(self)
        self.percentage_input.setPlaceholderText("Entrez %")
        self.percentage_input.setAlignment(Qt.AlignCenter)
        self.percentage_input.returnPressed.connect(self.apply_percentage)

        # Sélection de la position
        self.position_select = QComboBox(self)
        self.position_select.addItems(self.positions)
        self.position_select.currentIndexChanged.connect(self.load_range)

        # Sélection du type de range
        self.range_type_select = QComboBox(self)
        self.range_type_select.addItems(self.range_types)
        self.range_type_select.currentIndexChanged.connect(self.load_range)

        # Ajouter au layout des informations
        self.info_layout.addWidget(self.percentage_label)
        self.info_layout.addWidget(self.percentage_input)
        self.info_layout.addWidget(QLabel("Position :", self))
        self.info_layout.addWidget(self.position_select)
        self.info_layout.addWidget(QLabel("Type :", self))
        self.info_layout.addWidget(self.range_type_select)

        # Grille de mains
        for i, row in enumerate(self.hands_grid):
            for j, hand in enumerate(row):
                button = QPushButton(hand, self)
                button.setCheckable(True)
                button.setFixedSize(50, 50)  # Dimensions initiales des boutons
                button.clicked.connect(lambda checked, h=hand: self.toggle_hand(h, checked))
                self.grid_layout.addWidget(button, i, j)

        # Bouton Sauvegarder
        self.save_button = QPushButton("Sauvegarder", self)
        self.save_button.setFixedHeight(40)
        self.save_button.clicked.connect(self.save_range)

        # Ajouter les layouts
        self.main_layout.addLayout(self.info_layout)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addWidget(self.save_button)

        # Ajuster automatiquement les tailles
        self.central_widget.setLayout(self.main_layout)

    def resizeEvent(self, event):
        """Ajuste la taille des boutons et widgets lors du redimensionnement."""
        # Calcul des nouvelles dimensions pour maintenir les proportions
        button_width = self.width() // 15
        button_height = self.height() // 20

        for i in range(self.grid_layout.count()):
            button = self.grid_layout.itemAt(i).widget()
            button.setFixedSize(button_width, button_height)

        # Ajuster les autres widgets
        self.save_button.setFixedHeight(button_height)
        self.percentage_input.setFixedWidth(button_width * 2)

        super().resizeEvent(event)

    def toggle_hand(self, hand, checked):
        """Ajoute ou retire une main du range."""
        if checked:
            self.range.add(hand)
        else:
            self.range.discard(hand)

        self.update_percentage()

    def update_percentage(self):
        """Met à jour le pourcentage des mains jouées."""
        percentage = calculate_percentage(self.range)
        self.percentage_label.setText(f"Pourcentage des mains jouées : {percentage:.2f}%")

    def apply_percentage(self):
        """Applique un range basé sur un pourcentage."""
        try:
            percentage = float(self.percentage_input.text())
            hands = get_hands_for_percentage(percentage)
            self.range = set(hands)
            self.update_buttons()
            self.update_percentage()
        except ValueError:
            pass

    def update_buttons(self):
        """Met à jour l'état des boutons en fonction du range sélectionné."""
        for i in range(self.grid_layout.count()):
            button = self.grid_layout.itemAt(i).widget()
            button.setChecked(button.text() in self.range)

    def save_range(self):
        """Enregistre le range sélectionné avec la position et le type."""
        position = self.position_select.currentText()
        range_type = self.range_type_select.currentText()
        save_range(position, range_type, list(self.range))
        print(f"Range sauvegardé pour {position} ({range_type}) : {sorted(self.range)}")

        # Affiche l'animation de confirmation
        self.show_save_animation()

    def load_range(self):
        """Charge un range depuis la base de données."""
        position = self.position_select.currentText()
        range_type = self.range_type_select.currentText()
        hands = load_range(position, range_type)

        if hands:
            self.range = set(hands)
            print(f"Range chargée pour {position} ({range_type}) : {hands}")
        else:
            self.range = set()
            print(f"Aucun range trouvé pour {position} ({range_type}).")

        self.update_buttons()
        self.update_percentage()

    def show_save_animation(self):
        """Affiche une animation pour confirmer la sauvegarde."""
        self.save_label = QLabel("Range sauvegardé avec succès !", self)
        self.save_label.setStyleSheet("""
            QLabel {
                color: #4ABFF7;  /* Bleu clair */
                font-size: 16px;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 150);  /* Fond semi-transparent */
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.save_label.setAlignment(Qt.AlignCenter)
        self.save_label.setFixedSize(300, 50)
        self.save_label.move(
            self.width() // 2 - self.save_label.width() // 2,
            self.height() // 2 - self.save_label.height() // 2
        )
        self.save_label.show()

        # Crée une animation de fondu
        self.fade_animation = QPropertyAnimation(self.save_label, b"windowOpacity")
        self.fade_animation.setDuration(2000)
        self.fade_animation.setStartValue(1)
        self.fade_animation.setEndValue(0)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.fade_animation.finished.connect(self.save_label.deleteLater)
        self.fade_animation.start()

    def apply_styles(self):
        """Applique les styles directement au widget."""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1B2838;  /* Bleu foncé */
            }
            QLabel {
                color: #FFFFFF;  /* Blanc */
                font-size: 14px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #FFFFFF;  /* Blanc */
                color: #000000;  /* Noir */
                border: 2px solid #4ABFF7;  /* Bleu clair */
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox {
                background-color: #FFFFFF;  /* Blanc */
                color: #000000;  /* Noir */
                border: 2px solid #4ABFF7;  /* Bleu clair */
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4ABFF7;  /* Bleu clair */
                color: #FFFFFF;  /* Blanc */
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5B7A99;  /* Bleu acier */
            }
            QPushButton:checked {
                background-color: #B0C4DE;  /* Argenté */
                color: #000000;  /* Noir */
            }
        """)


if __name__ == "__main__":
    create_table()
    app = QApplication(sys.argv)
    window = RangeSelector()
    window.show()
    sys.exit(app.exec_())
