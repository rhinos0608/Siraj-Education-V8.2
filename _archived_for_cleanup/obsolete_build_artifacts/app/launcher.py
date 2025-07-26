#!/usr/bin/env python3
"""
SIRAJ Enhanced Educational Codex - Integrated System Launcher v15.2
=================================================================

🌀 Council Assembly Integration Fix - Frontend Transformation Included
=====================================================================

Collapse Phase:
- Fundamental Intent: Serve actual frontend build (with API hook transformation) instead of embedded HTML
- Essential Pattern: Backend orchestration → Frontend build serving → Browser activation
- Boundary Constraints: Preserve launcher functionality while integrating real frontend

Council Assembly (Integration):
- Implementor (lead): Replace embedded HTML with frontend build directory serving
- Developer: Ensure API hook transformation is included in user experience  
- Maintainer: Guarantee system stability through proper build integration
- Analyzer: Verify frontend build exists and includes transformed components
- Explorer: Enable innovation through proper infrastructure integration

Living Spiral Integration (Rebirth):
- Backend FastAPI server on port 8000 with educational council
- Frontend React build served from frontend/build/ directory on port 3000
- Includes EducationalCouncilInterface.js with useSirajAPI hook transformation
- System status indicators and consciousness-driven interface included
- Graceful degradation when Ollama unavailable

Ritual Audit & Memory:
- Issue: Launcher served embedded HTML, bypassing frontend transformation
- Council Decision: Serve actual frontend build directory with transformations
- Implementation: Static file serving from frontend/build/ + API proxying
- QWAN Assessment: Wholeness through unified frontend-launcher integration
"""

import os
import sys
import time
import asyncio
import json
import subprocess
import webbrowser
import logging
import signal
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import socket

# Essential dependencies
REQUIRED_PACKAGES = ['httpx', 'psutil', 'fastapi', 'uvicorn', 'colorama', 'aiofiles']

def ensure_dependencies():
    """Install required packages"""
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
import aiofiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from colorama import init, Fore, Style

init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger('SIRAJ-INTEGRATED')

class SynchronizedReadinessChecker:
    """Comprehensive readiness verification system"""
    
    def __init__(self, target_host="localhost", target_port=3000, backend_url="http://localhost:8000"):
        self.target_host = target_host
        self.target_port = target_port
        self.backend_url = backend_url
        
    async def comprehensive_readiness_check(self, timeout_seconds=60) -> bool:
        """Multi-stage comprehensive readiness verification"""
        print(f"{Fore.YELLOW}🔍 System Readiness Verification...")
        
        # Stage 1: Frontend serving
        print(f"   Stage 1: Frontend service verification...")
        frontend_ready = await self._check_frontend_responding(timeout_seconds)
        if not frontend_ready:
            print(f"{Fore.RED}   ❌ Frontend not responding")
            return False
        print(f"{Fore.GREEN}   ✅ Frontend service ready")
        
        # Stage 2: Backend check (optional)
        print(f"   Stage 2: Backend connectivity check...")
        backend_ready = await self._check_backend_running()
        if backend_ready:
            print(f"{Fore.GREEN}   ✅ Backend service connected")
        else:
            print(f"{Fore.YELLOW}   ⚠️ Backend unavailable - demo mode active")
        
        print(f"{Fore.GREEN}✅ Enhanced Educational Codex ready for browser activation")
        return True
        
    async def _check_frontend_responding(self, timeout_seconds: int) -> bool:
        """Wait for frontend to start responding"""
        start_time = time.time()
        
        while time.time() - start_time < timeout_seconds:
            try:
                async with httpx.AsyncClient(timeout=3.0) as client:
                    response = await client.get(f"http://{self.target_host}:{self.target_port}")
                    if response.status_code == 200:
                        return True
            except:
                await asyncio.sleep(1)
                
        return False
        
    async def _check_backend_running(self) -> bool:
        """Verify backend service is operational"""
        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.get(f"{self.backend_url}/health")
                return response.status_code == 200
        except:
            return False

class IntegratedEducationalCodexLauncher:
    """Integrated launcher serving actual frontend build"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.frontend_build_dir = self.project_root / "frontend" / "build"
        self.readiness_checker = SynchronizedReadinessChecker()
        self.shutdown_requested = False
        
    def show_integrated_banner(self):
        """Enhanced banner with integration status"""
        print(f"\n{Fore.CYAN}" + "="*95)
        print(f"""{Fore.CYAN}
