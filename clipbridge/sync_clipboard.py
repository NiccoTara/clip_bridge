import os
from flask import Flask, request
import flask.cli
import logging

from clipbridge.config import SAVE_DIR, PORT, HOST, TOKEN_FILE
from clipbridge.file_handler import FileHandler
from clipbridge.clipboard_manager import ClipboardManager
from clipbridge.response_handler import ResponseHandler
from clipbridge.auth import get_or_create_token, validate_request
from clipbridge.network_utils import get_local_url
from clipbridge.qr_generator import print_startup_qr

flask.cli.show_server_banner = lambda *args: None
logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
file_handler = FileHandler(SAVE_DIR)
clipboard = ClipboardManager()
is_first_run = not os.path.exists(TOKEN_FILE)
TOKEN = get_or_create_token(TOKEN_FILE)

@app.before_request
def enforce_security():
    validate_request(request, TOKEN)
@app.route('/post', methods=['POST'])
def sync_da_iphone():
    """Receive data from iPhone and sync it to the clipboard."""
    # Handle file uploads
    if 'file' in request.files:
        f = request.files['file']
        filepath = file_handler.process_file(f)
        if not filepath:
            return "Error", 500
        
        # For text files, read the content and copy it
        text_content = file_handler.get_file_content_if_text(filepath)
        if text_content is not None:
            return "OK", 200 if clipboard.copy_text(text_content) else ("Error", 500)
        
        # For binary files (images, PDFs, etc), copy the file path
        return "OK", 200 if clipboard.copy_file(filepath) else ("Error", 500)

    # Handle plain text submissions
    try:
        text_data = request.data.decode('utf-8')
    except Exception:
        return "Error", 400
    
    if text_data:
        return "OK", 200 if clipboard.copy_text(text_data) else ("Error", 500)
    
    return "No data", 400


@app.route('/get', methods=['GET'])
def sync_verso_iphone():
    """Send clipboard content to the iPhone."""
    # Check for images first
    image_data = clipboard.read_image()
    if image_data:
        return ResponseHandler.send_image(image_data)

    # Get text content
    text_content = clipboard.read_text()
    if not text_content:
        return "", 200

    # If it's a file path, send the file itself
    file_response = ResponseHandler.send_file_if_exists(text_content)
    if file_response:
        return file_response

    # Otherwise just send the text
    return ResponseHandler.send_text(text_content)


def main():
    """Start the ClipBridge server."""
    url = get_local_url(PORT)
    print_startup_qr(url, TOKEN)

    print("\n" + "═"*65)
    print("🎉 WELCOME TO CLIP BRIDGE!")
    print("═"*65)
    print("To permanently connect your phone, follow 3 simple steps:")
    print("  1. Open the Shortcuts app on your iPhone.")
    print("  2. Run the 'Receive from PC' (GET) or 'Send to PC' (POST) shortcut.")
    print("  3. The camera will open automatically: scan the QR Code.")
    print("\nDone! Your clipboards will be linked and you'll NEVER need to")
    print("scan this code again.")
    print("═"*65 + "\n")

    # Start the server
    app.run(host=HOST, port=PORT)


if __name__ == '__main__':
    main()