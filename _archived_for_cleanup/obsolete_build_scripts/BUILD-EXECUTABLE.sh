#!/bin/bash
# SIRAJ Educational AI - Unix/Linux/Mac Build Script
# =================================================

echo "============================================================"
echo "SIRAJ Educational AI - Executable Builder"
echo "Version 8.1.0"
echo "============================================================"
echo

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python installation
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed!${NC}"
    echo "Please install Python 3.11 or higher"
    exit 1
fi

# Check Node.js installation
if ! command -v node &> /dev/null; then
    echo -e "${RED}ERROR: Node.js is not installed!${NC}"
    echo "Please install Node.js 16+ from https://nodejs.org"
    exit 1
fi

# Check npm installation
if ! command -v npm &> /dev/null; then
    echo -e "${RED}ERROR: npm is not installed!${NC}"
    echo "Please install Node.js which includes npm"
    exit 1
fi

echo -e "${GREEN}All prerequisites found!${NC}"
echo

# Function to display menu
show_menu() {
    echo "What would you like to do?"
    echo
    echo "1. Build complete executable (recommended)"
    echo "2. Build frontend only"
    echo "3. Build executable only (frontend must be built first)"
    echo "4. Clean build files"
    echo "5. Exit"
    echo
}

# Function to build all
build_all() {
    echo
    echo "Starting complete build process..."
    echo "This will:"
    echo "- Install all dependencies"
    echo "- Build the React frontend"
    echo "- Create the executable"
    echo "- Package everything for distribution"
    echo
    echo "This may take 10-20 minutes..."
    echo
    read -p "Press Enter to continue..."
    
    python3 build_exe.py
    
    if [ $? -eq 0 ]; then
        echo
        echo "============================================================"
        echo -e "${GREEN}BUILD SUCCESSFUL!${NC}"
        echo
        echo "Your executable is ready in: dist/SIRAJ-Educational-AI"
        echo "Distribution package: dist/SIRAJ-Educational-AI-$(uname -s | tr '[:upper:]' '[:lower:]')-v8.1.0.zip"
        echo
        echo "You can now distribute the .zip file to users."
        echo "============================================================"
    else
        echo
        echo -e "${RED}Build failed! Check the error messages above.${NC}"
    fi
}

# Function to build frontend
build_frontend() {
    echo
    echo "Building frontend only..."
    python3 build_exe.py frontend
}

# Function to build executable
build_exe() {
    echo
    echo "Building executable only..."
    python3 build_exe.py exe
}

# Function to clean
clean() {
    echo
    echo "Cleaning build files..."
    python3 build_exe.py clean
    echo -e "${GREEN}Clean complete!${NC}"
}

# Main loop
while true; do
    show_menu
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            build_all
            ;;
        2)
            build_frontend
            ;;
        3)
            build_exe
            ;;
        4)
            clean
            ;;
        5)
            echo
            echo "Thank you for using SIRAJ Educational AI Builder!"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            echo
            ;;
    esac
    
    echo
    read -p "Press Enter to continue..."
    echo
done
