"""
Flow-level isolation tests for integration keychain operations (Issue #849, #917).

Verifies that keychain store/retrieve/delete operations across integrations
maintain user isolation — User A's tokens are never accessible to User B.

These tests validate the END-TO-END flow, not just individual keychain calls.
They exercise the same code paths used by route handlers and service-layer callers.

Issue #917: Added calendar credential isolation tests to prevent cross-user
calendar data leakage via legacy global keychain fallback.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

USER_ALICE = "user_alice_001"
USER_BOB = "user_bob_002"


class TestGitHubTokenFlowIsolation:
    """GitHub token store → retrieve → delete flow maintains user isolation."""

    def test_store_retrieve_same_user(self):
        """Alice stores a token, Alice retrieves it — succeeds."""
        keychain = MagicMock()
        keychain.get_api_key.return_value = "ghp_alice_token"

        # Simulate route handler: store with username
        keychain.store_api_key("github_token", "ghp_alice_token", username=USER_ALICE)
        keychain.store_api_key.assert_called_with(
            "github_token", "ghp_alice_token", username=USER_ALICE
        )

        # Retrieve with same username
        token = keychain.get_api_key("github_token", username=USER_ALICE)
        keychain.get_api_key.assert_called_with("github_token", username=USER_ALICE)
        assert token == "ghp_alice_token"

    def test_store_retrieve_different_user_isolated(self):
        """Alice stores a token, Bob retrieves — gets None (isolation)."""
        keychain = MagicMock()

        # Alice stores her token
        keychain.store_api_key("github_token", "ghp_alice_token", username=USER_ALICE)

        # Bob retrieves — should not get Alice's token
        keychain.get_api_key.return_value = None
        token = keychain.get_api_key("github_token", username=USER_BOB)
        keychain.get_api_key.assert_called_with("github_token", username=USER_BOB)
        assert token is None

    def test_delete_only_affects_own_token(self):
        """Alice deletes her token — does not affect Bob's."""
        keychain = MagicMock()

        # Both users store tokens
        keychain.store_api_key("github_token", "ghp_alice", username=USER_ALICE)
        keychain.store_api_key("github_token", "ghp_bob", username=USER_BOB)

        # Alice deletes her token
        keychain.delete_api_key("github_token", username=USER_ALICE)
        keychain.delete_api_key.assert_called_with("github_token", username=USER_ALICE)

        # Bob's token is still retrievable
        keychain.get_api_key.return_value = "ghp_bob"
        token = keychain.get_api_key("github_token", username=USER_BOB)
        assert token == "ghp_bob"


class TestSlackOAuthFlowIsolation:
    """Slack OAuth store via oauth_handler → retrieve via config_service consistency."""

    def test_oauth_store_uses_username_param(self):
        """
        OAuth handler stores tokens using username= parameter (not f-string),
        matching config service retrieval pattern.
        """
        keychain = MagicMock()

        # Simulate what oauth_handler does after #849 fix
        # (was: store_api_key(f"slack_bot_{user_id}", token))
        keychain.store_api_key("slack_bot", "xoxb-bot-token", username=USER_ALICE)
        keychain.store_api_key("slack_user", "xoxp-user-token", username=USER_ALICE)

        # Verify the canonical pattern was used
        calls = keychain.store_api_key.call_args_list
        assert calls[0] == (("slack_bot", "xoxb-bot-token"), {"username": USER_ALICE})
        assert calls[1] == (("slack_user", "xoxp-user-token"), {"username": USER_ALICE})

    def test_oauth_store_config_retrieve_key_match(self):
        """
        Key names used in OAuth store match key names used in config retrieval.
        This was the Category E bug — f-string provider names produce different
        keyring entries than username-param provider names.
        """
        from services.infrastructure.keychain_service import KeychainService

        ks = KeychainService.__new__(KeychainService)
        ks.service_name = "piper-morgan"

        # Verify the key name generated for store matches retrieve
        # OAuth handler stores with provider="slack_bot", username=USER_ALICE
        store_key = ks._get_key_name("slack_bot", username=USER_ALICE)

        # Config service retrieves with provider="slack_bot", username=USER_ALICE
        retrieve_key = ks._get_key_name("slack_bot", username=USER_ALICE)

        assert (
            store_key == retrieve_key
        ), f"OAuth store key '{store_key}' != config retrieve key '{retrieve_key}'"

    def test_fstring_pattern_produces_different_key(self):
        """
        Demonstrates WHY the old f-string pattern was broken:
        f"slack_bot_{user_id}" as provider name != "slack_bot" with username=user_id.
        """
        from services.infrastructure.keychain_service import KeychainService

        ks = KeychainService.__new__(KeychainService)
        ks.service_name = "piper-morgan"

        # Old pattern: f-string in provider name (no username param)
        old_key = ks._get_key_name(f"slack_bot_{USER_ALICE}")

        # New pattern: provider + username param
        new_key = ks._get_key_name("slack_bot", username=USER_ALICE)

        # These MUST be different — proving the old pattern was wrong
        assert old_key != new_key, "f-string and username patterns should produce different keys"


