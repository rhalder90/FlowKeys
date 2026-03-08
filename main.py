# main.py — The entry point for FlowKeys.
# This file ties everything together: initializes the logger, player, and listener,
# then keeps the script running until the user presses Ctrl+C.

# === IMPORTS ===
import sys       # For reading command-line arguments and exiting
import os        # For working with the PID file
import signal    # For handling shutdown signals (SIGTERM, SIGINT)
import time      # For keeping the main loop alive
import subprocess  # For sending macOS notifications

import config          # Our settings
import logger_setup    # Sets up file + console logging
import player          # Sound playback
import listener        # Keyboard listener


def show_help():
    """
    Print usage information and exit.
    Called when the user runs: python3 main.py --help
    """
    # Print a helpful usage guide with all shortcuts and options.
    print(f"""
  FlowKeys v{config.VERSION}
  Mechanical keyboard sounds for your Mac.

  USAGE:
    python3 main.py                   Start FlowKeys
    python3 main.py --help            Show this help message
    python3 main.py --fix-permissions Reset and re-grant Accessibility permission

  SHORTCUTS (while running):
    Cmd+Ctrl+K    Toggle sound on/off
    Cmd+Ctrl+S    Switch between mechanical and soft sound

  SOUNDS:
    mechanical    Classic Cherry MX clicky sound
    soft          Quieter, softer tactile click

  LOGS:
    {config.LOG_DIR}/{config.LOG_FILE}

  STOP:
    Press Ctrl+C in the terminal, or close the terminal window.
""")
    # Exit after showing help — don't start the listener.
    sys.exit(0)


