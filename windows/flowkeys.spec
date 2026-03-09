# flowkeys.spec — PyInstaller build specification for FlowKeys Windows .exe
#
# Build command (run on Windows):
#   pip install pyinstaller pygame-ce pynput
#   pyinstaller windows/flowkeys.spec
#
# Output: dist/FlowKeys.exe (single file, ~15-25 MB)

import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sounds/*.wav', 'sounds'),  # Bundle sound files into the exe
    ],
    hiddenimports=[
        'pynput.keyboard._win32',    # pynput Windows keyboard backend
        'pynput._util.win32',        # pynput Windows utilities
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='FlowKeys',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Show console window (user sees shortcuts info)
    icon=None,     # TODO: Add a .ico file for the exe icon
)
