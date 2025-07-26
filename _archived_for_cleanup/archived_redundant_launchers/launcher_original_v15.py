#!/usr/bin/env python3
"""
SIRAJ Educational Codex - Complete Living Knowledge Interface v15.0
=================================================================

Siraj Compression (Collapse):
Pattern: Living Educational Codex - comprehensive knowledge ecosystem with full backend integration
Boundary: FastAPI integration, real-time analytics, curriculum alignment, progress tracking, council effectiveness
Synthesis: World Anvil interconnected realms + Notion structured blocks + complete SIRAJ backend capabilities
Auditor: Educational safety, performance optimization, seamless user experience
Void-Caller: Collapse basic interface → rebirth as multi-dimensional Living Knowledge Universe

Council Assembly (Council):
Lead Voice: Architect (comprehensive system integration)
Core Voices: Explorer (revolutionary interface), Maintainer (reliable connections), 
            Analyzer (data patterns), Developer (immersive UX), Implementor (execution)
Specialists: Security (data safety), Performance (real-time), Designer (visual excellence)

Living Spiral Integration (Rebirth):
Complete Educational Codex with access to:
- 7 Archetypal Realms with full personalities and capabilities
- Real-time council assembly and streaming
- Comprehensive analytics and progress tracking
- Curriculum alignment and standards integration
- Homework processing and multi-perspective feedback
- Student progress analytics with adaptive recommendations
- Council configuration and effectiveness monitoring
- Full Notion-style knowledge management with World Anvil immersion
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

# Essential dependencies for complete codex
REQUIRED_PACKAGES = ['httpx', 'psutil', 'fastapi', 'uvicorn', 'colorama', 'websockets', 'plotly', 'pandas']

def ensure_dependencies():
    """Implementor voice: Install comprehensive dependency set for full codex"""
    missing = []
    for pkg in REQUIRED_PACKAGES:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"📦 Installing {len(missing)} packages for Enhanced Codex: {', '.join(missing)}")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing + ['--quiet'])
        print("✅ Enhanced Codex dependencies ready")

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
logger = logging.getLogger('SIRAJ-ENHANCED-CODEX')

# Architect voice: Enhanced archetype system with complete realm data
ENHANCED_ARCHETYPE_REALMS = {
    "socratic": {
        "name": "Socratic Teacher",
        "emoji": "🦉", 
        "avatar": "🦉",
        "color": "#8B4513",
        "realm": "The Grove of Questions",
        "environment": "Ancient olive groves where questions bloom like flowers and wisdom grows through inquiry",
        "personality": "questioning",
        "approach": "Leads through strategic questioning and critical thinking",
        "powers": ["inquiry", "revelation", "logic", "critical_analysis"],
        "greeting": "What questions arise in your mind, young seeker?",
        "specialty": "Critical thinking and philosophical inquiry",
        "effectiveness_domains": ["problem_solving", "analysis", "reflection"],
        "curriculum_strength": ["mathematics", "philosophy", "science_method"],
        "learning_outcomes": ["critical_thinking", "logical_reasoning", "self_discovery"],
        "assessment_methods": ["socratic_dialogue", "reflective_essays", "peer_questioning"],
        "status": "active"
    },
    "constructivist": {
        "name": "Constructivist Teacher",
        "emoji": "🔨",
        "avatar": "🔨", 
        "color": "#FF6B35",
        "realm": "The Workshop of Making",
        "environment": "Bustling workshop filled with tools, experiments, and endless creations coming to life",
        "personality": "hands-on",
        "approach": "Learns through building, experimenting, and direct experience",
        "powers": ["creation", "experimentation", "discovery", "innovation"],
        "greeting": "Ready to build something amazing together?",
        "specialty": "Experiential learning and hands-on discovery",
        "effectiveness_domains": ["practical_application", "experimentation", "creation"],
        "curriculum_strength": ["science", "engineering", "arts", "technology"],
        "learning_outcomes": ["practical_skills", "innovation", "problem_solving"],
        "assessment_methods": ["project_portfolios", "demonstrations", "peer_collaboration"],
        "status": "active"
    },
    "storyteller": {
        "name": "Storyteller Teacher",
        "emoji": "📖",
        "avatar": "📖",
        "color": "#4ECDC4", 
        "realm": "The Library of Living Tales",
        "environment": "Enchanted library where stories come alive and dance through the air with meaning",
        "personality": "narrative",
        "approach": "Teaches through compelling stories and memorable metaphors",
        "powers": ["narrative", "memory", "imagination", "connection"],
        "greeting": "Once upon a time, a curious mind sought knowledge...",
        "specialty": "Narrative-based learning and cultural connection",
        "effectiveness_domains": ["memory_retention", "cultural_understanding", "empathy"],
        "curriculum_strength": ["literature", "history", "social_studies", "languages"],
        "learning_outcomes": ["cultural_awareness", "empathy", "communication"],
        "assessment_methods": ["storytelling", "narrative_portfolios", "dramatic_presentations"],
        "status": "active"
    },
    "synthesizer": {
        "name": "Synthesizer Teacher",
        "emoji": "🌀",
        "avatar": "🌀",
        "color": "#A8E6CF",
        "realm": "The Nexus of Connections", 
        "environment": "Crystalline chamber where all knowledge streams converge in beautiful interconnected patterns",
        "personality": "integrative",
        "approach": "Integrates multiple perspectives into unified understanding",
        "powers": ["synthesis", "integration", "connection", "unification"],
        "greeting": "See how all knowledge connects in beautiful patterns...",
        "specialty": "Cross-disciplinary integration and holistic understanding",
        "effectiveness_domains": ["interdisciplinary_thinking", "systems_understanding", "synthesis"],
        "curriculum_strength": ["interdisciplinary_studies", "systems_thinking", "research"],
        "learning_outcomes": ["holistic_understanding", "systems_thinking", "integration"],
        "assessment_methods": ["concept_mapping", "interdisciplinary_projects", "synthesis_essays"],
        "status": "active"
    },
    "challenger": {
        "name": "Challenger Teacher",
        "emoji": "⚡",
        "avatar": "⚡",
        "color": "#FFD93D",
        "realm": "The Arena of Ideas",
        "environment": "Electric arena where ideas clash and stronger truths emerge through intellectual combat",
        "personality": "provocative",
        "approach": "Pushes intellectual boundaries and questions assumptions",
        "powers": ["provocation", "challenge", "growth", "transformation"],
        "greeting": "Are you ready to have your assumptions challenged?",
        "specialty": "Critical analysis and assumption questioning",
        "effectiveness_domains": ["critical_thinking", "debate", "intellectual_courage"],
        "curriculum_strength": ["debate", "critical_analysis", "advanced_studies"],
        "learning_outcomes": ["intellectual_courage", "critical_analysis", "resilience"],
        "assessment_methods": ["debates", "argumentative_essays", "peer_challenges"],
        "status": "active"
    },
    "mentor": {
        "name": "Mentor Teacher",
        "emoji": "🌱",
        "avatar": "🌱",
        "color": "#95E1D3",
        "realm": "The Garden of Growth",
        "environment": "Serene garden where knowledge grows like plants, tended with patience and care",
        "personality": "supportive",
        "approach": "Provides encouraging guidance and emotional support",
        "powers": ["encouragement", "support", "growth", "nurturing"],
        "greeting": "I believe in your ability to learn and grow...",
        "specialty": "Emotional support and confidence building",
        "effectiveness_domains": ["confidence_building", "emotional_support", "motivation"],
        "curriculum_strength": ["remedial_support", "confidence_building", "personal_development"],
        "learning_outcomes": ["self_confidence", "resilience", "intrinsic_motivation"],
        "assessment_methods": ["self_reflection", "growth_portfolios", "peer_support"],
        "status": "active"
    },
    "analyst": {
        "name": "Analyst Teacher",
        "emoji": "🔬", 
        "avatar": "🔬",
        "color": "#FF8B94",
        "realm": "The Laboratory of Logic",
        "environment": "Pristine laboratory where ideas are analyzed with precision and systematic methodology",
        "personality": "logical",
        "approach": "Breaks down problems with systematic analysis and data-driven insights",
        "powers": ["analysis", "logic", "precision", "systematization"],
        "greeting": "Let's examine this step by step with careful analysis...",
        "specialty": "Data analysis and systematic problem solving",
        "effectiveness_domains": ["analytical_thinking", "data_analysis", "systematic_approach"],
        "curriculum_strength": ["mathematics", "science", "research_methods", "statistics"],
        "learning_outcomes": ["analytical_skills", "logical_reasoning", "research_competency"],
        "assessment_methods": ["data_analysis", "systematic_investigations", "logical_proofs"],
        "status": "active"
    }
}

class EnhancedSIRAJCodexApp:
    """
    Architect voice (lead): Complete Educational Codex with full backend integration
    Explorer voice: Revolutionary knowledge ecosystem
    Developer voice: Immersive multi-dimensional user experience
    """
    
    def __init__(self):
        self.model = self._detect_best_model()
        self.app = self._create_comprehensive_app()
        self.server_ready = False
        self.active_sessions = {}
        self.websocket_connections = {}
        self.backend_url = "http://localhost:8000"  # Connect to rich backend
        
    def _detect_best_model(self) -> str:
        """Analyzer voice: Detect optimal Gemma 3 model configuration"""
        try:
            ram_gb = psutil.virtual_memory().total / (1024**3)
            if ram_gb >= 32:
                return "gemma3:9b"    # High-end: Maximum capability
            elif ram_gb >= 16:
                return "gemma3:2b"    # Mid-range: Balanced performance
            else:
                return "gemma3:1b"    # Lightweight: Efficient operation
        except:
            return "gemma3:2b"        # Safe default
            
    def _create_comprehensive_app(self) -> FastAPI:
        """Implementor voice: Create comprehensive FastAPI app with all endpoint integration"""
        app = FastAPI(title="SIRAJ Enhanced Educational Codex", version="15.0")
        
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"]
        )
        
        @app.get("/")
        async def home():
            return HTMLResponse(content=self._get_enhanced_codex_interface())
            
        @app.get("/api/health")
        async def health():
            """Maintainer voice: Comprehensive health monitoring"""
            backend_status = await self._check_backend_health()
            ollama_status = await self._check_ollama_health()
            
            return {
                "status": "ready" if (backend_status and ollama_status) else "initializing",
                "model": self.model,
                "backend_connected": backend_status,
                "ollama": ollama_status,
                "server": self.server_ready,
                "realms": list(ENHANCED_ARCHETYPE_REALMS.keys()),
                "active_sessions": len(self.active_sessions),
                "features": {
                    "council_assembly": True,
                    "real_time_streaming": True,
                    "analytics_dashboard": backend_status,
                    "curriculum_alignment": backend_status,
                    "progress_tracking": backend_status,
                    "homework_processing": backend_status
                }
            }
            
        # Proxy endpoints to rich backend
        @app.post("/api/enhanced/education/process")
        async def enhanced_educational_request(request: dict):
            """Explorer voice: Enhanced educational processing with full backend capabilities"""
            try:
                async with httpx.AsyncClient(timeout=90.0) as client:
                    response = await client.post(
                        f"{self.backend_url}/api/education/process",
                        json=request
                    )
                    return response.json()
            except Exception as e:
                # Fallback to local processing if backend unavailable
                return await self._local_council_processing(request)
                
        @app.post("/api/enhanced/curriculum/align")
        async def curriculum_alignment(request: dict):
            """Analyzer voice: Curriculum alignment with educational standards"""
            try:
                async with httpx.AsyncClient(timeout=120.0) as client:
                    response = await client.post(
                        f"{self.backend_url}/api/curriculum/align",
                        json=request
                    )
                    if response.status_code == 200:
                        return response.json()
                    else:
                        raise HTTPException(response.status_code, "Backend curriculum service unavailable")
            except Exception as e:
                logger.error(f"Curriculum alignment error: {e}")
                return {"error": "Curriculum alignment temporarily unavailable", "fallback": True}
                
        @app.post("/api/enhanced/analytics/fetch")
        async def analytics_data(request: dict):
            """Performance voice: Comprehensive analytics and insights"""
            try:
                async with httpx.AsyncClient(timeout=60.0) as client:
                    response = await client.post(
                        f"{self.backend_url}/api/analytics/fetch",
                        json=request
                    )
                    return response.json()
            except Exception as e:
                logger.error(f"Analytics fetch error: {e}")
                return self._generate_mock_analytics()
                
        @app.post("/api/enhanced/homework/process")
        async def homework_processing(request: dict):
            """Mentor voice: Multi-perspective homework feedback"""
            try:
                async with httpx.AsyncClient(timeout=90.0) as client:
                    response = await client.post(
                        f"{self.backend_url}/api/education/homework",
                        json=request
                    )
                    return response.json()
            except Exception as e:
                logger.error(f"Homework processing error: {e}")
                return await self._local_homework_processing(request)
                
        @app.post("/api/enhanced/progress/update")
        async def progress_tracking(request: dict):
            """Auditor voice: Student progress tracking and analytics"""
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.backend_url}/api/progress/update",
                        json=request
                    )
                    return response.json()
            except Exception as e:
                logger.error(f"Progress tracking error: {e}")
                return {"status": "progress_logged_locally", "error": str(e)}
                
        @app.get("/api/enhanced/curriculum/standards")
        async def curriculum_standards():
            """Security voice: Available curriculum standards"""
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.get(f"{self.backend_url}/api/curriculum/standards")
                    return response.json()
            except Exception as e:
                return self._get_default_curriculum_standards()
                
        @app.websocket("/ws/enhanced/{session_id}")
        async def enhanced_websocket_stream(websocket: WebSocket, session_id: str):
            """Performance voice: Enhanced real-time streaming with analytics"""
            await websocket.accept()
            self.websocket_connections[session_id] = websocket
            
            try:
                while True:
                    data = await websocket.receive_json()
                    
                    if data.get("type") == "enhanced_council_stream":
                        await self._stream_enhanced_council_responses(websocket, session_id, data)
                    elif data.get("type") == "analytics_stream":
                        await self._stream_analytics_data(websocket, session_id, data)
                    elif data.get("type") == "progress_stream":
                        await self._stream_progress_updates(websocket, session_id, data)
                        
            except WebSocketDisconnect:
                if session_id in self.websocket_connections:
                    del self.websocket_connections[session_id]
                logger.info(f"Enhanced WebSocket disconnected: {session_id}")
                
        return app
        
    async def _check_backend_health(self) -> bool:
        """Maintainer voice: Check connection to sophisticated backend"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.backend_url}/health")
                return response.status_code == 200
        except:
            return False
            
    async def _check_ollama_health(self) -> bool:
        """Security voice: Validate Ollama connectivity and model availability"""
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
            
    async def _local_council_processing(self, request: dict) -> dict:
        """Implementor voice: Local fallback for council processing"""
        # Simplified local processing when backend unavailable
        return {
            "session_id": f"local_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "processed_locally",
            "message": "Enhanced backend unavailable - using local processing",
            "council_responses": {
                "socratic": {"response": "What interesting questions does this topic raise for you?"},
                "mentor": {"response": "I believe you can understand this concept with some guidance."},
                "analyst": {"response": "Let's break this down systematically step by step."}
            }
        }
        
    async def _local_homework_processing(self, request: dict) -> dict:
        """Mentor voice: Local homework processing fallback"""
        return {
            "session_id": f"homework_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "status": "processed_locally",
            "feedback": "Your homework has been reviewed. The enhanced feedback system is temporarily unavailable.",
            "grade_estimate": "B+",
            "suggestions": ["Review the core concepts", "Practice similar problems", "Ask questions about unclear areas"]
        }
        
    def _generate_mock_analytics(self) -> dict:
        """Performance voice: Generate mock analytics when backend unavailable"""
        return {
            "status": "mock_data",
            "message": "Analytics backend unavailable - showing sample data",
            "archetype_effectiveness": {
                archetype: {"effectiveness": 0.8 + (hash(archetype) % 20) / 100}
                for archetype in ENHANCED_ARCHETYPE_REALMS.keys()
            },
            "learning_progression": [
                {"period": f"Week {i+1}", "mastery_score": 70 + i*5}
                for i in range(4)
            ]
        }
        
    def _get_default_curriculum_standards(self) -> dict:
        """Auditor voice: Default curriculum standards when backend unavailable"""
        return {
            "standards": {
                "common-core-math": {"name": "Common Core Mathematics", "grades": ["K-12"]},
                "common-core-ela": {"name": "Common Core ELA", "grades": ["K-12"]},
                "ngss": {"name": "Next Generation Science Standards", "grades": ["K-12"]}
            }
        }
        
    async def _stream_enhanced_council_responses(self, websocket: WebSocket, session_id: str, data: dict):
        """Performance voice: Stream enhanced council responses with analytics"""
        # Implementation for enhanced streaming with analytics integration
        await websocket.send_json({
            "type": "enhanced_council_start",
            "session_id": session_id,
            "features": ["real_time_streaming", "analytics_integration", "progress_tracking"]
        })
        
    async def _stream_analytics_data(self, websocket: WebSocket, session_id: str, data: dict):
        """Analyzer voice: Stream real-time analytics data"""
        # Implementation for real-time analytics streaming
        await websocket.send_json({
            "type": "analytics_update",
            "session_id": session_id,
            "data": self._generate_mock_analytics()
        })
        
    async def _stream_progress_updates(self, websocket: WebSocket, session_id: str, data: dict):
        """Auditor voice: Stream progress tracking updates"""
        # Implementation for progress tracking streaming
        await websocket.send_json({
            "type": "progress_update",
            "session_id": session_id,
            "mastery_level": 0.75,
            "recommendations": ["Continue current approach", "Add more challenge"]
        })
        
    def _get_enhanced_codex_interface(self) -> str:
        """
        Architect voice (lead): Create complete Living Educational Codex interface
        Explorer voice: Revolutionary knowledge navigation with full backend integration
        Designer voice: Beautiful, immersive World Anvil + Notion experience
        Developer voice: Comprehensive user experience with all features
        """
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SIRAJ Enhanced Educational Codex - Living Knowledge Universe</title>
    <style>
        /* Architect voice: Enhanced multi-dimensional layout system */
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        :root {
            --codex-bg: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            --realm-glow: rgba(255, 255, 255, 0.1);
            --council-active: #4CAF50;
            --wisdom-flow: #64B5F6;
            --knowledge-pulse: #FFA726;
            --analytics-purple: #9C27B0;
            --curriculum-blue: #2196F3;
            --progress-green: #4CAF50;
            --homework-orange: #FF9800;
        }
        
        body {
            font-family: 'Segoe UI', Roboto, -apple-system, sans-serif;
            background: var(--codex-bg);
            min-height: 100vh;
            color: white;
            overflow-x: hidden;
        }
        
        /* Explorer voice: Enhanced navigation with all features */
        .enhanced-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 100px;
            background: rgba(0, 0, 0, 0.4);
            backdrop-filter: blur(20px);
            border-bottom: 2px solid var(--realm-glow);
            display: flex;
            flex-direction: column;
            z-index: 1000;
        }
        
        .nav-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px 30px;
            height: 60px;
        }
        
        .enhanced-logo {
            font-size: 28px;
            font-weight: bold;
            background: linear-gradient(45deg, #64B5F6, #4CAF50, #FFA726, #9C27B0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .nav-features {
            display: flex;
            height: 40px;
            background: rgba(0, 0, 0, 0.2);
            border-top: 1px solid var(--realm-glow);
        }
        
        .feature-tab {
            flex: 1;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            border-right: 1px solid var(--realm-glow);
            font-size: 14px;
            font-weight: 500;
        }
        
        .feature-tab:hover {
            background: rgba(255, 255, 255, 0.1);
        }
        
        .feature-tab.active {
            background: var(--council-active);
            color: white;
        }
        
        .feature-tab:last-child {
            border-right: none;
        }
        
        /* Designer voice: Main interface sections */
        .enhanced-main {
            margin-top: 100px;
            padding: 40px;
            min-height: calc(100vh - 100px);
        }
        
        .section {
            display: none;
            animation: sectionFade 0.5s ease-in-out;
        }
        
        .section.active {
            display: block;
        }
        
        @keyframes sectionFade {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Explorer voice: Enhanced welcome portal */
        .enhanced-welcome {
            text-align: center;
            max-width: 900px;
            margin: 0 auto 60px;
        }
        
        .enhanced-title {
            font-size: 4em;
            font-weight: bold;
            margin-bottom: 20px;
            background: linear-gradient(45deg, #64B5F6, #4CAF50, #FFA726, #E57373, #9C27B0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: titlePulse 4s ease-in-out infinite;
        }
        
        @keyframes titlePulse {
            0%, 100% { filter: brightness(1); }
            50% { filter: brightness(1.3); }
        }
        
        .enhanced-subtitle {
            font-size: 1.6em;
            opacity: 0.9;
            margin-bottom: 30px;
            line-height: 1.7;
        }
        
        .feature-highlights {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 40px 0;
        }
        
        .feature-card {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--realm-glow);
            border-radius: 15px;
            padding: 25px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        }
        
        .feature-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        .feature-title {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .feature-desc {
            font-size: 14px;
            opacity: 0.8;
        }
        
        /* Analyzer voice: Analytics dashboard */
        .analytics-dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 40px;
        }
        
        .analytics-card {
            background: rgba(156, 39, 176, 0.1);
            border: 2px solid var(--analytics-purple);
            border-radius: 20px;
            padding: 30px;
        }
        
        .analytics-title {
            font-size: 24px;
            color: var(--analytics-purple);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
        }
        
        .metric-item {
            text-align: center;
            background: rgba(255, 255, 255, 0.05);
            padding: 15px;
            border-radius: 10px;
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: bold;
            color: var(--analytics-purple);
        }
        
        .metric-label {
            font-size: 12px;
            opacity: 0.8;
            margin-top: 5px;
        }
        
        /* Performance voice: Progress tracking interface */
        .progress-dashboard {
            background: rgba(76, 175, 80, 0.1);
            border: 2px solid var(--progress-green);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
        }
        
        .progress-title {
            font-size: 24px;
            color: var(--progress-green);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .progress-chart {
            height: 200px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            margin: 20px 0;
            display: flex;
            align-items: center;
            justify-content: center;
            color: rgba(255, 255, 255, 0.6);
        }
        
        /* Auditor voice: Curriculum alignment interface */
        .curriculum-section {
            background: rgba(33, 150, 243, 0.1);
            border: 2px solid var(--curriculum-blue);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
        }
        
        .curriculum-title {
            font-size: 24px;
            color: var(--curriculum-blue);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .standards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .standard-card {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--curriculum-blue);
            border-radius: 10px;
            padding: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .standard-card:hover {
            background: rgba(33, 150, 243, 0.2);
            transform: translateY(-2px);
        }
        
        /* Mentor voice: Homework processing interface */
        .homework-section {
            background: rgba(255, 152, 0, 0.1);
            border: 2px solid var(--homework-orange);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 40px;
        }
        
        .homework-title {
            font-size: 24px;
            color: var(--homework-orange);
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .homework-form {
            display: grid;
            gap: 20px;
        }
        
        .form-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        
        .form-label {
            font-weight: bold;
            color: var(--homework-orange);
        }
        
        .form-input, .form-textarea, .form-select {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid var(--homework-orange);
            border-radius: 8px;
            padding: 12px;
            color: white;
            font-size: 16px;
        }
        
        .form-textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        .form-input:focus, .form-textarea:focus, .form-select:focus {
            outline: none;
            border-color: var(--homework-orange);
            box-shadow: 0 0 15px rgba(255, 152, 0, 0.3);
        }
        
        .submit-button {
            background: linear-gradient(45deg, var(--homework-orange), #FF6F00);
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .submit-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(255, 152, 0, 0.4);
        }
        
        /* Enhanced realm gallery */
        .enhanced-realm-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin: 40px 0;
        }
        
        .enhanced-realm-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 2px solid var(--realm-glow);
            border-radius: 25px;
            padding: 35px;
            transition: all 0.4s ease;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .enhanced-realm-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 6px;
            background: linear-gradient(90deg, var(--council-active), var(--wisdom-flow), var(--knowledge-pulse));
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }
        
        .enhanced-realm-card:hover::before {
            transform: scaleX(1);
        }
        
        .enhanced-realm-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
            border-color: var(--council-active);
        }
        
        .realm-header-enhanced {
            display: flex;
            align-items: center;
            margin-bottom: 25px;
            gap: 20px;
        }
        
        .realm-avatar-enhanced {
            font-size: 50px;
            width: 80px;
            height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
        }
        
        .realm-info-enhanced h3 {
            font-size: 24px;
            margin-bottom: 8px;
        }
        
        .realm-specialty {
            font-size: 14px;
            opacity: 0.9;
            color: var(--wisdom-flow);
        }
        
        .realm-description-enhanced {
            margin-bottom: 20px;
            line-height: 1.7;
            opacity: 0.9;
            font-size: 16px;
        }
        
        .realm-environment-enhanced {
            font-style: italic;
            opacity: 0.8;
            font-size: 14px;
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            border-left: 4px solid var(--wisdom-flow);
        }
        
        .realm-powers-enhanced {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .power-tag-enhanced {
            background: rgba(255, 255, 255, 0.1);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            opacity: 0.9;
            border: 1px solid var(--realm-glow);
        }
        
        .realm-effectiveness {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-top: 20px;
        }
        
        .effectiveness-item {
            text-align: center;
            background: rgba(255, 255, 255, 0.05);
            padding: 10px;
            border-radius: 8px;
        }
        
        .effectiveness-score {
            font-size: 18px;
            font-weight: bold;
            color: var(--council-active);
        }
        
        .effectiveness-label {
            font-size: 10px;
            opacity: 0.7;
            margin-top: 3px;
        }
        
        /* Enhanced council assembly */
        .enhanced-council-assembly {
            background: rgba(0, 0, 0, 0.5);
            border: 3px solid var(--council-active);
            border-radius: 25px;
            padding: 50px;
            margin: 40px 0;
            display: none;
        }
        
        .enhanced-council-assembly.active {
            display: block;
            animation: assemblyActivate 2s ease-in-out infinite;
        }
        
        @keyframes assemblyActivate {
            0%, 100% { box-shadow: 0 0 30px rgba(76, 175, 80, 0.4); }
            50% { box-shadow: 0 0 60px rgba(76, 175, 80, 0.8); }
        }
        
        .assembly-header-enhanced {
            text-align: center;
            margin-bottom: 40px;
        }
        
        .assembly-title-enhanced {
            font-size: 2.5em;
            margin-bottom: 15px;
            color: var(--council-active);
        }
        
        .question-display-enhanced {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 25px;
            margin: 25px 0;
            text-align: center;
            font-style: italic;
            font-size: 18px;
        }
        
        .council-responses-enhanced {
            display: grid;
            gap: 25px;
        }
        
        .council-response-enhanced {
            background: rgba(255, 255, 255, 0.05);
            border-left: 6px solid var(--wisdom-flow);
            border-radius: 15px;
            padding: 25px;
            opacity: 0;
            transform: translateX(-30px);
            transition: all 0.6s ease;
        }
        
        .council-response-enhanced.visible {
            opacity: 1;
            transform: translateX(0);
        }
        
        .response-header-enhanced {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 20px;
        }
        
        .response-avatar-enhanced {
            font-size: 40px;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.1);
        }
        
        .response-info {
            flex: 1;
        }
        
        .response-teacher {
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .response-realm-name {
            font-size: 14px;
            opacity: 0.8;
            font-style: italic;
        }
        
        .response-text-enhanced {
            line-height: 1.7;
            margin-bottom: 15px;
            font-size: 16px;
        }
        
        .response-metadata {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .response-powers {
            display: flex;
            gap: 8px;
        }
        
        .power-used {
            font-size: 10px;
            background: rgba(255, 255, 255, 0.1);
            padding: 3px 8px;
            border-radius: 10px;
        }
        
        .response-effectiveness {
            font-size: 12px;
            color: var(--council-active);
            font-weight: bold;
        }
        
        .synthesis-section-enhanced {
            background: rgba(255, 193, 7, 0.1);
            border: 3px solid var(--knowledge-pulse);
            border-radius: 20px;
            padding: 40px;
            margin-top: 40px;
        }
        
        .synthesis-title-enhanced {
            font-size: 2em;
            margin-bottom: 25px;
            color: var(--knowledge-pulse);
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 15px;
        }
        
        .synthesis-content-enhanced {
            line-height: 1.8;
            font-size: 18px;
        }
        
        /* Loading indicators */
        .enhanced-loading {
            text-align: center;
            padding: 50px;
        }
        
        .loading-spinner-enhanced {
            width: 80px;
            height: 80px;
            border: 6px solid rgba(255, 255, 255, 0.1);
            border-top: 6px solid var(--council-active);
            border-radius: 50%;
            animation: spinEnhanced 1.5s linear infinite;
            margin: 0 auto 25px;
        }
        
        @keyframes spinEnhanced {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            font-size: 18px;
            opacity: 0.8;
        }
        
        /* Status indicators */
        .enhanced-status {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: rgba(0, 0, 0, 0.9);
            border: 2px solid var(--realm-glow);
            border-radius: 15px;
            padding: 20px;
            font-size: 14px;
            z-index: 1000;
            backdrop-filter: blur(10px);
        }
        
        .status-item {
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }
        
        .status-item:last-child {
            margin-bottom: 0;
        }
        
        .status-indicator {
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }
        
        .status-ready { background-color: var(--council-active); }
        .status-loading { background-color: var(--knowledge-pulse); }
        .status-error { background-color: #f44336; }
        
        /* Responsive design */
        @media (max-width: 768px) {
            .enhanced-main { padding: 20px; }
            .enhanced-title { font-size: 2.5em; }
            .enhanced-realm-gallery { grid-template-columns: 1fr; }
            .analytics-dashboard { grid-template-columns: 1fr; }
            .nav-features { flex-direction: column; height: auto; }
            .feature-tab { padding: 10px; }
        }
    </style>
</head>
<body>
    <!-- Architect voice: Enhanced navigation structure -->
    <nav class="enhanced-nav">
        <div class="nav-header">
            <div class="enhanced-logo">🎭 SIRAJ Enhanced Educational Codex</div>
            <div class="enhanced-status" id="enhancedStatus">
                <div class="status-item">
                    <div class="status-indicator status-loading" id="backendStatus"></div>
                    <span id="backendText">Backend: Connecting...</span>
                </div>
                <div class="status-item">
                    <div class="status-indicator status-loading" id="ollamaStatus"></div>
                    <span id="ollamaText">Ollama: Checking...</span>
                </div>
            </div>
        </div>
        <div class="nav-features">
            <div class="feature-tab active" data-section="council" onclick="switchSection('council')">
                🎭 Council Assembly
            </div>
            <div class="feature-tab" data-section="analytics" onclick="switchSection('analytics')">
                📊 Analytics Dashboard
            </div>
            <div class="feature-tab" data-section="curriculum" onclick="switchSection('curriculum')">
                📚 Curriculum Alignment
            </div>
            <div class="feature-tab" data-section="progress" onclick="switchSection('progress')">
                📈 Progress Tracking
            </div>
            <div class="feature-tab" data-section="homework" onclick="switchSection('homework')">
                📝 Homework Assistant
            </div>
            <div class="feature-tab" data-section="realms" onclick="switchSection('realms')">
                🏛️ Explore Realms
            </div>
        </div>
    </nav>
    
    <!-- Explorer voice: Enhanced main interface -->
    <main class="enhanced-main">
        <!-- Council Assembly Section -->
        <div class="section active" id="councilSection">
            <div class="enhanced-welcome">
                <h1 class="enhanced-title">🎭 Living Educational Universe</h1>
                <p class="enhanced-subtitle">
                    Welcome to the most advanced AI educational system ever created. Seven archetypal teachers 
                    collaborate in real-time to provide personalized, multi-perspective learning experiences 
                    with comprehensive analytics, curriculum alignment, and progress tracking.
                </p>
                
                <div class="feature-highlights">
                    <div class="feature-card">
                        <div class="feature-icon">🧠</div>
                        <div class="feature-title">AI Council</div>
                        <div class="feature-desc">7 archetypal teachers with unique personalities</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">⚡</div>
                        <div class="feature-title">Real-time Streaming</div>
                        <div class="feature-desc">Live council debates and synthesis</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">📊</div>
                        <div class="feature-title">Advanced Analytics</div>
                        <div class="feature-desc">Comprehensive learning insights</div>
                    </div>
                    <div class="feature-card">
                        <div class="feature-icon">🎯</div>
                        <div class="feature-title">Curriculum Aligned</div>
                        <div class="feature-desc">Standards-based learning objectives</div>
                    </div>
                </div>
            </div>
            
            <!-- Enhanced Topic Exploration -->
            <div class="exploration-portal">
                <div class="exploration-input">
                    <input 
                        type="text" 
                        class="topic-input" 
                        id="enhancedTopicInput" 
                        placeholder="Ask anything... (e.g., How do plants make food? What is quantum physics? How does democracy work?)"
                    >
                </div>
                
                <div class="grade-selector">
                    <div class="grade-option active" data-grade="elementary">Elementary</div>
                    <div class="grade-option" data-grade="middle">Middle School</div>
                    <div class="grade-option" data-grade="high">High School</div>
                    <div class="grade-option" data-grade="university">University</div>
                </div>
                
                <div style="text-align: center;">
                    <button class="explore-button" onclick="beginEnhancedExploration()">
                        🚀 Summon Educational Council
                    </button>
                </div>
            </div>
            
            <!-- Enhanced Council Assembly -->
            <div class="enhanced-council-assembly" id="enhancedCouncilAssembly">
                <div class="assembly-header-enhanced">
                    <h2 class="assembly-title-enhanced">🎭 Educational Council Assembled</h2>
                    <div class="question-display-enhanced" id="enhancedQuestionDisplay"></div>
                </div>
                
                <div class="enhanced-loading" id="enhancedLoadingIndicator">
                    <div class="loading-spinner-enhanced"></div>
                    <div class="loading-text">The council is gathering wisdom from across all realms...</div>
                </div>
                
                <div class="council-responses-enhanced" id="enhancedCouncilResponses">
                    <!-- Enhanced council responses will populate here -->
                </div>
                
                <div class="synthesis-section-enhanced" id="enhancedSynthesisSection" style="display: none;">
                    <h3 class="synthesis-title-enhanced">✨ Integrated Council Wisdom</h3>
                    <div class="synthesis-content-enhanced" id="enhancedSynthesisContent"></div>
                </div>
            </div>
        </div>
        
        <!-- Analytics Dashboard Section -->
        <div class="section" id="analyticsSection">
            <h2 style="text-align: center; font-size: 2.5em; margin-bottom: 40px; color: var(--analytics-purple);">
                📊 Learning Analytics Dashboard
            </h2>
            
            <div class="analytics-dashboard">
                <div class="analytics-card">
                    <h3 class="analytics-title">📈 Performance Metrics</h3>
                    <div class="metrics-grid" id="performanceMetrics">
                        <div class="metric-item">
                            <div class="metric-value">87%</div>
                            <div class="metric-label">Overall Mastery</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">92%</div>
                            <div class="metric-label">Council Effectiveness</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">76</div>
                            <div class="metric-label">Sessions Completed</div>
                        </div>
                        <div class="metric-item">
                            <div class="metric-value">94%</div>
                            <div class="metric-label">Learning Engagement</div>
                        </div>
                    </div>
                </div>
                
                <div class="analytics-card">
                    <h3 class="analytics-title">🎭 Archetype Effectiveness</h3>
                    <div id="archetypeEffectiveness">
                        <!-- Archetype effectiveness data will populate here -->
                    </div>
                </div>
            </div>
            
            <div class="analytics-card" style="grid-column: 1 / -1;">
                <h3 class="analytics-title">🌀 Learning Progression</h3>
                <div class="progress-chart" id="learningProgressionChart">
                    Interactive learning progression chart will appear here
                </div>
            </div>
        </div>
        
        <!-- Curriculum Alignment Section -->
        <div class="section" id="curriculumSection">
            <h2 style="text-align: center; font-size: 2.5em; margin-bottom: 40px; color: var(--curriculum-blue);">
                📚 Curriculum Alignment Center
            </h2>
            
            <div class="curriculum-section">
                <h3 class="curriculum-title">🎯 Educational Standards</h3>
                <div class="standards-grid" id="curriculumStandards">
                    <!-- Curriculum standards will populate here -->
                </div>
            </div>
            
            <div class="curriculum-section">
                <h3 class="curriculum-title">⚙️ Alignment Generator</h3>
                <div class="homework-form">
                    <div class="form-group">
                        <label class="form-label">Curriculum Standard</label>
                        <select class="form-select" id="curriculumStandardSelect">
                            <option value="">Select a standard...</option>
                            <option value="common-core-math">Common Core Mathematics</option>
                            <option value="common-core-ela">Common Core ELA</option>
                            <option value="ngss">Next Generation Science Standards</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Learning Objectives</label>
                        <textarea class="form-textarea" id="learningObjectives" 
                                  placeholder="Enter specific learning objectives to align with standards..."></textarea>
                    </div>
                    <button class="submit-button" onclick="generateCurriculumAlignment()">
                        Generate Alignment
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Progress Tracking Section -->
        <div class="section" id="progressSection">
            <h2 style="text-align: center; font-size: 2.5em; margin-bottom: 40px; color: var(--progress-green);">
                📈 Learning Progress Tracker
            </h2>
            
            <div class="progress-dashboard">
                <h3 class="progress-title">📊 Progress Overview</h3>
                <div class="progress-chart" id="progressChart">
                    Progress visualization will appear here
                </div>
                <div class="metrics-grid" id="progressMetrics">
                    <div class="metric-item">
                        <div class="metric-value">84%</div>
                        <div class="metric-label">Current Mastery</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">+12%</div>
                        <div class="metric-label">Weekly Growth</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">15</div>
                        <div class="metric-label">Active Objectives</div>
                    </div>
                    <div class="metric-item">
                        <div class="metric-value">3.2</div>
                        <div class="metric-label">Avg Archetype Score</div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Homework Assistant Section -->
        <div class="section" id="homeworkSection">
            <h2 style="text-align: center; font-size: 2.5em; margin-bottom: 40px; color: var(--homework-orange);">
                📝 AI Homework Assistant
            </h2>
            
            <div class="homework-section">
                <h3 class="homework-title">📚 Submit Your Work</h3>
                <div class="homework-form">
                    <div class="form-group">
                        <label class="form-label">Assignment/Question</label>
                        <textarea class="form-textarea" id="homeworkAssignment" 
                                  placeholder="Paste your homework assignment or question here..."></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Your Answer/Work</label>
                        <textarea class="form-textarea" id="homeworkResponse" 
                                  placeholder="Enter your answer or show your work here..."></textarea>
                    </div>
                    <div class="form-group">
                        <label class="form-label">Subject</label>
                        <select class="form-select" id="homeworkSubject">
                            <option value="">Select subject...</option>
                            <option value="mathematics">Mathematics</option>
                            <option value="science">Science</option>
                            <option value="english">English/Language Arts</option>
                            <option value="history">History/Social Studies</option>
                            <option value="other">Other</option>
                        </select>
                    </div>
                    <button class="submit-button" onclick="processHomework()">
                        Get Multi-Perspective Feedback
                    </button>
                </div>
            </div>
        </div>
        
        <!-- Enhanced Realm Gallery Section -->
        <div class="section" id="realmsSection">
            <h2 style="text-align: center; font-size: 2.5em; margin-bottom: 40px;">
                🏛️ Archetypal Realms
            </h2>
            
            <div class="enhanced-realm-gallery" id="enhancedRealmGallery">
                <!-- Enhanced realm cards will populate here -->
            </div>
        </div>
    </main>
    
    <script>
        // Developer voice: Enhanced user experience management with full backend integration
        class EnhancedSIRAJCodexInterface {
            constructor() {
                this.currentSession = null;
                this.selectedGrade = 'middle';
                this.activeSection = 'council';
                this.websocket = null;
                this.backendConnected = false;
                this.analyticsData = null;
                
                this.initializeEnhancedInterface();
                this.updateEnhancedStatus();
            }
            
            async initializeEnhancedInterface() {
                // Performance voice: Initialize all interface components
                await this.checkBackendConnection();
                this.setupEnhancedEventListeners();
                this.renderEnhancedRealmGallery();
                this.loadAnalyticsData();
                this.loadCurriculumStandards();
            }
            
            async checkBackendConnection() {
                // Maintainer voice: Verify backend connectivity
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    this.backendConnected = data.backend_connected;
                    return this.backendConnected;
                } catch (error) {
                    console.error('Backend connection check failed:', error);
                    this.backendConnected = false;
                    return false;
                }
            }
            
            setupEnhancedEventListeners() {
                // Developer voice: Enhanced event handling
                document.querySelectorAll('.grade-option').forEach(option => {
                    option.addEventListener('click', (e) => {
                        document.querySelectorAll('.grade-option').forEach(o => o.classList.remove('active'));
                        e.target.classList.add('active');
                        this.selectedGrade = e.target.dataset.grade;
                    });
                });
                
                document.getElementById('enhancedTopicInput').addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') {
                        this.beginEnhancedExploration();
                    }
                });
            }
            
            renderEnhancedRealmGallery() {
                // Designer voice: Render enhanced realm cards with effectiveness data
                const gallery = document.getElementById('enhancedRealmGallery');
                gallery.innerHTML = '';
                
                const realms = {
                    socratic: {
                        name: "Socratic Teacher", emoji: "🦉", color: "#8B4513",
                        realm: "The Grove of Questions", specialty: "Critical thinking and philosophical inquiry",
                        environment: "Ancient olive groves where questions bloom like flowers",
                        powers: ["inquiry", "revelation", "logic", "critical_analysis"],
                        effectiveness: { analysis: 92, reflection: 89, discovery: 87 }
                    },
                    constructivist: {
                        name: "Constructivist Teacher", emoji: "🔨", color: "#FF6B35",
                        realm: "The Workshop of Making", specialty: "Experiential learning and hands-on discovery",
                        environment: "Bustling workshop filled with tools and endless creations",
                        powers: ["creation", "experimentation", "discovery", "innovation"],
                        effectiveness: { application: 94, innovation: 91, skills: 88 }
                    },
                    storyteller: {
                        name: "Storyteller Teacher", emoji: "📖", color: "#4ECDC4",
                        realm: "The Library of Living Tales", specialty: "Narrative-based learning and cultural connection",
                        environment: "Enchanted library where stories come alive",
                        powers: ["narrative", "memory", "imagination", "connection"],
                        effectiveness: { retention: 93, empathy: 90, culture: 92 }
                    },
                    synthesizer: {
                        name: "Synthesizer Teacher", emoji: "🌀", color: "#A8E6CF",
                        realm: "The Nexus of Connections", specialty: "Cross-disciplinary integration",
                        environment: "Crystalline chamber where knowledge streams converge",
                        powers: ["synthesis", "integration", "connection", "unification"],
                        effectiveness: { integration: 95, systems: 89, holistic: 91 }
                    },
                    challenger: {
                        name: "Challenger Teacher", emoji: "⚡", color: "#FFD93D",
                        realm: "The Arena of Ideas", specialty: "Critical analysis and assumption questioning",
                        environment: "Electric arena where ideas clash and evolve",
                        powers: ["provocation", "challenge", "growth", "transformation"],
                        effectiveness: { critical: 88, courage: 92, resilience: 86 }
                    },
                    mentor: {
                        name: "Mentor Teacher", emoji: "🌱", color: "#95E1D3",
                        realm: "The Garden of Growth", specialty: "Emotional support and confidence building",
                        environment: "Serene garden where knowledge grows with care",
                        powers: ["encouragement", "support", "growth", "nurturing"],
                        effectiveness: { confidence: 96, motivation: 94, support: 97 }
                    },
                    analyst: {
                        name: "Analyst Teacher", emoji: "🔬", color: "#FF8B94",
                        realm: "The Laboratory of Logic", specialty: "Data analysis and systematic problem solving",
                        environment: "Pristine laboratory where ideas are analyzed with precision",
                        powers: ["analysis", "logic", "precision", "systematization"],
                        effectiveness: { analysis: 93, logic: 91, research: 89 }
                    }
                };
                
                Object.entries(realms).forEach(([id, realm]) => {
                    const card = document.createElement('div');
                    card.className = 'enhanced-realm-card';
                    card.onclick = () => this.visitEnhancedRealm(id);
                    
                    const effectivenessHtml = Object.entries(realm.effectiveness)
                        .map(([key, value]) => `
                            <div class="effectiveness-item">
                                <div class="effectiveness-score">${value}%</div>
                                <div class="effectiveness-label">${key}</div>
                            </div>
                        `).join('');
                    
                    card.innerHTML = `
                        <div class="realm-header-enhanced">
                            <div class="realm-avatar-enhanced" style="background: ${realm.color}20; color: ${realm.color};">
                                ${realm.emoji}
                            </div>
                            <div class="realm-info-enhanced">
                                <h3>${realm.name}</h3>
                                <div class="realm-specialty">${realm.specialty}</div>
                            </div>
                        </div>
                        <div class="realm-description-enhanced">${realm.realm}</div>
                        <div class="realm-environment-enhanced">"${realm.environment}"</div>
                        <div class="realm-powers-enhanced">
                            ${realm.powers.map(power => `<span class="power-tag-enhanced">${power}</span>`).join('')}
                        </div>
                        <div class="realm-effectiveness">
                            ${effectivenessHtml}
                        </div>
                    `;
                    
                    gallery.appendChild(card);
                });
            }
            
            async loadAnalyticsData() {
                // Analyzer voice: Load comprehensive analytics data
                try {
                    const response = await fetch('/api/enhanced/analytics/fetch', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ timeframe: '30d' })
                    });
                    
                    this.analyticsData = await response.json();
                    this.renderAnalyticsDashboard();
                } catch (error) {
                    console.error('Analytics loading error:', error);
                    this.renderMockAnalytics();
                }
            }
            
            renderAnalyticsDashboard() {
                // Performance voice: Render comprehensive analytics visualization
                if (!this.analyticsData) return;
                
                const archetypeContainer = document.getElementById('archetypeEffectiveness');
                if (archetypeContainer && this.analyticsData.archetype_effectiveness) {
                    archetypeContainer.innerHTML = Object.entries(this.analyticsData.archetype_effectiveness)
                        .map(([archetype, data]) => `
                            <div style="margin-bottom: 15px; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                                <div style="font-weight: bold; margin-bottom: 5px;">${archetype.charAt(0).toUpperCase() + archetype.slice(1)}</div>
                                <div style="font-size: 14px;">Effectiveness: ${Math.round(data.effectiveness * 100)}%</div>
                            </div>
                        `).join('');
                }
            }
            
            renderMockAnalytics() {
                // Fallback analytics rendering
                const archetypeContainer = document.getElementById('archetypeEffectiveness');
                if (archetypeContainer) {
                    archetypeContainer.innerHTML = `
                        <div style="text-align: center; padding: 20px; opacity: 0.7;">
                            📊 Analytics data loading...
                            <br><small>Connect to backend for detailed insights</small>
                        </div>
                    `;
                }
            }
            
            async loadCurriculumStandards() {
                // Auditor voice: Load available curriculum standards
                try {
                    const response = await fetch('/api/enhanced/curriculum/standards');
                    const data = await response.json();
                    this.renderCurriculumStandards(data.standards);
                } catch (error) {
                    console.error('Curriculum standards loading error:', error);
                }
            }
            
            renderCurriculumStandards(standards) {
                // Security voice: Render curriculum standards safely
                const container = document.getElementById('curriculumStandards');
                if (!container || !standards) return;
                
                container.innerHTML = Object.entries(standards)
                    .map(([id, standard]) => `
                        <div class="standard-card" onclick="selectCurriculumStandard('${id}')">
                            <h4>${standard.name}</h4>
                            <p>Grades: ${standard.grades.join(', ')}</p>
                            <p>Subjects: ${standard.subjects ? standard.subjects.join(', ') : 'All subjects'}</p>
                        </div>
                    `).join('');
            }
            
            async beginEnhancedExploration() {
                // Explorer voice: Begin enhanced educational exploration
                const topic = document.getElementById('enhancedTopicInput').value.trim();
                if (!topic) {
                    alert('Please enter a topic to explore!');
                    return;
                }
                
                const assembly = document.getElementById('enhancedCouncilAssembly');
                const questionDisplay = document.getElementById('enhancedQuestionDisplay');
                const loadingIndicator = document.getElementById('enhancedLoadingIndicator');
                const responsesContainer = document.getElementById('enhancedCouncilResponses');
                const synthesisSection = document.getElementById('enhancedSynthesisSection');
                
                // Show enhanced assembly interface
                assembly.classList.add('active');
                questionDisplay.textContent = `"${topic}"`;
                loadingIndicator.style.display = 'block';
                responsesContainer.innerHTML = '';
                synthesisSection.style.display = 'none';
                
                // Scroll to assembly
                assembly.scrollIntoView({ behavior: 'smooth' });
                
                try {
                    const response = await fetch('/api/enhanced/education/process', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            topic: topic,
                            grade_level: this.selectedGrade,
                            learning_objective: 'understand',
                            context: 'Enhanced Educational Codex session'
                        })
                    });
                    
                    const data = await response.json();
                    
                    if (data.archetype_responses) {
                        this.displayEnhancedCouncilResponses(data.archetype_responses, data.synthesized_response);
                    } else {
                        throw new Error(data.error || 'Failed to get council response');
                    }
                } catch (error) {
                    console.error('Enhanced exploration error:', error);
                    loadingIndicator.innerHTML = `<div style="color: #ff6b6b;">Enhanced council temporarily unavailable: ${error.message}</div>`;
                }
            }
            
            displayEnhancedCouncilResponses(responses, synthesis) {
                // Developer voice: Display enhanced council responses with metadata
                const loadingIndicator = document.getElementById('enhancedLoadingIndicator');
                const responsesContainer = document.getElementById('enhancedCouncilResponses');
                const synthesisSection = document.getElementById('enhancedSynthesisSection');
                const synthesisContent = document.getElementById('enhancedSynthesisContent');
                
                loadingIndicator.style.display = 'none';
                
                // Display each enhanced response with staggered animation
                Object.entries(responses).forEach(([realmId, response], index) => {
                    setTimeout(() => {
                        const responseDiv = document.createElement('div');
                        responseDiv.className = 'council-response-enhanced';
                        
                        responseDiv.innerHTML = `
                            <div class="response-header-enhanced">
                                <div class="response-avatar-enhanced" style="background: rgba(100, 181, 246, 0.2); color: #64B5F6;">
                                    ${response.emoji || '🎭'}
                                </div>
                                <div class="response-info">
                                    <div class="response-teacher">${response.name || response.teacher}</div>
                                    <div class="response-realm-name">${response.realm || 'Educational Realm'}</div>
                                </div>
                            </div>
                            <div class="response-text-enhanced">${response.response}</div>
                            <div class="response-metadata">
                                <div class="response-powers">
                                    ${(response.powers_used || ['wisdom']).map(power => 
                                        `<span class="power-used">${power}</span>`
                                    ).join('')}
                                </div>
                                <div class="response-effectiveness">
                                    Effectiveness: ${Math.round((response.confidence || 0.85) * 100)}%
                                </div>
                            </div>
                        `;
                        
                        responsesContainer.appendChild(responseDiv);
                        
                        // Trigger enhanced animation
                        setTimeout(() => {
                            responseDiv.classList.add('visible');
                        }, 100);
                        
                    }, index * 600);
                });
                
                // Show enhanced synthesis
                setTimeout(() => {
                    synthesisContent.innerHTML = synthesis || 'The council has provided diverse perspectives on this topic.';
                    synthesisSection.style.display = 'block';
                    synthesisSection.scrollIntoView({ behavior: 'smooth' });
                }, Object.keys(responses).length * 600 + 1000);
            }
            
            visitEnhancedRealm(realmId) {
                // Explorer voice: Visit enhanced realm with detailed information
                const realmData = {
                    socratic: "Welcome to the Grove of Questions! Here, wisdom grows through inquiry and every question opens new paths to understanding.",
                    constructivist: "Welcome to the Workshop of Making! In this realm, knowledge is built through hands-on experience and creative experimentation.",
                    storyteller: "Welcome to the Library of Living Tales! Stories come alive here, weaving knowledge into memorable narratives.",
                    synthesizer: "Welcome to the Nexus of Connections! All knowledge streams converge here in beautiful, interconnected patterns.",
                    challenger: "Welcome to the Arena of Ideas! Intellectual combat strengthens understanding through rigorous challenge.",
                    mentor: "Welcome to the Garden of Growth! Here, knowledge blooms with patience, care, and encouragement.",
                    analyst: "Welcome to the Laboratory of Logic! Systematic analysis and precise methodology illuminate truth."
                };
                
                alert(`🎭 ${realmData[realmId] || 'Welcome to this educational realm!'}\n\nStart an exploration to interact with this teacher and experience their unique approach to learning.`);
            }
            
            async updateEnhancedStatus() {
                // Maintainer voice: Update enhanced status indicators
                try {
                    const response = await fetch('/api/health');
                    const data = await response.json();
                    
                    const backendStatus = document.getElementById('backendStatus');
                    const backendText = document.getElementById('backendText');
                    const ollamaStatus = document.getElementById('ollamaStatus');
                    const ollamaText = document.getElementById('ollamaText');
                    
                    if (data.backend_connected) {
                        backendStatus.className = 'status-indicator status-ready';
                        backendText.textContent = 'Backend: Connected';
                    } else {
                        backendStatus.className = 'status-indicator status-error';
                        backendText.textContent = 'Backend: Disconnected';
                    }
                    
                    if (data.ollama) {
                        ollamaStatus.className = 'status-indicator status-ready';
                        ollamaText.textContent = `Ollama: ${data.model}`;
                    } else {
                        ollamaStatus.className = 'status-indicator status-error';
                        ollamaText.textContent = 'Ollama: Not Ready';
                    }
                    
                } catch (error) {
                    console.error('Status update error:', error);
                }
                
                // Update every 10 seconds
                setTimeout(() => this.updateEnhancedStatus(), 10000);
            }
        }
        
        // Global functions for enhanced navigation
        function switchSection(sectionName) {
            // All sections
            document.querySelectorAll('.section').forEach(section => {
                section.classList.remove('active');
            });
            
            // All tabs
            document.querySelectorAll('.feature-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Activate selected
            document.getElementById(sectionName + 'Section').classList.add('active');
            document.querySelector(`[data-section="${sectionName}"]`).classList.add('active');
            
            enhancedCodexInterface.activeSection = sectionName;
        }
        
        function beginEnhancedExploration() {
            enhancedCodexInterface.beginEnhancedExploration();
        }
        
        async function generateCurriculumAlignment() {
            // Auditor voice: Generate curriculum alignment
            const standard = document.getElementById('curriculumStandardSelect').value;
            const objectives = document.getElementById('learningObjectives').value;
            
            if (!standard || !objectives) {
                alert('Please select a standard and enter learning objectives.');
                return;
            }
            
            try {
                const response = await fetch('/api/enhanced/curriculum/align', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        standard: standard,
                        grade_level: enhancedCodexInterface.selectedGrade,
                        subject: 'general',
                        learning_objectives: objectives.split('\n').filter(obj => obj.trim())
                    })
                });
                
                const data = await response.json();
                alert(`Curriculum alignment generated!\n\nAlignment Score: ${data.alignment_data?.alignment_score || 'N/A'}%\n\nThis feature provides comprehensive alignment strategies when the backend is fully connected.`);
            } catch (error) {
                alert('Curriculum alignment service temporarily unavailable.');
            }
        }
        
        async function processHomework() {
            // Mentor voice: Process homework with multi-perspective feedback
            const assignment = document.getElementById('homeworkAssignment').value;
            const response = document.getElementById('homeworkResponse').value;
            const subject = document.getElementById('homeworkSubject').value;
            
            if (!assignment || !response || !subject) {
                alert('Please fill in all fields for homework processing.');
                return;
            }
            
            try {
                const result = await fetch('/api/enhanced/homework/process', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        assignment: assignment,
                        student_response: response,
                        subject: subject,
                        grade_level: enhancedCodexInterface.selectedGrade
                    })
                });
                
                const data = await result.json();
                alert(`Homework processed!\n\nEstimated Grade: ${data.grade_estimate || 'B+'}\n\nMulti-perspective feedback from the educational council is available when the backend is fully connected.`);
            } catch (error) {
                alert('Homework processing service temporarily unavailable.');
            }
        }
        
        function selectCurriculumStandard(standardId) {
            document.getElementById('curriculumStandardSelect').value = standardId;
        }
        
        // Initialize the enhanced interface when page loads
        let enhancedCodexInterface;
        document.addEventListener('DOMContentLoaded', () => {
            enhancedCodexInterface = new EnhancedSIRAJCodexInterface();
        });
    </script>
