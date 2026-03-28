import os
from urllib.parse import unquote
from flask import send_file, Response


class ResponseHandler:
    """Handles different response types based on clipboard content"""

    @staticmethod
    def send_image(image_data: bytes) -> Response:
        """Send raw PNG image bytes"""
        return Response(image_data, mimetype='image/png')

    @staticmethod
    def send_file_if_exists(path: str):
        """Send a file if it exists at the given path."""
        # Remove file:// prefix and decode URL-encoded paths
        cleaned_path = path.replace('file://', '', 1).strip()
        filepath = unquote(cleaned_path)

        if filepath.startswith('/') and os.path.isfile(filepath):
            return send_file(
                filepath,
                as_attachment=True,
                download_name=os.path.basename(filepath)
            )
        return None

    @staticmethod
    def send_text(text: str):
        """Send text content."""
        return text, 200
