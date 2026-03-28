# Development Guide

## Project Structure

```
clip_bridge/
├── clipbridge/
│   ├── __init__.py
│   ├── sync_clipboard.py      # Main Flask app and endpoints
│   ├── config.py              # Configuration constants
│   ├── auth.py                # Token validation
│   ├── clipboard_manager.py   # CopyQ interface
│   ├── file_handler.py        # File operations
│   ├── network_utils.py       # mDNS URL generation
│   ├── qr_generator.py        # QR code display
│   └── response_handler.py    # HTTP response formatting
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions build pipeline
├── clipbridge.spec            # PyInstaller configuration
├── requirements.txt           # Python dependencies
├── install.sh                 # Installer script for release/local build
├── LICENSE                    # MIT License
└── README.md                  # User documentation
```

## Development Setup

### 1. Clone and setup
```bash
git clone https://github.com/NiccoTara/clip_bridge
cd clip_bridge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Run in development mode
```bash
python3 -m clipbridge.sync_clipboard
```

The server will start on `http://localhost:5000` and print a QR code.

### 3. Testing with curl

Get clipboard:
```bash
curl "http://localhost:5000/get?token=your_token"
```

Send text:
```bash
curl -X POST \
  --data "Hello from PC" \
  "http://localhost:5000/post?token=your_token"
```

Send file:
```bash
curl -F "file=@path/to/file.txt" \
  "http://localhost:5000/post?token=your_token"
```

## Code Style

- Use descriptive variable names
- Add comments for non-obvious logic
- Keep functions small and focused
- Use type hints where helpful

## Adding Features

### New Endpoint Example

```python
@app.route('/status', methods=['GET'])
def get_status():
    """Get server status."""
    validate_request(request, TOKEN)
    return {"status": "ok", "token": TOKEN[:8] + "..."}, 200
```

### Testing New Changes

1. Run locally: `python3 -m clipbridge.sync_clipboard`
2. Test the endpoint
3. Build with PyInstaller: `pyinstaller clipbridge.spec`
4. Test the binary: `./dist/clipbridge`

## Debugging

### Enable Flask debug mode
Edit `sync_clipboard.py`:
```python
app.run(host=HOST, port=PORT, debug=True)
```

### View logs
```bash
tail -f /tmp/clipbridge.log
```

### Check what's listening on port 5000
```bash
lsof -i :5000
```

## Performance Tips

- CopyQ operations can be slow on large files
- Consider adding rate limiting for production
- Token negotiation happens on first run, not per request

## Known Limitations

- CopyQ must be running as a service
- No encryption (uses mDNS on local Wi-Fi only)
- Token is stored in plaintext (consider adding encryption)
- Binary size is ~50MB due to Python runtime

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Test thoroughly
5. Push and create a Pull Request

---

Questions? Open an issue!
