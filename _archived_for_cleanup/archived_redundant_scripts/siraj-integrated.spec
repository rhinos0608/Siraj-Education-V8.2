# -*- mode: python ; coding: utf-8 -*-
"""
SIRAJ Educational AI - PyInstaller Specification v8.2
=====================================================

Complete one-click executable with integrated educational council:
- Includes integrated launcher with full council functionality
- Embeds Gemma 3n model management
- Bundles frontend and backend components
- Supports zero-touch deployment
"""

import os
import sys
from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Project paths
PROJECT_ROOT = os.path.abspath('.')
FRONTEND_BUILD = os.path.join(PROJECT_ROOT, 'frontend', 'build')
DOCS_DIR = os.path.join(PROJECT_ROOT, 'docs')

# Data files to include
datas = []

# Core Python dependencies
datas += collect_data_files('fastapi')
datas += collect_data_files('uvicorn')
datas += collect_data_files('httpx')
datas += collect_data_files('pydantic')
datas += collect_data_files('psutil')

# Frontend build files (if they exist)
if os.path.exists(FRONTEND_BUILD):
    datas.append((FRONTEND_BUILD, 'frontend/build'))

# Documentation
if os.path.exists(DOCS_DIR):
    datas.append((DOCS_DIR, 'docs'))

# Configuration files
config_files = [
    '.env.example',
    'README.md',
    'DEPLOY-ONE-CLICK.bat',
    'fix_model_consistency_correct.py',
    'consciousness_educational_bridge.py'
]

for config_file in config_files:
    if os.path.exists(config_file):
        datas.append((config_file, '.'))

# Backend files
backend_files = [
    'backend/main.py',
    'backend/backend_router.py',
    'backend/requirements.txt'
]

for backend_file in backend_files:
    if os.path.exists(backend_file):
        datas.append((backend_file, os.path.dirname(backend_file) or '.'))

# Hidden imports for all dependencies
hiddenimports = []
hiddenimports += collect_submodules('fastapi')
hiddenimports += collect_submodules('uvicorn')
hiddenimports += collect_submodules('httpx')
hiddenimports += collect_submodules('pydantic')
hiddenimports += collect_submodules('psutil')
hiddenimports += collect_submodules('asyncio')
hiddenimports += collect_submodules('json')
hiddenimports += collect_submodules('logging')
hiddenimports += collect_submodules('threading')
hiddenimports += collect_submodules('subprocess')
hiddenimports += collect_submodules('webbrowser')
hiddenimports += collect_submodules('platform')
hiddenimports += collect_submodules('urllib')
hiddenimports += collect_submodules('zipfile')
hiddenimports += collect_submodules('shutil')
hiddenimports += collect_submodules('pathlib')
hiddenimports += collect_submodules('datetime')

# Specific hidden imports that might be missed
critical_imports = [
    'uvicorn.logging',
    'uvicorn.loops.auto',
    'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets.auto',
    'uvicorn.lifespan.on',
    'fastapi.middleware.cors',
    'fastapi.responses',
    'httpx._client',
    'httpx._auth',
    'httpx._config',
    'pydantic.fields',
    'pydantic.main',
    'pydantic.typing',
    'psutil._psplatform',
    'email.mime.text',
    'email.mime.multipart'
]

hiddenimports.extend(critical_imports)

# Analysis
a = Analysis(
    ['launcher_integrated.py'],  # Use the integrated launcher
    pathex=[PROJECT_ROOT],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib', 'numpy', 'pandas', 'scipy', 'PIL', 'tkinter',
        'pytest', 'sphinx', 'jupyter', 'notebook'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove unnecessary libraries to reduce size
excluded_binaries = ['matplotlib', 'numpy', 'pandas', 'scipy', 'PIL']
a.binaries = [x for x in a.binaries if not any(ex in x[0].lower() for ex in excluded_binaries)]

# Create PYZ
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SIRAJ-Educational-AI-v8.2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console for educational feedback
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='siraj_icon.ico' if os.path.exists('siraj_icon.ico') else None,
    uac_admin=False,
    uac_uiaccess=False,
)

# Create distribution folder
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SIRAJ-Educational-AI-Suite-v8.2',
)
