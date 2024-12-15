# overlay_styles.py

# Feuille de style pour l'interface PyQt5

# Couleurs principales
BLEU_CLAIR = "#4ABFF7"  # Aura et accents
BLEU_FONCE = "#1B2838"  # Arrière-plan
ARGENTE = "#B0C4DE"    # Détails métalliques
BLANC = "#FFFFFF"       # Texte et reflets

# Couleurs secondaires
BLEU_PROFOND = "#133B5C"  # Ombres et motifs
BLEU_ACIER = "#5B7A99"    # Éléments secondaires
NOIR_DOUX = "#101820"     # Contraste et profondeur

# Style global pour l'interface principale
MAIN_WINDOW_STYLE = f"""
    QMainWindow {{
        background-color: {BLEU_FONCE};
    }}
    QPushButton {{
        background-color: {BLEU_CLAIR};
        color: {BLANC};
        border-radius: 10px;
        font-size: 14px;
        font-weight: bold;
        padding: 8px 12px;
    }}
    QPushButton:hover {{
        background-color: {BLEU_ACIER};
    }}
    QPushButton:pressed {{
        background-color: {BLEU_PROFOND};
    }}
    QLabel {{
        color: {ARGENTE};
        font-size: 12px;
        font-weight: normal;
    }}
    QFrame {{
        border: 2px solid {BLEU_ACIER};
        background-color: rgba(74, 191, 247, 50);
        border-radius: 5px;
    }}
    QLineEdit {{
        background-color: {BLANC};
        color: {NOIR_DOUX};
        border: 1px solid {ARGENTE};
        border-radius: 5px;
        padding: 4px;
    }}
    QLineEdit:focus {{
        border: 2px solid {BLEU_CLAIR};
        outline: none;
    }}
    QComboBox {{
        background-color: {BLANC};
        color: {NOIR_DOUX};
        border: 1px solid {ARGENTE};
        border-radius: 5px;
        padding: 4px;
        selection-background-color: {BLEU_CLAIR};
    }}
    QComboBox QAbstractItemView {{
        background-color: {BLANC};
        selection-background-color: {BLEU_CLAIR};
        border: 1px solid {ARGENTE};
    }}
"""

# Styles pour les rectangles dessinés (via QPainter)
RECTANGLE_STYLE = {
    "pen_color": BLEU_CLAIR,
    "pen_width": 2,
    "fill_color": "rgba(74, 191, 247, 50)",  # Semi-transparent bleu clair
}
