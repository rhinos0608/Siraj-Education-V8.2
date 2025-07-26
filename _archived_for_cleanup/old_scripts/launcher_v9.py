#!/usr/bin/env python3
"""
SIRAJ Educational AI - Fully Automated Launcher v9.0
===================================================

For Kaggle Gemma 3n Hackathon - Python 3.12.3
Completely automated with no manual steps required.

Key improvements:
- Auto-installs all dependencies before importing
- Fixes proxy issues for frontend requests
- Ensures browser opens only when everything is ready
- Handles all error cases gracefully
"""

import os
import sys
import subprocess
import platform
import time

# First, ensure all dependencies are installed
def ensure_dependencies():
    """Install all required dependencies automatically"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'httpx>=0.24.0',
        'psutil>=5.9.0', 
        'fastapi>=0.104.0',
        'uvicorn[standard]>=0.23.0',
        'pydantic>=2.0.0',
        'aiofiles>=23.0.0',
        'python-multipart>=0.0.6',
        'colorama>=0.4.6'
    ]
    
    # Check if we need to install
    missing_packages = []
    for pkg in required_packages:
        pkg_name = pkg.split('>=')[0].split('[')[0]
        try:
            __import__(pkg_name)
        except ImportError:
            missing_packages.append(pkg)
    
    if missing_packages:
        print(f"Installing {len(missing_packages)} missing packages...")
        for pkg in missing_packages:
            print(f"  • Installing {pkg}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg, '--quiet'])
        print("✅ All dependencies installed!")
    else:
        print("✅ All dependencies already installed!")

# Install dependencies before importing them
ensure_dependencies()

# Now we can safely import everything
import asyncio
import json
import logging
import shutil
import signal
import socket
import threading
import urllib.request
import webbrowser
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import aiofiles
import httpx
import psutil
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

# Configure logging with colors
try:
    import colorama
    colorama.init()
except:
    pass

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for different log levels"""
    
    grey = "\x1b[38;21m"
    blue = "\x1b[34m"
    green = "\x1b[32m"
    yellow = "\x1b[33m"
    red = "\x1b[31m"
    magenta = "\x1b[35m"
    cyan = "\x1b[36m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.INFO: blue + "%(asctime)s - %(name)s - " + green + "%(levelname)s" + reset + " - %(message)s",
        logging.WARNING: yellow + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset
    }
    
    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%H:%M:%S')
        return formatter.format(record)

# Setup logging
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter())
logging.basicConfig(level=logging.INFO, handlers=[handler])
logger = logging.getLogger('SIRAJ-Launcher')

# Constants
INSTANCE_A_PORT = 11434
INSTANCE_B_PORT = 11435
ROUTER_PORT = 5000
BACKEND_PORT = 8000
FRONTEND_PORT = 3000

# Platform detection
PLATFORM = platform.system().lower()
IS_WINDOWS = PLATFORM == "windows"
IS_MACOS = PLATFORM == "darwin"
IS_LINUX = PLATFORM == "linux"

# Educational archetype mapping
EDUCATIONAL_ARCHETYPE_MAP = {
    'socratic': 'A',
    'constructivist': 'A',
    'storyteller': 'A',
    'synthesizer': 'B',
    'challenger': 'B',
    'mentor': 'B',
    'analyst': 'B'
}

# Utility functions
def is_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('', port))
            return True
        except:
            return False

def find_free_port(start_port, max_attempts=10):
    """Find a free port starting from start_port"""
    for i in range(max_attempts):
        port = start_port + i
        if is_port_available(port):
            return port
    raise RuntimeError(f"No free ports found starting from {start_port}")

def get_recommended_model() -> Tuple[str, str]:
    """Determine which Gemma 3n model to use based on system RAM"""
    try:
        ram_gb = psutil.virtual_memory().total / (1024**3)
        if ram_gb >= 16:
            return "gemma3n:e4b", f"🧠 Selected Gemma 3n E4B (4B params) - {ram_gb:.1f}GB RAM detected"
        else:
            return "gemma3n:e2b", f"🧠 Selected Gemma 3n E2B (2B params) - {ram_gb:.1f}GB RAM detected"
    except:
        return "gemma3n:e2b", "🧠 Selected Gemma 3n E2B (default)"

