# -*- mode: python ; coding: utf-8 -*-
"""
SIRAJ Educational AI - PyInstaller Specification
================================================

This spec file builds the complete SIRAJ Educational AI platform into a single executable.
It includes the FastAPI backend, static frontend files, and all necessary dependencies.
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
datas += collect_data_files('alembic')

# Add frontend build files
if os.path.exists(FRONTEND_DIR):
    datas.append((FRONTEND_DIR, 'frontend/build'))

# Add simple frontend fallback directory (will be created at runtime if needed)
# This ensures the launcher can create a fallback HTML frontend

# Add documentation
if os.path.exists(DOCS_DIR):
    datas.append((DOCS_DIR, 'docs'))

# Add configuration files
datas.append(('.env.example', '.'))
datas.append(('README.md', '.'))
datas.append(('PROJECT_COMPLETE.md', '.'))

# Add backend source files
datas.append((os.path.join(BACKEND_DIR, 'main.py'), 'backend'))
datas.append((os.path.join(BACKEND_DIR, 'extended_endpoints.py'), 'backend'))
if os.path.exists(os.path.join(BACKEND_DIR, 'requirements.txt')):
    datas.append((os.path.join(BACKEND_DIR, 'requirements.txt'), 'backend'))

# Collect all necessary hidden imports
hiddenimports = []
hiddenimports += collect_submodules('fastapi')
hiddenimports += collect_submodules('uvicorn')
hiddenimports += collect_submodules('sqlalchemy')
hiddenimports += collect_submodules('alembic')
hiddenimports += collect_submodules('pydantic')
hiddenimports += collect_submodules('httpx')
hiddenimports += collect_submodules('websockets')
hiddenimports += collect_submodules('aiofiles')
hiddenimports += collect_submodules('python-multipart')
hiddenimports += collect_submodules('jinja2')
hiddenimports += collect_submodules('asyncpg')
hiddenimports += collect_submodules('aiosqlite')
hiddenimports += collect_submodules('redis')
hiddenimports += collect_submodules('passlib')
hiddenimports += collect_submodules('python-jose')
hiddenimports += collect_submodules('email-validator')

# Add specific hidden imports that might be missed
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
    'fastapi.middleware.cors',
    'fastapi.middleware.gzip',
    'fastapi.security',
    'sqlalchemy.dialects.postgresql',
    'sqlalchemy.dialects.sqlite',
    'passlib.handlers.bcrypt',
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
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'PIL', 'tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Remove unnecessary modules to reduce size
a.binaries = [x for x in a.binaries if not x[0].startswith('matplotlib')]
a.binaries = [x for x in a.binaries if not x[0].startswith('numpy')]
a.binaries = [x for x in a.binaries if not x[0].startswith('pandas')]

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
    name='SIRAJ-Educational-AI',
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

# Create additional files for complete distribution
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SIRAJ-Educational-AI-Suite',
)
