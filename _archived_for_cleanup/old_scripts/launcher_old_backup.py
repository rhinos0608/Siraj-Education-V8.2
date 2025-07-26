#!/usr/bin/env python3
"""
SIRAJ Educational AI - Enhanced Multi-Instance Launcher
======================================================

Zero-touch launcher with automatic Ollama installation and Gemma 3n support:
- Auto-installs Ollama if missing
- Pulls Gemma 3n model based on system specs
- Launches two separate instances for true multi-voice AI
- Continues in degraded mode if one instance fails
- PyInstaller-safe for executable distribution
"""

import os
import sys
import time
import signal
import logging
import threading
import webbrowser
import subprocess
import asyncio
import json
import platform
import urllib.request
import zipfile
import shutil
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime
import psutil
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel

# Configure logging with colors
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

# Model selection based on system RAM
def get_recommended_model() -> Tuple[str, str]:
    """Determine which Gemma 3n model to use based on system RAM"""
    try:
        ram_gb = psutil.virtual_memory().total / (1024**3)
        if ram_gb >= 16:
            return "gemma3n:e4b", f"Selected Gemma 3n E4B (4B params) - {ram_gb:.1f}GB RAM detected"
        else:
            return "gemma3n:e2b", f"Selected Gemma 3n E2B (2B params) - {ram_gb:.1f}GB RAM detected"
    except:
        return "gemma3n:e2b", "Selected Gemma 3n E2B (default)"

# Get paths for PyInstaller compatibility
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Platform detection
PLATFORM = platform.system().lower()
IS_WINDOWS = PLATFORM == "windows"
IS_MACOS = PLATFORM == "darwin"
IS_LINUX = PLATFORM == "linux"

# Archetype to instance mapping
ARCHETYPE_INSTANCE_MAP = {
    'socratic': 'A',
    'constructivist': 'A', 
    'storyteller': 'A',
    'synthesizer': 'B',
    'challenger': 'B',
    'mentor': 'B',
    'analyst': 'B'
}

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
            # Download with progress
            def download_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(int(downloaded * 100 / total_size), 100)
                logger.info(f"Downloading Ollama... {percent}%")
            
            urllib.request.urlretrieve(installer_url, installer_path, download_progress)
            
            logger.info("🔧 Installing Ollama...")
            # Silent install
            subprocess.run([installer_path, '/S'], check=True)
            
            # Add to PATH if needed
            ollama_path = os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'Ollama')
            if os.path.exists(ollama_path):
                current_path = os.environ.get('PATH', '')
                if ollama_path not in current_path:
                    os.environ['PATH'] = f"{current_path};{ollama_path}"
            
            # Clean up installer
            os.remove(installer_path)
            
            logger.info("✅ Ollama installed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to install Ollama: {e}")
            return False
    
    @staticmethod
    async def install_macos():
        """Install Ollama on macOS"""
        # Check if Homebrew is available
        try:
            subprocess.run(['brew', '--version'], capture_output=True, check=True)
            logger.info("🍺 Installing Ollama via Homebrew...")
            subprocess.run(['brew', 'install', 'ollama'], check=True)
            logger.info("✅ Ollama installed successfully via Homebrew")
            return True
        except:
            # Fallback to direct download
            logger.info("📥 Downloading Ollama for macOS...")
            
            download_url = "https://ollama.com/download/Ollama-darwin.zip"
            zip_path = os.path.join(os.environ['TMPDIR'], 'Ollama-darwin.zip')
            
            try:
                # Download
                urllib.request.urlretrieve(download_url, zip_path)
                
                logger.info("📦 Extracting Ollama...")
                # Extract to Applications
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall('/Applications/')
                
                # Clean up
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
    async def install():
        """Install Ollama based on platform"""
        if OllamaInstaller.is_installed():
            logger.info("✅ Ollama is already installed")
            return True
        
        logger.info("🔍 Ollama not found, installing...")
        
        if IS_WINDOWS:
            return await OllamaInstaller.install_windows()
        elif IS_MACOS:
            return await OllamaInstaller.install_macos()
        else:
            logger.error("❌ Automatic Ollama installation not supported on Linux")
            logger.info("Please install Ollama manually: curl -fsSL https://ollama.ai/install.sh | sh")
            return False

