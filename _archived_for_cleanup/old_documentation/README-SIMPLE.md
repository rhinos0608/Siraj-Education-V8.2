# SIRAJ Educational AI v8.3

## 🎓 Multi-Archetype Educational AI Council

SIRAJ is an innovative educational platform that uses multiple AI teaching personalities (archetypes) to provide comprehensive learning experiences. Each archetype brings a unique teaching style - from Socratic questioning to hands-on constructivism.

## 🚀 Quick Start

### Option 1: Run from Source (Recommended)
1. **Prerequisites**: Python 3.11+ installed
2. **Start**: Double-click `START-SIRAJ.bat`
3. **Wait**: First run downloads AI models (10-15 minutes)
4. **Learn**: Browser opens automatically when ready

### Option 2: Build Standalone Executable
1. **Prerequisites**: Python 3.11+ and Node.js 16+
2. **Build**: Double-click `BUILD-SIRAJ.bat`
3. **Find**: Executable in `dist/SIRAJ-Educational-AI.exe`
4. **Share**: Distribute the .zip file from dist folder

## 🎭 Educational Archetypes

The AI Council includes 7 teaching personalities:
- **Socratic Teacher**: Guides through strategic questions
- **Constructivist**: Promotes hands-on learning
- **Storyteller**: Teaches through narratives
- **Synthesizer**: Connects ideas across domains
- **Challenger**: Pushes intellectual boundaries
- **Mentor**: Provides supportive guidance
- **Analyst**: Offers systematic analysis

## 🔧 Key Features

- **Auto-Installation**: Ollama AI runtime installs automatically
- **Smart Model Selection**: Chooses AI model based on your RAM
- **Dual Instance Architecture**: Runs two AI instances for better performance
- **Browser Auto-Launch**: Opens when all services are ready
- **Fallback UI**: Creates simple interface if frontend build is missing
- **Graceful Degradation**: Works even if some services fail

## 📋 System Requirements

- **OS**: Windows 10/11 (Mac/Linux experimental)
- **RAM**: 8GB minimum (16GB recommended)
- **Storage**: 10GB free space
- **Internet**: Required for initial model download
- **Ports**: 3000, 5000, 8000, 11434, 11435

## 🛠️ Troubleshooting

### Browser doesn't open automatically
- Wait 30-60 seconds for all services to start
- Manually open: http://localhost:3000
- Check console for error messages

### "Ollama not found" error
- The installer should download it automatically
- If it fails, manually install from: https://ollama.ai

### Port already in use
- Close other applications using ports 3000, 5000, 8000, 11434, 11435
- Or modify port numbers in launcher.py

### Build fails
- Ensure Node.js is installed: https://nodejs.org
- Run `npm install` in the frontend folder
- Check for antivirus interference

## 📁 Project Structure

```
siraj-ai-school/
├── launcher.py          # Main application launcher
├── build_exe.py         # Executable builder script
├── START-SIRAJ.bat      # Quick start script
├── BUILD-SIRAJ.bat      # Build executable script
├── frontend/            # React UI application
├── backend/             # FastAPI backend (if present)
├── docs/                # Documentation
└── old_scripts/         # Archived scripts
```

## 🔒 Privacy & Security

- All AI processing happens locally on your machine
- No data is sent to external servers
- Models are downloaded from official Ollama repository
- Educational conversations remain private

## 📚 Using the Platform

1. **Ask Questions**: Type any educational topic
2. **Select Grade Level**: Elementary to University
3. **Choose Archetypes**: Pick teaching styles that suit you
4. **Explore Responses**: Each archetype provides unique insights
5. **Learn & Grow**: Combine perspectives for deep understanding

## 🤝 Contributing

This is an educational project. Contributions welcome!
- Report issues on GitHub
- Submit pull requests for improvements
- Share your learning experiences

## 📄 License

MIT License - Free for educational use

---

**Need help?** Check the console output for detailed error messages or consult the troubleshooting section above.
