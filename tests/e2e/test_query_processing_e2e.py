"""
E2E: Query/intent processing verification.

Tests the core user journey: login, submit a message via /api/v1/intent,
and verify a structured response is returned. Does NOT assert on LLM-generated
content (that would be fragile) — only on response structure and deterministic fields.

Issue: #352 TEST-SMOKE-E2E
"""

import pytest


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_intent_returns_structured_response(e2e_client, e2e_auth_headers):
    """Authenticated intent request returns well-structured response."""
    response = await e2e_client.post(
        "/api/v1/intent",
        json={"message": "Hello", "session_id": "e2e-test-session"},
        **e2e_auth_headers,
    )

    assert response.status_code == 200
    data = response.json()

    # Response must have these structural fields
    assert "message" in data, f"Response missing 'message': {data}"
    assert isinstance(data["message"], str)
    assert len(data["message"]) > 0, "Empty response message"

    # Intent classification should be present
    assert "intent" in data, f"Response missing 'intent': {data}"

    # Session ID should be echoed back
    assert data.get("session_id") == "e2e-test-session"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_intent_without_auth_still_responds(e2e_client):
    """Intent endpoint works without auth (graceful degradation)."""
    response = await e2e_client.post(
        "/api/v1/intent",
        json={"message": "What can you do?", "session_id": "e2e-unauth"},
    )

    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert len(data["message"]) > 0


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_intent_does_not_echo_input(e2e_client, e2e_auth_headers):
    """Response should never be a verbatim echo of user input."""
    test_message = "This is a unique test string that should not be echoed back verbatim"

    response = await e2e_client.post(
        "/api/v1/intent",
        json={"message": test_message, "session_id": "e2e-echo-test"},
        **e2e_auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["message"] != test_message, f"Response echoed user input verbatim"


@pytest.mark.e2e
@pytest.mark.asyncio
async def test_intent_handles_empty_message_gracefully(e2e_client, e2e_auth_headers):
    """Empty message should get a response, not a crash."""
    response = await e2e_client.post(
        "/api/v1/intent",
        json={"message": "", "session_id": "e2e-empty-test"},
        **e2e_auth_headers,
    )

    # Should return 200 (graceful degradation) or 422 (validation error)
    assert response.status_code in (200, 422)
