#!/bin/bash
# install.command — Double-click this file to install FlowKeys.
# It installs Python dependencies, sets up auto-start on login,
# and reminds you to grant Accessibility permissions.

# === CONFIGURATION ===
# Get the folder where this script lives (the FlowKeys folder).
# This works no matter where the user downloaded FlowKeys to.
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# The name of the LaunchAgent plist file.
PLIST_NAME="com.flowkeys.agent.plist"

# Where macOS looks for user-level LaunchAgents.
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"

# Where FlowKeys writes its logs.
LOG_DIR="$HOME/Library/Logs/FlowKeys"

# === PRETTY PRINTING ===
echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Installer             ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

# === STEP 1: Check if Python 3 is installed ===
echo "  [1/5] Checking for Python 3..."
if ! command -v python3 &> /dev/null; then
    # python3 command not found — tell the user how to install it.
    echo ""
    echo "  ✗ Python 3 is not installed!"
    echo ""
    echo "  To install Python 3:"
    echo "    1. Go to https://www.python.org/downloads/"
    echo "    2. Download the latest Python 3 for macOS"
    echo "    3. Run the installer"
    echo "    4. Then double-click install.command again"
    echo ""
    # Wait for the user to read the message before the terminal closes.
    read -p "  Press Enter to exit..."
    exit 1
fi
echo "  ✓ Python 3 found: $(python3 --version)"

# === STEP 2: Install Python dependencies ===
echo ""
echo "  [2/5] Installing dependencies (pynput, pygame-ce)..."
# pip3 install will download and install the packages.
# --quiet reduces the output noise.
pip3 install pynput pygame-ce --quiet 2>&1
if [ $? -eq 0 ]; then
    echo "  ✓ Dependencies installed"
else
    echo "  ✗ Failed to install dependencies"
    echo "  Try running manually: pip3 install pynput pygame-ce"
    read -p "  Press Enter to exit..."
    exit 1
fi

# === STEP 3: Create log directory ===
echo ""
echo "  [3/5] Setting up log directory..."
# Create the log directory if it doesn't exist.
# -p means "create parent directories too" and "don't error if it already exists".
mkdir -p "$LOG_DIR"
echo "  ✓ Logs will be written to: $LOG_DIR"

# === STEP 4: Set up LaunchAgent (auto-start on login) ===
echo ""
echo "  [4/5] Setting up auto-start on login..."

# Create the LaunchAgents directory if it doesn't exist.
mkdir -p "$LAUNCH_AGENTS_DIR"

# Copy the plist template from the FlowKeys folder.
cp "$SCRIPT_DIR/$PLIST_NAME" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# Replace the __FLOWKEYS_PATH__ placeholder with the actual path.
# sed -i '' means "edit the file in place" on macOS.
sed -i '' "s|__FLOWKEYS_PATH__|$SCRIPT_DIR|g" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# Replace the __HOME__ placeholder with the user's home directory.
sed -i '' "s|__HOME__|$HOME|g" "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

# Unload the old LaunchAgent if it exists (ignore errors).
launchctl unload "$LAUNCH_AGENTS_DIR/$PLIST_NAME" 2>/dev/null

# Load the new LaunchAgent.
launchctl load "$LAUNCH_AGENTS_DIR/$PLIST_NAME"

if [ $? -eq 0 ]; then
    echo "  ✓ FlowKeys will auto-start on login"
else
    echo "  ⚠ Could not set up auto-start. You can run FlowKeys manually:"
    echo "    python3 $SCRIPT_DIR/main.py"
fi

# === STEP 5: Remind about Accessibility permissions ===
echo ""
echo "  [5/5] Accessibility Permission Required"
echo ""
echo "  ⚠ IMPORTANT: FlowKeys needs Accessibility permission to detect keypresses."
echo ""
echo "  To grant permission:"
echo "    1. Open System Settings (Apple menu → System Settings)"
echo "    2. Go to Privacy & Security → Accessibility"
echo "    3. Click the + button"
echo "    4. Add 'Terminal' (or your terminal app)"
echo "    5. Make sure the toggle is ON"
echo ""

# === DONE ===
echo "  ╔══════════════════════════════════════╗"
echo "  ║       Installation Complete!          ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
echo "  FlowKeys is now running!"
echo ""
echo "  Shortcuts:"
echo "    Cmd+Ctrl+K  →  Toggle sound on/off"
echo "    Cmd+Ctrl+S  →  Switch sound (mechanical ↔ soft)"
echo ""
echo "  ⚠ WARNING: If you move this folder, run install.command again!"
echo ""

# Wait so the user can read the output.
read -p "  Press Enter to close this window..."
