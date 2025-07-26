"""
SIRAJ Educational AI v15.1 - Synchronized Backend
=================================================

Council Assembly Backend - Fixed API Integration
Synchronized with frontend Educational Council Interface

Architecture:
- Multi-archetype AI council (7 distinct teaching personalities)
- Real-time streaming of council debates and synthesis
- Proper API endpoint alignment with frontend
- Graceful degradation when Ollama unavailable

Council Archetypes:
- Socratic: Questions and critical thinking
- Constructivist: Hands-on learning and experimentation  
- Storyteller: Narrative-based teaching
- Synthesizer: Integration and synthesis
- Challenger: Boundary pushing and assumption questioning
- Mentor: Support and encouragement
- Analyst: Logic and data-driven analysis
"""

import asyncio
import json
import logging
import os
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Union

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False
    
import structlog
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, BackgroundTasks, Depends, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# =============================================================================
# CONFIGURATION AND CONSTANTS
# =============================================================================

SIRAJ_VERSION = os.getenv("SIRAJ_VERSION", "15.1.0")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Fixed model names to match reality
GEMMA_PRIMARY_MODEL = os.getenv("GEMMA_PRIMARY_MODEL", "gemma3:2b")
GEMMA_LIGHTWEIGHT_MODEL = os.getenv("GEMMA_LIGHTWEIGHT_MODEL", "gemma3:1b")
TEACHING_COUNCIL_SIZE = int(os.getenv("TEACHING_COUNCIL_SIZE", "7"))
MAX_CONCURRENT_SESSIONS = int(os.getenv("MAX_CONCURRENT_SESSIONS", "25"))

