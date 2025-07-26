#!/usr/bin/env python3
"""
SIRAJ Educational AI - FIXED Browser Timing v13.0
================================================

CRITICAL FIXES:
✅ Correct Gemma 3 model names (gemma3:2b, not gemma3n:e2b)
✅ Single instance mode (no port conflicts)
✅ Browser opens ONLY after services are verified ready
✅ Robust health checks
✅ Zero redundancy, maximum reliability

For Kaggle Gemma 3 Hackathon
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
from typing import Dict, List, Optional
from datetime import datetime
import socket

# Essential dependencies only
REQUIRED_PACKAGES = ['httpx', 'psutil', 'fastapi', 'uvicorn', 'colorama']

def ensure_dependencies():
    """Install only what we need"""
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

# Import after ensuring packages exist
import httpx
import psutil
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from colorama import init, Fore, Style

init(autoreset=True)  # Initialize colorama

# Configure clean logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger('SIRAJ')

class EducationalAI:
    """Simplified, reliable educational AI"""
    
    def __init__(self):
        self.model = self._detect_best_model()
        self.app = self._create_app()
        self.server_ready = False
        
    def _detect_best_model(self) -> str:
        """Detect best Gemma 3 model for system"""
        try:
            ram_gb = psutil.virtual_memory().total / (1024**3)
            if ram_gb >= 32:
                return "gemma3:9b"    # High-end: 5.5GB model
            elif ram_gb >= 16:
                return "gemma3:2b"    # Mid-range: 1.6GB model  
            else:
                return "gemma3:1b"    # Low-end: 637MB model
        except:
            return "gemma3:2b"        # Safe default
            
    def _create_app(self) -> FastAPI:
        """Create clean FastAPI app"""
        app = FastAPI(title="SIRAJ Educational AI", version="13.0")
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        @app.get("/")
        async def home():
            return HTMLResponse(content=self._get_ui())
            
        @app.get("/api/health")
        async def health():
            """Health check endpoint"""
            ollama_status = await self._check_ollama_health()
            return {
                "status": "ready" if ollama_status else "initializing",
                "model": self.model,
                "ollama": ollama_status,
                "server": self.server_ready
            }
            
        @app.post("/api/chat")
        async def chat(request: dict):
            """Educational chat endpoint"""
            try:
                question = request.get('question', '').strip()
                if not question:
                    raise HTTPException(400, "Question required")
                    
                archetype = request.get('archetype', 'mentor')
                grade = request.get('grade', 'middle')
                
                # Create educational prompt
                prompt = self._create_educational_prompt(archetype, question, grade)
                
                # Call Ollama
                async with httpx.AsyncClient(timeout=90.0) as client:
                    response = await client.post(
                        'http://localhost:11434/api/generate',
                        json={
                            'model': self.model,
                            'prompt': prompt,
                            'stream': False
                        }
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        return {
                            'response': data.get('response', 'No response generated'),
                            'archetype': archetype,
                            'grade': grade,
                            'success': True
                        }
                    else:
                        raise HTTPException(500, f"Ollama error: {response.status_code}")
                        
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return {
                    'error': str(e),
                    'success': False
                }
                
        return app
        
    def _create_educational_prompt(self, archetype: str, question: str, grade: str) -> str:
        """Create archetype-specific educational prompts"""
        base_prompt = f"You are an expert {archetype} teacher. "
        
        prompts = {
            'socratic': f"{base_prompt}Ask 2-3 thought-provoking questions to help {grade} students discover '{question}' themselves.",
            'constructivist': f"{base_prompt}Suggest hands-on activities for {grade} students to learn '{question}' through experience.",
            'storyteller': f"{base_prompt}Create an engaging story that teaches '{question}' to {grade} students.",
            'synthesizer': f"{base_prompt}Explain how '{question}' connects to other subjects for {grade} students.",
            'challenger': f"{base_prompt}Present alternative perspectives on '{question}' for {grade} students.",
            'mentor': f"{base_prompt}Provide supportive guidance about '{question}' for {grade} students.",
            'analyst': f"{base_prompt}Break down '{question}' systematically for {grade} students."
        }
        
        return prompts.get(archetype, f"Explain '{question}' clearly for {grade} school students.")
        
    async def _check_ollama_health(self) -> bool:
        """Check if Ollama is healthy and has our model"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                # Check Ollama is running
                response = await client.get('http://localhost:11434/api/tags')
                if response.status_code != 200:
                    return False
                    
                # Check our model exists
                data = response.json()
                models = [m['name'] for m in data.get('models', [])]
                
                # Look for our model or compatible variants
                model_base = self.model.split(':')[0]  # e.g., 'gemma3' from 'gemma3:2b'
                
                return any(model_base in model for model in models)
                
        except:
            return False
            
    def _get_ui(self) -> str:
        """Beautiful, functional UI"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRAJ Educational AI - Gemma 3</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            padding: 20px;
        }
        
        .container {
            max-width: 700px;
            width: 100%;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(15px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        
        h1 {
            text-align: center;
            font-size: 2.8em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle {
            text-align: center;
            opacity: 0.9;
            margin-bottom: 15px;
            font-size: 1.1em;
        }
        
        .powered-by {
            text-align: center;
            font-size: 0.9em;
            opacity: 0.8;
            margin-bottom: 30px;
            color: #4CAF50;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 14px;
        }
        
        textarea, select {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.95);
            color: #333;
            transition: all 0.3s;
        }
        
        textarea:focus, select:focus {
            outline: none;
            background: rgba(255, 255, 255, 1);
            box-shadow: 0 0 20px rgba(255,255,255,0.3);
        }
        
        textarea {
            min-height: 100px;
            resize: vertical;
            font-family: inherit;
        }
        
        button {
            width: 100%;
            padding: 18px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        button:disabled {
            background: #666;
            cursor: not-allowed;
            transform: none;
        }
        
        .response {
            margin-top: 30px;
            padding: 25px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 15px;
            display: none;
        }
        
        .response-content {
            line-height: 1.6;
            font-size: 16px;
        }
        
        .archetype-badge {
            display: inline-block;
            background: #4CAF50;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .loading {
            text-align: center;
            font-style: italic;
            opacity: 0.8;
        }
        
        .error {
            color: #ff6b6b;
            background: rgba(255, 107, 107, 0.1);
            padding: 15px;
            border-radius: 8px;
            border: 1px solid rgba(255, 107, 107, 0.3);
        }
        
        .status {
            text-align: center;
            font-size: 12px;
            opacity: 0.7;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 SIRAJ Educational AI</h1>
        <p class="subtitle">Multi-Archetype Learning Assistant</p>
        <p class="powered-by">⚡ Powered by Google Gemma 3</p>
        
        <div class="form-group">
            <label>What would you like to learn about?</label>
            <textarea id="question" placeholder="Enter your question or topic..."></textarea>
        </div>
        
        <div class="form-group">
            <label>Teaching Style:</label>
            <select id="archetype">
                <option value="mentor">🌱 Mentor - Supportive guidance</option>
                <option value="socratic">🦉 Socratic - Thought-provoking questions</option>
                <option value="constructivist">🔨 Constructivist - Hands-on activities</option>
                <option value="storyteller">📖 Storyteller - Engaging narratives</option>
                <option value="synthesizer">🌐 Synthesizer - Cross-subject connections</option>
                <option value="challenger">🎯 Challenger - Alternative perspectives</option>
                <option value="analyst">🔬 Analyst - Systematic breakdown</option>
            </select>
        </div>
        
        <div class="form-group">
            <label>Grade Level:</label>
            <select id="grade">
                <option value="elementary">Elementary School</option>
                <option value="middle" selected>Middle School</option>
                <option value="high">High School</option>
                <option value="university">University</option>
            </select>
        </div>
        
        <button id="askBtn" onclick="askTeacher()">Ask Your AI Teacher</button>
        
        <div id="response" class="response">
            <div id="content" class="response-content"></div>
        </div>
        
        <div class="status" id="status">Ready</div>
    </div>

    <script>
        async function askTeacher() {
            const question = document.getElementById('question').value.trim();
            if (!question) {
                alert('Please enter a question!');
                return;
            }
            
            const btn = document.getElementById('askBtn');
            const responseDiv = document.getElementById('response');
            const contentDiv = document.getElementById('content');
            
            btn.disabled = true;
            btn.textContent = 'AI Teacher is thinking...';
            responseDiv.style.display = 'block';
            contentDiv.innerHTML = '<div class="loading">🤔 Your AI teacher is preparing a thoughtful response...</div>';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        question: question,
                        archetype: document.getElementById('archetype').value,
                        grade: document.getElementById('grade').value
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    const archetype = data.archetype.charAt(0).toUpperCase() + data.archetype.slice(1);
                    contentDiv.innerHTML = `
                        <div class="archetype-badge">${archetype} Teacher</div>
                        <div>${data.response}</div>
                    `;
                } else {
                    contentDiv.innerHTML = `<div class="error">Sorry, I'm having trouble thinking right now. ${data.error || 'Please try again.'}</div>`;
                }
            } catch (error) {
                contentDiv.innerHTML = `<div class="error">Connection error: ${error.message}</div>`;
            }
            
            btn.disabled = false;
            btn.textContent = 'Ask Your AI Teacher';
        }
        
        // Enter key to submit
        document.getElementById('question').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                askTeacher();
            }
        });
        
        // Status updates
        async function updateStatus() {
            try {
                const response = await fetch('/api/health');
                const health = await response.json();
                const statusDiv = document.getElementById('status');
                
                if (health.status === 'ready') {
                    statusDiv.textContent = `✅ Ready - Model: ${health.model}`;
                    statusDiv.style.color = '#4CAF50';
                } else {
                    statusDiv.textContent = '⏳ Initializing...';
                    statusDiv.style.color = '#ff9800';
                }
            } catch (e) {
                document.getElementById('status').textContent = '❌ Connection issue';
            }
        }
        
        // Update status every 5 seconds
        updateStatus();
        setInterval(updateStatus, 5000);
    </script>
</body>
</html>"""

