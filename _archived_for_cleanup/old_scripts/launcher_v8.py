#!/usr/bin/env python3
"""
SIRAJ Educational AI - Fixed Browser Launch v8.3
===============================================

For Kaggle Gemma 3n Hackathon
Developed with Python 3.12.3

Fixes browser auto-launch and frontend service issues:
- Proper service startup sequencing
- Better frontend service detection
- Improved browser opening timing
- Enhanced error handling
"""

# Python 3.12.3 is our development version
# The hackathon has no version restrictions

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
import socket
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

# Utility functions
def is_port_available(port):
    """Check if a port is available"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return True
        except OSError:
            return False

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

# Platform detection
PLATFORM = platform.system().lower()
IS_WINDOWS = PLATFORM == "windows"
IS_MACOS = PLATFORM == "darwin"
IS_LINUX = PLATFORM == "linux"

# Educational archetype to instance mapping
EDUCATIONAL_ARCHETYPE_MAP = {
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
            def download_progress(block_num, block_size, total_size):
                downloaded = block_num * block_size
                percent = min(int(downloaded * 100 / total_size), 100)
                if percent % 20 == 0:
                    logger.info(f"Downloading Ollama... {percent}%")
            
            urllib.request.urlretrieve(installer_url, installer_path, download_progress)
            
            logger.info("🔧 Installing Ollama...")
            subprocess.run([installer_path, '/S'], check=True)
            
            ollama_path = os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'Ollama')
            if os.path.exists(ollama_path):
                current_path = os.environ.get('PATH', '')
                if ollama_path not in current_path:
                    os.environ['PATH'] = f"{current_path};{ollama_path}"
            
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
            subprocess.run(['brew', '--version'], capture_output=True, check=True)
            logger.info("🍺 Installing Ollama via Homebrew...")
            subprocess.run(['brew', 'install', 'ollama'], check=True)
            logger.info("✅ Ollama installed successfully via Homebrew")
            return True
        except:
            logger.info("📥 Downloading Ollama for macOS...")
            
            download_url = "https://ollama.com/download/Ollama-darwin.zip"
            zip_path = os.path.join(os.environ.get('TMPDIR', '/tmp'), 'Ollama-darwin.zip')
            
            try:
                urllib.request.urlretrieve(download_url, zip_path)
                
                logger.info("📦 Extracting Ollama...")
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall('/Applications/')
                
                os.remove(zip_path)
                
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

class EducationalOllamaInstance:
    """Enhanced Ollama instance with educational archetype awareness"""
    
    def __init__(self, name: str, port: int, model: str, assigned_archetypes: List[str]):
        self.name = name
        self.port = port
        self.model = model
        self.assigned_archetypes = assigned_archetypes
        self.process: Optional[subprocess.Popen] = None
        self.healthy = False
        self.start_time = None
        self.request_count = 0
        self.last_health_check = None
        self.restart_count = 0
        
    async def ensure_model_present(self):
        """Ensure the Gemma 3n model is downloaded"""
        logger.info(f"🔍 Checking if {self.model} is present on {self.name}...")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f'http://localhost:{self.port}/api/tags')
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    if any(m['name'] == self.model for m in models):
                        logger.info(f"✅ {self.model} already present on {self.name}")
                        return True
                
                logger.info(f"📥 Pulling {self.model} for {self.name} (archetypes: {', '.join(self.assigned_archetypes)})...")
                
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
                                        logger.info(f"Pulling {self.model}... {percent}%")
                                        last_percent = percent
                            
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
        """Start the educational Ollama instance"""
        logger.info(f"🚀 Starting {self.name} on port {self.port} (archetypes: {', '.join(self.assigned_archetypes)})...")
        
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
            
            await self._wait_for_ready()
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
        
        self.instances = {
            'A': EducationalOllamaInstance(
                'Gemma_Instance_A', INSTANCE_A_PORT, model,
                ['socratic', 'constructivist', 'storyteller']
            ),
            'B': EducationalOllamaInstance(
                'Gemma_Instance_B', INSTANCE_B_PORT, model,
                ['synthesizer', 'challenger', 'mentor', 'analyst']
            )
        }
        
        self.round_robin_counter = 0
        self.request_history = []
        self.degraded_mode = False
        
    async def start_instances(self):
        """Start all educational instances with graceful degradation"""
        logger.info("🎭 Starting SIRAJ Educational AI Council...")
        
        successful_starts = 0
        failed_instances = []
        
        for name, instance in self.instances.items():
            try:
                logger.info(f"Starting {instance.name} for archetypes: {', '.join(instance.assigned_archetypes)}")
                await instance.start()
                successful_starts += 1
            except Exception as e:
                logger.error(f"Failed to start {instance.name}: {e}")
                failed_instances.append(name)
                instance.healthy = False
        
        if successful_starts == 0:
            logger.error("❌ No instances could be started!")
            raise RuntimeError("Failed to start any Ollama instances")
        elif successful_starts < len(self.instances):
            self.degraded_mode = True
            logger.warning(f"⚠️ Running in DEGRADED MODE - Only {successful_starts}/{len(self.instances)} instances started")
            logger.warning(f"Failed instances: {', '.join(failed_instances)}")
            
            for name in failed_instances:
                del self.instances[name]
        else:
            logger.info("✨ All educational instances started successfully!")
            
        logger.info("🎓 SIRAJ Educational AI Council is operational!")
        
    async def get_instance_for_archetype(self, archetype: str) -> Optional[EducationalOllamaInstance]:
        """Get the appropriate instance for an educational archetype"""
        instance_key = EDUCATIONAL_ARCHETYPE_MAP.get(archetype, 'A')
        
        if self.degraded_mode and instance_key not in self.instances:
            if self.instances:
                instance_key = list(self.instances.keys())[0]
                logger.debug(f"Degraded mode: routing {archetype} to {instance_key}")
            else:
                return None
        
        instance = self.instances.get(instance_key)
        if not instance:
            return None
            
        if not instance.healthy:
            logger.warning(f"Instance {instance.name} unhealthy, checking...")
            if not await instance.health_check():
                if not self.degraded_mode:
                    self.degraded_mode = True
                    logger.warning("⚠️ Entering DEGRADED MODE")
                        
        return instance
        
    async def process_educational_query(
        self, 
        topic: str, 
        grade_level: str = "middle",
        selected_archetypes: Optional[List[str]] = None,
        context: Optional[Dict] = None
    ) -> Dict:
        """Process educational query through the council"""
        
        session_id = f"edu_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not selected_archetypes:
            selected_archetypes = ['socratic', 'constructivist', 'synthesizer', 'mentor']
        
        logger.info(f"🎓 Processing educational query: {topic}")
        logger.info(f"📚 Grade level: {grade_level}, Archetypes: {', '.join(selected_archetypes)}")
        
        educational_context = self._build_educational_context(topic, grade_level, context)
        
        council_responses = {}
        
        for archetype in selected_archetypes:
            try:
                instance = await self.get_instance_for_archetype(archetype)
                if not instance:
                    continue
                    
                educational_prompt = self._create_archetype_prompt(archetype, topic, educational_context)
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f'http://localhost:{instance.port}/api/generate',
                        json={
                            'model': self.model,
                            'prompt': educational_prompt,
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
                            'archetype_role': self._get_archetype_role(archetype),
                            'teaching_focus': self._get_teaching_focus(archetype),
                            'success': True
                        }
                        instance.request_count += 1
                        logger.info(f"✅ {archetype} responded from {instance.name}")
                    
            except Exception as e:
                logger.error(f"❌ Error with {archetype}: {e}")
                council_responses[archetype] = {
                    'response': f"[{archetype} is reflecting deeply...]",
                    'success': False,
                    'error': str(e)
                }
        
        synthesis = await self._synthesize_responses(council_responses, topic, educational_context)
        
        return {
            'session_id': session_id,
            'topic': topic,
            'grade_level': grade_level,
            'council_responses': council_responses,
            'synthesis': synthesis,
            'next_steps': self._generate_next_steps(topic, council_responses),
            'consciousness_level': self._calculate_consciousness_level(council_responses),
            'degraded_mode': self.degraded_mode,
            'timestamp': datetime.now().isoformat()
        }
    
    def _build_educational_context(self, topic: str, grade_level: str, context: Optional[Dict]) -> str:
        """Build educational context"""
        parts = [
            f"Educational Topic: {topic}",
            f"Student Level: {grade_level}",
            f"Teaching Mode: Multi-archetype council approach"
        ]
        
        if context:
            if context.get('learning_style'):
                parts.append(f"Learning Style: {context['learning_style']}")
            if context.get('background'):
                parts.append(f"Background: {context['background']}")
        
        return " | ".join(parts)
    
    def _create_archetype_prompt(self, archetype: str, topic: str, context: str) -> str:
        """Create educational prompt for archetype"""
        
        prompts = {
            'socratic': f"""You are a Socratic teacher in the SIRAJ Educational Council. Your role is to guide learning through strategic questions and critical thinking.

