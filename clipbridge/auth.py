import os
import secrets
from flask import abort

def get_or_create_token(filepath):
    """Load existing token or generate a new one if it doesn't exist."""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read().strip()
    else:
        # Generate a random 16-char hex token
        new_token = secrets.token_hex(8)
        with open(filepath, 'w') as f:
            f.write(new_token)
        return new_token

def validate_request(request, valid_token):
    """Verify the client provided the correct token."""
    client_token = request.args.get('token')
    if client_token != valid_token:
        abort(403)  # Deny access