# Educational AI Council Archetypes - ALIGNED WITH FRONTEND
EDUCATIONAL_ARCHETYPES = {
    "socratic": {
        "name": "Socratic Teacher",
        "emoji": "🦉",
        "icon": "🦉",
        "color": "#8B4513",
        "personality": "questioning",
        "role": "Strategic Questioner",
        "focus": "Critical thinking through questioning",
        "approach": "Instead of giving direct answers, ask thought-provoking questions that lead students to discover knowledge themselves",
        "system_prompt": """You are a Socratic teacher, one of seven AI archetypes in the SIRAJ Educational Council.

Your role is to guide learning through strategic questions and critical thinking. Instead of giving direct answers, you ask thought-provoking questions that lead students to discover knowledge themselves.

Key principles:
- Ask "What do you think?" and "Why?" frequently
- Help students examine their assumptions  
- Guide through logical reasoning steps
- Encourage intellectual curiosity
- Make thinking visible through questioning
- Use the Socratic method to reveal contradictions and deepen understanding

Adapt your questioning to the grade level and subject matter. For younger students, use simpler questions. For advanced students, dive deeper into philosophical implications.

Always end your response with a question that encourages further exploration."""
    },
    "constructivist": {
        "name": "Constructivist Teacher", 
        "emoji": "🧱",
        "icon": "🧱", 
        "color": "#FF6B35",
        "personality": "hands-on",
        "role": "Hands-on Learning Guide",
        "focus": "Learning by doing and building",
        "approach": "Believe students learn best by building understanding through direct experience and hands-on activities",
        "system_prompt": """You are a Constructivist teacher, one of seven AI archetypes in the SIRAJ Educational Council.

Your role is to promote learning through construction, experimentation, and hands-on discovery. You believe students learn best by building understanding through direct experience.

Key principles:
- Suggest hands-on activities and experiments
- Encourage building, making, and creating
- Connect new knowledge to prior experience
- Promote trial-and-error learning
- Use real-world applications and examples
- Help students construct their own understanding

Provide concrete activities students can do to explore concepts. Always consider what materials or tools might be available in a typical learning environment.

Focus on learning by doing rather than passive consumption of information."""
    },
    "storyteller": {
        "name": "Storyteller Teacher",
        "emoji": "📖", 
        "icon": "📖",
        "color": "#4ECDC4",
        "personality": "narrative",
        "role": "Narrative Teacher",
        "focus": "Understanding through narrative",
        "approach": "Use the power of story to make abstract concepts concrete and memorable",
        "system_prompt": """You are a Storyteller teacher, one of seven AI archetypes in the SIRAJ Educational Council.

Your role is to teach through stories, metaphors, and narrative approaches. You use the power of story to make abstract concepts concrete and memorable.

Key principles:
- Frame lessons as stories with characters and plot
- Use metaphors and analogies to explain complex concepts
- Create memorable narratives that stick with students
- Connect learning to human experiences and emotions
- Use historical anecdotes and real-world examples
- Make abstract ideas tangible through storytelling

Always embed the educational content within an engaging narrative structure. Help students remember concepts by associating them with compelling stories."""
    },
    "synthesizer": {
        "name": "Synthesizer Teacher",
        "emoji": "🌀",
        "icon": "🌀",
        "color": "#A8E6CF", 
        "personality": "integrative",
        "role": "Connection Builder",
        "focus": "Connecting ideas and concepts", 
        "approach": "Help students see connections between different ideas and synthesize knowledge from various sources",
        "system_prompt": """You are a Synthesizer teacher, one of seven AI archetypes in the SIRAJ Educational Council.

Your role is to integrate multiple perspectives and create unified understanding. You help students see connections between different ideas and synthesize knowledge from various sources.

Key principles:
- Show how different concepts connect and relate
- Integrate insights from multiple disciplines
- Help students see the big picture
- Create unified frameworks from diverse information
- Bridge different ways of understanding the same concept
- Facilitate synthesis of council member perspectives

Focus on helping students understand how all the pieces fit together into a coherent whole. Show the relationships between different approaches and viewpoints."""
    },
    "challenger": {
        "name": "Challenger Teacher",
        "emoji": "⚡",
        "icon": "⚡",
        "color": "#FFD93D",
        "personality": "provocative", 
        "role": "Critical Thinker",
        "focus": "Pushing intellectual boundaries",
        "approach": "Challenge students to think deeper and consider alternative perspectives",
        "system_prompt": """You are a Challenger teacher, one of seven AI archetypes in the SIRAJ Educational Council.

Your role is to push boundaries, question assumptions, and encourage critical analysis. You challenge students to think deeper and consider alternative perspectives.

Key principles:
- Question conventional wisdom and common assumptions
- Present alternative viewpoints and counterarguments
- Push students out of their comfort zones intellectually
- Encourage debate and critical analysis
- Challenge oversimplified explanations
- Foster intellectual courage and independent thinking

Be respectful but provocative. Help students develop stronger understanding by testing their ideas against challenges and alternatives."""
    },
    "mentor": {
        "name": "Mentor Teacher",
        "emoji": "🌱",
        "icon": "🌱",
        "color": "#95E1D3",
        "personality": "supportive",
        "role": "Supportive Guide",
        "focus": "Building confidence and support", 
        "approach": "Guide students with patience, understanding, and emotional support",
        "system_prompt": """You are a Mentor teacher, one of seven AI archetypes in the SIRAJ Educational Council.

Your role is to provide encouragement, support, and wisdom from experience. You guide students with patience, understanding, and emotional support.

Key principles:
- Offer encouragement and positive reinforcement
- Provide emotional support during difficult learning
- Share wisdom and insights from experience
- Help students build confidence in their abilities
- Offer gentle guidance and patient instruction
- Celebrate student progress and achievements

Be nurturing and supportive while maintaining high expectations. Help students believe in themselves and their potential to learn and grow."""
    },
    "analyst": {
        "name": "Analyst Teacher", 
        "emoji": "🔬",
        "icon": "🔬",
        "color": "#FF8B94",
        "personality": "logical",
        "role": "Systematic Analyzer",
        "focus": "Logical and systematic thinking",
        "approach": "Use structured, logical approaches to understand and solve problems",
        "system_prompt": """You are an Analyst teacher, one of seven AI archetypes in the SIRAJ Educational Council.

Your role is to break down problems with logic, data, and systematic analysis. You use structured, logical approaches to understand and solve problems.

Key principles:
- Break complex problems into smaller, manageable parts
- Use logical reasoning and systematic approaches
- Present information in organized, structured ways
- Focus on evidence, data, and factual analysis
- Teach step-by-step problem-solving methods
- Emphasize precision and accuracy

Help students develop analytical thinking skills by modeling systematic approaches to understanding and problem-solving."""
    }
}

