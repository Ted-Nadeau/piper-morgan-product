"""
Unit tests for Calendar Sync Preferences API
Issue #571: Calendar sync preferences

Tests the calendar list and preferences endpoints in settings_integrations.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    CalendarPreferencesRequest,
    get_calendar_list,
    get_calendar_preferences,
    save_calendar_preferences,
)


class TestGetCalendarList:
    """Tests for GET /api/v1/settings/integrations/calendar/calendars"""

    @pytest.mark.asyncio
    async def test_returns_401_when_not_connected(self):
        """Should return 401 when no refresh token in keychain"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = None

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "services.infrastructure.keychain_service.KeychainService",
            return_value=mock_keychain,
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_calendar_list(current_user=mock_user)

            assert exc_info.value.status_code == 401
            assert "Calendar not connected" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_returns_401_when_token_refresh_fails(self):
        """Should return 401 when token refresh fails"""
        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "test_refresh_token"

        mock_handler = MagicMock()
        mock_handler.refresh_access_token = AsyncMock(return_value=None)

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=mock_handler,
            ),
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_calendar_list(current_user=mock_user)

            assert exc_info.value.status_code == 401
            assert "refresh" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_returns_calendar_list_when_connected(self):
        """Should return list of calendars when connected"""
        import aiohttp

        mock_keychain = MagicMock()
        mock_keychain.get_api_key.return_value = "test_refresh_token"

        mock_tokens = MagicMock()
        mock_tokens.access_token = "test_access_token"

        mock_handler = MagicMock()
        mock_handler.refresh_access_token = AsyncMock(return_value=mock_tokens)

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # Mock Google API response
        mock_google_response = {
            "items": [
                {
                    "id": "primary",
                    "summary": "Work Calendar",
                    "description": "Main work calendar",
                    "primary": True,
                },
                {
                    "id": "personal@gmail.com",
                    "summary": "Personal",
                    "description": "",
                    "primary": False,
                },
            ]
        }

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_google_response)

        mock_session_instance = MagicMock()
        mock_session_instance.get = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.infrastructure.keychain_service.KeychainService",
                return_value=mock_keychain,
            ),
            patch(
                "services.integrations.calendar.oauth_handler.GoogleCalendarOAuthHandler",
                return_value=mock_handler,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
            patch(
                "web.api.routes.settings_integrations._load_calendar_preferences",
                return_value={},
            ),
        ):
            result = await get_calendar_list(current_user=mock_user)

            assert len(result.calendars) == 2
            assert result.calendars[0].id == "primary"
            assert result.calendars[0].name == "Work Calendar"
            assert result.calendars[0].primary is True
            assert result.calendars[1].id == "personal@gmail.com"


class TestGetCalendarPreferences:
    """Tests for GET /api/v1/settings/integrations/calendar/preferences"""

    @pytest.mark.asyncio
    async def test_returns_empty_preferences_when_not_saved(self):
        """Should return empty preferences when user has no saved preferences"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "web.api.routes.settings_integrations._load_calendar_preferences",
            return_value={},
        ):
            result = await get_calendar_preferences(current_user=mock_user)

            assert result.selected_calendars == []
            assert result.primary_calendar is None

    @pytest.mark.asyncio
    async def test_returns_saved_preferences(self):
        """Should return saved preferences for the user"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        saved_prefs = {
            "test-user-123": {
                "selected_calendars": ["primary", "personal@gmail.com"],
                "primary_calendar": "primary",
            }
        }

        with patch(
            "web.api.routes.settings_integrations._load_calendar_preferences",
            return_value=saved_prefs,
        ):
            result = await get_calendar_preferences(current_user=mock_user)

            assert result.selected_calendars == ["primary", "personal@gmail.com"]
            assert result.primary_calendar == "primary"

    @pytest.mark.asyncio
    async def test_returns_empty_for_different_user(self):
        """Should return empty for user without saved preferences"""
        mock_user = MagicMock()
        mock_user.sub = "different-user-456"

        saved_prefs = {
            "test-user-123": {
                "selected_calendars": ["primary"],
                "primary_calendar": "primary",
            }
        }

        with patch(
            "web.api.routes.settings_integrations._load_calendar_preferences",
            return_value=saved_prefs,
        ):
            result = await get_calendar_preferences(current_user=mock_user)

            assert result.selected_calendars == []
            assert result.primary_calendar is None


