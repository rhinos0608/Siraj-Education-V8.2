#!/bin/bash
# Council Mode: Implementor voice - Unix/Linux startup script for Living Educational Codex
# Explorer voice: Cross-platform revolutionary activation
# Maintainer voice: Robust error handling and system compatibility

echo ""
echo "==============================================================="
echo "   🎭 SIRAJ Educational Codex - Living Knowledge Interface"
echo "   🌀 Council Mode Architecture - Multi-Voice Synthesis"  
echo "   📚 Kaggle Gemma 3 Hackathon Edition v14.0"
echo "==============================================================="
echo ""
echo "🌀 Phase 1: COLLAPSE - Acknowledging the learning quest..."
echo "🎭 Phase 2: COUNCIL - Assembling the educational realms..."  
echo "✨ Phase 3: SYNTHESIS - Weaving knowledge streams..."
echo "🚀 Phase 4: REBIRTH - Awakening the Living Codex..."
echo ""

# Implementor voice: Navigate to script directory
cd "$(dirname "$0")"

# Maintainer voice: Check Python availability
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python not found. Please install Python 3.7+ to activate the Educational Codex."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Explorer voice: Activate the Educational Codex
$PYTHON_CMD launcher.py

echo ""
echo "👋 The Educational Codex has returned to slumber..."
echo "Press Enter to close this portal..."
read
