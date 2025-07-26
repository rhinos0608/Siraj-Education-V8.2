@echo off
REM Start SIRAJ Backend Service Only
REM =================================

cd /d "%~dp0"

echo.
echo ========================================
echo   SIRAJ Backend Service Starter
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found!
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if backend exists
if not exist "backend\main.py" (
    echo ❌ Backend not found!
    pause
    exit /b 1
)

echo 🚀 Starting backend service on port 8000...
echo.

cd backend
python main.py

pause
