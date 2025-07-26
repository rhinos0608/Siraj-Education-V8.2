@echo off
REM SIRAJ Educational AI - Clean Build Script
REM ========================================

echo.
echo Building SIRAJ Educational AI Executable...
echo.

REM Check PyInstaller
python -m pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller --quiet
)

REM Clean previous builds
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

REM Build executable
echo Creating executable...
pyinstaller siraj-clean.spec --noconfirm

if exist "dist\SIRAJ-Educational-AI.exe" (
    echo.
    echo ========================================
    echo BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable: dist\SIRAJ-Educational-AI.exe
    echo.
) else (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo.
)

pause