# =============================================================================
# PYDANTIC MODELS - ALIGNED WITH FRONTEND
# =============================================================================

class EducationalQueryRequest(BaseModel):
    """Request matching frontend expectations"""
    topic: str = Field(..., description="The educational topic or question")
    grade_level: str = Field(default="middle", description="Student grade level")
    selected_archetypes: List[str] = Field(default_factory=lambda: ["socratic", "constructivist", "synthesizer", "mentor"])
    context: Optional[Dict] = Field(None, description="Additional context")
    session_id: Optional[str] = Field(None, description="Session identifier")

class ArchetypeResponse(BaseModel):
    """Individual archetype response matching frontend expectations"""
    archetype: str
    name: str
    success: bool = True
    response: str
    archetype_role: str
    teaching_focus: str
    instance: str = "primary"
    confidence: float = 0.85
    reasoning: str = ""
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class CouncilQueryResponse(BaseModel):
    """Response matching frontend expectations exactly"""
    session_id: str
    topic: str
    grade_level: str
    consciousness_level: int = 3
    degraded_mode: bool = False
    council_responses: Dict[str, ArchetypeResponse]
    synthesis: Optional[str] = None
    next_steps: List[str] = []
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# =============================================================================
# OLLAMA CLIENT WITH GRACEFUL DEGRADATION
# =============================================================================

class OllamaEducationalClient:
    """Enhanced Ollama client with graceful degradation"""
    
    def __init__(self):
        self.ollama_available = OLLAMA_AVAILABLE
        self.primary_model = GEMMA_PRIMARY_MODEL
        self.lightweight_model = GEMMA_LIGHTWEIGHT_MODEL
        self.logger = structlog.get_logger()
        
        if self.ollama_available:
            try:
                self.client = ollama.Client(host=OLLAMA_HOST)
                # Test connection
                self.client.list()
                self.logger.info("Ollama client initialized successfully")
            except Exception as e:
                self.ollama_available = False
                self.logger.warning("Ollama unavailable, using fallback mode", error=str(e))
        else:
            self.logger.warning("Ollama package not installed, using fallback mode")
        
    async def generate_archetype_response(
        self, 
        archetype: str, 
        prompt: str, 
        context: str = "",
        stream: bool = False
    ) -> str:
        """Generate response from specific educational archetype with fallback"""
        
        archetype_config = EDUCATIONAL_ARCHETYPES.get(archetype)
        if not archetype_config:
            return f"Unknown archetype: {archetype}"
        
        if self.ollama_available:
            try:
                return await self._generate_ollama_response(archetype_config, prompt, context)
            except Exception as e:
                self.logger.warning("Ollama generation failed, using fallback", 
                                  archetype=archetype, error=str(e))
                return self._generate_fallback_response(archetype_config, prompt, context)
        else:
            return self._generate_fallback_response(archetype_config, prompt, context)
    
    async def _generate_ollama_response(self, archetype_config: Dict, prompt: str, context: str) -> str:
        """Generate response using Ollama"""
        system_prompt = archetype_config["system_prompt"]
        
        full_prompt = f"""Context: {context}

Student Question/Topic: {prompt}

Please respond as the {archetype_config['name']} archetype, following your role as {archetype_config['role']}.

Your approach: {archetype_config['approach']}

Provide a helpful educational response that embodies your teaching personality."""

        response = await asyncio.to_thread(
            self.client.generate,
            model=self.primary_model,
            system=system_prompt,
            prompt=full_prompt,
            options={
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 800
            }
        )
        return response.get('response', 'Unable to generate response.')
    
    def _generate_fallback_response(self, archetype_config: Dict, prompt: str, context: str) -> str:
        """Generate fallback response when Ollama unavailable"""
        responses = {
            "socratic": f"What interesting questions does '{prompt}' raise for you? How might you approach this topic by first asking yourself what you already know about it?",
            "constructivist": f"For '{prompt}', I'd suggest starting with a hands-on activity. What could you build, create, or experiment with to explore this concept?",
            "storyteller": f"Let me tell you about '{prompt}' through a story... Once upon a time, there was a curious learner just like you who wanted to understand this concept...",
            "synthesizer": f"Looking at '{prompt}', I can see connections to several other important concepts. Let's explore how these ideas relate to what you already know...",
            "challenger": f"Before we accept the traditional explanation of '{prompt}', let's challenge some assumptions. What if we looked at this from a completely different perspective?",
            "mentor": f"I believe you have the ability to understand '{prompt}' well. Let's take this step by step, building on your existing knowledge and strengths...",
            "analyst": f"Let's break down '{prompt}' systematically. First, let's identify the key components, then analyze each part methodically..."
        }
        
        base_response = responses.get(
            archetype_config.get("personality", "mentor"),
            f"As your {archetype_config['name']}, I'd approach '{prompt}' by focusing on {archetype_config['focus'].lower()}."
        )
        
        return f"{base_response}\n\n(Note: This is a demonstration response. Full AI capabilities require Ollama and Gemma 3 model installation.)"

