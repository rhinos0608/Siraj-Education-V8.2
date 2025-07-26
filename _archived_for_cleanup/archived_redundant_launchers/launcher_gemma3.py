#!/usr/bin/env python3
"""
SIRAJ Educational AI - Gemma 3 Competition Launcher v12.0
========================================================

For Kaggle Gemma 3n Hackathon
Uses correct Gemma 3 model names
"""

import os
import sys
import time
import asyncio
import json
import subprocess
import webbrowser
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import socket

# Phase 1: COLLAPSE - Acknowledge what we need
REQUIRED_PACKAGES = [
    'httpx', 'psutil', 'fastapi', 'uvicorn', 
    'aiofiles', 'colorama'
]

# Simple dependency check
def ensure_dependencies():
    """Ensure dependencies following anti-entropy principles"""
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"📦 Installing {len(missing)} packages: {', '.join(missing)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing + ['--quiet'])
        print("✅ Dependencies ready")

ensure_dependencies()

# Now import what we need
import httpx
import psutil
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

# Configure logging with simplicity
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('SIRAJ')

# Constants following council-driven architecture
EDUCATIONAL_ARCHETYPES = {
    # Perspective Voices (Instance A)
    'socratic': {'instance': 'A', 'port': 11434, 'focus': 'questions'},
    'constructivist': {'instance': 'A', 'port': 11434, 'focus': 'building'},
    'storyteller': {'instance': 'A', 'port': 11434, 'focus': 'narrative'},
    
    # Synthesis Voices (Instance B)
    'synthesizer': {'instance': 'B', 'port': 11435, 'focus': 'integration'},
    'challenger': {'instance': 'B', 'port': 11435, 'focus': 'alternatives'},
    'mentor': {'instance': 'B', 'port': 11435, 'focus': 'guidance'},
    'analyst': {'instance': 'B', 'port': 11435, 'focus': 'patterns'}
}

