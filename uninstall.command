#!/bin/bash
# uninstall.command — Double-click this file to completely stop FlowKeys.
# This kills ALL FlowKeys processes, removes the LaunchAgent, and cleans up.
# It does NOT delete the FlowKeys folder or your sound files.

# === CONFIGURATION ===
# The name of the LaunchAgent plist file.
PLIST_NAME="com.flowkeys.agent.plist"

# The full path to the installed plist.
PLIST_PATH="$HOME/Library/LaunchAgents/$PLIST_NAME"

# The PID file that tracks the running FlowKeys process.
PID_FILE="$HOME/.flowkeys.pid"

# === PRETTY PRINTING ===
echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Uninstaller           ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

# === STEP 1: Kill ALL FlowKeys processes ===
echo "  [1/3] Stopping all FlowKeys processes..."

# Method 1: Kill using the PID file (the normal way).
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    kill "$PID" 2>/dev/null
    rm -f "$PID_FILE"
fi

# Method 2: Kill ANY process running main.py from the FlowKeys folder.
# This catches nohup processes, background processes, and anything else.
pkill -f "python3.*FlowKeys.*main.py" 2>/dev/null

# Method 3: Kill any process matching "FlowKeys" (catches the .app too).
pkill -f "FlowKeys/FlowKeys.app" 2>/dev/null
pkill -f "FlowKeys/main.py" 2>/dev/null

# Give processes a moment to die gracefully.
sleep 1

# Method 4: Force kill anything still alive (SIGKILL — cannot be ignored).
pkill -9 -f "python3.*FlowKeys.*main.py" 2>/dev/null
pkill -9 -f "FlowKeys/FlowKeys.app" 2>/dev/null
pkill -9 -f "FlowKeys/main.py" 2>/dev/null

# Clean up the PID file if it still exists.
rm -f "$PID_FILE"

echo "  ✓ All FlowKeys processes stopped"

# === STEP 2: Remove the LaunchAgent ===
echo ""
echo "  [2/3] Removing auto-start..."

if [ -f "$PLIST_PATH" ]; then
    # Unload the LaunchAgent (tells macOS to stop managing it).
    launchctl unload "$PLIST_PATH" 2>/dev/null

    # Delete the plist file.
    rm -f "$PLIST_PATH"

    echo "  ✓ Auto-start removed"
else
    echo "  ✓ Auto-start was not set up"
fi

# === STEP 3: Done ===
echo ""
echo "  [3/3] Cleanup complete!"
echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Fully Stopped         ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
echo "  ✓ All processes killed"
echo "  ✓ Auto-start removed"
echo "  ✓ Your FlowKeys folder and sound files are still intact"
echo ""
echo "  To reinstall later, just double-click install.command again."
echo ""

# Wait so the user can read the output.
read -p "  Press Enter to close this window..."
