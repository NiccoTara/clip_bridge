import os
from flask import Flask, request
import flask.cli
import logging
from config import SAVE_DIR, PORT, HOST, TOKEN_FILE
from file_handler import FileHandler
from clipboard_manager import ClipboardManager
from response_handler import ResponseHandler
from auth import get_or_create_token, validate_request
from network_utils import get_local_url
from qr_generator import print_startup_qr

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
    """Receive file or text from iPhone and sync to clipboard"""
    # Handle file upload
    if 'file' in request.files:
        f = request.files['file']
        filepath = file_handler.process_file(f)
        if not filepath:
            return "Error", 500
        
        # If it's a text file, extract and copy content
        text_content = file_handler.get_file_content_if_text(filepath)
        if text_content is not None:
            return "OK", 200 if clipboard.copy_text(text_content) else ("Error", 500)
        
        # Otherwise it's a binary file (image, PDF, etc)
        return "OK", 200 if clipboard.copy_file(filepath) else ("Error", 500)

    # Handle raw text data
    try:
        text_data = request.data.decode('utf-8')
    except Exception:
        return "Error", 400
    
    if text_data:
        return "OK", 200 if clipboard.copy_text(text_data) else ("Error", 500)
    
    return "No data", 400


@app.route('/get', methods=['GET'])
def sync_verso_iphone():
    """Send clipboard content to iPhone (image, file, or text)"""
    # Try to read image first - most direct path
    image_data = clipboard.read_image()
    if image_data:
        return ResponseHandler.send_image(image_data)

    # Fall back to text content
    text_content = clipboard.read_text()
    if not text_content:
        return "", 200

    # Check if text is a file path and serve the actual file
    file_response = ResponseHandler.send_file_if_exists(text_content)
    if file_response:
        return file_response

    # It's just plain text
    return ResponseHandler.send_text(text_content)


if __name__ == '__main__':

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

    
    # Run server
    app.run(host=HOST, port=PORT)