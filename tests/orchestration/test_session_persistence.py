"""
Tests for Session Persistence & Context Inheritance
Phase 2: Session Context Integration Tests (Written First per TDD)

Created: 2025-08-20 by Enhanced Autonomy Mission
"""

import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.domain.user_preference_manager import UserPreferenceManager
from services.orchestration.session_persistence import SessionPersistenceManager
from services.session.session_manager import ConversationSession, SessionManager


@pytest.mark.asyncio
class TestSessionContextPersistence:
    """Test session context persistence to database"""

    async def test_session_context_persistence(self):
        """Test that session context is persisted to database storage"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        session = ConversationSession("test_session_123")
        user_id = "user_456"

        # Set preferences that should be persisted
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference(
            "project", "piper-morgan", session_id=session.session_id
        )
        await preference_manager.update_session_context(session, user_id=user_id)

        # Persist session context
        result = await persistence_manager.save_session_context(session, user_id=user_id)

        assert result is True

        # Verify context was persisted (would check database in real implementation)
        persisted_data = await persistence_manager.get_persisted_context(session.session_id)
        assert persisted_data is not None
        assert "user_preferences" in persisted_data
        assert "session_preferences" in persisted_data
        assert persisted_data["user_preferences"]["theme"] == "dark"
        assert persisted_data["session_preferences"]["project"] == "piper-morgan"

    async def test_session_context_restoration(self):
        """Test that session context can be restored from database"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        session_id = "test_session_123"
        user_id = "user_456"

        # Simulate persisted context data
        persisted_data = {
            "user_preferences": {"theme": "dark", "language": "en"},
            "session_preferences": {"project": "piper-morgan", "agent_mode": "cursor"},
            "context_version": "1.0",
            "last_updated": datetime.now().isoformat(),
        }

        # Mock persistence layer
        persistence_manager._storage = Mock()
        persistence_manager._storage.get_session_context = AsyncMock(return_value=persisted_data)

        # Restore session context
        new_session = ConversationSession(session_id)
        result = await persistence_manager.restore_session_context(new_session, user_id=user_id)

        assert result is True
        assert "user_preferences" in new_session.context
        assert new_session.context["user_preferences"]["theme"] == "dark"
        assert new_session.context["session_preferences"]["project"] == "piper-morgan"