Topic: {topic}
Context: {context}

Respond as the Socratic teacher would: Ask 2-3 thought-provoking questions that help students discover the core concepts themselves. Use "What do you think?" and "Why?" frequently. Help students examine their assumptions and reasoning.

End with an invitation for further exploration.""",

            'constructivist': f"""You are a Constructivist teacher in the SIRAJ Educational Council. Your role is to promote hands-on learning and experiential discovery.

Topic: {topic}
Context: {context}

Respond as the Constructivist teacher would: Suggest 2-3 specific hands-on activities, experiments, or projects that help students build understanding through direct experience. Include what materials they might need and what they would discover.""",

            'storyteller': f"""You are a Storyteller teacher in the SIRAJ Educational Council. Your role is to teach through narrative, metaphors, and engaging stories.

Topic: {topic}
Context: {context}

Respond as the Storyteller teacher would: Create a brief, engaging story or powerful metaphor that illuminates the key concepts. Make it emotionally resonant and memorable.""",

            'synthesizer': f"""You are a Synthesizer teacher in the SIRAJ Educational Council. Your role is to integrate different perspectives and show connections.

Topic: {topic}
Context: {context}

Respond as the Synthesizer teacher would: Explain how this topic connects to other areas of knowledge and life. Show relationships and patterns that create coherent understanding.""",

            'challenger': f"""You are a Challenger teacher in the SIRAJ Educational Council. Your role is to push intellectual boundaries and question assumptions.

