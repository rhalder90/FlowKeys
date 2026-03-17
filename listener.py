# listener.py — Listens for every keypress on the entire system.
# Uses pynput to create a global keyboard hook that runs in a background thread.
# Detects the toggle shortcut (Cmd+Ctrl+K) and switch shortcut (Cmd+Ctrl+S).

# === IMPORTS ===
import sys        # For getting the actual python executable path and detecting OS
import threading  # For running the accessibility check timer

# ctypes is only needed on macOS for calling AXIsProcessTrusted()
if sys.platform == "darwin":
    import ctypes
    import ctypes.util
import time       # For tracking last key event time
import logging    # For recording events
from pynput import keyboard  # The library that captures global keypresses
import config   # Our settings: shortcut keys, sound order
import player   # Our sound player: play(), set_sound(), etc.

# Get the FlowKeys logger.
logger = logging.getLogger("FlowKeys")

# === MODULE-LEVEL VARIABLES ===

# The pynput Listener object. Runs in its own thread.
_listener = None

# Is sound currently enabled? Starts as True (on).
_enabled = True

# A set that tracks which modifier keys are currently held down.
# Example: when you hold Cmd+Ctrl, this becomes {"cmd", "ctrl"}.
_pressed_modifiers = set()

# A flag that tracks whether we've received at least one key event.
# Used to detect if Accessibility permissions are missing.
_received_key_event = False

# Timestamp of the last key event. Used to detect sleep/wake stalls.
_last_key_time = 0.0


def _print_shortcuts():
    """
    Print the keyboard shortcuts to the terminal as a reminder.
    Called every time the user toggles or switches sounds.
    """
    # Print a blank line for visual separation.
    print()

    # Show platform-appropriate shortcuts.
    if sys.platform == "win32":
        mod = "Win+Ctrl"
    else:
        mod = "Cmd+Ctrl"
    print("  Shortcuts:")
    print(f"    {mod}+K  →  Toggle sound on/off")
    print(f"    {mod}+S  →  Switch sound (mechanical ↔ soft)")
    print()


def _on_press(key):
    """
    Called every time ANY key is pressed anywhere on the system.
    This is the heart of FlowKeys — it decides what happens on each keypress.
    """
    # We need to modify these module-level variables.
    global _enabled, _received_key_event, _last_key_time

    # Mark that we received a key event (used for accessibility check).
    _received_key_event = True
    _last_key_time = time.time()

    # === STEP 1: Track modifier keys ===
    # Modifier keys (Cmd, Ctrl, Alt, Shift) are special — pynput gives them
    # as Key objects, not characters. We need to track them separately.
    try:
        # Check if the pressed key is the Command key (⌘).
        if key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
            _pressed_modifiers.add("cmd")  # Add "cmd" to our tracking set
            return  # Don't play a sound for modifier keys

        # Check if the pressed key is the Control key (⌃).
        if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            _pressed_modifiers.add("ctrl")  # Add "ctrl" to our tracking set
            return  # Don't play a sound for modifier keys

    except AttributeError:
        # Some special keys might cause AttributeError — ignore and continue.
        pass

    # === STEP 2: Check for keyboard shortcuts ===
    # Get the character of the pressed key (lowercase).
    # Regular keys have a .char attribute; special keys (Enter, Backspace) don't.
    try:
        # Try to get the character (works for letters, numbers, symbols).
        key_char = key.char.lower() if key.char else None
    except AttributeError:
        # Special keys (Enter, Backspace, Arrow keys, etc.) don't have .char.
        key_char = None

    # --- Toggle shortcut: Cmd+Ctrl+K ---
    # Check if the right modifiers are held AND the right key was pressed.
    if (key_char == config.TOGGLE_COMBO_KEY and
            config.TOGGLE_COMBO_MODIFIERS.issubset(_pressed_modifiers)):

        # Flip the enabled flag (True becomes False, False becomes True).
        _enabled = not _enabled

        # Build a status message.
        status = "ON" if _enabled else "OFF"
        sound_name = player.get_current_sound_name()

        # Print and log the new status.
        print(f"\n  ✦ FlowKeys: {status}")
        if _enabled:
            print(f"    Sound: {sound_name}")
        logger.info("FlowKeys toggled %s (sound: %s)", status, sound_name)

        # Remind the user of all shortcuts.
        _print_shortcuts()

        return  # Don't play a sound for the shortcut key itself

    # --- Switch sound shortcut: Cmd+Ctrl+S ---
    if (key_char == config.SWITCH_COMBO_KEY and
            config.SWITCH_COMBO_MODIFIERS.issubset(_pressed_modifiers)):

        # Find the current sound's position in the order list.
        current = player.get_current_sound_name()
        order = config.SOUND_ORDER

        # Calculate the next sound index (wraps around to 0 at the end).
        current_index = order.index(current) if current in order else 0
        next_index = (current_index + 1) % len(order)  # Modulo wraps around
        next_sound = order[next_index]

        # Switch to the next sound.
        player.set_sound(next_sound)

        # Print and log the switch.
        print(f"\n  ✦ Switched to: {next_sound}")
        logger.info("Sound switched to: %s", next_sound)

        # Remind the user of all shortcuts.
        _print_shortcuts()

        return  # Don't play a sound for the shortcut key itself

    # === STEP 3: Play sound on normal keypress ===
    # If sound is enabled, play the click sound.
    if _enabled:
        player.play()


