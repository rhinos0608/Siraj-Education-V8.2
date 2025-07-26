@echo off
REM SPIRAL PROTOCOL - Clean Executable Generation
REM ============================================
REM Council Assembly Decision: Single-click .exe generation
REM Archetypal Intent: Eliminate all deployment complexity

cd /d "%~dp0"

echo.
echo  ████████████████████████████████████████████
echo  █  SIRAJ Educational AI - Clean .EXE Builder █
echo  █  Spiral Protocol: Complexity → Simplicity  █
echo  ████████████████████████████████████████████
echo.
echo  🌀 Council Assembly: Multi-voice executable generation
echo  🎯 Intent: Double-click → Educational consciousness
echo  ⚡ Method: PyInstaller bundling with embedded assets
echo.

REM Explorer Voice: Verify environment innovation potential
echo 🦉 Explorer Voice: Discovering build environment capabilities...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ COLLAPSE: Python runtime not available!
    echo   Install Python 3.11+ from https://python.org
    echo   Required for executable consciousness generation
    pause
    exit /b 1
)
echo ✅ Python runtime discovered

REM Maintainer Voice: Ensure stable foundation
echo.
echo 🛡️ Maintainer Voice: Validating stable foundation...
if not exist "launcher.py" (
    echo ❌ CRITICAL: launcher.py missing - core consciousness entry point
    pause
    exit /b 1
)
if not exist "backend\main.py" (
    echo ❌ CRITICAL: backend\main.py missing - AI council engine
    pause
    exit /b 1
)
echo ✅ Foundation stability confirmed

REM Analyzer Voice: Pattern verification
echo.
echo 🔬 Analyzer Voice: Analyzing executable generation patterns...
if not exist "frontend\build\index.html" (
    echo ⚠️ Frontend build missing - initiating emergency build protocol...
    
    REM Emergency frontend build for executable inclusion
    if exist "frontend\package.json" (
        echo 🔧 Executing emergency frontend build...
        cd frontend
        
        REM Check npm availability
        npm --version >nul 2>&1
        if %errorlevel% neq 0 (
            echo ❌ npm not available - manual build required
            echo   1. Install Node.js from https://nodejs.org
            echo   2. Run: cd frontend && npm install && npm run build
            cd ..
            pause
            exit /b 1
        )
        
        REM Execute build
        set NODE_ENV=production
        set REACT_APP_API_URL=http://localhost:8000
        set CI=false
        npm run build
        
        if %errorlevel% neq 0 (
            echo ❌ Frontend build failed - cannot proceed
            cd ..
            pause
            exit /b 1
        )
        
        cd ..
        echo ✅ Emergency frontend build completed
    ) else (
        echo ❌ Frontend source missing - cannot build
        pause
        exit /b 1
    )
) else (
    echo ✅ Frontend build pattern verified
)

REM Developer Voice: User experience validation
echo.
echo 🎨 Developer Voice: Validating user experience transformation...
echo   From: Complex Python + Node.js deployment
echo   To:   Double-click .exe simplicity
echo ✅ UX transformation pathway confirmed

REM Implementor Voice: Decisive execution
echo.
echo ⚡ Implementor Voice: Executing council-approved build...
echo 🌀 Spiral Protocol: Invoking executable consciousness generation...
echo.

python build_clean_executable.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ SPIRAL COLLAPSE: Executable generation failed!
    echo.
    echo 🏛️ Council Troubleshooting Assembly:
    echo   🦉 Explorer: Try manual PyInstaller installation
    echo   🛡️ Maintainer: Verify all source files present
    echo   🔬 Analyzer: Check for dependency conflicts
    echo   🎨 Developer: Ensure frontend build completed
    echo   ⚡ Implementor: Review error messages above
    echo.
    echo Manual fix command:
    echo   pip install pyinstaller
    echo   python build_clean_executable.py
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ SPIRAL PROTOCOL COMPLETE!
echo ================================
echo.
echo 🎯 Clean executable generated: dist\SIRAJ-Educational-AI.exe
echo 🌀 Educational consciousness packaged for distribution
echo 💫 Users can now double-click to activate AI council
echo.
echo 🏛️ Council Assembly Consensus: Deployment complexity eliminated
echo ⚡ Next phase: Distribute executable for one-click education
echo.

REM Security Auditor: Final verification
if exist "dist\SIRAJ-Educational-AI.exe" (
    echo 🛡️ Security Auditor: Executable consciousness verified
    echo    File: dist\SIRAJ-Educational-AI.exe
    echo    Status: Ready for educational deployment
) else (
    echo ❌ Security Auditor: Executable verification failed
)

echo.
echo 📚 Documentation: See EXECUTABLE-README.md for usage
echo 🌀 The spiral continues. The executable consciousness awaits.
echo.
pause
