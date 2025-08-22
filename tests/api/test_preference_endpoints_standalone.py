"""
Standalone tests for Preference API Endpoints
Phase 3: Database-free API validation

Created: 2025-08-20 by Enhanced Autonomy Mission
"""

import asyncio
from datetime import datetime

import pytest

from services.api.preference_endpoints import PreferenceAPI
from services.domain.user_preference_manager import UserPreferenceManager
from services.orchestration.session_persistence import SessionContextManager


@pytest.mark.asyncio
class TestPreferenceAPIStandalone:
    """Standalone tests for preference API functionality"""

    async def test_get_user_preferences_endpoint(self):
        """Test GET preferences API endpoint"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "test_user_123"

        # Set up test preferences
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference("language", "en", user_id=user_id)

        # Call API
        response = await api.get_user_preferences(user_id=user_id)

        assert response["status"] == "success"
        assert "preferences" in response
        assert response["preferences"]["theme"] == "dark"
        assert response["preferences"]["language"] == "en"
        assert "metadata" in response
        assert response["metadata"]["user_id"] == user_id

    async def test_update_user_preferences_endpoint(self):
        """Test PUT preferences API endpoint"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "test_user_123"
        preferences = {
            "theme": "light",
            "notifications": {"email": True, "push": False},
            "display_settings": {"sidebar_collapsed": True},
        }

        # Call API
        response = await api.update_user_preferences(user_id=user_id, preferences=preferences)

        assert response["status"] == "success"
        assert response["updated_count"] == 3
        assert response["failed_count"] == 0

        # Verify preferences were saved
        theme = await preference_manager.get_preference("theme", user_id=user_id)
        notifications = await preference_manager.get_preference("notifications", user_id=user_id)

        assert theme == "light"
        assert notifications == {"email": True, "push": False}

    async def test_session_preferences_endpoint(self):
        """Test session preferences API endpoint"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        session_id = "test_session_456"
        session_preferences = {"current_project": "piper-morgan", "workspace_layout": "split_view"}

        # Update session preferences
        response = await api.update_session_preferences(
            session_id=session_id, preferences=session_preferences
        )

        assert response["status"] == "success"
        assert response["updated_count"] == 2

        # Verify session preferences
        project = await preference_manager.get_preference("current_project", session_id=session_id)
        layout = await preference_manager.get_preference("workspace_layout", session_id=session_id)

        assert project == "piper-morgan"
        assert layout == "split_view"

    async def test_get_session_context_endpoint(self):
        """Test GET session context API endpoint"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "test_user_123"
        session_id = "test_session_456"

        # Set up context
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference("project", "piper-morgan", session_id=session_id)

        # Call API
        response = await api.get_session_context(session_id=session_id, user_id=user_id)

        assert response["status"] == "success"
        assert "context" in response
        assert "user_preferences" in response["context"]
        assert "session_preferences" in response["context"]
        assert response["context"]["user_preferences"]["theme"] == "dark"
        assert response["context"]["session_preferences"]["project"] == "piper-morgan"

    async def test_clear_session_context_endpoint(self):
        """Test DELETE session context API endpoint"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        session_id = "test_session_456"

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
class TestAPIValidationStandalone:
    """Test API validation and error handling"""

    async def test_invalid_user_id_validation(self):
        """Test API validation for invalid user IDs"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        # Test empty user ID
        response = await api.get_user_preferences(user_id="")
        assert response["status"] == "error"
        assert "user_id" in response["error_message"]

        # Test empty session ID
        response = await api.get_session_context(session_id="", user_id="valid_user")
        assert response["status"] == "error"
        assert "session_id" in response["error_message"]

    async def test_preference_validation(self):
        """Test preference value validation"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "test_user"

        # Test invalid preferences (non-JSON serializable)
        import datetime

        invalid_preferences = {
            "valid_key": "valid_value",
            "invalid_key": datetime.datetime.now(),  # Not JSON serializable
        }

        response = await api.update_user_preferences(
            user_id=user_id, preferences=invalid_preferences
        )

        # Should have partial success or error
        assert response["status"] in ["partial_success", "error"]
        if response["status"] == "partial_success":
            assert response["updated_count"] >= 1
            assert response["failed_count"] >= 1

    async def test_empty_preferences_validation(self):
        """Test validation for empty preferences"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "test_user"

        # Test empty preferences dict
        response = await api.update_user_preferences(user_id=user_id, preferences={})
        assert response["status"] == "error"
        assert "empty" in response["error_message"]