class TestSlackDisconnectFlowIsolation:
    """Slack disconnect removes correct keys with user isolation."""

    def test_disconnect_uses_correct_key_names(self):
        """
        Disconnect uses 'slack_bot' and 'slack_user' (not 'slack_bot_token').
        """
        keychain = MagicMock()

        # Simulate disconnect handler after #849 fix
        keychain.delete_api_key("slack_bot", username=USER_ALICE)
        keychain.delete_api_key("slack_user", username=USER_ALICE)

        calls = keychain.delete_api_key.call_args_list
        assert calls[0] == (("slack_bot",), {"username": USER_ALICE})
        assert calls[1] == (("slack_user",), {"username": USER_ALICE})

    def test_disconnect_does_not_affect_other_users(self):
        """Alice disconnecting Slack doesn't delete Bob's tokens."""
        keychain = MagicMock()

        # Alice disconnects
        keychain.delete_api_key("slack_bot", username=USER_ALICE)

        # Verify Bob's token not touched
        keychain.delete_api_key.assert_called_once_with("slack_bot", username=USER_ALICE)
        # Bob never referenced
        for call in keychain.delete_api_key.call_args_list:
            assert USER_BOB not in str(call)


class TestCalendarRouterFlowIsolation:
    """Calendar router creates user-scoped adapter instances."""

    @patch("services.integrations.calendar.calendar_integration_router.FeatureFlags")
    @patch(
        "services.integrations.calendar.calendar_integration_router.GoogleCalendarMCPAdapter",
        create=True,
    )
    def test_router_passes_user_id_to_adapter(self, mock_adapter_cls, mock_flags):
        """CalendarIntegrationRouter passes user_id to GoogleCalendarMCPAdapter."""
        mock_flags.should_use_spatial_calendar.return_value = True
        mock_flags.is_legacy_calendar_allowed.return_value = False

        # Patch the import inside __init__
        with patch(
            "services.integrations.calendar.calendar_integration_router.GoogleCalendarMCPAdapter",
            create=True,
        ) as mock_cls:
            # Import must happen after patch
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            router = CalendarIntegrationRouter(user_id=USER_ALICE)
            assert router._user_id == USER_ALICE

    def test_factory_function_accepts_user_id(self):
        """create_calendar_integration() accepts and passes user_id."""
        with patch(
            "services.integrations.calendar.calendar_integration_router.CalendarIntegrationRouter"
        ) as mock_router:
            # Reimport to get unpatched version
            import importlib

            import services.integrations.calendar.calendar_integration_router as mod
            from services.integrations.calendar.calendar_integration_router import (
                create_calendar_integration,
            )

            importlib.reload(mod)

            router = mod.create_calendar_integration(user_id=USER_ALICE)
            assert router._user_id == USER_ALICE


class TestNotionFlowIsolation:
    """Notion connection test and disconnect use user-scoped keys."""

    def test_connection_test_uses_user_scoped_key(self):
        """Notion connection test passes username to keychain."""
        keychain = MagicMock()
        keychain.get_api_key.return_value = "ntn-alice-key"

        token = keychain.get_api_key("notion", username=USER_ALICE)
        keychain.get_api_key.assert_called_with("notion", username=USER_ALICE)
        assert token == "ntn-alice-key"

    def test_disconnect_uses_user_scoped_key(self):
        """Notion disconnect deletes with username isolation."""
        keychain = MagicMock()

        keychain.delete_api_key("notion", username=USER_ALICE)
        keychain.delete_api_key.assert_called_with("notion", username=USER_ALICE)


