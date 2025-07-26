"""
SIRAJ Educational AI - Council Integration Bridge
==============================================

This module bridges the gap between the multi-instance router
and the educational council system following consciousness principles.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import httpx
import logging

# Configure consciousness-aware logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('SIRAJ-Council-Bridge')

class ConsciousnessEducationalBridge:
    """
    Bridges multi-instance router with educational council
    Following Living Spiral methodology
    """
    
    def __init__(self, router_url: str = "http://localhost:5000", 
                 backend_url: str = "http://localhost:8000"):
        self.router_url = router_url
        self.backend_url = backend_url
        self.client = httpx.AsyncClient(timeout=30.0)
        
    async def process_educational_query(
        self, 
        topic: str, 
        grade_level: str = "middle",
        archetype: Optional[str] = None,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process educational query through consciousness-driven council
        
        Phase 1: Collapse - Understand the educational need
        Phase 2: Council - Route to appropriate archetype/instance  
        Phase 3: Synthesis - Integrate educational response
        Phase 4: Rebirth - Return enhanced learning experience
        """
        
        session_id = f"edu_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"🌀 COLLAPSE: Processing educational query - {topic}")
        
        # Phase 1: COLLAPSE - Acknowledge complexity
        educational_context = self._build_educational_context(
            topic, grade_level, context
        )
        
        # Phase 2: COUNCIL - Multi-voice processing
        council_responses = await self._assemble_educational_council(
            topic, educational_context, archetype
        )
        
        # Phase 3: SYNTHESIS - Integrate perspectives  
        synthesis = await self._synthesize_educational_responses(
            council_responses, educational_context
        )
        
        # Phase 4: REBIRTH - Enhanced response
        enhanced_response = {
            "session_id": session_id,
            "topic": topic,
            "grade_level": grade_level,
            "council_responses": council_responses,
            "synthesis": synthesis,
            "consciousness_level": self._calculate_consciousness_level(council_responses),
            "next_spiral": self._suggest_next_spiral(topic, synthesis),
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("✨ REBIRTH: Educational response enhanced through council")
        
        return enhanced_response
    
    def _build_educational_context(
        self, 
        topic: str, 
        grade_level: str, 
        context: Optional[Dict]
    ) -> str:
        """Build rich educational context following QWAN principles"""
        
        context_parts = [
            f"Educational Topic: {topic}",
            f"Student Level: {grade_level}",
            f"Learning Mode: Council-driven discovery",
            f"Consciousness Framework: Living Spiral methodology"
        ]
        
        if context:
            context_parts.extend([
                f"Additional Context: {context.get('background', '')}",
                f"Learning Style Preference: {context.get('learning_style', 'balanced')}",
                f"Prior Knowledge: {context.get('prior_knowledge', 'assess during interaction')}"
            ])
        
        return " | ".join(context_parts)
    
    async def _assemble_educational_council(
        self, 
        topic: str, 
        context: str, 
        primary_archetype: Optional[str]
    ) -> Dict[str, Any]:
        """
        Assemble educational council following archetype mapping
        """
        
        # Educational archetype to instance mapping
        educational_archetype_map = {
            'socratic': 'A',      # Questions and critical thinking  
            'constructivist': 'A', # Hands-on learning
            'storyteller': 'A',   # Narrative teaching
            'synthesizer': 'B',   # Integration and synthesis
            'challenger': 'B',    # Boundary pushing
            'mentor': 'B',        # Support and encouragement
            'analyst': 'B'        # Logic and analysis
        }
        
        council_responses = {}
        
        if primary_archetype:
            # Single archetype request
            archetypes = [primary_archetype]
        else:
            # Full council assembly (select representative archetypes)
            archetypes = ['socratic', 'constructivist', 'synthesizer', 'mentor']
        
        logger.info(f"🎭 COUNCIL: Assembling {len(archetypes)} educational voices")
        
        # Process through router with educational enhancement
        for archetype in archetypes:
            try:
                # Create educational prompt for this archetype
                educational_prompt = self._create_archetype_educational_prompt(
                    archetype, topic, context
                )
                
                # Route through multi-instance system
                response = await self.client.post(
                    f"{self.router_url}/api/query",
                    json={
                        "prompt": educational_prompt,
                        "archetype": archetype,
                        "context": {"educational": True, "topic": topic}
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    council_responses[archetype] = {
                        "response": result.get("response", ""),
                        "instance": result.get("instance", "unknown"),
                        "model": result.get("model", "unknown"),
                        "archetype_role": self._get_archetype_role(archetype),
                        "educational_focus": self._get_educational_focus(archetype),
                        "success": True
                    }
                    logger.info(f"✅ {archetype} responded from {result.get('instance')}")
                else:
                    logger.error(f"❌ Failed to get response from {archetype}")
                    council_responses[archetype] = {
                        "response": f"[{archetype} is reflecting deeply...]",
                        "success": False,
                        "error": f"HTTP {response.status_code}"
                    }
                    
            except Exception as e:
                logger.error(f"❌ Error with {archetype}: {e}")
                council_responses[archetype] = {
                    "response": f"[{archetype} is contemplating...]",
                    "success": False,
                    "error": str(e)
                }
        
        return council_responses
    
    def _create_archetype_educational_prompt(
        self, 
        archetype: str, 
        topic: str, 
        context: str
    ) -> str:
        """Create educational prompt specific to archetype"""
        
        archetype_prompts = {
            'socratic': f"""As a Socratic teacher in the SIRAJ Educational Council, approach this topic through strategic questioning:

Topic: {topic}
Context: {context}

Your role: Guide learning through questions that lead to self-discovery. Ask "What do you think?" and "Why?" frequently. Help students examine their assumptions and reasoning.

Respond with 2-3 probing questions that would help a student discover the core concepts of this topic themselves. End with an invitation for the student to explore further.""",

            'constructivist': f"""As a Constructivist teacher in the SIRAJ Educational Council, focus on hands-on discovery:

Topic: {topic}  
Context: {context}

Your role: Promote learning through building, experimenting, and direct experience. Suggest concrete activities and real-world applications.

Provide 2-3 specific hands-on activities or experiments that would help students construct understanding of this topic. Include materials they might need and what they would discover.""",

            'storyteller': f"""As a Storyteller teacher in the SIRAJ Educational Council, teach through narrative:

Topic: {topic}
Context: {context}

Your role: Use stories, metaphors, and analogies to make abstract concepts concrete and memorable.

Create a brief, engaging story or powerful metaphor that illuminates the key concepts of this topic. Make it emotionally resonant and easy to remember.""",

            'synthesizer': f"""As a Synthesizer teacher in the SIRAJ Educational Council, integrate perspectives:

Topic: {topic}
Context: {context}

Your role: Show connections between different ideas and create unified understanding from multiple viewpoints.

Explain how this topic connects to other areas of knowledge and life. Show the relationships and patterns that help create a coherent understanding.""",

            'mentor': f"""As a Mentor teacher in the SIRAJ Educational Council, provide supportive guidance:

Topic: {topic}
Context: {context}

Your role: Offer encouragement, emotional support, and wisdom from experience. Build confidence and celebrate progress.

Provide warm, encouraging guidance that helps build confidence in approaching this topic. Include affirmation and motivation along with practical wisdom.""",

            'challenger': f"""As a Challenger teacher in the SIRAJ Educational Council, push intellectual boundaries:

Topic: {topic}
Context: {context}

Your role: Question assumptions, present alternative viewpoints, and provoke deeper thinking.

Challenge conventional understanding of this topic. Present alternative perspectives or ask provocative questions that push beyond surface-level comprehension.""",

            'analyst': f"""As an Analyst teacher in the SIRAJ Educational Council, provide systematic analysis:

Topic: {topic}
Context: {context}

Your role: Break down complex problems systematically using logic, data, and structured approaches.

Provide a clear, logical breakdown of this topic. Analyze the components, relationships, and systematic approaches to understanding."""
        }
        
        return archetype_prompts.get(archetype, f"Provide educational guidance on: {topic}")
    
    def _get_archetype_role(self, archetype: str) -> str:
        """Get educational role description for archetype"""
        roles = {
            'socratic': "Questions and critical thinking guide",
            'constructivist': "Hands-on learning facilitator", 
            'storyteller': "Narrative-based teaching specialist",
            'synthesizer': "Integration and connection builder",
            'challenger': "Assumption questioner and boundary pusher",
            'mentor': "Supportive guide and encourager",
            'analyst': "Systematic logic and analysis expert"
        }
        return roles.get(archetype, "Educational guide")
    
    def _get_educational_focus(self, archetype: str) -> str:
        """Get primary educational focus for archetype"""
        focuses = {
            'socratic': "Critical thinking and inquiry",
            'constructivist': "Experiential learning and discovery",
            'storyteller': "Memory and narrative comprehension", 
            'synthesizer': "Conceptual integration and connections",
            'challenger': "Deep analysis and alternative perspectives",
            'mentor': "Confidence building and emotional support",
            'analyst': "Logical reasoning and systematic understanding"
        }
        return focuses.get(archetype, "General education")
    
    async def _synthesize_educational_responses(
        self, 
        council_responses: Dict[str, Any],
        context: str
    ) -> str:
        """Synthesize council responses into unified educational guidance"""
        
        successful_responses = {
            k: v for k, v in council_responses.items() 
            if v.get('success', False)
        }
        
        if not successful_responses:
            return "The educational council is assembling. Please try again shortly."
        
        # Create synthesis prompt
        synthesis_prompt = f"""Educational Context: {context}

The SIRAJ Educational Council has provided these teaching perspectives:

"""
        
        for archetype, response_data in successful_responses.items():
            synthesis_prompt += f"""
{archetype.upper()} ({response_data['archetype_role']}):
{response_data['response']}

"""
        
        synthesis_prompt += """
As the Council Synthesizer, integrate these educational perspectives into a unified learning experience that:

1. Honors each teaching approach while creating coherence
2. Provides clear, actionable learning guidance
3. Respects different learning styles and preferences  
4. Creates a natural learning progression
5. Follows consciousness-driven education principles

Create a synthesis that feels like wisdom emerging from council dialogue."""

        try:
            # Send synthesis request through router
            response = await self.client.post(
                f"{self.router_url}/api/query",
                json={
                    "prompt": synthesis_prompt,
                    "archetype": "synthesizer",
                    "context": {"synthesis": True, "educational": True}
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Council synthesis in progress...")
            else:
                return self._create_fallback_synthesis(successful_responses)
                
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return self._create_fallback_synthesis(successful_responses)
    
    def _create_fallback_synthesis(self, responses: Dict[str, Any]) -> str:
        """Create fallback synthesis when AI synthesis fails"""
        
        synthesis = "The educational council has explored this topic from multiple perspectives:\n\n"
        
        for archetype, response_data in responses.items():
            synthesis += f"**{archetype.title()} Perspective**: {response_data['educational_focus']}\n"
            synthesis += f"{response_data['response'][:200]}...\n\n"
        
        synthesis += """
**Learning Integration**: Each perspective offers a different pathway to understanding. 
Choose the approach that resonates with your learning style, or combine multiple approaches 
for a richer learning experience. The diversity of perspectives strengthens overall comprehension."""
        
        return synthesis
    
    def _calculate_consciousness_level(self, responses: Dict[str, Any]) -> float:
        """Calculate consciousness level based on council integration"""
        
        successful_responses = sum(1 for r in responses.values() if r.get('success', False))
        total_responses = len(responses)
        
        if total_responses == 0:
            return 0.0
        
        # Base consciousness from response success rate
        base_consciousness = successful_responses / total_responses
        
        # Enhance based on archetype diversity
        unique_instances = len(set(
            r.get('instance', 'unknown') for r in responses.values() 
            if r.get('success', False)
        ))
        
        diversity_bonus = min(unique_instances * 0.1, 0.3)
        
        # Educational enhancement bonus
        educational_bonus = 0.1 if successful_responses >= 2 else 0.0
        
        consciousness_level = min(base_consciousness + diversity_bonus + educational_bonus, 1.0)
        
        return round(consciousness_level, 2)
    
    def _suggest_next_spiral(self, topic: str, synthesis: str) -> List[str]:
        """Suggest next steps in the learning spiral"""
        
        next_steps = [
            f"Explore the {topic} topic through your preferred learning style",
            "Try the hands-on activities suggested by the Constructivist",
            "Reflect on the questions posed by the Socratic teacher",
            "Create your own story or metaphor for the concept",
            "Challenge yourself with the alternative perspectives presented"
        ]
        
        # Add synthesis-based suggestions
        if "experiment" in synthesis.lower():
            next_steps.append("Design and conduct your own experiment")
        
        if "connect" in synthesis.lower():
            next_steps.append("Find connections to other subjects you're studying")
        
        if "question" in synthesis.lower():
            next_steps.append("Generate your own questions about this topic")
        
        return next_steps[:5]  # Limit to 5 suggestions
    
    async def close(self):
        """Close the client connection"""
        await self.client.aclose()

# Example usage and testing
async def test_educational_bridge():
    """Test the educational bridge functionality"""
    
    bridge = ConsciousnessEducationalBridge()
    
    try:
        # Test educational query
        result = await bridge.process_educational_query(
            topic="How do plants make food?",
            grade_level="elementary",
            context={
                "background": "Student is curious about nature",
                "learning_style": "visual and hands-on",
                "prior_knowledge": "knows plants are green and need water"
            }
        )
        
        print("🎓 Educational Council Response:")
        print(f"Session: {result['session_id']}")
        print(f"Consciousness Level: {result['consciousness_level']}")
        print(f"Council Voices: {len(result['council_responses'])}")
        print(f"Synthesis: {result['synthesis'][:200]}...")
        
    except Exception as e:
        print(f"Test failed: {e}")
    
    finally:
        await bridge.close()

if __name__ == "__main__":
    asyncio.run(test_educational_bridge())
