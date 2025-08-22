"""
Tests for Preference API Endpoints
Phase 3: Integration & API Tests (Written First per TDD)

Created: 2025-08-20 by Enhanced Autonomy Mission
"""

import json
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.api.preference_endpoints import PreferenceAPI
from services.domain.user_preference_manager import UserPreferenceManager
from services.orchestration.session_persistence import SessionContextManager


@pytest.mark.asyncio
class TestGetUserPreferencesEndpoint:
    """Test GET /preferences endpoint"""

    async def test_get_user_preferences_endpoint(self):
        """Test retrieving user preferences via API"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "user_123"

        # Set up test preferences
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference("language", "en", user_id=user_id)

        # Call API endpoint
        response = await api.get_user_preferences(user_id=user_id)

        assert response["status"] == "success"
        assert "preferences" in response
        assert response["preferences"]["theme"] == "dark"
        assert response["preferences"]["language"] == "en"
        assert "metadata" in response

    async def test_get_user_preferences_with_session_context(self):
        """Test retrieving preferences with session context"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "user_123"
        session_id = "session_456"

        # Set preferences at different levels
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference("workspace", "backend", session_id=session_id)

        # Call API with session context
        response = await api.get_user_preferences(user_id=user_id, session_id=session_id)

        assert response["status"] == "success"
        assert response["preferences"]["theme"] == "dark"
        assert response["preferences"]["workspace"] == "backend"
        assert response["metadata"]["session_id"] == session_id

    async def test_get_user_preferences_not_found(self):
        """Test API response when user has no preferences"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "nonexistent_user"

        response = await api.get_user_preferences(user_id=user_id)

        assert response["status"] == "success"
        assert response["preferences"] == {}
        assert response["metadata"]["user_id"] == user_id

    async def test_get_user_preferences_error_handling(self):
        """Test API error handling"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        # Mock an error in preference manager
        with patch.object(
            preference_manager, "get_all_preferences", side_effect=Exception("Database error")
        ):
            response = await api.get_user_preferences(user_id="user_123")

            assert response["status"] == "error"
            assert "error_message" in response
            assert "Database error" in response["error_message"]


@pytest.mark.asyncio
class TestUpdateUserPreferencesEndpoint:
    """Test PUT/PATCH /preferences endpoint"""

    async def test_update_user_preferences_endpoint(self):
        """Test updating user preferences via API"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "user_123"
        preferences_data = {
            "theme": "light",
            "notifications": {"email": True, "push": False},
            "display_settings": {"sidebar_collapsed": True},
        }

        # Call API endpoint
        response = await api.update_user_preferences(user_id=user_id, preferences=preferences_data)

        assert response["status"] == "success"
        assert "updated_count" in response
        assert response["updated_count"] == 3

        # Verify preferences were saved
        theme = await preference_manager.get_preference("theme", user_id=user_id)
        notifications = await preference_manager.get_preference("notifications", user_id=user_id)

        assert theme == "light"
        assert notifications == {"email": True, "push": False}

    async def test_update_session_preferences(self):
        """Test updating session-specific preferences"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        session_id = "session_456"
        session_preferences = {
            "current_project": "piper-morgan",
            "workspace_layout": "split_view",
            "temp_settings": {"auto_save": True},
        }

        response = await api.update_session_preferences(
            session_id=session_id, preferences=session_preferences
        )

        assert response["status"] == "success"
        assert response["updated_count"] == 3

        # Verify session preferences
        project = await preference_manager.get_preference("current_project", session_id=session_id)
        layout = await preference_manager.get_preference("workspace_layout", session_id=session_id)

        assert project == "piper-morgan"
        assert layout == "split_view"

    async def test_update_preferences_validation(self):
        """Test preference validation in API"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "user_123"

        # Test with invalid JSON-serializable data
        import datetime

        invalid_preferences = {
            "theme": "dark",
            "created_at": datetime.datetime.now(),  # Not JSON serializable
        }

        response = await api.update_user_preferences(
            user_id=user_id, preferences=invalid_preferences
        )

        assert response["status"] == "error"
        assert "validation_error" in response["error_type"]

    async def test_update_preferences_partial_failure(self):
        """Test partial failure handling in preference updates"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "user_123"

        # Mock partial failure
        with patch.object(preference_manager, "set_preference") as mock_set:
            mock_set.side_effect = [True, False, True]  # Second preference fails

            preferences_data = {"setting1": "value1", "setting2": "value2", "setting3": "value3"}

            response = await api.update_user_preferences(
                user_id=user_id, preferences=preferences_data
            )

            assert response["status"] == "partial_success"
            assert response["updated_count"] == 2
            assert response["failed_count"] == 1
            assert "failed_preferences" in response


