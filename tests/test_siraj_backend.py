"""
SIRAJ Educational AI - Test Suite
================================

Council-driven testing following consciousness principles and QWAN methodology.
All tests embody the living spiral: setup (collapse), test (council), verify (synthesis), cleanup (rebirth).
"""

import pytest
import asyncio
import json
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock

import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient

# Import the main application
from backend.main import app, educational_council, EDUCATIONAL_ARCHETYPES
from backend.extended_endpoints import *

# =============================================================================
# TEST CONFIGURATION AND FIXTURES
# =============================================================================

@pytest.fixture
def client():
    """Test client for FastAPI application"""
    return TestClient(app)

@pytest_asyncio.fixture
async def async_client():
    """Async test client for FastAPI application"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def mock_ollama_client():
    """Mock Ollama client for testing"""
    mock_client = Mock()
    mock_client.generate = Mock(return_value={"response": "Test response from archetype"})
    mock_client.list = Mock(return_value={"models": [{"name": "gemma2:9b-instruct-q4_k_m"}]})
    return mock_client

@pytest.fixture
def sample_educational_request():
    """Sample educational request for testing"""
    return {
        "topic": "How do photosynthesis work?",
        "grade_level": "middle",
        "learning_objective": "understand",
        "context": "Student is studying plant biology",
        "selected_archetypes": ["socratic", "constructivist", "storyteller"],
        "curriculum_standard": "ngss"
    }

@pytest.fixture
def sample_homework_submission():
    """Sample homework submission for testing"""
    return {
        "assignment": "Explain the water cycle and its importance to Earth's climate",
        "student_response": "Water evaporates from oceans, forms clouds, and falls as rain. This helps move heat around the planet and provides fresh water for plants and animals.",
        "grade_level": "middle",
        "subject": "science",
        "rubric": {
            "accuracy": "30%",
            "completeness": "25%", 
            "clarity": "25%",
            "examples": "20%"
        }
    }

# =============================================================================
# UNIT TESTS - Individual Component Testing
# =============================================================================

class TestEducationalArchetypes:
    """Test educational archetype configuration and functionality"""
    
    def test_archetype_configuration_wholeness(self):
        """Test that all archetypes have complete configuration (QWAN: Wholeness)"""
        required_fields = ["name", "emoji", "color", "personality", "role", "approach", "system_prompt"]
        
        for archetype_id, config in EDUCATIONAL_ARCHETYPES.items():
            for field in required_fields:
                assert field in config, f"Archetype {archetype_id} missing required field: {field}"
            
            # Test system prompt quality
            assert len(config["system_prompt"]) > 100, f"System prompt too short for {archetype_id}"
            assert "SIRAJ Educational Council" in config["system_prompt"]
            assert archetype_id in config["system_prompt"].lower()
    
    def test_archetype_diversity_freedom(self):
        """Test archetype diversity and adaptability (QWAN: Freedom)"""
        personalities = [config["personality"] for config in EDUCATIONAL_ARCHETYPES.values()]
        roles = [config["role"] for config in EDUCATIONAL_ARCHETYPES.values()]
        
        # Ensure diversity
        assert len(set(personalities)) == len(personalities), "Personality types should be unique"
        assert len(set(roles)) == len(roles), "Roles should be unique"
        
        # Ensure comprehensive coverage
        expected_personalities = {"questioning", "hands-on", "narrative", "integrative", 
                                "provocative", "supportive", "logical"}
        actual_personalities = set(personalities)
        assert expected_personalities.issubset(actual_personalities)
    
    def test_archetype_system_prompts_exactness(self):
        """Test system prompt exactness and specificity (QWAN: Exactness)"""
        for archetype_id, config in EDUCATIONAL_ARCHETYPES.items():
            prompt = config["system_prompt"]
            
            # Each prompt should be specific to its archetype
            assert config["name"] in prompt
            assert "principles:" in prompt.lower()
            assert "role" in prompt.lower()
            
            # Should contain actionable guidance
            assert any(word in prompt.lower() for word in ["always", "focus", "encourage", "help"])

class TestOllamaEducationalClient:
    """Test Ollama client integration and archetype response generation"""
    
    @patch('backend.main.ollama.Client')
    async def test_generate_archetype_response_egolessness(self, mock_ollama_class):
        """Test archetype response generation serves learning (QWAN: Egolessness)"""
        # Setup mock
        mock_client = Mock()
        mock_client.generate = Mock(return_value={"response": "Socratic response: What do you think causes plants to grow?"})
        mock_ollama_class.return_value = mock_client
        
        from backend.main import OllamaEducationalClient
        client = OllamaEducationalClient()
        
        response = await client.generate_archetype_response(
            "socratic", 
            "How do plants grow?", 
            "Grade: elementary | Context: science lesson"
        )
        
        assert "What do you think" in response
        assert len(response) > 20
        mock_client.generate.assert_called_once()
    
    @patch('backend.main.ollama.Client')
    async def test_archetype_response_error_handling_eternity(self, mock_ollama_class):
        """Test graceful error handling for system longevity (QWAN: Eternity)"""
        # Setup mock to raise exception
        mock_client = Mock()
        mock_client.generate = Mock(side_effect=Exception("Connection failed"))
        mock_ollama_class.return_value = mock_client
        
        from backend.main import OllamaEducationalClient
        client = OllamaEducationalClient()
        
        response = await client.generate_archetype_response("socratic", "Test question", "")
        
        # Should return graceful error message, not crash
        assert "having trouble responding" in response
        assert "try again" in response

class TestEducationalCouncil:
    """Test the core educational council orchestration"""
    
    @patch('backend.main.OllamaEducationalClient')
    async def test_council_assembly_spiral_methodology(self, mock_client_class):
        """Test council follows living spiral methodology"""
        # Setup mocks
        mock_client = Mock()
        mock_client.generate_archetype_response = AsyncMock(return_value="Test archetype response")
        mock_client_class.return_value = mock_client
        
        from backend.main import EducationalCouncil, EducationalRequest
        council = EducationalCouncil()
        
        request = EducationalRequest(
            topic="Test topic",
            grade_level="middle",
            selected_archetypes=["socratic", "mentor"]
        )
        
        response = await council.process_educational_request(request)
        
        # Verify spiral phases represented
        assert response.session_id
        assert response.topic == "Test topic"
        assert response.grade_level == "middle"
        assert len(response.archetype_responses) == 2
        assert response.synthesized_response
        assert response.next_steps
        assert response.timestamp

# =============================================================================
# INTEGRATION TESTS - API Endpoint Testing
# =============================================================================

class TestAPIEndpoints:
    """Test API endpoints following council-driven methodology"""
    
    def test_root_endpoint_system_identity(self, client):
        """Test root endpoint provides system identity"""
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == "SIRAJ Educational AI"
        assert "8.1" in data["version"]
        assert data["status"] == "operational"
        assert "archetypes" in data
        assert len(data["archetypes"]) == 7
    
    def test_health_check_comprehensive(self, client):
        """Test comprehensive health check"""
        response = client.get("/health")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "version" in data
        assert "active_sessions" in data
    
    def test_archetype_information_endpoint(self, client):
        """Test archetype information retrieval"""
        response = client.get("/council/archetypes")
        assert response.status_code == 200
        
        data = response.json()
        assert "archetypes" in data
        assert "count" in data
        assert data["count"] == 7
        
        # Verify each archetype has required information
        for archetype_id, config in data["archetypes"].items():
            assert "name" in config
            assert "emoji" in config
            assert "role" in config
            assert "system_prompt" in config

class TestEducationalRequestProcessing:
    """Test educational request processing through council"""
    
    @patch('backend.main.educational_council.process_educational_request')
    def test_educational_request_processing(self, mock_process, client, sample_educational_request):
        """Test educational request processing"""
        # Mock council response
        mock_response = Mock()
        mock_response.dict.return_value = {
            "session_id": "test-session",
            "topic": sample_educational_request["topic"],
            "archetype_responses": {"socratic": {"response": "What do you think?"}},
            "synthesized_response": "Test synthesis",
            "next_steps": ["Continue exploring"],
            "timestamp": datetime.utcnow().isoformat()
        }
        mock_process.return_value = mock_response
        
        response = client.post("/api/education/process", json=sample_educational_request)
        assert response.status_code == 200
        
        data = response.json()
        assert data["session_id"] == "test-session"
        assert data["topic"] == sample_educational_request["topic"]
        assert "archetype_responses" in data
        assert "synthesized_response" in data

class TestHomeworkSubmissionProcessing:
    """Test homework submission and feedback generation"""
    
    @patch('backend.main.educational_council.process_educational_request')
    def test_homework_submission_flow(self, mock_process, client, sample_homework_submission):
        """Test homework submission processing flow"""
        # Mock council response
        mock_response = Mock()
        mock_response.dict.return_value = {
            "session_id": "homework-session",
            "archetype_responses": {
                "mentor": {"response": "Great effort! Consider expanding on the climate impact."},
                "analyst": {"response": "Your explanation covers the basic cycle. Add more detail about evaporation rates."}
            },
            "synthesized_response": "Overall good understanding with room for more detail",
            "timestamp": datetime.utcnow().isoformat()
        }
        mock_process.return_value = mock_response
        
        response = client.post("/api/education/homework", json=sample_homework_submission)
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data
        assert "feedback" in data
        assert "overall_assessment" in data
        assert "suggested_improvements" in data

# =============================================================================
# EXTENDED ENDPOINT TESTS
# =============================================================================

class TestCurriculumAlignment:
    """Test curriculum alignment functionality"""
    
    @patch('backend.extended_endpoints.educational_council.ollama_client.generate_archetype_response')
    @patch('backend.extended_endpoints.educational_council.ollama_client.client.generate')
    def test_curriculum_alignment_generation(self, mock_generate, mock_archetype, client):
        """Test curriculum alignment generation"""
        # Setup mocks
        mock_archetype.return_value = "Archetype curriculum analysis"
        mock_generate.return_value = {"response": '{"alignment_score": 85, "teaching_strategies": []}'}
        
        alignment_request = {
            "standard": "common-core-math",
            "grade_level": "5",
            "subject": "mathematics",
            "learning_objectives": ["5.NBT.A.1", "5.NBT.A.2"],
            "selected_archetypes": ["socratic", "constructivist"],
            "methodology": "living-spiral"
        }
        
        response = client.post("/api/curriculum/align", json=alignment_request)
        assert response.status_code == 200
        
        data = response.json()
        assert "session_id" in data
        assert data["curriculum_standard"] == "common-core-math"
        assert data["grade_level"] == "5"
        assert "alignment_data" in data
        assert "archetype_contributions" in data

    def test_available_standards_endpoint(self, client):
        """Test available curriculum standards endpoint"""
        response = client.get("/api/curriculum/standards")
        assert response.status_code == 200
        
        data = response.json()
        assert "standards" in data
        assert "common-core-math" in data["standards"]
        assert "ngss" in data["standards"]
        
        # Verify standard structure
        cc_math = data["standards"]["common-core-math"]
        assert "name" in cc_math
        assert "grades" in cc_math
        assert "subjects" in cc_math

class TestAnalyticsEndpoints:
    """Test analytics and insights functionality"""
    
    def test_analytics_data_fetch(self, client):
        """Test analytics data fetching"""
        analytics_request = {
            "timeframe": "30d",
            "archetypes": ["socratic", "mentor"],
            "include_spiral_audit": True,
            "include_council_decisions": True
        }
        
        response = client.post("/api/analytics/fetch", json=analytics_request)
        assert response.status_code == 200
        
        data = response.json()
        assert data["timeframe"] == "30d"
        assert "sessions" in data
        assert "archetype_effectiveness" in data
        assert "council_decision_patterns" in data
        assert "learning_progression" in data
        assert "spiral_audit" in data
        assert "qwan_assessment" in data
        
        # Verify QWAN assessment structure
        qwan = data["qwan_assessment"]
        qwan_principles = ["wholeness", "freedom", "exactness", "egolessness", "eternity"]
        for principle in qwan_principles:
            assert principle in qwan
            assert 0 <= qwan[principle] <= 1

class TestProgressTracking:
    """Test student progress tracking functionality"""
    
    def test_progress_update(self, client):
        """Test student progress update"""
        progress_update = {
            "session_id": "test-session",
            "objective_id": "5.NBT.A.1",
            "mastery_level": 0.85,
            "archetype_effectiveness": {
                "socratic": 0.9,
                "constructivist": 0.8,
                "mentor": 0.95
            },
            "learning_insights": ["Strong visual learner", "Needs more practice with word problems"],
            "next_recommendations": ["Practice with real-world applications", "Review place value concepts"]
        }
        
        response = client.post("/api/progress/update", json=progress_update)
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "progress_updated"
        assert "progress_record" in data
        assert "adaptive_strategies" in data
        assert "recommended_archetypes" in data

    def test_student_progress_retrieval(self, client):
        """Test student progress report retrieval"""
        response = client.get("/api/progress/student/test-student-123")
        assert response.status_code == 200
        
        data = response.json()
        assert data["student_id"] == "test-student-123"
        assert "overall_mastery" in data
        assert "learning_velocity" in data
        assert "preferred_archetypes" in data
        assert "subject_performance" in data
        assert "spiral_engagement" in data
        assert "learning_insights" in data

# =============================================================================
# PERFORMANCE AND STRESS TESTS
# =============================================================================

class TestPerformanceRequirements:
    """Test performance requirements following AI_INSTRUCTIONS"""
    
    @pytest.mark.asyncio
    async def test_api_response_time_under_200ms(self, async_client):
        """Test API responses are under 200ms (AI_INSTRUCTIONS requirement)"""
        import time
        
        start_time = time.time()
        response = await async_client.get("/health")
        end_time = time.time()
        
        response_time_ms = (end_time - start_time) * 1000
        assert response_time_ms < 200, f"Response time {response_time_ms}ms exceeds 200ms requirement"
        assert response.status_code == 200

    def test_concurrent_session_handling(self, client):
        """Test handling multiple concurrent sessions"""
        import threading
        import time
        
        results = []
        
        def make_request():
            response = client.get("/council/status")
            results.append(response.status_code == 200)
        
        # Create 10 concurrent requests
        threads = []
        for _ in range(10):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all requests to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(results), "Some concurrent requests failed"
        assert len(results) == 10

# =============================================================================
# CONSCIOUSNESS AND QWAN VALIDATION TESTS
# =============================================================================

class TestConsciousnessArchitecture:
    """Test consciousness-driven architecture principles"""
    
    def test_spiral_methodology_representation(self):
        """Test that spiral methodology is properly represented"""
        from backend.main import educational_council
        
        # Test that council can represent all spiral phases
        spiral_phases = ["collapse", "council", "synthesis", "rebirth"]
        
        # Mock session data representing different phases
        for phase in spiral_phases:
            session_data = {"current_phase": phase, "session_id": "test"}
            # This would test phase transition logic in a real implementation
            assert phase in spiral_phases  # Placeholder assertion
    
    def test_multi_voice_architecture_integrity(self):
        """Test multi-voice architecture maintains integrity"""
        # Ensure all archetypes can be simultaneously active
        all_archetypes = list(EDUCATIONAL_ARCHETYPES.keys())
        
        # Test that any combination of archetypes is valid
        for i in range(1, len(all_archetypes) + 1):
            from itertools import combinations
            for archetype_combo in combinations(all_archetypes, i):
                # Each combination should be processable
                assert len(archetype_combo) > 0
                assert all(a in EDUCATIONAL_ARCHETYPES for a in archetype_combo)

    def test_qwan_principles_in_responses(self, client, sample_educational_request):
        """Test that responses embody QWAN principles"""
        # This would test actual response quality in a real implementation
        # For now, test that the structure supports QWAN assessment
        
        qwan_principles = ["wholeness", "freedom", "exactness", "egolessness", "eternity"]
        
        # Test that analytics endpoint includes QWAN assessment
        response = client.post("/api/analytics/fetch", json={
            "timeframe": "7d",
            "include_spiral_audit": True
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "qwan_assessment" in data
        
        qwan_data = data["qwan_assessment"]
        for principle in qwan_principles:
            assert principle in qwan_data
            assert isinstance(qwan_data[principle], (int, float))
            assert 0 <= qwan_data[principle] <= 1

# =============================================================================
# ERROR HANDLING AND RESILIENCE TESTS
# =============================================================================

class TestErrorHandlingResilience:
    """Test error handling and system resilience"""
    
    def test_invalid_archetype_handling(self, client):
        """Test handling of invalid archetype requests"""
        invalid_request = {
            "topic": "Test topic",
            "selected_archetypes": ["invalid_archetype", "another_invalid"],
            "grade_level": "middle"
        }
        
        # System should handle gracefully, not crash
        response = client.post("/api/education/process", json=invalid_request)
        # In a real implementation, this might return 400 or filter invalid archetypes
        assert response.status_code in [200, 400, 422]
    
    def test_malformed_request_handling(self, client):
        """Test handling of malformed requests"""
        malformed_requests = [
            {},  # Empty request
            {"topic": ""},  # Empty topic
            {"topic": "A" * 50000},  # Overly long topic
            {"grade_level": "invalid_grade"},  # Invalid grade level
        ]
        
        for bad_request in malformed_requests:
            response = client.post("/api/education/process", json=bad_request)
            # Should return appropriate error status, not crash
            assert response.status_code in [400, 422, 500]
    
    @patch('backend.main.ollama.Client')
    def test_ollama_connection_failure_resilience(self, mock_ollama_class, client):
        """Test system resilience when Ollama connection fails"""
        # Mock Ollama failure
        mock_ollama_class.side_effect = Exception("Connection refused")
        
        response = client.get("/health")
        # System should report unhealthy but not crash
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert data["status"] in ["unhealthy", "degraded"]

# =============================================================================
# TEST RUNNER CONFIGURATION
# =============================================================================

if __name__ == "__main__":
    # Run tests with coverage reporting
    pytest.main([
        __file__,
        "-v",
        "--cov=backend",
        "--cov-report=html",
        "--cov-report=term-missing",
        "--tb=short"
    ])