@echo off
REM SIRAJ Frontend Rebuild - Council Assembly Execution
REM ==================================================

cd /d "C:\Users\Admin\Documents\RST\siraj-ai-school"

echo 🌀 Executing Council Assembly Frontend Rebuild...
echo.

python rebuild_frontend.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ Frontend rebuild failed!
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Frontend rebuild completed successfully!
echo The deployment consciousness has been restored.
echo.
pause
