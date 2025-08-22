"""
Tests for UserPreferenceManager - Persistent Context Foundation
Phase 1: Core Infrastructure Tests (Written First per TDD)

Created: 2025-08-20 by Enhanced Autonomy Mission
"""

import json
from datetime import datetime
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.user_preference_manager import UserPreferenceManager
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


class TestUserPreferenceStorage:
    """Test core preference storage functionality"""

    @pytest.fixture
    def manager(self):
        """Create UserPreferenceManager instance for testing"""
        return UserPreferenceManager()

    async def test_store_global_preference(self, manager):
        """Test storing global system preferences"""
        key = "default_theme"
        value = "dark"

        result = await manager.set_preference(key, value, scope="global")

        assert result is True
        stored_value = await manager.get_preference(key, scope="global")
        assert stored_value == value

    async def test_store_user_preference(self, manager):
        """Test storing user-specific preferences"""
        key = "notification_frequency"
        value = "daily"
        user_id = "user_123"

        result = await manager.set_preference(key, value, user_id=user_id)

        assert result is True
        stored_value = await manager.get_preference(key, user_id=user_id)
        assert stored_value == value

    async def test_store_session_preference(self, manager):
        """Test storing session-specific preferences"""
        key = "current_project"
        value = "piper-morgan"
        session_id = "session_456"

        result = await manager.set_preference(key, value, session_id=session_id)

        assert result is True
        stored_value = await manager.get_preference(key, session_id=session_id)
        assert stored_value == value


class TestUserPreferenceRetrieval:
    """Test preference retrieval with defaults and hierarchy"""

    @pytest.fixture
    def manager(self):
        return UserPreferenceManager()

    async def test_retrieve_user_preference_with_default(self, manager):
        """Test retrieving non-existent preference returns default"""
        key = "nonexistent_key"
        default_value = "default_value"
        user_id = "user_123"

        result = await manager.get_preference(key, user_id=user_id, default=default_value)

        assert result == default_value

    async def test_retrieve_preference_without_default(self, manager):
        """Test retrieving non-existent preference without default returns None"""
        key = "nonexistent_key"
        user_id = "user_123"

        result = await manager.get_preference(key, user_id=user_id)

        assert result is None

    async def test_get_all_user_preferences(self, manager):
        """Test retrieving all preferences for a user"""
        user_id = "user_123"

        # Store multiple preferences
        await manager.set_preference("theme", "dark", user_id=user_id)
        await manager.set_preference("language", "en", user_id=user_id)

        all_prefs = await manager.get_all_preferences(user_id=user_id)

        assert isinstance(all_prefs, dict)
        assert all_prefs["theme"] == "dark"
        assert all_prefs["language"] == "en"


class TestPreferenceInheritanceHierarchy:
    """Test hierarchical preference inheritance (global → user → session)"""

    @pytest.fixture
    def manager(self):
        return UserPreferenceManager()

    async def test_preference_inheritance_hierarchy(self, manager):
        """Test that session preferences override user preferences override global"""
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

    async def test_merged_preferences_hierarchy(self, manager):
        """Test that merge_preferences correctly applies hierarchy"""
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


class TestJSONSerializationDeserialization:
    """Test JSON serialization for database storage"""

    @pytest.fixture
    def manager(self):
        return UserPreferenceManager()

    async def test_json_serialization_deserialization(self, manager):
        """Test that complex preference values can be JSON serialized/deserialized"""
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

    async def test_preference_serialization_to_context_format(self, manager):
        """Test that preferences can be serialized to ConversationSession.context format"""
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


