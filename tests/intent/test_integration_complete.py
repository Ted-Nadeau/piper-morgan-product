"""
Integration tests for complete intent system.

GREAT-5 Phase 1.5: Updated to use client_with_intent fixture for proper
IntentService initialization in test environment.
"""

import pytest


@pytest.fixture
def client(client_with_intent):
    """Use the properly initialized client from conftest."""
    return client_with_intent


class TestIntentSystemIntegration:
    """Full system integration tests."""

    def test_complete_pipeline_exists(self, client):
        """Verify all pipeline components exist."""
        # 1. Intent endpoint exists
        response = client.post("/api/v1/intent", json={"text": "test"})
        # GREAT-5: Intent endpoint must work reliably - no server crashes (500)
        assert response.status_code in [200, 422]

        # 2. Middleware monitoring exists
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 200

        # 3. Cache monitoring exists
        response = client.get("/api/admin/intent-cache-metrics")
        assert response.status_code == 200

    def test_nl_endpoints_configured(self, client):
        """All NL endpoints should be in middleware config."""
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 200

        data = response.json()
        nl_endpoints = data.get("nl_endpoints", [])

        # Should have at least these
        assert "/api/v1/intent" in nl_endpoints
        assert "/api/standup" in nl_endpoints

    def test_cache_operational(self, client):
        """Cache should be operational."""
        response = client.get("/api/admin/intent-cache-metrics")
        assert response.status_code == 200

        data = response.json()
        assert data.get("cache_enabled") is True
        assert data.get("status") == "operational"
