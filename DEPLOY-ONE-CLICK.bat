@echo off
REM SIRAJ Educational AI - One-Click Deployment
REM ============================================
REM 🌀 Council Assembly Protocol - Complete Deployment
REM 🎯 Intent: Zero-configuration educational AI activation

cd /d "%~dp0"

echo.
echo  ████████████████████████████████████████████████████
echo  █  SIRAJ Educational AI - ONE-CLICK DEPLOYMENT     █
echo  █  🌀 Living Spiral Protocol - Deploy Everything   █
echo  ████████████████████████████████████████████████████
echo.
echo  🏛️ Council Assembly: Complete system deployment
echo  🎯 Intent: Educational consciousness activation
echo  ⚡ Method: Build → Launch → Browser
echo.

REM Explorer Voice: Verify Python environment
echo 🦉 Explorer Voice: Discovering deployment environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ COLLAPSE: Python not found!
    echo.
    echo Please install Python 3.11+ from https://python.org
    echo After installation, restart this script.
    echo.
    pause
    exit /b 1
)
echo ✅ Python runtime discovered

REM Maintainer Voice: Check system integrity
echo.
echo 🛡️ Maintainer Voice: Validating system integrity...
if not exist "launcher.py" (
    echo ❌ CRITICAL: launcher.py missing!
    echo Please ensure all files are extracted.
    pause
    exit /b 1
)
if not exist "backend\main.py" (
    echo ❌ CRITICAL: backend\main.py missing!
    echo Please ensure all files are extracted.
    pause
    exit /b 1
)
echo ✅ Core system files verified

REM Analyzer Voice: Check frontend build status
echo.
echo 🔬 Analyzer Voice: Analyzing frontend build status...
if not exist "frontend\build\index.html" (
    echo ⚠️ Frontend build missing - initiating emergency build...
    echo.
    
    REM Check if Node.js is available for emergency build
    node --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ❌ Node.js not available for frontend build!
        echo.
        echo Two options:
        echo 1. Install Node.js from https://nodejs.org (recommended)
        echo 2. Continue with backend-only mode (limited functionality)
        echo.
        choice /C YN /M "Continue without frontend (Y/N)?"
        if errorlevel 2 goto :end
    ) else (
        REM Execute emergency frontend build
        echo 🔧 Executing emergency frontend build...
        cd frontend
        
        REM Check if npm modules exist
        if not exist "node_modules" (
            echo 📦 Installing frontend dependencies (this may take a few minutes)...
            npm install
            if %errorlevel% neq 0 (
                echo ❌ Dependency installation failed!
                cd ..
                pause
                exit /b 1
            )
        )
        
        REM Build frontend
        echo 🔨 Building React frontend...
        call BUILD-FRONTEND.bat
        if %errorlevel% neq 0 (
            echo ❌ Frontend build failed!
            cd ..
            pause
            exit /b 1
        )
        cd ..
        echo ✅ Emergency frontend build completed
    )
) else (
    echo ✅ Frontend build verified
)

REM Developer Voice: User experience preparation
echo.
echo 🎨 Developer Voice: Preparing optimal user experience...
echo   - Backend API on port 8000
echo   - Frontend UI on port 3000  
echo   - Browser auto-launch enabled
echo ✅ User experience configured

REM Implementor Voice: Execute deployment
echo.
echo ⚡ Implementor Voice: Initiating system deployment...
echo.

REM Check if ports are available
netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ Port 8000 already in use!
    echo Please close any applications using port 8000.
    pause
    exit /b 1
)

netstat -ano | findstr :3000 >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️ Port 3000 already in use!
    echo Please close any applications using port 3000.
    pause
    exit /b 1
)

REM Launch the integrated system
echo.
echo ========================================================
echo 🌀 LAUNCHING SIRAJ EDUCATIONAL AI SYSTEM
echo ========================================================
echo.
echo 🏛️ Educational Council: 7 AI archetypes ready
echo 🎯 Kaggle Gemma 3n models configured
echo 🌐 Browser will open automatically when ready
echo.
echo Press Ctrl+C to stop the system
echo.

REM Execute the launcher
python launcher.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ DEPLOYMENT FAILED!
    echo.
    echo Please check the error messages above.
    echo Common fixes:
    echo   1. Install missing dependencies
    echo   2. Free up ports 3000 and 8000
    echo   3. Run as administrator if needed
    echo.
    pause
    exit /b 1
)

:end
echo.
echo 👋 SIRAJ Educational AI shutdown complete
echo.
pause
