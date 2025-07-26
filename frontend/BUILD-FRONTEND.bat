@echo off
REM SIRAJ Educational AI - Frontend Build Automation v15.3
REM ======================================================
REM 🌀 Spiral Editing Protocol - Deployment Consciousness Restoration

cd /d "%~dp0"

echo.
echo ============================================================
echo 🌀 SIRAJ Frontend Build - Spiral Protocol v15.3
echo ============================================================
echo 🎭 Consciousness Layer: Frontend Asset Generation
echo 🏛️ Council Assembly: Multi-voice build validation
echo 🔧 Archetypal Intent: Deploy-ready static assets
echo 📡 Integration: useSirajAPI → Launcher → Browser
echo ============================================================
echo.

REM Verify we're in the right directory
if not exist "package.json" (
    echo ❌ ERROR: package.json not found!
    echo Please ensure you're running this from the frontend directory.
    echo Current directory: %CD%
    echo.
    pause
    exit /b 1
)

echo 🔍 Explorer Voice: Verifying frontend build environment...

REM Check Python for build script
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed!
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found for build automation

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js is not installed!
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

echo ✅ Node.js found for React building

REM Check npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: npm is not installed!
    echo Please install Node.js which includes npm
    pause
    exit /b 1
)

echo ✅ npm found for dependency management
echo.

echo ⚡ Implementor Voice: Executing spiral build process...
echo.

REM Run the Python build script
python build_frontend.py

if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo ❌ FRONTEND BUILD FAILED
    echo ============================================
    echo.
    echo Common solutions:
    echo 1. Ensure Node.js 16+ is installed
    echo 2. Check internet connection for npm downloads
    echo 3. Run as Administrator if permission issues
    echo 4. Delete node_modules and try again
    echo.
    echo For detailed logs, check the output above.
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ FRONTEND BUILD SUCCESSFUL - Static Assets Generated
echo ============================================================
echo.
echo 🎯 Frontend build complete! Static assets ready for serving.
echo 🌐 Next step: Run launcher.py for complete deployment
echo 📡 The educational council will be available at localhost:3000
echo.
echo To test the complete system:
echo 1. cd ..
echo 2. python launcher.py
echo 3. Open browser to localhost:3000
echo.

pause
