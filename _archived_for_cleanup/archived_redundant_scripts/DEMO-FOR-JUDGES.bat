@echo off
rem =============================================================================
rem Council Mode: Enhanced Educational Codex - Demonstration for Judges
rem Pattern: One-click demonstration launch for Kaggle Gemma 3 Hackathon
rem Voices: Presenter (lead), Explorer, Architect, Developer, Implementor
rem =============================================================================

title SIRAJ Enhanced Educational Codex - Judge Demonstration

echo.
echo ================================================================================
echo   🏆 KAGGLE GEMMA 3 HACKATHON - ENHANCED EDUCATIONAL CODEX DEMONSTRATION
echo   🎭 Revolutionary Multi-Archetypal AI Education System
echo   🌀 Council Mode Architecture - Living Knowledge Universe  
echo ================================================================================
echo.

cd /d "%~dp0"

echo 🎯 Welcome, Kaggle Judges! This is the Enhanced Educational Codex demonstration.
echo.
echo Revolutionary Features:
echo   🧠 7 AI Archetypal Teachers with Unique Personalities
echo   📊 Advanced Learning Analytics Dashboard  
echo   📚 Intelligent Curriculum Alignment Engine
echo   📈 Adaptive Progress Tracking System
echo   📝 Multi-Perspective Homework Assistant
echo   🎨 Immersive World Anvil + Notion Interface
echo   ⚡ Real-time Council Assembly and Streaming
echo.

echo Choose your demonstration experience:
echo.
echo   [1] FULL LIVE DEMO - Start Enhanced Codex + Run Demo
echo   [2] SYSTEM DEMO ONLY - Just run the demonstration script  
echo   [3] AUDIT RESULTS - Show comprehensive system audit
echo   [4] QUICK START - Launch Enhanced Codex for exploration
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto :full_demo
if "%choice%"=="2" goto :demo_only
if "%choice%"=="3" goto :audit_only
if "%choice%"=="4" goto :quick_start

:full_demo
echo.
echo 🚀 Starting Full Live Demonstration...
echo.
echo Phase 1: Launching Enhanced Educational Codex...
start "Enhanced Codex" cmd /c "START-ENHANCED-CODEX.bat"

echo Waiting for system initialization...
timeout /t 10 /nobreak > nul

echo.
echo Phase 2: Running Comprehensive Demonstration...
python demo-enhanced-codex.py

echo.
echo 🎭 Live system should now be running at http://localhost:3000
echo 📖 Explore the Enhanced Educational Codex interface!
goto :end

:demo_only
echo.
echo 🎯 Running Demonstration Script Only...
echo.
python demo-enhanced-codex.py
goto :end

:audit_only
echo.
echo 📊 Running Comprehensive System Audit...
echo.
python enhanced-council-audit.py
goto :end

:quick_start
echo.
echo ⚡ Quick Starting Enhanced Educational Codex...
echo.
call START-ENHANCED-CODEX.bat
goto :end

:end
echo.
echo ================================================================================
echo   🏆 Thank you for exploring the Enhanced Educational Codex!
echo   🌀 Revolutionary AI Education through Council Mode Architecture
echo   📚 Ready to transform learning through Living AI Intelligence
echo ================================================================================
echo.
pause