# Phase 2: COUNCIL - Multi-voice architecture
class EducationalCouncil:
    """Living council following AI_INSTRUCTIONS principles"""
    
    def __init__(self):
        self.model = self._select_model()
        self.instances = {}
        self.app = self._create_app()
        
    def _select_model(self) -> str:
        """Select Gemma 3 model based on system resources"""
        try:
            ram_gb = psutil.virtual_memory().total / (1024**3)
            # Use correct Gemma 3 model names
            if ram_gb >= 32:
                model = "gemma3:9b"  # 9B parameter model for high-end systems
            elif ram_gb >= 16:
                model = "gemma3:2b"  # 2B parameter model for mid-range
            else:
                model = "gemma3:1b"  # 1B parameter model for lower RAM
            logger.info(f"🧠 Selected {model} for {ram_gb:.1f}GB RAM")
            return model
        except:
            return "gemma3:2b"  # Default to 2B model
            
    def _create_app(self) -> FastAPI:
        """Create FastAPI app with council endpoints"""
        app = FastAPI(title="SIRAJ Educational Council")
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        @app.get("/")
        async def serve_frontend():
            return HTMLResponse(content=self._get_frontend_html())
            
        @app.post("/api/education/query")
        async def educational_query(request: dict):
            """Process query through educational council"""
            try:
                # Input validation (security-first)
                topic = request.get('topic', '').strip()
                if not topic:
                    raise HTTPException(400, "Topic required")
                    
                grade_level = request.get('grade_level', 'middle')
                archetypes = request.get('selected_archetypes', 
                    ['socratic', 'constructivist', 'synthesizer', 'mentor'])
                
                # For single instance mode (if multi-instance fails)
                if hasattr(self, 'single_instance_mode') and self.single_instance_mode:
                    responses = await self._gather_single_instance_responses(topic, grade_level, archetypes)
                else:
                    # Try multi-instance first
                    responses = await self._gather_council_responses(topic, grade_level, archetypes)
                
                # Synthesis
                synthesis = self._synthesize_responses(responses, topic)
                
                return JSONResponse({
                    'topic': topic,
                    'grade_level': grade_level,
                    'council_responses': responses,
                    'synthesis': synthesis,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Council error: {e}")
                raise HTTPException(500, str(e))
                
        @app.get("/api/health")
        async def health():
            return {"status": "healthy", "council": "assembled", "model": self.model}
            
        return app
        
    async def _gather_single_instance_responses(self, topic: str, grade_level: str, archetypes: List[str]) -> Dict:
        """Gather responses using single Ollama instance"""
        responses = {}
        
        for archetype in archetypes:
            prompt = self._create_archetype_prompt(archetype, topic, grade_level)
            
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f'http://localhost:11434/api/generate',
                        json={
                            'model': self.model,
                            'prompt': prompt,
                            'stream': False
                        },
                        timeout=60.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        responses[archetype] = {
                            'response': result.get('response', ''),
                            'success': True,
                            'focus': EDUCATIONAL_ARCHETYPES.get(archetype, {}).get('focus', 'teaching')
                        }
                    else:
                        responses[archetype] = {
                            'response': f'[{archetype} is contemplating...]',
                            'success': False
                        }
                        
            except Exception as e:
                logger.error(f"Error with {archetype}: {e}")
                responses[archetype] = {
                    'response': f'[{archetype} is reflecting...]',
                    'success': False
                }
                
        return responses
        
    async def _gather_council_responses(self, topic: str, grade_level: str, archetypes: List[str]) -> Dict:
        """Gather responses from educational archetypes"""
        responses = {}
        
        for archetype in archetypes:
            if archetype not in EDUCATIONAL_ARCHETYPES:
                continue
                
            config = EDUCATIONAL_ARCHETYPES[archetype]
            prompt = self._create_archetype_prompt(archetype, topic, grade_level)
            
            try:
                # Make request to appropriate Ollama instance
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f'http://localhost:{config["port"]}/api/generate',
                        json={
                            'model': self.model,
                            'prompt': prompt,
                            'stream': False
                        },
                        timeout=60.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        responses[archetype] = {
                            'response': result.get('response', ''),
                            'success': True,
                            'focus': config['focus']
                        }
                    else:
                        responses[archetype] = {
                            'response': f'[{archetype} is contemplating...]',
                            'success': False
                        }
                        
            except Exception as e:
                logger.error(f"Error with {archetype}: {e}")
                responses[archetype] = {
                    'response': f'[{archetype} is reflecting...]',
                    'success': False
                }
                
        return responses
        
    def _create_archetype_prompt(self, archetype: str, topic: str, grade_level: str) -> str:
        """Create prompt following voice archetype patterns"""
        prompts = {
            'socratic': f"As a Socratic teacher, ask 2-3 thought-provoking questions about '{topic}' for {grade_level} students that help them discover the concepts themselves.",
            
            'constructivist': f"As a Constructivist teacher, suggest hands-on activities or experiments for {grade_level} students to learn '{topic}' through direct experience.",
            
            'storyteller': f"As a Storyteller teacher, create a brief, engaging story or metaphor that teaches '{topic}' to {grade_level} students.",
            
            'synthesizer': f"As a Synthesizer teacher, explain how '{topic}' connects to other subjects and real life for {grade_level} students.",
            
            'challenger': f"As a Challenger teacher, present alternative perspectives on '{topic}' that push {grade_level} students beyond surface understanding.",
            
            'mentor': f"As a Mentor teacher, provide supportive guidance about '{topic}' for {grade_level} students with encouragement.",
            
            'analyst': f"As an Analyst teacher, break down '{topic}' systematically for {grade_level} students with clear logical analysis."
        }
        
        return prompts.get(archetype, f"Teach about {topic}")
        
    def _synthesize_responses(self, responses: Dict, topic: str) -> str:
        """Synthesize council responses following Living Spiral"""
        successful = [r for r in responses.values() if r.get('success')]
        
        if not successful:
            return "The educational council is assembling wisdom..."
            
        return f"The Educational Council explored '{topic}' from {len(successful)} perspectives, offering a rich tapestry of understanding through questions, activities, stories, and analysis."
        
    def _get_frontend_html(self) -> str:
        """Simple, beautiful frontend following QWAN principles"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRAJ Educational AI Council - Gemma 3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        
        .container {
            max-width: 800px;
            width: 90%;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
        }
        
        h1 {
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .subtitle {
            text-align: center;
            opacity: 0.9;
            margin-bottom: 30px;
        }
        
        .powered-by {
            text-align: center;
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 20px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        textarea, select {
            width: 100%;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
        }
        
        button {
            width: 100%;
            padding: 15px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        button:hover {
            background: #45a049;
            transform: translateY(-2px);
        }
        
        button:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        
        .response {
            margin-top: 30px;
            padding: 20px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            display: none;
        }
        
        .archetype {
            margin: 15px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 8px;
        }
        
        .archetype h4 {
            margin-bottom: 10px;
            color: #4CAF50;
        }
        
        .loading {
            text-align: center;
            font-style: italic;
        }
        
        .error {
            color: #ff6b6b;
            background: rgba(255, 0, 0, 0.1);
            padding: 10px;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 SIRAJ Educational AI</h1>
        <p class="subtitle">Multi-Archetype Educational Council</p>
        <p class="powered-by">Powered by Google Gemma 3</p>
        
        <div class="form-group">
            <label>What would you like to learn?</label>
            <textarea id="question" rows="3" placeholder="Enter your question..."></textarea>
        </div>
        
        <div class="form-group">
            <label>Grade Level:</label>
            <select id="gradeLevel">
                <option value="elementary">Elementary</option>
                <option value="middle" selected>Middle School</option>
                <option value="high">High School</option>
                <option value="university">University</option>
            </select>
        </div>
        
        <button id="askBtn" onclick="askCouncil()">Ask the Council</button>
        
        <div id="response" class="response">
            <div id="loading" class="loading">The council is deliberating...</div>
            <div id="results"></div>
        </div>
    </div>

    <script>
        async function askCouncil() {
            const question = document.getElementById('question').value.trim();
            const gradeLevel = document.getElementById('gradeLevel').value;
            
            if (!question) {
                alert('Please enter a question!');
                return;
            }
            
            const btn = document.getElementById('askBtn');
            const responseDiv = document.getElementById('response');
            const loadingDiv = document.getElementById('loading');
            const resultsDiv = document.getElementById('results');
            
            btn.disabled = true;
            btn.textContent = 'Council is thinking...';
            responseDiv.style.display = 'block';
            loadingDiv.style.display = 'block';
            resultsDiv.innerHTML = '';
            
            try {
                const response = await fetch('/api/education/query', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        topic: question,
                        grade_level: gradeLevel,
                        selected_archetypes: ['socratic', 'constructivist', 'synthesizer', 'mentor']
                    })
                });
                
                const data = await response.json();
                loadingDiv.style.display = 'none';
                
                let html = '<h3>Council Responses:</h3>';
                
                for (const [archetype, response] of Object.entries(data.council_responses || {})) {
                    if (response.success) {
                        html += `
                            <div class="archetype">
                                <h4>${archetype.charAt(0).toUpperCase() + archetype.slice(1)}</h4>
                                <p>${response.response}</p>
                            </div>
                        `;
                    }
                }
                
                if (data.synthesis) {
                    html += `
                        <div class="archetype">
                            <h4>Council Synthesis</h4>
                            <p>${data.synthesis}</p>
                        </div>
                    `;
                }
                
                resultsDiv.innerHTML = html;
                
            } catch (error) {
                loadingDiv.style.display = 'none';
                resultsDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            }
            
            btn.disabled = false;
            btn.textContent = 'Ask the Council';
        }
        
        // Enter key to submit
        document.getElementById('question').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                askCouncil();
            }
        });
    </script>
</body>
</html>"""

# Phase 3: SYNTHESIS - Ollama management
class OllamaManager:
    """Simple Ollama management following anti-entropy principles"""
    
    @staticmethod
    def is_installed() -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True)
            return result.returncode == 0
        except:
            return False
            
    @staticmethod
    async def check_model_exists(model: str) -> bool:
        """Check if model is already downloaded"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get('http://localhost:11434/api/tags', timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    models = data.get('models', [])
                    return any(m['name'].startswith(model.split(':')[0]) for m in models)
        except:
            return False
            
    @staticmethod
    async def ensure_running():
        """Ensure Ollama service is running"""
        # Check if already running
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get('http://localhost:11434/api/tags', timeout=2)
                if response.status_code == 200:
                    logger.info("✅ Ollama already running")
                    return True
        except:
            pass
            
        # Try to start Ollama
        logger.info("🚀 Starting Ollama service...")
        try:
            if sys.platform == 'win32':
                subprocess.Popen(['ollama', 'serve'], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
            
            # Wait for startup
            await asyncio.sleep(5)
            return True
        except Exception as e:
            logger.error(f"Failed to start Ollama: {e}")
            return False
        
    @staticmethod
    async def ensure_model(model: str):
        """Ensure model is available"""
        logger.info(f"🔍 Checking {model}...")
        
        # Check if already exists
        if await OllamaManager.check_model_exists(model):
            logger.info(f"✅ {model} already available")
            return True
            
        # Pull model
        logger.info(f"📥 Downloading {model} (this may take 10-15 minutes)...")
        logger.info("   Model sizes: 1B=637MB, 2B=1.6GB, 9B=5.5GB")
        
        try:
            # Use subprocess for better progress display
            process = subprocess.Popen(
                ['ollama', 'pull', model],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            for line in process.stdout:
                if line.strip():
                    print(f"   {line.strip()}")
                    
            process.wait()
            
            if process.returncode == 0:
                logger.info(f"✅ {model} downloaded successfully")
                return True
            else:
                logger.error(f"Failed to download {model}")
                return False
                
        except Exception as e:
            logger.error(f"Error downloading model: {e}")
            return False

# Phase 4: REBIRTH - Main launcher
class SIRAJLauncher:
    """Clean launcher following Living Spiral methodology"""
    
    def __init__(self):
        self.council = EducationalCouncil()
        self.running = True
        
    def show_banner(self):
        """Show startup banner"""
        print("\n" + "="*60)
        print("""
   _____ _____ _____            _    
  / ____|_   _|  __ \     /\   | |   
 | (___   | | | |__) |   /  \  | |   
  \___ \  | | |  _  /   / /\ \ | |   
  ____) |_| |_| | \ \  / ____ \| |   
 |_____/|_____|_|  \_\/_/    \_\_|   
                                     
  Educational AI Council v12.0
  🌀 Living Spiral Architecture
  📚 Kaggle Gemma 3 Hackathon
        """)
        print("="*60 + "\n")
        
    async def setup_ollama(self):
        """Setup Ollama following collapse-council pattern"""
        # Check installation
        if not OllamaManager.is_installed():
            logger.error("❌ Ollama not installed")
            logger.info("Please install from: https://ollama.com")
            logger.info("After installing, run this script again")
            return False
            
        # Ensure running
        if not await OllamaManager.ensure_running():
            logger.error("❌ Failed to start Ollama service")
            return False
            
        # Ensure model
        model = self.council.model
        if not await OllamaManager.ensure_model(model):
            logger.warning(f"⚠️ Failed to download {model}")
            
            # Try fallback to any available Gemma model
            logger.info("🔍 Checking for any available Gemma models...")
            if await OllamaManager.check_model_exists('gemma'):
                self.council.model = 'gemma3'  # Use whatever gemma3 is available
                logger.info(f"✅ Using available Gemma model")
            else:
                logger.error("❌ No Gemma models available")
                logger.info("Please run: ollama pull gemma3:2b")
                return False
        
        # For simplicity, use single instance mode
        logger.info("📍 Using single instance mode for stability")
        self.council.single_instance_mode = True
        
        return True
        
    async def start_server(self):
        """Start unified server"""
        logger.info("🌐 Starting educational server on port 3000...")
        
        config = uvicorn.Config(
            self.council.app,
            host="0.0.0.0",
            port=3000,
            log_level="error"
        )
        
        server = uvicorn.Server(config)
        await server.serve()
        
    def open_browser(self):
        """Open browser when ready"""
        def opener():
            time.sleep(3)
            url = "http://localhost:3000"
            logger.info(f"🌐 Opening browser to {url}")
            
            try:
                webbrowser.open(url)
            except:
                logger.info(f"Please open manually: {url}")
                
        import threading
        threading.Thread(target=opener, daemon=True).start()
        
    async def run(self):
        """Main run loop following Living Spiral"""
        try:
            self.show_banner()
            
            # Collapse: Acknowledge what we need
            logger.info("🌀 Phase 1: COLLAPSE - Checking requirements...")
            
            # Council: Setup components
            logger.info("🎭 Phase 2: COUNCIL - Assembling components...")
            if not await self.setup_ollama():
                return
                
            # Synthesis: Start server
            logger.info("✨ Phase 3: SYNTHESIS - Starting server...")
            self.open_browser()
            
            # Rebirth: Serve
            logger.info("🚀 Phase 4: REBIRTH - System ready!")
            print("\n" + "="*60)
            print("✅ SIRAJ Educational AI Ready!")
            print(f"🌐 Open: http://localhost:3000")
            print(f"🤖 Using model: {self.council.model}")
            print("\nPress Ctrl+C to stop")
            print("="*60 + "\n")
            
            await self.start_server()
            
        except KeyboardInterrupt:
            logger.info("\n👋 Shutting down...")
        except Exception as e:
            logger.error(f"Error: {e}")
            import traceback
            traceback.print_exc()

# Entry point
def main():
    """Main entry following council principles"""
    launcher = SIRAJLauncher()
    asyncio.run(launcher.run())

if __name__ == '__main__':
    main()
