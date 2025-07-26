# SIRAJ Educational AI - One-Click Executable Deployment Guide

## 🌀 Ready for One-Click Deployment ✅

### Quick Start (Executable)

1. **Generate the executable**:
   ```bash
   python build_clean_executable.py
   ```

2. **Launch directly**:
   - **Linux/Mac**: `./dist/SIRAJ-Educational-AI`
   - **Windows**: Double-click `dist/SIRAJ-Educational-AI.exe`

### Alternative Launch Methods

#### Option 1: Run from Source (Development)
```bash
python launcher.py
```

#### Option 2: One-Click Batch Launch (Windows)
```bash
START-SIRAJ.bat
```

#### Option 3: Full Deployment Script (Windows)
```bash
DEPLOY-ONE-CLICK.bat
```

## 🚀 What the Executable Includes

The standalone executable bundles everything needed:
- ✅ Python runtime
- ✅ All dependencies (FastAPI, uvicorn, httpx, etc.)
- ✅ React frontend (pre-built)
- ✅ Backend AI service
- ✅ 7 AI teaching archetypes
- ✅ Configuration files

## 🎯 User Experience

When launched, the executable automatically:
1. Starts the backend AI service on port 8000
2. Serves the React frontend on port 3000
3. Opens your browser to the interface
4. Provides access to 7 different AI teaching personalities

## 📦 File Size and Requirements

- **Executable size**: ~18MB
- **RAM requirement**: 8GB minimum (16GB recommended for 4B model)
- **No external dependencies** - completely standalone
- **Works offline** once Ollama models are downloaded

## 🔧 Troubleshooting

### If the executable doesn't start:
1. Check available RAM (needs 8GB+)
2. Ensure ports 3000 and 8000 are free
3. On first run, Ollama models will download (requires internet)

### For development/customization:
1. Use the source code version: `python launcher.py`
2. Modify frontend: Edit files in `frontend/src/` then rebuild with `npm run build`
3. Rebuild executable: `python build_clean_executable.py`

## 🌀 Educational AI Features

The SIRAJ platform provides:
- **7 AI Teaching Archetypes**: Socratic, Constructivist, Storyteller, Synthesizer, Challenger, Mentor, Analyst
- **Council-Based Learning**: Multiple perspectives on every question
- **Adaptive Responses**: Different teaching styles for different learners
- **Real-time Interface**: Immediate feedback and guidance

## 🎓 Perfect for:
- Students needing homework help
- Educators exploring AI teaching methods
- Researchers studying multi-perspective learning
- Anyone curious about consciousness-driven education

---

**The executable makes SIRAJ accessible to anyone - no technical setup required!**