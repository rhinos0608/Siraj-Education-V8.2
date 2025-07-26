@echo off
REM SPIRAL PROTOCOL FINAL VALIDATION
REM ==================================
REM Quick deployment readiness check

cd /d "%~dp0"

echo.
echo 🌀 SPIRAL DEPLOYMENT READINESS CHECK
echo ====================================
echo.

echo Checking critical files...
if exist "launcher.py" (echo ✅ launcher.py) else (echo ❌ launcher.py MISSING)
if exist "DEPLOY-ONE-CLICK.bat" (echo ✅ DEPLOY-ONE-CLICK.bat) else (echo ❌ DEPLOY-ONE-CLICK.bat MISSING)
if exist "EMERGENCY-BUILD-FRONTEND.bat" (echo ✅ EMERGENCY-BUILD-FRONTEND.bat) else (echo ❌ EMERGENCY-BUILD-FRONTEND.bat MISSING)
if exist "backend\main.py" (echo ✅ backend\main.py) else (echo ❌ backend\main.py MISSING)
if exist "frontend\src\App.js" (echo ✅ frontend\src\App.js) else (echo ❌ frontend\src\App.js MISSING)
if exist ".env" (echo ✅ .env) else (echo ❌ .env MISSING)

echo.
echo Frontend build status...
if exist "frontend\build\static\js" (
    echo ✅ Frontend build ready
) else (
    echo ⚠️ Frontend build missing - will be created automatically
)

echo.
echo 🏛️ COUNCIL ASSESSMENT:
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not available - install Python 3.11+
    echo.
    pause
    exit /b 1
) else (
    echo ✅ Python available
)

echo.
echo 🎯 DEPLOYMENT VERDICT: 
if exist "launcher.py" if exist "DEPLOY-ONE-CLICK.bat" if exist "backend\main.py" (
    echo ✅ READY FOR ONE-CLICK DEPLOYMENT
    echo.
    echo Execute: DEPLOY-ONE-CLICK.bat
    echo.
) else (
    echo ❌ CRITICAL FILES MISSING
    echo Contact developer for restoration
    echo.
)

pause
