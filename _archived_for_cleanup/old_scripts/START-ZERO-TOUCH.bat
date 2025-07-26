@echo off
REM SIRAJ Multi-Instance Zero-Touch Launcher
REM ========================================
REM Auto-installs Ollama and Gemma 3n models

echo.
echo   _____ _____ _____            _    
echo  / ____^|_   _^|  __ \     /\   ^| ^|   
echo ^| (___   ^| ^| ^| ^|__) ^|   /  \  ^| ^|   
echo  \___ \  ^| ^| ^|  _  /   / /\ \ ^| ^|   
echo  ____) ^|_^| ^|_^| ^| \ \  / ____ \^| ^|   
echo ^|_____/^|_____^|_^|  \_\/_/    \_\_^|   
echo.
echo  Zero-Touch Educational AI v8.1
echo  Powered by Gemma 3n Technology
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.11+ from https://python.org
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo Starting SIRAJ Zero-Touch Setup...
echo.
echo This will automatically:
echo [1] Check and install Ollama if needed
echo [2] Download Gemma 3n model (auto-selected for your hardware)
echo [3] Start dual AI instances
echo [4] Launch the educational platform
echo.
echo No manual setup required!
echo.

REM Install required Python packages if missing
echo Checking Python dependencies...
pip show httpx >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing required packages...
    pip install httpx psutil fastapi uvicorn pydantic
)

REM Start the zero-touch launcher
echo Launching SIRAJ Educational AI...
echo.
python launcher.py

if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo Setup failed! Please check the error above.
    echo ============================================
    echo.
    echo Common issues:
    echo - Ensure you have admin rights
    echo - Check internet connection
    echo - Verify Python 3.11+ is installed
    echo.
)

pause
