"""
E2E: Health check endpoint verification.

Verifies the server boots correctly and responds to health checks.
This is the most basic E2E test — if this fails, nothing else will work.

Note: /api/v1/health is behind auth middleware (not excluded like /health).
Tests use auth credentials. See discovered work note about excluding health
endpoints from auth.

Issue: #352 TEST-SMOKE-E2E
"""

import pytest


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_health_endpoint_returns_healthy(e2e_client, e2e_auth_headers):
    """Health endpoint returns 200 with expected structure."""
    response = await e2e_client.get("/api/v1/health", **e2e_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "piper-morgan"
    assert "timestamp" in data


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_health_database_endpoint(e2e_client, e2e_auth_headers):
    """Database health check returns connectivity status."""
    response = await e2e_client.get("/api/v1/health/database", **e2e_auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    # Database should be reachable in test environment
    assert data["status"] in ("healthy", "degraded")
