import subprocess
import os
from werkzeug.utils import secure_filename


class FileHandler:
    """Gestisce il salvataggio e la conversione dei file"""

    def __init__(self, save_dir: str):
        self.save_dir = save_dir

    def save_file(self, file_obj) -> str:
        """Salva un file ricevuto. Ritorna il percorso del file."""
        if not file_obj or not file_obj.filename:
            return None

        filename = secure_filename(file_obj.filename)
        filepath = os.path.join(self.save_dir, filename)
        file_obj.save(filepath)
        return filepath

    def convert_heic_to_jpg(self, filepath: str) -> str:
        """Converte HEIC in JPG. Ritorna il nuovo percorso o il percorso originale."""
        if not filepath.lower().endswith('.heic'):
            return filepath

        try:
            jpg_filepath = os.path.join(
                self.save_dir,
                os.path.basename(filepath).rsplit('.', 1)[0] + '.jpg'
            )
            
            # 1. Prevenzione: se il file destinazione esiste già (es. test ripetuti), eliminiamolo
            if os.path.exists(jpg_filepath):
                os.remove(jpg_filepath)

            # 2. Esecuzione della conversione
            subprocess.run(
                ['heif-convert', filepath, jpg_filepath], 
                capture_output=True, 
                check=True
            )
            
            os.remove(filepath)
            return jpg_filepath

        except (subprocess.CalledProcessError, Exception):
            # Fallback: se fallisce (es. era un falso HEIC), restituiamo il file originale
            # così il server non va in errore 500 e tenta comunque di metterlo in CopyQ
            return filepath

    def process_file(self, file_obj) -> str:
        """Elabora un file: salvataggio + conversione se necessaria"""
        filepath = self.save_file(file_obj)
        if not filepath:
            return None

        filepath = self.convert_heic_to_jpg(filepath)
        return filepath

    def is_text_file(self, filepath: str) -> bool:
        """Controlla se il file è un file di testo"""
        text_extensions = {'.txt', '.md', '.json', '.csv', '.log', '.xml', '.html', '.css', '.js', '.py'}
        _, ext = os.path.splitext(filepath.lower())
        return ext in text_extensions

    def get_file_content_if_text(self, filepath: str) -> str:
        """Se il file è testo, ritorna il contenuto. Altrimenti ritorna None."""
        if not self.is_text_file(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            os.remove(filepath)
            return content
        except Exception:
            return None
