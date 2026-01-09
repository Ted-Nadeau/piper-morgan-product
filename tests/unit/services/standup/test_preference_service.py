"""
Unit tests for Preference Service

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Tests for UserPreferenceService CRUD operations and persistence.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from services.standup.preference_models import (
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)
from services.standup.preference_service import UserPreferenceService


class TestUserPreferenceService:
    """Tests for UserPreferenceService class."""

    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def service(self, temp_storage):
        """Create a service with temporary storage."""
        return UserPreferenceService(storage_path=temp_storage)

    # =========================================================================
    # Basic CRUD Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_save_preference(self, service):
        """Test saving a new preference."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
        )
        saved = await service.save_preference(pref)
        assert saved.user_id == "user-123"
        assert saved.value == "github"

    @pytest.mark.asyncio
    async def test_get_preferences(self, service):
        """Test getting all preferences for a user."""
        # Save multiple preferences
        pref1 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
        )
        pref2 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="docs",
        )
        await service.save_preference(pref1)
        await service.save_preference(pref2)

        prefs = await service.get_preferences("user-123")
        assert len(prefs) == 2

    @pytest.mark.asyncio
    async def test_get_preference(self, service):
        """Test getting a specific preference by type and key."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        await service.save_preference(pref)

        result = await service.get_preference("user-123", PreferenceType.FORMAT, "format")
        assert result is not None
        assert result.value == "brief"

    @pytest.mark.asyncio
    async def test_get_preference_not_found(self, service):
        """Test getting a non-existent preference returns None."""
        result = await service.get_preference("user-123", PreferenceType.FORMAT, "nonexistent")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_preferences_by_type(self, service):
        """Test filtering preferences by type."""
        pref1 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="docs",
        )
        pref2 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="tests",
        )
        pref3 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        await service.save_preference(pref1)
        await service.save_preference(pref2)
        await service.save_preference(pref3)

        exclusions = await service.get_preferences_by_type("user-123", PreferenceType.EXCLUSION)
        # Note: Both exclusions have same key, so only one is kept (conflict resolution)
        assert len(exclusions) == 1

    @pytest.mark.asyncio
    async def test_delete_preference(self, service):
        """Test deleting a preference."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        saved = await service.save_preference(pref)

        deleted = await service.delete_preference("user-123", saved.id)
        assert deleted is True

        # Verify it's gone
        prefs = await service.get_preferences("user-123")
        assert len(prefs) == 0

    @pytest.mark.asyncio
    async def test_delete_nonexistent_preference(self, service):
        """Test deleting a non-existent preference returns False."""
        deleted = await service.delete_preference("user-123", "nonexistent-id")
        assert deleted is False

    @pytest.mark.asyncio
    async def test_clear_preferences(self, service):
        """Test clearing all preferences for a user."""
        pref1 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        pref2 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
        )
        await service.save_preference(pref1)
        await service.save_preference(pref2)

        count = await service.clear_preferences("user-123")
        assert count == 2

        prefs = await service.get_preferences("user-123")
        assert len(prefs) == 0

    # =========================================================================
    # Conflict Resolution Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_same_value_boosts_confidence(self, service):
        """Test that repeating the same preference boosts confidence."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
            confidence=0.7,
        )
        await service.save_preference(pref)

        # Save again with same value
        pref2 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
            confidence=0.7,
        )
        result = await service.save_preference(pref2)

        # Confidence should be boosted
        assert result.confidence > 0.7

    @pytest.mark.asyncio
    async def test_different_value_updates(self, service):
        """Test that a different value updates the preference."""
        pref1 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        await service.save_preference(pref1)

        # Save with different value
        pref2 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="detailed",
        )
        await service.save_preference(pref2)

        # Should have updated, not added
        prefs = await service.get_preferences("user-123")
        assert len(prefs) == 1
        assert prefs[0].value == "detailed"

    # =========================================================================
    # Persistence Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_preferences_persist_across_sessions(self, temp_storage):
        """Test that preferences persist across service instances."""
        # First service instance
        service1 = UserPreferenceService(storage_path=temp_storage)
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        await service1.save_preference(pref)

        # New service instance (simulates new session)
        service2 = UserPreferenceService(storage_path=temp_storage)
        prefs = await service2.get_preferences("user-123")

        assert len(prefs) == 1
        assert prefs[0].value == "brief"

    @pytest.mark.asyncio
    async def test_different_users_isolated(self, service):
        """Test that different users' preferences are isolated."""
        pref1 = UserStandupPreference(
            user_id="user-1",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        pref2 = UserStandupPreference(
            user_id="user-2",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="detailed",
        )
        await service.save_preference(pref1)
        await service.save_preference(pref2)

        prefs1 = await service.get_preferences("user-1")
        prefs2 = await service.get_preferences("user-2")

        assert len(prefs1) == 1
        assert prefs1[0].value == "brief"
        assert len(prefs2) == 1
        assert prefs2[0].value == "detailed"

    # =========================================================================
    # History Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_get_preference_history(self, service):
        """Test getting preference change history."""
        pref1 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        await service.save_preference(pref1)

        # Update to different value (creates history entry)
        pref2 = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="detailed",
        )
        await service.save_preference(pref2)

        history = await service.get_preference_history("user-123")
        assert len(history) >= 1
        assert history[0].previous_value == "brief"
        assert history[0].new_value == "detailed"

    @pytest.mark.asyncio
    async def test_update_preference(self, service):
        """Test updating an existing preference."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        saved = await service.save_preference(pref)

        updated = await service.update_preference(
            user_id="user-123",
            preference_id=saved.id,
            value="detailed",
            confidence=0.9,
        )

        assert updated is not None
        assert updated.value == "detailed"
        assert updated.confidence == 0.9

    # =========================================================================
    # Confidence Filtering Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_get_high_confidence_preferences(self, service):
        """Test getting high confidence preferences."""
        high_conf = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
            confidence=0.9,
        )
        low_conf = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.6,
        )
        await service.save_preference(high_conf)
        await service.save_preference(low_conf)

        high = await service.get_high_confidence_preferences("user-123", threshold=0.8)
        assert len(high) == 1
        assert high[0].value == "brief"

    @pytest.mark.asyncio
    async def test_get_preferences_needing_confirmation(self, service):
        """Test getting low confidence preferences that need confirmation."""
        high_conf = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
            confidence=0.9,
        )
        low_conf = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.4,
        )
        await service.save_preference(high_conf)
        await service.save_preference(low_conf)

        needs_confirm = await service.get_preferences_needing_confirmation(
            "user-123", threshold=0.5
        )
        assert len(needs_confirm) == 1
        assert needs_confirm[0].value == "github"

    # =========================================================================
    # Edge Cases
    # =========================================================================

    @pytest.mark.asyncio
    async def test_empty_user_returns_empty_list(self, service):
        """Test getting preferences for a user with none returns empty list."""
        prefs = await service.get_preferences("nonexistent-user")
        assert prefs == []

    @pytest.mark.asyncio
    async def test_empty_history_returns_empty_list(self, service):
        """Test getting history for a user with none returns empty list."""
        history = await service.get_preference_history("nonexistent-user")
        assert history == []
