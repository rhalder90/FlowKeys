#!/bin/bash
# install.command — Double-click this file to install FlowKeys.
#
# What this does:
#   1. Checks for Python 3
#   2. Installs Python dependencies (pynput, pygame-ce)
#   3. Copies FlowKeys to ~/FlowKeys (a safe, non-protected location)
#   4. Sets up auto-start on login (LaunchAgent)
#   5. Opens Accessibility settings with clear instructions
#
# WHY ~/FlowKeys?
#   macOS protects Desktop, Documents, and Downloads folders.
#   LaunchAgents can't read files from those locations without
#   Full Disk Access. ~/FlowKeys sits in the home directory root,
#   which has no such restriction. This makes auto-start "just work".

# === CONFIGURATION ===

# Get the folder where this install.command script lives.
# This is where the user downloaded/cloned FlowKeys.
SOURCE_DIR="$(cd "$(dirname "$0")" && pwd)"

# Where FlowKeys will actually live and run from.
# This is the CANONICAL install location — always the same, always safe.
INSTALL_DIR="$HOME/FlowKeys"

# The name of the LaunchAgent plist file.
PLIST_NAME="com.flowkeys.agent.plist"

# Where macOS looks for user-level LaunchAgents.
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

# Where FlowKeys writes its logs.
LOG_DIR="$HOME/Library/Logs/FlowKeys"

# The PID file that tracks the running process.
PID_FILE="$HOME/.flowkeys.pid"

# === PRETTY PRINTING ===
echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Installer             ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

# === STEP 1: Check if Python 3 is installed ===
echo "  [1/6] Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "  ✗ Python 3 is not installed!"
    echo ""
    echo "  To install Python 3:"
    echo "    1. Go to https://www.python.org/downloads/"
    echo "    2. Download the latest Python 3 for macOS"
    echo "    3. Run the installer"
    echo "    4. Then double-click install.command again"
    echo ""
    read -p "  Press Enter to exit..."
    exit 1
fi
echo "  ✓ Python 3 found: $(python3 --version)"

# === STEP 2: Install Python dependencies ===
echo ""
echo "  [2/6] Installing dependencies (pynput, pygame-ce)..."
pip3 install pynput pygame-ce --quiet 2>&1
if [ $? -eq 0 ]; then
    echo "  ✓ Dependencies installed"
else
    echo "  ✗ Failed to install dependencies"
    echo "  Try running manually: pip3 install pynput pygame-ce"
    read -p "  Press Enter to exit..."
    exit 1
fi

# === STEP 3: Stop any existing FlowKeys processes ===
echo ""
echo "  [3/6] Stopping any existing FlowKeys processes..."

# Kill using PID file if it exists.
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    kill "$PID" 2>/dev/null
    rm -f "$PID_FILE"
fi

# Kill any FlowKeys processes by pattern matching.
pkill -f "python3.*FlowKeys.*main.py" 2>/dev/null
pkill -f "FlowKeys/FlowKeys.app" 2>/dev/null
pkill -f "FlowKeys/main.py" 2>/dev/null
sleep 1

# Force kill anything still alive.
pkill -9 -f "python3.*FlowKeys.*main.py" 2>/dev/null
pkill -9 -f "FlowKeys/FlowKeys.app" 2>/dev/null
pkill -9 -f "FlowKeys/main.py" 2>/dev/null
rm -f "$PID_FILE"

# Unload old LaunchAgent if it exists.
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null

echo "  ✓ Clean slate"

# === STEP 4: Copy FlowKeys to ~/FlowKeys ===
echo ""
echo "  [4/6] Installing FlowKeys to ~/FlowKeys..."

# If ~/FlowKeys already exists, remove it so we get a clean copy.
# This ensures updates are always applied.
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
fi

# Copy the entire FlowKeys folder to ~/FlowKeys.
# We copy only the files needed to run — not .git or __pycache__.
mkdir -p "$INSTALL_DIR"
mkdir -p "$INSTALL_DIR/sounds"

# Copy core Python files.
cp "$SOURCE_DIR/main.py"         "$INSTALL_DIR/"
cp "$SOURCE_DIR/config.py"       "$INSTALL_DIR/"
cp "$SOURCE_DIR/player.py"       "$INSTALL_DIR/"
cp "$SOURCE_DIR/listener.py"     "$INSTALL_DIR/"
cp "$SOURCE_DIR/logger_setup.py" "$INSTALL_DIR/"

