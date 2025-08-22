"""
Standalone tests for UserPreferenceManager (no database dependencies)
Phase 1: Core Infrastructure Tests - Database-free execution

Created: 2025-08-20 by Enhanced Autonomy Mission
"""

import asyncio
from datetime import datetime

import pytest

# Import the manager directly without conftest database fixtures
from services.domain.user_preference_manager import PreferenceItem, UserPreferenceManager
from services.session.session_manager import ConversationSession


class TestUserPreferenceManagerInitialization:
    """Test UserPreferenceManager initialization and basic setup"""

    def test_user_preference_manager_initialization(self):
        """Test that UserPreferenceManager initializes correctly"""
        manager = UserPreferenceManager()

        assert manager is not None
        assert hasattr(manager, "global_preferences")
        assert hasattr(manager, "user_preferences")
        assert hasattr(manager, "session_preferences")
        assert isinstance(manager.global_preferences, dict)
        assert isinstance(manager.user_preferences, dict)
        assert isinstance(manager.session_preferences, dict)


class TestPreferenceItem:
    """Test PreferenceItem dataclass functionality"""

    def test_preference_item_creation(self):
        """Test creating a preference item"""
        item = PreferenceItem(value="test_value")

        assert item.value == "test_value"
        assert isinstance(item.created_at, datetime)
        assert isinstance(item.updated_at, datetime)
        assert isinstance(item.version, datetime)
        assert item.ttl_minutes is None

    def test_preference_item_expiration(self):
        """Test preference item expiration logic"""
        # Non-expiring item
        item1 = PreferenceItem(value="test")
        assert item1.is_expired() is False

        # Item with TTL
        item2 = PreferenceItem(value="test", ttl_minutes=60)
        assert item2.is_expired() is False

    def test_preference_item_serialization(self):
        """Test preference item to/from dict conversion"""
        item = PreferenceItem(value={"complex": "data"}, ttl_minutes=30)

        # Convert to dict
        data = item.to_dict()
        assert data["value"] == {"complex": "data"}
        assert data["ttl_minutes"] == 30
        assert "created_at" in data
        assert "version" in data

        # Convert back from dict
        item2 = PreferenceItem.from_dict(data)
        assert item2.value == {"complex": "data"}
        assert item2.ttl_minutes == 30


@pytest.mark.asyncio
class TestUserPreferenceStorage:
    """Test core preference storage functionality"""

    async def test_store_global_preference(self):
        """Test storing global system preferences"""
        manager = UserPreferenceManager()
        key = "default_theme"
        value = "dark"

        result = await manager.set_preference(key, value, scope="global")

        assert result is True
        stored_value = await manager.get_preference(key, scope="global")
        assert stored_value == value

    async def test_store_user_preference(self):
        """Test storing user-specific preferences"""
        manager = UserPreferenceManager()
        key = "notification_frequency"
        value = "daily"
        user_id = "user_123"

        result = await manager.set_preference(key, value, user_id=user_id)

        assert result is True
        stored_value = await manager.get_preference(key, user_id=user_id)
        assert stored_value == value

    async def test_store_session_preference(self):
        """Test storing session-specific preferences"""
        manager = UserPreferenceManager()
        key = "current_project"
        value = "piper-morgan"
        session_id = "session_456"

        result = await manager.set_preference(key, value, session_id=session_id)

        assert result is True
        stored_value = await manager.get_preference(key, session_id=session_id)
        assert stored_value == value


@pytest.mark.asyncio
class TestUserPreferenceRetrieval:
    """Test preference retrieval with defaults and hierarchy"""

    async def test_retrieve_user_preference_with_default(self):
        """Test retrieving non-existent preference returns default"""
        manager = UserPreferenceManager()
        key = "nonexistent_key"
        default_value = "default_value"
        user_id = "user_123"

        result = await manager.get_preference(key, user_id=user_id, default=default_value)

        assert result == default_value

    async def test_retrieve_preference_without_default(self):
        """Test retrieving non-existent preference without default returns None"""
        manager = UserPreferenceManager()
        key = "nonexistent_key"
        user_id = "user_123"

        result = await manager.get_preference(key, user_id=user_id)

        assert result is None

    async def test_get_all_user_preferences(self):
        """Test retrieving all preferences for a user"""
        manager = UserPreferenceManager()
        user_id = "user_123"

        # Store multiple preferences
        await manager.set_preference("theme", "dark", user_id=user_id)
        await manager.set_preference("language", "en", user_id=user_id)

        all_prefs = await manager.get_all_preferences(user_id=user_id)

        assert isinstance(all_prefs, dict)
        assert all_prefs["theme"] == "dark"
        assert all_prefs["language"] == "en"


