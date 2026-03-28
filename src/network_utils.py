import socket

def get_local_url(port):
    """Trova l'hostname mDNS (.local) del computer."""
    hostname = socket.gethostname()
    return f"http://{hostname}.local:{port}"