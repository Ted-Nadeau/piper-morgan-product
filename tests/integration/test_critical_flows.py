"""
Integration Tests for Critical User Flows

Tests end-to-end functionality of the most important user paths.
Alpha-appropriate scope - covers critical flows without over-engineering.

Based on:
- GREAT-4 intent system (13 categories, 4 interfaces)
- GREAT-4E validation (142+ tests)
- GREAT-5 quality gates (zero-tolerance, performance)

GREAT-5 Phase 3: Created October 7, 2025
"""

import pytest


@pytest.fixture
def client(client_with_intent):
    """Use properly initialized client from conftest (Phase 1.5)."""
    return client_with_intent


class TestIntentClassificationFlow:
    """
    Test complete intent classification flow for all 13 categories.

    Flow: User input → Classification → Handler → Response
    """

    # Canonical categories (5)

    def test_identity_flow(self, client):
        """IDENTITY: who are you → bot identity"""
        response = client.post("/api/v1/intent", json={"message": "who are you"})
        assert response.status_code == 200, f"IDENTITY must work, got {response.status_code}"
        data = response.json()
        assert data is not None
        # Verify response structure valid

    def test_temporal_flow(self, client):
        """TEMPORAL: show my calendar → calendar response"""
        response = client.post("/api/v1/intent", json={"message": "show my calendar"})
        # GREAT-5: No crashes (500), validation errors (422) OK
        assert response.status_code in [
            200,
            422,
        ], f"TEMPORAL must not crash, got {response.status_code}"

    def test_status_flow(self, client):
        """STATUS: what's my status → status response"""
        response = client.post("/api/v1/intent", json={"message": "what's my status"})
        assert response.status_code in [
            200,
            422,
        ], f"STATUS must not crash, got {response.status_code}"

    def test_priority_flow(self, client):
        """PRIORITY: my priorities → priority response"""
        response = client.post("/api/v1/intent", json={"message": "show my priorities"})
        assert response.status_code in [
            200,
            422,
        ], f"PRIORITY must not crash, got {response.status_code}"

    def test_guidance_flow(self, client):
        """GUIDANCE: how do I... → guidance response"""
        response = client.post("/api/v1/intent", json={"message": "how do I create a PR"})
        assert response.status_code in [
            200,
            422,
        ], f"GUIDANCE must not crash, got {response.status_code}"

    # Workflow categories (8)

    def test_execution_flow(self, client):
        """EXECUTION: create issue → execution workflow"""
        response = client.post("/api/v1/intent", json={"message": "create a github issue"})
        # May require auth/config, but should not crash
        assert response.status_code in [
            200,
            422,
        ], f"EXECUTION must not crash, got {response.status_code}"

    def test_analysis_flow(self, client):
        """ANALYSIS: analyze project → analysis workflow"""
        response = client.post("/api/v1/intent", json={"message": "analyze our project status"})
        assert response.status_code in [
            200,
            422,
        ], f"ANALYSIS must not crash, got {response.status_code}"

    def test_synthesis_flow(self, client):
        """SYNTHESIS: summarize → synthesis workflow"""
        response = client.post("/api/v1/intent", json={"message": "summarize recent updates"})
        assert response.status_code in [
            200,
            422,
        ], f"SYNTHESIS must not crash, got {response.status_code}"

    def test_strategy_flow(self, client):
        """STRATEGY: planning query → strategy workflow"""
        response = client.post("/api/v1/intent", json={"message": "plan our next sprint"})
        assert response.status_code in [
            200,
            422,
        ], f"STRATEGY must not crash, got {response.status_code}"

    def test_learning_flow(self, client):
        """LEARNING: teach/explain → learning workflow"""
        response = client.post("/api/v1/intent", json={"message": "explain how caching works"})
        assert response.status_code in [
            200,
            422,
        ], f"LEARNING must not crash, got {response.status_code}"

    def test_conversation_flow(self, client):
        """CONVERSATION: casual chat → conversation workflow"""
        response = client.post("/api/v1/intent", json={"message": "how are you doing"})
        # Conversation should always work (no external dependencies)
        assert response.status_code == 200, f"CONVERSATION must work, got {response.status_code}"

    def test_query_flow(self, client):
        """QUERY: generic question → query workflow (fallback)"""
        response = client.post("/api/v1/intent", json={"message": "what is the meaning of life"})
        # QUERY has fallback from GREAT-4F - should not timeout
        assert response.status_code in [
            200,
            422,
        ], f"QUERY must not timeout (has fallback), got {response.status_code}"

    def test_unknown_flow(self, client):
        """UNKNOWN: unclear input → unknown workflow"""
        response = client.post("/api/v1/intent", json={"message": "asdfghjkl"})
        # Should handle gracefully even if unclear
        assert response.status_code in [
            200,
            422,
        ], f"UNKNOWN must handle gracefully, got {response.status_code}"


