# FlowKeys

Mechanical keyboard sounds for your Mac. Every keypress plays a satisfying click through your speakers.

Two sounds included: **mechanical** (Cherry MX-style) and **soft** (quiet tactile). Switch between them with a keyboard shortcut.

---

## Install

1. Download or clone this folder
2. Double-click **`install.command`**
3. Grant Accessibility permission (see below)
4. Done — FlowKeys auto-starts on every login

## Accessibility Permission (Required)

FlowKeys needs permission to detect your keypresses. Without this, it won't work.

1. Open **System Settings** (Apple menu → System Settings)
2. Go to **Privacy & Security** → **Accessibility**
3. Click the **+** button
4. Navigate to `/Applications/Utilities/` and add **Terminal** (or your terminal app: iTerm2, Warp, etc.)
5. Make sure the toggle next to it is **ON**
6. Restart FlowKeys

> If you run FlowKeys with Python directly, you may need to add Python instead of Terminal.

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Cmd + Ctrl + K` | Toggle sound on/off |
| `Cmd + Ctrl + S` | Switch between mechanical and soft sound |

## Run Manually

If you prefer not to use auto-start:

```bash
cd path/to/FlowKeys
python3 main.py
```

Press `Ctrl+C` to stop.

To see all options:

```bash
python3 main.py --help
```

## Uninstall

Double-click **`uninstall.command`** to stop FlowKeys and remove auto-start. Your files stay intact.

## Logs

FlowKeys writes logs to:

```
~/Library/Logs/FlowKeys/flowkeys.log
```

Check this file if something isn't working.

## Troubleshooting

**No sound when I type**
- Grant Accessibility permission (see above)
- Check that your volume is not muted
- Check the log file for errors

**"FlowKeys is already running"**
- Another instance is active. To stop it:
  ```bash
  cat ~/.flowkeys.pid  # shows the process ID
  kill $(cat ~/.flowkeys.pid)  # stops it
  ```

**Moved the FlowKeys folder**
- Double-click `install.command` again to update the auto-start path

**Sound is delayed or laggy**
- Close other audio-heavy apps
- Check log for audio mixer errors

## Sound Credits

- Keyboard sounds from [OpenGameArt](https://opengameart.org/content/single-key-press-sounds) by eklee and qubodup, licensed under [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/)

## License

MIT
