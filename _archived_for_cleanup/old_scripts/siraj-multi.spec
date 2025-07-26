# -*- mode: python ; coding: utf-8 -*-
"""
SIRAJ Educational AI - Multi-Instance PyInstaller Specification
===============================================================

Enhanced spec file for building SIRAJ with multi-instance support.
Includes router service, multiple Ollama management, and all dependencies.
"""

import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Get the absolute path to the project directory
PROJECT_ROOT = os.path.abspath('.')
BACKEND_DIR = os.path.join(PROJECT_ROOT, 'backend')
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'build')
DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs')

# Collect all necessary data files
datas = []

# Add backend files
datas += collect_data_files('fastapi')
datas += collect_data_files('uvicorn')
datas += collect_data_files('sqlalchemy')
datas += collect_data_files('httpx')
datas += collect_data_files('psutil')

# Add frontend build files
if os.path.exists(FRONTEND_DIR):
    datas.append((FRONTEND_DIR, 'frontend/build'))

# Add documentation
if os.path.exists(DOCS_DIR):
    datas.append((DOCS_DIR, 'docs'))

# Add configuration files
datas.append(('.env.example', '.'))
datas.append(('README.md', '.'))
datas.append(('PROJECT_COMPLETE.md', '.'))
datas.append(('MULTI-INSTANCE-README.md', '.'))

# Add backend source files
datas.append((os.path.join(BACKEND_DIR, 'main.py'), 'backend'))
datas.append((os.path.join(BACKEND_DIR, 'extended_endpoints.py'), 'backend'))
datas.append((os.path.join(BACKEND_DIR, 'backend_router.py'), 'backend'))
if os.path.exists(os.path.join(BACKEND_DIR, 'requirements.txt')):
    datas.append((os.path.join(BACKEND_DIR, 'requirements.txt'), 'backend'))

# Collect all necessary hidden imports
hiddenimports = []
hiddenimports += collect_submodules('fastapi')
hiddenimports += collect_submodules('uvicorn')
hiddenimports += collect_submodules('sqlalchemy')
hiddenimports += collect_submodules('httpx')
hiddenimports += collect_submodules('psutil')
hiddenimports += collect_submodules('pydantic')
hiddenimports += collect_submodules('websockets')
hiddenimports += collect_submodules('aiofiles')
hiddenimports += collect_submodules('asyncio')
hiddenimports += collect_submodules('multidict')
hiddenimports += collect_submodules('yarl')

# Add specific imports for multi-instance support
hiddenimports += [
    'uvicorn.logging',
    'uvicorn.loops',
    'uvicorn.loops.auto',
    'uvicorn.protocols',
    'uvicorn.protocols.http',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan',
    'uvicorn.lifespan.on',
    'httpx._transports.default',
    'httpx._transports.asgi',
    'psutil._psutil_windows',
    'psutil._psutil_linux',
    'psutil._psutil_osx',
    'psutil._psutil_posix',
]

# Binary files to include
binaries = []

# Analysis configuration
a = Analysis(
    ['launcher.py'],
    pathex=[PROJECT_ROOT, BACKEND_DIR],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'PIL', 'tkinter', 'PyQt5', 'PySide2'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove unnecessary modules to reduce size
excluded_binaries = [
    'matplotlib', 'numpy', 'pandas', 'scipy',
    'PIL', 'Pillow', 'sklearn', 'tensorflow',
    'torch', 'keras', 'opencv'
]

a.binaries = [
    binary for binary in a.binaries 
    if not any(excluded in binary[0] for excluded in excluded_binaries)
]

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SIRAJ-Educational-AI-MultiInstance',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='siraj_version.txt',
    icon='siraj_icon.ico',
    uac_admin=False,
    uac_uiaccess=False,
)

# Create distribution package
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SIRAJ-Multi-Instance-Suite',
)
