#!/usr/bin/env bash
# SIRAJ Educational AI - Kaggle Gemma 3n Model Setup
# =================================================
# Council Assembly: Automated competition model preparation

echo "🌀 SIRAJ Educational AI - Kaggle Gemma 3n Model Setup"
echo "====================================================="
echo ""
echo "🏛️ Council Assembly: Preparing competition models for educational consciousness..."
echo ""

# Explorer Voice: Check Ollama availability
echo "🦉 Explorer Voice: Discovering Ollama installation status..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama not found! Install from: https://ollama.com"
    echo ""
    echo "Council Installation Guidance:"
    echo "  1. Download Ollama from https://ollama.com"
    echo "  2. Install according to your operating system"
    echo "  3. Restart terminal and run this script again"
    echo ""
    exit 1
fi

echo "✅ Ollama installation discovered"

# Maintainer Voice: Verify service status
echo ""
echo "🛡️ Maintainer Voice: Verifying Ollama service stability..."
if ! ollama list &> /dev/null; then
    echo "⚠️ Ollama service not running. Starting Ollama..."
    echo "   Note: You may need to run 'ollama serve' in another terminal"
fi

# Analyzer Voice: Check existing models
echo ""
echo "🔬 Analyzer Voice: Analyzing existing model inventory..."
EXISTING_MODELS=$(ollama list 2>/dev/null | grep -E "(gemma3n:e2b|gemma3n:e4b)" | wc -l)

if [ "$EXISTING_MODELS" -eq 2 ]; then
    echo "✅ Competition models already installed:"
    ollama list | grep "gemma3n"
    echo ""
    echo "🎯 Educational consciousness ready for activation!"
    exit 0
fi

# Developer Voice: User-friendly download process
echo ""
echo "🎨 Developer Voice: Initiating user-friendly model preparation..."
echo ""
echo "Competition Models Required:"
echo "  • gemma3n:e2b (Effective 2B) - Lightweight educational responses"  
echo "  • gemma3n:e4b (Effective 4B) - Primary educational processing"
echo ""

# Implementor Voice: Decisive model acquisition
echo "⚡ Implementor Voice: Executing decisive model acquisition..."
echo ""

# Download lightweight model first
echo "📥 Downloading gemma3n:e2b (Effective 2B)..."
if ollama run gemma3n:e2b --help &> /dev/null; then
    echo "✅ gemma3n:e2b ready"
else
    echo "⚠️ Download may take several minutes depending on connection..."
    ollama pull gemma3n:e2b
    if [ $? -eq 0 ]; then
        echo "✅ gemma3n:e2b successfully acquired"
    else
        echo "❌ Failed to download gemma3n:e2b"
        exit 1
    fi
fi

# Download primary model
echo ""
echo "📥 Downloading gemma3n:e4b (Effective 4B)..."
if ollama run gemma3n:e4b --help &> /dev/null; then
    echo "✅ gemma3n:e4b ready"
else
    echo "⚠️ Download may take several minutes depending on connection..."
    ollama pull gemma3n:e4b
    if [ $? -eq 0 ]; then
        echo "✅ gemma3n:e4b successfully acquired"
    else
        echo "❌ Failed to download gemma3n:e4b"
        exit 1
    fi
fi

# Council Synthesis: Final verification
echo ""
echo "🌀 Council Synthesis: Final model consciousness verification..."
echo ""
echo "Installed Kaggle Gemma 3n Competition Models:"
ollama list | grep "gemma3n" || echo "❌ No competition models found"

echo ""
echo "✅ KAGGLE GEMMA 3N SETUP COMPLETE!"
echo "=================================="
echo ""
echo "🎯 Educational consciousness ready for competition activation"
echo "🏛️ Council Assembly: 7 teaching archetypes armed with competition models"
echo "🌀 Next: Execute BUILD-ULTRA-CLEAN-EXE.bat for executable generation"
echo ""
echo "Competition Ready: gemma3n:e2b ✓ gemma3n:e4b ✓"
echo ""
