@echo off
REM Council Mode: Implementor voice - Quick verification launcher for Educational Codex
REM Maintainer voice: Reliable testing before full activation
REM Explorer voice: Revolutionary one-click validation

echo.
echo ===============================================================
echo   🧪 SIRAJ Educational Codex - System Verification
echo   🎭 Council Mode: Multi-Voice Testing Protocol
echo   🌀 Living Spiral Methodology: Comprehensive Validation
echo ===============================================================
echo.
echo 🔍 Running comprehensive system verification...
echo ⏳ This will test all Educational Codex components...
echo.

cd /d "%~dp0"

REM Implementor voice: Execute verification
python verify-educational-codex.py

echo.
echo 📊 Verification complete! Review results above.
echo.
echo Press any key to continue...
pause >nul
