from flask import Flask, request
from config import SAVE_DIR, PORT, HOST
from file_handler import FileHandler
from clipboard_manager import ClipboardManager

app = Flask(__name__)
file_handler = FileHandler(SAVE_DIR)
clipboard = ClipboardManager()


@app.route('/sync', methods=['POST'])
def sync_da_iphone():
    """Sincronizza file o testo da iPhone alla clipboard"""
    # CASO 1: FILE / IMMAGINE / TESTO COME FILE
    if 'file' in request.files:
        f = request.files['file']
        filepath = file_handler.process_file(f)
        if not filepath:
            return "Errore salvataggio file", 500
        
        # Se è un file di testo, copia il contenuto
        text_content = file_handler.get_file_content_if_text(filepath)
        if text_content is not None:
            if clipboard.copy_text(text_content):
                return "OK", 200
            else:
                return "Errore", 500
        
        # Altrimenti è un file binario/immagine
        if clipboard.copy_file(filepath):
            return "OK", 200
        else:
            return "Errore", 500

    # CASO 2: TESTO COME RAW DATA
    testo_ricevuto = request.data.decode('utf-8')
    if testo_ricevuto:
        if clipboard.copy_text(testo_ricevuto):
            return "OK", 200
        else:
            return "Errore", 500
    
    return "Nessun dato", 400


@app.route('/get', methods=['GET'])
def sync_verso_iphone():
    """Recupera il contenuto della clipboard"""
    content = clipboard.get_clipboard()
    return content if content else "", 200


if __name__ == '__main__':
    app.run(host=HOST, port=PORT)