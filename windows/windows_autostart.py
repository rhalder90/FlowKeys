# windows_autostart.py — Manage Windows auto-start for FlowKeys.
# Creates/removes a shortcut in the Windows Startup folder so FlowKeys
# runs automatically when the user logs in.

import os
import sys


def get_startup_folder():
    """Return the path to the Windows Startup folder."""
    return os.path.join(
        os.environ.get("APPDATA", os.path.expanduser("~")),
        "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
    )


def get_shortcut_path():
    """Return the full path where the FlowKeys shortcut would be."""
    return os.path.join(get_startup_folder(), "FlowKeys.lnk")


def is_autostart_enabled():
    """Check if FlowKeys is set to auto-start."""
    return os.path.exists(get_shortcut_path())


def enable_autostart(exe_path):
    """
    Create a .lnk shortcut in the Startup folder pointing to the given exe.
    Uses PowerShell to create the shortcut (avoids needing pywin32).
    """
    shortcut_path = get_shortcut_path()
    working_dir = os.path.dirname(exe_path)

    # Escape backslashes for PowerShell string
    shortcut_escaped = shortcut_path.replace("'", "''")
    exe_escaped = exe_path.replace("'", "''")
    working_escaped = working_dir.replace("'", "''")

    ps_command = (
        f"$ws = New-Object -ComObject WScript.Shell; "
        f"$sc = $ws.CreateShortcut('{shortcut_escaped}'); "
        f"$sc.TargetPath = '{exe_escaped}'; "
        f"$sc.WorkingDirectory = '{working_escaped}'; "
        f"$sc.Description = 'FlowKeys - Mechanical keyboard sounds'; "
        f"$sc.Save()"
    )

    os.system(f'powershell -Command "{ps_command}"')


def disable_autostart():
    """Remove the FlowKeys shortcut from the Startup folder."""
    shortcut_path = get_shortcut_path()
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)
        return True
    return False
