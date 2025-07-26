# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

# Define paths
base_dir = Path(r'C:\Users\Admin\Documents\RST\siraj-ai-school\build_selfcontained')
embedded_dir = base_dir / 'embedded'
app_dir = base_dir / 'app'

# Collect all embedded files with error handling
embedded_data = []

def collect_files_safely(source_dir, target_prefix):
    """Safely collect files with error handling"""
    if not source_dir.exists():
        return []
    
    files = []
    try:
        for item in source_dir.rglob('*'):
            if item.is_file():
                try:
                    relative_path = item.relative_to(source_dir.parent)
                    files.append((str(item), str(Path(target_prefix) / relative_path)))
                except Exception:
                    continue  # Skip problematic files
    except Exception:
        pass
    return files

# Add embedded files
embedded_data.extend(collect_files_safely(embedded_dir / 'python', 'embedded'))
embedded_data.extend(collect_files_safely(embedded_dir / 'nodejs', 'embedded'))
embedded_data.extend(collect_files_safely(app_dir, 'app'))

a = Analysis(
    [r'C:\Users\Admin\Documents\RST\siraj-ai-school\build_selfcontained\siraj_launcher.py'],
    pathex=[r'C:\Users\Admin\Documents\RST\siraj-ai-school\build_selfcontained'],
    binaries=[],
    datas=embedded_data,
    hiddenimports=[
        'asyncio', 'json', 'pathlib', 'subprocess', 'tempfile',
        'logging', 'webbrowser', 'shutil', 'time', 'zipfile',
        'urllib', 'urllib.request', 'urllib.error', 'ssl'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SIRAJ-Educational-AI-Complete',
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
    coerce_archive_to_exe=True,
    coerce_archive_to_dll=False,
    icon=None,
    version=None
)
