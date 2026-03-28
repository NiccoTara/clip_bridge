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

Use one of these two options.

### Option A — Prebuilt executable (when available in Releases)

1. Open [GitHub Releases](https://github.com/NiccoTara/clip_bridge/releases)
2. Download `clipbridge-linux-x64.tar.gz` (if present)
3. Run:
   ```bash
   cd ~/Downloads
   tar -xzf clipbridge-linux-x64.tar.gz
   cd clipbridge-linux-x64
   chmod +x install.sh
   sudo ./install.sh
   clipbridge
   ```

### Option B — Only tag source is available (`.zip` / `.tar.gz`)

If in the release page you only see **Source code (zip)** and **Source code (tar.gz)**, do this:

```bash
cd ~/Downloads
# If you downloaded the source tar.gz from Tags:
tar -xzf clip_bridge-*.tar.gz
cd clip_bridge-*

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install pyinstaller
pyinstaller clipbridge.spec
chmod +x install.sh
sudo ./install.sh
clipbridge
```

### First-time setup on iPhone

- Keep `clipbridge` running on your PC
- Open Shortcuts on iPhone
- Import your shortcuts (links below)
- Run one shortcut and scan the QR code once
- From then on, token auth is already configured

## iPhone Shortcut Links (paste your iCloud links here)

- Send to PC (POST): `PASTE_ICLOUD_LINK_HERE`
- Receive from PC (GET): `PASTE_ICLOUD_LINK_HERE`

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
