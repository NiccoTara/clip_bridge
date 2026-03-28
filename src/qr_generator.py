import qrcode

def print_startup_qr(base_url, token):
    """Disegna il QR Code ASCII nel terminale."""
    full_url = f"{base_url}/?token={token}"
    
    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(full_url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)
    
    print("\nIn attesa di connessioni sicure dall'iPhone...\n")