# Copy sound files.
cp "$SOURCE_DIR/sounds/"*.wav    "$INSTALL_DIR/sounds/"

# Copy the .app bundle (for Accessibility permission).
cp -R "$SOURCE_DIR/FlowKeys.app" "$INSTALL_DIR/"

# Make the .app executable.
chmod +x "$INSTALL_DIR/FlowKeys.app/Contents/MacOS/FlowKeys"

# Copy the plist template and uninstaller.
cp "$SOURCE_DIR/$PLIST_NAME"        "$INSTALL_DIR/"
cp "$SOURCE_DIR/uninstall.command"  "$INSTALL_DIR/"
chmod +x "$INSTALL_DIR/uninstall.command"

# Copy README for reference.
cp "$SOURCE_DIR/README.md"  "$INSTALL_DIR/" 2>/dev/null

# Remove macOS quarantine flags from all copied files.
# Without this, macOS Gatekeeper blocks the .app and uninstall.command
# with "can't be verified" warnings.
xattr -dr com.apple.quarantine "$INSTALL_DIR" 2>/dev/null

echo "  ✓ Installed to: $INSTALL_DIR"

# === STEP 5: Set up LaunchAgent (auto-start on login) ===
echo ""
echo "  [5/6] Setting up auto-start on login..."

# Create the LaunchAgents directory if it doesn't exist.
mkdir -p "$LAUNCH_AGENTS_DIR"

# Create the log directory.
mkdir -p "$LOG_DIR"

# Copy the plist template to the LaunchAgents directory.
cp "$INSTALL_DIR/$PLIST_NAME" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# Replace the __FLOWKEYS_PATH__ placeholder with ~/FlowKeys.
sed -i '' "s|__FLOWKEYS_PATH__|$INSTALL_DIR|g" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# Replace the __HOME__ placeholder with the user's home directory.
sed -i '' "s|__HOME__|$HOME|g" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# Load the new LaunchAgent. This also starts FlowKeys immediately.
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

if [ $? -eq 0 ]; then
    echo "  ✓ FlowKeys will auto-start on login"
else
    echo "  ⚠ Could not set up auto-start. You can run FlowKeys manually:"
    echo "    python3 $INSTALL_DIR/main.py"
fi

# === STEP 6: Accessibility Permission ===
echo ""
echo "  [6/6] Accessibility Permission"
echo ""
echo "  ┌─────────────────────────────────────────────────────────┐"
echo "  │  FlowKeys needs permission to detect your keypresses.  │"
echo "  │  Without this, it won't make any sound.                │"
echo "  │  You only need to do this ONCE.                        │"
echo "  └─────────────────────────────────────────────────────────┘"
echo ""
echo "  Opening System Settings now..."
echo ""

# Open Accessibility settings directly.
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"

# Wait a moment for Settings to open.
sleep 2

echo "  Follow these steps in the window that just opened:"
echo ""
echo "    Step 1. Click the + button (bottom-left)"
echo ""
echo "    Step 2. A file picker will open."
echo "            Go to your home folder, then select:"
echo ""
echo "            FlowKeys → FlowKeys.app"
echo ""
echo "            Full path: $INSTALL_DIR/FlowKeys.app"
echo ""
echo "    Step 3. Click Open"
echo ""
echo "    Step 4. Make sure the toggle next to FlowKeys is ON (blue)"
echo ""

# === DONE ===
echo "  ╔══════════════════════════════════════════════╗"
echo "  ║         Installation Complete!               ║"
echo "  ╚══════════════════════════════════════════════╝"
echo ""
echo "  FlowKeys is installed at: ~/FlowKeys"
echo ""
echo "  Shortcuts:"
echo "    Cmd+Ctrl+K  →  Toggle sound on/off"
echo "    Cmd+Ctrl+S  →  Switch sound (mechanical ↔ soft)"
echo ""
echo "  Logs: ~/Library/Logs/FlowKeys/"
echo ""
echo "  To uninstall: double-click ~/FlowKeys/uninstall.command"
echo ""

# Wait so the user can read the output.
read -p "  Press Enter to close this window..."