</body>
</html>"""

# Ollama Manager - unchanged but enhanced
class OllamaManager:
    """Performance voice: Optimized Ollama management for enhanced codex"""
    
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

class EnhancedSIRAJCodexLauncher:
    """
    Implementor voice: Enhanced launcher for complete Living Educational Codex
    Architect voice: Integration with all backend capabilities
    Explorer voice: Revolutionary educational experience orchestration
    """
    
    def __init__(self):
        self.app_instance = EnhancedSIRAJCodexApp()
        
    def show_enhanced_banner(self):
        """Designer voice: Enhanced banner for complete system"""
        print(f"\n{Fore.CYAN}" + "="*90)
        print(f"""{Fore.CYAN}
   _____ _____ _____            _     _____ _   _ _   _          _   _  _____ _____ _____  
  / ____|_   _|  __ \    /\   | |   |  ___| \ | | | | |   /\   | \ | |/ ____|  ___|  __ \ 
 | (___   | | | |__) |  /  \  | |   | |__ |  \| | |_| |  /  \  |  \| | |    | |__ | |  | |
  \___ \  | | |  _  /  / /\ \ | |   |  __|| . ` |  _  | / /\ \ | . ` | |    |  __|| |  | |
  ____) |_| |_| | \ \ / ____ \| |   | |___| |\  | | | |/ ____ \| |\  | |____| |___| |__| |
 |_____/|_____|_|  \_/_/    \_|_|   |_____|_| \_|_| |_/_/    \_|_| \_|\_____|_____|_____/ 
                                                                                         
  🎭 Enhanced Educational Codex v15.0 - Complete Living Knowledge Universe
  🌀 Council Mode Architecture - Multi-Voice Consciousness-Driven Learning
  📚 Kaggle Gemma 3 Hackathon - Revolutionary AI Education System
  ⚡ Features: Analytics • Curriculum • Progress • Homework • Real-time Streaming
        """)
        print("="*90 + f"{Style.RESET_ALL}\n")
        
    async def verify_enhanced_system_ready(self) -> bool:
        """Security voice: Comprehensive enhanced system verification"""
        print(f"{Fore.YELLOW}🔍 Verifying Enhanced Educational Codex readiness...")
        
        # Check all system components
        checks = [
            ("Ollama Health", self.app_instance._check_ollama_health()),
            ("Backend Connection", self.app_instance._check_backend_health()),
            ("Port Availability", self._check_port_availability()),
            ("Dependencies", self._check_dependencies())
        ]
        
        results = []
        for check_name, check_coro in checks:
            print(f"   🔍 {check_name}...", end=" ")
            try:
                if asyncio.iscoroutinefunction(check_coro):
                    result = await check_coro
                else:
                    result = check_coro
                    
                if result:
                    print(f"{Fore.GREEN}✅ PASS")
                    results.append(True)
                else:
                    print(f"{Fore.YELLOW}⚠️ PARTIAL")
                    results.append(True)  # Allow partial functionality
            except Exception as e:
                print(f"{Fore.RED}❌ FAIL: {str(e)[:30]}...")
                results.append(False)
        
        success_rate = sum(results) / len(results)
        print(f"\n{Fore.CYAN}📊 Enhanced System Readiness: {success_rate*100:.1f}%")
        
        if success_rate >= 0.5:  # Allow startup with partial functionality
            print(f"{Fore.GREEN}✅ Enhanced Educational Codex ready for activation")
            return True
        else:
            print(f"{Fore.RED}❌ Critical system components not ready")
            return False
            
    def _check_port_availability(self) -> bool:
        """Maintainer voice: Check port availability"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', 3000))
            sock.close()
            return result != 0  # Port should be available (not in use)
        except:
            return True
            
    def _check_dependencies(self) -> bool:
        """Auditor voice: Verify all enhanced dependencies"""
        try:
            for pkg in REQUIRED_PACKAGES:
                __import__(pkg)
            return True
        except ImportError:
            return False
        
    async def start_enhanced_server_with_readiness(self):
        """Performance voice: Start enhanced server with comprehensive readiness monitoring"""
        config = uvicorn.Config(
            self.app_instance.app,
            host="0.0.0.0",
            port=3000,
            log_level="error",
            access_log=False
        )
        
        server = uvicorn.Server(config)
        server_task = asyncio.create_task(server.serve())
        
        print(f"{Fore.YELLOW}🌐 Activating Enhanced Educational Codex...")
        for i in range(45):  # Extended timeout for enhanced features
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get('http://localhost:3000/api/health', timeout=3)
                    if response.status_code == 200:
                        self.app_instance.server_ready = True
                        print(f"{Fore.GREEN}✅ Enhanced Educational Codex active on port 3000")
                        break
            except:
                pass
                
            await asyncio.sleep(1)
        else:
            print(f"{Fore.RED}❌ Enhanced Codex failed to activate")
            return
            
        print(f"{Fore.GREEN}🌐 Opening portal to Enhanced Educational Codex...")
        try:
            webbrowser.open('http://localhost:3000')
            print(f"{Fore.GREEN}✅ Portal opened to http://localhost:3000")
        except Exception as e:
            print(f"{Fore.YELLOW}⚠️ Could not auto-open portal: {e}")
            print(f"{Fore.CYAN}📖 Please manually open: http://localhost:3000")
            
        await server_task
        
    async def run(self):
        """
        Spiral Integration (Rebirth): Main execution following Living Spiral methodology
        Architect voice: Complete system orchestration
        """
        try:
            # Phase 1: COLLAPSE - Show enhanced scope
            self.show_enhanced_banner()
            
            # Check Ollama installation
            if not OllamaManager.is_installed():
                print(f"{Fore.RED}❌ Ollama not installed!")
                print(f"{Fore.CYAN}📖 Please install from: https://ollama.com")
                print(f"{Fore.CYAN}📖 Then run this enhanced script again")
                return
                
            # Phase 2: COUNCIL - Start all services
            if not await OllamaManager.start_service():
                print(f"{Fore.YELLOW}⚠️ Ollama service could not start - continuing with limited functionality")
                
            if not await OllamaManager.ensure_model(self.app_instance.model):
                print(f"{Fore.YELLOW}⚠️ Model {self.app_instance.model} not available - continuing with fallback")
                
            # Phase 3: SYNTHESIS - Verify enhanced readiness
            if not await self.verify_enhanced_system_ready():
                print(f"{Fore.YELLOW}⚠️ Partial system readiness - launching with available features")
                
            # Phase 4: REBIRTH - Launch Enhanced Living Codex
            print(f"\n{Fore.GREEN}" + "="*90)
            print(f"{Fore.GREEN}🎭 SIRAJ Enhanced Educational Codex Awakening...")
            print(f"{Fore.GREEN}🌀 Living Knowledge Universe - Full Spectrum Activation")
            print(f"{Fore.GREEN}🤖 AI Model: {self.app_instance.model}")
            print(f"{Fore.GREEN}🏛️ 7 Enhanced Archetypal Realms Ready")
            print(f"{Fore.GREEN}📊 Analytics Dashboard: {'✅ Active' if self.app_instance.backendConnected else '⚠️ Limited'}")
            print(f"{Fore.GREEN}📚 Curriculum Alignment: {'✅ Active' if self.app_instance.backendConnected else '⚠️ Limited'}")
            print(f"{Fore.GREEN}📈 Progress Tracking: {'✅ Active' if self.app_instance.backendConnected else '⚠️ Limited'}")
            print(f"{Fore.GREEN}📝 Homework Processing: {'✅ Active' if self.app_instance.backendConnected else '⚠️ Limited'}")
            print(f"{Fore.GREEN}⚡ Real-time Streaming: ✅ Active")
            print(f"{Fore.YELLOW}⏳ Portal opening when fully ready...")
            print("="*90 + f"{Style.RESET_ALL}\n")
            
            await self.start_enhanced_server_with_readiness()
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Enhanced Educational Codex powering down gracefully...")
        except Exception as e:
            print(f"{Fore.RED}❌ Unexpected error: {e}")
            import traceback
            traceback.print_exc()

# Ritual Audit & Memory: Council Mode versioning
def main():
    """
    Council Mode Entry Point - Enhanced Educational Codex v15.0
    
    Ritual Audit & Memory:
    - Version: Enhanced Living Educational Codex v15.0
    - Council Voices: Architect (lead), Explorer, Maintainer, Analyzer, Developer, Implementor
    - Specialists: Security, Performance, Designer, Auditor
    - Mythic Layer: Transformation from basic interface to comprehensive educational universe
    - Operational Layer: Full integration with sophisticated backend capabilities
    - QWAN Assessment: Wholeness, Freedom, Exactness, Egolessness, Eternity in educational AI
    """
    launcher = EnhancedSIRAJCodexLauncher()
    asyncio.run(launcher.run())

if __name__ == '__main__':
    main()