class OllamaInstance:
    """Manages a single Ollama instance"""
    
    def __init__(self, name: str, port: int, model: str):
        self.name = name
        self.port = port
        self.model = model
        self.process: Optional[subprocess.Popen] = None
        self.healthy = False
        self.start_time = None
        self.request_count = 0
        self.last_health_check = None
        self.restart_count = 0
        
    async def ensure_model_present(self):
        """Ensure the model is downloaded"""
        logger.info(f"🔍 Checking if {self.model} is present on {self.name}...")
        
        async with httpx.AsyncClient() as client:
            try:
                # Check existing models
                response = await client.get(f'http://localhost:{self.port}/api/tags')
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    if any(m['name'] == self.model for m in models):
                        logger.info(f"✅ {self.model} already present on {self.name}")
                        return True
                
                # Pull the model
                logger.info(f"📥 Pulling {self.model} for {self.name}...")
                
                response = await client.post(
                    f'http://localhost:{self.port}/api/pull',
                    json={'name': self.model, 'stream': True},
                    timeout=None
                )
                
                # Stream progress
                last_percent = 0
                async for line in response.aiter_lines():
                    if line:
                        try:
                            data = json.loads(line)
                            
                            # Extract progress
                            if 'completed' in data and 'total' in data:
                                total = data['total']
                                completed = data['completed']
                                if total > 0:
                                    percent = int((completed / total) * 100)
                                    if percent != last_percent and percent % 10 == 0:
                                        logger.info(f"Pulling {self.model}... {percent}%")
                                        last_percent = percent
                            
                            # Show status messages
                            if 'status' in data:
                                status = data['status']
                                if 'pulling' not in status.lower() and 'verifying' not in status.lower():
                                    logger.info(f"{self.name}: {status}")
                                    
                        except json.JSONDecodeError:
                            pass
                
                logger.info(f"✅ {self.model} successfully pulled for {self.name}")
                return True
                
            except Exception as e:
                logger.error(f"❌ Failed to pull {self.model} for {self.name}: {e}")
                return False
        
    async def start(self):
        """Start the Ollama instance"""
        logger.info(f"🚀 Starting {self.name} on port {self.port}...")
        
        try:
            # Set environment for this instance
            env = os.environ.copy()
            env['OLLAMA_HOST'] = f'0.0.0.0:{self.port}'
            env['OLLAMA_MODELS'] = os.path.expanduser('~/.ollama/models')
            env['OLLAMA_NUM_PARALLEL'] = '2'
            
            # Start Ollama serve
            if IS_WINDOWS:
                # Windows needs special handling for subprocess
                self.process = subprocess.Popen(
                    ['ollama', 'serve'],
                    env=env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW if IS_WINDOWS else 0
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
            
            # Start output readers
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
            
            # Ensure model is loaded
            await self.ensure_model_present()
            
            self.healthy = True
            logger.info(f"✅ {self.name} is ready on port {self.port}")
            
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
        
    async def health_check(self) -> bool:
        """Check if instance is healthy"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f'http://localhost:{self.port}/api/tags',
                    timeout=5.0
                )
                self.healthy = response.status_code == 200
                self.last_health_check = datetime.now()
                return self.healthy
        except:
            self.healthy = False
            return False
            
    async def restart(self):
        """Restart the instance"""
        logger.warning(f"🔄 Restarting {self.name}...")
        self.restart_count += 1
        
        # Stop existing process
        if self.process:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except:
                self.process.kill()
                
        # Start again
        await self.start()
        
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

class SIRAJRequestRouter:
    """Intelligent request router for multi-instance Ollama"""
    
    def __init__(self, model: str):
        self.model = model
        self.instances = {
            'A': OllamaInstance('Gemma_Instance_A', INSTANCE_A_PORT, model),
            'B': OllamaInstance('Gemma_Instance_B', INSTANCE_B_PORT, model)
        }
        self.round_robin_counter = 0
        self.request_history = []
        self.degraded_mode = False
        
    async def start_instances(self):
        """Start all Ollama instances with graceful degradation"""
        logger.info("🎭 Starting multi-instance Gemma council...")
        
        successful_starts = 0
        failed_instances = []
        
        for name, instance in self.instances.items():
            try:
                logger.info(f"Starting {instance.name}...")
                await instance.start()
                successful_starts += 1
            except Exception as e:
                logger.error(f"Failed to start {instance.name}: {e}")
                failed_instances.append(name)
                instance.healthy = False
        
        # Check if we can continue
        if successful_starts == 0:
            logger.error("❌ No instances could be started!")
            raise RuntimeError("Failed to start any Ollama instances")
        elif successful_starts < len(self.instances):
            self.degraded_mode = True
            logger.warning(f"⚠️ Running in DEGRADED MODE - Only {successful_starts}/{len(self.instances)} instances started")
            logger.warning(f"Failed instances: {', '.join(failed_instances)}")
            
            # Disable failed instances
            for name in failed_instances:
                del self.instances[name]
        else:
            logger.info("✨ All instances started successfully!")
            
        logger.info("✨ SIRAJ Multi-Voice AI Council is operational!")
        
    async def get_instance_for_archetype(self, archetype: str) -> Optional[OllamaInstance]:
        """Get the appropriate instance for an archetype"""
        instance_key = ARCHETYPE_INSTANCE_MAP.get(archetype, 'A')
        
        # In degraded mode, use any available instance
        if self.degraded_mode and instance_key not in self.instances:
            # Use first available instance
            if self.instances:
                instance_key = list(self.instances.keys())[0]
                logger.debug(f"Degraded mode: routing {archetype} to {instance_key}")
            else:
                return None
        
        instance = self.instances.get(instance_key)
        if not instance:
            return None
            
        # Check health before returning
        if not instance.healthy:
            logger.warning(f"Instance {instance.name} unhealthy, checking...")
            if not await instance.health_check():
                # Try to restart
                try:
                    await instance.restart()
                except:
                    # If restart fails, try other instance
                    if self.degraded_mode:
                        return None
                    else:
                        # Enter degraded mode
                        self.degraded_mode = True
                        logger.warning("⚠️ Entering DEGRADED MODE")
                        
        return instance
        
    async def get_next_instance(self) -> Optional[OllamaInstance]:
        """Get next instance using round-robin"""
        if not self.instances:
            return None
            
        # In degraded mode with single instance
        if len(self.instances) == 1:
            return list(self.instances.values())[0]
        
        # Normal round-robin
        available_keys = list(self.instances.keys())
        instance_key = available_keys[self.round_robin_counter % len(available_keys)]
        self.round_robin_counter += 1
        
        return self.instances[instance_key]
        
    async def send_completion(self, prompt: str, archetype: str = None) -> Dict:
        """Send completion request to appropriate instance"""
        # Get instance based on archetype or round-robin
        if archetype:
            instance = await self.get_instance_for_archetype(archetype)
        else:
            instance = await self.get_next_instance()
            
        if not instance:
            raise HTTPException(status_code=503, detail="No healthy instances available")
            
        logger.info(f"📤 Routing request to {instance.name} (archetype: {archetype or 'general'})")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f'http://localhost:{instance.port}/api/generate',
                    json={
                        'model': self.model,
                        'prompt': prompt,
                        'stream': False,
                        'options': {
                            'temperature': 0.7,
                            'top_p': 0.9,
                            'max_tokens': 1000
                        }
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    instance.request_count += 1
                    
                    # Track request
                    self.request_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'instance': instance.name,
                        'archetype': archetype,
                        'success': True
                    })
                    
                    return {
                        'response': result.get('response', ''),
                        'instance': instance.name,
                        'archetype': archetype,
                        'model': self.model,
                        'degraded_mode': self.degraded_mode
                    }
                else:
                    raise HTTPException(status_code=response.status_code, detail="Generation failed")
                    
        except Exception as e:
            logger.error(f"Error with {instance.name}: {e}")
            
            # Track failure
            self.request_history.append({
                'timestamp': datetime.now().isoformat(),
                'instance': instance.name,
                'archetype': archetype,
                'success': False,
                'error': str(e)
            })
            
            raise
            
    async def health_check_loop(self):
        """Continuous health monitoring"""
        while True:
            try:
                for instance in self.instances.values():
                    healthy = await instance.health_check()
                    if not healthy and instance.restart_count < 3:
                        logger.warning(f"Health check failed for {instance.name}")
                        await instance.restart()
                        
                await asyncio.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Health check error: {e}")
                await asyncio.sleep(30)
                
    def get_status(self) -> Dict:
        """Get router status"""
        return {
            'instances': {
                name: {
                    'healthy': inst.healthy,
                    'port': inst.port,
                    'uptime': str(datetime.now() - inst.start_time) if inst.start_time else None,
                    'requests': inst.request_count,
                    'restarts': inst.restart_count,
                    'last_health_check': inst.last_health_check.isoformat() if inst.last_health_check else None
                }
                for name, inst in self.instances.items()
            },
            'round_robin_counter': self.round_robin_counter,
            'total_requests': len(self.request_history),
            'archetype_mapping': ARCHETYPE_INSTANCE_MAP,
            'degraded_mode': self.degraded_mode,
            'model': self.model
        }
        
    def stop_all(self):
        """Stop all instances"""
        for instance in self.instances.values():
            instance.stop()

# Create router API
router_app = FastAPI(title="SIRAJ Multi-Instance Router")

# Will be initialized later
router = None

# CORS middleware
router_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    prompt: str
    archetype: Optional[str] = None
    context: Optional[Dict] = None

@router_app.post("/api/query")
async def handle_query(request: QueryRequest):
    """Unified query endpoint"""
    try:
        result = await router.send_completion(request.prompt, request.archetype)
        return JSONResponse(content=result)
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router_app.get("/api/status")
async def get_status():
    """Get router status"""
    return router.get_status()

@router_app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    status = router.get_status()
    healthy = all(inst['healthy'] for inst in status['instances'].values())
    degraded = status.get('degraded_mode', False)
    
    return {
        'status': 'degraded' if degraded else ('healthy' if healthy else 'unhealthy'),
        'timestamp': datetime.now().isoformat(),
        'instances': status['instances'],
        'degraded_mode': degraded
    }

class SIRAJMultiInstanceLauncher:
    """Main launcher for multi-instance SIRAJ"""
    
    def __init__(self):
        self.backend_process: Optional[subprocess.Popen] = None
        self.frontend_process: Optional[subprocess.Popen] = None
        self.router_server = None
        self.running = True
        
        # Determine paths
        if getattr(sys, 'frozen', False):
            self.base_path = Path(sys._MEIPASS)
            self.is_frozen = True
        else:
            self.base_path = Path(__file__).parent.absolute()
            self.is_frozen = False
            
    def show_splash(self):
        """Show startup splash screen"""
        print("\n" + "="*60)
        print("""
   _____ _____ _____            _    
  / ____|_   _|  __ \     /\   | |   
 | (___   | | | |__) |   /  \  | |   
  \___ \  | | |  _  /   / /\ \ | |   
  ____) |_| |_| | \ \  / ____ \| |   
 |_____/|_____|_|  \_\/_/    \_\_|   
                                     
  Multi-Instance Educational AI v8.1
  🧠 Powered by Gemma 3n Technology
        """)
        print("="*60 + "\n")
        
    def setup_environment(self):
        """Setup environment variables"""
        logger.info("🔧 Setting up environment...")
        
        env_defaults = {
            'SIRAJ_VERSION': '8.1.0',
            'MULTI_INSTANCE_MODE': 'true',
            'ROUTER_URL': f'http://localhost:{ROUTER_PORT}',
            'INSTANCE_A_PORT': str(INSTANCE_A_PORT),
            'INSTANCE_B_PORT': str(INSTANCE_B_PORT),
            'BACKEND_PORT': str(BACKEND_PORT),
            'FRONTEND_PORT': str(FRONTEND_PORT),
            'DATABASE_URL': 'sqlite+aiosqlite:///./siraj_educational.db',
        }
        
        for key, value in env_defaults.items():
            if key not in os.environ:
                os.environ[key] = value
                
    async def ensure_ollama_ready(self):
        """Ensure Ollama is installed and ready"""
        logger.info("🔍 Checking Ollama...")
        
        # Install if needed
        if not await OllamaInstaller.install():
            raise RuntimeError("Failed to install Ollama")
            
        # Start Ollama service if not running
        logger.info("🚀 Starting Ollama service...")
        try:
            # Check if already running
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get('http://localhost:11434/api/tags', timeout=2.0)
                    if response.status_code == 200:
                        logger.info("✅ Ollama service already running")
                        return
                except:
                    pass
            
            # Start service
            if IS_WINDOWS:
                subprocess.Popen(['ollama', 'serve'], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            
            # Wait for service
            logger.info("⏳ Waiting for Ollama service...")
            await asyncio.sleep(3)
            
        except Exception as e:
            logger.error(f"Failed to start Ollama service: {e}")
            raise
            
    async def start_router_server(self):
        """Start the router API server"""
        global router
        
        # Determine model based on system specs
        model, reason = get_recommended_model()
        logger.info(f"🧠 {reason}")
        
        # Create router with selected model
        router = SIRAJRequestRouter(model)
        
        logger.info(f"🌐 Starting router API on port {ROUTER_PORT}...")
        
        # Start router instances
        await router.start_instances()
        
        # Start health check loop
        asyncio.create_task(router.health_check_loop())
        
        # Start router server
        config = uvicorn.Config(
            router_app,
            host="0.0.0.0",
            port=ROUTER_PORT,
            log_level="error"  # Reduce uvicorn logging
        )
        
        self.router_server = uvicorn.Server(config)
        
        # Run in background
        asyncio.create_task(self.router_server.serve())
        
        # Wait for router to be ready
        await self._wait_for_service(f"http://localhost:{ROUTER_PORT}/api/health", "Router")
        
    async def _wait_for_service(self, url: str, name: str, timeout: int = 30):
        """Wait for a service to be ready"""
        start = time.time()
        async with httpx.AsyncClient() as client:
            while time.time() - start < timeout:
                try:
                    response = await client.get(url, timeout=2.0)
                    if response.status_code == 200:
                        logger.info(f"✅ {name} is ready")
                        return
                except:
                    await asyncio.sleep(1)
                    
        raise TimeoutError(f"{name} failed to start within {timeout}s")
        
    def start_backend(self):
        """Start the SIRAJ backend"""
        logger.info("🎓 Starting SIRAJ backend...")
        
        backend_path = self.base_path / 'backend' / 'main.py'
        
        if backend_path.exists():
            cmd = [sys.executable, str(backend_path)]
            
            if IS_WINDOWS:
                self.backend_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.backend_process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )
            
            # Log output
            threading.Thread(
                target=self._read_output,
                args=(self.backend_process.stdout, 'BACKEND'),
                daemon=True
            ).start()
        else:
            logger.warning("Backend not found, skipping...")
            
    def start_frontend(self):
        """Start the frontend"""
        logger.info("🎨 Starting SIRAJ frontend...")
        
        # Check for built frontend
        frontend_build = self.base_path / 'frontend' / 'build'
        
        if frontend_build.exists():
            # Serve static files
            import http.server
            import socketserver
            
            os.chdir(str(frontend_build))
            
            Handler = http.server.SimpleHTTPRequestHandler
            
            def serve():
                with socketserver.TCPServer(("", FRONTEND_PORT), Handler) as httpd:
                    logger.info(f"📱 Frontend serving at http://localhost:{FRONTEND_PORT}")
                    httpd.serve_forever()
                    
            threading.Thread(target=serve, daemon=True).start()
        else:
            # Development mode
            frontend_dir = self.base_path / 'frontend'
            if frontend_dir.exists():
                cmd = ['npm', 'start']
                self.frontend_process = subprocess.Popen(
                    cmd,
                    cwd=str(frontend_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
            else:
                logger.warning("Frontend not found, skipping...")
                
    def _read_output(self, pipe, prefix):
        """Read subprocess output"""
        try:
            for line in pipe:
                if line.strip():
                    logger.debug(f"{prefix}: {line.strip()}")
        except:
            pass
            
    def open_browser(self):
        """Open browser to application"""
        time.sleep(3)  # Wait for services
        url = f"http://localhost:{FRONTEND_PORT}"
        logger.info(f"🌐 Opening browser to {url}")
        
        try:
            webbrowser.open(url)
        except:
            logger.info(f"Please open your browser to: {url}")
            
    async def run(self):
        """Main run method"""
        try:
            self.show_splash()
            self.setup_environment()
            
            # Pre-run checks
            logger.info("📋 Running pre-flight checks...")
            await self.ensure_ollama_ready()
            
            # Start services
            await self.start_router_server()
            self.start_backend()
            self.start_frontend()
            self.open_browser()
            
            # Check if running in degraded mode
            if router and router.degraded_mode:
                logger.warning("⚠️  SYSTEM RUNNING IN DEGRADED MODE")
                logger.warning("Some features may be limited")
            
            # Show status
            print("\n" + "="*60)
            logger.info("✨ System Ready")
            print("="*60)
            print(f"\n📊 Dashboard: http://localhost:{FRONTEND_PORT}")
            print(f"🌐 Router API: http://localhost:{ROUTER_PORT}/api/status")
            print(f"📚 Backend API: http://localhost:{BACKEND_PORT}/docs")
            
            active_instances = [name for name, inst in router.instances.items() if inst.healthy]
            print(f"🧠 Active Instances: {', '.join(active_instances)}")
            
            if router.degraded_mode:
                print("\n⚠️  DEGRADED MODE - Some instances failed to start")
            
            print("\nPress Ctrl+C to stop\n")
            
            # Keep running
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down...")
            self.shutdown()
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            self.shutdown()
            raise
            
    def shutdown(self):
        """Graceful shutdown"""
        self.running = False
        
        # Stop router
        if router:
            router.stop_all()
        
        # Stop backend
        if self.backend_process:
            self.backend_process.terminate()
            
        # Stop frontend
        if self.frontend_process:
            self.frontend_process.terminate()
            
        logger.info("👋 SIRAJ shutdown complete")

def main():
    """Main entry point"""
    launcher = SIRAJMultiInstanceLauncher()
    
    # Run async main
    asyncio.run(launcher.run())

if __name__ == '__main__':
    main()
