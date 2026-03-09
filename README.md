# FlowKeys

Mechanical keyboard sounds for your Mac or PC. Every keypress plays a satisfying click through your speakers.

Two sounds included: **mechanical** (Cherry MX-style) and **soft** (quiet tactile). Switch between them with a keyboard shortcut.

**Works on macOS and Windows.**

---

## Install — Mac

Open **Terminal** (press `Cmd + Space`, type `Terminal`, press Enter) and paste this:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/install-remote.sh)"
```

That's it. The script downloads FlowKeys, installs it to `~/FlowKeys`, and sets up auto-start.

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

### Accessibility Permission (Mac — One-Time Setup)

FlowKeys needs permission to detect your keypresses. You only do this once.

1. The installer opens Accessibility settings automatically
2. Click the **+** button
3. Press **Cmd + Shift + G** to open the "Go to folder" bar
4. Type the **exact path shown by the installer** and press **Enter**
5. Click **Open**
6. Make sure the toggle next to it is **ON**
7. Also add **Terminal**: click **+** again → go to Applications → Utilities → Terminal → click Open → toggle **ON**

> **Tip:** The installer detects the correct Python binary path for your system and prints it. The path varies depending on how Python was installed. Always use the path shown by the installer.
>
> **If permission breaks after a Python update**, run: `python3 ~/FlowKeys/main.py --fix-permissions`

### Uninstall — Mac

Open Terminal and paste:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/uninstall-remote.sh)"
```

This stops FlowKeys, removes auto-start, and deletes all installed files.

---

## Install — Windows

1. Go to [**Releases**](https://github.com/rhalder90/FlowKeys/releases) and download **FlowKeys.exe**
2. Double-click **FlowKeys.exe**
3. Start typing — you'll hear clicks immediately

**No Python, no Terminal, no permissions needed.** Just download one file and run it.

> **Windows SmartScreen warning:** Windows may show a blue screen saying "Windows protected your PC". This is normal for unsigned apps. Click **More info** → **Run anyway**. FlowKeys is open source and safe.

### Auto-Start on Login (Windows)

To have FlowKeys start automatically when you turn on your PC:

```
FlowKeys.exe --enable-autostart
```

To remove auto-start:

```
FlowKeys.exe --disable-autostart
```

### Uninstall — Windows

1. If you enabled auto-start, run `FlowKeys.exe --disable-autostart` first
2. Delete `FlowKeys.exe`

That's it. No registry entries, no hidden files to clean up.

---

## Keyboard Shortcuts

| | Mac | Windows |
|---|---|---|
| Toggle sound on/off | `Cmd + Ctrl + K` | `Win + Ctrl + K` |
| Switch sound | `Cmd + Ctrl + S` | `Win + Ctrl + S` |

---

## FAQ

**What is FlowKeys?**
A tiny free app that plays a mechanical keyboard click sound every time you press a key. Works on Mac and Windows.

**Is it free?**
Yes. Free and open source (MIT license).

**Does it work on Windows?**
Yes. Download `FlowKeys.exe` from the [Releases](https://github.com/rhalder90/FlowKeys/releases) page. No installation needed.

**Does it work on Mac?**
Yes. Run the one-line installer in Terminal (see above).

**Do I need to install Python?**
- **Mac:** Python 3 is required. Most Macs have it already. The installer will tell you if it's missing.
- **Windows:** No. The `.exe` bundles everything. Just download and run.

**Does it start automatically when I restart my computer?**
- **Mac:** Yes, automatically. The installer sets this up.
- **Windows:** Run `FlowKeys.exe --enable-autostart` once. After that, it starts on every login.

**How do I stop it?**
Press `Ctrl+C` in the terminal window, or close the window. On Windows, you can also use Task Manager.

**How do I switch between mechanical and soft sounds?**
Press `Cmd+Ctrl+S` on Mac or `Win+Ctrl+S` on Windows.

**Will my antivirus flag it? (Windows)**
Some antivirus programs may flag keyboard hooks as suspicious. This is because FlowKeys listens to your keypresses to play sounds. Add FlowKeys as an exception if your antivirus blocks it. FlowKeys is open source — you can verify the code yourself.

**Why does Windows say "Windows protected your PC"?**
This is Windows SmartScreen. It shows this for any unsigned `.exe` downloaded from the internet. Click **More info** → **Run anyway**. This is a one-time warning.

**Why does Mac need Accessibility permission but Windows doesn't?**
macOS requires explicit permission for any app that monitors keyboard input. Windows allows keyboard hooks without special permissions.

**No sound when I type (Mac)**
1. Make sure Accessibility permission is granted — both the Python binary and Terminal must be added
2. Run `python3 ~/FlowKeys/main.py --fix-permissions` to auto-fix
3. Check logs: `cat ~/Library/Logs/FlowKeys/flowkeys.log`

**No sound when I type (Windows)**
1. Make sure your volume is not muted
2. Check if your antivirus is blocking FlowKeys — add it as an exception
3. Try running FlowKeys as Administrator (right-click → Run as administrator)

**Can I use it on both Mac and Windows?**
Yes. The same codebase runs on both. Mac uses the Terminal installer, Windows uses the `.exe`.

**Where are the log files?**
- **Mac:** `~/Library/Logs/FlowKeys/flowkeys.log`
- **Windows:** `%LOCALAPPDATA%\FlowKeys\Logs\flowkeys.log`

**Still stuck?**
Email **write.rhalder90@gmail.com** — happy to help.

---

## Troubleshooting — Mac

**FlowKeys doesn't start after reboot**
1. Run `launchctl list | grep flowkeys` in Terminal
2. If nothing shows up, re-run the install command

**"FlowKeys is already running"**
```bash
pkill -9 -f "FlowKeys" && rm -f ~/.flowkeys.pid
```

**macOS says "install.command can't be verified"**
Use the one-line Terminal installer instead — it bypasses Gatekeeper completely.

**Python or dependency errors**
```bash
python3 --version
pip3 install pynput pygame-ce
```

## Troubleshooting — Windows

**"FlowKeys is already running"**
Open Task Manager → find FlowKeys → End task. Then run FlowKeys.exe again.

**Sound is delayed**
Close audio-heavy apps (video calls, music production software).

**Keyboard shortcuts don't work in admin apps**
If you run an app as Administrator, FlowKeys can't detect keypresses in that app. This is a Windows security feature.

---

## Sound Credits

- Keyboard sounds from [OpenGameArt](https://opengameart.org/content/single-key-press-sounds) by eklee and qubodup, licensed under [CC-BY 3.0](https://creativecommons.org/licenses/by/3.0/)

## License

MIT