def fix_permissions():
    """
    Reset the macOS TCC (Transparency, Consent, Control) database for
    Accessibility permissions and open System Settings for re-granting.

    WHY THIS EXISTS:
    macOS TCC tracks Accessibility permissions by binary path + code signature hash.
    When Python updates (even a minor patch), the binary hash changes but the TCC
    entry keeps the old hash. macOS silently rejects the now-mismatched binary.
    Toggling the permission OFF/ON in System Settings doesn't help because it
    operates on the stale entry. The only fix is to RESET the TCC entry entirely
    so macOS re-evaluates the binary fresh.
    """
    import os

    # Get the ACTUAL binary that macOS sees (not the symlink or stub).
    # On macOS with official Python, python3 is a stub that exec's Python.app.
    actual_binary = None
    try:
        result = subprocess.run(
            ["ps", "-p", str(os.getpid()), "-o", "command="],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            candidate = result.stdout.strip().split()[0]
            if os.path.exists(candidate):
                actual_binary = candidate
    except Exception:
        pass

    if not actual_binary:
        actual_binary = os.path.realpath(sys.executable)

    print(f"\n  FlowKeys Permission Repair Tool")
    print(f"  ================================\n")
    print(f"  Python binary that macOS sees:")
    print(f"    {actual_binary}")
    print()

    # Step 1: Reset TCC entries that might be stale.
    # tccutil is a macOS command that manages the TCC database.
    # "reset Accessibility" clears ALL Accessibility entries for the given bundle ID.
    print("  Resetting Accessibility permissions...")
    tcc_targets = [
        "com.apple.Terminal",         # Terminal.app
        "com.googlecode.iterm2",      # iTerm2
        "com.microsoft.VSCode",       # VS Code
        "org.python.python",          # Official Python installer
    ]

    for bundle_id in tcc_targets:
        result = subprocess.run(
            ["tccutil", "reset", "Accessibility", bundle_id],
            capture_output=True, text=True
        )
        if "Successfully" in result.stdout:
            print(f"    ✓ Reset: {bundle_id}")

    # Step 2: Open System Settings to the Accessibility pane.
    print()
    print("  Opening System Settings → Accessibility...")
    subprocess.run([
        "open",
        "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
    ])

    # Step 3: Show instructions with the exact binary path.
    print(f"""
  NOW DO THIS:
  1. Click + → press Cmd+Shift+G
  2. Paste this exact path:
       {actual_binary}
  3. Press Enter → click Open → toggle ON
  4. Also add Terminal (Applications → Utilities → Terminal)
  5. QUIT Terminal (Cmd+Q) and reopen it
  6. Run: python3 ~/FlowKeys/main.py
""")
    sys.exit(0)


def check_already_running():
    """
    Check if another instance of FlowKeys is already running.
    Uses a PID file (~/.flowkeys.pid) to track the running process.
    Returns True if another instance is running, False if not.
    """
    # Check if the PID file exists.
    if os.path.exists(config.PID_FILE):
        try:
            # Read the PID (process ID) from the file.
            with open(config.PID_FILE, "r") as f:
                old_pid = int(f.read().strip())

            # Check if a process with that PID is still running.
            # os.kill with signal 0 doesn't actually kill anything —
            # it just checks if the process exists.
            os.kill(old_pid, 0)

            # If we get here, the process IS running.
            return True

        except (ValueError, ProcessLookupError, PermissionError):
            # ValueError: PID file contained garbage, not a number.
            # ProcessLookupError: The process is no longer running (stale PID file).
            # PermissionError: Process exists but we can't access it (unlikely).
            # In all cases, the old instance is gone — clean up the stale PID file.
            _remove_pid_file()

        except OSError:
            # Any other OS error — treat as "not running".
            _remove_pid_file()

    # No running instance found.
    return False


def _write_pid_file():
    """
    Write the current process ID to the PID file.
    This marks our process as the active FlowKeys instance.
    """
    try:
        # os.getpid() returns the process ID of this script.
        with open(config.PID_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception as e:
        # If we can't write the PID file, log it but continue.
        # FlowKeys can still work without it — just no duplicate protection.
        logger.warning("Could not write PID file: %s", e)


def _remove_pid_file():
    """
    Delete the PID file when FlowKeys is shutting down.
    """
    try:
        # Only try to remove if it exists.
        if os.path.exists(config.PID_FILE):
            os.remove(config.PID_FILE)
    except Exception:
        # If removal fails, it's not critical — ignore.
        pass


def _send_notification(title, message):
    """
    Send a macOS notification using osascript (AppleScript).
    Shows a brief popup in the top-right corner of the screen.
    """
    try:
        # Build the AppleScript command for a notification.
        script = f'display notification "{message}" with title "{title}"'

        # Run osascript as a subprocess. It talks to macOS's notification system.
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,  # Don't show osascript output in our terminal
            timeout=5             # Don't wait more than 5 seconds
        )
    except Exception:
        # If notifications fail (e.g., osascript not available), just skip.
        # This is a nice-to-have, not critical.
        pass


def _shutdown(signum=None, frame=None):
    """
    Cleanly shut down FlowKeys.
    Called when the user presses Ctrl+C or the process receives SIGTERM.
    """
    # Print a goodbye message.
    print("\n  FlowKeys shutting down...")

    # Stop the keyboard listener (stops its background thread).
    listener.stop()

    # Shut down the audio player (releases pygame resources).
    player.cleanup()

    # Remove the PID file so a new instance can start.
    _remove_pid_file()

    # Log the shutdown.
    logger.info("FlowKeys shut down cleanly")

    # Exit the program.
    sys.exit(0)


# === MAIN EXECUTION ===
# This block only runs when you execute this file directly (python3 main.py).
# It does NOT run when another file imports main.py.
if __name__ == "__main__":

    # --- Handle command-line flags ---
    # sys.argv is a list of command-line arguments.
    # sys.argv[0] is the script name, sys.argv[1] would be the first argument.
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        show_help()  # Print help and exit

    if len(sys.argv) > 1 and sys.argv[1] == "--fix-permissions":
        fix_permissions()  # Reset TCC and open System Settings

    # --- Set up logging ---
    # Initialize the logger first so all other modules can use it.
    logger = logger_setup.setup_logger()
    logger.info("FlowKeys v%s starting...", config.VERSION)

    # --- Check for duplicate instances ---
    if check_already_running():
        print(f"\n  FlowKeys is already running!")
        print(f"  To stop it, find its process or delete {config.PID_FILE}")
        print()
        sys.exit(1)  # Exit with error code 1

    # --- Write our PID file ---
    _write_pid_file()

    # --- Print startup banner ---
    # This is the first thing the user sees when FlowKeys starts.
    print()
    print(f"  ╔══════════════════════════════════════╗")
    print(f"  ║         FlowKeys v{config.VERSION}            ║")
    print(f"  ║   Mechanical keyboard sounds for Mac  ║")
    print(f"  ╚══════════════════════════════════════╝")
    print()
    print(f"  Sound:  {config.DEFAULT_SOUND}")
    print(f"  Volume: {int(config.VOLUME * 100)}%")
    print()
    print(f"  Shortcuts:")
    print(f"    Cmd+Ctrl+K  →  Toggle sound on/off")
    print(f"    Cmd+Ctrl+S  →  Switch sound (mechanical ↔ soft)")
    print()
    print(f"  Press Ctrl+C to quit.")
    print()

    # --- Initialize the sound player ---
    try:
        player.init()  # Loads both WAV files into RAM
    except Exception as e:
        # If the player fails, we can't continue.
        logger.error("Failed to initialize player: %s", e)
        print(f"\n  ERROR: Could not start audio player: {e}")
        print(f"  Make sure your sounds/ folder contains mechanical.wav and soft.wav")
        _remove_pid_file()
        sys.exit(1)

    # --- Check Accessibility permission BEFORE starting listener ---
    # Use the macOS AXIsProcessTrusted() API for an instant check.
    # This catches stale TCC entries immediately instead of waiting 3 seconds.
    if not listener.check_accessibility_trusted():
        real_path = os.path.realpath(sys.executable)
        logger.warning("Accessibility permission NOT granted for: %s", real_path)
        listener._print_permission_instructions()
        print("  TIP: Run this to auto-fix:")
        print("    python3 ~/FlowKeys/main.py --fix-permissions\n")
        # Don't exit — still start the listener in case the user grants
        # permission while FlowKeys is running (macOS picks it up live).

    # --- Start the keyboard listener ---
    listener.start()  # Begins listening in a background thread

    # --- Send macOS notification ---
    # Let the user know FlowKeys is active (shows in notification center).
    _send_notification("FlowKeys Active", f"Sound: {config.DEFAULT_SOUND} | Cmd+Ctrl+K to toggle")

    logger.info("FlowKeys is running. Sound: %s", config.DEFAULT_SOUND)

    # --- Register signal handlers ---
    # SIGTERM is sent when the system asks the process to stop (e.g., launchctl).
    signal.signal(signal.SIGTERM, _shutdown)

    # SIGINT is sent when the user presses Ctrl+C.
    signal.signal(signal.SIGINT, _shutdown)

    # --- Keep the script running ---
    # The keyboard listener runs in a background thread.
    # We need to keep the main thread alive, or the program would exit immediately.
    try:
        while True:
            time.sleep(1)  # Sleep 1 second, then loop. Low CPU usage.

    except KeyboardInterrupt:
        # This catches Ctrl+C if the signal handler doesn't fire first.
        _shutdown()