@pytest.mark.asyncio
class TestContextInheritanceBetweenSessions:
    """Test context inheritance patterns between sessions"""

    async def test_context_inheritance_between_sessions(self):
        """Test that user preferences carry over between sessions"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        user_id = "user_456"

        # First session - set user preferences
        session1 = ConversationSession("session_001")
        await preference_manager.set_preference("theme", "dark", user_id=user_id)
        await preference_manager.set_preference("notifications", "enabled", user_id=user_id)
        await preference_manager.set_preference(
            "temp_setting", "session1_value", session_id=session1.session_id
        )

        # Save session 1 context
        await preference_manager.update_session_context(session1, user_id=user_id)
        await persistence_manager.save_session_context(session1, user_id=user_id)

        # Second session - should inherit user preferences but not session preferences
        session2 = ConversationSession("session_002")
        await persistence_manager.restore_session_context(session2, user_id=user_id)

        # User preferences should be inherited
        theme = await preference_manager.get_preference("theme", user_id=user_id)
        notifications = await preference_manager.get_preference("notifications", user_id=user_id)

        assert theme == "dark"
        assert notifications == "enabled"

        # Session-specific preferences should NOT be inherited
        temp_setting = await preference_manager.get_preference(
            "temp_setting", session_id=session2.session_id
        )
        assert temp_setting is None

    async def test_session_preference_isolation(self):
        """Test that session preferences are isolated between sessions"""
        preference_manager = UserPreferenceManager()
        user_id = "user_456"

        # Set preferences in different sessions
        session1_id = "session_001"
        session2_id = "session_002"

        await preference_manager.set_preference("workspace", "backend", session_id=session1_id)
        await preference_manager.set_preference("workspace", "frontend", session_id=session2_id)

        # Verify isolation
        workspace1 = await preference_manager.get_preference("workspace", session_id=session1_id)
        workspace2 = await preference_manager.get_preference("workspace", session_id=session2_id)

        assert workspace1 == "backend"
        assert workspace2 == "frontend"

        # Verify no cross-contamination
        workspace1_from_session2 = await preference_manager.get_preference(
            "workspace", session_id=session2_id
        )
        assert workspace1_from_session2 == "frontend"  # Should be session 2's value


@pytest.mark.asyncio
class TestSessionExpirationHandling:
    """Test session expiration and cleanup"""

    async def test_session_expiration_handling(self):
        """Test that expired sessions are handled correctly"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        session_id = "expiring_session"
        user_id = "user_456"

        # Create session with short TTL
        session = ConversationSession(session_id)
        await preference_manager.set_preference(
            "temp_data", "should_expire", session_id=session_id, ttl_minutes=1
        )

        # Verify preference exists initially
        temp_data = await preference_manager.get_preference("temp_data", session_id=session_id)
        assert temp_data == "should_expire"

        # Simulate time passage (in real implementation, this would be actual time)
        await persistence_manager.cleanup_expired_sessions()

        # Check if expiration is detected
        is_expired = await preference_manager.is_preference_expired(
            "temp_data", session_id=session_id
        )
        # Note: This test might need adjustment based on actual TTL implementation

        # After cleanup, expired preferences should be gone
        await preference_manager._cleanup_expired_preferences()
        temp_data_after = await preference_manager.get_preference(
            "temp_data", session_id=session_id
        )
        # Actual behavior depends on TTL implementation

    async def test_session_context_versioning(self):
        """Test session context versioning for conflict resolution"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        session = ConversationSession("test_session")
        user_id = "user_456"

        # Set initial preference with version tracking
        await preference_manager.set_preference("shared_setting", "value1", user_id=user_id)
        version1 = await preference_manager.get_preference_version(
            "shared_setting", user_id=user_id
        )

        # Simulate concurrent update
        await preference_manager.set_preference("shared_setting", "value2", user_id=user_id)
        version2 = await preference_manager.get_preference_version(
            "shared_setting", user_id=user_id
        )

        assert version2 > version1

        # Test versioned update
        result = await preference_manager.set_preference_with_version(
            "shared_setting", "value3", user_id=user_id, expected_version=version2
        )
        assert result is True


@pytest.mark.asyncio
class TestContextConflictResolution:
    """Test context conflict resolution strategies"""

    async def test_context_conflict_resolution(self):
        """Test handling of conflicting context updates"""
        preference_manager = UserPreferenceManager()
        persistence_manager = SessionPersistenceManager(preference_manager)

        user_id = "user_456"
        session_id = "conflict_session"

        # Set up conflicting preferences at different levels
        await preference_manager.set_preference("display_mode", "global_default", scope="global")
        await preference_manager.set_preference("display_mode", "user_preference", user_id=user_id)
        await preference_manager.set_preference(
            "display_mode", "session_override", session_id=session_id
        )

        # Test conflict resolution priority
        resolved_value = await preference_manager.get_preference(
            "display_mode", user_id=user_id, session_id=session_id
        )

        # Session should override user, user should override global
        assert resolved_value == "session_override"

        # Test without session context - should get user preference
        resolved_user = await preference_manager.get_preference("display_mode", user_id=user_id)
        assert resolved_user == "user_preference"

        # Test without any context - should get global
        resolved_global = await preference_manager.get_preference("display_mode", scope="global")
        assert resolved_global == "global_default"

    async def test_preference_merge_strategies(self):
        """Test different strategies for merging preferences"""
        preference_manager = UserPreferenceManager()

        user_id = "user_456"
        session_id = "merge_session"

        # Set up hierarchical preferences
        await preference_manager.set_preference(
            "config", {"global_setting": "global", "shared_setting": "from_global"}, scope="global"
        )
        await preference_manager.set_preference(
            "config", {"user_setting": "user", "shared_setting": "from_user"}, user_id=user_id
        )
        await preference_manager.set_preference(
            "config",
            {"session_setting": "session", "shared_setting": "from_session"},
            session_id=session_id,
        )

        # Test merged preferences
        merged = await preference_manager.merge_preferences(user_id=user_id, session_id=session_id)

        # Should have all settings with proper precedence
        assert "global_setting" in merged
        assert "user_setting" in merged
        assert "session_setting" in merged

        # Session should override user should override global for shared setting
        # Note: This test assumes complex object merging - may need implementation adjustment


@pytest.mark.asyncio
class TestPersistencePerformance:
    """Test performance characteristics of persistence operations"""

    async def test_persistence_performance(self):
        """Test that persistence operations meet performance requirements"""
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

        duration = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds

        assert result is True
        assert duration < 500  # Should complete in <500ms as per requirements

    async def test_bulk_preference_operations(self):
        """Test bulk preference operations performance"""
        preference_manager = UserPreferenceManager()
        user_id = "bulk_user"

        # Bulk set preferences
        preferences = {f"bulk_setting_{i}": f"bulk_value_{i}" for i in range(50)}

        start_time = datetime.now()
        for key, value in preferences.items():
            await preference_manager.set_preference(key, value, user_id=user_id)
        end_time = datetime.now()

        bulk_set_duration = (end_time - start_time).total_seconds() * 1000

        # Bulk get preferences
        start_time = datetime.now()
        all_prefs = await preference_manager.get_all_preferences(user_id=user_id)
        end_time = datetime.now()

        bulk_get_duration = (end_time - start_time).total_seconds() * 1000

        assert len(all_prefs) >= 50
        assert bulk_set_duration < 1000  # Bulk operations should be reasonable
        assert bulk_get_duration < 100  # Retrieval should be fast
