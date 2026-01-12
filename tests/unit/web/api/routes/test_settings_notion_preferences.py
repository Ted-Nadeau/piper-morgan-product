"""
Unit tests for Notion Workspace Preferences API
Issue #572: Notion workspace preferences

Tests the Notion database list and preferences endpoints in settings_integrations.py.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from web.api.routes.settings_integrations import (
    NotionPreferencesRequest,
    get_notion_databases,
    get_notion_preferences,
    save_notion_preferences,
)


class TestGetNotionDatabases:
    """Tests for GET /api/v1/settings/integrations/notion/databases"""

    @pytest.mark.asyncio
    async def test_returns_401_when_not_connected(self):
        """Should return 401 when no API key configured"""
        mock_config = MagicMock()
        mock_config.api_key = None

        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "services.integrations.notion.config_service.NotionConfigService",
            return_value=mock_config_service,
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_notion_databases(current_user=mock_user)

            assert exc_info.value.status_code == 401
            assert "not connected" in str(exc_info.value.detail).lower()

    @pytest.mark.asyncio
    async def test_returns_database_list_when_connected(self):
        """Should return list of databases when connected"""
        mock_config = MagicMock()
        mock_config.api_key = "secret_test_key"

        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        # Mock Notion API response
        mock_notion_response = {
            "results": [
                {
                    "id": "abc123",
                    "title": [{"plain_text": "Work Tasks"}],
                    "description": [{"plain_text": "Team task tracker"}],
                },
                {
                    "id": "def456",
                    "title": [{"plain_text": "Project Notes"}],
                    "description": [],
                },
            ]
        }

        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value=mock_notion_response)

        mock_session_instance = MagicMock()
        mock_session_instance.post = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.integrations.notion.config_service.NotionConfigService",
                return_value=mock_config_service,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
            patch(
                "web.api.routes.settings_integrations._load_notion_preferences",
                return_value={},
            ),
        ):
            result = await get_notion_databases(current_user=mock_user)

            assert len(result.databases) == 2
            assert result.databases[0].id == "abc123"
            assert result.databases[0].name == "Work Tasks"
            assert result.databases[0].description == "Team task tracker"
            assert result.databases[1].id == "def456"
            assert result.databases[1].name == "Project Notes"
            assert result.databases[1].description == ""

    @pytest.mark.asyncio
    async def test_returns_error_when_notion_api_fails(self):
        """Should return error when Notion API returns error"""
        mock_config = MagicMock()
        mock_config.api_key = "secret_test_key"

        mock_config_service = MagicMock()
        mock_config_service.get_config.return_value = mock_config

        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        mock_response = AsyncMock()
        mock_response.status = 401
        mock_response.text = AsyncMock(return_value="Invalid API key")

        mock_session_instance = MagicMock()
        mock_session_instance.post = MagicMock(
            return_value=AsyncMock(
                __aenter__=AsyncMock(return_value=mock_response), __aexit__=AsyncMock()
            )
        )

        mock_session = MagicMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session_instance)
        mock_session.__aexit__ = AsyncMock()

        with (
            patch(
                "services.integrations.notion.config_service.NotionConfigService",
                return_value=mock_config_service,
            ),
            patch("aiohttp.ClientSession", return_value=mock_session),
        ):
            from fastapi import HTTPException

            with pytest.raises(HTTPException) as exc_info:
                await get_notion_databases(current_user=mock_user)

            # Should return an error status (either 502 from our code or 500 from exception handling)
            assert exc_info.value.status_code >= 500


class TestGetNotionPreferences:
    """Tests for GET /api/v1/settings/integrations/notion/preferences"""

    @pytest.mark.asyncio
    async def test_returns_empty_preferences_when_not_saved(self):
        """Should return empty preferences when user has no saved preferences"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        with patch(
            "web.api.routes.settings_integrations._load_notion_preferences",
            return_value={},
        ):
            result = await get_notion_preferences(current_user=mock_user)

            assert result.selected_databases == []
            assert result.default_database is None

    @pytest.mark.asyncio
    async def test_returns_saved_preferences(self):
        """Should return saved preferences for the user"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        saved_prefs = {
            "test-user-123": {
                "selected_databases": ["abc123", "def456"],
                "default_database": "abc123",
            }
        }

        with patch(
            "web.api.routes.settings_integrations._load_notion_preferences",
            return_value=saved_prefs,
        ):
            result = await get_notion_preferences(current_user=mock_user)

            assert result.selected_databases == ["abc123", "def456"]
            assert result.default_database == "abc123"

    @pytest.mark.asyncio
    async def test_returns_empty_for_different_user(self):
        """Should return empty for user without saved preferences"""
        mock_user = MagicMock()
        mock_user.sub = "different-user-456"

        saved_prefs = {
            "test-user-123": {
                "selected_databases": ["abc123"],
                "default_database": "abc123",
            }
        }

        with patch(
            "web.api.routes.settings_integrations._load_notion_preferences",
            return_value=saved_prefs,
        ):
            result = await get_notion_preferences(current_user=mock_user)

            assert result.selected_databases == []
            assert result.default_database is None


class TestSaveNotionPreferences:
    """Tests for POST /api/v1/settings/integrations/notion/preferences"""

    @pytest.mark.asyncio
    async def test_saves_preferences_successfully(self):
        """Should save preferences and return them"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        preferences = NotionPreferencesRequest(
            selected_databases=["abc123", "def456"],
            default_database="abc123",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_notion_preferences",
                return_value={},
            ),
            patch(
                "web.api.routes.settings_integrations._save_notion_preferences",
                side_effect=mock_save,
            ),
        ):
            result = await save_notion_preferences(preferences=preferences, current_user=mock_user)

            assert result.selected_databases == ["abc123", "def456"]
            assert result.default_database == "abc123"
            assert "test-user-123" in saved_data
            assert saved_data["test-user-123"]["selected_databases"] == [
                "abc123",
                "def456",
            ]

    @pytest.mark.asyncio
    async def test_overwrites_existing_preferences(self):
        """Should overwrite existing preferences for the user"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        existing_prefs = {
            "test-user-123": {
                "selected_databases": ["old-db"],
                "default_database": "old-db",
            }
        }

        new_preferences = NotionPreferencesRequest(
            selected_databases=["new-db"],
            default_database="new-db",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_notion_preferences",
                return_value=existing_prefs,
            ),
            patch(
                "web.api.routes.settings_integrations._save_notion_preferences",
                side_effect=mock_save,
            ),
        ):
            result = await save_notion_preferences(
                preferences=new_preferences, current_user=mock_user
            )

            assert result.selected_databases == ["new-db"]
            assert result.default_database == "new-db"
            assert saved_data["test-user-123"]["selected_databases"] == ["new-db"]

    @pytest.mark.asyncio
    async def test_preserves_other_users_preferences(self):
        """Should not affect other users' preferences"""
        mock_user = MagicMock()
        mock_user.sub = "test-user-123"

        existing_prefs = {
            "other-user-456": {
                "selected_databases": ["other-db"],
                "default_database": "other-db",
            }
        }

        new_preferences = NotionPreferencesRequest(
            selected_databases=["my-db"],
            default_database="my-db",
        )

        saved_data = {}

        def mock_save(prefs):
            saved_data.update(prefs)

        with (
            patch(
                "web.api.routes.settings_integrations._load_notion_preferences",
                return_value=existing_prefs,
            ),
            patch(
                "web.api.routes.settings_integrations._save_notion_preferences",
                side_effect=mock_save,
            ),
        ):
            await save_notion_preferences(preferences=new_preferences, current_user=mock_user)

            # Other user's preferences should be preserved
            assert "other-user-456" in saved_data
            assert saved_data["other-user-456"]["selected_databases"] == ["other-db"]
            # New user's preferences should be added
            assert "test-user-123" in saved_data
            assert saved_data["test-user-123"]["selected_databases"] == ["my-db"]


class TestNotionPreferencesFileStorage:
    """Tests for Notion preferences file-based storage helpers"""

    def test_load_preferences_returns_empty_when_file_missing(self):
        """Should return empty dict when preferences file doesn't exist"""
        from web.api.routes.settings_integrations import _load_notion_preferences

        with patch("os.path.exists", return_value=False):
            result = _load_notion_preferences()
            assert result == {}

    def test_load_preferences_returns_data_when_file_exists(self):
        """Should return parsed JSON when file exists"""
        import json

        from web.api.routes.settings_integrations import _load_notion_preferences

        test_data = {
            "user-123": {
                "selected_databases": ["db1"],
                "default_database": "db1",
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
            result = _load_notion_preferences()
            assert result == test_data

    def test_save_preferences_creates_directory(self):
        """Should create data directory if it doesn't exist"""
        from web.api.routes.settings_integrations import _save_notion_preferences

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
            _save_notion_preferences({"test": "data"})

            # Should call makedirs with exist_ok=True
            mock_makedirs.assert_called_once()
            assert mock_makedirs.call_args[1]["exist_ok"] is True
