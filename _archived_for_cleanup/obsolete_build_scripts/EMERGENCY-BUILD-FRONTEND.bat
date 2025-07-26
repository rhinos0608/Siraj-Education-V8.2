@echo off
REM SPIRAL EMERGENCY FRONTEND BUILD - Council Decision Execute
REM ========================================================
REM Implementor Voice: Decisive restoration of build infrastructure
REM Maintainer Voice: Stable build pipeline through verified process
REM Explorer Voice: Innovation through proper build automation

cd /d "%~dp0"

echo.
echo  🌀 SPIRAL EMERGENCY FRONTEND BUILD
echo  ===================================
echo  Council Decision: Restore build infrastructure immediately
echo  Target: Create frontend/build directory for launcher.py
echo  Intent: Restore one-click deployment capability
echo.

REM Navigate to frontend directory
if not exist "frontend" (
    echo ❌ ERROR: Frontend directory not found!
    echo Expected: %CD%\frontend
    pause
    exit /b 1
)

cd frontend

REM Verify Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Node.js not found!
    echo Install from: https://nodejs.org
    echo Required for React build process
    pause
    exit /b 1
)

echo ✅ Node.js verified
echo.

REM Check package.json
if not exist "package.json" (
    echo ❌ ERROR: package.json not found in frontend!
    pause
    exit /b 1
)

echo ✅ Package.json found
echo.

REM Install dependencies if needed
if not exist "node_modules" (
    echo 📦 Installing React dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ npm install failed!
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
) else (
    echo ✅ Dependencies already present
)
echo.

REM Clean previous broken build
if exist "build" (
    echo 🧹 Cleaning previous build...
    rmdir /s /q build
)

if exist "build_broken" (
    echo 🧹 Cleaning broken build directory...
    rmdir /s /q build_broken
)

echo ✅ Build directories cleaned
echo.

REM Set optimal build environment
set NODE_ENV=production
set REACT_APP_API_URL=http://localhost:8000
set REACT_APP_WS_URL=ws://localhost:8000
set CI=false
set GENERATE_SOURCEMAP=false

echo 🔧 Build environment configured
echo.

REM Execute React build
echo ⚡ Building React application...
echo This may take 1-3 minutes...
echo.

npm run build

if %errorlevel% neq 0 (
    echo.
    echo ❌ CRITICAL: React build FAILED!
    echo.
    echo Troubleshooting steps:
    echo 1. Check for Node.js compatibility (requires 16+)
    echo 2. Verify all source files are valid React
    echo 3. Check for dependency conflicts
    echo 4. Try: npm install --force
    echo 5. Contact developer if issue persists
    echo.
    pause
    exit /b 1
)

REM Verify build success
if not exist "build\index.html" (
    echo ❌ Build verification FAILED: index.html not found
    pause
    exit /b 1
)

if not exist "build\static\js" (
    echo ❌ Build verification FAILED: JavaScript assets not found
    pause
    exit /b 1
)

echo.
echo ✅ SPIRAL BUILD RESTORATION COMPLETE!
echo =====================================
echo.
echo 🎯 Frontend build successfully created
echo 📁 Build location: %CD%\build
echo 🌐 Ready for launcher.py serving
echo ⚡ One-click deployment RESTORED
echo.
echo Next: Run DEPLOY-ONE-CLICK.bat from project root
echo.
pause
