#!/bin/bash
# SIRAJ Multi-Instance Quick Start
# ================================

clear

echo ""
echo "   _____ _____ _____            _    "
echo "  / ____|_   _|  __ \     /\   | |   "
echo " | (___   | | | |__) |   /  \  | |   "
echo "  \___ \  | | |  _  /   / /\ \ | |   "
echo "  ____) |_| |_| | \ \  / ____ \| |   "
echo " |_____/|_____|_|  \_\/_/    \_\_|   "
echo ""
echo "  Multi-Instance Educational AI v8.1"
echo "  🧠 Dual Gemma Architecture"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed!${NC}"
    echo "Please install Python 3.11+ first"
    exit 1
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}ERROR: Ollama is not installed!${NC}"
    echo "Please install Ollama from https://ollama.ai"
    exit 1
fi

echo -e "${GREEN}Starting SIRAJ Multi-Instance AI...${NC}"
echo ""
echo "This will:"
echo "- Launch TWO Ollama instances (ports 11434 and 11435)"
echo "- Start the intelligent router (port 5000)"
echo "- Launch the backend API (port 8000)"
echo "- Start the frontend UI (port 3000)"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Make sure we're in the right directory
cd "$(dirname "$0")"

# Start the multi-instance launcher
python3 launcher.py
