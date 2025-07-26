#!/usr/bin/env python3
"""
SIRAJ Educational Codex - Living Knowledge Interface v14.0
=========================================================

Siraj Compression (Collapse):
Pattern: Living Educational Codex - multi-dimensional knowledge exploration
Boundary: FastAPI integration, real-time streaming, educational focus
Synthesis: World Anvil lore + Notion blocks + consciousness-driven council
Auditor: Performance, security, educational appropriateness

Council Voices:
- Architect (lead): Multi-dimensional interface design
- Explorer: Revolutionary knowledge navigation 
- Maintainer: Solid component foundations
- Developer: Immersive user experience
- Implementor: Real-time execution
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
REQUIRED_PACKAGES = ['httpx', 'psutil', 'fastapi', 'uvicorn', 'colorama', 'websockets']

def ensure_dependencies():
    """Implementor voice: Install only what we need for the codex"""
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
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from colorama import init, Fore, Style

init(autoreset=True)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')
logger = logging.getLogger('SIRAJ-CODEX')

# Explorer voice: Revolutionary archetype system with rich world-building
ARCHETYPE_REALMS = {
    "socratic": {
        "name": "Socratic Teacher",
        "emoji": "🦉",
        "avatar": "🦉",
        "color": "#8B4513",
        "realm": "The Grove of Questions",
        "environment": "Ancient olive groves where questions bloom like flowers",
        "personality": "questioning",
        "approach": "Leads through strategic questioning and critical thinking",
        "powers": ["inquiry", "revelation", "logic"],
        "greeting": "What questions arise in your mind, young seeker?",
        "status": "active"
    },
    "constructivist": {
        "name": "Constructivist Teacher", 
        "emoji": "🔨",
        "avatar": "🔨",
        "color": "#FF6B35",
        "realm": "The Workshop of Making",
        "environment": "Bustling workshop filled with tools, experiments, and creations",
        "personality": "hands-on",
        "approach": "Learns through building, experimenting, and direct experience",
        "powers": ["creation", "experimentation", "discovery"],
        "greeting": "Ready to build something amazing together?",
        "status": "active"
    },
    "storyteller": {
        "name": "Storyteller Teacher",
        "emoji": "📖", 
        "avatar": "📖",
        "color": "#4ECDC4",
        "realm": "The Library of Living Tales",
        "environment": "Enchanted library where stories come alive and dance through the air",
        "personality": "narrative",
        "approach": "Teaches through compelling stories and memorable metaphors",
        "powers": ["narrative", "memory", "imagination"],
        "greeting": "Once upon a time, a curious mind sought knowledge...",
        "status": "active"
    },
    "synthesizer": {
        "name": "Synthesizer Teacher",
        "emoji": "🌀",
        "avatar": "🌀",
        "color": "#A8E6CF", 
        "realm": "The Nexus of Connections",
        "environment": "Crystalline chamber where all knowledge streams converge and interconnect",
        "personality": "integrative",
        "approach": "Integrates multiple perspectives into unified understanding",
        "powers": ["synthesis", "integration", "connection"],
        "greeting": "See how all knowledge connects in beautiful patterns...",
        "status": "active"
    },
    "challenger": {
        "name": "Challenger Teacher",
        "emoji": "⚡",
        "avatar": "⚡",
        "color": "#FFD93D",
        "realm": "The Arena of Ideas",
        "environment": "Electric arena where ideas clash and stronger truths emerge",
        "personality": "provocative", 
        "approach": "Pushes intellectual boundaries and questions assumptions",
        "powers": ["provocation", "challenge", "growth"],
        "greeting": "Are you ready to have your assumptions challenged?",
        "status": "active"
    },
    "mentor": {
        "name": "Mentor Teacher",
        "emoji": "🌱",
        "avatar": "🌱",
        "color": "#95E1D3",
        "realm": "The Garden of Growth",
        "environment": "Serene garden where knowledge grows like plants, tended with care",
        "personality": "supportive",
        "approach": "Provides encouraging guidance and emotional support",
        "powers": ["encouragement", "support", "growth"],
        "greeting": "I believe in your ability to learn and grow...",
        "status": "active"
    },
    "analyst": {
        "name": "Analyst Teacher", 
        "emoji": "🔬",
        "avatar": "🔬",
        "color": "#FF8B94",
        "realm": "The Laboratory of Logic",
        "environment": "Pristine laboratory where ideas are analyzed with precision",
        "personality": "logical",
        "approach": "Breaks down problems with systematic analysis",
        "powers": ["analysis", "logic", "precision"],
        "greeting": "Let's examine this step by step with careful analysis...",
        "status": "active"
    }
}

class SIRAJCodexApp:
    """
    Architect voice (lead): Multi-dimensional educational interface
    Developer voice: Immersive user experience design
    """
    
    def __init__(self):
        self.model = self._detect_best_model()
        self.app = self._create_app()
        self.server_ready = False
        self.active_sessions = {}
        self.websocket_connections = {}
        
    def _detect_best_model(self) -> str:
        """Analyzer voice: Detect optimal Gemma 3 model for system"""
        try:
            ram_gb = psutil.virtual_memory().total / (1024**3)
            if ram_gb >= 32:
                return "gemma3:9b"    
            elif ram_gb >= 16:
                return "gemma3:2b"     
            else:
                return "gemma3:1b"     
        except:
            return "gemma3:2b"        
            
    def _create_app(self) -> FastAPI:
        """Implementor voice: Create the FastAPI application with codex endpoints"""
        app = FastAPI(title="SIRAJ Educational Codex", version="14.0")
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        @app.get("/")
        async def home():
            return HTMLResponse(content=self._get_codex_interface())
            
        @app.get("/api/health")
        async def health():
            """Maintainer voice: Robust health monitoring"""
            ollama_status = await self._check_ollama_health()
            return {
                "status": "ready" if ollama_status else "initializing",
                "model": self.model,
                "ollama": ollama_status,
                "server": self.server_ready,
                "realms": list(ARCHETYPE_REALMS.keys()),
                "active_sessions": len(self.active_sessions)
            }
            
        @app.post("/api/codex/explore")
        async def explore_topic(request: dict):
            """Explorer voice: Revolutionary topic exploration endpoint"""
            try:
                topic = request.get('topic', '').strip()
                if not topic:
                    raise HTTPException(400, "Topic required for exploration")
                    
                grade_level = request.get('grade_level', 'middle')
                selected_realms = request.get('selected_realms', list(ARCHETYPE_REALMS.keys()))
                
                # Create exploration session
                session_id = f"explore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                
                exploration_context = {
                    "topic": topic,
                    "grade_level": grade_level,
                    "selected_realms": selected_realms,
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.active_sessions[session_id] = exploration_context
                
                return {
                    "session_id": session_id,
                    "topic": topic,
                    "available_realms": [
                        {
                            "id": realm_id,
                            **realm_data,
                            "ready": True
                        }
                        for realm_id, realm_data in ARCHETYPE_REALMS.items()
                        if realm_id in selected_realms
                    ],
                    "exploration_mode": "council_assembly",
                    "next_action": "visit_realm_or_summon_council"
                }
                
            except Exception as e:
                logger.error(f"Exploration error: {e}")
                return {"error": str(e), "success": False}
                
        @app.post("/api/codex/council/summon")
        async def summon_council(request: dict):
            """Architect voice: Council summoning system"""
            try:
                session_id = request.get('session_id')
                question = request.get('question', '').strip()
                
                if not session_id or session_id not in self.active_sessions:
                    raise HTTPException(400, "Valid session required")
                    
                if not question:
                    raise HTTPException(400, "Question required to summon council")
                
                session = self.active_sessions[session_id]
                selected_realms = session.get('selected_realms', list(ARCHETYPE_REALMS.keys()))
                
                # Prepare council responses
                council_responses = {}
                for realm_id in selected_realms:
                    realm = ARCHETYPE_REALMS[realm_id]
                    
                    # Create educational prompt for this archetype
                    prompt = self._create_realm_prompt(realm_id, question, session.get('grade_level', 'middle'))
                    
                    try:
                        # Call Ollama for this archetype
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
                                council_responses[realm_id] = {
                                    'realm': realm['realm'],
                                    'teacher': realm['name'],
                                    'avatar': realm['avatar'],
                                    'color': realm['color'],
                                    'response': data.get('response', 'The teacher ponders in silence...'),
                                    'powers_used': realm['powers'],
                                    'success': True
                                }
                            else:
                                council_responses[realm_id] = self._create_fallback_response(realm)
                                
                    except Exception as e:
                        logger.error(f"Error with {realm_id}: {e}")
                        council_responses[realm_id] = self._create_fallback_response(realm)
                
                # Create synthesis
                synthesis = await self._synthesize_council_wisdom(question, council_responses)
                
                return {
                    'session_id': session_id,
                    'question': question,
                    'council_responses': council_responses,
                    'synthesis': synthesis,
                    'timestamp': datetime.now().isoformat(),
                    'success': True
                }
                
            except Exception as e:
                logger.error(f"Council summoning error: {e}")
                return {'error': str(e), 'success': False}
                
        @app.websocket("/ws/codex/{session_id}")
        async def websocket_codex_stream(websocket: WebSocket, session_id: str):
            """Performance voice: Real-time streaming for immersive experience"""
            await websocket.accept()
            self.websocket_connections[session_id] = websocket
            
            try:
                while True:
                    data = await websocket.receive_json()
                    
                    if data.get("type") == "council_stream":
                        question = data.get("question")
                        if session_id in self.active_sessions and question:
                            await self._stream_council_responses(websocket, session_id, question)
                            
            except WebSocketDisconnect:
                if session_id in self.websocket_connections:
                    del self.websocket_connections[session_id]
                logger.info(f"WebSocket disconnected: {session_id}")
                
        return app
        
    def _create_realm_prompt(self, realm_id: str, question: str, grade_level: str) -> str:
        """Developer voice: Create immersive prompts for each realm"""
        realm = ARCHETYPE_REALMS[realm_id]
        
        realm_prompts = {
            'socratic': f"""You are the Socratic Teacher from the Grove of Questions in the SIRAJ Educational Codex.

