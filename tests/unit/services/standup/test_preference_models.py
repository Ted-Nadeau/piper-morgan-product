"""
Unit tests for Preference Models

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Tests for UserStandupPreference, PreferenceChange, and ExtractedPreference dataclasses.
"""

from datetime import datetime, timedelta

import pytest

from services.standup.preference_models import (
    ExtractedPreference,
    PreferenceChange,
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)


class TestUserStandupPreference:
    """Tests for UserStandupPreference dataclass."""

    def test_default_creation(self):
        """Test creating preference with defaults."""
        pref = UserStandupPreference(user_id="user-123")
        assert pref.user_id == "user-123"
        assert pref.preference_type == PreferenceType.CONTENT_FILTER
        assert pref.confidence == 0.7
        assert pref.source == PreferenceSource.EXPLICIT
        assert pref.version == 1
        assert pref.id is not None

    def test_full_creation(self):
        """Test creating preference with all fields."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="docs",
            confidence=0.9,
            source=PreferenceSource.INFERRED,
        )
        assert pref.preference_type == PreferenceType.EXCLUSION
        assert pref.key == "exclude"
        assert pref.value == "docs"
        assert pref.confidence == 0.9
        assert pref.source == PreferenceSource.INFERRED

    def test_to_dict(self):
        """Test converting preference to dictionary."""
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
        )
        d = pref.to_dict()
        assert d["user_id"] == "user-123"
        assert d["preference_type"] == "format"
        assert d["key"] == "format"
        assert d["value"] == "brief"
        assert d["source"] == "explicit"
        assert "created_at" in d
        assert "updated_at" in d

    def test_from_dict(self):
        """Test creating preference from dictionary."""
        data = {
            "id": "pref-456",
            "user_id": "user-123",
            "preference_type": "exclusion",
            "key": "exclude",
            "value": "tests",
            "confidence": 0.85,
            "source": "inferred",
            "created_at": "2026-01-08T10:00:00",
            "updated_at": "2026-01-08T10:00:00",
            "version": 2,
        }
        pref = UserStandupPreference.from_dict(data)
        assert pref.id == "pref-456"
        assert pref.user_id == "user-123"
        assert pref.preference_type == PreferenceType.EXCLUSION
        assert pref.value == "tests"
        assert pref.confidence == 0.85
        assert pref.source == PreferenceSource.INFERRED

    def test_boost_confidence(self):
        """Test boosting confidence."""
        pref = UserStandupPreference(user_id="user-123", confidence=0.7)
        original_version = pref.version
        pref.boost_confidence(0.1)
        assert abs(pref.confidence - 0.8) < 0.001  # Float comparison
        assert pref.version == original_version + 1

    def test_boost_confidence_max(self):
        """Test confidence is capped at 1.0."""
        pref = UserStandupPreference(user_id="user-123", confidence=0.95)
        pref.boost_confidence(0.1)
        assert pref.confidence == 1.0

    def test_reduce_confidence(self):
        """Test reducing confidence."""
        pref = UserStandupPreference(user_id="user-123", confidence=0.8)
        original_version = pref.version
        pref.reduce_confidence(0.2)
        assert abs(pref.confidence - 0.6) < 0.001  # Float comparison
        assert pref.version == original_version + 1

    def test_reduce_confidence_min(self):
        """Test confidence is floored at 0.0."""
        pref = UserStandupPreference(user_id="user-123", confidence=0.1)
        pref.reduce_confidence(0.2)
        assert pref.confidence == 0.0

    def test_is_high_confidence(self):
        """Test high confidence detection."""
        high = UserStandupPreference(user_id="user-123", confidence=0.85)
        low = UserStandupPreference(user_id="user-123", confidence=0.7)
        assert high.is_high_confidence(threshold=0.8) is True
        assert low.is_high_confidence(threshold=0.8) is False

    def test_needs_confirmation(self):
        """Test low confidence confirmation check."""
        low = UserStandupPreference(user_id="user-123", confidence=0.4)
        high = UserStandupPreference(user_id="user-123", confidence=0.7)
        assert low.needs_confirmation(threshold=0.5) is True
        assert high.needs_confirmation(threshold=0.5) is False


class TestPreferenceChange:
    """Tests for PreferenceChange dataclass."""

    def test_creation(self):
        """Test creating a preference change record."""
        change = PreferenceChange(
            preference_id="pref-123",
            user_id="user-456",
            previous_value="github",
            new_value="calendar",
            previous_confidence=0.7,
            new_confidence=0.8,
            change_reason="user_correction",
        )
        assert change.preference_id == "pref-123"
        assert change.previous_value == "github"
        assert change.new_value == "calendar"
        assert change.change_reason == "user_correction"

    def test_to_dict(self):
        """Test converting change to dictionary."""
        change = PreferenceChange(
            preference_id="pref-123",
            user_id="user-456",
            previous_value="brief",
            new_value="detailed",
            change_reason="repetition",
        )
        d = change.to_dict()
        assert d["preference_id"] == "pref-123"
        assert d["previous_value"] == "brief"
        assert d["new_value"] == "detailed"
        assert d["change_reason"] == "repetition"
        assert "changed_at" in d


class TestExtractedPreference:
    """Tests for ExtractedPreference dataclass."""

    def test_default_creation(self):
        """Test creating extracted preference with defaults."""
        extracted = ExtractedPreference(
            raw_text="focus on GitHub",
            key="focus",
            value="github",
        )
        assert extracted.raw_text == "focus on GitHub"
        assert extracted.preference_type == PreferenceType.CONTENT_FILTER
        assert extracted.is_temporary is False

    def test_to_preference(self):
        """Test converting extracted preference to storable preference."""
        extracted = ExtractedPreference(
            raw_text="skip docs",
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="docs",
            confidence=0.85,
            source=PreferenceSource.EXPLICIT,
        )
        pref = extracted.to_preference("user-123")
        assert isinstance(pref, UserStandupPreference)
        assert pref.user_id == "user-123"
        assert pref.preference_type == PreferenceType.EXCLUSION
        assert pref.key == "exclude"
        assert pref.value == "docs"
        assert pref.confidence == 0.85

    def test_temporary_extraction(self):
        """Test temporary preference flag."""
        extracted = ExtractedPreference(
            raw_text="just for today, include tests",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="tests",
            is_temporary=True,
        )
        assert extracted.is_temporary is True


class TestPreferenceEnums:
    """Tests for PreferenceType and PreferenceSource enums."""

    def test_preference_types(self):
        """Test all preference types exist."""
        assert PreferenceType.CONTENT_FILTER.value == "content_filter"
        assert PreferenceType.EXCLUSION.value == "exclusion"
        assert PreferenceType.FORMAT.value == "format"
        assert PreferenceType.TIMING.value == "timing"
        assert PreferenceType.NOTIFICATION.value == "notification"

    def test_preference_sources(self):
        """Test all preference sources exist."""
        assert PreferenceSource.EXPLICIT.value == "explicit"
        assert PreferenceSource.INFERRED.value == "inferred"
        assert PreferenceSource.CORRECTED.value == "corrected"
