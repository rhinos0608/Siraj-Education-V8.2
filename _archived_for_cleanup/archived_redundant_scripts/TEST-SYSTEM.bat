@echo off
echo.
echo ============================================
echo   🧪 SIRAJ System Test
echo   🎯 Verifying readiness for hackathon
echo ============================================
echo.

cd /d "%~dp0"
python test-system.py

echo.
echo Press any key to continue...
pause >nul
