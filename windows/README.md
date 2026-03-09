# FlowKeys for Windows

Mechanical keyboard sounds for your PC. Every keypress plays a satisfying click through your speakers.

## Download

Go to [**Releases**](https://github.com/rhalder90/FlowKeys/releases) and download **FlowKeys.exe**.

That's it. No installation, no Python, no setup. Just download and double-click.

## First Time Running

Windows SmartScreen may show a blue warning: **"Windows protected your PC"**

This is normal for unsigned apps downloaded from the internet. FlowKeys is free, open source, and safe.

1. Click **More info**
2. Click **Run anyway**

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Win + Ctrl + K` | Toggle sound on/off |
| `Win + Ctrl + S` | Switch between mechanical and soft sound |

## Auto-Start on Login

To have FlowKeys start automatically when you turn on your PC:

```
FlowKeys.exe --enable-autostart
```

To remove auto-start:

```
FlowKeys.exe --disable-autostart
```

## Uninstall

Just delete `FlowKeys.exe`. If you enabled auto-start, run `FlowKeys.exe --disable-autostart` first.

## Troubleshooting

**No sound when I type**
- Make sure your volume is not muted
- Some antivirus software may block keyboard hooks — add FlowKeys as an exception

**"FlowKeys is already running"**
- Another instance is active. Close the other FlowKeys window, or open Task Manager and end the FlowKeys process.

**Sound is delayed**
- Close audio-heavy apps (video calls, music production software)

**Still stuck?**
Email **write.rhalder90@gmail.com** — happy to help.
