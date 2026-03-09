# config.py — All settings for FlowKeys live here.
# Change these values to customize how FlowKeys behaves.

# === IMPORTS ===
import os   # We use 'os' to work with file paths on any system
import sys  # We use 'sys' to detect the operating system (Windows vs macOS)

# === VERSION ===
# The current version of FlowKeys. Shown in the startup banner.
VERSION = "1.0.0"

# === FILE PATHS ===
# When packaged as a .exe by PyInstaller, files are extracted to a temp folder.
# sys._MEIPASS points to that temp folder. In normal Python, we use __file__.
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# The "sounds" folder sits right next to this config.py file.
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

# === SOUND FILES ===
# A dictionary mapping friendly names to their WAV file paths.
# "mechanical" = classic Cherry MX clicky sound
# "soft" = quieter, softer tactile click
SOUNDS = {
    "mechanical": os.path.join(SOUND_DIR, "mechanical.wav"),
    "soft": os.path.join(SOUND_DIR, "soft.wav"),
}

# The order in which sounds cycle when you press the switch shortcut.
SOUND_ORDER = ["mechanical", "soft"]

# Which sound plays when FlowKeys first starts up.
DEFAULT_SOUND = "mechanical"

# === VOLUME ===
# Volume level from 0.0 (silent) to 1.0 (full volume).
# 0.5 is a comfortable default — not too loud, not too quiet.
VOLUME = 0.5

# === AUDIO SETTINGS ===
# Number of audio channels pygame can use at once.
# 16 channels means up to 16 key sounds can overlap simultaneously.
# A fast typist hits ~10 keys/second, so 16 gives plenty of headroom.
NUM_AUDIO_CHANNELS = 16

# === KEYBOARD SHORTCUTS ===
# The modifier keys that must be held down for each shortcut.
# macOS: Cmd + Ctrl (⌘ + ⌃)
# Windows: Win + Ctrl (the Windows key acts like Cmd)

if sys.platform == "win32":
    # Toggle FlowKeys on/off: hold Win + Ctrl, then press K
    TOGGLE_COMBO_MODIFIERS = {"cmd", "ctrl"}  # pynput maps Win key to "cmd"
    TOGGLE_COMBO_KEY = "k"
    # Switch sounds: hold Win + Ctrl, then press S
    SWITCH_COMBO_MODIFIERS = {"cmd", "ctrl"}
    SWITCH_COMBO_KEY = "s"
else:
    # Toggle FlowKeys on/off: hold Cmd + Ctrl, then press K
    TOGGLE_COMBO_MODIFIERS = {"cmd", "ctrl"}
    TOGGLE_COMBO_KEY = "k"
    # Switch sounds: hold Cmd + Ctrl, then press S
    SWITCH_COMBO_MODIFIERS = {"cmd", "ctrl"}
    SWITCH_COMBO_KEY = "s"

# === LOGGING ===
# Where FlowKeys writes its log file.
if sys.platform == "win32":
    # Windows: %LOCALAPPDATA%\FlowKeys\Logs (e.g. C:\Users\Name\AppData\Local\FlowKeys\Logs)
    LOG_DIR = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "FlowKeys", "Logs")
else:
    # macOS: ~/Library/Logs/ is the standard location for app logs.
    LOG_DIR = os.path.expanduser("~/Library/Logs/FlowKeys")

# The name of the log file inside LOG_DIR.
LOG_FILE = "flowkeys.log"

# === PID FILE ===
# A PID file prevents two copies of FlowKeys from running at the same time.
if sys.platform == "win32":
    PID_FILE = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "FlowKeys", "flowkeys.pid")
else:
    PID_FILE = os.path.expanduser("~/.flowkeys.pid")
