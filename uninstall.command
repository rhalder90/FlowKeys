#!/bin/bash
# uninstall.command — Double-click this file to remove FlowKeys auto-start.
# This stops FlowKeys and removes the LaunchAgent so it won't start on login.
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

# === STEP 1: Stop the running FlowKeys process ===
echo "  [1/3] Stopping FlowKeys..."

# Check if the PID file exists and kill the process.
if [ -f "$PID_FILE" ]; then
    # Read the process ID from the file.
    PID=$(cat "$PID_FILE")

    # Try to gracefully stop the process (SIGTERM).
    kill "$PID" 2>/dev/null

    if [ $? -eq 0 ]; then
        echo "  ✓ Stopped FlowKeys (PID: $PID)"
    else
        echo "  ✓ FlowKeys was not running"
    fi

    # Remove the PID file.
    rm -f "$PID_FILE"
else
    echo "  ✓ FlowKeys was not running"
fi

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
echo "  FlowKeys has been stopped and auto-start has been removed."
echo "  Your FlowKeys folder and sound files are still intact."
echo ""
echo "  To reinstall later, just double-click install.command again."
echo ""

# Wait so the user can read the output.
read -p "  Press Enter to close this window..."
