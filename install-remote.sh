#!/bin/bash
# install-remote.sh — One-line installer for FlowKeys.
#
# Usage (paste this in Terminal):
#   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/install-remote.sh)"
#
# This script:
#   1. Downloads FlowKeys from GitHub
#   2. Runs the full installer
#   3. Cleans up the download
#
# Why this exists:
#   macOS Gatekeeper blocks downloaded .command files with a
#   "can't be verified" warning. This curl-based approach bypasses
#   Gatekeeper entirely because no file is ever "downloaded" through
#   a browser — it's fetched directly by Terminal.

set -e

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Quick Installer       ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

# --- Step 1: Check for Python 3 ---
echo "  Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "  ✗ Python 3 is not installed!"
    echo ""
    echo "  To install Python 3:"
    echo "    1. Go to https://www.python.org/downloads/"
    echo "    2. Download the latest Python 3 for macOS"
    echo "    3. Run the installer"
    echo "    4. Then run this command again"
    echo ""
    exit 1
fi
echo "  ✓ Python 3 found: $(python3 --version)"

# --- Step 2: Download FlowKeys from GitHub ---
echo ""
echo "  Downloading FlowKeys..."

# Use a temp directory for the download.
TEMP_DIR=$(mktemp -d)
ARCHIVE_URL="https://github.com/rhalder90/FlowKeys/archive/refs/heads/main.zip"

# Download the zip quietly.
curl -fsSL "$ARCHIVE_URL" -o "$TEMP_DIR/FlowKeys.zip"

# Unzip it.
unzip -q "$TEMP_DIR/FlowKeys.zip" -d "$TEMP_DIR"

echo "  ✓ Downloaded"

# --- Step 3: Run the real installer ---
# The unzipped folder is FlowKeys-main/.
# We source the install logic directly instead of running install.command
# (which would also get quarantined on some systems).

SOURCE_DIR="$TEMP_DIR/FlowKeys-main"
INSTALL_DIR="$HOME/FlowKeys"
PLIST_NAME="com.flowkeys.agent.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
LOG_DIR="$HOME/Library/Logs/FlowKeys"
PID_FILE="$HOME/.flowkeys.pid"

# --- Install dependencies ---
echo ""
echo "  Installing dependencies..."
pip3 install pynput pygame-ce --quiet 2>&1
echo "  ✓ Dependencies installed"

# --- Stop existing FlowKeys ---
echo ""
echo "  Stopping any existing FlowKeys..."
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    kill "$PID" 2>/dev/null || true
    rm -f "$PID_FILE"
fi
pkill -f "python3.*FlowKeys.*main.py" 2>/dev/null || true
pkill -f "FlowKeys/FlowKeys.app" 2>/dev/null || true
pkill -f "FlowKeys/main.py" 2>/dev/null || true
sleep 1
pkill -9 -f "python3.*FlowKeys.*main.py" 2>/dev/null || true
pkill -9 -f "FlowKeys/FlowKeys.app" 2>/dev/null || true
pkill -9 -f "FlowKeys/main.py" 2>/dev/null || true
rm -f "$PID_FILE"
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null || true
echo "  ✓ Clean slate"

# --- Copy to ~/FlowKeys ---
echo ""
echo "  Installing to ~/FlowKeys..."
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/sounds"

cp "$SOURCE_DIR/main.py"         "$INSTALL_DIR/"
cp "$SOURCE_DIR/config.py"       "$INSTALL_DIR/"
cp "$SOURCE_DIR/player.py"       "$INSTALL_DIR/"
cp "$SOURCE_DIR/listener.py"     "$INSTALL_DIR/"
cp "$SOURCE_DIR/logger_setup.py" "$INSTALL_DIR/"
cp "$SOURCE_DIR/sounds/"*.wav    "$INSTALL_DIR/sounds/"
cp -R "$SOURCE_DIR/FlowKeys.app" "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/FlowKeys.app/Contents/MacOS/FlowKeys"
cp "$SOURCE_DIR/$PLIST_NAME"        "$INSTALL_DIR/"
cp "$SOURCE_DIR/uninstall.command"  "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/uninstall.command"
cp "$SOURCE_DIR/README.md"  "$INSTALL_DIR/" 2>/dev/null || true

# Remove quarantine flags.
xattr -dr com.apple.quarantine "$INSTALL_DIR" 2>/dev/null || true

echo "  ✓ Installed to ~/FlowKeys"

# --- Set up LaunchAgent ---
echo ""
echo "  Setting up auto-start..."
mkdir -p "$LAUNCH_AGENTS_DIR"
mkdir -p "$LOG_DIR"
cp "$INSTALL_DIR/$PLIST_NAME" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
sed -i '' "s|__FLOWKEYS_PATH__|$INSTALL_DIR|g" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
sed -i '' "s|__HOME__|$HOME|g" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME"
echo "  ✓ FlowKeys will auto-start on login"

# --- Clean up temp download ---
rm -rf "$TEMP_DIR"

# --- Accessibility Permission ---
echo ""
echo "  ┌─────────────────────────────────────────────────────────┐"
echo "  │  FlowKeys needs permission to detect your keypresses.  │"
echo "  │  Without this, it won't make any sound.                │"
echo "  │  You only need to do this ONCE.                        │"
echo "  └─────────────────────────────────────────────────────────┘"
echo ""
echo "  Opening System Settings now..."
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
sleep 2
echo ""
echo "    1. Click the + button"
echo "    2. Go to: home folder → FlowKeys → FlowKeys.app"
echo "       Full path: $INSTALL_DIR/FlowKeys.app"
echo "    3. Click Open"
echo "    4. Make sure the toggle is ON (blue)"
echo ""

# --- Done ---
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║         Installation Complete!               ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""
echo "  Shortcuts:"
echo "    Cmd+Ctrl+K  →  Toggle sound on/off"
echo "    Cmd+Ctrl+S  →  Switch sound (mechanical ↔ soft)"
echo ""
echo "  To uninstall: double-click ~/FlowKeys/uninstall.command"
echo ""
