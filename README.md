# FlowKeys

Mechanical keyboard sounds for your Mac. Every keypress plays a satisfying click through your speakers.

Two sounds included: **mechanical** (Cherry MX-style) and **soft** (quiet tactile). Switch between them with a keyboard shortcut.

---

## Install

1. Download or clone this folder
2. Double-click **`install.command`**
3. Grant Accessibility permission (see below)
4. Done — FlowKeys auto-starts on every login

## Accessibility Permission (Required — One-Time Setup)

FlowKeys needs permission to detect your keypresses. Without this, it won't work. You only do this once.

1. The installer opens Accessibility settings automatically
2. Click the **+** button
3. Navigate to your **FlowKeys folder** and select **FlowKeys.app**
4. Click **Open**
5. Make sure the toggle next to FlowKeys is **ON**

> If running manually via Terminal instead of install.command, add **Terminal** to Accessibility instead (Applications → Utilities → Terminal).

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

**If sound is still playing after uninstall**, open Terminal and run:
```bash
pkill -9 -f "FlowKeys"
```
This force-kills any remaining FlowKeys process. This should not normally be needed — the uninstaller handles it automatically.

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
- Another instance is active. Double-click `uninstall.command` to stop it, then try again.
- Or run this in Terminal to force stop:
  ```bash
  pkill -9 -f "FlowKeys" && rm -f ~/.flowkeys.pid
  ```

**Sound still playing after uninstall**
- Run this in Terminal:
  ```bash
  pkill -9 -f "FlowKeys"
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
