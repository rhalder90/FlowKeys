# FlowKeys — Product Requirements Document

## What We're Building

FlowKeys is a lightweight macOS background script that plays mechanical keyboard click sounds through your speakers on every real keystroke. It includes two sound profiles (mechanical and soft), keyboard shortcuts to toggle and switch sounds, auto-start on login, and a double-click installer. No terminal knowledge required.

The goal: make typing on a MacBook feel and sound like a satisfying mechanical keyboard — without buying one.

---

## File Structure

```
FlowKeys/
├── sounds/
│   ├── mechanical.wav            # Classic Cherry MX click sound
│   └── soft.wav                  # Softer, quieter tactile click sound
├── main.py                       # Entry point — startup, shutdown, signal handling
├── listener.py                   # pynput global hook — keypresses, toggle, sound switching
├── player.py                     # pygame mixer — pre-loads sounds, play(), device recovery
├── config.py                     # All settings: volume, paths, shortcuts, version
├── logger_setup.py               # Configures Python logging to file + console
├── com.flowkeys.agent.plist      # macOS LaunchAgent for auto-start on login
├── install.command               # Double-click installer
├── uninstall.command             # Double-click uninstaller
├── .gitignore                    # Python bytecache, .DS_Store, venvs
├── PRD.md                        # This document
└── README.md                     # Setup, permissions, troubleshooting
```

---

## Tech Stack and Why

| Technology | Purpose | Why This Choice |
|---|---|---|
| **Python 3** | Language | Simple, readable, great library ecosystem. Perfect for a beginner-friendly project. |
| **pynput** | Global keypress detection | Listens for keypresses system-wide (not just inside a terminal). Works on macOS with Accessibility permissions. |
| **pygame-ce (mixer)** | Audio playback | Community edition of pygame. Pre-loads sounds into RAM for near-zero latency. Non-blocking playback so rapid typing never queues or stutters. |
| **WAV format** | Sound files | Uncompressed audio = no decoding overhead = fastest possible playback. |

### Why not other options?

- **sounddevice / pyaudio**: Lower-level, more complex setup, overkill for playing a single sound.
- **playsound**: Reads from disk every time — too slow for rapid typing.
- **Objective-C / Swift**: Would be faster, but Python keeps this beginner-friendly.
- **pygame (original)**: Doesn't have pre-built wheels for Python 3.14; pygame-ce does.

---

## Key Features

### Two Sound Profiles
- **Mechanical**: Classic Cherry MX clicky sound
- **Soft**: Quieter, softer tactile click
- Both pre-loaded into RAM at startup
- Switch between them with Cmd+Ctrl+S (no restart needed)

### Keyboard Shortcuts
- **Cmd+Ctrl+K**: Toggle sound on/off
- **Cmd+Ctrl+S**: Cycle between mechanical and soft sound
- Shortcuts print reminders to terminal on each use

### Auto-Start on Login
- macOS LaunchAgent starts FlowKeys automatically when you log in
- Set up via double-click `install.command`
- Remove via double-click `uninstall.command`

### Consumer-Friendly Install
- Double-click `install.command` — installs dependencies, sets up auto-start
- Double-click `uninstall.command` — removes auto-start
- No terminal commands needed

---

## Key Performance Requirements

1. **Pre-load sounds into RAM at startup** — both WAV files are loaded once. Every keypress plays from memory, never from disk.
2. **Low-latency mixer initialization** — pygame mixer uses a small buffer:
   ```python
   pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)
   ```
3. **Non-blocking playback** — 16 audio channels allow rapid keypresses to overlap without queuing.
4. **Audio device recovery** — if the audio device disconnects (e.g., headphone unplug), the mixer attempts automatic reinitialization.

---

## Production-Readiness Features

| Feature | File | Description |
|---|---|---|
| File + console logging | `logger_setup.py` | Logs to `~/Library/Logs/FlowKeys/flowkeys.log` with rotation at 1MB |
| Accessibility check | `listener.py` | 3-second timeout warns if no key events detected |
| Startup notification | `main.py` | macOS notification on successful launch |
| Duplicate prevention | `main.py` | PID file at `~/.flowkeys.pid` prevents multiple instances |
| Channel exhaustion | `player.py` | 16 channels; silently skips if all busy |
| Audio device recovery | `player.py` | Try/except in play(); reinit mixer once on failure |
| Folder-move warning | `install.command` | Warns user to re-run installer if folder is moved |
| Version tracking | `config.py` | `VERSION = "1.0.0"` shown in startup banner and --help |
| --help flag | `main.py` | `python3 main.py --help` shows usage and shortcuts |

---

## Risks

| Risk | Impact | Mitigation |
|---|---|---|
| **macOS Accessibility permission not granted** | pynput cannot detect keypresses — script silently fails | 3-second timeout check warns user. README has step-by-step setup. install.command reminds user. |
| **Audio latency / delay** | Typing feels laggy | Pre-loading + buffer=512 keeps latency under ~12ms. Non-blocking playback. |
| **pygame.mixer conflicts** | Mixer init fails if audio device unavailable | Try/except with clear error. Auto-reinit on device change. |
| **pynput modifier key detection on macOS** | Toggle shortcut may not work | Testing with Key.cmd, Key.ctrl_l, Key.ctrl_r. |
| **Sound file missing or corrupted** | Script crashes on startup | File existence check before loading. Helpful error message. |
| **High CPU usage** | Battery drain | pynput listener is event-driven (not polling). Negligible CPU. |
| **Duplicate instances** | Two processes fighting over audio | PID file prevents multiple instances. |
| **Folder moved after install** | LaunchAgent points to wrong path | install.command prints warning. User re-runs installer. |
| **Security concerns (keylogging)** | User trust | FlowKeys never records, stores, or transmits keypress data. Only plays sounds. Documented in README. |

---

## Sound Credits

- Keyboard sounds from [OpenGameArt](https://opengameart.org/content/single-key-press-sounds) by eklee and qubodup, licensed under [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/)