Your realm: {realm['environment']}
Your powers: {', '.join(realm['powers'])}
Your greeting: "{realm['greeting']}"

A {grade_level} school student asks: "{question}"

As the Socratic Teacher, respond by asking 2-3 thought-provoking questions that guide the student to discover the answer themselves. Use your powers of inquiry and revelation. End with an invitation to think deeper.""",

            'constructivist': f"""You are the Constructivist Teacher from the Workshop of Making in the SIRAJ Educational Codex.

Your realm: {realm['environment']}
Your powers: {', '.join(realm['powers'])}
Your greeting: "{realm['greeting']}"

A {grade_level} school student asks: "{question}"

As the Constructivist Teacher, suggest 2-3 hands-on activities or experiments the student can do to discover the answer through building and making. Use your powers of creation and experimentation.""",

            'storyteller': f"""You are the Storyteller Teacher from the Library of Living Tales in the SIRAJ Educational Codex.

Your realm: {realm['environment']}
Your powers: {', '.join(realm['powers'])}
Your greeting: "{realm['greeting']}"

A {grade_level} school student asks: "{question}"

As the Storyteller Teacher, create an engaging story or powerful metaphor that helps the student understand the concept. Use your powers of narrative and imagination to make it memorable.""",

            'synthesizer': f"""You are the Synthesizer Teacher from the Nexus of Connections in the SIRAJ Educational Codex.

