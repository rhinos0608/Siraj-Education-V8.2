# Building SIRAJ Educational AI Executable

This guide explains how to build a standalone executable for SIRAJ Educational AI that can be distributed to users without requiring them to install Python, Node.js, or any development tools.

## 🎯 What Gets Built

The build process creates:
- A single executable file (`SIRAJ-Educational-AI.exe` on Windows, `SIRAJ-Educational-AI` on Mac/Linux)
- A distribution package (`.zip` file) containing:
  - The executable
  - Configuration files
  - Documentation
  - Quick start scripts

## 📋 Prerequisites

Before building, ensure you have:

1. **Python 3.11+** installed
2. **Node.js 16+** and npm installed
3. **Git** (to clone the repository)
4. **Ollama** (will be checked at runtime)

## 🚀 Quick Build

### Windows
```batch
BUILD-EXECUTABLE.bat
```
Then select option 1 for a complete build.

### Mac/Linux
```bash
chmod +x BUILD-EXECUTABLE.sh
./BUILD-EXECUTABLE.sh
```
Then select option 1 for a complete build.

## 🔧 Manual Build Steps

If you prefer to run the build manually:

```bash
# 1. Install Python dependencies
pip install -r backend/requirements.txt
pip install pyinstaller

# 2. Build the React frontend
cd frontend
npm install
npm run build
cd ..

# 3. Create the executable
python build_exe.py
```

## 📁 Build Output

After a successful build, you'll find:

```
dist/
├── SIRAJ-Educational-AI.exe (or no extension on Mac/Linux)
└── SIRAJ-Educational-AI-[platform]-v8.1.0.zip
```

The `.zip` file is ready for distribution and includes everything users need.

## 🎨 Customization

### Adding an Icon
1. Create a `.ico` file (Windows) or `.icns` file (Mac)
2. Name it `siraj_icon.ico`
3. Place it in the project root
4. The build will automatically use it

### Modifying Build Settings
Edit `siraj.spec` to customize:
- Excluded modules (to reduce size)
- Additional data files
- Runtime options
- Version information

## 🐛 Troubleshooting

### "Module not found" errors
- Ensure all dependencies are installed: `pip install -r backend/requirements.txt`
- Check that hidden imports are specified in `siraj.spec`

### Large executable size
- The executable includes Python runtime and all dependencies
- Typical size: 50-150 MB (compressed)
- Use UPX compression (enabled by default) to reduce size

### Frontend not loading
- Ensure `npm run build` completed successfully
- Check that `frontend/build` directory exists
- Verify the build is included in the executable

### Antivirus warnings
- Some antivirus software may flag PyInstaller executables
- This is a false positive - sign your executable for production use
- Add to antivirus whitelist during development

## 🔒 Security Considerations

For production distribution:

1. **Code Signing**: Sign the executable with a code signing certificate
2. **Environment Variables**: Never include sensitive data in the build
3. **API Keys**: Use `.env` files that users configure locally
4. **Updates**: Implement a secure update mechanism

## 📦 Distribution

The generated `.zip` file includes:

```
SIRAJ-Educational-AI-Package/
├── SIRAJ-Educational-AI.exe
├── START-SIRAJ.bat (or .sh)
├── .env.example
├── README.md
├── PROJECT_COMPLETE.md
├── QUICK-START.txt
└── LICENSE
```

Users only need to:
1. Extract the `.zip` file
2. Install Ollama (if not already installed)
3. Run the START script
4. The app will open in their browser

## 🎯 Platform-Specific Notes

### Windows
- Executable is built with Windows 10/11 compatibility
- Requires Visual C++ Redistributables (usually pre-installed)
- Windows Defender may scan on first run

### macOS
- May require approval in Security & Privacy settings
- Use `xattr -c SIRAJ-Educational-AI` if "damaged" error appears
- Universal binary for Intel and Apple Silicon

### Linux
- Make executable: `chmod +x SIRAJ-Educational-AI`
- May need to install: `sudo apt install libxcb-xinerama0`
- Works on Ubuntu 20.04+, Fedora 35+, etc.

## 🚀 Advanced Options

### Reducing Size
```python
# In siraj.spec, add more excludes:
excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'PIL', 'tkinter', 'qt5', 'PyQt5']
```

### Debug Build
```bash
python build_exe.py --debug
```

### Clean Build
```bash
python build_exe.py clean
```

## 📞 Support

If you encounter issues:
1. Check the console output for errors
2. Ensure all prerequisites are installed
3. Try a clean build: `python build_exe.py clean` then rebuild
4. Open an issue on GitHub with the error message

---

**Happy Building! 🎓🤖✨**
