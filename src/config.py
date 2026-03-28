import os

# Configurazione
SAVE_DIR = os.path.expanduser('~/Downloads/iphone')
PORT = 5000
HOST = '0.0.0.0'

# Assicura che la directory esista
os.makedirs(SAVE_DIR, exist_ok=True)
