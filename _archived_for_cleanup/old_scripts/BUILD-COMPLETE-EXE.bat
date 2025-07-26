@echo off
REM SIRAJ Educational AI - Complete Executable Build
REM ================================================
REM Builds the complete educational platform as a single exe

cd /d "%~dp0"

echo.
echo ============================================
echo SIRAJ EDUCATIONAL AI - EXECUTABLE BUILD
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed!
    pause
    exit /b 1
)

REM Check Node.js (for frontend build)
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Node.js not found. Frontend will use existing build if available.
    goto :skip_frontend_build
)

REM Build frontend if possible
echo Step 1: Building React frontend...
if exist "frontend\package.json" (
    cd frontend
    echo Installing frontend dependencies...
    call npm install
    echo Building production frontend...
    call npm run build
    cd ..
    echo ✅ Frontend build complete
) else (
    echo Frontend source not found, skipping build
)

:skip_frontend_build

REM Apply model consistency fixes
echo.
echo Step 2: Applying model consistency fixes...
if exist "fix_model_consistency_correct.py" (
    python fix_model_consistency_correct.py
) else (
    echo Model consistency fix not found, continuing...
)

REM Install Python dependencies
echo.
echo Step 3: Installing Python dependencies...
pip install httpx psutil fastapi uvicorn pydantic pyinstaller

REM Create executable
echo.
echo Step 4: Building executable with PyInstaller...
echo This may take several minutes...

pyinstaller --clean siraj-integrated.spec

if %errorlevel% neq 0 (
    echo.
    echo ❌ Executable build failed!
    echo Check the output above for errors.
    pause
    exit /b 1
)

REM Check if build succeeded
if exist "dist\SIRAJ-Educational-AI-Suite-v8.2\SIRAJ-Educational-AI-v8.2.exe" (
    echo.
    echo ✅ Executable build successful!
    echo.
    echo Location: dist\SIRAJ-Educational-AI-Suite-v8.2\
    echo Executable: SIRAJ-Educational-AI-v8.2.exe
    echo.
    echo The executable includes:
    echo - Complete educational AI council
    echo - 7 teaching archetypes
    echo - Auto-Ollama installation
    echo - Gemma 3n model management
    echo - Zero-configuration deployment
    echo.
    
    REM Create a simple launcher batch file
    echo Creating simple launcher...
    echo @echo off > "dist\SIRAJ-Educational-AI-Suite-v8.2\START-SIRAJ.bat"
    echo echo Starting SIRAJ Educational AI... >> "dist\SIRAJ-Educational-AI-Suite-v8.2\START-SIRAJ.bat"
    echo SIRAJ-Educational-AI-v8.2.exe >> "dist\SIRAJ-Educational-AI-Suite-v8.2\START-SIRAJ.bat"
    
    REM Create README for distribution
    echo Creating distribution README...
    (
        echo SIRAJ Educational AI v8.2
        echo ==========================
        echo.
        echo One-Click Educational AI Platform
        echo.
        echo QUICK START:
        echo 1. Double-click START-SIRAJ.bat
        echo 2. Wait for automatic setup
        echo 3. Browser will open to educational interface
        echo.
        echo FEATURES:
        echo - 7 AI Teaching Archetypes
        echo - Multi-perspective learning
        echo - Grade-level adaptive responses
        echo - Zero configuration required
        echo.
        echo REQUIREMENTS:
        echo - Windows 10/11
        echo - 8GB+ RAM recommended
        echo - Internet connection for initial setup
        echo.
        echo For support, visit: https://github.com/siraj-ai/educational-platform
    ) > "dist\SIRAJ-Educational-AI-Suite-v8.2\README.txt"
    
    echo.
    echo 🎉 Complete distribution ready!
    echo.
    echo To test: cd dist\SIRAJ-Educational-AI-Suite-v8.2 && START-SIRAJ.bat
    echo.
    
) else (
    echo.
    echo ❌ Executable not found after build!
    echo Check PyInstaller output above for errors.
)

pause