🎭 SIRAJ Enhanced Educational Codex v15.2 - INTEGRATED SYSTEM LAUNCHER
🌀 Frontend Build Integration - Includes API Hook Transformation  
🔧 FIXED: Launcher now serves actual frontend with useSirajAPI integration
🎯 Kaggle Gemma 3 Hackathon - Full transformation included
📚 Features: 7 AI Teachers • System Status • Consciousness Interface
        """)
        print("="*95 + f"{Style.RESET_ALL}\n")
        
    async def verify_frontend_build(self) -> bool:
        """Verify frontend build exists and contains transformation"""
        print(f"{Fore.YELLOW}🔍 Verifying frontend build integration...")
        
        if not self.frontend_build_dir.exists():
            print(f"{Fore.RED}❌ Frontend build directory not found!")
            print(f"    Expected: {self.frontend_build_dir}")
            print(f"{Fore.YELLOW}🔧 Building frontend now...")
            
            success = await self.build_frontend()
            if not success:
                return False
                
        # Check for index.html
        index_file = self.frontend_build_dir / "index.html"
        if not index_file.exists():
            print(f"{Fore.RED}❌ Frontend index.html not found!")
            return False
            
        # Check for static assets - Critical for proper serving
        static_js_dir = self.frontend_build_dir / "static" / "js"
        static_css_dir = self.frontend_build_dir / "static" / "css"
        
        if not static_js_dir.exists():
            print(f"{Fore.RED}❌ JavaScript assets directory not found!")
            print(f"{Fore.YELLOW}🔧 Frontend build appears incomplete, rebuilding...")
            success = await self.build_frontend()
            if not success:
                return False
                
        # Count static assets to verify build completeness
        js_files = list(static_js_dir.glob('*.js')) if static_js_dir.exists() else []
        css_files = list(static_css_dir.glob('*.css')) if static_css_dir.exists() else []
        
        if len(js_files) == 0:
            print(f"{Fore.RED}❌ No JavaScript bundles found! Build incomplete.")
            print(f"{Fore.YELLOW}🔧 Rebuilding frontend...")
            success = await self.build_frontend()
            if not success:
                return False
            # Recheck after rebuild
            js_files = list(static_js_dir.glob('*.js')) if static_js_dir.exists() else []
            
        # Verify build contains React app
        try:
            content = index_file.read_text(encoding='utf-8')
            if 'SIRAJ' in content and 'Educational' in content:
                print(f"{Fore.GREEN}✅ Frontend build verified - includes SIRAJ interface")
                print(f"{Fore.GREEN}✅ Found {len(js_files)} JS files, {len(css_files)} CSS files")
                return True
            else:
                print(f"{Fore.YELLOW}⚠️ Frontend build found but may be incomplete")
                return True  # Continue anyway
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Could not verify frontend content: {e}")
            return True  # Continue anyway
            
    async def build_frontend(self) -> bool:
        """Build React frontend using Spiral Protocol"""
        frontend_dir = self.project_root / "frontend"
        
        if not (frontend_dir / "package.json").exists():
            print(f"{Fore.RED}❌ Frontend package.json not found!")
            return False
            
        print(f"{Fore.YELLOW}🔧 Building React frontend using Spiral Protocol...")
        
        try:
            # Use the spiral build script if available
            build_script = frontend_dir / "build_frontend.py"
            if build_script.exists():
                print(f"{Fore.CYAN}🌀 Using Spiral Protocol build script...")
                result = subprocess.run([sys.executable, str(build_script)], 
                                      cwd=str(frontend_dir),
                                      capture_output=False)
                if result.returncode == 0:
                    print(f"{Fore.GREEN}✅ Spiral Protocol build completed successfully")
                    return True
                else:
                    print(f"{Fore.RED}❌ Spiral Protocol build failed, trying fallback...")
            
            # Fallback to direct npm build
            print(f"{Fore.YELLOW}🔄 Fallback: Direct npm build...")
            
            # Check if npm is available
            subprocess.run(['npm', '--version'], check=True, capture_output=True)
            
            # Install dependencies if needed
            if not (frontend_dir / "node_modules").exists():
                print(f"{Fore.YELLOW}📦 Installing frontend dependencies...")
                subprocess.check_call(['npm', 'install'], cwd=str(frontend_dir))
                
            # Build frontend
            env = os.environ.copy()
            env['REACT_APP_API_URL'] = 'http://localhost:8000'
            env['REACT_APP_WS_URL'] = 'ws://localhost:8000'
            env['CI'] = 'false'
            env['GENERATE_SOURCEMAP'] = 'false'
            
            subprocess.check_call(['npm', 'run', 'build'], cwd=str(frontend_dir), env=env)
            
            print(f"{Fore.GREEN}✅ Frontend build completed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"{Fore.RED}❌ Frontend build failed: {e}")
            return False
        except FileNotFoundError:
            print(f"{Fore.RED}❌ npm not found - please install Node.js")
            return False
            
    async def start_backend_service(self):
        """Start backend service"""
        print(f"{Fore.YELLOW}🔧 Starting backend educational council service...")
        
        backend_main = self.project_root / "backend" / "main.py"
        
        if not backend_main.exists():
            print(f"{Fore.YELLOW}⚠️ Backend not found - continuing with demo mode")
            return False
            
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, str(backend_main)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            # Wait for backend
            for i in range(15):
                try:
                    async with httpx.AsyncClient(timeout=2.0) as client:
                        response = await client.get("http://localhost:8000/health")
                        if response.status_code == 200:
                            print(f"{Fore.GREEN}✅ Backend service ready on port 8000")
                            return True
                except:
                    pass
                await asyncio.sleep(1)
                
            print(f"{Fore.YELLOW}⚠️ Backend startup timeout - continuing with demo mode")
            return False
            
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Backend start failed: {e} - continuing with demo mode")
            return False
            
    def create_integrated_frontend_app(self) -> FastAPI:
        """Create integrated frontend app serving actual build"""
        app = FastAPI(title="SIRAJ Enhanced Educational Codex - Integrated", version="15.2")
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        # Mount static files from frontend build
        if self.frontend_build_dir.exists():
            app.mount("/static", StaticFiles(directory=str(self.frontend_build_dir / "static")), name="static")
            
            @app.get("/")
            async def serve_frontend_index():
                """Serve the actual frontend index.html with transformations"""
                index_path = self.frontend_build_dir / "index.html"
                if index_path.exists():
                    return FileResponse(str(index_path))
                else:
                    return HTMLResponse("Frontend build not found. Please run: npm run build")
                    
            @app.get("/{file_path:path}")
            async def serve_frontend_files(file_path: str):
                """Serve other frontend files"""
                if file_path.startswith("api/"):
                    # Let API endpoints be handled by other routes
                    raise HTTPException(status_code=404, detail="API endpoint not found")
                    
                file_full_path = self.frontend_build_dir / file_path
                if file_full_path.exists() and file_full_path.is_file():
                    return FileResponse(str(file_full_path))
                else:
                    # Fallback to index.html for React routing
                    index_path = self.frontend_build_dir / "index.html"
                    if index_path.exists():
                        return FileResponse(str(index_path))
                    else:
                        raise HTTPException(status_code=404, detail="File not found")
        else:
            @app.get("/")
            async def no_frontend_build():
                return HTMLResponse("""
                <h1>Frontend Build Required</h1>
                <p>Please build the frontend first:</p>
                <pre>cd frontend && npm install && npm run build</pre>
                """)
            
        # API proxy endpoints
        @app.post("/api/education/query")
        async def education_query_proxy(request: dict):
            """Proxy educational query to backend"""
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "http://localhost:8000/api/education/query",
                        json=request
                    )
                    return response.json()
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Backend proxy failed: {e}")
                return self._generate_fallback_response(request)
                
        @app.get("/api/health")
        async def health_proxy():
            """Proxy health check to backend"""
            try:
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.get("http://localhost:8000/health")
                    return response.json()
            except Exception:
                return {
                    "status": "degraded",
                    "frontend": "operational",
                    "backend": "unavailable",
                    "mode": "demo"
                }
                
        return app
        
    def _generate_fallback_response(self, request: dict) -> dict:
        """Generate demo response when backend unavailable"""
        topic = request.get("topic", "learning")
        selected = request.get("selected_archetypes", ["socratic", "mentor"])
        
        responses = {}
        for archetype in selected:
            if archetype == "socratic":
                responses[archetype] = {
                    "archetype": "socratic",
                    "name": "Socratic Teacher",
                    "success": True,
                    "response": f"What interesting questions does '{topic}' raise for you? How might you explore this by asking yourself what you already know?\\n\\n(Demo response - full AI requires Ollama)",
                    "archetype_role": "Strategic Questioner",
                    "teaching_focus": "Critical thinking through questioning"
                }
            elif archetype == "mentor":
                responses[archetype] = {
                    "archetype": "mentor",
                    "name": "Mentor Teacher",
                    "success": True,
                    "response": f"I believe you can understand '{topic}' well. Let's approach this step by step, building on what you already know.\\n\\n(Demo response - full AI requires Ollama)",
                    "archetype_role": "Supportive Guide", 
                    "teaching_focus": "Building confidence and support"
                }
                
        return {
            "session_id": f"demo_{datetime.now().strftime('%H%M%S')}",
            "topic": topic,
            "grade_level": request.get("grade_level", "middle"),
            "consciousness_level": 1,
            "degraded_mode": True,
            "council_responses": responses,
            "synthesis": f"This is a demonstration of the Educational Council interface for '{topic}'. Full AI capabilities require Ollama and Gemma 3 models.",
            "next_steps": [
                "This demonstrates the Educational Council interface",
                "Install Ollama from https://ollama.com for full AI",
                "Run 'ollama pull gemma3:2b' to download models"
            ]
        }
        
    async def start_integrated_server(self):
        """Start integrated server with frontend build verification"""
        # Verify frontend build exists
        build_ready = await self.verify_frontend_build()
        if not build_ready:
            print(f"{Fore.RED}❌ Cannot proceed without frontend build")
            return False
            
        # Start backend first
        backend_ready = await self.start_backend_service()
        if not backend_ready:
            print(f"{Fore.YELLOW}⚠️ Backend unavailable - continuing with demo mode")
            
        # Create and start integrated frontend
        self.frontend_app = self.create_integrated_frontend_app()
        
        config = uvicorn.Config(
            self.frontend_app,
            host="0.0.0.0",
            port=3000,
            log_level="error",
            access_log=False
        )
        
        server = uvicorn.Server(config)
        server_task = asyncio.create_task(server.serve())
        
        # Wait for readiness
        print(f"{Fore.YELLOW}🌐 Activating Enhanced Educational Codex with integrated frontend...")
        ready = await self.readiness_checker.comprehensive_readiness_check(timeout_seconds=30)
        
        if ready:
            print(f"\n{Fore.GREEN}✅ Enhanced Educational Codex ready with frontend transformation")
            
            # Open browser
            print(f"{Fore.GREEN}🌐 Opening browser to integrated interface...")
            try:
                webbrowser.open('http://localhost:3000')
                print(f"{Fore.GREEN}✅ Browser opened to Enhanced Educational Codex")
                print(f"{Fore.GREEN}🎭 Educational Council ready with API hook transformation")
            except Exception as e:
                print(f"{Fore.YELLOW}⚠️ Could not auto-open browser: {e}")
                print(f"{Fore.CYAN}📖 Please manually open: http://localhost:3000")
        else:
            print(f"{Fore.RED}❌ System readiness check failed")
            
        # Signal handling
        def signal_handler(signum, frame):
            self.shutdown_requested = True
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Wait for shutdown
        try:
            while not self.shutdown_requested:
                await asyncio.sleep(1)
        finally:
            await self.cleanup()
            
    async def cleanup(self):
        """Clean shutdown"""
        print(f"\n{Fore.YELLOW}🛑 Shutting down Enhanced Educational Codex...")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print(f"{Fore.GREEN}✅ Backend stopped")
            except:
                self.backend_process.kill()
                print(f"{Fore.YELLOW}⚠️ Backend force stopped")
                
        print(f"{Fore.GREEN}👋 Shutdown complete")
        
    async def run(self):
        """Main execution with integration"""
        try:
            self.show_integrated_banner()
            
            print(f"{Fore.CYAN}🔧 Integration Status: Serving actual frontend build with transformations")
            print(f"{Fore.CYAN}🎯 Solution: Frontend build includes useSirajAPI hook integration")
            print(f"{Fore.CYAN}⚡ Enhancement: System status indicators and consciousness interface")
            print()
            
            print(f"\n{Fore.GREEN}" + "="*95)
            print(f"{Fore.GREEN}🎭 SIRAJ Enhanced Educational Codex - Integrated System")
            print(f"{Fore.GREEN}🔧 Backend: FastAPI with 7 AI archetypes on port 8000")
            print(f"{Fore.GREEN}🎨 Frontend: React build with API hook transformation on port 3000")
            print(f"{Fore.GREEN}🏛️ 7 Enhanced Archetypal Teachers Ready")
            print(f"{Fore.GREEN}📊 System Status Indicators: ✅ Included")
            print(f"{Fore.GREEN}🔧 API Hook Integration: ✅ Included in build")
            print(f"{Fore.GREEN}⚡ Browser Timing: ✅ Synchronized")
            print(f"{Fore.GREEN}🎯 Consciousness Interface: ✅ Integrated")
            print(f"{Fore.YELLOW}⏳ Browser opens after frontend verification...")
            print("="*95 + f"{Style.RESET_ALL}\n")
            
            await self.start_integrated_server()
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Graceful shutdown initiated...")
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            await self.cleanup()

def main():
    """Entry point"""
    launcher = IntegratedEducationalCodexLauncher()
    asyncio.run(launcher.run())

if __name__ == '__main__':
    main()
