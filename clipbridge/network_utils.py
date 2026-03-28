import socket

def get_local_url(port):
    """Build the mDNS URL for this machine."""
    hostname = socket.gethostname()
    return f"http://{hostname}.local:{port}"