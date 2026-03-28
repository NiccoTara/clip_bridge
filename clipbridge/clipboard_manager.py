import subprocess
import os


class ClipboardManager:
    """Handles read/write operations with system clipboard via CopyQ"""

    @staticmethod
    def copy_text(text: str) -> bool:
        """Copy text to the clipboard."""
        try:
            subprocess.run(['copyq', 'add', text], capture_output=True, check=True)
            subprocess.run(['copyq', 'copy', text], capture_output=True, check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def copy_file(filepath: str) -> bool:
        """Copy a file path to the clipboard."""
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
    def read_image() -> bytes:
        """Read PNG image data from the clipboard, or None if not available."""
        try:
            return subprocess.check_output(['copyq', 'read', 'image/png'])
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def read_text() -> str:
        """Read text from the clipboard."""
        try:
            content_bytes = subprocess.check_output(['copyq', 'read', 'text/plain'])
            return content_bytes.decode('utf-8').strip()
        except subprocess.CalledProcessError:
            return ""