class TestSaveCalendarPreferences:
    """Tests for POST /api/v1/settings/integrations/calendar/preferences"""

    @pytest.mark.asyncio
    async def test_saves_preferences_successfully(self):
        """Should save preferences and return them"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        preferences = CalendarPreferencesRequest(
            selected_calendars=["primary", "personal@gmail.com"],
            primary_calendar="primary",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_calendar_preferences",
                return_value={},
            ),
            patch(
                "web.api.routes.settings_integrations._save_calendar_preferences",
                side_effect=mock_save,
            ),
        ):
            result = await save_calendar_preferences(
                preferences=preferences, current_user=mock_user
            )

            assert result.selected_calendars == ["primary", "personal@gmail.com"]
            assert result.primary_calendar == "primary"
            assert "test-user-123" in saved_data
            assert saved_data["test-user-123"]["selected_calendars"] == [
                "primary",
                "personal@gmail.com",
            ]

    @pytest.mark.asyncio
    async def test_overwrites_existing_preferences(self):
        """Should overwrite existing preferences for the user"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        existing_prefs = {
            "test-user-123": {
                "selected_calendars": ["old-calendar"],
                "primary_calendar": "old-calendar",
            }
        }

        new_preferences = CalendarPreferencesRequest(
            selected_calendars=["new-calendar"],
            primary_calendar="new-calendar",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_calendar_preferences",
                return_value=existing_prefs,
            ),
            patch(
                "web.api.routes.settings_integrations._save_calendar_preferences",
                side_effect=mock_save,
            ),
        ):
            result = await save_calendar_preferences(
                preferences=new_preferences, current_user=mock_user
            )

            assert result.selected_calendars == ["new-calendar"]
            assert result.primary_calendar == "new-calendar"
            assert saved_data["test-user-123"]["selected_calendars"] == ["new-calendar"]

    @pytest.mark.asyncio
    async def test_preserves_other_users_preferences(self):
        """Should not affect other users' preferences"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        existing_prefs = {
            "other-user-456": {
                "selected_calendars": ["other-calendar"],
                "primary_calendar": "other-calendar",
            }
        }

        new_preferences = CalendarPreferencesRequest(
            selected_calendars=["my-calendar"],
            primary_calendar="my-calendar",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_calendar_preferences",
                return_value=existing_prefs,
            ),
            patch(
                "web.api.routes.settings_integrations._save_calendar_preferences",
                side_effect=mock_save,
            ),
        ):
            await save_calendar_preferences(preferences=new_preferences, current_user=mock_user)

            # Other user's preferences should be preserved
            assert "other-user-456" in saved_data
            assert saved_data["other-user-456"]["selected_calendars"] == ["other-calendar"]
            # New user's preferences should be added
            assert "test-user-123" in saved_data
            assert saved_data["test-user-123"]["selected_calendars"] == ["my-calendar"]


class TestCalendarPreferencesFileStorage:
    """Tests for calendar preferences file-based storage helpers"""

    def test_load_preferences_returns_empty_when_file_missing(self):
        """Should return empty dict when preferences file doesn't exist"""
        from web.api.routes.settings_integrations import _load_calendar_preferences

        with patch("os.path.exists", return_value=False):
            result = _load_calendar_preferences()
            assert result == {}

    def test_load_preferences_returns_data_when_file_exists(self):
        """Should return parsed JSON when file exists"""
        import json

        from web.api.routes.settings_integrations import _load_calendar_preferences

        test_data = {
            "user-123": {
                "selected_calendars": ["cal1"],
                "primary_calendar": "cal1",
            }
        }

        with (
            patch("os.path.exists", return_value=True),
            patch(
                "builtins.open",
                MagicMock(
                    return_value=MagicMock(
                        __enter__=MagicMock(
                            return_value=MagicMock(
                                read=MagicMock(return_value=json.dumps(test_data))
                            )
                        ),
                        __exit__=MagicMock(return_value=False),
                    )
                ),
            ),
            patch("json.load", return_value=test_data),
        ):
            result = _load_calendar_preferences()
            assert result == test_data

    def test_save_preferences_creates_directory(self):
        """Should create data directory if it doesn't exist"""
        from web.api.routes.settings_integrations import _save_calendar_preferences

        mock_makedirs = MagicMock()
        mock_open = MagicMock()
        mock_file = MagicMock()
        mock_open.return_value.__enter__ = MagicMock(return_value=mock_file)
        mock_open.return_value.__exit__ = MagicMock(return_value=False)

        with (
            patch("os.makedirs", mock_makedirs),
            patch("builtins.open", mock_open),
            patch("json.dump"),
        ):
            _save_calendar_preferences({"test": "data"})

            # Should call makedirs with exist_ok=True
            mock_makedirs.assert_called_once()
            assert mock_makedirs.call_args[1]["exist_ok"] is True
