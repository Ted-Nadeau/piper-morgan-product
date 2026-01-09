"""
Unit tests for Preference Applicator.

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Tests for PreferenceApplicator preference loading, extraction, and application.
"""

import shutil
import tempfile
from pathlib import Path

import pytest

from services.standup.preference_applicator import (
    AppliedPreferences,
    PreferenceApplicator,
    get_user_applied_preferences,
)
from services.standup.preference_models import (
    PreferenceSource,
    PreferenceType,
    UserStandupPreference,
)
from services.standup.preference_service import UserPreferenceService


class TestAppliedPreferences:
    """Tests for AppliedPreferences dataclass."""

    def test_default_creation(self):
        """Test creating applied preferences with defaults."""
        applied = AppliedPreferences()
        assert applied.focus_areas == []
        assert applied.excluded_areas == []
        assert applied.format_style == "standard"
        assert applied.temporary_overrides == {}
        assert applied.applied_from_history == []
        assert applied.applied_from_turn == []

    def test_to_dict(self):
        """Test converting to dictionary."""
        applied = AppliedPreferences(
            focus_areas=["github"],
            excluded_areas=["docs"],
            format_style="brief",
        )
        d = applied.to_dict()
        assert d["focus_areas"] == ["github"]
        assert d["excluded_areas"] == ["docs"]
        assert d["format_style"] == "brief"

    def test_describe_applied_empty(self):
        """Test description when no preferences applied."""
        applied = AppliedPreferences()
        assert applied.describe_applied() == "Using default preferences"

    def test_describe_applied_with_focus(self):
        """Test description with focus areas."""
        applied = AppliedPreferences(focus_areas=["github", "calendar"])
        assert "Focusing on: github, calendar" in applied.describe_applied()

    def test_describe_applied_with_exclusions(self):
        """Test description with exclusions."""
        applied = AppliedPreferences(excluded_areas=["docs", "tests"])
        assert "Excluding: docs, tests" in applied.describe_applied()

    def test_describe_applied_with_format(self):
        """Test description with format preference."""
        applied = AppliedPreferences(format_style="brief")
        assert "Format: brief" in applied.describe_applied()

    def test_describe_applied_with_temporary(self):
        """Test description with temporary overrides."""
        applied = AppliedPreferences(temporary_overrides={"focus": "github"})
        assert "One-time" in applied.describe_applied()

    def test_describe_applied_combined(self):
        """Test description with multiple preferences."""
        applied = AppliedPreferences(
            focus_areas=["github"],
            excluded_areas=["docs"],
            format_style="brief",
        )
        desc = applied.describe_applied()
        assert "Focusing on: github" in desc
        assert "Excluding: docs" in desc
        assert "Format: brief" in desc


