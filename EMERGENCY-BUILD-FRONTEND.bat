@echo off
REM SIRAJ Educational AI - Emergency Frontend Build
REM ===============================================
REM 🚨 Emergency protocol for missing frontend build

cd /d "%~dp0"

echo.
echo  ================================================
echo    EMERGENCY FRONTEND BUILD PROTOCOL
echo  ================================================
echo    🚨 Use when frontend/build is missing
echo    🔧 Requires Node.js installed
echo    ⏱️ Takes 2-5 minutes to complete
echo  ================================================
echo.

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js not installed!
    echo.
    echo Please install Node.js first:
    echo 1. Download from https://nodejs.org
    echo 2. Install with default settings
    echo 3. Restart this script
    echo.
    pause
    exit /b 1
)

echo ✅ Node.js found

REM Check npm
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: npm not found!
    echo Please ensure Node.js installation includes npm
    pause
    exit /b 1
)

echo ✅ npm found
echo.

REM Navigate to frontend
cd frontend
if %errorlevel% neq 0 (
    echo ❌ ERROR: frontend directory not found!
    pause
    exit /b 1
)

echo 📦 Installing dependencies (this may take a few minutes)...
npm install
if %errorlevel% neq 0 (
    echo ❌ ERROR: Dependency installation failed!
    echo.
    echo Try these fixes:
    echo 1. Check internet connection
    echo 2. Delete node_modules folder and try again
    echo 3. Run as Administrator
    echo.
    pause
    exit /b 1
)

echo.
echo 🔨 Building React frontend...
set NODE_ENV=production
set REACT_APP_API_URL=http://localhost:8000
set CI=false
npm run build

if %errorlevel% neq 0 (
    echo.
    echo ❌ ERROR: Build failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

cd ..

echo.
echo ================================================
echo ✅ EMERGENCY BUILD COMPLETE!
echo ================================================
echo.
echo Frontend successfully built at: frontend\build
echo.
echo Next steps:
echo 1. Run START-SIRAJ.bat or DEPLOY-ONE-CLICK.bat
echo 2. Open browser to http://localhost:3000
echo.

pause
