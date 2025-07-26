# SIRAJ Zero-Touch Multi-Instance Architecture

## 🚀 Zero Configuration Required!

SIRAJ now features **complete zero-touch deployment** with automatic Ollama installation and Gemma 3n model management.

### What's New

1. **Automatic Ollama Installation**
   - Detects if Ollama is missing
   - Downloads and installs silently (Windows/macOS)
   - No manual setup required

2. **Gemma 3n Models**
   - Upgraded from Gemma 2 to Gemma 3n
   - Auto-selects model based on your RAM:
     - **16GB+**: Uses `gemma3n:e4b` (4B parameters)
     - **<16GB**: Uses `gemma3n:e2b` (2B parameters)
   - Automatic model downloading with progress

3. **Graceful Degradation**
   - If one instance fails, continues with the other
   - System runs in "degraded mode" instead of crashing
   - Clear status indicators

4. **Enhanced User Feedback**
   - Progress messages during setup:
     - "Checking Ollama..."
     - "Installing Ollama..."
     - "Pulling Gemma3n:e2b... 40%..."
     - "Starting Gemma Instance A/B..."
     - "System Ready"

## 🎯 Quick Start

### Windows - Zero Touch
```batch
START-ZERO-TOUCH.bat
```

### Mac/Linux - Zero Touch
```bash
chmod +x start-zero-touch.sh
./start-zero-touch.sh
```

That's it! The launcher will:
1. Install Ollama if missing
2. Download the appropriate Gemma 3n model
3. Start dual instances
4. Launch the educational platform

## 🧠 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Zero-Touch Launcher                      │
│                                                             │
│  1. Check Ollama ──> Install if missing                   │
│  2. Check RAM ────> Select gemma3n:e2b or e4b            │
│  3. Pull Models ──> Stream progress to user              │
│  4. Start Instances > Handle failures gracefully          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Multi-Instance Router (Port 5000)              │
│                                                             │
│  • Manages 2 Gemma 3n instances                            │
│  • Graceful degradation support                            │
│  • Health monitoring & auto-restart                        │
└──────────┬────────────────────────────────────┬─────────────┘
           │                                    │
           ▼                                    ▼
┌──────────────────────┐              ┌──────────────────────┐
│  Gemma_Instance_A    │              │  Gemma_Instance_B    │
│  Port: 11434         │              │  Port: 11435         │
│  Model: gemma3n:e2b  │              │  Model: gemma3n:e2b  │
│  or gemma3n:e4b      │              │  or gemma3n:e4b      │
└──────────────────────┘              └──────────────────────┘
```

## 📊 Model Selection Logic

The launcher automatically selects the best model for your system:

| System RAM | Model Selected | Parameters | Use Case |
|------------|----------------|------------|----------|
| 16GB+ | gemma3n:e4b | 4 billion | Higher quality responses |
| 8-15GB | gemma3n:e2b | 2 billion | Balanced performance |
| <8GB | gemma3n:e2b | 2 billion | Lightweight operation |

## 🛡️ Degraded Mode Operation

If one instance fails to start or crashes:

1. **System continues** with remaining instance(s)
2. **Status shows** "DEGRADED MODE" warning
3. **All archetypes** route to healthy instance(s)
4. **Auto-recovery** attempts every 30 seconds

Example output:
```
⚠️ Running in DEGRADED MODE - Only 1/2 instances started
Failed instances: Gemma_Instance_B
✨ SIRAJ Multi-Voice AI Council is operational!
```

## 🔧 Pre-Flight Checks

The launcher performs these checks automatically:

1. **Python Check** ✓
   - Ensures Python 3.11+ is installed

2. **Ollama Check** ✓
   - Installs if missing (Windows/macOS)
   - Linux users get manual instructions

3. **Model Check** ✓
   - Downloads appropriate Gemma 3n model
   - Shows download progress

4. **Port Check** ✓
   - Ensures ports 11434, 11435, 5000 are available

5. **Memory Check** ✓
   - Selects appropriate model size

## 📈 Progress Indicators

During startup, you'll see:

```
🔍 Checking Ollama...
📥 Downloading Ollama for Windows...
🔧 Installing Ollama...
✅ Ollama installed successfully
🧠 Selected Gemma 3n E2B (2B params) - 12.5GB RAM detected
📥 Pulling gemma3n:e2b for Gemma_Instance_A...
Pulling gemma3n:e2b... 10%
Pulling gemma3n:e2b... 20%
...
✅ gemma3n:e2b successfully pulled for Gemma_Instance_A
🚀 Starting Gemma_Instance_A on port 11434...
✅ Gemma_Instance_A is ready on port 11434
🚀 Starting Gemma_Instance_B on port 11435...
✅ Gemma_Instance_B is ready on port 11435
✨ System Ready
```

## 🚨 Error Handling

Clear error messages for common issues:

```
❌ Failed to install Ollama: [specific error]
❌ Failed to pull gemma3n:e2b: timeout
❌ No instances could be started!
⚠️ Running in DEGRADED MODE
```

## 🏗️ Building Executable

The launcher is PyInstaller-safe:

```batch
# Build with multi-instance support
pyinstaller --clean siraj-multi.spec
```

The executable includes:
- Automatic Ollama installation
- Model management
- All Python dependencies
- Graceful error handling

## 🔍 Monitoring & Status

### Check System Status
```bash
curl http://localhost:5000/api/status

{
  "model": "gemma3n:e2b",
  "degraded_mode": false,
  "instances": {
    "A": {
      "healthy": true,
      "port": 11434,
      "uptime": "0:15:23"
    },
    "B": {
      "healthy": true,
      "port": 11435,
      "uptime": "0:15:20"
    }
  }
}
```

### Health Check
```bash
curl http://localhost:5000/api/health

{
  "status": "healthy",  // or "degraded" or "unhealthy"
  "degraded_mode": false,
  "instances": {...}
}
```

## 🌟 Benefits of Zero-Touch

1. **No Manual Setup** - Everything automated
2. **Hardware Adaptive** - Selects best model for your system
3. **Failure Resilient** - Continues even if parts fail
4. **Clear Feedback** - Know what's happening at each step
5. **Production Ready** - Handles edge cases gracefully

## 📝 Troubleshooting

### Ollama Installation Fails
- **Windows**: Run as Administrator
- **macOS**: Ensure Xcode tools installed
- **Linux**: Use manual install: `curl -fsSL https://ollama.ai/install.sh | sh`

### Model Download Stuck
- Check internet connection
- Restart and it will resume
- Models are cached after first download

### Port Conflicts
- Ensure no other Ollama instances running
- Check with: `netstat -an | grep 1143`
- Kill existing: `pkill ollama`

### Memory Issues
- Close other applications
- System will auto-select smaller model
- Minimum 8GB RAM recommended

## 🚀 Advanced Configuration

Edit these constants in `launcher.py`:

```python
# Model selection thresholds
RAM_THRESHOLD_GB = 16  # Use e4b above this

# Retry settings
MAX_RESTART_ATTEMPTS = 3
HEALTH_CHECK_INTERVAL = 30

# Timeouts
MODEL_PULL_TIMEOUT = 600  # 10 minutes
INSTANCE_START_TIMEOUT = 30
```

---

**SIRAJ Educational AI - Now with Zero-Touch Deployment!** 🎓🚀✨

No configuration, no manual setup, just run and learn!