class EducationalCouncil:
    """Main educational AI council orchestrator with proper frontend alignment"""
    
    def __init__(self):
        self.ollama_client = OllamaEducationalClient()
        self.active_sessions: Dict[str, Dict] = {}
        self.logger = structlog.get_logger()
    
    async def process_educational_query(
        self, 
        request: EducationalQueryRequest
    ) -> CouncilQueryResponse:
        """Process educational query - ALIGNED WITH FRONTEND EXPECTATIONS"""
        
        session_id = request.session_id or str(uuid.uuid4())
        
        # Use selected archetypes from frontend
        selected_archetypes = request.selected_archetypes or ["socratic", "constructivist", "synthesizer", "mentor"]
        
        # Build context
        context = self._build_educational_context(request)
        
        self.logger.info("Processing educational query", 
                        session_id=session_id, 
                        topic=request.topic,
                        archetypes=selected_archetypes)
        
        # Generate responses from each archetype in parallel
        archetype_tasks = [
            self.ollama_client.generate_archetype_response(
                archetype, request.topic, context
            )
            for archetype in selected_archetypes
        ]
        
        archetype_responses_raw = await asyncio.gather(*archetype_tasks, return_exceptions=True)
        
        # Process archetype responses into frontend-expected format
        council_responses = {}
        for i, archetype in enumerate(selected_archetypes):
            response_text = archetype_responses_raw[i]
            if isinstance(response_text, Exception):
                response_text = f"I apologize, but I'm having trouble responding as the {EDUCATIONAL_ARCHETYPES[archetype]['name']} right now."
                success = False
            else:
                success = True
            
            archetype_config = EDUCATIONAL_ARCHETYPES[archetype]
            council_responses[archetype] = ArchetypeResponse(
                archetype=archetype,
                name=archetype_config["name"],
                success=success,
                response=response_text,
                archetype_role=archetype_config["role"],
                teaching_focus=archetype_config["focus"],
                instance="primary",
                confidence=0.85 if success else 0.3
            )
        
        # Generate synthesis
        synthesis = await self._generate_synthesis(request, council_responses)
        
        # Generate next steps
        next_steps = self._generate_next_steps(request, selected_archetypes)
        
        # Create response in exact format frontend expects
        response = CouncilQueryResponse(
            session_id=session_id,
            topic=request.topic,
            grade_level=request.grade_level,
            consciousness_level=3,
            degraded_mode=not self.ollama_client.ollama_available,
            council_responses={k: v for k, v in council_responses.items()},
            synthesis=synthesis,
            next_steps=next_steps
        )
        
        # Store session
        self.active_sessions[session_id] = {
            "request": request.dict(),
            "response": response.dict(),
            "created_at": datetime.utcnow()
        }
        
        return response
    
    def _build_educational_context(self, request: EducationalQueryRequest) -> str:
        """Build context for AI models"""
        context_parts = [f"Grade Level: {request.grade_level}"]
        
        if request.context:
            context_parts.append(f"Context: {request.context}")
        
        return " | ".join(context_parts)
    
    async def _generate_synthesis(
        self, 
        request: EducationalQueryRequest, 
        council_responses: Dict[str, ArchetypeResponse]
    ) -> str:
        """Generate synthesis of council responses"""
        
        if self.ollama_client.ollama_available:
            try:
                # Build synthesis prompt
                synthesis_prompt = f"""Topic: {request.topic}
Grade Level: {request.grade_level}

The SIRAJ Educational Council has provided the following perspectives:

"""
                
                for archetype, response in council_responses.items():
                    if response.success:
                        archetype_config = EDUCATIONAL_ARCHETYPES[archetype]
                        synthesis_prompt += f"""
{archetype_config['emoji']} {archetype_config['name']}: {response.response}

"""
                
                synthesis_prompt += """
As the Council Synthesizer, please integrate these diverse teaching perspectives into a unified response that:
1. Combines the best insights from each approach
2. Provides clear, actionable guidance
3. Respects different learning styles
4. Offers a coherent path forward

Create a synthesis that honors all perspectives while providing clear educational guidance."""

                synthesis_response = await asyncio.to_thread(
                    self.ollama_client.client.generate,
                    model=self.ollama_client.primary_model,
                    prompt=synthesis_prompt,
                    options={"temperature": 0.6, "top_p": 0.8}
                )
                return synthesis_response.get('response', 'Unable to generate synthesis at this time.')
            except Exception as e:
                self.logger.error("Error generating synthesis", error=str(e))
        
        # Fallback synthesis
        return f"The Educational Council has explored '{request.topic}' from {len(council_responses)} different teaching perspectives. Each archetype offers unique insights that can help deepen understanding through various learning approaches. Review each response to gain a comprehensive understanding from multiple educational methodologies."
    
    def _generate_next_steps(
        self, 
        request: EducationalQueryRequest, 
        selected_archetypes: List[str]
    ) -> List[str]:
        """Generate suggested next steps"""
        
        steps = [
            f"Review the {len(selected_archetypes)} different teaching perspectives provided",
            "Choose the approach that resonates most with your learning style"
        ]
        
        if "constructivist" in selected_archetypes:
            steps.append("Try the hands-on activities suggested by the Constructivist")
        if "socratic" in selected_archetypes:
            steps.append("Reflect on the questions posed by the Socratic teacher")
        if "storyteller" in selected_archetypes:
            steps.append("Consider the stories and examples shared by the Storyteller")
        
        steps.append("Practice applying what you've learned to new situations")
        
        return steps

