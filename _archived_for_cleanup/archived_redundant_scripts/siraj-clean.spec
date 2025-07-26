# -*- mode: python ; coding: utf-8 -*-
# SIRAJ Educational AI - PyInstaller Spec
# Clean build following Living Spiral principles

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'httpx',
        'psutil',
        'fastapi',
        'uvicorn',
        'aiofiles',
        'colorama',
        'asyncio',
        'multiprocessing'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pandas',
        'numpy', 
        'scipy',
        'matplotlib',
        'sklearn',
        'torch',
        'tensorflow'
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='SIRAJ-Educational-AI',
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
    icon='siraj.ico' if os.path.exists('siraj.ico') else None,
    version='version.txt' if os.path.exists('version.txt') else None,
)
