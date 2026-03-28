import subprocess
import os


class ClipboardManager:
    """Gestisce le operazioni con la clipboard tramite CopyQ"""

    @staticmethod
    def copy_text(text: str) -> bool:
        """Copia testo nella clipboard"""
        try:
            subprocess.run(['copyq', 'add', text], capture_output=True, check=True)
            subprocess.run(['copyq', 'copy', text], capture_output=True, check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def copy_file(filepath: str) -> bool:
        """Copia file nella clipboard come URI"""
        try:
            file_uri = f"file://{os.path.abspath(filepath)}"
            subprocess.run([
                'copyq',
                'write',
                'text/uri-list', file_uri,
                'text/plain', filepath
            ], check=True)
            subprocess.run(['copyq', 'select', '0'], check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def get_clipboard() -> str:
        """Legge il contenuto della clipboard"""
        try:
            result = subprocess.run(['copyq', 'clipboard'], 
                                    capture_output=True, text=True, check=True)
            return result.stdout
        except Exception:
            return ""
