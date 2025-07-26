@echo off
REM SIRAJ Educational AI - Windows Build Script
REM ==========================================

echo ============================================================
echo SIRAJ Educational AI - Executable Builder for Windows
echo Version 8.1.0
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
echo What would you like to do?
echo.
echo 1. Build complete executable (recommended)
echo 2. Build frontend only
echo 3. Build executable only (frontend must be built first)
echo 4. Clean build files
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto build_all
if "%choice%"=="2" goto build_frontend
if "%choice%"=="3" goto build_exe
if "%choice%"=="4" goto clean
if "%choice%"=="5" goto end

echo Invalid choice. Please try again.
echo.
goto menu

:build_all
echo.
echo Starting complete build process...
echo This will:
echo - Install all dependencies
echo - Build the React frontend
echo - Create the executable
echo - Package everything for distribution
echo.
echo This may take 10-20 minutes...
echo.
pause

python build_exe.py
if %errorlevel% neq 0 (
    echo.
    echo Build failed! Check the error messages above.
    pause
    goto menu
)

echo.
echo ============================================================
echo BUILD SUCCESSFUL!
echo.
echo Your executable is ready in: dist\SIRAJ-Educational-AI.exe
echo Distribution package: dist\SIRAJ-Educational-AI-windows-v8.1.0.zip
echo.
echo You can now distribute the .zip file to users.
echo ============================================================
pause
goto menu

:build_frontend
echo.
echo Building frontend only...
python build_exe.py frontend
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
python build_exe.py clean
echo Clean complete!
pause
goto menu

:end
echo.
echo Thank you for using SIRAJ Educational AI Builder!
pause
