# FlowKeys

### The sound you love. Without the keyboard you don't need.

---

## The Problem

Mechanical keyboards sound incredible. That satisfying *click* on every keypress — it just makes typing feel better.

But here's the thing.

A good mechanical keyboard costs anywhere from **$80 to $300+**. Custom builds? Even more. And if you already have a MacBook with a perfectly good keyboard, buying another one just for the sound feels... unnecessary.

What if you could get that satisfying click — on the keyboard you already have?

---

## Meet FlowKeys

FlowKeys is a tiny app that runs quietly on your Mac. Every time you press a key, it plays a crisp mechanical keyboard sound through your speakers.

That's it. No extra hardware. No expensive purchases. Just the sound you love, on the Mac you already own.

**Two sounds to choose from:**
- **Mechanical** — Classic Cherry MX clicky. The one you hear in every coding video.
- **Soft** — A quieter, gentler tap. Perfect for late nights or shared spaces.

Switch between them instantly with a keyboard shortcut. Turn it off when you're on a call. Turn it back on when you're in the zone.

**It just works.** Starts automatically when you turn on your Mac. Runs silently in the background. No dock icon, no menu bar clutter, nothing to think about.

---

## How to Install

One command. That's it. No downloading ZIP files, no Gatekeeper warnings, no "can't be verified" popups.

### Step 1. Open Terminal

Press `Cmd + Space`, type **Terminal**, press Enter. A window with a text prompt will appear.

### Step 2. Paste this command and press Enter

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/install-remote.sh)"
```

The installer will download FlowKeys, install dependencies, set up auto-start, and open System Settings for the next step. Takes about 30 seconds.

### Step 3. Grant Permission (One-Time)

FlowKeys needs your permission to hear your keypresses. macOS takes your privacy seriously — no app can do this without your explicit approval.

This takes 30 seconds and you only do it once.

1. The installer opens **System Settings > Privacy & Security > Accessibility** automatically

2. Click the **+** button (bottom-left)

3. A file picker will open. Press **Cmd + Shift + G** to open the "Go to folder" bar. Type the **exact path shown by the installer** and press **Enter**. Click **Open**.

   > **Why not just python3?** macOS tracks Accessibility permissions by the actual binary running your code. Depending on how Python is installed, the real binary may be deep inside a framework path (e.g. `/Library/Frameworks/Python.framework/.../Python`). The installer detects this for you and prints the correct path.

4. Make sure the toggle next to it is turned **ON** (blue)

5. Also add **Terminal**: click **+** again, go to Applications → Utilities → Terminal, click Open, toggle **ON**

### Step 4. Done

That's it. Start typing. You should hear a mechanical click on every keypress.

FlowKeys will start automatically every time you turn on your Mac. You don't need to do anything.

---

## Keyboard Shortcuts

| What you press | What happens |
|---|---|
| `Cmd + Ctrl + K` | Turn sound on or off |
| `Cmd + Ctrl + S` | Switch between mechanical and soft |

That's all you need to remember.

---

## Uninstalling

Changed your mind? No worries. Open Terminal and paste:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/rhalder90/FlowKeys/main/uninstall-remote.sh)"
```

Everything gets cleaned up. No leftover files, no lingering processes.

---

## Need Help?

**No sound when you type?**
The most common reason is the Accessibility permission from Step 3. Go back and make sure both the Python binary and **Terminal** are added and toggled ON.

**Permission broke after a Python update?**
Run this in Terminal to auto-fix: `python3 ~/FlowKeys/main.py --fix-permissions`

**Still not working?**
Email **write.rhalder90@gmail.com** — happy to help.

---

*FlowKeys is free and open source. Built with Python, pynput, and pygame-ce.*
*Sound credits: [OpenGameArt](https://opengameart.org/content/single-key-press-sounds) by eklee and qubodup (CC-BY 3.0).*