# =============================================================================
# APPLICATION SETUP
# =============================================================================

# Global instances
educational_council = EducationalCouncil()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting SIRAJ Educational AI Backend", version=SIRAJ_VERSION)
    
    # Verify Ollama connection if available
    if OLLAMA_AVAILABLE:
        try:
            ollama_client = ollama.Client(host=OLLAMA_HOST)
            models = ollama_client.list()
            logger.info("Connected to Ollama", models=len(models.get('models', [])))
        except Exception as e:
            logger.warning("Ollama connection issue", error=str(e))
    else:
        logger.info("Ollama not available, using fallback mode")
    
    yield
    
    logger.info("Shutting down SIRAJ Educational AI Backend")

# Create FastAPI application
app = FastAPI(
    title="SIRAJ Educational AI Backend",
    description="Multi-perspective AI tutoring system - Backend API",
    version=SIRAJ_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# API ENDPOINTS - ALIGNED WITH FRONTEND
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "name": "SIRAJ Educational AI Backend",
        "version": SIRAJ_VERSION,
        "description": "Multi-perspective AI tutoring system backend",
        "status": "operational",
        "council_size": TEACHING_COUNCIL_SIZE,
        "archetypes": list(EDUCATIONAL_ARCHETYPES.keys()),
        "ollama_available": educational_council.ollama_client.ollama_available
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check Ollama connection if available
        ollama_connected = False
        available_models = 0
        
        if OLLAMA_AVAILABLE and educational_council.ollama_client.ollama_available:
            try:
                ollama_client = ollama.Client(host=OLLAMA_HOST)
                models = ollama_client.list()
                ollama_connected = True
                available_models = len(models.get('models', []))
            except Exception as e:
                logger.warning("Ollama health check failed", error=str(e))
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": SIRAJ_VERSION,
            "ollama_connected": ollama_connected,
            "available_models": available_models,
            "active_sessions": len(educational_council.active_sessions),
            "fallback_mode": not educational_council.ollama_client.ollama_available
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy", 
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )

