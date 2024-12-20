# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\__main__.py'],
    pathex=[],
    binaries=[('C:\\Users\\taiyo\\Documents\\Python\humusic\\.venv\\Lib\\site-packages\\symusic\\bin\\midi2abc.exe','symusic\\bin\\'),
    ('C:\\Users\\taiyo\\Documents\\Python\humusic\\.venv\\Lib\\site-packages\\symusic\\bin\\abc2midi.exe','symusic\\bin\\'),
    ('C:\\Users\\taiyo\\Documents\\Python\\humusic\\resources\\path\\path_to_resources.json','resources\\path')
    ],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='__main__',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