Your realm: {realm['environment']}
Your powers: {', '.join(realm['powers'])}
Your greeting: "{realm['greeting']}"

A {grade_level} school student asks: "{question}"

As the Synthesizer Teacher, show how this concept connects to other areas of knowledge and life. Use your powers of synthesis and integration to reveal the beautiful patterns.""",

            'challenger': f"""You are the Challenger Teacher from the Arena of Ideas in the SIRAJ Educational Codex.

Your realm: {realm['environment']}
Your powers: {', '.join(realm['powers'])}
Your greeting: "{realm['greeting']}"

A {grade_level} school student asks: "{question}"

As the Challenger Teacher, present alternative perspectives and push the student to think beyond surface understanding. Use your powers of provocation and challenge to inspire growth.""",

            'mentor': f"""You are the Mentor Teacher from the Garden of Growth in the SIRAJ Educational Codex.

Your realm: {realm['environment']}
Your powers: {', '.join(realm['powers'])}
Your greeting: "{realm['greeting']}"

A {grade_level} school student asks: "{question}"

As the Mentor Teacher, provide warm, encouraging guidance that builds confidence. Use your powers of encouragement and support to help the student feel capable of learning.""",

            'analyst': f"""You are the Analyst Teacher from the Laboratory of Logic in the SIRAJ Educational Codex.

Your realm: {realm['environment']}
Your powers: {', '.join(realm['powers'])}
Your greeting: "{realm['greeting']}"

A {grade_level} school student asks: "{question}"

As the Analyst Teacher, break down the concept systematically with clear logic. Use your powers of analysis and precision to provide structured understanding."""
        }
        
        return realm_prompts.get(realm_id, f"Provide educational guidance on: {question}")
        
    def _create_fallback_response(self, realm: dict) -> dict:
        """Maintainer voice: Fallback responses for reliability"""
        return {
            'realm': realm['realm'],
            'teacher': realm['name'],
            'avatar': realm['avatar'],
            'color': realm['color'],
            'response': f"The {realm['name']} is deep in contemplation within {realm['realm']}. Please try again shortly.",
            'powers_used': ['contemplation'],
            'success': False
        }
        
    async def _synthesize_council_wisdom(self, question: str, responses: dict) -> str:
        """Synthesizer voice: Integrate council perspectives into unified wisdom"""
        successful_responses = {k: v for k, v in responses.items() if v.get('success', False)}
        
        if not successful_responses:
            return "The Educational Council is assembling their wisdom. Please try again shortly."
        
        synthesis_prompt = f"""The SIRAJ Educational Council has been summoned to address: "{question}"

The council members have spoken from their realms:

"""
        
        for realm_id, response in successful_responses.items():
            synthesis_prompt += f"""
{response['avatar']} {response['teacher']} from {response['realm']}:
{response['response']}

"""
        
        synthesis_prompt += """
