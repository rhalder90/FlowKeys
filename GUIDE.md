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

You'll download FlowKeys from GitHub. Don't worry if you've never used GitHub before — it's just a website where developers share their projects. You're simply downloading a folder.

### Step 1. Download FlowKeys

1. Open this link in your browser:
   **https://github.com/rhalder90/FlowKeys**

2. Click the green **Code** button

3. Click **Download ZIP**

4. Open your **Downloads** folder and double-click the ZIP file to unzip it. You should see a folder called **FlowKeys-main**

### Step 2. Install Python (if you don't have it)

FlowKeys is built with Python, a free programming language. Most Macs already have it, but let's make sure.

1. Open **Terminal**
   (Press `Cmd + Space`, type **Terminal**, press Enter)

2. Type this and press Enter:
   ```
   python3 --version
   ```

3. If you see something like `Python 3.12.0` — you're good. Skip to Step 3.

4. If you see an error, download Python from:
   **https://www.python.org/downloads/**
   Run the installer, then try the command above again.

### Step 3. Run the Installer

1. Open the **FlowKeys-main** folder you downloaded

2. Double-click **`install.command`**

3. A Terminal window will open and start installing. Let it do its thing. It takes about 30 seconds.

4. When it's done, it will open **System Settings** automatically. This is for the next step.

### Step 4. Grant Permission (One-Time)

FlowKeys needs your permission to hear your keypresses. macOS takes your privacy seriously — no app can do this without your explicit approval.

This takes 30 seconds and you only do it once.

1. In the **System Settings** window that just opened, you should see **Privacy & Security > Accessibility**

2. Click the **+** button (bottom-left)

3. A file picker will open. Navigate to:
   **Your home folder > FlowKeys > FlowKeys.app**

   > **How to find your home folder:** In the file picker, press `Cmd + Shift + H`. That takes you straight there. You'll see a folder called **FlowKeys**. Open it, select **FlowKeys.app**, and click **Open**.

4. Make sure the toggle next to **FlowKeys** is turned **ON** (blue)

### Step 5. Done

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

Changed your mind? No worries.

1. Open **Finder**
2. Press `Cmd + Shift + H` to go to your home folder
3. Open the **FlowKeys** folder
4. Double-click **`uninstall.command`**

Everything gets cleaned up. No leftover files, no lingering processes.

---

## Need Help?

**No sound when you type?**
The most common reason is the Accessibility permission from Step 4. Go back and make sure FlowKeys.app is added and toggled ON.

**Still not working?**
Email **write.rhalder90@gmail.com** — happy to help.

---

*FlowKeys is free and open source. Built with Python, pynput, and pygame-ce.*
*Sound credits: [OpenGameArt](https://opengameart.org/content/single-key-press-sounds) by eklee and qubodup (CC-BY 3.0).*
