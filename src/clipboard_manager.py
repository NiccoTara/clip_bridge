import subprocess
import os


class ClipboardManager:
    """Handles read/write operations with system clipboard via CopyQ"""

    @staticmethod
    def copy_text(text: str) -> bool:
        """Write plain text to clipboard"""
        try:
            subprocess.run(['copyq', 'add', text], capture_output=True, check=True)
            subprocess.run(['copyq', 'copy', text], capture_output=True, check=True)
            return True
        except Exception:
            return False

    @staticmethod
    def copy_file(filepath: str) -> bool:
        """Write file path as URI to clipboard"""
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
        """Try to read PNG image from clipboard. Returns bytes or None."""
        try:
            return subprocess.check_output(['copyq', 'read', 'image/png'])
        except subprocess.CalledProcessError:
            return None

    @staticmethod
    def read_text() -> str:
        """Read plain text from clipboard. Returns empty string if unavailable."""
        try:
            content_bytes = subprocess.check_output(['copyq', 'read', 'text/plain'])
            return content_bytes.decode('utf-8').strip()
        except subprocess.CalledProcessError:
            return ""