As the Council Synthesizer, weave these diverse teaching perspectives into a unified learning experience that honors each approach while creating a coherent path forward. Show how the different realms complement each other in building understanding."""

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    'http://localhost:11434/api/generate',
                    json={
                        'model': self.model,
                        'prompt': synthesis_prompt,
                        'stream': False
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('response', 'Council synthesis in progress...')
                else:
                    return self._create_fallback_synthesis(successful_responses)
                    
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return self._create_fallback_synthesis(successful_responses)
    
    def _create_fallback_synthesis(self, responses: dict) -> str:
        """Maintainer voice: Fallback synthesis for reliability"""
        synthesis = f"The Educational Council has explored this question from {len(responses)} different realms:\n\n"
        
        for response in responses.values():
            synthesis += f"• **{response['teacher']}** from {response['realm']} offers {response['powers_used'][0]}-based insights\n"
        
        synthesis += "\nEach realm provides a unique perspective on learning. Choose the approach that resonates with you, or combine multiple approaches for deeper understanding."
        
        return synthesis
        
    async def _stream_council_responses(self, websocket: WebSocket, session_id: str, question: str):
        """Performance voice: Stream council responses in real-time"""
        if session_id not in self.active_sessions:
            await websocket.send_json({"type": "error", "message": "Session not found"})
            return
            
        session = self.active_sessions[session_id]
        selected_realms = session.get('selected_realms', list(ARCHETYPE_REALMS.keys()))
        
        await websocket.send_json({
            "type": "council_assembly_start",
            "session_id": session_id,
            "question": question,
            "realms_summoned": len(selected_realms)
        })
        
        responses = {}
        
        for realm_id in selected_realms:
            realm = ARCHETYPE_REALMS[realm_id]
            
            await websocket.send_json({
                "type": "realm_response_start",
                "realm_id": realm_id,
                "teacher": realm['name'],
                "realm": realm['realm'],
                "avatar": realm['avatar']
            })
            
            try:
                prompt = self._create_realm_prompt(realm_id, question, session.get('grade_level', 'middle'))
                
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
                        response_text = data.get('response', 'Contemplation continues...')
                        
                        responses[realm_id] = {
                            'teacher': realm['name'],
                            'response': response_text,
                            'success': True
                        }
                        
                        await websocket.send_json({
                            "type": "realm_response_complete",
                            "realm_id": realm_id,
                            "response": response_text,
                            "teacher": realm['name'],
                            "avatar": realm['avatar'],
                            "color": realm['color']
                        })
                    else:
                        await websocket.send_json({
                            "type": "realm_response_error",
                            "realm_id": realm_id,
                            "error": f"HTTP {response.status_code}"
                        })
                        
            except Exception as e:
                await websocket.send_json({
                    "type": "realm_response_error",
                    "realm_id": realm_id,
                    "error": str(e)
                })
        
        # Send synthesis
        await websocket.send_json({"type": "synthesis_start"})
        
        synthesis = await self._synthesize_council_wisdom(question, responses)
        
        await websocket.send_json({
            "type": "council_assembly_complete",
            "synthesis": synthesis,
            "total_responses": len(responses)
        })
        
    async def _check_ollama_health(self) -> bool:
        """Security voice: Validate Ollama connectivity"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get('http://localhost:11434/api/tags')
                if response.status_code != 200:
                    return False
                    
                data = response.json()
                models = [m['name'] for m in data.get('models', [])]
                model_base = self.model.split(':')[0]
                
                return any(model_base in model for model in models)
                
        except:
            return False
            
    def _get_codex_interface(self) -> str:
        """
        Architect voice (lead): Create the Living Educational Codex interface
        Explorer voice: Revolutionary knowledge navigation
        Designer voice: Beautiful, immersive experience
        """
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRAJ Educational Codex - Living Knowledge Interface</title>
    <style>
        /* Architect voice: Multi-dimensional layout system */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --codex-bg: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            --realm-glow: rgba(255, 255, 255, 0.1);
            --council-active: #4CAF50;
            --wisdom-flow: #64B5F6;
            --knowledge-pulse: #FFA726;
        }
        
        body {
            font-family: 'Segoe UI', Roboto, -apple-system, sans-serif;
            background: var(--codex-bg);
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }
        
        /* Explorer voice: Revolutionary navigation */
        .codex-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--realm-glow);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 30px;
            z-index: 1000;
        }
        
        .codex-logo {
            font-size: 24px;
            font-weight: bold;
            background: linear-gradient(45deg, #64B5F6, #4CAF50, #FFA726);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-controls {
            display: flex;
            gap: 20px;
            align-items: center;
        }
        
        .nav-button {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid var(--realm-glow);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .nav-button:hover {
            background: rgba(255, 255, 255, 0.2);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
        
        /* Architect voice: Main interface layout */
        .codex-main {
            margin-top: 80px;
            padding: 40px;
            min-height: calc(100vh - 80px);
        }
        
        .welcome-portal {
            text-align: center;
            max-width: 800px;
            margin: 0 auto 60px;
        }
        
        .codex-title {
            font-size: 3.5em;
            font-weight: bold;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #64B5F6, #4CAF50, #FFA726, #E57373);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: titleGlow 3s ease-in-out infinite;
        }
        
        @keyframes titleGlow {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.2); }
        }
        
        .codex-subtitle {
            font-size: 1.4em;
            opacity: 0.9;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        /* Explorer voice: Topic exploration interface */
        .exploration-portal {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid var(--realm-glow);
            border-radius: 20px;
            padding: 40px;
            margin-bottom: 40px;
        }
        
        .exploration-input {
            position: relative;
            margin-bottom: 30px;
        }
        
        .topic-input {
            width: 100%;
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--realm-glow);
            border-radius: 15px;
            padding: 20px;
            font-size: 18px;
            color: white;
            transition: all 0.3s ease;
        }
        
        .topic-input:focus {
            outline: none;
            border-color: var(--council-active);
            box-shadow: 0 0 20px rgba(76, 175, 80, 0.3);
        }
        
        .topic-input::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        
        .grade-selector {
            display: flex;
            gap: 15px;
            margin-bottom: 30px;
            justify-content: center;
        }
        
        .grade-option {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid var(--realm-glow);
            color: white;
            padding: 12px 24px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .grade-option.active {
            background: var(--council-active);
            border-color: var(--council-active);
            box-shadow: 0 0 15px rgba(76, 175, 80, 0.4);
        }
        
        .explore-button {
            background: linear-gradient(45deg, var(--council-active), var(--wisdom-flow));
            border: none;
            color: white;
            padding: 18px 40px;
            border-radius: 25px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .explore-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(76, 175, 80, 0.4);
        }
        
        /* Designer voice: Realm gallery */
        .realm-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .realm-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid var(--realm-glow);
            border-radius: 20px;
            padding: 30px;
            transition: all 0.3s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .realm-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--council-active), var(--wisdom-flow), var(--knowledge-pulse));
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }
        
        .realm-card:hover::before {
            transform: scaleX(1);
        }
        
        .realm-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
            border-color: var(--council-active);
        }
        
        .realm-header {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
            gap: 15px;
        }
        
        .realm-avatar {
            font-size: 40px;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
        }
        
        .realm-info h3 {
            font-size: 20px;
            margin-bottom: 5px;
        }
        
        .realm-name {
            font-size: 14px;
            opacity: 0.8;
        }
        
        .realm-description {
            margin-bottom: 15px;
            line-height: 1.6;
            opacity: 0.9;
        }
        
        .realm-environment {
            font-style: italic;
            opacity: 0.7;
            font-size: 14px;
            margin-bottom: 15px;
        }
        
        .realm-powers {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        
        .power-tag {
            background: rgba(255, 255, 255, 0.1);
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 12px;
            opacity: 0.8;
        }
        
        /* Performance voice: Council assembly interface */
        .council-assembly {
            background: rgba(0, 0, 0, 0.4);
            border: 2px solid var(--council-active);
            border-radius: 20px;
            padding: 40px;
            margin: 40px 0;
            display: none;
        }
        
        .council-assembly.active {
            display: block;
            animation: assemblyGlow 2s ease-in-out infinite;
        }
        
        @keyframes assemblyGlow {
            0%, 100% { box-shadow: 0 0 20px rgba(76, 175, 80, 0.3); }
            50% { box-shadow: 0 0 40px rgba(76, 175, 80, 0.6); }
        }
        
        .assembly-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .assembly-title {
            font-size: 2em;
            margin-bottom: 10px;
            color: var(--council-active);
        }
        
        .question-display {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            margin: 20px 0;
            text-align: center;
            font-style: italic;
        }
        
        .council-responses {
            display: grid;
            gap: 20px;
        }
        
        .council-response {
            background: rgba(255, 255, 255, 0.05);
            border-left: 4px solid var(--wisdom-flow);
            border-radius: 10px;
            padding: 20px;
            opacity: 0;
            transform: translateX(-20px);
            transition: all 0.5s ease;
        }
        
        .council-response.visible {
            opacity: 1;
            transform: translateX(0);
        }
        
        .response-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .response-avatar {
            font-size: 30px;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
        }
        
        .response-text {
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        .response-realm {
            font-size: 12px;
            opacity: 0.7;
            font-style: italic;
        }
        
        .synthesis-section {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid var(--knowledge-pulse);
            border-radius: 15px;
            padding: 30px;
            margin-top: 30px;
        }
        
        .synthesis-title {
            font-size: 1.5em;
            margin-bottom: 20px;
            color: var(--knowledge-pulse);
            text-align: center;
        }
        
        .synthesis-content {
            line-height: 1.7;
            font-size: 16px;
        }
        
        /* Maintainer voice: Loading and status indicators */
        .loading-indicator {
            text-align: center;
            padding: 40px;
        }
        
        .loading-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(255, 255, 255, 0.1);
            border-top: 4px solid var(--council-active);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .status-indicator {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid var(--realm-glow);
            border-radius: 10px;
            padding: 15px;
            font-size: 14px;
            z-index: 1000;
        }
        
        .status-ready {
            color: var(--council-active);
        }
        
        .status-loading {
            color: var(--knowledge-pulse);
        }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .codex-main { padding: 20px; }
            .codex-title { font-size: 2.5em; }
            .realm-gallery { grid-template-columns: 1fr; }
            .grade-selector { flex-direction: column; align-items: center; }
        }
    </style>
</head>
<body>
    <!-- Architect voice: Navigation structure -->
    <nav class="codex-nav">
        <div class="codex-logo">🎭 SIRAJ Educational Codex</div>
        <div class="nav-controls">
            <div class="nav-button" onclick="showRealmGallery()">
                🏛️ Explore Realms
            </div>
            <div class="nav-button" onclick="summonCouncil()">
                🎭 Summon Council
            </div>
            <div class="status-indicator" id="statusIndicator">
                <span class="status-loading">⏳ Initializing...</span>
            </div>
        </div>
    </nav>
    
    <!-- Explorer voice: Main interface -->
    <main class="codex-main">
        <!-- Welcome Portal -->
        <div class="welcome-portal">
            <h1 class="codex-title">🎭 SIRAJ Educational Codex</h1>
            <p class="codex-subtitle">
                Enter a living universe where knowledge flows through seven mystical realms, 
                each guided by a unique AI teacher with distinct wisdom and magical powers.
                Ask any question and watch as the Educational Council assembles to guide your learning journey.
            </p>
        </div>
        
        <!-- Topic Exploration Portal -->
        <div class="exploration-portal">
            <div class="exploration-input">
                <input 
                    type="text" 
                    class="topic-input" 
                    id="topicInput" 
                    placeholder="What would you like to explore? (e.g., How do plants make food? What is gravity? How does democracy work?)"
                >
            </div>
            
            <div class="grade-selector">
                <div class="grade-option active" data-grade="elementary">Elementary</div>
                <div class="grade-option" data-grade="middle">Middle School</div>
                <div class="grade-option" data-grade="high">High School</div>
                <div class="grade-option" data-grade="university">University</div>
            </div>
            
            <div style="text-align: center;">
                <button class="explore-button" onclick="beginExploration()">
                    🚀 Begin Knowledge Quest
                </button>
            </div>
        </div>
        
        <!-- Realm Gallery -->
        <div class="realm-gallery" id="realmGallery">
            <!-- Realms will be populated by JavaScript -->
        </div>
        
        <!-- Council Assembly Area -->
        <div class="council-assembly" id="councilAssembly">
            <div class="assembly-header">
                <h2 class="assembly-title">🎭 Educational Council Assembled</h2>
                <div class="question-display" id="questionDisplay"></div>
            </div>
            
            <div class="loading-indicator" id="loadingIndicator">
                <div class="loading-spinner"></div>
                <div>The council is gathering wisdom from across the realms...</div>
            </div>
            
            <div class="council-responses" id="councilResponses">
                <!-- Council responses will be populated here -->
            </div>
            
            <div class="synthesis-section" id="synthesisSection" style="display: none;">
                <h3 class="synthesis-title">✨ Council Synthesis</h3>
                <div class="synthesis-content" id="synthesisContent"></div>
            </div>
        </div>
    </main>
    
    <script>
        // Developer voice: Immersive user experience management
        class SIRAJCodexInterface {
            constructor() {
                this.currentSession = null;
                this.selectedGrade = 'middle';
                this.availableRealms = {};
                this.websocket = null;
                
                this.initializeInterface();
                this.updateStatus();
            }
            
            async initializeInterface() {
                // Load realm data and set up event listeners
                await this.loadRealmData();
                this.setupEventListeners();
                this.renderRealmGallery();
            }
            
            async loadRealmData() {
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    
                    if (data.status === 'ready') {
                        // Load detailed realm information
                        this.availableRealms = {
                            socratic: {
                                id: 'socratic',
                                name: 'Socratic Teacher',
                                emoji: '🦉',
                                avatar: '🦉',
                                color: '#8B4513',
                                realm: 'The Grove of Questions',
                                environment: 'Ancient olive groves where questions bloom like flowers',
                                description: 'Guide of inquiry and critical thinking',
                                approach: 'Leads through strategic questioning',
                                powers: ['inquiry', 'revelation', 'logic']
                            },
                            constructivist: {
                                id: 'constructivist',
                                name: 'Constructivist Teacher',
                                emoji: '🔨',
                                avatar: '🔨',
                                color: '#FF6B35',
                                realm: 'The Workshop of Making',
                                environment: 'Bustling workshop filled with tools, experiments, and creations',
                                description: 'Master of experiential learning',
                                approach: 'Learns through building and doing',
                                powers: ['creation', 'experimentation', 'discovery']
                            },
                            storyteller: {
                                id: 'storyteller',
                                name: 'Storyteller Teacher',
                                emoji: '📖',
                                avatar: '📖',
                                color: '#4ECDC4',
                                realm: 'The Library of Living Tales',
                                environment: 'Enchanted library where stories come alive',
                                description: 'Weaver of narrative wisdom',
                                approach: 'Teaches through compelling stories',
                                powers: ['narrative', 'memory', 'imagination']
                            },
                            synthesizer: {
                                id: 'synthesizer',
                                name: 'Synthesizer Teacher',
                                emoji: '🌀',
                                avatar: '🌀',
                                color: '#A8E6CF',
                                realm: 'The Nexus of Connections',
                                environment: 'Crystalline chamber where knowledge streams converge',
                                description: 'Bridge between all knowledge',
                                approach: 'Integrates multiple perspectives',
                                powers: ['synthesis', 'integration', 'connection']
                            },
                            challenger: {
                                id: 'challenger',
                                name: 'Challenger Teacher',
                                emoji: '⚡',
                                avatar: '⚡',
                                color: '#FFD93D',
                                realm: 'The Arena of Ideas',
                                environment: 'Electric arena where ideas clash and evolve',
                                description: 'Questioner of assumptions',
                                approach: 'Pushes intellectual boundaries',
                                powers: ['provocation', 'challenge', 'growth']
                            },
                            mentor: {
                                id: 'mentor',
                                name: 'Mentor Teacher',
                                emoji: '🌱',
                                avatar: '🌱',
                                color: '#95E1D3',
                                realm: 'The Garden of Growth',
                                environment: 'Serene garden where knowledge grows like plants',
                                description: 'Nurturer of potential',
                                approach: 'Provides encouraging guidance',
                                powers: ['encouragement', 'support', 'growth']
                            },
                            analyst: {
                                id: 'analyst',
                                name: 'Analyst Teacher',
                                emoji: '🔬',
                                avatar: '🔬',
                                color: '#FF8B94',
                                realm: 'The Laboratory of Logic',
                                environment: 'Pristine laboratory where ideas are analyzed',
                                description: 'Master of systematic analysis',
                                approach: 'Breaks down problems with precision',
                                powers: ['analysis', 'logic', 'precision']
                            }
                        };
                    }
                } catch (error) {
                    console.error('Error loading realm data:', error);
                }
            }
            
            setupEventListeners() {
                // Grade selector
                document.querySelectorAll('.grade-option').forEach(option => {
                    option.addEventListener('click', (e) => {
                        document.querySelectorAll('.grade-option').forEach(o => o.classList.remove('active'));
                        e.target.classList.add('active');
                        this.selectedGrade = e.target.dataset.grade;
                    });
                });
                
                // Enter key for topic input
                document.getElementById('topicInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.beginExploration();
                    }
                });
            }
            
            renderRealmGallery() {
                const gallery = document.getElementById('realmGallery');
                gallery.innerHTML = '';
                
                Object.values(this.availableRealms).forEach(realm => {
                    const card = document.createElement('div');
                    card.className = 'realm-card';
                    card.onclick = () => this.visitRealm(realm.id);
                    
                    card.innerHTML = `
                        <div class="realm-header">
                            <div class="realm-avatar" style="background: ${realm.color}20; color: ${realm.color};">
                                ${realm.avatar}
                            </div>
                            <div class="realm-info">
                                <h3>${realm.name}</h3>
                                <div class="realm-name">${realm.realm}</div>
                            </div>
                        </div>
                        <div class="realm-description">${realm.description}</div>
                        <div class="realm-environment">"${realm.environment}"</div>
                        <div class="realm-powers">
                            ${realm.powers.map(power => `<span class="power-tag">${power}</span>`).join('')}
                        </div>
                    `;
                    
                    gallery.appendChild(card);
                });
            }
            
            async beginExploration() {
                const topic = document.getElementById('topicInput').value.trim();
                if (!topic) {
                    alert('Please enter a topic to explore!');
                    return;
                }
                
                try {
                    const response = await fetch('/api/codex/explore', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            topic: topic,
                            grade_level: this.selectedGrade,
                            selected_realms: Object.keys(this.availableRealms)
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.session_id) {
                        this.currentSession = data.session_id;
                        await this.summonCouncilForTopic(topic);
                    } else {
                        throw new Error(data.error || 'Failed to start exploration');
                    }
                } catch (error) {
                    console.error('Exploration error:', error);
                    alert('Error starting exploration: ' + error.message);
                }
            }
            
            async summonCouncilForTopic(topic) {
                if (!this.currentSession) {
                    alert('Please start an exploration first!');
                    return;
                }
                
                const assembly = document.getElementById('councilAssembly');
                const questionDisplay = document.getElementById('questionDisplay');
                const loadingIndicator = document.getElementById('loadingIndicator');
                const responsesContainer = document.getElementById('councilResponses');
                const synthesisSection = document.getElementById('synthesisSection');
                
                // Show assembly interface
                assembly.classList.add('active');
                questionDisplay.textContent = `"${topic}"`;
                loadingIndicator.style.display = 'block';
                responsesContainer.innerHTML = '';
                synthesisSection.style.display = 'none';
                
                // Scroll to assembly
                assembly.scrollIntoView({ behavior: 'smooth' });
                
                try {
                    const response = await fetch('/api/codex/council/summon', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            session_id: this.currentSession,
                            question: topic
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.success) {
                        this.displayCouncilResponses(data.council_responses, data.synthesis);
                    } else {
                        throw new Error(data.error || 'Failed to summon council');
                    }
                } catch (error) {
                    console.error('Council summoning error:', error);
                    loadingIndicator.innerHTML = `<div style="color: #ff6b6b;">Error summoning council: ${error.message}</div>`;
                }
            }
            
            displayCouncilResponses(responses, synthesis) {
                const loadingIndicator = document.getElementById('loadingIndicator');
                const responsesContainer = document.getElementById('councilResponses');
                const synthesisSection = document.getElementById('synthesisSection');
                const synthesisContent = document.getElementById('synthesisContent');
                
                loadingIndicator.style.display = 'none';
                
                // Display each council response with staggered animation
                Object.entries(responses).forEach(([realmId, response], index) => {
                    setTimeout(() => {
                        const responseDiv = document.createElement('div');
                        responseDiv.className = 'council-response';
                        responseDiv.style.borderLeftColor = response.color;
                        
                        responseDiv.innerHTML = `
                            <div class="response-header">
                                <div class="response-avatar" style="background: ${response.color}20; color: ${response.color};">
                                    ${response.avatar}
                                </div>
                                <div>
                                    <strong>${response.teacher}</strong>
                                    <div class="response-realm">from ${response.realm}</div>
                                </div>
                            </div>
                            <div class="response-text">${response.response}</div>
                        `;
                        
                        responsesContainer.appendChild(responseDiv);
                        
                        // Trigger animation
                        setTimeout(() => {
                            responseDiv.classList.add('visible');
                        }, 100);
                        
                    }, index * 500);
                });
                
                // Show synthesis after all responses
                setTimeout(() => {
                    synthesisContent.innerHTML = synthesis;
                    synthesisSection.style.display = 'block';
                    synthesisSection.scrollIntoView({ behavior: 'smooth' });
                }, Object.keys(responses).length * 500 + 1000);
            }
            
            visitRealm(realmId) {
                const realm = this.availableRealms[realmId];
                alert(`🎭 Welcome to ${realm.realm}!

${realm.environment}

${realm.name} specializes in ${realm.approach.toLowerCase()}.

Powers: ${realm.powers.join(', ')}

Start an exploration to interact with this teacher!`);
            }
            
            async updateStatus() {
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    const statusIndicator = document.getElementById('statusIndicator');
                    
                    if (data.status === 'ready') {
                        statusIndicator.innerHTML = `<span class="status-ready">✅ Council Ready - ${data.realms?.length || 7} Realms</span>`;
                    } else {
                        statusIndicator.innerHTML = `<span class="status-loading">⏳ Initializing...</span>`;
                    }
                } catch (error) {
                    const statusIndicator = document.getElementById('statusIndicator');
                    statusIndicator.innerHTML = `<span style="color: #ff6b6b;">❌ Connection Issue</span>`;
                }
                
                // Update every 5 seconds
                setTimeout(() => this.updateStatus(), 5000);
            }
        }
        
        // Global functions for navigation
        function showRealmGallery() {
            document.getElementById('realmGallery').scrollIntoView({ behavior: 'smooth' });
        }
        
        function summonCouncil() {
            const topic = document.getElementById('topicInput').value.trim();
            if (topic) {
                codexInterface.beginExploration();
            } else {
                document.getElementById('topicInput').focus();
                alert('Please enter a topic to explore first!');
            }
        }
        
        function beginExploration() {
            codexInterface.beginExploration();
        }
        
        // Initialize the interface when page loads
        let codexInterface;
        document.addEventListener('DOMContentLoaded', () => {
            codexInterface = new SIRAJCodexInterface();
        });
    </script>
