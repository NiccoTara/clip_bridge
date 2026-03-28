# ClipBridge 🌉

Sync your iPhone clipboard with your Linux PC over Wi-Fi. Seamlessly copy text, files, and images between devices without touching a cable.

## Features ✨

- 📱 Real-time clipboard sync between iPhone and Linux
- 🔐 Secure token-based authentication
- 📤 Send text, files, and images from iPhone to PC
- 📥 Get clipboard content from PC to iPhone
- 🚀 Runs as a background daemon
- 🔄 Requires QR code scan only once

## Installation 🚀

### Quick Start (Recommended)

1. **Download the latest release** from [GitHub Releases](https://github.com/NiccoTara/clip_bridge/releases)

2. **Extract and install:**
   ```bash
   tar -xzf clipbridge-linux-x64.tar.gz
   cd clipbridge-linux-x64
   sudo ./install.sh
   ```

3. **Start ClipBridge:**
   ```bash
   clipbridge
   ```

4. **On your iPhone:**
   - Open the Shortcuts app
   - Create shortcuts using the endpoints shown in the terminal
   - Scan the QR code when prompted
   - Done! Your clipboards are now linked

### Build from Source (for developers)

If you want to build your own executable:

```bash
git clone https://github.com/NiccoTara/clip_bridge
cd clip_bridge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller clipbridge.spec
sudo ./install.sh
```

## Requirements

- **Linux** (Ubuntu/Debian recommended)
- **CopyQ** - Will be installed automatically by the installer
- **iPhone** with Shortcuts app

## How It Works

1. **First Run:** ClipBridge generates a random token and displays a QR code
2. **iOS Shortcut:** You create shortcuts on your iPhone that:
   - Send clipboard content to the PC via HTTP POST
   - Retrieve clipboard content from the PC via HTTP GET
3. **Running App:** ClipBridge listens for requests while it is running
4. **Token Auth:** Each request includes the token for security

## Architecture

```
iPhone (Shortcuts) ←→ [Wi-Fi] ←→ Linux PC (ClipBridge)
                        ↓
                    Flask Server
                        ↓
              CopyQ (System Clipboard)
```

## Configuration

Configuration files are stored in `~/.config/clipbridge/`:
- `clipbridge_token.txt` - Your unique auth token
- Downloaded files go to `~/Downloads/ClipBridge/`

## Troubleshooting

### CopyQ not found
Make sure CopyQ is running and accessible:
```bash
copyq --help
```

### Token reset
To reset your token and get a new QR code:
```bash
rm ~/.config/clipbridge/clipbridge_token.txt
clipbridge  # Will generate new token
```

### Check logs
If running in background with `nohup`:
```bash
tail -f /tmp/clipbridge.log
```

## License

MIT - See [LICENSE](LICENSE) file

## Contributing

Found a bug? Have a feature idea? Open an issue or submit a pull request!

---

Made with ❤️ by [Niccolò](https://github.com/NiccoTara)