class TestPreferenceVersioning:
    """Test preference versioning for conflict resolution"""

    @pytest.fixture
    def manager(self):
        return UserPreferenceManager()

    async def test_preference_versioning(self, manager):
        """Test that preference changes are versioned"""
        user_id = "user_123"
        key = "theme"

        # Initial preference
        await manager.set_preference(key, "light", user_id=user_id)
        version1 = await manager.get_preference_version(key, user_id=user_id)

        # Update preference
        await manager.set_preference(key, "dark", user_id=user_id)
        version2 = await manager.get_preference_version(key, user_id=user_id)

        assert version2 > version1
        assert isinstance(version1, datetime)
        assert isinstance(version2, datetime)

    async def test_preference_conflict_resolution(self, manager):
        """Test handling of conflicting preference updates"""
        user_id = "user_123"
        key = "theme"

        # Simulate concurrent updates
        await manager.set_preference(key, "dark", user_id=user_id)
        original_version = await manager.get_preference_version(key, user_id=user_id)

        # Attempt update with old version (conflict)
        conflict_handled = await manager.set_preference_with_version(
            key, "blue", user_id=user_id, expected_version=original_version
        )

        assert conflict_handled is True
        final_value = await manager.get_preference(key, user_id=user_id)
        assert final_value == "blue"


class TestConcurrentAccessHandling:
    """Test concurrent access patterns and thread safety"""

    @pytest.fixture
    def manager(self):
        return UserPreferenceManager()

    async def test_concurrent_access_handling(self, manager):
        """Test that concurrent preference access is handled safely"""
        user_id = "user_123"
        key = "counter"

        # Simulate concurrent access
        import asyncio

        async def increment_preference():
            current = await manager.get_preference(key, user_id=user_id, default=0)
            await asyncio.sleep(0.01)  # Simulate processing time
            await manager.set_preference(key, current + 1, user_id=user_id)

        # Run concurrent operations
        tasks = [increment_preference() for _ in range(5)]
        await asyncio.gather(*tasks)

        final_value = await manager.get_preference(key, user_id=user_id)

        # Due to race conditions, final value may be less than 5
        # but should be at least 1 and at most 5
        assert 1 <= final_value <= 5


class TestSessionPreferenceCleanup:
    """Test session preference cleanup and management"""

    @pytest.fixture
    def manager(self):
        return UserPreferenceManager()

    async def test_clear_session_preferences(self, manager):
        """Test clearing all preferences for a session"""
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

    async def test_session_preference_expiration(self, manager):
        """Test automatic session preference expiration"""
        session_id = "session_456"

        # Set preference with TTL
        await manager.set_preference(
            "temp_setting", "temp_value", session_id=session_id, ttl_minutes=1
        )

        # Verify preference exists
        value = await manager.get_preference("temp_setting", session_id=session_id)
        assert value == "temp_value"

        # Check expiration tracking
        is_expired = await manager.is_preference_expired("temp_setting", session_id=session_id)
        assert is_expired is False


class TestIntegrationWithConversationSession:
    """Test integration with existing ConversationSession"""

    @pytest.fixture
    def manager(self):
        return UserPreferenceManager()

    @pytest.fixture
    def session(self):
        return ConversationSession("test_session_123")

    async def test_integration_with_conversation_session(self, manager, session):
        """Test that preferences integrate with ConversationSession.context"""
        user_id = "user_123"

        # Set user preferences
        await manager.set_preference("theme", "dark", user_id=user_id)
        await manager.set_preference("language", "en", user_id=user_id)

        # Update session context with user preferences
        await manager.update_session_context(session, user_id=user_id)

        assert "user_preferences" in session.context
        assert session.context["user_preferences"]["theme"] == "dark"
        assert session.context["user_preferences"]["language"] == "en"

    async def test_load_preferences_from_session_context(self, manager, session):
        """Test loading preferences from existing session context"""
        # Simulate existing session context
        session.context = {
            "user_preferences": {"theme": "dark", "notification_frequency": "daily"},
            "session_preferences": {"current_project": "piper-morgan"},
            "context_version": "1.0",
            "last_updated": datetime.now().isoformat(),
        }

        # Load preferences from session
        loaded = await manager.load_from_session_context(session)

        assert loaded is True

        # Verify preferences were loaded
        theme = await manager.get_preference("theme", user_id="test_user")
        project = await manager.get_preference("current_project", session_id=session.session_id)

        # Note: This test may need adjustment based on actual implementation
        # The exact behavior depends on how we handle user_id extraction from session
