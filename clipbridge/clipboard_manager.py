import subprocess
import shutil
import time
import os


class ClipboardManager:
    """Handles read/write operations with system clipboard via CopyQ"""

    @staticmethod
    def ensure_running() -> None:
        """Ensure CopyQ is installed and its server is responsive, launching it if needed."""
        if not shutil.which('copyq'):
            raise RuntimeError(
                "CopyQ is not installed. Install it using: sudo apt install copyq"
            )

        # Check if the CopyQ server is already responding
        try:
            subprocess.run(
                ['copyq', 'eval', ''],
                capture_output=True, timeout=2, check=True,
            )
            return  # already running
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
            pass

        # Start CopyQ in the background (Popen does not block)
        subprocess.Popen(
            ['copyq', '--start-server'],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait until the server becomes responsive (up to ~5 s)
        for _ in range(10):
            time.sleep(0.5)
            try:
                subprocess.run(
                    ['copyq', 'eval', ''],
                    capture_output=True, timeout=2, check=True,
                )
                return
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
                continue

        raise RuntimeError("CopyQ was started but is not responding.")

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