@pytest.mark.asyncio
class TestPreferenceInheritanceHierarchy:
    """Test hierarchical preference inheritance (global → user → session)"""

    async def test_preference_inheritance_hierarchy(self):
        """Test that session preferences override user preferences override global"""
        manager = UserPreferenceManager()
        key = "theme"
        user_id = "user_123"
        session_id = "session_456"

        # Set preferences at different levels
        await manager.set_preference(key, "light", scope="global")
        await manager.set_preference(key, "dark", user_id=user_id)
        await manager.set_preference(key, "blue", session_id=session_id)

        # Test inheritance priority
        global_value = await manager.get_preference(key, scope="global")
        user_value = await manager.get_preference(key, user_id=user_id)
        session_value = await manager.get_preference(key, session_id=session_id)

        assert global_value == "light"
        assert user_value == "dark"  # User overrides global
        assert session_value == "blue"  # Session overrides user

    async def test_merged_preferences_hierarchy(self):
        """Test that merge_preferences correctly applies hierarchy"""
        manager = UserPreferenceManager()
        user_id = "user_123"
        session_id = "session_456"

        # Set preferences at different levels
        await manager.set_preference("global_setting", "global_value", scope="global")
        await manager.set_preference("user_setting", "user_value", user_id=user_id)
        await manager.set_preference("theme", "user_theme", user_id=user_id)
        await manager.set_preference("theme", "session_theme", session_id=session_id)

        merged = await manager.merge_preferences(user_id=user_id, session_id=session_id)

        assert merged["global_setting"] == "global_value"
        assert merged["user_setting"] == "user_value"
        assert merged["theme"] == "session_theme"  # Session overrides user


@pytest.mark.asyncio
class TestJSONSerializationDeserialization:
    """Test JSON serialization for database storage"""

    async def test_json_serialization_deserialization(self):
        """Test that complex preference values can be JSON serialized/deserialized"""
        manager = UserPreferenceManager()
        user_id = "user_123"
        complex_preference = {
            "ui_settings": {
                "theme": "dark",
                "sidebar_collapsed": False,
                "recent_files": ["file1.py", "file2.md"],
            },
            "workflow_preferences": {"auto_save": True, "git_auto_commit": False},
        }

        # Store complex preference
        await manager.set_preference("complex_config", complex_preference, user_id=user_id)

        # Retrieve and verify
        retrieved = await manager.get_preference("complex_config", user_id=user_id)

        assert retrieved == complex_preference
        assert isinstance(retrieved["ui_settings"]["recent_files"], list)
        assert retrieved["workflow_preferences"]["auto_save"] is True

    async def test_preference_serialization_to_context_format(self):
        """Test that preferences can be serialized to ConversationSession.context format"""
        manager = UserPreferenceManager()
        user_id = "user_123"
        session_id = "session_456"

        # Set various preferences
        await manager.set_preference("theme", "dark", user_id=user_id)
        await manager.set_preference("language", "en", user_id=user_id)
        await manager.set_preference("current_project", "piper-morgan", session_id=session_id)

        # Get context-compatible format
        context_data = await manager.get_context_format(user_id=user_id, session_id=session_id)

        assert "user_preferences" in context_data
        assert "session_preferences" in context_data
        assert "context_version" in context_data
        assert "last_updated" in context_data
        assert context_data["user_preferences"]["theme"] == "dark"
        assert context_data["session_preferences"]["current_project"] == "piper-morgan"


@pytest.mark.asyncio
class TestSessionPreferenceCleanup:
    """Test session preference cleanup and management"""

    async def test_clear_session_preferences(self):
        """Test clearing all preferences for a session"""
        manager = UserPreferenceManager()
        session_id = "session_456"

        # Set multiple session preferences
        await manager.set_preference("theme", "dark", session_id=session_id)
        await manager.set_preference("project", "piper-morgan", session_id=session_id)

        # Verify preferences exist
        theme = await manager.get_preference("theme", session_id=session_id)
        project = await manager.get_preference("project", session_id=session_id)
        assert theme == "dark"
        assert project == "piper-morgan"

        # Clear session preferences
        result = await manager.clear_session_preferences(session_id)

        assert result is True

        # Verify preferences are cleared
        theme_after = await manager.get_preference("theme", session_id=session_id)
        project_after = await manager.get_preference("project", session_id=session_id)
        assert theme_after is None
        assert project_after is None


@pytest.mark.asyncio
class TestIntegrationWithConversationSession:
    """Test integration with existing ConversationSession"""

    async def test_integration_with_conversation_session(self):
        """Test that preferences integrate with ConversationSession.context"""
        manager = UserPreferenceManager()
        session = ConversationSession("test_session_123")
        user_id = "user_123"

        # Set user preferences
        await manager.set_preference("theme", "dark", user_id=user_id)
        await manager.set_preference("language", "en", user_id=user_id)

        # Update session context with user preferences
        result = await manager.update_session_context(session, user_id=user_id)

        assert result is True
        assert "user_preferences" in session.context
        assert session.context["user_preferences"]["theme"] == "dark"
        assert session.context["user_preferences"]["language"] == "en"


# Simple test runner for standalone execution
if __name__ == "__main__":
    import asyncio

    async def run_tests():
        """Run a few key tests manually"""
        print("🧪 Running UserPreferenceManager standalone tests...")

        # Test initialization
        manager = UserPreferenceManager()
        print("✅ Initialization test passed")

        # Test preference storage and retrieval
        await manager.set_preference("test_key", "test_value", user_id="user123")
        value = await manager.get_preference("test_key", user_id="user123")
        assert value == "test_value"
        print("✅ Storage/retrieval test passed")

        # Test hierarchy
        await manager.set_preference("theme", "global_theme", scope="global")
        await manager.set_preference("theme", "user_theme", user_id="user123")
        await manager.set_preference("theme", "session_theme", session_id="session456")

        global_theme = await manager.get_preference("theme", scope="global")
        user_theme = await manager.get_preference("theme", user_id="user123")
        session_theme = await manager.get_preference("theme", session_id="session456")

        assert global_theme == "global_theme"
        assert user_theme == "user_theme"
        assert session_theme == "session_theme"
        print("✅ Hierarchy test passed")

        print("🎉 All standalone tests passed!")

    asyncio.run(run_tests())