Topic: {topic}
Context: {context}

Respond as the Challenger teacher would: Present alternative perspectives or provocative questions that push beyond surface understanding. Challenge conventional thinking respectfully.""",

            'mentor': f"""You are a Mentor teacher in the SIRAJ Educational Council. Your role is to provide supportive guidance and encouragement.

Topic: {topic}
Context: {context}

Respond as the Mentor teacher would: Provide warm, encouraging guidance that builds confidence. Include affirmation and motivation along with practical wisdom.""",

            'analyst': f"""You are an Analyst teacher in the SIRAJ Educational Council. Your role is to provide systematic, logical analysis.

Topic: {topic}
Context: {context}

Respond as the Analyst teacher would: Provide clear, logical breakdown of the topic. Analyze components, relationships, and systematic approaches to understanding."""
        }
        
        return prompts.get(archetype, f"Provide educational guidance on: {topic}")
    
    def _get_archetype_role(self, archetype: str) -> str:
        """Get role description"""
        roles = {
            'socratic': "Strategic Questioner",
            'constructivist': "Hands-on Learning Guide",
            'storyteller': "Narrative Teacher",
            'synthesizer': "Connection Builder",
            'challenger': "Critical Thinker",
            'mentor': "Supportive Guide",
            'analyst': "Systematic Analyzer"
        }
        return roles.get(archetype, "Educational Guide")
    
    def _get_teaching_focus(self, archetype: str) -> str:
        """Get teaching focus"""
        focuses = {
            'socratic': "Critical thinking through questioning",
            'constructivist': "Learning by doing and building",
            'storyteller': "Understanding through narrative",
            'synthesizer': "Connecting ideas and concepts",
            'challenger': "Pushing intellectual boundaries",
            'mentor': "Building confidence and support",
            'analyst': "Logical and systematic thinking"
        }
        return focuses.get(archetype, "General education")
    
    async def _synthesize_responses(self, responses: Dict, topic: str, context: str) -> str:
        """Synthesize council responses"""
        
        successful = {k: v for k, v in responses.items() if v.get('success', False)}
        
        if not successful:
            return "The educational council is assembling wisdom. Please try again shortly."
        
        if len(successful) == 1:
            archetype, response = list(successful.items())[0]
            return f"The {archetype} teacher offers this guidance: {response['response']}"
        
        synthesis = f"The SIRAJ Educational Council has explored '{topic}' from {len(successful)} teaching perspectives:\n\n"
        
        for archetype, data in successful.items():
            synthesis += f"**{data['archetype_role']}**: {data['teaching_focus']}\n"
            synthesis += f"{data['response'][:150]}...\n\n"
        
        synthesis += "**Council Synthesis**: Each perspective offers a unique pathway to understanding. "
        synthesis += "Combine these approaches for the richest learning experience, or focus on the style that resonates most with you."
        
        return synthesis
    
    def _generate_next_steps(self, topic: str, responses: Dict) -> List[str]:
        """Generate learning next steps"""
        steps = [
            f"Explore the {topic} topic using your preferred learning style",
            "Try the hands-on activities suggested by the Constructivist",
            "Reflect on the questions posed by the Socratic teacher",
            "Consider the story or metaphor from the Storyteller"
        ]
        
        if 'challenger' in responses:
            steps.append("Challenge yourself with alternative perspectives")
        
        if 'synthesizer' in responses:
            steps.append("Look for connections to other subjects you're studying")
        
        return steps
    
    def _calculate_consciousness_level(self, responses: Dict) -> float:
        """Calculate consciousness level"""
        successful = sum(1 for r in responses.values() if r.get('success', False))
        total = len(responses)
        
        if total == 0:
            return 0.0
        
        base = successful / total
        bonus = min(successful * 0.1, 0.3)
        
        return round(min(base + bonus, 1.0), 2)
    
    def get_status(self) -> Dict:
        """Get router status"""
        return {
            'instances': {
                name: {
                    'healthy': inst.healthy,
                    'port': inst.port,
                    'assigned_archetypes': inst.assigned_archetypes,
                    'uptime': str(datetime.now() - inst.start_time) if inst.start_time else None,
                    'requests': inst.request_count,
                    'restarts': inst.restart_count
                }
                for name, inst in self.instances.items()
            },
            'degraded_mode': self.degraded_mode,
            'model': self.model,
            'archetype_mapping': EDUCATIONAL_ARCHETYPE_MAP
        }
        
    def stop_all(self):
        """Stop all instances"""
        for instance in self.instances.values():
            instance.stop()

# Create educational router API
router_app = FastAPI(title="SIRAJ Educational Router")
router = None

router_app.add_middleware(
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

@router_app.post("/api/education/query")
async def educational_query(request: EducationalRequest):
    """Process educational query through council"""
    try:
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

@router_app.get("/api/status")
async def get_status():
    """Get router status"""
    return router.get_status()

@router_app.get("/api/health")
async def health_check():
    """Health check"""
    status = router.get_status()
    healthy = all(inst['healthy'] for inst in status['instances'].values())
    
    return {
        'status': 'degraded' if status['degraded_mode'] else ('healthy' if healthy else 'unhealthy'),
        'timestamp': datetime.now().isoformat(),
        'instances': status['instances'],
        'degraded_mode': status['degraded_mode']
    }

class SIRAJFixedLauncher:
    """Fixed launcher with proper browser launching and frontend service"""
    
    def __init__(self):
        self.backend_process: Optional[subprocess.Popen] = None
        self.frontend_process: Optional[subprocess.Popen] = None
        self.router_server = None
        self.running = True
        
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
                                     
  Educational AI Council v8.3
  🎭 Fixed Browser & Frontend
        """)
        print("="*60 + "\n")
        
    async def ensure_ollama_ready(self):
        """Ensure Ollama is installed and ready""" 
        logger.info("🔍 Checking Ollama...")
        
        if not await OllamaInstaller.install():
            raise RuntimeError("Failed to install Ollama")
            
        logger.info("🚀 Starting Ollama service...")
        try:
            async with httpx.AsyncClient() as client:
                try:
                    response = await client.get('http://localhost:11434/api/tags', timeout=2.0)
                    if response.status_code == 200:
                        logger.info("✅ Ollama service already running")
                        return
                except:
                    pass
            
            if IS_WINDOWS:
                subprocess.Popen(['ollama', 'serve'], 
                               creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(['ollama', 'serve'], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
            
            logger.info("⏳ Waiting for Ollama service...")
            await asyncio.sleep(3)
            
        except Exception as e:
            logger.error(f"Failed to start Ollama service: {e}")
            raise
            
    async def start_educational_router(self):
        """Start the educational router"""
        global router
        
        model, reason = get_recommended_model()
        logger.info(reason)
        
        router = SIRAJEducationalRouter(model)
        
        logger.info(f"🎭 Starting Educational Council Router on port {ROUTER_PORT}...")
        await router.start_instances()
        
        config = uvicorn.Config(
            router_app,
            host="0.0.0.0",
            port=ROUTER_PORT,
            log_level="error"
        )
        
        self.router_server = uvicorn.Server(config)
        asyncio.create_task(self.router_server.serve())
        
        await self._wait_for_service(f"http://localhost:{ROUTER_PORT}/api/health", "Educational Router")
        
    async def _wait_for_service(self, url: str, name: str, timeout: int = 30):
        """Wait for service to be ready"""
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
        
    def start_frontend(self):
        """Start the frontend with better error handling"""
        logger.info("🎨 Starting SIRAJ frontend...")
        
        # Check for built frontend first
        frontend_build = self.base_path / 'frontend' / 'build'
        
        if frontend_build.exists():
            logger.info(f"📦 Found built frontend at {frontend_build}")
            
            # Start HTTP server for static files
            import http.server
            import socketserver
            
            os.chdir(str(frontend_build))
            
            class CustomHandler(http.server.SimpleHTTPRequestHandler):
                def end_headers(self):
                    self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
                    self.send_header('Pragma', 'no-cache')
                    self.send_header('Expires', '0')
                    super().end_headers()
                    
                def log_message(self, format, *args):
                    # Suppress default server logs
                    pass
            
            def serve_frontend():
                try:
                    with socketserver.TCPServer(("", FRONTEND_PORT), CustomHandler) as httpd:
                        logger.info(f"📱 Frontend serving at http://localhost:{FRONTEND_PORT}")
                        httpd.serve_forever()
                except Exception as e:
                    logger.error(f"Frontend server error: {e}")
                    
            threading.Thread(target=serve_frontend, daemon=True).start()
            
            # Wait for frontend to be ready
            self._wait_for_frontend()
            
        else:
            logger.warning(f"Built frontend not found at {frontend_build}")
            # Try development mode
            frontend_dir = self.base_path / 'frontend'
            if frontend_dir.exists():
                logger.info("🔧 Starting frontend in development mode...")
                if IS_WINDOWS:
                    cmd = ['npm.cmd', 'start']
                else:
                    cmd = ['npm', 'start']
                    
                try:
                    self.frontend_process = subprocess.Popen(
                        cmd,
                        cwd=str(frontend_dir),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # Wait for dev server
                    time.sleep(10)
                    logger.info("📱 Frontend development server should be running")
                    
                except Exception as e:
                    logger.error(f"Failed to start frontend development server: {e}")
            else:
                logger.error("❌ No frontend found! Creating simple HTML fallback...")
                self._create_simple_frontend()
                
    def _wait_for_frontend(self):
        """Wait for frontend to be ready"""
        logger.info("⏳ Waiting for frontend to be ready...")
        
        for i in range(30):  # Try for 30 seconds
            try:
                import urllib.request
                with urllib.request.urlopen(f'http://localhost:{FRONTEND_PORT}', timeout=2) as response:
                    if response.status == 200:
                        logger.info("✅ Frontend is ready")
                        return
            except:
                time.sleep(1)
                
        logger.warning("⚠️ Frontend may not be fully ready, but continuing...")
        
    def _create_simple_frontend(self):
        """Create a simple HTML frontend as fallback"""
        logger.info("📝 Creating simple HTML frontend...")
        
        simple_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRAJ Educational AI Council</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }
        h1 { text-align: center; font-size: 2.5em; margin-bottom: 10px; }
        .subtitle { text-align: center; opacity: 0.8; margin-bottom: 30px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, textarea, select { 
            width: 100%; 
            padding: 10px; 
            border: none; 
            border-radius: 5px; 
            margin-bottom: 10px;
            font-size: 16px;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 18px;
            width: 100%;
        }
        button:hover { background: #45a049; }
        .response {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
        }
        .archetype {
            margin: 15px 0;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
        }
        .loading {
            text-align: center;
            font-style: italic;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎭 SIRAJ Educational AI</h1>
        <p class="subtitle">Multi-Archetype Educational Council</p>
        
        <div class="form-group">
            <label>What would you like to learn about?</label>
            <textarea id="question" placeholder="Enter your educational question..." rows="3"></textarea>
        </div>
        
        <div class="form-group">
            <label>Grade Level:</label>
            <select id="gradeLevel">
                <option value="elementary">Elementary (K-5)</option>
                <option value="middle" selected>Middle School (6-8)</option>
                <option value="high">High School (9-12)</option>
                <option value="university">University</option>
            </select>
        </div>
        
        <button onclick="askCouncil()">Ask the Educational Council</button>
        
        <div id="response" class="response">
            <div id="loading" class="loading">🤔 The council is deliberating...</div>
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
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const data = await response.json();
                
                loadingDiv.style.display = 'none';
                
                let html = `<h3>📚 Topic: ${data.topic}</h3>`;
                
                // Show archetype responses
                for (const [archetype, response] of Object.entries(data.council_responses)) {
                    if (response.success) {
                        const archetypeInfo = {
                            socratic: { emoji: '🦉', name: 'Socratic Teacher' },
                            constructivist: { emoji: '🧱', name: 'Constructivist Teacher' },
                            synthesizer: { emoji: '🌀', name: 'Synthesizer Teacher' },
                            mentor: { emoji: '🌱', name: 'Mentor Teacher' }
                        };
                        
                        const info = archetypeInfo[archetype] || { emoji: '🎓', name: archetype };
                        
                        html += `
                            <div class="archetype">
                                <h4>${info.emoji} ${info.name}</h4>
                                <p>${response.response}</p>
                                <small>Instance: ${response.instance}</small>
                            </div>
                        `;
                    }
                }
                
                // Show synthesis
                if (data.synthesis) {
                    html += `
                        <div class="archetype">
                            <h4>✨ Council Synthesis</h4>
                            <p>${data.synthesis}</p>
                        </div>
                    `;
                }
                
                resultsDiv.innerHTML = html;
                
            } catch (error) {
                loadingDiv.style.display = 'none';
                resultsDiv.innerHTML = `
                    <div class="archetype">
                        <h4>❌ Error</h4>
                        <p>Failed to get council response: ${error.message}</p>
                        <p><strong>Make sure the Educational Router is running on port 5000</strong></p>
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
    </script>
</body>
</html>"""
        
        # Create simple frontend directory and file
        simple_dir = self.base_path / 'simple_frontend'
        simple_dir.mkdir(exist_ok=True)
        
        with open(simple_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(simple_html)
            
        # Start simple server
        import http.server
        import socketserver
        
        os.chdir(str(simple_dir))
        
        def serve_simple():
            try:
                with socketserver.TCPServer(("", FRONTEND_PORT), http.server.SimpleHTTPRequestHandler) as httpd:
                    logger.info(f"📱 Simple frontend serving at http://localhost:{FRONTEND_PORT}")
                    httpd.serve_forever()
            except Exception as e:
                logger.error(f"Simple frontend server error: {e}")
                
        threading.Thread(target=serve_simple, daemon=True).start()
        time.sleep(2)  # Give server time to start
            
    def open_browser_when_ready(self):
        """Open browser only when all services are confirmed ready"""
        def browser_opener():
            logger.info("🕐 Waiting for all services to be ready before opening browser...")
            
            # Wait for router to be ready
            router_ready = False
            for i in range(60):  # Wait up to 60 seconds
                try:
                    import urllib.request
                    with urllib.request.urlopen(f'http://localhost:{ROUTER_PORT}/api/health', timeout=2) as response:
                        if response.status == 200:
                            router_ready = True
                            break
                except:
                    time.sleep(1)
            
            # Wait for frontend to be ready
            frontend_ready = False
            for i in range(30):  # Wait up to 30 seconds
                try:
                    import urllib.request
                    with urllib.request.urlopen(f'http://localhost:{FRONTEND_PORT}', timeout=2) as response:
                        if response.status == 200:
                            frontend_ready = True
                            break
                except:
                    time.sleep(1)
            
            if router_ready and frontend_ready:
                url = f"http://localhost:{FRONTEND_PORT}"
                logger.info(f"🌐 All services ready! Opening browser to {url}")
                
                try:
                    webbrowser.open(url)
                    logger.info("✅ Browser opened successfully")
                except Exception as e:
                    logger.error(f"Failed to open browser: {e}")
                    logger.info(f"Please manually open your browser to: {url}")
            else:
                logger.warning("⚠️ Not all services ready, but you can try manually opening:")
                logger.info(f"Frontend: http://localhost:{FRONTEND_PORT}")
                logger.info(f"Router API: http://localhost:{ROUTER_PORT}/api/status")
                
                # Try to open anyway
                try:
                    webbrowser.open(f"http://localhost:{FRONTEND_PORT}")
                except:
                    pass
                    
        # Start browser opener in background thread
        threading.Thread(target=browser_opener, daemon=True).start()
            
    async def run(self):
        """Main run method with improved sequencing"""
        try:
            self.show_splash()
            
            logger.info("📋 Running pre-flight checks...")
            await self.ensure_ollama_ready()
            
            logger.info("🎭 Starting Educational Council Router...")
            await self.start_educational_router()
            
            logger.info("🎨 Starting Frontend Service...")
            self.start_frontend()
            
            logger.info("🌐 Preparing to open browser...")
            self.open_browser_when_ready()
            
            if router and router.degraded_mode:
                logger.warning("⚠️  SYSTEM RUNNING IN DEGRADED MODE")
            
            print("\n" + "="*60)
            logger.info("✨ SIRAJ Educational AI Council Ready!")
            print("="*60)
            print(f"\n🎓 Educational Dashboard: http://localhost:{FRONTEND_PORT}")
            print(f"🎭 Council API: http://localhost:{ROUTER_PORT}/api/status")
            
            if router:
                active_archetypes = []
                for instance in router.instances.values():
                    if instance.healthy:
                        active_archetypes.extend(instance.assigned_archetypes)
                print(f"👥 Active Archetypes: {', '.join(active_archetypes)}")
            
            if router and router.degraded_mode:
                print("\n⚠️  DEGRADED MODE - Some archetypes may be limited")
            
            print("\n🌐 Browser should open automatically when all services are ready")
            print("If not, manually open: http://localhost:3000")
            print("\nPress Ctrl+C to stop\n")
            
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
        
        if router:
            router.stop_all()
        
        if self.frontend_process:
            self.frontend_process.terminate()
            
        logger.info("👋 SIRAJ Educational AI shutdown complete")

def main():
    """Main entry point"""
    launcher = SIRAJFixedLauncher()
    asyncio.run(launcher.run())

if __name__ == '__main__':
    main()