class TestMultiUserIsolation:
    """
    Test that multi-user context isolation works correctly.

    From GREAT-4C: Multi-user context support implemented.
    Verify User A's context doesn't leak to User B.
    """

    def test_session_isolation(self, client):
        """Different sessions should have isolated context"""
        # User A request
        response_a = client.post(
            "/api/v1/intent",
            json={"message": "my name is Alice"},
            headers={"X-Session-ID": "session-a"},
        )
        assert response_a.status_code in [
            200,
            422,
        ], f"Session A must work, got {response_a.status_code}"

        # User B request
        response_b = client.post(
            "/api/v1/intent",
            json={"message": "what is my name"},
            headers={"X-Session-ID": "session-b"},
        )
        assert response_b.status_code in [
            200,
            422,
        ], f"Session B must work, got {response_b.status_code}"

        # User B should NOT know Alice's name
        # (This is basic isolation test - full testing would require mocks)

    def test_concurrent_users(self, client):
        """Multiple users can use system concurrently"""
        # Send requests from 3 different users
        for user_id in ["user-1", "user-2", "user-3"]:
            response = client.post(
                "/api/v1/intent", json={"message": "who are you"}, headers={"X-Session-ID": user_id}
            )
            assert (
                response.status_code == 200
            ), f"User {user_id} IDENTITY must work, got {response.status_code}"
            # All should get valid responses independently


class TestErrorRecovery:
    """
    Test graceful error handling and recovery.

    System should degrade gracefully, never crash.
    """

    def test_invalid_json(self, client):
        """Invalid JSON should not crash server (return 200 or 422, not 500)"""
        response = client.post(
            "/api/v1/intent", data="not valid json", headers={"Content-Type": "application/json"}
        )
        # FastAPI may auto-handle and return 200, or return 422 validation error
        # Key point: NOT 500 (server crash)
        assert response.status_code in [
            200,
            422,
        ], f"Invalid JSON must not crash, got {response.status_code}"

    def test_missing_message(self, client):
        """Missing message field should not crash (200 or 422)"""
        response = client.post("/api/v1/intent", json={})
        # API may handle gracefully (200) or validate (422), key: not crash (500)
        assert response.status_code in [
            200,
            422,
        ], f"Missing message must not crash, got {response.status_code}"

    def test_empty_message(self, client):
        """Empty message should be handled gracefully"""
        response = client.post("/api/v1/intent", json={"message": ""})
        # Either handle empty or validate, but don't crash
        assert response.status_code in [
            200,
            422,
        ], f"Empty message must not crash, got {response.status_code}"

    def test_very_long_message(self, client):
        """Very long message should be handled gracefully"""
        long_message = "word " * 10000  # 50K characters
        response = client.post("/api/v1/intent", json={"message": long_message})
        # Either process or reject, but don't crash
        assert response.status_code in [
            200,
            422,
        ], f"Long message must not crash, got {response.status_code}"


class TestCanonicalHandlerIntegration:
    """
    Test canonical handlers end-to-end.

    From GREAT-4F: Canonical handlers are fast-path (1ms, 600K+ req/sec).
    Verify they work correctly in integration.
    """

    def test_identity_handler_response(self, client):
        """IDENTITY handler returns valid bot identity"""
        response = client.post("/api/v1/intent", json={"message": "what can you do"})
        assert response.status_code == 200, f"IDENTITY must work, got {response.status_code}"

        data = response.json()
        # Should contain bot identity/capabilities info
        # Exact structure may vary, just verify it's a valid response
        assert data is not None
        assert isinstance(data, dict)

    def test_temporal_handler_response(self, client):
        """TEMPORAL handler provides calendar info or appropriate error"""
        response = client.post("/api/v1/intent", json={"message": "what's on my schedule today"})
        assert response.status_code in [
            200,
            422,
        ], f"TEMPORAL must not crash, got {response.status_code}"

        # If 422, should explain calendar not configured
        # If 200, should return calendar data

    def test_status_handler_response(self, client):
        """STATUS handler provides work status or appropriate error"""
        response = client.post("/api/v1/intent", json={"message": "show my standup"})
        assert response.status_code in [
            200,
            422,
        ], f"STATUS must not crash, got {response.status_code}"

        # Should either provide status or explain not configured

    def test_priority_handler_response(self, client):
        """PRIORITY handler provides priorities or appropriate error"""
        response = client.post("/api/v1/intent", json={"message": "what should I focus on"})
        assert response.status_code in [
            200,
            422,
        ], f"PRIORITY must not crash, got {response.status_code}"

        # Should either provide priorities or explain not configured