@pytest.mark.asyncio
class TestSessionContextEndpoint:
    """Test session context management endpoints"""

    async def test_get_session_context_endpoint(self):
        """Test retrieving complete session context"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "user_123"
        session_id = "session_456"

        # Set up context
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference("project", "piper-morgan", session_id=session_id)

        response = await api.get_session_context(session_id=session_id, user_id=user_id)

        assert response["status"] == "success"
        assert "context" in response
        assert "user_preferences" in response["context"]
        assert "session_preferences" in response["context"]
        assert response["context"]["user_preferences"]["theme"] == "dark"
        assert response["context"]["session_preferences"]["project"] == "piper-morgan"

    async def test_update_session_context_endpoint(self):
        """Test updating complete session context"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        session_id = "session_456"
        user_id = "user_123"

        context_data = {
            "user_preferences": {"theme": "light", "language": "es"},
            "session_preferences": {"project": "new-project", "mode": "development"},
            "metadata": {"updated_by": "api_test"},
        }

        response = await api.update_session_context(
            session_id=session_id, user_id=user_id, context_data=context_data
        )

        assert response["status"] == "success"

        # Verify context was updated
        theme = await preference_manager.get_preference("theme", user_id=user_id)
        project = await preference_manager.get_preference("project", session_id=session_id)

        assert theme == "light"
        assert project == "new-project"

    async def test_clear_session_context_endpoint(self):
        """Test clearing session context"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        session_id = "session_456"

        # Set up session preferences
        await preference_manager.set_preference("temp1", "value1", session_id=session_id)
        await preference_manager.set_preference("temp2", "value2", session_id=session_id)

        # Clear session context
        response = await api.clear_session_context(session_id=session_id)

        assert response["status"] == "success"

        # Verify preferences were cleared
        temp1 = await preference_manager.get_preference("temp1", session_id=session_id)
        temp2 = await preference_manager.get_preference("temp2", session_id=session_id)

        assert temp1 is None
        assert temp2 is None


@pytest.mark.asyncio
class TestPreferenceValidation:
    """Test API validation and error handling"""

    async def test_preference_validation(self):
        """Test comprehensive preference validation"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        # Test invalid user ID
        response = await api.get_user_preferences(user_id="")
        assert response["status"] == "error"
        assert "user_id" in response["error_message"]

        # Test invalid session ID format
        response = await api.get_session_context(session_id="", user_id="valid_user")
        assert response["status"] == "error"
        assert "session_id" in response["error_message"]

    async def test_preference_value_validation(self):
        """Test preference value validation rules"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "user_123"

        # Test preference key validation
        invalid_preferences = {
            "": "empty_key",  # Empty key
            "valid_key": "valid_value",
            123: "numeric_key",  # Non-string key
        }

        response = await api.update_user_preferences(
            user_id=user_id, preferences=invalid_preferences
        )

        assert response["status"] == "partial_success" or response["status"] == "error"
        assert "validation_errors" in response or "error_message" in response

    async def test_api_authentication_integration(self):
        """Test API integration with authentication (mock)"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        # Mock authentication check
        with patch.object(api, "_validate_user_access") as mock_auth:
            mock_auth.return_value = False

            response = await api.get_user_preferences(
                user_id="user_123", requesting_user_id="different_user"
            )

            assert response["status"] == "error"
            assert "unauthorized" in response["error_type"]

    async def test_rate_limiting_simulation(self):
        """Test API rate limiting behavior"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "user_123"

        # Mock rate limiting
        with patch.object(api, "_check_rate_limit") as mock_rate_limit:
            mock_rate_limit.return_value = False

            response = await api.get_user_preferences(user_id=user_id)

            assert response["status"] == "error"
            assert "rate_limit" in response["error_type"]


@pytest.mark.asyncio
class TestAPIPerformance:
    """Test API performance requirements"""

    async def test_preference_api_performance(self):
        """Test that API endpoints meet performance requirements"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "perf_user"

        # Set up test data
        large_preferences = {f"setting_{i}": f"value_{i}" for i in range(100)}

        # Test update performance
        start_time = datetime.now()
        response = await api.update_user_preferences(user_id=user_id, preferences=large_preferences)
        end_time = datetime.now()

        update_duration = (end_time - start_time).total_seconds() * 1000

        assert response["status"] == "success"
        assert update_duration < 1000  # Should complete in <1 second

        # Test retrieval performance
        start_time = datetime.now()
        response = await api.get_user_preferences(user_id=user_id)
        end_time = datetime.now()

        get_duration = (end_time - start_time).total_seconds() * 1000

        assert response["status"] == "success"
        assert get_duration < 200  # Should complete in <200ms
        assert len(response["preferences"]) == 100

    async def test_concurrent_api_requests(self):
        """Test concurrent API request handling"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "concurrent_user"

        # Simulate concurrent requests
        import asyncio

        async def make_request(i):
            return await api.update_user_preferences(
                user_id=user_id, preferences={f"concurrent_setting_{i}": f"value_{i}"}
            )

        # Run concurrent requests
        tasks = [make_request(i) for i in range(10)]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # All requests should succeed
        success_count = sum(
            1 for r in results if isinstance(r, dict) and r.get("status") == "success"
        )
        assert success_count >= 8  # At least 80% should succeed under concurrent load


@pytest.mark.asyncio
class TestAPIIntegrationWithSessionManager:
    """Test API integration with SessionContextManager"""

    async def test_api_session_manager_integration(self):
        """Test API integration with SessionContextManager"""
        session_manager = SessionContextManager()
        api = PreferenceAPI(session_manager.preference_manager, session_manager)

        user_id = "integration_user"
        session_id = "integration_session"

        # Create session through context manager
        session = await session_manager.get_or_create_session_with_context(
            session_id=session_id, user_id=user_id
        )

        # Update preferences through API
        preferences = {"api_test": "integration_value"}
        response = await api.update_user_preferences(user_id=user_id, preferences=preferences)

        assert response["status"] == "success"

        # Verify integration worked
        value = await session_manager.preference_manager.get_preference("api_test", user_id=user_id)
        assert value == "integration_value"

    async def test_api_persistence_integration(self):
        """Test API integration with persistence layer"""
        session_manager = SessionContextManager()
        api = PreferenceAPI(session_manager.preference_manager, session_manager)

        user_id = "persistence_user"
        session_id = "persistence_session"

        # Set preferences through API
        preferences = {"persistent_setting": "persistent_value"}
        response = await api.update_user_preferences(user_id=user_id, preferences=preferences)
        assert response["status"] == "success"

        # Create session and verify persistence
        session = await session_manager.get_or_create_session_with_context(
            session_id=session_id, user_id=user_id, restore_context=True
        )

        # End session with persistence
        result = await session_manager.end_session_with_persistence(session, user_id=user_id)
        assert result is True

        # Create new session and verify preferences persisted
        new_session = await session_manager.get_or_create_session_with_context(
            session_id=f"{session_id}_new", user_id=user_id, restore_context=True
        )

        # Preferences should be available in new session
        persistent_value = await session_manager.preference_manager.get_preference(
            "persistent_setting", user_id=user_id
        )
        assert persistent_value == "persistent_value"
