import os
import tempfile


class TempFileManager:
    @staticmethod
    def save_temp_file(filename, data):
        """Sauvegarde un fichier temporaire."""
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, filename)
        with open(file_path, "wb") as f:
            f.write(data)
        return file_path

    @staticmethod
    def delete_temp_file(filepath):
        """Supprime un fichier temporaire."""
        if os.path.exists(filepath):
            os.remove(filepath)
