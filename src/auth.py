import os
import secrets
from flask import abort

def get_or_create_token(filepath):
    """Legge il token segreto o ne crea uno nuovo se non esiste."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read().strip()
    else:
        new_token = secrets.token_hex(8) # Genera password di 16 caratteri
        with open(filepath, 'w') as f:
            f.write(new_token)
        return new_token

def validate_request(request, valid_token):
    """Controlla se l'iPhone ha fornito il token giusto."""
    client_token = request.args.get('token')
    if client_token != valid_token:
        abort(403) # 403 Forbidden: Accesso negato!