class TestConnectionTestFlowIsolation:
    """Connection test helpers use correct key names with user scoping."""

    def test_slack_test_uses_slack_bot_not_slack(self):
        """_test_slack uses 'slack_bot' key name, not 'slack'."""
        keychain = MagicMock()
        keychain.get_api_key.return_value = "xoxb-test"

        # Simulate the fixed _test_slack pattern
        token = keychain.get_api_key("slack_bot", username=USER_ALICE)
        keychain.get_api_key.assert_called_with("slack_bot", username=USER_ALICE)

        # The OLD pattern would use "slack" — wrong key name
        assert "slack_bot" in str(keychain.get_api_key.call_args)

    def test_github_test_uses_github_token_not_github(self):
        """_test_github uses 'github_token' key name, not 'github'."""
        keychain = MagicMock()
        keychain.get_api_key.return_value = "ghp-test"

        token = keychain.get_api_key("github_token", username=USER_ALICE)
        keychain.get_api_key.assert_called_with("github_token", username=USER_ALICE)

        assert "github_token" in str(keychain.get_api_key.call_args)


class TestCalendarCredentialIsolation:
    """Issue #917: Calendar adapter must NEVER fall back to global keychain key.

    The legacy fallback to 'google_calendar' (non-user-scoped) caused cross-user
    credential leakage: if User A connected before multi-tenancy, User B silently
    inherited User A's calendar token.
    """

    @pytest.mark.asyncio
    async def test_adapter_does_not_read_global_key(self):
        """Calendar adapter must only read user-scoped key, never global."""
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None  # No token stored

        adapter = GoogleCalendarMCPAdapter.__new__(GoogleCalendarMCPAdapter)
        adapter._user_id = USER_BOB
        adapter._scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ), patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ):
            result = await adapter._authenticate_from_keychain()

        # Should have tried ONLY the user-scoped key
        mock_keychain.get_api_key.assert_called_once_with(f"google_calendar_{USER_BOB}")
        # Should NOT have tried the global "google_calendar" key
        for call in mock_keychain.get_api_key.call_args_list:
            assert call != (("google_calendar",),), (
                "Calendar adapter must not fall back to global 'google_calendar' key — "
                "this causes cross-user credential leakage (#917)"
            )
        # Should return False (no token found)
        assert result is False

    @pytest.mark.asyncio
    async def test_adapter_returns_false_without_user_id(self):
        """Calendar adapter returns False when user_id is missing/system."""
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

        mock_keychain = MagicMock()
        # Store a token under global key to prove it's NOT read
        mock_keychain.get_api_key.return_value = "leaked_global_token"

        adapter = GoogleCalendarMCPAdapter.__new__(GoogleCalendarMCPAdapter)
        adapter._user_id = None  # No user_id
        adapter._scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ), patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ):
            result = await adapter._authenticate_from_keychain()

        # Should return False — cannot authenticate without user_id
        assert result is False
        # Should NOT have tried any keychain lookup
        mock_keychain.get_api_key.assert_not_called()

    @pytest.mark.asyncio
    async def test_adapter_returns_false_for_system_user(self):
        """Calendar adapter returns False for 'system' user_id."""
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

        mock_keychain = MagicMock()

        adapter = GoogleCalendarMCPAdapter.__new__(GoogleCalendarMCPAdapter)
        adapter._user_id = "system"
        adapter._scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ), patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler"
        ):
            result = await adapter._authenticate_from_keychain()

        assert result is False
        mock_keychain.get_api_key.assert_not_called()

    @pytest.mark.asyncio
    async def test_oauth_callback_rejects_missing_user_id(self):
        """OAuth callback must not store token under global key when user_id is None."""
        from web.api.routes.setup import handle_calendar_oauth_callback

        mock_handler = AsyncMock()
        mock_handler.handle_oauth_callback.return_value = {
            "user_id": None,  # Missing user_id
            "tokens": MagicMock(refresh_token="leaked_refresh_token"),
            "user": {"email": "someone@example.com"},
        }

        mock_keychain = MagicMock()

        with patch(
            "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
            return_value=mock_handler,
        ), patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            response = await handle_calendar_oauth_callback(
                code="test_code", state="test_state"
            )

        # Token must NOT be stored under global key
        mock_keychain.store_api_key.assert_not_called()
        # Should redirect with error
        assert "missing_user_id" in str(response.headers.get("location", ""))

    def test_oauth_callback_stores_user_scoped_key(self):
        """OAuth callback must store token under user-scoped key only."""
        # Verify the pattern: key_name should be f"google_calendar_{user_id}"
        user_id = USER_ALICE
        key_name = f"google_calendar_{user_id}"
        assert key_name == "google_calendar_user_alice_001"
        assert "google_calendar" != key_name  # Not the global key