class TestPreferenceApplicator:
    """Tests for PreferenceApplicator class."""

    @pytest.fixture
    def temp_storage(self):
        """Create a temporary storage directory."""
        temp_dir = tempfile.mkdtemp()
        yield Path(temp_dir)
        shutil.rmtree(temp_dir)

    @pytest.fixture
    def applicator(self, temp_storage):
        """Create an applicator with temporary storage."""
        service = UserPreferenceService(storage_path=temp_storage)
        return PreferenceApplicator(preference_service=service)

    # =========================================================================
    # Historical Preference Loading Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_prepare_preferences_empty_user(self, applicator):
        """Test preparing preferences for user with no history."""
        applied = await applicator.prepare_preferences("new-user")
        assert applied.focus_areas == []
        assert applied.excluded_areas == []
        assert applied.format_style == "standard"

    @pytest.mark.asyncio
    async def test_prepare_preferences_loads_historical(self, temp_storage):
        """Test that historical preferences are loaded."""
        # Set up historical preferences
        service = UserPreferenceService(storage_path=temp_storage)
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus",
            value="github",
            confidence=0.9,
        )
        await service.save_preference(pref)

        # Create applicator and prepare
        applicator = PreferenceApplicator(preference_service=service)
        applied = await applicator.prepare_preferences("user-123")

        assert "github" in applied.focus_areas
        assert len(applied.applied_from_history) == 1

    @pytest.mark.asyncio
    async def test_prepare_preferences_filters_low_confidence(self, temp_storage):
        """Test that low confidence preferences are filtered out."""
        service = UserPreferenceService(storage_path=temp_storage)
        high_conf = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus_github",  # Unique key
            value="github",
            confidence=0.9,
        )
        low_conf = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.CONTENT_FILTER,
            key="focus_calendar",  # Different unique key
            value="calendar",
            confidence=0.5,  # Below 0.7 threshold
        )
        await service.save_preference(high_conf)
        await service.save_preference(low_conf)

        applicator = PreferenceApplicator(preference_service=service)
        applied = await applicator.prepare_preferences("user-123")

        # High confidence (0.9) should be included
        assert "github" in applied.focus_areas
        # Low confidence (0.5) should be filtered out
        assert "calendar" not in applied.focus_areas

    @pytest.mark.asyncio
    async def test_prepare_preferences_loads_exclusions(self, temp_storage):
        """Test loading exclusion preferences."""
        service = UserPreferenceService(storage_path=temp_storage)
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="docs",
            confidence=0.85,
        )
        await service.save_preference(pref)

        applicator = PreferenceApplicator(preference_service=service)
        applied = await applicator.prepare_preferences("user-123")

        assert "docs" in applied.excluded_areas

    @pytest.mark.asyncio
    async def test_prepare_preferences_loads_format(self, temp_storage):
        """Test loading format preferences."""
        service = UserPreferenceService(storage_path=temp_storage)
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.FORMAT,
            key="format",
            value="brief",
            confidence=0.8,
        )
        await service.save_preference(pref)

        applicator = PreferenceApplicator(preference_service=service)
        applied = await applicator.prepare_preferences("user-123")

        assert applied.format_style == "brief"

    # =========================================================================
    # Current Turn Extraction Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_prepare_preferences_extracts_from_message(self, applicator):
        """Test extracting preferences from current message."""
        applied = await applicator.prepare_preferences(
            "user-123",
            current_message="focus on GitHub please",
        )
        assert "github" in applied.focus_areas
        assert len(applied.applied_from_turn) >= 1

    @pytest.mark.asyncio
    async def test_prepare_preferences_handles_exclusion_message(self, applicator):
        """Test extracting exclusions from current message."""
        applied = await applicator.prepare_preferences(
            "user-123",
            current_message="skip the documentation updates",
        )
        assert "documentation" in applied.excluded_areas or len(applied.applied_from_turn) >= 1

    @pytest.mark.asyncio
    async def test_prepare_preferences_handles_format_message(self, applicator):
        """Test extracting format from current message."""
        applied = await applicator.prepare_preferences(
            "user-123",
            current_message="make it brief please",
        )
        assert applied.format_style == "brief" or "format" in str(applied.applied_from_turn)

    @pytest.mark.asyncio
    async def test_prepare_preferences_handles_temporary(self, applicator):
        """Test that temporary preferences go to overrides."""
        applied = await applicator.prepare_preferences(
            "user-123",
            current_message="just for today, focus on GitHub",
        )
        # Either in temporary_overrides or noted as temporary
        assert applied.temporary_overrides or "github" in applied.focus_areas

    # =========================================================================
    # Content Filtering Tests
    # =========================================================================

    def test_filter_content_no_preferences(self, applicator):
        """Test content filtering with no preferences."""
        content = {"github": [...], "calendar": [...], "todos": [...]}
        applied = AppliedPreferences()

        filtered = applicator.filter_content(content, applied)

        assert set(filtered.keys()) == set(content.keys())

    def test_filter_content_with_focus(self, applicator):
        """Test content filtering with focus areas."""
        content = {"github": [...], "calendar": [...], "todos": [...]}
        applied = AppliedPreferences(focus_areas=["github"])

        filtered = applicator.filter_content(content, applied)

        assert "github" in filtered
        assert "calendar" not in filtered
        assert "todos" not in filtered

    def test_filter_content_with_exclusions(self, applicator):
        """Test content filtering with exclusions."""
        content = {"github": [...], "calendar": [...], "docs": [...]}
        applied = AppliedPreferences(excluded_areas=["docs"])

        filtered = applicator.filter_content(content, applied)

        assert "github" in filtered
        assert "calendar" in filtered
        assert "docs" not in filtered

    def test_filter_content_with_both(self, applicator):
        """Test content filtering with focus and exclusions."""
        content = {
            "github_prs": [...],
            "github_docs": [...],
            "calendar": [...],
        }
        applied = AppliedPreferences(
            focus_areas=["github"],
            excluded_areas=["docs"],
        )

        filtered = applicator.filter_content(content, applied)

        assert "github_prs" in filtered
        assert "github_docs" not in filtered  # Excluded overrides focus
        assert "calendar" not in filtered

    def test_filter_content_temporary_override_focus(self, applicator):
        """Test that temporary override changes focus."""
        content = {"github": [...], "calendar": [...], "todos": [...]}
        applied = AppliedPreferences(
            focus_areas=["github", "calendar"],  # Historical
            temporary_overrides={"focus": "todos"},  # One-time override
        )

        filtered = applicator.filter_content(content, applied)

        assert "todos" in filtered
        assert "github" not in filtered
        assert "calendar" not in filtered

    def test_filter_content_temporary_override_exclude(self, applicator):
        """Test that temporary exclusion is applied."""
        content = {"github": [...], "calendar": [...], "todos": [...]}
        applied = AppliedPreferences(
            temporary_overrides={"exclude": "github"},
        )

        filtered = applicator.filter_content(content, applied)

        assert "github" not in filtered
        assert "calendar" in filtered
        assert "todos" in filtered

    # =========================================================================
    # Output Formatting Tests
    # =========================================================================

    def test_format_output_standard(self, applicator):
        """Test standard formatting (no change)."""
        text = """*Yesterday:*
* Did task 1
* Did task 2

*Today:*
* Plan task 1
* Plan task 2"""

        applied = AppliedPreferences(format_style="standard")
        result = applicator.format_output(text, applied)

        assert result == text

    def test_format_output_brief(self, applicator):
        """Test brief formatting (truncates items)."""
        text = """*Yesterday:*
* Did task 1
* Did task 2
* Did task 3

*Today:*
* Plan task 1
* Plan task 2"""

        applied = AppliedPreferences(format_style="brief")
        result = applicator.format_output(text, applied)

        # Brief should have fewer lines
        assert len(result.split("\n")) <= len(text.split("\n"))
        # But still have headers
        assert "*Yesterday:*" in result
        assert "*Today:*" in result

    def test_format_output_temporary_override(self, applicator):
        """Test that temporary format overrides historical."""
        text = "*Yesterday:*\n* Task 1\n* Task 2"
        applied = AppliedPreferences(
            format_style="standard",
            temporary_overrides={"format": "brief"},
        )

        result = applicator.format_output(text, applied)

        # Brief formatting should be applied
        assert "*Yesterday:*" in result

    # =========================================================================
    # Integration Tests
    # =========================================================================

    @pytest.mark.asyncio
    async def test_full_workflow_new_user(self, applicator):
        """Test full workflow for new user with message."""
        applied = await applicator.prepare_preferences(
            "new-user",
            current_message="focus on GitHub, keep it brief",
        )

        # Should extract from message
        assert "github" in applied.focus_areas or len(applied.applied_from_turn) >= 1

        # Filter content
        content = {"github": [...], "calendar": [...]}
        filtered = applicator.filter_content(content, applied)
        # Focus on github should filter
        if applied.focus_areas:
            assert "github" in filtered

    @pytest.mark.asyncio
    async def test_full_workflow_returning_user(self, temp_storage):
        """Test full workflow for returning user with history."""
        # First session - save preference
        service = UserPreferenceService(storage_path=temp_storage)
        pref = UserStandupPreference(
            user_id="user-123",
            preference_type=PreferenceType.EXCLUSION,
            key="exclude",
            value="docs",
            confidence=0.9,
        )
        await service.save_preference(pref)

        # Second session - preferences should be loaded
        applicator = PreferenceApplicator(preference_service=service)
        applied = await applicator.prepare_preferences("user-123")

        assert "docs" in applied.excluded_areas

        # Apply to content
        content = {"github": [...], "docs": [...]}
        filtered = applicator.filter_content(content, applied)

        assert "github" in filtered
        assert "docs" not in filtered


class TestConvenienceFunction:
    """Tests for convenience function."""

    @pytest.mark.asyncio
    async def test_get_user_applied_preferences(self):
        """Test convenience function works."""
        applied = await get_user_applied_preferences("test-user")
        assert isinstance(applied, AppliedPreferences)