def _on_release(key):
    """
    Called every time ANY key is released.
    We use this to track when modifier keys are let go.
    """
    try:
        # If Command key was released, remove "cmd" from our tracking set.
        if key == keyboard.Key.cmd or key == keyboard.Key.cmd_r:
            _pressed_modifiers.discard("cmd")  # discard won't error if not present

        # If Control key was released, remove "ctrl" from our tracking set.
        if key == keyboard.Key.ctrl or key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            _pressed_modifiers.discard("ctrl")  # discard won't error if not present

    except AttributeError:
        # Some special keys might cause AttributeError — ignore.
        pass


def _get_python_binary_path():
    """
    Get the ACTUAL binary that the OS sees running this process.
    On Windows, sys.executable is reliable. On macOS, python3 is a launcher
    stub that exec's Python.app — we use `ps` to find the real binary.
    """
    import os

    # On Windows, sys.executable is the actual binary. No symlink games.
    if sys.platform == "win32":
        return sys.executable

    # macOS: TCC prefers .app bundles over raw binaries.
    # Walk up from the resolved binary to find the Python.app bundle.
    real_bin = os.path.realpath(sys.executable)
    parts = real_bin.split(os.sep)
    for i, part in enumerate(parts):
        if part.endswith(".app"):
            app_path = os.sep + os.path.join(*parts[1:i+1])
            if os.path.exists(app_path):
                return app_path

    # Fallback: construct from framework path
    framework_base = os.path.dirname(os.path.dirname(real_bin))
    candidate = os.path.join(framework_base, "Resources", "Python.app")
    if os.path.exists(candidate):
        return candidate

    # Last resort: raw binary path
    return real_bin


def check_accessibility_trusted():
    """
    Check if this process has permission to monitor keyboard events.
    On macOS, uses AXIsProcessTrusted() from ApplicationServices framework.
    On Windows, keyboard hooks work without special permissions — always returns True.
    """
    # Windows doesn't need Accessibility permission for keyboard hooks.
    if sys.platform != "darwin":
        return True

    try:
        lib = ctypes.cdll.LoadLibrary(
            "/System/Library/Frameworks/ApplicationServices.framework/ApplicationServices"
        )
        lib.AXIsProcessTrusted.restype = ctypes.c_bool
        return lib.AXIsProcessTrusted()

    except Exception:
        return True


def _print_permission_instructions():
    """
    Print detailed instructions for fixing Accessibility permissions.
    Only relevant on macOS — Windows doesn't need this.
    """
    # On Windows, keyboard hooks work without special permissions.
    if sys.platform != "darwin":
        return

    real_path = _get_python_binary_path()

    msg = (
        "\n"
        "  ⚠ ACCESSIBILITY PERMISSION MISSING\n"
        "  FlowKeys needs Accessibility permission to hear your keystrokes.\n"
        "\n"
        f"  The Python app to add to Accessibility:\n"
        f"    {real_path}\n"
        "\n"
        "  To fix this:\n"
        "  1. Open System Settings → Privacy & Security → Accessibility\n"
        f"  2. Click + → press Cmd+Shift+G → type:\n"
        f"       {real_path}\n"
        "  3. Press Enter → click Open → toggle ON\n"
        "\n"
        "  Also add your Terminal app (Applications → Utilities → Terminal)\n"
        "\n"
        "  If it was already added but stopped working, run:\n"
        f"    python3 ~/FlowKeys/main.py --fix-permissions\n"
        "\n"
    )
    print(msg)
    logger.warning(
        "Accessibility permission missing for binary: %s", real_path
    )


def _check_accessibility():
    """
    Backup check: if no key events received after 3 seconds, warn the user.
    This catches edge cases where AXIsProcessTrusted returned True but
    pynput still can't receive events (e.g., Terminal not in Accessibility list).
    """
    if not _received_key_event:
        _print_permission_instructions()
        logger.warning("No key events received — Accessibility permission may be missing")


def start():
    """
    Start listening for keypresses on the entire system.
    The listener runs in a background thread so it doesn't block the main program.
    """
    global _listener, _last_key_time

    # Set initial key time so the watchdog doesn't trigger immediately.
    _last_key_time = time.time()

    # Create a pynput keyboard listener.
    # on_press is called for every key down, on_release for every key up.
    _listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)

    # Start the listener in its own background thread.
    _listener.start()

    # Log that we're now listening.
    logger.info("Keyboard listener started")

    # Start a 3-second timer to check for Accessibility permissions.
    # If no key events arrive in 3 seconds, we'll warn the user.
    timer = threading.Timer(3.0, _check_accessibility)
    timer.daemon = True  # Don't keep the program running just for this timer
    timer.start()


def restart():
    """
    Restart the keyboard listener. Used to recover from sleep/wake
    where macOS drops the accessibility connection.
    """
    global _listener, _received_key_event, _last_key_time

    logger.info("Restarting keyboard listener (recovering from sleep/wake)...")

    # Stop old listener.
    if _listener is not None:
        try:
            _listener.stop()
        except Exception:
            pass
        _listener = None

    # Reset tracking state.
    _received_key_event = False
    _last_key_time = time.time()

    # Create and start a fresh listener.
    _listener = keyboard.Listener(on_press=_on_press, on_release=_on_release)
    _listener.start()
    logger.info("Keyboard listener restarted")


def stop():
    """
    Stop listening for keypresses and clean up.
    """
    global _listener

    # If there's an active listener, stop it.
    if _listener is not None:
        _listener.stop()  # Signal the listener thread to stop
        _listener = None  # Clear the reference
        logger.info("Keyboard listener stopped")


def is_enabled():
    """
    Return whether sound playback is currently enabled.
    """
    return _enabled


def get_last_key_time():
    """
    Return the timestamp of the last key event received.
    Used by the main loop watchdog to detect sleep/wake stalls.
    """
    return _last_key_time
