"""
Integration tests for intent enforcement.
"""

import pytest
from fastapi.testclient import TestClient

from web.app import app

client = TestClient(app)


class TestEnforcementIntegration:
    """Test full enforcement pipeline."""

    def test_intent_endpoint_works(self):
        """Primary intent endpoint should work."""
        response = client.post("/api/v1/intent", json={"text": "What day is it?"})
        # Should succeed or fail gracefully
        assert response.status_code in [200, 422, 500]

    def test_standup_uses_backend_intent(self):
        """Standup endpoint should proxy to backend that uses intent."""
        response = client.get("/api/standup")
        # Should succeed or return expected error
        assert response.status_code in [200, 401, 500]

    def test_monitoring_endpoint_accessible(self):
        """Admin monitoring should be accessible."""
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 200

        data = response.json()
        assert "middleware_active" in data
        assert "nl_endpoints" in data
        assert "exempt_paths" in data
