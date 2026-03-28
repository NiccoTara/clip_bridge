from flask import Flask, request
from werkzeug.utils import secure_filename
import subprocess
import os

app = Flask(__name__)

SAVE_DIR = os.path.expanduser('~/Downloads/iphone')
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/sync', methods=['POST'])
def sync_da_iphone():
    print("\n--- NUOVA RICHIESTA RICEVUTA ---")
    
    # CASO 1: FILE / IMMAGINE
    if 'file' in request.files:
        f = request.files['file']
        print(f"[DEBUG] Ricevuto file: {f.filename}")
        
        if f.filename:
            filename = secure_filename(f.filename)
            filepath = os.path.join(SAVE_DIR, filename)
            f.save(filepath)
            print(f"[DEBUG] File salvato in: {filepath} ({os.path.getsize(filepath)} bytes)")
            
            # Se è HEIC lo convertiamo in JPG (lasciamo questo comodo fallback)
            if filename.lower().endswith('.heic'):
                jpg_filepath = os.path.join(SAVE_DIR, filename.rsplit('.', 1)[0] + '.jpg')
                try:
                    subprocess.run(['heif-convert', filepath, jpg_filepath], capture_output=True, check=True)
                    os.remove(filepath)
                    filepath = jpg_filepath
                    print("[DEBUG] Convertito HEIC in JPG")
                except Exception as e:
                    print(f"[ERRORE] Conversione HEIC: {e}")
                    return "Errore HEIC", 500

            # --- LA NUOVA MAGIA (Zero lag, zero freeze) ---
            try:
                # Otteniamo il percorso assoluto formattato come URI
                file_uri = f"file://{os.path.abspath(filepath)}"
                
                # Diciamo a CopyQ di comportarsi come un File Manager
                # Passiamo text/uri-list per le GUI, e text/plain per il terminale
                subprocess.run([
                    'copyq', 
                    'write', 
                    'text/uri-list', file_uri, 
                    'text/plain', filepath
                ], check=True)
                
                subprocess.run(['copyq', 'select', '0'], check=True)
                
                print("[SUCCESS] URI Immagine copiato in CopyQ! (0 lag)")
                return "Immagine copiata", 200
            except Exception as e:
                print(f"[ERRORE] Scrittura CopyQ: {e}")
                return "Errore CopyQ", 500

    # CASO 2: TESTO
    testo_ricevuto = request.data.decode('utf-8')
    print(f"[DEBUG] Testo ricevuto (Lunghezza: {len(testo_ricevuto)} caratteri)")
    
    if testo_ricevuto:
        try:
            subprocess.run(['copyq', 'add', testo_ricevuto], capture_output=True, check=True)
            subprocess.run(['copyq', 'copy', testo_ricevuto], capture_output=True, check=True)
            print("[SUCCESS] Testo copiato in CopyQ!")
            return "Testo copiato", 200
        except Exception as e:
            print(f"[ERRORE] Aggiunta testo CopyQ: {e}")
            return "Errore CopyQ", 500
            
    print("[WARNING] Nessun dato valido ricevuto!")
    return "Nessun dato", 400

@app.route('/get', methods=['GET'])
def sync_verso_iphone():
    try:
        result = subprocess.run(['copyq', 'clipboard'], capture_output=True, text=True, check=True)
        return result.stdout, 200
    except:
        return "ERR", 500

if __name__ == '__main__':
    print("🚀 Server in ascolto sulla porta 5000...")
    app.run(host='0.0.0.0', port=5000)