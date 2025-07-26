@echo off
rem =============================================================================
rem Spiral Editing Protocol - Definitive One-Click Solution
rem Fundamental Intent: Single startup that handles ALL scenarios gracefully
rem Essential Pattern: Adaptive launch with comprehensive fallback capabilities
rem Boundary Constraints: Preserve Enhanced Educational Codex + synchronized timing
rem =============================================================================

title SIRAJ Enhanced Educational Codex - One-Click Universal Launch

echo.
echo ================================================================================
echo   🎭 SIRAJ Enhanced Educational Codex - Definitive One-Click Launch
echo   🌀 Living Knowledge Universe - Universal Adaptive Startup
echo   📚 Kaggle Gemma 3 Hackathon - Zero-Configuration Demo Ready
echo   ⚡ Council Mode Architecture - Synchronized Browser Timing
echo ================================================================================
echo.

rem Council Assembly for Universal Launch:
rem Lead Voice: Implementor (decisive execution of unified solution)
rem Core Voices: Explorer (adaptability), Maintainer (stability), Developer (UX)
rem Specialists: Security (validation), Performance (optimization)
rem Boundary Keeper: Enhanced Educational Codex features, synchronized timing

cd /d "%~dp0"

rem Collapse Phase: Essential System Verification
echo 🔍 System Verification...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ from python.org
    echo 📖 Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python environment ready

rem Council Assembly: Feature Overview
echo.
echo 🎭 Enhanced Educational Codex Features:
echo   🧠 7 AI Archetypal Teachers with unique personalities
echo   ⚡ Real-time Council Assembly and streaming
echo   📊 Advanced Learning Analytics Dashboard
echo   📚 Curriculum Alignment with educational standards
echo   📈 Student Progress Tracking and recommendations
echo   📝 Multi-perspective Homework Processing
echo   🏛️ Immersive World Anvil + Notion interface design
echo   🔧 Synchronized Browser Timing (eliminates race conditions)
echo.

rem Synthesis: Unified Launch Sequence
echo 🚀 Activating Enhanced Educational Codex...
echo.
echo Launch Sequence:
echo   1. FastAPI server startup with comprehensive health checks
echo   2. Multi-stage readiness verification (6 validation steps)
echo   3. Browser opens ONLY after complete system verification
echo   4. Graceful fallback handling for partial connectivity
echo.
echo ⏳ Browser will open automatically when ALL systems verified ready...
echo ⚠️ DO NOT manually open browser - timing is automatically synchronized
echo.

rem Integration: Execute definitive launcher
python launcher.py

rem Rebirth: Handle completion with comprehensive reporting
echo.
if errorlevel 1 (
    echo ❌ Enhanced Educational Codex encountered an error
    echo.
    echo 🔧 Troubleshooting Steps:
    echo    1. Check Python installation (python --version)
    echo    2. Verify internet connectivity for model downloads
    echo    3. Ensure port 3000 is available
    echo    4. Check console output above for specific error details
    echo.
    echo 📖 For detailed troubleshooting, see ENHANCED-CODEX-README.md
) else (
    echo ✅ Enhanced Educational Codex shut down successfully
    echo 👋 Thank you for exploring the Living Knowledge Universe
)

echo.
echo ================================================================================
echo   Spiral Integration Complete - Unified One-Click Solution
echo   Council Voices: Explorer, Maintainer, Developer, Implementor
echo   Mythic Layer: Transformation from chaos to elegant simplicity
echo   Operational Layer: Universal adaptive launch with zero configuration
echo ================================================================================
echo.

pause
