import os
from werkzeug.utils import secure_filename


class FileHandler:
    """Manages file operations: saving and detecting file types"""

    def __init__(self, save_dir: str):
        self.save_dir = save_dir

    def save_file(self, file_obj) -> str:
        """Save an uploaded file to disk."""
        if not file_obj or not file_obj.filename:
            return None

        filename = secure_filename(file_obj.filename)
        filepath = os.path.join(self.save_dir, filename)
        file_obj.save(filepath)
        return filepath

    def process_file(self, file_obj) -> str:
        """Save the uploaded file"""
        return self.save_file(file_obj)

    def is_text_file(self, filepath: str) -> bool:
        """Check if a file is a text format."""
        text_extensions = {'.txt', '.md', '.json', '.csv', '.log', '.xml', '.html', '.css', '.js', '.py'}
        _, ext = os.path.splitext(filepath.lower())
        return ext in text_extensions

    def get_file_content_if_text(self, filepath: str) -> str:
        """Read text file content if applicable, otherwise return None."""
        if not self.is_text_file(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            os.remove(filepath)
            return content
        except Exception:
            return None
