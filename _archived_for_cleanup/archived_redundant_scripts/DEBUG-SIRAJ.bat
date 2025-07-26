@echo off
REM SIRAJ Debug Helper
REM ==================

echo.
echo SIRAJ Debug Information
echo ======================
echo.

REM Check if Ollama is installed
echo 1. Checking Ollama installation...
ollama --version 2>nul
if %errorlevel% equ 0 (
    echo    ✅ Ollama is installed
) else (
    echo    ❌ Ollama NOT installed
    echo    Please install from: https://ollama.com
)
echo.

REM Check if Ollama service is running
echo 2. Checking Ollama service...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ Ollama service is running
) else (
    echo    ❌ Ollama service NOT running
    echo    Try running: ollama serve
)
echo.

REM Check installed models
echo 3. Checking installed models...
ollama list 2>nul
echo.

REM Check Python packages
echo 4. Checking Python packages...
python -c "import httpx, psutil, fastapi, uvicorn; print('   ✅ All packages installed')" 2>nul || echo    ❌ Missing packages
echo.

REM Check if port 3000 is accessible
echo 5. Checking web server...
curl -s http://localhost:3000/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ Web server is running on port 3000
) else (
    echo    ❌ Web server not accessible
)
echo.

echo 6. Manual steps to fix:
echo    a) Install Ollama: https://ollama.com
echo    b) Run in new terminal: ollama serve
echo    c) Pull model manually: ollama pull gemma:2b
echo    d) Then restart SIRAJ
echo.

pause
