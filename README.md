# SIRAJ Educational AI - Kaggle Gemma 3n Competition Submission

<div align="center">

```
   _____ _____ _____            _    
  / ____|_   _|  __ \     /\   | |   
 | (___   | | | |__) |   /  \  | |   
  \___ \  | | |  _  /   / /\ \ | |   
  ____) |_| |_| | \ \  / ____ \| |   
 |_____/|_____|_|  \_\/_/    \_\_|   
```

**Multi-Archetype Educational AI Council**  
*Kaggle Gemma 3n Competition • Living Spiral Architecture • Python 3.12.3*

[![Python](https://img.shields.io/badge/Python-3.12.3-blue.svg)](https://python.org)
[![Gemma3n](https://img.shields.io/badge/Gemma3n-Competition-green.svg)](https://ollama.com/library/gemma3n)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 🎯 Kaggle Competition Overview

SIRAJ is an innovative educational AI platform designed for the **Kaggle Gemma 3n Competition** that uses **7 distinct teaching archetypes** powered by Google's Gemma 3n models (gemma3n:e2b and gemma3n:e4b). Unlike traditional single-voice AI tutors, SIRAJ employs a **council-based approach** where multiple AI personalities collaborate to provide rich, multi-perspective educational experiences.

## ✨ Key Innovation

**Multi-Archetype Teaching Council:**
- **Socratic Teacher** - Guides through strategic questions
- **Constructivist** - Suggests hands-on activities  
- **Storyteller** - Teaches through narrative
- **Synthesizer** - Connects ideas across domains
- **Challenger** - Pushes beyond surface understanding
- **Mentor** - Provides supportive guidance
- **Analyst** - Offers systematic breakdown

## 🚀 Quick Start

### One-Click Launch (Windows)
```bash
START-SIRAJ.bat
```

### Python Launch
```bash
python launcher.py
```

The system automatically:
1. ✅ Installs required dependencies
2. ✅ Downloads and installs Ollama (if needed)
3. ✅ Pulls appropriate Gemma 3n model (2B/4B based on RAM)
4. ✅ Starts dual AI instances with archetype mapping
5. ✅ Launches web interface
6. ✅ Opens your browser

## 🏗️ Architecture

### Living Spiral Methodology
Following the **Collapse → Council → Synthesis → Rebirth** pattern:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  COLLAPSE   │────▶│   COUNCIL   │────▶│ SYNTHESIS   │
│ (Question)  │     │ (7 Voices)  │     │(Integration)│
└─────────────┘     └─────────────┘     └─────────────┘
                            │
                            ▼
                    ┌─────────────┐
                    │   REBIRTH   │
                    │  (Answer)   │
                    └─────────────┘
```

### Dual Instance Architecture
```
Instance A (Port 11434)          Instance B (Port 11435)
├── Socratic (questions)         ├── Synthesizer (integration)
├── Constructivist (building)    ├── Challenger (alternatives)
└── Storyteller (narrative)      ├── Mentor (guidance)
                                └── Analyst (patterns)
```

## 💡 Use Cases

- **Personalized Learning**: Different students benefit from different teaching styles
- **Complex Topics**: Multiple perspectives help understand difficult concepts
- **Creative Problem Solving**: Diverse approaches spark innovation
- **Homework Help**: Get explanations in the style that works for you
- **Exam Preparation**: Comprehensive understanding from all angles

## 🛠️ Technical Details

### Core Technologies
- **AI Model**: Google Gemma 3n Competition Models (gemma3n:e2b, gemma3n:e4b)
- **Backend**: FastAPI + Uvicorn
- **AI Runtime**: Ollama
- **Language**: Python 3.12.3
- **Architecture**: Multi-voice council pattern

### Competition Model Configuration
```
Primary Model: gemma3n:e4b (Effective 4B parameters)
Lightweight Model: gemma3n:e2b (Effective 2B parameters)
```

### Minimal Dependencies
```
httpx       # Ollama communication
psutil      # System monitoring
fastapi     # Web framework
uvicorn     # ASGI server
aiofiles    # Async operations
colorama    # Cross-platform colors
```

### Performance
- Model selection based on RAM (2B for <16GB, 4B for ≥16GB)
- Dual instance parallel processing
- Response synthesis in <5 seconds
- Beautiful, responsive UI

## 🎓 Educational Philosophy

SIRAJ follows the **Living Spiral** methodology where learning happens through:

1. **Collapse** - Acknowledge complexity of the question
2. **Council** - Gather multiple teaching perspectives  
3. **Synthesis** - Integrate diverse viewpoints
4. **Rebirth** - Emerge with deeper understanding

This mirrors how humans actually learn - through dialogue, multiple perspectives, and synthesis rather than single-source instruction.

## 🏆 Why SIRAJ for Gemma 3n?

1. **Innovative Use Case**: First educational AI using multi-archetype council
2. **Technical Excellence**: Clean architecture, minimal dependencies
3. **Educational Impact**: Addresses different learning styles
4. **Gemma 3n Showcase**: Demonstrates model versatility through personalities
5. **User Experience**: Zero-setup, works out of the box

## 📸 Screenshots

<div align="center">
<img src="https://placeholder.com/800x600" alt="SIRAJ Interface" width="600">

*Clean, intuitive interface for educational queries*
</div>

## 🤝 Contributing

Contributions welcome! SIRAJ follows:
- Living Spiral methodology
- Multi-voice council for decisions
- QWAN (Quality Without A Name) principles
- Security-first development

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Google for the amazing Gemma 3n model
- Kaggle for hosting this hackathon
- The open-source community

---

<div align="center">

**Built with 🎓 for the Kaggle Gemma 3n Hackathon**

*"Education is not filling a bucket, but lighting a fire" - Through multiple sparks*

</div>
