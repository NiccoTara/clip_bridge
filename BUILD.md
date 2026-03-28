# Building ClipBridge

If you want to build the binary locally or contribute to ClipBridge, follow these steps.

## Prerequisites

- Python 3.8+
- pip
- git

## Build Steps

### 1. Clone the repository
```bash
git clone https://github.com/NiccoTara/clip_bridge
cd clip_bridge
```

### 2. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### 4. Build with PyInstaller
```bash
pyinstaller clipbridge.spec
```

The binary will be created in `dist/clipbridge`

### 5. Test the binary
```bash
./dist/clipbridge
```

You should see the QR code and startup message.

## Creating a Release

1. Commit changes: `git commit -am "Release v1.0.1"`
2. Tag the release: `git tag v1.0.1`
3. Push: `git push && git push --tags`

GitHub Actions will automatically:
- Build the binary
- Create a release bundle (`clipbridge-linux-x64.tar.gz`)
- Upload bundle + SHA256 checksum
- Generate SHA256 checksum

## Package Size

The compiled binary is typically 40-50 MB and includes:
- Python runtime
- Flask and dependencies
- All required libraries

## Troubleshooting

### PyInstaller fails with "module not found"
This usually means a dependency is missing from the `hiddenimports` in `clipbridge.spec`. Add it and rebuild.

### Binary doesn't start
Run it with verbose output:
```bash
./dist/clipbridge --verbose
```

### Check what's bundled
```bash
tar -tzf clipbridge-linux-x64.tar.gz | head -20
```
