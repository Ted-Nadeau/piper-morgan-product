"""
API-Level Degradation Integration Tests
Verification-first methodology: Test that API properly handles QueryRouter degradation responses
"""

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from web.app import app


class TestAPIDegradationIntegration:
    """Test API-level degradation handling and response structure"""

    @pytest.fixture
    def test_client(self):
        """Create test client for API testing with lifespan context"""
        # Use context manager to ensure lifespan events run
        with TestClient(app) as client:
            yield client

    def test_api_handles_database_degradation_gracefully(self, test_client):
        """Test API returns proper structured response when IntentService is unavailable"""

        # Mock IntentService being unavailable (simulates service initialization failure)
        with patch.object(test_client.app.state, "intent_service", None):
            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            # Should return 200 with proper structured response (Pattern-007 graceful degradation)
            assert response.status_code == 200
            data = response.json()

            # Verify IntentResponse structure
            assert "message" in data
            assert "intent" in data
            assert "workflow_id" in data
            assert "requires_clarification" in data
            assert "clarification_type" in data

            # Verify degradation message is user-friendly
            assert "Database temporarily unavailable" in data["message"]
            assert "Docker" in data["message"] or "try again" in data["message"]

    def test_api_handles_circuit_breaker_degradation(self, test_client):
        """Test API handles exceptions during intent processing gracefully"""

        # Mock IntentService.process_intent to throw exception
        async def mock_process_intent_error(*args, **kwargs):
            raise Exception("Circuit breaker open")

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            side_effect=mock_process_intent_error,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            # Should return 200 with degradation response (Pattern-007)
            assert response.status_code == 200
            data = response.json()

            # Verify structured response
            assert "message" in data
            assert "intent" in data
            assert data["intent"]["action"] == "list_projects"
            assert data["intent"]["category"] == "query"

    def test_api_handles_context_validation_errors(self, test_client):
        """Test API properly handles context validation errors"""

        response = test_client.post("/api/v1/intent", json={"message": "Get project details"})

        # Should return 422 for missing context
        assert response.status_code == 422
        data = response.json()

        # Verify error message is helpful
        assert "project_id" in data["detail"].lower()

    def test_api_handles_file_service_degradation(self, test_client):
        """Test API handles file service exceptions gracefully"""

        # Mock IntentService.process_intent to throw file service exception
        async def mock_process_intent_file_error(*args, **kwargs):
            raise Exception("File service unavailable")

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            side_effect=mock_process_intent_file_error,
        ):
            response = test_client.post(
                "/api/v1/intent",
                json={"message": "Read file contents", "context": {"resolved_file_id": "test-id"}},
            )

            # Should return 200 with degradation response (Pattern-007)
            assert response.status_code == 200
            data = response.json()

            # Verify structured response
            assert "message" in data
            assert "intent" in data
            assert data["intent"]["action"] == "read_file_contents"

    def test_api_handles_conversation_service_degradation(self, test_client):
        """Test API handles conversation service exceptions gracefully"""

        # Mock IntentService.process_intent to throw conversation service exception
        async def mock_process_intent_conv_error(*args, **kwargs):
            raise Exception("Conversation service unavailable")

        with patch.object(
            test_client.app.state.intent_service,
            "process_intent",
            side_effect=mock_process_intent_conv_error,
        ):
            response = test_client.post("/api/v1/intent", json={"message": "Hello"})

            # Should return 200 with degradation response (Pattern-007)
            assert response.status_code == 200
            data = response.json()

            # Verify structured response
            assert "message" in data
            assert "intent" in data

    def test_api_maintains_response_structure_consistency(self, test_client):
        """Test API maintains consistent response structure when IntentService unavailable"""

        degradation_scenarios = [
            ("List all projects", "list_projects"),
            ("How many projects do we have?", "count_projects"),
            ("Show me the default project", "get_default_project"),
        ]

        # Test that all scenarios return consistent degradation response structure
        with patch.object(test_client.app.state, "intent_service", None):
            for message, expected_action in degradation_scenarios:
                response = test_client.post("/api/v1/intent", json={"message": message})

                # All should return 200 with consistent structure (Pattern-007)
                assert response.status_code == 200
                data = response.json()

                # Verify consistent IntentResponse structure
                assert "message" in data
                assert "intent" in data
                assert "workflow_id" in data
                assert "requires_clarification" in data
                assert "clarification_type" in data

                # Verify intent structure
                assert data["intent"]["action"] == expected_action
                assert data["intent"]["category"] == "query"
                assert "confidence" in data["intent"]
                assert "context" in data["intent"]

    def test_api_handles_mixed_response_types(self, test_client):
        """Test API handles both string and structured degradation responses"""

        # Test string degradation response
        with patch("services.queries.query_router.QueryRouter.route_query") as mock_route:
            mock_route.return_value = (
                "Database temporarily unavailable. Please ensure Docker is running."
            )

            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            assert response.status_code == 200
            data = response.json()
            assert "Database temporarily unavailable" in data["message"]

        # Test structured degradation response
        with patch("services.queries.query_router.QueryRouter.route_query") as mock_route:
            mock_route.return_value = {
                "success": False,
                "error": "File service temporarily unavailable",
                "suggestion": "Please try again in a few moments.",
            }

            response = test_client.post("/api/v1/intent", json={"message": "Read file contents"})

            assert response.status_code == 200
            data = response.json()
            assert "File service temporarily unavailable" in data["message"]

    def test_api_error_recovery_mechanism(self, test_client):
        """Test API can recover from temporary failures"""

        # First call fails, second call succeeds
        with patch(
            "services.database.connection.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session.side_effect = [
                Exception("Temporary database failure"),
                None,  # Second call succeeds
            ]

            # First call should handle degradation gracefully
            response1 = test_client.post("/api/v1/intent", json={"message": "List all projects"})
            assert response1.status_code == 200
            data1 = response1.json()
            assert "Database temporarily unavailable" in data1["message"]

            # Second call should work normally
            response2 = test_client.post("/api/v1/intent", json={"message": "List all projects"})
            assert response2.status_code == 200
            data2 = response2.json()
            # Should not contain degradation message
            assert "Database temporarily unavailable" not in data2["message"]

    def test_api_graceful_degradation_message_quality(self, test_client):
        """Test degradation messages are user-friendly and actionable"""

        with patch(
            "services.database.connection.AsyncSessionFactory.session_scope"
        ) as mock_session:
            mock_session.side_effect = Exception("Database connection failed")

            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            assert response.status_code == 200
            data = response.json()
            message = data["message"]

            # Verify message quality criteria
            assert "Database temporarily unavailable" in message
            assert any(word in message.lower() for word in ["docker", "try again", "ensure"])
            assert len(message) > 20  # Should be informative
            assert not any(word in message.lower() for word in ["error", "exception", "traceback"])

    def test_api_maintains_backward_compatibility(self, test_client):
        """Test API maintains backward compatibility with existing response patterns"""

        # Test successful query maintains existing response structure
        with patch("services.queries.query_router.QueryRouter.route_query") as mock_route:
            mock_route.return_value = ["project1", "project2"]

            response = test_client.post("/api/v1/intent", json={"message": "List all projects"})

            assert response.status_code == 200
            data = response.json()

            # Verify existing response structure is maintained
            assert "message" in data
            assert "intent" in data
            assert "workflow_id" in data
            assert "requires_clarification" in data
            assert "clarification_type" in data

            # Verify successful response content
            assert "I found 2 projects" in data["message"]
            assert "project1" in data["message"]
            assert "project2" in data["message"]
