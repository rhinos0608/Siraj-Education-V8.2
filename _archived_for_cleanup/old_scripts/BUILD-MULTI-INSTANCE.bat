@echo off
REM SIRAJ Educational AI - Enhanced Multi-Instance Build Script
REM ==========================================================

echo ============================================================
echo SIRAJ Educational AI - Multi-Instance Executable Builder
echo Version 8.1.0 - Dual Gemma Architecture
echo ============================================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.11 or higher from https://python.org
    pause
    exit /b 1
)

REM Check Node.js installation
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH!
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

REM Check npm installation
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: npm is not installed!
    echo Please install Node.js which includes npm
    pause
    exit /b 1
)

echo All prerequisites found!
echo.

REM Main menu
:menu
echo What would you like to build?
echo.
echo 1. Multi-Instance Executable (NEW - Recommended)
echo 2. Standard Single-Instance Executable
echo 3. Build frontend only
echo 4. Build executable only (frontend must be built first)
echo 5. Clean build files
echo 6. Exit
echo.

set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto build_multi
if "%choice%"=="2" goto build_standard
if "%choice%"=="3" goto build_frontend
if "%choice%"=="4" goto build_exe
if "%choice%"=="5" goto clean
if "%choice%"=="6" goto end

echo Invalid choice. Please try again.
echo.
goto menu

:build_multi
echo.
echo ============================================================
echo Building MULTI-INSTANCE Executable
echo ============================================================
echo.
echo This will create an executable with:
echo - Dual Ollama instance management
echo - Intelligent request routing
echo - True multi-voice AI architecture
echo - Auto-failover and health monitoring
echo.
echo This build is larger but provides TRUE multi-archetype AI!
echo.
pause

REM Install additional dependencies for multi-instance
echo Installing multi-instance dependencies...
pip install httpx psutil

REM Build frontend first
echo.
echo Building frontend...
cd frontend
call npm install
call npm run build
cd ..

if not exist "frontend\build" (
    echo ERROR: Frontend build failed!
    pause
    goto menu
)

REM Build multi-instance executable
echo.
echo Building multi-instance executable...
python -m PyInstaller --clean --noconfirm siraj-multi.spec

if %errorlevel% neq 0 (
    echo.
    echo Build failed! Check the error messages above.
    pause
    goto menu
)

echo.
echo ============================================================
echo MULTI-INSTANCE BUILD SUCCESSFUL!
echo.
echo Your executable: dist\SIRAJ-Educational-AI-MultiInstance.exe
echo.
echo Features included:
echo - Dual Gemma instances for true multi-voice AI
echo - 5x faster council responses
echo - Automatic failover and health monitoring  
echo - Unified router API
echo.
echo To run: Double-click the executable or use:
echo   SIRAJ-Educational-AI-MultiInstance.exe
echo ============================================================
pause
goto menu

:build_standard
echo.
echo Building standard single-instance executable...
python build_exe.py
pause
goto menu

:build_frontend
echo.
echo Building frontend only...
cd frontend
call npm install
call npm run build
cd ..
echo Frontend build complete!
pause
goto menu

:build_exe
echo.
echo Building executable only...
python build_exe.py exe
pause
goto menu

:clean
echo.
echo Cleaning build files...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
rmdir /s /q __pycache__ 2>nul
del *.spec.log 2>nul
echo Clean complete!
pause
goto menu

:end
echo.
echo Thank you for using SIRAJ Educational AI Builder!
echo.
echo Remember: The multi-instance build provides the best
echo educational experience with true multi-voice AI!
echo.
pause
