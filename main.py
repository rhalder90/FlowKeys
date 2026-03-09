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
    if sys.platform == "win32":
        platform_name = "Windows"
        mod = "Win+Ctrl"
        extra_cmds = (
            "    FlowKeys.exe --enable-autostart  Start FlowKeys on login\n"
            "    FlowKeys.exe --disable-autostart Remove auto-start"
        )
    else:
        platform_name = "Mac"
        mod = "Cmd+Ctrl"
        extra_cmds = "    python3 main.py --fix-permissions Reset and re-grant Accessibility permission"

    print(f"""
  FlowKeys v{config.VERSION}
  Mechanical keyboard sounds for your {platform_name}.

  USAGE:
    python3 main.py                   Start FlowKeys
    python3 main.py --help            Show this help message
{extra_cmds}

  SHORTCUTS (while running):
    {mod}+K    Toggle sound on/off
    {mod}+S    Switch between mechanical and soft sound

  SOUNDS:
    mechanical    Classic Cherry MX clicky sound
    soft          Quieter, softer tactile click

  LOGS:
    {config.LOG_DIR}/{config.LOG_FILE}

  STOP:
    Press Ctrl+C in the terminal, or close the terminal window.
""")
    sys.exit(0)


def fix_permissions():
    """
    Reset the macOS TCC database for Accessibility permissions.
    On Windows, this is not needed — prints a message and exits.
    """
    if sys.platform == "win32":
        print("\n  Permission repair is only needed on macOS.")
        print("  On Windows, FlowKeys works without special permissions.\n")
        sys.exit(0)

    import os

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

    print("  Resetting Accessibility permissions...")
    tcc_targets = [
        "com.apple.Terminal",
        "com.googlecode.iterm2",
        "com.microsoft.VSCode",
        "org.python.python",
    ]

    for bundle_id in tcc_targets:
        result = subprocess.run(
            ["tccutil", "reset", "Accessibility", bundle_id],
            capture_output=True, text=True
        )
        if "Successfully" in result.stdout:
            print(f"    ✓ Reset: {bundle_id}")

    print()
    print("  Opening System Settings → Accessibility...")
    subprocess.run([
        "open",
        "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
    ])

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
    Send a desktop notification. Uses osascript on macOS.
    On Windows, notifications are skipped for now (no extra dependency needed).
    """
    if sys.platform == "win32":
        return  # Skip notifications on Windows (can add win10toast later)

    try:
        script = f'display notification "{message}" with title "{title}"'
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, timeout=5
        )
    except Exception:
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
        fix_permissions()  # Reset TCC and open System Settings (macOS only)

    # --- Windows auto-start flags ---
    if len(sys.argv) > 1 and sys.argv[1] == "--enable-autostart":
        if sys.platform != "win32":
            print("\n  On macOS, auto-start is managed by LaunchAgent (see install.command).\n")
            sys.exit(0)
        from windows import windows_autostart
        exe_path = sys.executable if getattr(sys, 'frozen', False) else os.path.abspath(__file__)
        windows_autostart.enable_autostart(exe_path)
        print("\n  FlowKeys will now start automatically when you log in.")
        print(f"  Shortcut created in: {windows_autostart.get_startup_folder()}\n")
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "--disable-autostart":
        if sys.platform != "win32":
            print("\n  On macOS, remove the LaunchAgent to disable auto-start.\n")
            sys.exit(0)
        from windows import windows_autostart
        windows_autostart.disable_autostart()
        print("\n  FlowKeys will no longer start automatically.\n")
        sys.exit(0)

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
    if sys.platform == "win32":
        platform_name = "Windows"
        mod = "Win+Ctrl"
    else:
        platform_name = "Mac"
        mod = "Cmd+Ctrl"

    print()
    print(f"  ======================================")
    print(f"         FlowKeys v{config.VERSION}")
    print(f"   Mechanical keyboard sounds for {platform_name}")
    print(f"  ======================================")
    print()
    print(f"  Sound:  {config.DEFAULT_SOUND}")
    print(f"  Volume: {int(config.VOLUME * 100)}%")
    print()
    print(f"  Shortcuts:")
    print(f"    {mod}+K  ->  Toggle sound on/off")
    print(f"    {mod}+S  ->  Switch sound (mechanical <-> soft)")
    print()
    print(f"  Press Ctrl+C to quit.")
    print()

    # On Windows, hint about auto-start if not set up yet.
    if sys.platform == "win32":
        try:
            from windows import windows_autostart
            if not windows_autostart.is_autostart_enabled():
                print(f"  TIP: Run 'FlowKeys.exe --enable-autostart' to start on login.\n")
        except ImportError:
            pass

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
    # Only relevant on macOS. Windows doesn't need Accessibility permission.
    if sys.platform == "darwin":
        if not listener.check_accessibility_trusted():
            real_path = os.path.realpath(sys.executable)
            logger.warning("Accessibility permission NOT granted for: %s", real_path)
            listener._print_permission_instructions()
            print("  TIP: Run this to auto-fix:")
            print("    python3 ~/FlowKeys/main.py --fix-permissions\n")

    # --- Start the keyboard listener ---
    listener.start()  # Begins listening in a background thread

    # --- Send desktop notification ---
    if sys.platform == "win32":
        _send_notification("FlowKeys Active", f"Sound: {config.DEFAULT_SOUND} | Win+Ctrl+K to toggle")
    else:
        _send_notification("FlowKeys Active", f"Sound: {config.DEFAULT_SOUND} | Cmd+Ctrl+K to toggle")

    logger.info("FlowKeys is running. Sound: %s", config.DEFAULT_SOUND)

    # --- Register signal handlers ---
    # SIGTERM is sent when the system asks the process to stop (e.g., launchctl).
    signal.signal(signal.SIGTERM, _shutdown)

    # SIGINT is sent when the user presses Ctrl+C.
    signal.signal(signal.SIGINT, _shutdown)

    # On Windows, SIGBREAK is sent when the console window is closed.
    if sys.platform == "win32" and hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, _shutdown)

    # --- Keep the script running ---
    # The keyboard listener runs in a background thread.
    # We need to keep the main thread alive, or the program would exit immediately.
    try:
        while True:
            time.sleep(1)  # Sleep 1 second, then loop. Low CPU usage.

    except KeyboardInterrupt:
        # This catches Ctrl+C if the signal handler doesn't fire first.
        _shutdown()