class OllamaManager:
    """Simplified Ollama management"""
    
    @staticmethod
    def is_installed() -> bool:
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True, timeout=10)
            return result.returncode == 0
        except:
            return False
            
    @staticmethod
    async def is_running() -> bool:
        """Check if Ollama is running"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get('http://localhost:11434/api/version')
                return response.status_code == 200
        except:
            return False
            
    @staticmethod
    async def start_service():
        """Start Ollama service if not running"""
        if await OllamaManager.is_running():
            print(f"{Fore.GREEN}✅ Ollama already running")
            return True
            
        print(f"{Fore.YELLOW}🚀 Starting Ollama service...")
        try:
            if sys.platform == 'win32':
                subprocess.Popen(
                    ['ollama', 'serve'],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            else:
                subprocess.Popen(
                    ['ollama', 'serve'],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            
            # Wait for startup with timeout
            for i in range(30):  # 30 second timeout
                await asyncio.sleep(1)
                if await OllamaManager.is_running():
                    print(f"{Fore.GREEN}✅ Ollama service started")
                    return True
                    
            print(f"{Fore.RED}❌ Ollama failed to start within 30 seconds")
            return False
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to start Ollama: {e}")
            return False
            
    @staticmethod
    async def ensure_model(model: str) -> bool:
        """Ensure model is downloaded"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Check if model exists
                response = await client.get('http://localhost:11434/api/tags')
                if response.status_code == 200:
                    data = response.json()
                    models = [m['name'] for m in data.get('models', [])]
                    
                    # Check exact match or partial match
                    if model in models or any(model.split(':')[0] in m for m in models):
                        print(f"{Fore.GREEN}✅ Model {model} available")
                        return True
                        
            # Need to download
            print(f"{Fore.YELLOW}📥 Downloading {model}...")
            print(f"{Fore.CYAN}   This may take 5-15 minutes depending on your internet speed")
            
            # Use subprocess for real-time output
            process = subprocess.Popen(
                ['ollama', 'pull', model],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            # Show progress
            for line in process.stdout:
                if line.strip():
                    print(f"{Fore.CYAN}   {line.strip()}")
                    
            process.wait()
            
            if process.returncode == 0:
                print(f"{Fore.GREEN}✅ Model {model} downloaded successfully")
                return True
            else:
                print(f"{Fore.RED}❌ Failed to download {model}")
                return False
                
        except Exception as e:
            print(f"{Fore.RED}❌ Error with model: {e}")
            return False

class SIRAJLauncher:
    """Main launcher with fixed browser timing"""
    
    def __init__(self):
        self.ai = EducationalAI()
        
    def show_banner(self):
        print(f"\n{Fore.CYAN}" + "="*70)
        print(f"""{Fore.CYAN}
   _____ _____ _____            _    
  / ____|_   _|  __ \\     /\\   | |   
 | (___   | | | |__) |   /  \\  | |   
  \\___ \\  | | |  _  /   / /\\ \\ | |   
  ____) |_| |_| | \\ \\  / ____ \\| |   
 |_____/|_____|_|  \\_\\/_/    \\_\\_|   
                                     
  🎭 Educational AI v13.0 - FIXED BROWSER TIMING
  📚 Kaggle Gemma 3 Hackathon Edition
  🌀 Living Spiral Architecture
        """)
        print("="*70 + f"{Style.RESET_ALL}\n")
        
    async def verify_system_ready(self) -> bool:
        """Comprehensive system readiness check"""
        print(f"{Fore.YELLOW}🔍 Verifying system readiness...")
        
        # Check Ollama health
        ollama_healthy = await self.ai._check_ollama_health()
        if not ollama_healthy:
            print(f"{Fore.RED}❌ Ollama not ready")
            return False
            
        # Check server can start
        try:
            # Test port availability
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 3000))
            sock.close()
            
            if result == 0:
                print(f"{Fore.RED}❌ Port 3000 already in use")
                return False
                
        except:
            pass
            
        print(f"{Fore.GREEN}✅ System ready for launch")
        return True
        
    async def start_server_with_readiness(self):
        """Start server and mark as ready only when truly ready"""
        config = uvicorn.Config(
            self.ai.app,
            host="0.0.0.0",
            port=3000,
            log_level="error",
            access_log=False
        )
        
        server = uvicorn.Server(config)
        
        # Start server in background
        server_task = asyncio.create_task(server.serve())
        
        # Wait for server to be ready
        print(f"{Fore.YELLOW}🌐 Starting web server...")
        for i in range(30):  # 30 second timeout
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get('http://localhost:3000/api/health', timeout=2)
                    if response.status_code == 200:
                        self.ai.server_ready = True
                        print(f"{Fore.GREEN}✅ Web server ready on port 3000")
                        break
            except:
                pass
                
            await asyncio.sleep(1)
        else:
            print(f"{Fore.RED}❌ Server failed to become ready")
            return
            
        # NOW it's safe to open browser
        print(f"{Fore.GREEN}🌐 Opening browser...")
        try:
            webbrowser.open('http://localhost:3000')
            print(f"{Fore.GREEN}✅ Browser opened to http://localhost:3000")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Could not auto-open browser: {e}")
            print(f"{Fore.CYAN}📖 Please manually open: http://localhost:3000")
            
        # Wait for server
        await server_task
        
    async def run(self):
        """Main execution with proper sequencing"""
        try:
            self.show_banner()
            
            # 1. Check Ollama installation
            if not OllamaManager.is_installed():
                print(f"{Fore.RED}❌ Ollama not installed!")
                print(f"{Fore.CYAN}📖 Please install from: https://ollama.com")
                print(f"{Fore.CYAN}📖 Then run this script again")
                return
                
            # 2. Start Ollama service
            if not await OllamaManager.start_service():
                print(f"{Fore.RED}❌ Could not start Ollama service")
                return
                
            # 3. Ensure model exists
            if not await OllamaManager.ensure_model(self.ai.model):
                print(f"{Fore.RED}❌ Could not download model {self.ai.model}")
                print(f"{Fore.CYAN}📖 You can manually try: ollama pull {self.ai.model}")
                return
                
            # 4. Verify everything is ready
            if not await self.verify_system_ready():
                print(f"{Fore.RED}❌ System not ready")
                return
                
            # 5. Start server (browser opens only when ready)
            print(f"\n{Fore.GREEN}" + "="*70)
            print(f"{Fore.GREEN}🚀 SIRAJ Educational AI is starting...")
            print(f"{Fore.GREEN}🤖 Using model: {self.ai.model}")
            print(f"{Fore.GREEN}🎭 7 Educational archetypes ready")
            print(f"{Fore.YELLOW}⏳ Starting web server (browser will open when ready)...")
            print("="*70 + f"{Style.RESET_ALL}\n")
            
            await self.start_server_with_readiness()
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Shutting down gracefully...")
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Entry point"""
    launcher = SIRAJLauncher()
    asyncio.run(launcher.run())

if __name__ == '__main__':
    main()
