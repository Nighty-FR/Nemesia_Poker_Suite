import sys
from PyQt5.QtWidgets import QApplication
from ui_elements import NemesiaPokerSuite  # Importation de l'interface principale

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NemesiaPokerSuite()
    window.show()
    sys.exit(app.exec_())
