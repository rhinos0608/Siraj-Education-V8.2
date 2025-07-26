@echo off
REM Quick Ollama Setup for Testing
REM ==============================

echo.
echo Quick Ollama Setup
echo ==================
echo.

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama not installed!
    echo.
    echo Please:
    echo 1. Download from: https://ollama.com
    echo 2. Install it
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Starting Ollama service...
start /b ollama serve

echo.
echo Waiting for Ollama to start...
timeout /t 5 /nobreak >nul

echo.
echo Pulling tiny test model (tinyllama - only 637MB)...
ollama pull tinyllama

echo.
echo ✅ Setup complete!
echo.
echo Now you can run SIRAJ with a working model:
echo python launcher.py
echo.
pause
