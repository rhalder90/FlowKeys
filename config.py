# config.py — All settings for FlowKeys live here.
# Change these values to customize how FlowKeys behaves.

# === IMPORTS ===
import os  # We use 'os' to work with file paths on any system

# === VERSION ===
# The current version of FlowKeys. Shown in the startup banner.
VERSION = "1.0.0"

# === FILE PATHS ===
# __file__ is a special Python variable that holds the path to THIS file (config.py).
# os.path.dirname gets the folder that contains this file.
# This way, we always find the sounds folder relative to where the code lives,
# no matter where the user runs the script from.
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
# These are the modifier keys that must be held down for each shortcut.
# "cmd" = Command key (⌘) on Mac
# "ctrl" = Control key (⌃) on Mac
# The third key in the combo is a regular letter key.

# Toggle FlowKeys on/off: hold Cmd + Ctrl, then press K
TOGGLE_COMBO_MODIFIERS = {"cmd", "ctrl"}  # Set of modifier keys to hold
TOGGLE_COMBO_KEY = "k"                     # The letter key to press

# Switch between mechanical/soft sounds: hold Cmd + Ctrl, then press S
SWITCH_COMBO_MODIFIERS = {"cmd", "ctrl"}  # Set of modifier keys to hold
SWITCH_COMBO_KEY = "s"                     # The letter key to press

# === LOGGING ===
# Where FlowKeys writes its log file.
# ~/Library/Logs/ is the standard macOS location for app logs.
LOG_DIR = os.path.expanduser("~/Library/Logs/FlowKeys")

# The name of the log file inside LOG_DIR.
LOG_FILE = "flowkeys.log"

# === PID FILE ===
# A PID file prevents two copies of FlowKeys from running at the same time.
# It stores the process ID of the running instance.
# ~ means your home folder (e.g., /Users/rahulhalder).
PID_FILE = os.path.expanduser("~/.flowkeys.pid")
