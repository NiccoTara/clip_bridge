import qrcode

def print_startup_qr(base_url, token):
    """Generate and display the QR code."""
    full_url = f"{base_url}/?token={token}"
    
    qr = qrcode.QRCode(version=1, box_size=1, border=2)
    qr.add_data(full_url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)
    
    print("\nWaiting for iPhone connections...\n")