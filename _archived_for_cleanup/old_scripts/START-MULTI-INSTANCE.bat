@echo off
REM SIRAJ Multi-Instance Quick Start
REM ================================

echo.
echo   _____ _____ _____            _    
echo  / ____^|_   _^|  __ \     /\   ^| ^|   
echo ^| (___   ^| ^| ^| ^|__) ^|   /  \  ^| ^|   
echo  \___ \  ^| ^| ^|  _  /   / /\ \ ^| ^|   
echo  ____) ^|_^| ^|_^| ^| \ \  / ____ \^| ^|   
echo ^|_____/^|_____^|_^|  \_\/_/    \_\_^|   
echo.
echo  Multi-Instance Educational AI v8.1
echo  Dual Gemma Architecture
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not installed!
    echo Please install Ollama from https://ollama.ai
    pause
    exit /b 1
)

echo Starting SIRAJ Multi-Instance AI...
echo.
echo This will:
echo - Launch TWO Ollama instances (ports 11434 and 11435)
echo - Start the intelligent router (port 5000)
echo - Launch the backend API (port 8000)
echo - Start the frontend UI (port 3000)
echo.
echo Press Ctrl+C to stop all services
echo.

REM Start the multi-instance launcher
python launcher.py

pause
