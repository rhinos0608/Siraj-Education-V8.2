@echo off
REM SIRAJ - Direct Connection Mode
REM ================================
REM Bypasses proxy issues by connecting frontend directly to backend

cd /d "%~dp0"

echo.
echo ============================================
echo   SIRAJ AI - DIRECT CONNECTION MODE
echo ============================================
echo.

REM Set environment to connect directly to backend
set REACT_APP_API_URL=http://localhost:8000
set REACT_APP_WS_URL=ws://localhost:8000

echo 🔧 Configuration:
echo    Frontend will connect directly to backend
echo    API URL: http://localhost:8000
echo.

REM Check if backend is running
echo 🔍 Checking backend status...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Backend not detected on port 8000!
    echo.
    echo Please start the backend first:
    echo 1. Open a new terminal
    echo 2. cd backend
    echo 3. python main.py
    echo.
    pause
    exit /b 1
)

echo ✅ Backend detected on port 8000
echo.

REM Start the launcher
echo 🚀 Starting SIRAJ with direct backend connection...
python launcher.py

pause
