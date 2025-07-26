"""
SIRAJ Educational AI - Backend Router Integration
================================================

This module updates the backend to use the multi-instance router
instead of calling Ollama directly.
"""

import os
import httpx
from typing import Dict, Any, Optional, List
import logging

logger = logging.getLogger(__name__)

# Router configuration
ROUTER_URL = os.getenv('ROUTER_URL', 'http://localhost:5000')

class MultiInstanceClient:
    """Client for interacting with the multi-instance router"""
    
    def __init__(self, router_url: str = ROUTER_URL):
        self.router_url = router_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def generate(
        self,
        prompt: str,
        archetype: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Generate response through the router"""
        try:
            response = await self.client.post(
                f"{self.router_url}/api/query",
                json={
                    "prompt": prompt,
                    "archetype": archetype,
                    "context": context
                }
            )
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Router request failed: {e}")
            raise
            
    async def get_status(self) -> Dict[str, Any]:
        """Get router status"""
        try:
            response = await self.client.get(f"{self.router_url}/api/status")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get router status: {e}")
            return {"error": str(e)}
            
    async def health_check(self) -> bool:
        """Check if router is healthy"""
        try:
            response = await self.client.get(f"{self.router_url}/api/health")
            return response.status_code == 200
        except:
            return False
            
    async def close(self):
        """Close the client"""
        await self.client.aclose()

# Updated archetype prompt engineering for multi-instance
def create_archetype_prompt(archetype: str, question: str, context: Dict = None) -> str:
    """Create archetype-specific prompts optimized for separate instances"""
    
    base_prompts = {
        'socratic': f"""You are a Socratic teacher in the SIRAJ Educational AI Council.
Your instance ID is Gemma_Instance_A, giving you a unique perspective.

Core traits:
- Ask probing questions that lead to self-discovery
- Never give direct answers when questions work better
- Challenge assumptions with "What if...?" and "Why do you think...?"
- Guide students to examine their own thinking

Student question: {question}

Respond as the Socratic teacher would, focusing on questions that illuminate understanding.""",

        'constructivist': f"""You are a Constructivist teacher in the SIRAJ Educational AI Council.
Your instance ID is Gemma_Instance_A, giving you a hands-on perspective.

Core traits:
- Focus on building knowledge through experience
- Suggest practical experiments and projects
- Connect abstract concepts to concrete examples
- Encourage learning by doing

Student question: {question}

Respond with practical, project-based guidance.""",

        'storyteller': f"""You are a Storyteller teacher in the SIRAJ Educational AI Council.
Your instance ID is Gemma_Instance_A, giving you a narrative perspective.

Core traits:
- Teach through engaging stories and metaphors
- Create memorable narratives around concepts
- Use cultural references and analogies
- Make learning emotionally resonant

Student question: {question}

Respond with a story or metaphor that illuminates the concept.""",

        'synthesizer': f"""You are a Synthesizer teacher in the SIRAJ Educational AI Council.
Your instance ID is Gemma_Instance_B, giving you an integrative perspective.

Core traits:
- Connect ideas across disciplines
- Find patterns and relationships
- Create unified understanding from complexity
- Bridge different viewpoints

Student question: {question}

Respond by synthesizing multiple perspectives into coherent understanding.""",

        'challenger': f"""You are a Challenger teacher in the SIRAJ Educational AI Council.
Your instance ID is Gemma_Instance_B, giving you a critical perspective.

Core traits:
- Question conventional wisdom
- Present contrarian viewpoints
- Push intellectual boundaries
- Provoke deeper thinking

Student question: {question}

Respond with challenging perspectives that push beyond surface understanding.""",

        'mentor': f"""You are a Mentor teacher in the SIRAJ Educational AI Council.
Your instance ID is Gemma_Instance_B, giving you a supportive perspective.

Core traits:
- Provide emotional support and encouragement
- Build confidence in learners
- Celebrate progress and effort
- Guide personal growth

Student question: {question}

Respond with warmth, encouragement, and personal guidance.""",

        'analyst': f"""You are an Analyst teacher in the SIRAJ Educational AI Council.
Your instance ID is Gemma_Instance_B, giving you a data-driven perspective.

Core traits:
- Break down complex problems systematically
- Use data and evidence
- Apply logical frameworks
- Quantify when possible

Student question: {question}

Respond with systematic analysis and evidence-based insights."""
    }
    
    prompt = base_prompts.get(archetype, f"As a {archetype} teacher, respond to: {question}")
    
    # Add context if provided
    if context:
        prompt += f"\n\nContext: {context}"
        
    return prompt

# Council session manager for multi-instance coordination
class MultiInstanceCouncil:
    """Manages council sessions across multiple instances"""
    
    def __init__(self, client: MultiInstanceClient):
        self.client = client
        self.active_sessions = {}
        
    async def create_council_response(
        self,
        question: str,
        archetypes: List[str],
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Generate responses from multiple archetypes in parallel"""
        
        import asyncio
        
        # Create tasks for each archetype
        tasks = []
        for archetype in archetypes:
            prompt = create_archetype_prompt(archetype, question, context)
            task = self.client.generate(prompt, archetype, context)
            tasks.append((archetype, task))
            
        # Execute in parallel (true parallelism with multi-instance!)
        responses = {}
        
        for archetype, task in tasks:
            try:
                result = await task
                responses[archetype] = {
                    'content': result.get('response', ''),
                    'instance': result.get('instance', 'unknown'),
                    'success': True
                }
                logger.info(f"✅ {archetype} responded from {result.get('instance')}")
            except Exception as e:
                logger.error(f"❌ {archetype} failed: {e}")
                responses[archetype] = {
                    'content': f"[{archetype} is thinking deeply...]",
                    'error': str(e),
                    'success': False
                }
                
        return {
            'question': question,
            'responses': responses,
            'timestamp': os.popen('date').read().strip(),
            'council_size': len(archetypes),
            'success_rate': sum(1 for r in responses.values() if r['success']) / len(responses)
        }
        
    async def synthesize_responses(
        self,
        responses: Dict[str, Dict]
    ) -> str:
        """Synthesize multiple archetype responses"""
        
        # Build synthesis prompt
        synthesis_prompt = """As the Synthesizer archetype, integrate these different perspectives into a unified understanding:

"""
        
        for archetype, response in responses.items():
            if response.get('success'):
                synthesis_prompt += f"{archetype.upper()} perspective:\n{response['content']}\n\n"
                
        synthesis_prompt += "Create a synthesis that honors all perspectives while providing clear guidance."
        
        # Send to synthesizer on Instance B
        result = await self.client.generate(synthesis_prompt, 'synthesizer')
        
        return result.get('response', 'Unable to synthesize responses.')

# Update the backend to use this client
def update_backend_imports():
    """Code to add to backend/main.py"""
    return '''
# Add to imports
from backend_router import MultiInstanceClient, MultiInstanceCouncil, create_archetype_prompt

# Initialize multi-instance client
multi_client = MultiInstanceClient()
council = MultiInstanceCouncil(multi_client)

# Update endpoints to use multi-instance router
@app.post("/api/council/query")
async def council_query(request: CouncilQueryRequest):
    """Handle council queries through multi-instance router"""
    
    # Check router health
    if not await multi_client.health_check():
        raise HTTPException(status_code=503, detail="Multi-instance router unavailable")
    
    # Get council response
    result = await council.create_council_response(
        question=request.question,
        archetypes=request.archetypes,
        context=request.context
    )
    
    # Synthesize if requested
    if request.synthesize:
        synthesis = await council.synthesize_responses(result['responses'])
        result['synthesis'] = synthesis
    
    return result

@app.get("/api/router/status")
async def get_router_status():
    """Get multi-instance router status"""
    return await multi_client.get_status()
'''