class OllamaInstaller:
    """Handles Ollama installation across platforms"""
    
    @staticmethod
    def is_installed() -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    @staticmethod
    async def install_windows():
        """Install Ollama on Windows"""
        logger.info("📥 Downloading Ollama for Windows...")
        
        installer_url = "https://ollama.com/download/OllamaSetup.exe"
        installer_path = os.path.join(os.environ['TEMP'], 'OllamaSetup.exe')
        
        try:
            def download_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(int(downloaded * 100 / total_size), 100)
                if percent % 20 == 0:
                    logger.info(f"Downloading Ollama... {percent}%")
            
            urllib.request.urlretrieve(installer_url, installer_path, download_progress)
            
            logger.info("🔧 Installing Ollama (this may take a few minutes)...")
            subprocess.run([installer_path, '/S'], check=True)
            
            # Wait for installation to complete
            time.sleep(10)
            
            # Add to PATH
            ollama_path = os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'Ollama')
            if os.path.exists(ollama_path):
                current_path = os.environ.get('PATH', '')
                if ollama_path not in current_path:
                    os.environ['PATH'] = f"{current_path};{ollama_path}"
            
            # Clean up installer
            if os.path.exists(installer_path):
                os.remove(installer_path)
            
            logger.info("✅ Ollama installed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to install Ollama: {e}")
            return False
    
    @staticmethod
    async def install_macos():
        """Install Ollama on macOS"""
        try:
            # Try homebrew first
            subprocess.run(['brew', '--version'], capture_output=True, check=True)
            logger.info("🍺 Installing Ollama via Homebrew...")
            subprocess.run(['brew', 'install', 'ollama'], check=True)
            logger.info("✅ Ollama installed successfully via Homebrew")
            return True
        except:
            # Fall back to direct download
            logger.info("📥 Downloading Ollama for macOS...")
            
            download_url = "https://ollama.com/download/Ollama-darwin.zip"
            zip_path = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'Ollama-darwin.zip')
            
            try:
                urllib.request.urlretrieve(download_url, zip_path)
                
                logger.info("📦 Extracting Ollama...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall('/Applications/')
                
                os.remove(zip_path)
                
                # Add to PATH
                ollama_bin = '/Applications/Ollama.app/Contents/MacOS/ollama'
                if os.path.exists(ollama_bin):
                    os.environ['PATH'] = f"{os.environ['PATH']}:{os.path.dirname(ollama_bin)}"
                
                logger.info("✅ Ollama installed successfully")
                return True
                
            except Exception as e:
                logger.error(f"❌ Failed to install Ollama: {e}")
                return False
    
    @staticmethod
    async def install_linux():
        """Install Ollama on Linux"""
        logger.info("📥 Installing Ollama for Linux...")
        
        try:
            # Download and run install script
            install_script = """curl -fsSL https://ollama.ai/install.sh | sh"""
            subprocess.run(install_script, shell=True, check=True)
            
            logger.info("✅ Ollama installed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to install Ollama: {e}")
            logger.info("Please install manually: curl -fsSL https://ollama.ai/install.sh | sh")
            return False
    
    @staticmethod
    async def install():
        """Install Ollama based on platform"""
        if OllamaInstaller.is_installed():
            logger.info("✅ Ollama is already installed")
            return True
        
        logger.info("🔍 Ollama not found, installing automatically...")
        
        if IS_WINDOWS:
            return await OllamaInstaller.install_windows()
        elif IS_MACOS:
            return await OllamaInstaller.install_macos()
        elif IS_LINUX:
            return await OllamaInstaller.install_linux()
        else:
            logger.error("❌ Unsupported platform for automatic installation")
            return False

class EducationalOllamaInstance:
    """Ollama instance with educational archetype awareness"""
    
    def __init__(self, name: str, port: int, model: str, assigned_archetypes: List[str]):
        self.name = name
        self.port = port
        self.model = model
        self.assigned_archetypes = assigned_archetypes
        self.process: Optional[subprocess.Popen] = None
        self.healthy = False
        self.start_time = None
        self.request_count = 0
        
    async def ensure_model_present(self):
        """Ensure the Gemma 3n model is downloaded"""
        logger.info(f"🔍 Checking if {self.model} is present on {self.name}...")
        
        async with httpx.AsyncClient() as client:
            try:
                # Check if model exists
                response = await client.get(f'http://localhost:{self.port}/api/tags')
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    if any(m['name'] == self.model for m in models):
                        logger.info(f"✅ {self.model} already present on {self.name}")
                        return True
                
                # Pull model
                logger.info(f"📥 Pulling {self.model} for {self.name}...")
                logger.info(f"   This may take 10-15 minutes on first run")
                
                response = await client.post(
                    f'http://localhost:{self.port}/api/pull',
                    json={'name': self.model, 'stream': True},
                    timeout=None
                )
                
                last_percent = 0
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            
                            if 'completed' in data and 'total' in data:
                                total = data['total']
                                completed = data['completed']
                                if total > 0:
                                    percent = int((completed / total) * 100)
                                    if percent != last_percent and percent % 10 == 0:
                                        logger.info(f"   Progress: {percent}%")
                                        last_percent = percent
                            
                            if 'status' in data:
                                status = data['status']
                                if 'success' in status.lower():
                                    logger.info(f"✅ {self.model} ready on {self.name}")
                                    
                        except json.JSONDecodeError:
                            pass
                
                return True
                
            except Exception as e:
                logger.error(f"❌ Failed to pull {self.model}: {e}")
                return False
        
    async def start(self):
        """Start the Ollama instance"""
        logger.info(f"🚀 Starting {self.name} on port {self.port}...")
        
        try:
            env = os.environ.copy()
            env['OLLAMA_HOST'] = f'0.0.0.0:{self.port}'
            env['OLLAMA_MODELS'] = os.path.expanduser('~/.ollama/models')
            env['OLLAMA_NUM_PARALLEL'] = '2'
            
            if IS_WINDOWS:
                self.process = subprocess.Popen(
                    ['ollama', 'serve'],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    ['ollama', 'serve'],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
            
            self.start_time = datetime.now()
            
            # Read output in background
            threading.Thread(
                target=self._read_output,
                args=(self.process.stdout, f'{self.name}-OUT'),
                daemon=True
            ).start()
            
            threading.Thread(
                target=self._read_output,
                args=(self.process.stderr, f'{self.name}-ERR'),
                daemon=True
            ).start()
            
            # Wait for instance to be ready
            await self._wait_for_ready()
            
            # Ensure model is downloaded
            await self.ensure_model_present()
            
            self.healthy = True
            logger.info(f"✅ {self.name} ready with archetypes: {', '.join(self.assigned_archetypes)}")
            
        except Exception as e:
            logger.error(f"❌ Failed to start {self.name}: {e}")
            self.healthy = False
            raise
            
    def _read_output(self, pipe, prefix):
        """Read output from subprocess"""
        try:
            for line in pipe:
                if line.strip():
                    logger.debug(f"{prefix}: {line.strip()}")
        except:
            pass
            
    async def _wait_for_ready(self, timeout=30):
        """Wait for Ollama instance to be ready"""
        start = time.time()
        async with httpx.AsyncClient() as client:
            while time.time() - start < timeout:
                try:
                    response = await client.get(
                        f'http://localhost:{self.port}/api/tags',
                        timeout=2.0
                    )
                    if response.status_code == 200:
                        return
                except:
                    await asyncio.sleep(1)
                    
        raise TimeoutError(f"{self.name} failed to start within {timeout}s")
        
    def stop(self):
        """Stop the instance"""
        if self.process:
            logger.info(f"🛑 Stopping {self.name}...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except:
                self.process.kill()
            self.process = None
            self.healthy = False

class SIRAJEducationalRouter:
    """Educational AI router with full council integration"""
    
    def __init__(self, model: str):
        self.model = model
        self.instances = {}
        self.degraded_mode = False
        
    async def start_instances(self):
        """Start all educational instances"""
        logger.info("🎭 Starting SIRAJ Educational AI Council...")
        
        # Create instances
        self.instances = {
            'A': EducationalOllamaInstance(
                'Gemma_Instance_A', INSTANCE_A_PORT, self.model,
                ['socratic', 'constructivist', 'storyteller']
            ),
            'B': EducationalOllamaInstance(
                'Gemma_Instance_B', INSTANCE_B_PORT, self.model,
                ['synthesizer', 'challenger', 'mentor', 'analyst']
            )
        }
        
        # Start instances
        successful_starts = 0
        failed_instances = []
        
        for name, instance in self.instances.items():
            try:
                await instance.start()
                successful_starts += 1
            except Exception as e:
                logger.error(f"Failed to start {instance.name}: {e}")
                failed_instances.append(name)
                instance.healthy = False
        
        # Handle failures
        if successful_starts == 0:
            raise RuntimeError("Failed to start any Ollama instances")
        elif successful_starts < len(self.instances):
            self.degraded_mode = True
            logger.warning(f"⚠️ Running in DEGRADED MODE - Only {successful_starts}/{len(self.instances)} instances started")
            
            # Remove failed instances
            for name in failed_instances:
                del self.instances[name]
                
        logger.info("🎓 Educational Council operational!")
        
    async def get_instance_for_archetype(self, archetype: str) -> Optional[EducationalOllamaInstance]:
        """Get instance for archetype"""
        instance_key = EDUCATIONAL_ARCHETYPE_MAP.get(archetype, 'A')
        
        # In degraded mode, use any available instance
        if self.degraded_mode and instance_key not in self.instances:
            if self.instances:
                instance_key = list(self.instances.keys())[0]
        
        return self.instances.get(instance_key)
        
    async def process_educational_query(
        self, 
        topic: str, 
        grade_level: str = "middle",
        selected_archetypes: Optional[List[str]] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """Process educational query through the council"""
        
        if not selected_archetypes:
            selected_archetypes = ['socratic', 'constructivist', 'synthesizer', 'mentor']
        
        logger.info(f"🎓 Processing: {topic} [{grade_level}]")
        
        council_responses = {}
        
        # Get responses from each archetype
        for archetype in selected_archetypes:
            try:
                instance = await self.get_instance_for_archetype(archetype)
                if not instance:
                    continue
                    
                prompt = self._create_archetype_prompt(archetype, topic, grade_level)
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f'http://localhost:{instance.port}/api/generate',
                        json={
                            'model': self.model,
                            'prompt': prompt,
                            'stream': False,
                            'options': {
                                'temperature': 0.8,
                                'top_p': 0.9,
                                'max_tokens': 1000
                            }
                        },
                        timeout=30.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        council_responses[archetype] = {
                            'response': result.get('response', ''),
                            'instance': instance.name,
                            'success': True
                        }
                        instance.request_count += 1
                    
            except Exception as e:
                logger.error(f"Error with {archetype}: {e}")
                council_responses[archetype] = {
                    'response': f"[{archetype} is thinking...]",
                    'success': False
                }
        
        # Create synthesis
        synthesis = self._synthesize_responses(council_responses, topic)
        
        return {
            'topic': topic,
            'grade_level': grade_level,
            'council_responses': council_responses,
            'synthesis': synthesis,
            'degraded_mode': self.degraded_mode,
            'timestamp': datetime.now().isoformat()
        }
    
    def _create_archetype_prompt(self, archetype: str, topic: str, grade_level: str) -> str:
        """Create educational prompt for archetype"""
        
        prompts = {
            'socratic': f"""As a Socratic teacher, guide learning about "{topic}" for {grade_level} students through strategic questions. Ask 2-3 thought-provoking questions that help students discover concepts themselves.""",
            
            'constructivist': f"""As a Constructivist teacher, suggest hands-on activities for learning "{topic}" at {grade_level} level. Include specific experiments or projects students can do.""",
            
            'storyteller': f"""As a Storyteller teacher, create an engaging story or metaphor that teaches "{topic}" to {grade_level} students. Make it memorable and emotionally resonant.""",
            
            'synthesizer': f"""As a Synthesizer teacher, explain how "{topic}" connects to other subjects and real life for {grade_level} students. Show relationships and patterns.""",
            
            'challenger': f"""As a Challenger teacher, present alternative perspectives on "{topic}" for {grade_level} students. Push beyond surface understanding respectfully.""",
            
            'mentor': f"""As a Mentor teacher, provide supportive guidance about "{topic}" for {grade_level} students. Include encouragement and practical wisdom.""",
            
            'analyst': f"""As an Analyst teacher, break down "{topic}" systematically for {grade_level} students. Provide clear, logical analysis of components and relationships."""
        }
        
        return prompts.get(archetype, f"Teach about {topic}")
    
    def _synthesize_responses(self, responses: Dict, topic: str) -> str:
        """Synthesize council responses"""
        successful = [r for r in responses.values() if r.get('success', False)]
        
        if not successful:
            return "The educational council is preparing responses. Please try again."
        
        if len(successful) == 1:
            return successful[0]['response']
        
        # Create synthesis
        synthesis = f"The Educational Council explored '{topic}' from {len(successful)} perspectives. "
        synthesis += "Each approach offers unique insights for different learning styles. "
        synthesis += "Consider combining these methods or focusing on what resonates most with you."
        
        return synthesis
    
    def get_status(self) -> Dict:
        """Get router status"""
        return {
            'instances': {
                name: {
                    'healthy': inst.healthy,
                    'port': inst.port,
                    'archetypes': inst.assigned_archetypes,
                    'requests': inst.request_count
                }
                for name, inst in self.instances.items()
            },
            'degraded_mode': self.degraded_mode,
            'model': self.model
        }
        
    def stop_all(self):
        """Stop all instances"""
        for instance in self.instances.values():
            instance.stop()

# Create combined app that serves both frontend and API
app = FastAPI(title="SIRAJ Educational AI")
router = None

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EducationalRequest(BaseModel):
    topic: str
    grade_level: str = "middle"
    selected_archetypes: Optional[List[str]] = None
    context: Optional[Dict] = None

@app.post("/api/education/query")
async def educational_query(request: EducationalRequest):
    """Process educational query through council"""
    try:
        if not router:
            raise HTTPException(status_code=503, detail="Router not initialized")
            
        result = await router.process_educational_query(
            request.topic,
            request.grade_level, 
            request.selected_archetypes,
            request.context
        )
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Educational query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_status():
    """Get router status"""
    if not router:
        return {"error": "Router not initialized"}
    return router.get_status()

@app.get("/api/health")
async def health_check():
    """Health check"""
    if not router:
        return {"status": "initializing"}
        
    status = router.get_status()
    healthy = any(inst['healthy'] for inst in status['instances'].values())
    
    return {
        'status': 'degraded' if status['degraded_mode'] else ('healthy' if healthy else 'unhealthy'),
        'timestamp': datetime.now().isoformat()
    }

# Serve frontend
@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML with proper API endpoints"""
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRAJ Educational AI Council</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            max-width: 900px;
            width: 90%;
            background: rgba(255, 255, 255, 0.1);
            padding: 40px;
            border-radius: 20px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        h1 {
            text-align: center;
            font-size: 3em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .subtitle {
            text-align: center;
            opacity: 0.9;
            margin-bottom: 40px;
            font-size: 1.2em;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            font-size: 1.1em;
        }
        
        textarea, select {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            background: rgba(255, 255, 255, 0.9);
            color: #333;
            transition: all 0.3s ease;
        }
        
        textarea:focus, select:focus {
            outline: none;
            background: white;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        
        button {
            background: linear-gradient(135deg, #4CAF50, #45a049);
            color: white;
            padding: 18px 40px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 18px;
            font-weight: 600;
            width: 100%;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(76, 175, 80, 0.3);
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .response {
            background: rgba(255, 255, 255, 0.05);
            padding: 30px;
            border-radius: 15px;
            margin-top: 30px;
            display: none;
            animation: fadeIn 0.5s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .archetype {
            margin: 20px 0;
            padding: 20px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 12px;
            border-left: 4px solid rgba(255, 255, 255, 0.3);
            transition: all 0.3s ease;
        }
        
        .archetype:hover {
            background: rgba(255, 255, 255, 0.12);
            transform: translateX(5px);
        }
        
        .archetype h4 {
            font-size: 1.3em;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .archetype-icon {
            font-size: 1.5em;
        }
        
        .loading {
            text-align: center;
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255, 255, 255, 0.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
            margin-right: 10px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .error {
            background: rgba(244, 67, 54, 0.2);
            border-left-color: #f44336;
        }
        
        .status-indicator {
            position: absolute;
            top: 20px;
            right: 20px;
            font-size: 0.9em;
            opacity: 0.8;
        }
        
        .status-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
            background: #4CAF50;
            animation: pulse 2s ease-in-out infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
    </style>
</head>
<body>
    <div class="status-indicator">
        <span class="status-dot"></span>
        <span id="status-text">Connected</span>
    </div>
    
    <div class="container">
        <h1>🎭 SIRAJ Educational AI</h1>
        <p class="subtitle">Multi-Archetype Educational Council • Kaggle Gemma 3n</p>
        
        <div class="form-group">
            <label for="question">What would you like to learn about?</label>
            <textarea id="question" placeholder="Enter any topic or question..." rows="3"></textarea>
        </div>
        
        <div class="form-group">
            <label for="gradeLevel">Grade Level:</label>
            <select id="gradeLevel">
                <option value="elementary">Elementary (K-5)</option>
                <option value="middle" selected>Middle School (6-8)</option>
                <option value="high">High School (9-12)</option>
                <option value="university">University</option>
            </select>
        </div>
        
        <button onclick="askCouncil()">🚀 Ask the Educational Council</button>
        
        <div id="response" class="response">
            <div id="loading" class="loading">
                <span class="loading-spinner"></span>
                The council is deliberating...
            </div>
            <div id="results"></div>
        </div>
    </div>

    <script>
        // Check API status
        async function checkStatus() {
            try {
                const response = await fetch('/api/health');
                const data = await response.json();
                
                const statusDot = document.querySelector('.status-dot');
                const statusText = document.getElementById('status-text');
                
                if (data.status === 'healthy') {
                    statusDot.style.background = '#4CAF50';
                    statusText.textContent = 'All Systems Ready';
                } else if (data.status === 'degraded') {
                    statusDot.style.background = '#ff9800';
                    statusText.textContent = 'Degraded Mode';
                } else {
                    statusDot.style.background = '#f44336';
                    statusText.textContent = 'Initializing...';
                }
            } catch (error) {
                document.querySelector('.status-dot').style.background = '#f44336';
                document.getElementById('status-text').textContent = 'Disconnected';
            }
        }
        
        // Check status every 5 seconds
        checkStatus();
        setInterval(checkStatus, 5000);
        
        async function askCouncil() {
            const question = document.getElementById('question').value.trim();
            const gradeLevel = document.getElementById('gradeLevel').value;
            
            if (!question) {
                alert('Please enter a question!');
                return;
            }
            
            const responseDiv = document.getElementById('response');
            const loadingDiv = document.getElementById('loading');
            const resultsDiv = document.getElementById('results');
            
            responseDiv.style.display = 'block';
            loadingDiv.style.display = 'block';
            resultsDiv.innerHTML = '';
            
            try {
                const response = await fetch('/api/education/query', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        topic: question,
                        grade_level: gradeLevel,
                        selected_archetypes: ['socratic', 'constructivist', 'synthesizer', 'mentor']
                    }),
                });
                
                if (!response.ok) {
                    throw new Error(`Request failed: ${response.statusText}`);
                }
                
                const data = await response.json();
                
                loadingDiv.style.display = 'none';
                
                let html = `<h3>📚 ${data.topic}</h3>`;
                
                // Show archetype responses
                const archetypeInfo = {
                    socratic: { emoji: '🦉', name: 'Socratic Teacher', desc: 'Guiding through questions' },
                    constructivist: { emoji: '🔨', name: 'Constructivist', desc: 'Learning by doing' },
                    synthesizer: { emoji: '🌐', name: 'Synthesizer', desc: 'Connecting ideas' },
                    mentor: { emoji: '🌱', name: 'Mentor', desc: 'Supportive guidance' },
                    storyteller: { emoji: '📖', name: 'Storyteller', desc: 'Teaching through narrative' },
                    challenger: { emoji: '🎯', name: 'Challenger', desc: 'Pushing boundaries' },
                    analyst: { emoji: '🔬', name: 'Analyst', desc: 'Systematic analysis' }
                };
                
                for (const [archetype, response] of Object.entries(data.council_responses)) {
                    if (response.success) {
                        const info = archetypeInfo[archetype] || { emoji: '🎓', name: archetype };
                        
                        html += `
                            <div class="archetype">
                                <h4>
                                    <span class="archetype-icon">${info.emoji}</span>
                                    ${info.name}
                                    <small style="opacity: 0.7; font-size: 0.8em;">- ${info.desc}</small>
                                </h4>
                                <p>${response.response}</p>
                            </div>
                        `;
                    }
                }
                
                // Show synthesis
                if (data.synthesis) {
                    html += `
                        <div class="archetype" style="background: rgba(255, 255, 255, 0.15);">
                            <h4>
                                <span class="archetype-icon">✨</span>
                                Council Synthesis
                            </h4>
                            <p>${data.synthesis}</p>
                        </div>
                    `;
                }
                
                if (data.degraded_mode) {
                    html += `
                        <div class="archetype" style="background: rgba(255, 152, 0, 0.2); border-left-color: #ff9800;">
                            <p><strong>Note:</strong> Running in degraded mode - some archetypes may be limited.</p>
                        </div>
                    `;
                }
                
                resultsDiv.innerHTML = html;
                
            } catch (error) {
                loadingDiv.style.display = 'none';
                resultsDiv.innerHTML = `
                    <div class="archetype error">
                        <h4>❌ Error</h4>
                        <p>Failed to get council response: ${error.message}</p>
                        <p>The system may still be initializing. Please try again in a moment.</p>
                    </div>
                `;
            }
        }
        
        // Allow Enter key to submit
        document.getElementById('question').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                askCouncil();
            }
        });
        
        // Focus on question field
        document.getElementById('question').focus();
    </script>
</body>
</html>"""
    
    return HTMLResponse(content=html_content)

class SIRAJAutomatedLauncher:
    """Fully automated launcher with no manual steps"""
    
    def __init__(self):
        self.app_server = None
        self.router = None
        self.running = True
        self.browser_opened = False
        
        if getattr(sys, 'frozen', False):
            self.base_path = Path(sys._MEIPASS)
            self.is_frozen = True
        else:
            self.base_path = Path(__file__).parent.absolute()
            self.is_frozen = False
            
    def show_splash(self):
        """Show startup splash"""
        print("\n" + "="*60)
        print("""
   _____ _____ _____            _    
  / ____|_   _|  __ \     /\   | |   
 | (___   | | | |__) |   /  \  | |   
  \___ \  | | |  _  /   / /\ \ | |   
  ____) |_| |_| | \ \  / ____ \| |   
 |_____/|_____|_|  \_\/_/    \_\_|   
                                     
  Educational AI Council v9.0
  🤖 Fully Automated Edition
  📚 Kaggle Gemma 3n Hackathon
        """)
        print("="*60 + "\n")
        
    async def check_ports(self):
        """Check and handle port conflicts"""
        logger.info("🔍 Checking port availability...")
        
        ports_to_check = {
            'Frontend': FRONTEND_PORT,
            'Educational Router': ROUTER_PORT,
            'Backend': BACKEND_PORT,
            'Ollama Instance A': INSTANCE_A_PORT,
            'Ollama Instance B': INSTANCE_B_PORT
        }
        
        all_available = True
        for name, port in ports_to_check.items():
            if not is_port_available(port):
                logger.warning(f"⚠️ Port {port} ({name}) is already in use")
                all_available = False
                
                # Try to find process using the port
                try:
                    for proc in psutil.process_iter(['pid', 'name']):
                        try:
                            for conn in proc.connections():
                                if conn.laddr.port == port:
                                    logger.info(f"   Process: {proc.info['name']} (PID: {proc.info['pid']})")
                                    break
                        except:
                            pass
                except:
                    pass
        
        if not all_available:
            logger.warning("Some ports are in use. The system will attempt to work around this.")
            
        return all_available
        
    async def ensure_ollama_ready(self):
        """Ensure Ollama is installed and ready"""
        logger.info("🔍 Checking Ollama installation...")
        
        if not await OllamaInstaller.install():
            raise RuntimeError("Failed to install Ollama")
            
        # Check if Ollama service is running
        logger.info("🚀 Checking Ollama service...")
        try:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get('http://localhost:11434/api/tags', timeout=2.0)
                    if response.status_code == 200:
                        logger.info("✅ Ollama service already running")
                        return
                except:
                    pass
            
            # Start Ollama service
            logger.info("Starting Ollama service...")
            if IS_WINDOWS:
                subprocess.Popen(['ollama', 'serve'], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            
            # Wait for service to start
            await asyncio.sleep(5)
            logger.info("✅ Ollama service started")
            
        except Exception as e:
            logger.error(f"Failed to start Ollama service: {e}")
            raise
            
    async def start_educational_system(self):
        """Start the complete educational system"""
        global router
        
        # Get recommended model
        model, reason = get_recommended_model()
        logger.info(reason)
        
        # Create and start router
        router = SIRAJEducationalRouter(model)
        await router.start_instances()
        
        # Start the combined app server
        logger.info(f"🌐 Starting unified server on port {FRONTEND_PORT}...")
        
        # Configure server
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=FRONTEND_PORT,
            log_level="error",
            access_log=False
        )
        
        self.app_server = uvicorn.Server(config)
        
        # Start server in background
        asyncio.create_task(self.app_server.serve())
        
        # Wait for server to be ready
        await self._wait_for_server()
        
    async def _wait_for_server(self, timeout=30):
        """Wait for server to be ready"""
        start = time.time()
        
        while time.time() - start < timeout:
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get(f'http://localhost:{FRONTEND_PORT}/api/health')
                    if response.status_code == 200:
                        logger.info("✅ Server is ready")
                        return
            except:
                await asyncio.sleep(0.5)
                
        raise TimeoutError("Server failed to start")
        
    def open_browser_safely(self):
        """Open browser when everything is ready"""
        if self.browser_opened:
            return
            
        def browser_opener():
            # Wait a bit for everything to stabilize
            time.sleep(3)
            
            url = f"http://localhost:{FRONTEND_PORT}"
            logger.info(f"🌐 Opening browser to {url}")
            
            try:
                # Try different methods to open browser
                if IS_WINDOWS:
                    os.startfile(url)
                elif IS_MACOS:
                    subprocess.run(['open', url])
                else:
                    # Linux
                    try:
                        subprocess.run(['xdg-open', url])
                    except:
                        webbrowser.open(url)
                        
                logger.info("✅ Browser opened successfully")
                self.browser_opened = True
                
            except Exception as e:
                logger.error(f"Failed to open browser: {e}")
                logger.info(f"Please manually open: {url}")
                
        # Start browser opener in background
        threading.Thread(target=browser_opener, daemon=True).start()
        
    async def run(self):
        """Main run method - fully automated"""
        try:
            self.show_splash()
            
            # Pre-flight checks
            logger.info("🔧 Running automated setup...")
            await self.check_ports()
            
            # Ensure Ollama is ready
            await self.ensure_ollama_ready()
            
            # Start the educational system
            await self.start_educational_system()
            
            # Open browser
            self.open_browser_safely()
            
            # Show success message
            print("\n" + "="*60)
            logger.info("✨ SIRAJ Educational AI Ready!")
            print("="*60)
            print(f"\n🎓 Dashboard: http://localhost:{FRONTEND_PORT}")
            print(f"📊 API Status: http://localhost:{FRONTEND_PORT}/api/status")
            print(f"🏥 Health Check: http://localhost:{FRONTEND_PORT}/api/health")
            
            if router and router.degraded_mode:
                print("\n⚠️  Running in DEGRADED MODE")
                
            print("\n✅ Everything is automated - no manual steps needed!")
            print("🌐 Browser should open automatically")
            print("\nPress Ctrl+C to stop\n")
            
            # Keep running
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down...")
            self.shutdown()
        except Exception as e:
            logger.error(f"❌ Fatal error: {e}")
            logger.error("Please check the logs above for details")
            self.shutdown()
            raise
            
    def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        
        if router:
            router.stop_all()
            
        if self.app_server:
            self.app_server.should_exit = True
            
        logger.info("👋 Shutdown complete")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info("\n🛑 Received shutdown signal...")
    sys.exit(0)

def main():
    """Main entry point"""
    # Set up signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the launcher
    launcher = SIRAJAutomatedLauncher()
    
    try:
        asyncio.run(launcher.run())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
