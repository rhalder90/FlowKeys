# FlowKeys

Mechanical keyboard sounds for your Mac. Every keypress plays a satisfying click through your speakers.

Two sounds included: **mechanical** (Cherry MX-style) and **soft** (quiet tactile). Switch between them with a keyboard shortcut.

---

## Install

Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Enter) and paste this:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/install-remote.sh)"
```

That's it. The script downloads FlowKeys, installs it to `~/FlowKeys`, and sets up auto-start. No Gatekeeper warnings, no "can't be verified" popups.

After running the command, grant Accessibility permission (see below) and you're done.

<details>
<summary><strong>Alternative: Manual install</strong> (if you prefer downloading)</summary>

1. Download or clone this folder
2. Double-click **`install.command`**
   - **macOS may block it** — see "macOS says it can't be verified" below
3. Grant Accessibility permission (see below)
4. Done — FlowKeys auto-starts on every login

The installer copies FlowKeys to `~/FlowKeys` and sets up auto-start. You can delete the downloaded folder after installing.
</details>

## Accessibility Permission (Required — One-Time Setup)

FlowKeys needs permission to detect your keypresses. Without this, it won't work. You only do this once.

1. The installer opens Accessibility settings automatically
2. Click the **+** button
3. Navigate to your **home folder** → **FlowKeys** → select **FlowKeys.app**
4. Click **Open**
5. Make sure the toggle next to FlowKeys is **ON**

> **Tip:** Your home folder is usually `/Users/yourname`. Look for the FlowKeys folder there, not in Desktop or Downloads.

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Cmd + Ctrl + K` | Toggle sound on/off |
| `Cmd + Ctrl + S` | Switch between mechanical and soft sound |

## Run Manually

If you prefer not to use auto-start:

```bash
cd ~/FlowKeys
python3 main.py
```

Press `Ctrl+C` to stop.

To see all options:

```bash
python3 main.py --help
```

## Uninstall

Open Terminal and paste:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/uninstall-remote.sh)"
```

This stops FlowKeys, removes auto-start, and deletes all installed files.

## Logs

FlowKeys writes logs to:

```
~/Library/Logs/FlowKeys/flowkeys.log
```

Check this file if something isn't working.

## Troubleshooting

**No sound when I type**
1. Make sure Accessibility permission is granted (see above)
2. Check that your Mac volume is not muted
3. Open Terminal and run `python3 ~/FlowKeys/main.py` — if you see "This process is not trusted!", Accessibility permission is missing
4. Check the log file at `~/Library/Logs/FlowKeys/flowkeys.log` for errors

**FlowKeys doesn't start after reboot**
1. Open Terminal and run:
   ```bash
   launchctl list | grep flowkeys
   ```
2. If nothing shows up, double-click `install.command` again to re-register auto-start
3. If it shows up but FlowKeys isn't working, check `~/Library/Logs/FlowKeys/stderr.log` for errors

**"FlowKeys is already running"**
- Another instance is active. Double-click `~/FlowKeys/uninstall.command` to stop it, then try again.
- Or run this in Terminal to force stop:
  ```bash
  pkill -9 -f "FlowKeys" && rm -f ~/.flowkeys.pid
  ```

**Sound still playing after uninstall**
- Run this in Terminal:
  ```bash
  pkill -9 -f "FlowKeys"
  ```

**Sound is delayed or laggy**
- Close other audio-heavy apps (video calls, music production software)
- Check `~/Library/Logs/FlowKeys/flowkeys.log` for audio mixer errors

**macOS says "install.command can't be verified" or mentions malware**

*Method 1 — Right-click (try this first):*
1. Click **Done** (not "Move to Bin")
2. **Right-click** on `install.command`
3. Click **Open** from the context menu
4. A **new dialog** appears with an **Open** button — click it

*Method 2 — If right-click still doesn't work:*
1. Click **Done**
2. Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Enter)
3. Paste this command and press Enter:
   ```bash
   xattr -dr com.apple.quarantine ~/Downloads/FlowKeys*/
   ```
4. Now double-click `install.command` — it will open without warning

This is normal for files downloaded from the internet. macOS blocks unsigned scripts by default. FlowKeys is open source and safe.

**Python or dependency errors**
1. Make sure Python 3 is installed: `python3 --version`
2. Reinstall dependencies: `pip3 install pynput pygame-ce`
3. If you recently updated macOS, re-run `install.command`

**Reinstalling / Updating**
- Just double-click `install.command` again — it stops the old version and installs a fresh copy

**Still stuck?**
- Email **write.rhalder90@gmail.com** with a description of your issue and the contents of `~/Library/Logs/FlowKeys/flowkeys.log`

## Sound Credits

- Keyboard sounds from [OpenGameArt](https://opengameart.org/content/single-key-press-sounds) by eklee and qubodup, licensed under [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/)

## License

MIT
