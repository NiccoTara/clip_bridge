import os
from pathlib import Path

# Server configuration
HOST = '0.0.0.0'
PORT = 5000

# Get the user's home directory
USER_HOME = str(Path.home())

# Token and config files live in ~/.config/clipbridge/
CONFIG_DIR = os.path.join(USER_HOME, '.config', 'clipbridge')
os.makedirs(CONFIG_DIR, exist_ok=True)

# Store the auth token here
TOKEN_FILE = os.path.join(CONFIG_DIR, 'clipbridge_token.txt')

# Downloaded files go to ~/Downloads/ClipBridge/
SAVE_DIR = os.path.join(USER_HOME, 'Downloads', 'ClipBridge')
os.makedirs(SAVE_DIR, exist_ok=True)