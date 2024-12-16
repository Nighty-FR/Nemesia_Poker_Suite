def load_stylesheet():
    """Charge le style général de la fenêtre."""
    return """
        QMainWindow {
            background: qradialgradient(cx:0.5, cy:0.5, radius:1, stop:0 #101820, stop:1 #1B2838);
        }
    """

def get_slider_style():
    """Style des curseurs."""
    return """
        QSlider::groove:horizontal {
            background: #4ABFF7;
            height: 10px;
            border-radius: 5px;
        }
        QSlider::handle:horizontal {
            background: #4ABFF7;
            border: 2px solid #FFFFFF;
            width: 20px;
            height: 20px;
            margin: -5px 0;
            border-radius: 10px;
        }
    """

def get_selected_button_style():
    """Style pour les boutons sélectionnés."""
    return """
        QPushButton {
            background-color: #4ABFF7;
            color: #101820;
            border: 2px solid #FFFFFF;
            border-radius: 15px;
            font-weight: bold;
        }
    """

def get_unselected_button_style():
    """Style pour les boutons non sélectionnés."""
    return """
        QPushButton {
            background-color: #101820;
            color: #4ABFF7;
            border: 2px solid #4ABFF7;
            border-radius: 15px;
        }
        QPushButton:hover {
            background-color: #4ABFF7;
            color: #101820;
        }
    """