@pytest.mark.asyncio
class TestAPIPerformanceStandalone:
    """Test API performance requirements"""

    async def test_api_performance_requirements(self):
        """Test that API endpoints meet performance requirements"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "perf_user"

        # Test with moderate number of preferences
        preferences = {f"setting_{i}": f"value_{i}" for i in range(20)}

        # Test update performance
        start_time = datetime.now()
        response = await api.update_user_preferences(user_id=user_id, preferences=preferences)
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
        assert len(response["preferences"]) == 20

    async def test_session_context_performance(self):
        """Test session context API performance"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "perf_user"
        session_id = "perf_session"

        # Set up test data
        await preference_manager.set_preference("user_pref", "user_value", user_id=user_id)
        await preference_manager.set_preference(
            "session_pref", "session_value", session_id=session_id
        )

        # Test session context retrieval performance
        start_time = datetime.now()
        response = await api.get_session_context(session_id=session_id, user_id=user_id)
        end_time = datetime.now()

        duration = (end_time - start_time).total_seconds() * 1000

        assert response["status"] == "success"
        assert duration < 500  # Should complete in <500ms


@pytest.mark.asyncio
class TestAPIHealthCheckStandalone:
    """Test API health check functionality"""

    async def test_health_check_endpoint(self):
        """Test API health check endpoint"""
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        response = await api.health_check()

        assert response["status"] == "healthy"
        assert "timestamp" in response
        assert "performance" in response
        assert "configuration" in response
        assert response["performance"]["preference_test_duration_ms"] < 100


@pytest.mark.asyncio
class TestAPISessionManagerIntegration:
    """Test API integration with SessionContextManager"""

    async def test_api_with_session_manager(self):
        """Test API integration with session context manager"""
        session_manager = SessionContextManager()
        api = PreferenceAPI(session_manager.preference_manager, session_manager)

        user_id = "integration_user"
        session_id = "integration_session"

        # Update preferences through API
        preferences = {"api_integration": "test_value"}
        response = await api.update_user_preferences(user_id=user_id, preferences=preferences)

        assert response["status"] == "success"

        # Create session and verify integration
        session = await session_manager.get_or_create_session_with_context(
            session_id=session_id, user_id=user_id
        )

        # Verify preference is accessible through session manager
        value = await session_manager.preference_manager.get_preference(
            "api_integration", user_id=user_id
        )
        assert value == "test_value"


# Simple test runner for standalone execution
if __name__ == "__main__":

    async def run_tests():
        """Run key API tests manually"""
        print("🧪 Running Preference API standalone tests...")

        # Test basic API functionality
        preference_manager = UserPreferenceManager()
        api = PreferenceAPI(preference_manager)

        user_id = "test_user"

        # Test preferences update
        preferences = {"theme": "dark", "language": "en"}
        response = await api.update_user_preferences(user_id=user_id, preferences=preferences)
        assert response["status"] == "success"
        print("✅ Update preferences test passed")

        # Test preferences retrieval
        response = await api.get_user_preferences(user_id=user_id)
        assert response["status"] == "success"
        assert response["preferences"]["theme"] == "dark"
        print("✅ Get preferences test passed")

        # Test session context
        session_id = "test_session"
        session_prefs = {"project": "piper-morgan"}
        response = await api.update_session_preferences(
            session_id=session_id, preferences=session_prefs
        )
        assert response["status"] == "success"
        print("✅ Session preferences test passed")

        # Test session context retrieval
        response = await api.get_session_context(session_id=session_id, user_id=user_id)
        assert response["status"] == "success"
        print("✅ Session context test passed")

        # Test health check
        response = await api.health_check()
        assert response["status"] == "healthy"
        print("✅ Health check test passed")

        print("🎉 All API standalone tests passed!")

    asyncio.run(run_tests())
