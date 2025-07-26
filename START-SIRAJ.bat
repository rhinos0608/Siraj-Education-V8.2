@echo off
REM SIRAJ Educational AI - Quick Start Script
REM =========================================
REM 🌀 Simplified one-click launch for Windows

cd /d "%~dp0"

echo.
echo  ====================================================
echo    SIRAJ Educational AI - Multi-Voice Learning
echo  ====================================================
echo    🎓 7 AI Teaching Archetypes
echo    🤖 Powered by Gemma 3n Models
echo    🌐 Opening at http://localhost:3000
echo  ====================================================
echo.

REM Quick Python check
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.11+ from https://python.org
    echo.
    pause
    exit /b 1
)

REM Launch the system
echo 🚀 Starting SIRAJ Educational AI...
echo.
python launcher.py

pause
