"""
Standalone tests for Session Persistence & Context Inheritance
Phase 2: Database-free execution validation

Created: 2025-08-20 by Enhanced Autonomy Mission
"""

import asyncio
from datetime import datetime

import pytest

from services.domain.user_preference_manager import UserPreferenceManager
from services.orchestration.session_persistence import (
    SessionContextManager,
    SessionPersistenceManager,
)
from services.session.session_manager import ConversationSession


@pytest.mark.asyncio
class TestSessionPersistenceStandalone:
    """Standalone tests for session persistence functionality"""

    async def test_session_context_persistence_basic(self):
        """Test basic session context persistence functionality"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        session = ConversationSession("test_session_123")
        user_id = "user_456"

        # Set preferences
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference(
            "project", "piper-morgan", session_id=session.session_id
        )
        await preference_manager.update_session_context(session, user_id=user_id)

        # Persist session context
        result = await persistence_manager.save_session_context(session, user_id=user_id)
        assert result is True

        # Verify context was persisted
        persisted_data = await persistence_manager.get_persisted_context(session.session_id)
        assert persisted_data is not None
        assert "context_data" in persisted_data
        assert persisted_data["user_id"] == user_id

    async def test_session_context_restoration(self):
        """Test session context restoration"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        # First session - save context
        session1 = ConversationSession("test_session_123")
        user_id = "user_456"

        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference("language", "en", user_id=user_id)
        await persistence_manager.save_session_context(session1, user_id=user_id)

        # Second session - restore context
        session2 = ConversationSession("test_session_123")  # Same session ID
        result = await persistence_manager.restore_session_context(session2, user_id=user_id)

        assert result is True

        # Verify preferences were restored
        theme = await preference_manager.get_preference("theme", user_id=user_id)
        language = await preference_manager.get_preference("language", user_id=user_id)

        assert theme == "dark"
        assert language == "en"

    async def test_context_inheritance_between_sessions(self):
        """Test that user preferences carry over between different sessions"""
        preference_manager = UserPreferenceManager()
        user_id = "user_456"

        # Session 1 - set user preferences
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference("notifications", "enabled", user_id=user_id)
        await preference_manager.set_preference(
            "temp_setting", "session1_value", session_id="session_001"
        )

        # Session 2 - check inheritance
        theme = await preference_manager.get_preference("theme", user_id=user_id)
        notifications = await preference_manager.get_preference("notifications", user_id=user_id)
        temp_setting = await preference_manager.get_preference(
            "temp_setting", session_id="session_002"
        )

        # User preferences should be inherited
        assert theme == "dark"
        assert notifications == "enabled"

        # Session-specific preferences should NOT be inherited
        assert temp_setting is None

    async def test_session_preference_isolation(self):
        """Test that session preferences are isolated between sessions"""
        preference_manager = UserPreferenceManager()

        session1_id = "session_001"
        session2_id = "session_002"

        await preference_manager.set_preference("workspace", "backend", session_id=session1_id)
        await preference_manager.set_preference("workspace", "frontend", session_id=session2_id)

        workspace1 = await preference_manager.get_preference("workspace", session_id=session1_id)
        workspace2 = await preference_manager.get_preference("workspace", session_id=session2_id)

        assert workspace1 == "backend"
        assert workspace2 == "frontend"


@pytest.mark.asyncio
class TestSessionContextManagerStandalone:
    """Test high-level SessionContextManager functionality"""

    async def test_get_or_create_session_with_context(self):
        """Test unified session creation with context"""
        context_manager = SessionContextManager()
        user_id = "user_789"

        # Create session with context
        session = await context_manager.get_or_create_session_with_context(
            session_id="test_session", user_id=user_id, restore_context=True
        )

        assert session is not None
        assert session.session_id == "test_session"
        assert isinstance(session.context, dict)

    async def test_end_session_with_persistence(self):
        """Test session ending with persistence"""
        context_manager = SessionContextManager()
        user_id = "user_789"

        # Create and configure session
        session = await context_manager.get_or_create_session_with_context(
            session_id="ending_session", user_id=user_id
        )

        # Set some preferences
        await context_manager.preference_manager.set_preference(
            "test_pref", "test_value", user_id=user_id
        )

        # End session with persistence
        result = await context_manager.end_session_with_persistence(session, user_id=user_id)

        assert result is True

    async def test_cleanup_expired_sessions(self):
        """Test cleanup functionality"""
        context_manager = SessionContextManager()

        # Create some sessions
        session1 = await context_manager.get_or_create_session_with_context(session_id="session1")
        session2 = await context_manager.get_or_create_session_with_context(session_id="session2")

        # Run cleanup
        cleanup_stats = await context_manager.cleanup_expired_sessions()

        assert isinstance(cleanup_stats, dict)
        assert "total_cleaned" in cleanup_stats


@pytest.mark.asyncio
class TestPerformanceRequirements:
    """Test that persistence operations meet performance requirements"""

    async def test_persistence_performance(self):
        """Test that persistence operations complete within 500ms"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        session = ConversationSession("perf_test_session")
        user_id = "user_456"

        # Set up test data
        for i in range(10):
            await preference_manager.set_preference(f"setting_{i}", f"value_{i}", user_id=user_id)

        await preference_manager.update_session_context(session, user_id=user_id)

        # Measure persistence time
        start_time = datetime.now()
        result = await persistence_manager.save_session_context(session, user_id=user_id)
        end_time = datetime.now()

        duration_ms = (end_time - start_time).total_seconds() * 1000

        assert result is True
        assert duration_ms < 500  # Should complete in <500ms

    async def test_bulk_preference_operations(self):
        """Test bulk operations performance"""
        preference_manager = UserPreferenceManager()
        user_id = "bulk_user"

        # Set many preferences
        start_time = datetime.now()
        for i in range(50):
            await preference_manager.set_preference(f"bulk_{i}", f"value_{i}", user_id=user_id)
        end_time = datetime.now()

        set_duration_ms = (end_time - start_time).total_seconds() * 1000

        # Get all preferences
        start_time = datetime.now()
        all_prefs = await preference_manager.get_all_preferences(user_id=user_id)
        end_time = datetime.now()

        get_duration_ms = (end_time - start_time).total_seconds() * 1000

        assert len(all_prefs) >= 50
        assert set_duration_ms < 1000  # Bulk sets should be reasonable
        assert get_duration_ms < 100  # Gets should be fast


# Simple test runner for standalone execution
if __name__ == "__main__":

    async def run_tests():
        """Run key tests manually"""
        print("🧪 Running Session Persistence standalone tests...")

        # Test basic persistence
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        session = ConversationSession("test_session")
        user_id = "test_user"

        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        result = await persistence_manager.save_session_context(session, user_id=user_id)
        assert result is True
        print("✅ Basic persistence test passed")

        # Test context restoration
        new_session = ConversationSession("test_session")
        result = await persistence_manager.restore_session_context(new_session, user_id=user_id)
        assert result is True
        print("✅ Context restoration test passed")

        # Test session context manager
        context_manager = SessionContextManager()
        session = await context_manager.get_or_create_session_with_context(
            session_id="unified_test", user_id="test_user"
        )
        assert session is not None
        print("✅ Session context manager test passed")

        print("🎉 All standalone tests passed!")

    asyncio.run(run_tests())
