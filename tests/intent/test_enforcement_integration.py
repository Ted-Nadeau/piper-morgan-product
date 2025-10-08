"""
Integration tests for intent enforcement.

GREAT-5 Phase 1.5: Updated to use client_with_intent fixture for proper
IntentService initialization in test environment.
"""

import pytest


@pytest.fixture
def client(client_with_intent):
    """Use the properly initialized client from conftest."""
    return client_with_intent


class TestEnforcementIntegration:
    """Test full enforcement pipeline."""

    def test_intent_endpoint_works(self, client):
        """Primary intent endpoint should work."""
        response = client.post("/api/v1/intent", json={"text": "What day is it?"})
        # GREAT-5: Should succeed or validation error, but NOT crash (500)
        assert response.status_code in [200, 422]

    def test_standup_uses_backend_intent(self, client):
        """Standup endpoint should proxy to backend that uses intent."""
        response = client.get("/api/standup")
        # GREAT-5: Should succeed or auth error, but NOT crash (500)
        assert response.status_code in [200, 401]

    def test_monitoring_endpoint_accessible(self, client):
        """Admin monitoring should be accessible."""
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 200

        data = response.json()
        assert "middleware_active" in data
        assert "nl_endpoints" in data
        assert "exempt_paths" in data
