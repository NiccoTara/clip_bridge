# ClipBridge

Copy on your iPhone, paste on your Linux PC. And vice versa. Over Wi-Fi, no cables, no cloud.

It works through Apple Shortcuts and a tiny server that runs on your PC. You pair the two devices once with a QR code, and from that point on it just works — every time you run a shortcut on your phone, the clipboard syncs instantly.

## What you need

- A Linux PC (Ubuntu/Debian tested, others should work)
- An iPhone with the Shortcuts app
- Both devices on the same Wi-Fi network

That's it. CopyQ (the clipboard backend) gets installed automatically.

---

## Setup

Two things to do: install ClipBridge on your PC, then add the shortcuts on your iPhone.

### On your PC

Download the latest release from [GitHub Releases](https://github.com/NiccoTara/clip_bridge/releases) and run:

```bash
tar -xzf clipbridge-linux-x64.tar.gz
cd clipbridge-linux-x64
sudo ./install.sh
```

The installer puts the binary in `/usr/local/bin/` and sets up autostart, so ClipBridge will launch automatically every time you log in.

Now start it for the first time:

```bash
clipbridge
```

You'll see a QR code in the terminal. **Keep it open** — you'll need it in a second.

### On your iPhone

1. Install these two shortcuts:
   - [Send to PC](https://www.icloud.com/shortcuts/22a58d38ae064287b900dc7b0d62820e) — copies your iPhone clipboard to the PC
   - [Receive from PC](https://www.icloud.com/shortcuts/509fb40a8a314146b082fbe267002a84) — copies the PC clipboard to your iPhone

   > If the iCloud links don't work for you, the `.shortcut` files are also available in the [`ios/`](ios/) folder of this repo. You can AirDrop them to your phone or open them from the Files app.

2. Open either shortcut and run it. The camera will open — **scan the QR code** on your PC's terminal.

3. Done. The shortcuts now know your PC's address and auth token. You won't need to scan again, even after restarting.

---

## Daily use

Once paired, it's simple:

- **iPhone → PC:** Copy something on your phone, run the "Send to PC" shortcut. It lands in your PC clipboard instantly.
- **PC → iPhone:** Copy something on your PC, run the "Receive from PC" shortcut on your phone. Done.

Works with text, images, files, URLs — anything you can copy.

> **Tip:** Add the shortcuts to your home screen or assign them to the Action Button / Back Tap for one-tap sync.

---

## How it works under the hood

```
iPhone (Shortcuts)  ←→  Wi-Fi  ←→  Linux PC (ClipBridge)
                          ↓
               Flask server on port 5000
                          ↓
                CopyQ (system clipboard)
```

ClipBridge is a small Flask server that exposes two endpoints:

- `POST /post` — receives text/files from the iPhone and writes them to the system clipboard via CopyQ
- `GET /get` — reads the current clipboard and sends it back to the iPhone

Every request must include the auth token (embedded in the shortcut URL after the QR scan). No token, no access.

---

## Files and paths

| What | Where |
|---|---|
| Auth token | `~/.config/clipbridge/clipbridge_token.txt` |
| Downloaded files | `~/Downloads/ClipBridge/` |
| Autostart entry | `~/.config/autostart/clipbridge.desktop` |
| Binary (after install) | `/usr/local/bin/clipbridge` |

---

## Troubleshooting

**Shortcut says it can't connect**
- Make sure ClipBridge is running on your PC (`clipbridge` in a terminal)
- Check that both devices are on the same Wi-Fi network
- Your PC's firewall might be blocking port 5000

**CopyQ errors**
- CopyQ must be running for clipboard access to work
- Test it: `copyq read 0` should print your last copied text

**Want to re-pair? (new QR code)**
```bash
rm ~/.config/clipbridge/clipbridge_token.txt
clipbridge
```
This generates a fresh token. You'll need to scan the QR code again from your phone.

**Disable autostart**
```bash
rm ~/.config/autostart/clipbridge.desktop
```

---

## Uninstall

If you want to remove everything cleanly:

### On your PC

```bash
# Remove the binary
sudo rm /usr/local/bin/clipbridge

# Remove autostart
rm ~/.config/autostart/clipbridge.desktop

# Remove config and auth token
rm -rf ~/.config/clipbridge/

# Remove downloaded files (optional)
rm -rf ~/Downloads/ClipBridge/
```

This does **not** uninstall CopyQ — you might be using it for other things. If you want to remove it too: `sudo apt remove copyq`.

### On your iPhone

1. Open the **Shortcuts** app
2. Swipe left on "Send to PC" and "Receive from PC" → tap **Delete**
3. Open the **Files** app and navigate to `On My iPhone` → `Shortcuts`
4. Delete the `ClipBridge` file config (if present) to remove any stored auth tokens and server addresses
5. That's it — all ClipBridge data is now removed from your phone

---

## License

MIT — see [LICENSE](LICENSE).

---

Made by [Niccolò](https://github.com/NiccoTara)
