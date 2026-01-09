"""
Unit tests for Preference Extractor

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Tests rule-based preference extraction from conversation turns.
"""

import pytest

from services.standup.preference_extractor import PreferenceExtractor, extract_preferences
from services.standup.preference_models import PreferenceSource, PreferenceType


class TestPreferenceExtractor:
    """Tests for PreferenceExtractor class."""

    @pytest.fixture
    def extractor(self):
        """Create a fresh extractor for each test."""
        return PreferenceExtractor()

    # =========================================================================
    # Content Filter Tests
    # =========================================================================

    def test_extract_focus_on_github(self, extractor):
        """Test extracting 'focus on GitHub' preference."""
        prefs = extractor.extract_from_turn("focus on GitHub")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.CONTENT_FILTER
        assert prefs[0].key == "focus"
        assert prefs[0].value == "github"
        assert prefs[0].source == PreferenceSource.EXPLICIT

    def test_extract_prioritize(self, extractor):
        """Test extracting 'prioritize X' preference."""
        prefs = extractor.extract_from_turn("prioritize issues")
        assert len(prefs) == 1
        assert prefs[0].key == "focus"
        assert prefs[0].value == "issues"

    def test_extract_mainly(self, extractor):
        """Test extracting 'mainly X' preference."""
        prefs = extractor.extract_from_turn("mainly calendar")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.CONTENT_FILTER
        assert prefs[0].value == "calendar"

    def test_extract_show_me(self, extractor):
        """Test extracting 'show me X' preference."""
        prefs = extractor.extract_from_turn("show me commits")
        assert len(prefs) == 1
        assert prefs[0].value == "commits"

    # =========================================================================
    # Exclusion Tests
    # =========================================================================

    def test_extract_skip(self, extractor):
        """Test extracting 'skip X' exclusion."""
        prefs = extractor.extract_from_turn("skip docs")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.EXCLUSION
        assert prefs[0].key == "exclude"
        assert prefs[0].value == "docs"

    def test_extract_ignore(self, extractor):
        """Test extracting 'ignore X' exclusion."""
        prefs = extractor.extract_from_turn("ignore tests")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.EXCLUSION
        assert prefs[0].value == "tests"

    def test_extract_dont_include(self, extractor):
        """Test extracting "don't include X" exclusion."""
        prefs = extractor.extract_from_turn("don't include meetings")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.EXCLUSION
        assert prefs[0].value == "meetings"

    def test_extract_exclude(self, extractor):
        """Test extracting 'exclude X' exclusion."""
        prefs = extractor.extract_from_turn("exclude notifications")
        assert len(prefs) == 1
        assert prefs[0].value == "notifications"

    # =========================================================================
    # Format Tests
    # =========================================================================

    def test_extract_brief_format(self, extractor):
        """Test extracting 'brief' format preference."""
        prefs = extractor.extract_from_turn("make it brief")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.FORMAT
        assert prefs[0].value == "brief"

    def test_extract_detailed_format(self, extractor):
        """Test extracting 'detailed' format preference."""
        prefs = extractor.extract_from_turn("I want detailed updates")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.FORMAT
        assert prefs[0].value == "detailed"

    def test_extract_bullet_points(self, extractor):
        """Test extracting 'bullet points' format preference."""
        prefs = extractor.extract_from_turn("use bullet points")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.FORMAT
        assert prefs[0].value == "bullets"

    def test_extract_short_format(self, extractor):
        """Test extracting 'short' as 'brief' format."""
        prefs = extractor.extract_from_turn("keep it short")
        assert len(prefs) == 1
        assert prefs[0].value == "brief"

    # =========================================================================
    # Timing Tests
    # =========================================================================

    def test_extract_time_9am(self, extractor):
        """Test extracting '9am' timing preference."""
        prefs = extractor.extract_from_turn("send it at 9am")
        assert len(prefs) >= 1
        timing_prefs = [p for p in prefs if p.preference_type == PreferenceType.TIMING]
        assert len(timing_prefs) >= 1
        assert timing_prefs[0].value == "09:00"

    def test_extract_daily_frequency(self, extractor):
        """Test extracting 'daily' timing preference."""
        prefs = extractor.extract_from_turn("I want daily standups")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.TIMING
        assert prefs[0].key == "frequency"
        assert prefs[0].value == "daily"

    def test_extract_weekly_frequency(self, extractor):
        """Test extracting 'weekly' timing preference."""
        prefs = extractor.extract_from_turn("make it weekly")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.TIMING
        assert prefs[0].value == "weekly"

    def test_extract_day_of_week(self, extractor):
        """Test extracting 'every Monday' timing preference."""
        prefs = extractor.extract_from_turn("every Monday")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.TIMING
        assert prefs[0].value == "monday"

    # =========================================================================
    # Notification Tests
    # =========================================================================

    def test_extract_notify_via_slack(self, extractor):
        """Test extracting 'notify via Slack' notification preference."""
        prefs = extractor.extract_from_turn("notify via Slack")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.NOTIFICATION
        assert prefs[0].value == "slack"

    def test_extract_email_summary(self, extractor):
        """Test extracting 'email summary' notification preference."""
        prefs = extractor.extract_from_turn("send me an email summary")
        # May also extract "summary" as format preference
        notification_prefs = [p for p in prefs if p.preference_type == PreferenceType.NOTIFICATION]
        assert len(notification_prefs) >= 1
        assert notification_prefs[0].value == "email"

    def test_extract_no_notifications(self, extractor):
        """Test extracting 'no notifications' preference."""
        prefs = extractor.extract_from_turn("no notifications please")
        assert len(prefs) == 1
        assert prefs[0].preference_type == PreferenceType.NOTIFICATION
        assert prefs[0].value == "none"

    # =========================================================================
    # Multiple Preferences Tests
    # =========================================================================

    def test_extract_multiple_preferences(self, extractor):
        """Test extracting multiple preferences from one message."""
        prefs = extractor.extract_from_turn("focus on GitHub and skip docs")
        assert len(prefs) == 2
        types = {p.preference_type for p in prefs}
        assert PreferenceType.CONTENT_FILTER in types
        assert PreferenceType.EXCLUSION in types

    def test_extract_three_preferences(self, extractor):
        """Test extracting three preferences from one message."""
        prefs = extractor.extract_from_turn("focus on GitHub, skip tests, make it brief")
        assert len(prefs) == 3
        types = {p.preference_type for p in prefs}
        assert PreferenceType.CONTENT_FILTER in types
        assert PreferenceType.EXCLUSION in types
        assert PreferenceType.FORMAT in types

    # =========================================================================
    # Temporary Override Tests
    # =========================================================================

    def test_extract_temporary_just_for_today(self, extractor):
        """Test extracting temporary 'just for today' override."""
        prefs = extractor.extract_from_turn("just for today, include docs")
        # Should mark as temporary
        for pref in prefs:
            assert pref.is_temporary is True

    def test_extract_temporary_only_this_time(self, extractor):
        """Test extracting temporary 'only this time' override."""
        prefs = extractor.extract_from_turn("only this time, show me tests")
        for pref in prefs:
            assert pref.is_temporary is True

    def test_permanent_preference_default(self, extractor):
        """Test that regular preferences are not temporary."""
        prefs = extractor.extract_from_turn("always focus on GitHub")
        for pref in prefs:
            assert pref.is_temporary is False

    # =========================================================================
    # Edge Cases
    # =========================================================================

    def test_empty_message(self, extractor):
        """Test extracting from empty message."""
        prefs = extractor.extract_from_turn("")
        assert prefs == []

    def test_whitespace_message(self, extractor):
        """Test extracting from whitespace-only message."""
        prefs = extractor.extract_from_turn("   \n\t  ")
        assert prefs == []

    def test_no_preferences(self, extractor):
        """Test message with no preference patterns."""
        prefs = extractor.extract_from_turn("Hello, how are you today?")
        assert prefs == []

    def test_case_insensitive(self, extractor):
        """Test case-insensitive pattern matching."""
        prefs1 = extractor.extract_from_turn("FOCUS ON GITHUB")
        prefs2 = extractor.extract_from_turn("Focus On GitHub")
        prefs3 = extractor.extract_from_turn("focus on github")
        assert len(prefs1) == len(prefs2) == len(prefs3) == 1
        assert prefs1[0].value == prefs2[0].value == prefs3[0].value


class TestConvenienceFunction:
    """Tests for the extract_preferences convenience function."""

    def test_extract_preferences_function(self):
        """Test the convenience function works."""
        prefs = extract_preferences("focus on GitHub and skip docs")
        assert len(prefs) == 2

    def test_extract_preferences_empty(self):
        """Test convenience function with empty input."""
        prefs = extract_preferences("")
        assert prefs == []


class TestPreferenceConfidence:
    """Tests for confidence levels in extracted preferences."""

    @pytest.fixture
    def extractor(self):
        return PreferenceExtractor()

    def test_explicit_preference_high_confidence(self, extractor):
        """Test that explicit preferences have high confidence."""
        prefs = extractor.extract_from_turn("focus on GitHub")
        assert prefs[0].confidence >= 0.7

    def test_format_preference_confidence(self, extractor):
        """Test format preferences have appropriate confidence."""
        prefs = extractor.extract_from_turn("make it brief")
        assert prefs[0].confidence >= 0.8

    def test_timing_preference_confidence(self, extractor):
        """Test timing preferences have high confidence."""
        prefs = extractor.extract_from_turn("daily at 9am")
        for pref in prefs:
            assert pref.confidence >= 0.8
