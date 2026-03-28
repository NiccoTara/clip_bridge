#!/bin/bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     ClipBridge Installer v1.0      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════╝${NC}\n"

# Check if running as root (needed for apt and /usr/local/bin)
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}✗ This script must be run as root${NC}"
    echo "   Try: sudo ./install.sh"
    exit 1
fi

# Check for CopyQ
echo -e "${YELLOW}→${NC} Checking for CopyQ clipboard manager..."
if ! command -v copyq &> /dev/null; then
    echo -e "${YELLOW}✗ CopyQ not found. Installing...${NC}"
    apt-get update
    apt-get install -y copyq-server copyq-noX11
    if command -v copyq &> /dev/null; then
        echo -e "${GREEN}✓ CopyQ installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install CopyQ${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ CopyQ found${NC}"
fi

# Get the directory where the install script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BINARY="${SCRIPT_DIR}/clipbridge"

# Fallback for local dev builds run from repo root
if [ ! -f "$BINARY" ] && [ -f "${SCRIPT_DIR}/dist/clipbridge" ]; then
    BINARY="${SCRIPT_DIR}/dist/clipbridge"
fi

# Check if binary exists
if [ ! -f "$BINARY" ]; then
    echo -e "${RED}✗ Binary not found at ${BINARY}${NC}"
    echo "   Expected 'clipbridge' next to install.sh"
    echo "   If building locally, run: pyinstaller clipbridge.spec"
    exit 1
fi

# Copy binary to /usr/local/bin
echo -e "${YELLOW}→${NC} Installing ClipBridge binary..."
cp "$BINARY" /usr/local/bin/clipbridge
chmod +x /usr/local/bin/clipbridge
echo -e "${GREEN}✓ Binary installed to /usr/local/bin/clipbridge${NC}"

# Create config directory if needed
CONFIG_DIR="$HOME/.config/clipbridge"
mkdir -p "$CONFIG_DIR"
chmod 700 "$CONFIG_DIR"

echo ""
echo -e "${GREEN}╔════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Installation Complete! 🎉        ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Start ClipBridge: clipbridge"
echo "  2. Scan the QR code on your iPhone"
echo "  3. Keep the terminal open while using it"
echo "     (or run in background: nohup clipbridge >/tmp/clipbridge.log 2>&1 & )"
echo ""
echo "For more info: https://github.com/NiccoTara/clip_bridge"
