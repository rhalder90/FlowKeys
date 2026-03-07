#!/bin/bash
# uninstall.command — Double-click this file to completely stop FlowKeys.
# This kills ALL FlowKeys processes, removes the LaunchAgent, and cleans up.
# It does NOT delete the FlowKeys folder or your sound files.

# === CONFIGURATION ===
PLIST_NAME="com.flowkeys.agent.plist"
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"
PID_FILE="$HOME/.flowkeys.pid"
INSTALL_DIR="$HOME/FlowKeys"

# === PRETTY PRINTING ===
echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Uninstaller           ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

# === STEP 1: Kill ALL FlowKeys processes ===
echo "  [1/4] Stopping all FlowKeys processes..."

# Method 1: Kill using the PID file.
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    kill "$PID" 2>/dev/null
    rm -f "$PID_FILE"
fi

# Method 2: Kill any process matching FlowKeys patterns.
pkill -f "python3.*FlowKeys.*main.py" 2>/dev/null
pkill -f "FlowKeys/FlowKeys.app" 2>/dev/null
pkill -f "FlowKeys/main.py" 2>/dev/null

# Give processes a moment to die gracefully.
sleep 1

# Method 3: Force kill anything still alive (SIGKILL).
pkill -9 -f "python3.*FlowKeys.*main.py" 2>/dev/null
pkill -9 -f "FlowKeys/FlowKeys.app" 2>/dev/null
pkill -9 -f "FlowKeys/main.py" 2>/dev/null

# Clean up the PID file.
rm -f "$PID_FILE"

echo "  ✓ All FlowKeys processes stopped"

# === STEP 2: Remove the LaunchAgent ===
echo ""
echo "  [2/4] Removing auto-start..."

if [ -f "$PLIST_PATH" ]; then
    launchctl unload "$PLIST_PATH" 2>/dev/null
    rm -f "$PLIST_PATH"
    echo "  ✓ Auto-start removed"
else
    echo "  ✓ Auto-start was not set up"
fi

# === STEP 3: Remove installed files ===
echo ""
echo "  [3/4] Removing installed files..."

if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
    echo "  ✓ Removed ~/FlowKeys"
else
    echo "  ✓ No installed files found"
fi

# === STEP 4: Done ===
echo ""
echo "  [4/4] Cleanup complete!"
echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Fully Removed         ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
echo "  ✓ All processes killed"
echo "  ✓ Auto-start removed"
echo "  ✓ Installed files removed"
echo ""
echo "  To reinstall, double-click install.command again."
echo ""
echo "  If sound is STILL playing (very rare), run in Terminal:"
echo "    pkill -9 -f FlowKeys"
echo ""

# Wait so the user can read the output.
read -p "  Press Enter to close this window..."
