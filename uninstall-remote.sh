#!/bin/bash
# uninstall-remote.sh — One-line uninstaller for FlowKeys.
#
# Usage (paste this in Terminal):
#   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/uninstall-remote.sh)"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Uninstaller           ║"
echo "  ╚══════════════════════════════════════╝"
echo ""

PLIST_PATH="$HOME/Library/LaunchAgents/com.flowkeys.agent.plist"
PID_FILE="$HOME/.flowkeys.pid"
INSTALL_DIR="$HOME/FlowKeys"

# --- Stop all FlowKeys processes ---
echo "  [1/3] Stopping FlowKeys..."
if [ -f "$PID_FILE" ]; then
    kill "$(cat "$PID_FILE")" 2>/dev/null || true
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
echo "  ✓ Stopped"

# --- Remove auto-start ---
echo ""
echo "  [2/3] Removing auto-start..."
if [ -f "$PLIST_PATH" ]; then
    launchctl unload "$PLIST_PATH" 2>/dev/null || true
    rm -f "$PLIST_PATH"
fi
echo "  ✓ Auto-start removed"

# --- Remove installed files ---
echo ""
echo "  [3/3] Removing ~/FlowKeys..."
if [ -d "$INSTALL_DIR" ]; then
    rm -rf "$INSTALL_DIR"
fi
echo "  ✓ Removed"

echo ""
echo "  ╔══════════════════════════════════════╗"
echo "  ║       FlowKeys Fully Removed         ║"
echo "  ╚══════════════════════════════════════╝"
echo ""
echo "  To reinstall:"
echo '  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/install-remote.sh)"'
echo ""