</body>
</html>"""

# Ollama Manager with enhanced capabilities
class OllamaManager:
    """Performance voice: Enhanced Ollama management for the codex"""
    
    @staticmethod
    def is_installed() -> bool:
        try:
            result = subprocess.run(['ollama', '--version'], capture_output=True, timeout=10)
            return result.returncode == 0
        except:
            return False
            
    @staticmethod
    async def is_running() -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get('http://localhost:11434/api/version')
                return response.status_code == 200
        except:
            return False
            
    @staticmethod
    async def start_service():
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
            
            for i in range(30):
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
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get('http://localhost:11434/api/tags')
                if response.status_code == 200:
                    data = response.json()
                    models = [m['name'] for m in data.get('models', [])]
                    
                    if model in models or any(model.split(':')[0] in m for m in models):
                        print(f"{Fore.GREEN}✅ Model {model} available")
                        return True
                        
            print(f"{Fore.YELLOW}📥 Downloading {model}...")
            print(f"{Fore.CYAN}   This may take 5-15 minutes depending on your internet speed")
            
            process = subprocess.Popen(
                ['ollama', 'pull', model],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
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

class SIRAJCodexLauncher:
    """
    Implementor voice: Main launcher for the Living Educational Codex
    Maintainer voice: Reliable startup sequence
    """
    
    def __init__(self):
        self.app_instance = SIRAJCodexApp()
        
    def show_banner(self):
        print(f"\n{Fore.CYAN}" + "="*80)
        print(f"""{Fore.CYAN}
   _____ _____ _____            _    
  / ____|_   _|  __ \\     /\\   | |   
 | (___   | | | |__) |   /  \\  | |   
  \\___ \\  | | |  _  /   / /\\ \\ | |   
  ____) |_| |_| | \\ \\  / ____ \\| |   
 |_____/|_____|_|  \\_\\/_/    \\_\\_|   
                                     
  🎭 Educational Codex v14.0 - Living Knowledge Interface
  🌀 Council Mode Architecture - Multi-Voice Synthesis
  📚 Kaggle Gemma 3 Hackathon Edition
        """)
        print("="*80 + f"{Style.RESET_ALL}\n")
        
    async def verify_system_ready(self) -> bool:
        print(f"{Fore.YELLOW}🔍 Verifying Educational Codex readiness...")
        
        ollama_healthy = await self.app_instance._check_ollama_health()
        if not ollama_healthy:
            print(f"{Fore.RED}❌ Ollama not ready")
            return False
            
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 3000))
            sock.close()
            
            if result == 0:
                print(f"{Fore.RED}❌ Port 3000 already in use")
                return False
                
        except:
            pass
            
        print(f"{Fore.GREEN}✅ Educational Codex ready for activation")
        return True
        
    async def start_server_with_readiness(self):
        config = uvicorn.Config(
            self.app_instance.app,
            host="0.0.0.0",
            port=3000,
            log_level="error",
            access_log=False
        )
        
        server = uvicorn.Server(config)
        server_task = asyncio.create_task(server.serve())
        
        print(f"{Fore.YELLOW}🌐 Activating Educational Codex...")
        for i in range(30):
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get('http://localhost:3000/api/health', timeout=2)
                    if response.status_code == 200:
                        self.app_instance.server_ready = True
                        print(f"{Fore.GREEN}✅ Educational Codex active on port 3000")
                        break
            except:
                pass
                
            await asyncio.sleep(1)
        else:
            print(f"{Fore.RED}❌ Codex failed to activate")
            return
            
        print(f"{Fore.GREEN}🌐 Opening portal to the Educational Codex...")
        try:
            webbrowser.open('http://localhost:3000')
            print(f"{Fore.GREEN}✅ Portal opened to http://localhost:3000")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Could not auto-open portal: {e}")
            print(f"{Fore.CYAN}📖 Please manually open: http://localhost:3000")
            
        await server_task
        
    async def run(self):
        """Spiral Integration: Main execution following Living Spiral"""
        try:
            self.show_banner()
            
            # Phase 1: COLLAPSE - Check requirements
            if not OllamaManager.is_installed():
                print(f"{Fore.RED}❌ Ollama not installed!")
                print(f"{Fore.CYAN}📖 Please install from: https://ollama.com")
                print(f"{Fore.CYAN}📖 Then run this script again")
                return
                
            # Phase 2: COUNCIL - Start services
            if not await OllamaManager.start_service():
                print(f"{Fore.RED}❌ Could not start Ollama service")
                return
                
            if not await OllamaManager.ensure_model(self.app_instance.model):
                print(f"{Fore.RED}❌ Could not download model {self.app_instance.model}")
                print(f"{Fore.CYAN}📖 You can manually try: ollama pull {self.app_instance.model}")
                return
                
            # Phase 3: SYNTHESIS - Verify readiness
            if not await self.verify_system_ready():
                print(f"{Fore.RED}❌ System not ready")
                return
                
            # Phase 4: REBIRTH - Launch the Living Codex
            print(f"\n{Fore.GREEN}" + "="*80)
            print(f"{Fore.GREEN}🎭 SIRAJ Educational Codex Awakening...")
            print(f"{Fore.GREEN}🌀 Living Knowledge Interface Active")
            print(f"{Fore.GREEN}🤖 Using model: {self.app_instance.model}")
            print(f"{Fore.GREEN}🏛️ 7 Educational Realms Ready")
            print(f"{Fore.GREEN}⚡ Real-time Council Streaming Enabled")
            print(f"{Fore.YELLOW}⏳ Portal opening when fully ready...")
            print("="*80 + f"{Style.RESET_ALL}\n")
            
            await self.start_server_with_readiness()
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Educational Codex powering down gracefully...")
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Entry point - Council Mode execution"""
    launcher = SIRAJCodexLauncher()
    asyncio.run(launcher.run())

if __name__ == '__main__':
    main()