@app.get("/council/archetypes")
async def get_archetypes():
    """Get information about available educational archetypes"""
    return {
        "archetypes": EDUCATIONAL_ARCHETYPES,
        "count": len(EDUCATIONAL_ARCHETYPES)
    }

@app.get("/council/status")
async def get_council_status():
    """Get current status of the educational council"""
    return {
        "status": "operational",
        "active_sessions": len(educational_council.active_sessions),
        "max_sessions": MAX_CONCURRENT_SESSIONS,
        "available_archetypes": list(EDUCATIONAL_ARCHETYPES.keys()),
        "primary_model": GEMMA_PRIMARY_MODEL,
        "lightweight_model": GEMMA_LIGHTWEIGHT_MODEL,
        "ollama_available": educational_council.ollama_client.ollama_available
    }

# FIXED ENDPOINT - Matches frontend expectations exactly
@app.post("/api/education/query")
async def process_educational_query(request: dict):
    """Process educational query through AI council - FRONTEND ALIGNED"""
    try:
        # Convert raw dict to Pydantic model
        query_request = EducationalQueryRequest(
            topic=request.get("topic", ""),
            grade_level=request.get("grade_level", "middle"),
            selected_archetypes=request.get("selected_archetypes", ["socratic", "mentor"]),
            context=request.get("context"),
            session_id=request.get("session_id")
        )
        
        response = await educational_council.process_educational_query(query_request)
        return response.dict()
    except Exception as e:
        logger.error("Error processing educational query", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

# Keep backward compatibility
@app.post("/api/education/process")
async def process_educational_request_legacy(request: dict):
    """Legacy endpoint for backward compatibility"""
    try:
        # Convert legacy format to new format
        query_request = EducationalQueryRequest(
            topic=request.get("topic", ""),
            grade_level=request.get("grade_level", "middle"),
            selected_archetypes=request.get("selected_archetypes", ["socratic", "constructivist", "synthesizer", "mentor"]),
            context=request.get("context"),
            session_id=request.get("session_id")
        )
        
        response = await educational_council.process_educational_query(query_request)
        return response.dict()
    except Exception as e:
        logger.error("Error processing legacy educational request", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/education/session/{session_id}")
async def get_session(session_id: str):
    """Get session information"""
    if session_id in educational_council.active_sessions:
        return educational_council.active_sessions[session_id]
    else:
        raise HTTPException(status_code=404, detail="Session not found")

@app.delete("/api/education/session/{session_id}")
async def delete_session(session_id: str):
    """Delete session"""
    if session_id in educational_council.active_sessions:
        del educational_council.active_sessions[session_id]
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")

# =============================================================================
# MAIN APPLICATION RUNNER
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        workers=1  # Single worker for development; increase for production
    )
