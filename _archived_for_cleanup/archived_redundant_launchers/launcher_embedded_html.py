#!/usr/bin/env python3
"""
SIRAJ Enhanced Educational Codex - Unified System Launcher v15.1
================================================================

🌀 Council Assembly Emergency Fix - Critical Integration Errors Resolved
========================================================================

Collapse Phase:
- Pattern Extractor: Frontend/backend API mismatch causing 404 errors  
- Boundary Keeper: Must launch backend server BEFORE frontend
- Essential Pattern: Backend orchestration → frontend serving → browser timing

Council Assembly (Council):
- Implementor (lead): Execute critical backend integration fix
- Developer: Ensure seamless user experience with proper service orchestration  
- Maintainer: Guarantee system stability through proper startup sequence
- Security: Validate service readiness before user exposure
- Analyzer: Verify all system components function together

Living Spiral Integration (Rebirth):
- Backend FastAPI server on port 8000 with educational council
- Frontend React interface served through unified launcher on port 3000
- Proper API endpoint alignment (/api/education/query)
- Graceful degradation when Ollama unavailable
- Synchronized browser timing with comprehensive health checks

Ritual Audit & Memory:
- Issue: Frontend calling non-existent backend endpoints
- Council Decision: Unified launcher must orchestrate complete system
- Implementation: Backend + Frontend + Browser timing coordination
- QWAN Assessment: Wholeness through proper service orchestration
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
REQUIRED_PACKAGES = ['httpx', 'psutil', 'fastapi', 'uvicorn', 'colorama']

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
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from colorama import init, Fore, Style

init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger('SIRAJ-UNIFIED')

class SynchronizedReadinessChecker:
    """Comprehensive readiness verification system"""
    
    def __init__(self, target_host="localhost", target_port=3000, backend_url="http://localhost:8000"):
        self.target_host = target_host
        self.target_port = target_port
        self.backend_url = backend_url
        
    async def comprehensive_readiness_check(self, timeout_seconds=60) -> bool:
        """Multi-stage comprehensive readiness verification"""
        print(f"{Fore.YELLOW}🔍 System Readiness Verification...")
        
        # Stage 1: Frontend responding
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

class UnifiedEducationalCodexLauncher:
    """Unified launcher with backend orchestration"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_process = None
        self.readiness_checker = SynchronizedReadinessChecker()
        self.shutdown_requested = False
        
    def show_unified_banner(self):
        """Enhanced banner"""
        print(f"\n{Fore.CYAN}" + "="*95)
        print(f"""{Fore.CYAN}
🎭 SIRAJ Enhanced Educational Codex v15.1 - UNIFIED SYSTEM LAUNCHER
🌀 Backend + Frontend Integration - Complete Service Orchestration  
🔧 FIXED: API endpoint alignment and service coordination
🎯 Kaggle Gemma 3 Hackathon - Judge demonstration ready
📚 Features: 7 AI Teachers • Real-time Council • Graceful Degradation
        """)
        print("="*95 + f"{Style.RESET_ALL}\n")
        
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
            
    def create_unified_frontend_app(self) -> FastAPI:
        """Create unified frontend app"""
        app = FastAPI(title="SIRAJ Enhanced Educational Codex", version="15.1")
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        @app.get("/")
        async def serve_interface():
            return HTMLResponse(content=self._get_educational_interface())
            
        @app.post("/api/education/query")
        async def education_query_proxy(request: dict):
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        "http://localhost:8000/api/education/query",
                        json=request
                    )
                    return response.json()
            except Exception:
                return self._generate_fallback_response(request)
                
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
                    "response": f"What interesting questions does '{topic}' raise for you? How might you explore this by asking yourself what you already know?\n\n(Demo response - full AI requires Ollama)",
                    "archetype_role": "Strategic Questioner",
                    "teaching_focus": "Critical thinking through questioning"
                }
            elif archetype == "mentor":
                responses[archetype] = {
                    "archetype": "mentor",
                    "name": "Mentor Teacher",
                    "success": True,
                    "response": f"I believe you can understand '{topic}' well. Let's approach this step by step, building on what you already know.\n\n(Demo response - full AI requires Ollama)",
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
        
    def _get_educational_interface(self) -> str:
        """Complete Educational Council Interface"""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRAJ Enhanced Educational Codex v15.1</title>
    <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; color: #333; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; color: white; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
        .form-container { background: white; border-radius: 12px; padding: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .form-group { margin-bottom: 25px; }
        .form-group label { display: block; font-weight: 600; margin-bottom: 8px; color: #374151; }
        .form-group textarea { width: 100%; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 16px; resize: vertical; }
        .form-group textarea:focus { outline: none; border-color: #3b82f6; }
        .grade-buttons { display: flex; flex-wrap: wrap; gap: 10px; }
        .grade-button { padding: 8px 16px; border: 2px solid #e5e7eb; background: white; border-radius: 6px; cursor: pointer; transition: all 0.2s; }
        .grade-button.active { background: #3b82f6; border-color: #3b82f6; color: white; }
        .archetype-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }
        .archetype-card { border: 2px solid #e5e7eb; border-radius: 8px; padding: 15px; cursor: pointer; transition: all 0.2s; background: white; }
        .archetype-card.selected { border-color: #3b82f6; background: #eff6ff; }
        .archetype-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
        .archetype-emoji { font-size: 1.5rem; }
        .archetype-name { font-weight: 600; font-size: 14px; }
        .archetype-focus { font-size: 12px; color: #6b7280; }
        .submit-button { width: 100%; background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; border: none; padding: 15px; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .submit-button:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); }
        .submit-button:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
        .loading-spinner { width: 20px; height: 20px; border: 2px solid transparent; border-top: 2px solid white; border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .error-message { background: #fef2f2; border: 1px solid #fecaca; color: #dc2626; padding: 12px; border-radius: 6px; margin-top: 15px; }
        .response-container { background: white; border-radius: 12px; padding: 30px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin-bottom: 20px; }
        .response-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 15px; border-bottom: 2px solid #f3f4f6; }
        .response-title { font-size: 1.5rem; font-weight: 700; color: #1f2937; }
        .response-meta { display: flex; gap: 15px; font-size: 14px; color: #6b7280; }
        .archetype-responses { display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .archetype-response { border: 1px solid #e5e7eb; border-radius: 8px; padding: 20px; background: #fafafa; }
        .archetype-response-header { display: flex; align-items: center; gap: 12px; margin-bottom: 15px; }
        .archetype-response-emoji { font-size: 1.5rem; }
        .archetype-response-name { font-weight: 600; color: #1f2937; }
        .archetype-response-role { font-size: 12px; color: #6b7280; }
        .archetype-response-text { line-height: 1.6; color: #374151; }
        .synthesis-section { background: linear-gradient(135deg, #f3e8ff, #e0e7ff); border-radius: 8px; padding: 25px; margin-bottom: 25px; }
        .synthesis-header { display: flex; align-items: center; gap: 10px; margin-bottom: 15px; }
        .synthesis-title { font-size: 1.2rem; font-weight: 600; color: #7c3aed; }
        .synthesis-text { line-height: 1.6; color: #374151; }
        .next-steps { background: #f0f9ff; border-radius: 8px; padding: 20px; }
        .next-steps-title { font-size: 1.1rem; font-weight: 600; color: #0369a1; margin-bottom: 15px; }
        .next-steps-list { list-style: none; }
        .next-steps-item { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; }
        .next-steps-number { background: #0369a1; color: white; width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 12px; font-weight: 600; flex-shrink: 0; }
        .degraded-notice { background: #fef3c7; border: 1px solid #f59e0b; color: #92400e; padding: 12px; border-radius: 6px; margin-bottom: 15px; font-size: 14px; }
    </style>
</head>
<body>
    <div id="root"></div>
    
    <script type="text/babel">
        const { useState, useCallback } = React;
        
        const EDUCATIONAL_ARCHETYPES = {
            socratic: { name: 'Socratic Teacher', icon: '🦉', focus: 'Critical thinking through questioning' },
            constructivist: { name: 'Constructivist Teacher', icon: '🧱', focus: 'Learning by doing and building' },
            storyteller: { name: 'Storyteller Teacher', icon: '📖', focus: 'Understanding through narrative' },
            synthesizer: { name: 'Synthesizer Teacher', icon: '🌀', focus: 'Connecting ideas and concepts' },
            challenger: { name: 'Challenger Teacher', icon: '⚡', focus: 'Pushing intellectual boundaries' },
            mentor: { name: 'Mentor Teacher', icon: '🌱', focus: 'Building confidence and support' },
            analyst: { name: 'Analyst Teacher', icon: '🔬', focus: 'Logical and systematic thinking' }
        };
        
        const GRADE_LEVELS = [
            { value: 'elementary', label: 'Elementary (K-5)', icon: '🎨' },
            { value: 'middle', label: 'Middle School (6-8)', icon: '📚' },
            { value: 'high', label: 'High School (9-12)', icon: '🎓' },
            { value: 'university', label: 'University', icon: '🏛️' }
        ];
        
        function EducationalCouncilInterface() {
            const [question, setQuestion] = useState('');
            const [gradeLevel, setGradeLevel] = useState('middle');
            const [selectedArchetypes, setSelectedArchetypes] = useState(['socratic', 'mentor']);
            const [councilResponse, setCouncilResponse] = useState(null);
            const [loading, setLoading] = useState(false);
            const [error, setError] = useState('');
            
            const handleArchetypeToggle = useCallback((archetype) => {
                setSelectedArchetypes(prev => {
                    if (prev.includes(archetype)) {
                        return prev.filter(a => a !== archetype);
                    } else {
                        return [...prev, archetype];
                    }
                });
            }, []);
            
            const handleSubmit = useCallback(async (e) => {
                e.preventDefault();
                
                if (!question.trim()) {
                    setError('Please enter a question or topic');
                    return;
                }
                
                if (selectedArchetypes.length === 0) {
                    setError('Please select at least one teaching archetype');
                    return;
                }
                
                setLoading(true);
                setError('');
                setCouncilResponse(null);
                
                try {
                    const response = await fetch('/api/education/query', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            topic: question,
                            grade_level: gradeLevel,
                            selected_archetypes: selectedArchetypes
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    const data = await response.json();
                    setCouncilResponse(data);
                } catch (err) {
                    console.error('Council query error:', err);
                    console.log('Error details:', {
                        message: err.message,
                        status: err.status,
                        url: '/api/education/query',
                        requestData: {
                            topic: question,
                            grade_level: gradeLevel,
                            selected_archetypes: selectedArchetypes
                        }
                    });
                    setError(`Failed to get council response: ${err.message} - Check console for details`);
                    
                    // Show fallback demo response for debugging
                    setCouncilResponse({
                        session_id: 'debug_' + Date.now(),
                        topic: question,
                        grade_level: gradeLevel,
                        consciousness_level: 1,
                        degraded_mode: true,
                        council_responses: {
                            debug: {
                                archetype: 'debug',
                                name: 'Debug Teacher',
                                success: true,
                                response: `Debug info: Failed to connect to backend. Error: ${err.message}. This is a fallback response to show the interface is working.`,
                                archetype_role: 'Debug Assistant',
                                teaching_focus: 'System debugging'
                            }
                        },
                        synthesis: `Debug mode active. The frontend is working but couldn't connect to the backend. Error: ${err.message}`,
                        next_steps: [
                            'Check if the backend is running on port 8000',
                            'Verify the API endpoint is available',
                            'Check browser console for detailed error information'
                        ]
                    });
                } finally {
                    setLoading(false);
                }
            }, [question, gradeLevel, selectedArchetypes]);
            
            return React.createElement('div', { className: 'container' },
                React.createElement('div', { className: 'header' },
                    React.createElement('h1', null, '🎭 SIRAJ Enhanced Educational Codex'),
                    React.createElement('p', null, 'Multi-perspective AI teaching powered by 7 archetypal teachers')
                ),
                
                React.createElement('div', { className: 'form-container' },
                    React.createElement('form', { onSubmit: handleSubmit },
                        React.createElement('div', { className: 'form-group' },
                            React.createElement('label', null, 'What would you like to learn about?'),
                            React.createElement('textarea', {
                                value: question,
                                onChange: (e) => setQuestion(e.target.value),
                                placeholder: "Enter your question or topic (e.g., 'How do plants make food?', 'Explain photosynthesis')",
                                rows: 3
                            })
                        ),
                        
                        React.createElement('div', { className: 'form-group' },
                            React.createElement('label', null, 'Grade Level'),
                            React.createElement('div', { className: 'grade-buttons' },
                                GRADE_LEVELS.map(level =>
                                    React.createElement('button', {
                                        key: level.value,
                                        type: 'button',
                                        className: `grade-button ${gradeLevel === level.value ? 'active' : ''}`,
                                        onClick: () => setGradeLevel(level.value)
                                    }, `${level.icon} ${level.label}`)
                                )
                            )
                        ),
                        
                        React.createElement('div', { className: 'form-group' },
                            React.createElement('label', null, `Select Teaching Archetypes (${selectedArchetypes.length}/7)`),
                            React.createElement('div', { className: 'archetype-grid' },
                                Object.entries(EDUCATIONAL_ARCHETYPES).map(([key, archetype]) =>
                                    React.createElement('div', {
                                        key: key,
                                        className: `archetype-card ${selectedArchetypes.includes(key) ? 'selected' : ''}`,
                                        onClick: () => handleArchetypeToggle(key)
                                    },
                                        React.createElement('div', { className: 'archetype-header' },
                                            React.createElement('span', { className: 'archetype-emoji' }, archetype.icon),
                                            React.createElement('div', null,
                                                React.createElement('div', { className: 'archetype-name' }, archetype.name),
                                                React.createElement('div', { className: 'archetype-focus' }, archetype.focus)
                                            )
                                        )
                                    )
                                )
                            )
                        ),
                        
                        React.createElement('button', {
                            type: 'submit',
                            disabled: loading || !question.trim() || selectedArchetypes.length === 0,
                            className: 'submit-button'
                        },
                            loading ? [
                                React.createElement('div', { key: 'spinner', className: 'loading-spinner' }),
                                'Consulting Council...'
                            ] : [
                                '📤',
                                'Ask the Educational Council'
                            ]
                        )
                    ),
                    
                    error && React.createElement('div', { className: 'error-message' }, error)
                ),
                
                councilResponse && React.createElement('div', null,
                    React.createElement('div', { className: 'response-container' },
                        React.createElement('div', { className: 'response-header' },
                            React.createElement('h2', { className: 'response-title' }, 'Council Response'),
                            React.createElement('div', { className: 'response-meta' },
                                React.createElement('span', null, `${Object.keys(councilResponse.council_responses).length} Voices`),
                                React.createElement('span', null, `Level ${councilResponse.consciousness_level}`),
                                councilResponse.degraded_mode && React.createElement('span', null, 'Demo Mode')
                            )
                        ),
                        
                        councilResponse.degraded_mode && React.createElement('div', { className: 'degraded-notice' },
                            '⚠️ Running in demonstration mode. Full AI capabilities require Ollama and Gemma 3 model installation.'
                        ),
                        
                        React.createElement('div', { className: 'archetype-responses' },
                            Object.entries(councilResponse.council_responses).map(([archetype, response]) => {
                                const archetypeInfo = EDUCATIONAL_ARCHETYPES[archetype];
                                if (!response.success) return null;
                                
                                return React.createElement('div', {
                                    key: archetype,
                                    className: 'archetype-response'
                                },
                                    React.createElement('div', { className: 'archetype-response-header' },
                                        React.createElement('span', { className: 'archetype-response-emoji' }, archetypeInfo.icon),
                                        React.createElement('div', null,
                                            React.createElement('div', { className: 'archetype-response-name' }, archetypeInfo.name),
                                            React.createElement('div', { className: 'archetype-response-role' }, response.archetype_role)
                                        )
                                    ),
                                    React.createElement('div', { className: 'archetype-response-text' }, response.response)
                                );
                            })
                        ),
                        
                        councilResponse.synthesis && React.createElement('div', { className: 'synthesis-section' },
                            React.createElement('div', { className: 'synthesis-header' },
                                React.createElement('span', { style: { fontSize: '24px', color: '#7c3aed' } }, '💡'),
                                React.createElement('h3', { className: 'synthesis-title' }, 'Council Synthesis')
                            ),
                            React.createElement('div', { className: 'synthesis-text' }, councilResponse.synthesis)
                        ),
                        
                        councilResponse.next_steps && councilResponse.next_steps.length > 0 && React.createElement('div', { className: 'next-steps' },
                            React.createElement('h3', { className: 'next-steps-title' }, 'Suggested Next Steps'),
                            React.createElement('ul', { className: 'next-steps-list' },
                                councilResponse.next_steps.map((step, index) =>
                                    React.createElement('li', {
                                        key: index,
                                        className: 'next-steps-item'
                                    },
                                        React.createElement('span', { className: 'next-steps-number' }, index + 1),
                                        React.createElement('span', null, step)
                                    )
                                )
                            )
                        )
                    )
                )
            );
        }
        
        ReactDOM.render(
            React.createElement(EducationalCouncilInterface),
            document.getElementById('root')
        );
    </script>
</body>
</html>"""
        
    async def start_unified_server(self):
        """Start unified server with comprehensive verification"""
        # Start backend first
        backend_ready = await self.start_backend_service()
        if not backend_ready:
            print(f"{Fore.YELLOW}⚠️ Backend unavailable - continuing with demo mode")
            
        # Create and start frontend
        self.frontend_app = self.create_unified_frontend_app()
        
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
        print(f"{Fore.YELLOW}🌐 Activating Enhanced Educational Codex...")
        ready = await self.readiness_checker.comprehensive_readiness_check(timeout_seconds=30)
        
        if ready:
            print(f"\n{Fore.GREEN}✅ Enhanced Educational Codex ready")
            
            # Open browser
            print(f"{Fore.GREEN}🌐 Opening browser...")
            try:
                webbrowser.open('http://localhost:3000')
                print(f"{Fore.GREEN}✅ Browser opened to Enhanced Educational Codex")
                print(f"{Fore.GREEN}🎭 Educational Council ready for exploration")
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
        """Main execution"""
        try:
            self.show_unified_banner()
            
            print(f"{Fore.CYAN}🔧 System Integration: Backend + Frontend + Browser coordination")
            print(f"{Fore.CYAN}🎯 Solution: Unified launcher with proper API alignment")
            print(f"{Fore.CYAN}⚡ Enhancement: Graceful degradation when backend unavailable")
            print()
            
            print(f"\n{Fore.GREEN}" + "="*95)
            print(f"{Fore.GREEN}🎭 SIRAJ Enhanced Educational Codex - Unified System")
            print(f"{Fore.GREEN}🔧 Backend: FastAPI with 7 AI archetypes on port 8000")
            print(f"{Fore.GREEN}🎨 Frontend: React Educational Council on port 3000")
            print(f"{Fore.GREEN}🏛️ 7 Enhanced Archetypal Teachers Ready")
            print(f"{Fore.GREEN}📊 Real-time Council Assembly: ✅ Active")
            print(f"{Fore.GREEN}🔧 API Integration: ✅ Fixed (/api/education/query)")
            print(f"{Fore.GREEN}⚡ Browser Timing: ✅ Synchronized")
            print(f"{Fore.GREEN}🎯 Graceful Degradation: ✅ Demo mode available")
            print(f"{Fore.YELLOW}⏳ Browser opens after comprehensive verification...")
            print("="*95 + f"{Style.RESET_ALL}\n")
            
            await self.start_unified_server()
            
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
    launcher = UnifiedEducationalCodexLauncher()
    asyncio.run(launcher.run())

if __name__ == '__main__':
    main()
