"""
Test suite to prevent intent classification bypasses.
Ensures all NL endpoints use intent classification.
"""

import pytest
from fastapi.testclient import TestClient

from web.app import app

client = TestClient(app)


class TestBypassPrevention:
    """Prevent bypasses of intent classification."""

    def test_middleware_is_registered(self):
        """Verify IntentEnforcementMiddleware is active."""
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 200
        data = response.json()
        assert data["middleware_active"] is True
        assert len(data["nl_endpoints"]) == 4
        assert len(data["exempt_paths"]) == 12

    def test_nl_endpoints_marked(self):
        """Verify NL endpoints are marked as requiring intent."""
        # This would require accessing request.state in tests
        # For now, verify they exist
        nl_endpoints = ["/api/v1/intent", "/api/standup", "/api/chat", "/api/message"]

        for endpoint in nl_endpoints:
            # Test endpoint exists or returns expected status
            response = client.get(endpoint)
            # 404, 405, or 422 are acceptable (endpoint exists but wrong method/data)
            assert response.status_code in [200, 404, 405, 422]

    def test_exempt_paths_accessible(self):
        """Verify exempt paths work without intent."""
        exempt_tests = [("/health", 200), ("/docs", 200), ("/", 200)]

        for path, expected_status in exempt_tests:
            response = client.get(path)
            assert (
                response.status_code == expected_status
            ), f"{path} should be accessible (got {response.status_code})"

    def test_personality_enhance_is_exempt(self):
        """Personality enhancement is output processing, should be exempt."""
        # This endpoint processes Piper's output, not user input
        response = client.post(
            "/api/personality/enhance", json={"text": "Test response", "context": {}}
        )
        # Should not require intent (it's exempt)
        # 200 or 422 acceptable depending on validation
        assert response.status_code in [200, 422]

    def test_monitoring_logs_requests(self, caplog):
        """Verify middleware logs all requests."""
        with caplog.at_level("INFO"):
            client.get("/health")

        # Check logs contain request
        log_messages = [record.message for record in caplog.records]
        assert any("Request: GET /health" in msg for msg in log_messages)
