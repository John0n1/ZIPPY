# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for building Windows executable with icon.
Build with: pyinstaller zippy_windows.spec
"""

block_cipher = None

a = Analysis(
    ['zippy_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('debian/icons/zippy.svg', 'icons'),
    ],
    hiddenimports=['zippy', 'zippy.cli'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='zippy-launcher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console window open
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='debian/icons/zippy.ico',  # You'll need to convert SVG to ICO
)
