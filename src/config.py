import os

# Server configuration
HOST = '0.0.0.0'
PORT = 5000

# Directory where downloaded files are saved
SAVE_DIR = os.path.expanduser('~/Downloads/iphone')
os.makedirs(SAVE_DIR, exist_ok=True)
