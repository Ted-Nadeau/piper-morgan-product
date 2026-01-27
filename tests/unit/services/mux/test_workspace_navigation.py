"""
Tests for workspace navigation language generation.

Part of #659 WORKSPACE-NAVIGATION.

Tests cover:
- NAVIGATION_PATTERNS dictionary structure
- humanize_duration() for various intervals
- navigate_language() for switch types
- reference_language() output format
- Anti-pattern verification (no technical identifiers)
"""

from datetime import datetime, timedelta, timezone

import pytest

from services.mux.workspace_detection import ContextSwitch, WorkspaceContext
from services.mux.workspace_navigation import (
    NAVIGATION_PATTERNS,
    _select_pattern,
    humanize_duration,
    navigate_language,
    reference_language,
)
from services.shared_types import InteractionSpace

# =============================================================================
# Test Fixtures
# =============================================================================


def make_context(
    workspace_id: str = "workspace-1",
    friendly_name: str = "#general",
    place_type: InteractionSpace = InteractionSpace.SLACK_CHANNEL,
    hours_ago: float = 0,
) -> WorkspaceContext:
    """Helper to create test WorkspaceContext instances."""
    return WorkspaceContext(
        workspace_id=workspace_id,
        workspace_type="slack",
        friendly_name=friendly_name,
        last_active=datetime.now(timezone.utc) - timedelta(hours=hours_ago),
        place_type=place_type,
        metadata={},
    )


def make_switch(
    from_name: str = "#old-channel",
    to_name: str = "#new-channel",
    switch_type: str = "explicit",
    time_away: timedelta = None,
) -> ContextSwitch:
    """Helper to create test ContextSwitch instances."""
    return ContextSwitch(
        from_context=make_context(workspace_id="ws-from", friendly_name=from_name),
        to_context=make_context(workspace_id="ws-to", friendly_name=to_name),
        switch_type=switch_type,
        time_away=time_away,
    )


# =============================================================================
# Test: NAVIGATION_PATTERNS
# =============================================================================


class TestNavigationPatterns:
    """Tests for the NAVIGATION_PATTERNS dictionary."""

    def test_has_switch_to_patterns(self):
        """switch_to key exists with patterns."""
        assert "switch_to" in NAVIGATION_PATTERNS
        assert len(NAVIGATION_PATTERNS["switch_to"]) >= 1

    def test_has_return_to_patterns(self):
        """return_to key exists with patterns."""
        assert "return_to" in NAVIGATION_PATTERNS
        assert len(NAVIGATION_PATTERNS["return_to"]) >= 1

    def test_has_reference_patterns(self):
        """reference key exists with patterns."""
        assert "reference" in NAVIGATION_PATTERNS
        assert len(NAVIGATION_PATTERNS["reference"]) >= 1

    def test_patterns_contain_destination_placeholder(self):
        """switch_to and return_to patterns have {destination}."""
        for pattern in NAVIGATION_PATTERNS["switch_to"]:
            assert "{destination}" in pattern

        for pattern in NAVIGATION_PATTERNS["return_to"]:
            assert "{destination}" in pattern

    def test_reference_patterns_contain_location_placeholder(self):
        """reference patterns have {location}."""
        for pattern in NAVIGATION_PATTERNS["reference"]:
            assert "{location}" in pattern


# =============================================================================
# Test: humanize_duration
# =============================================================================


class TestHumanizeDuration:
    """Tests for the humanize_duration() function."""

    def test_seconds(self):
        """Very short durations return 'a few seconds'."""
        assert humanize_duration(timedelta(seconds=30)) == "a few seconds"

    def test_one_minute(self):
        """About one minute returns 'a minute'."""
        assert humanize_duration(timedelta(minutes=1)) == "a minute"
        assert humanize_duration(timedelta(seconds=90)) == "a minute"

    def test_multiple_minutes(self):
        """Multiple minutes return 'X minutes'."""
        assert humanize_duration(timedelta(minutes=5)) == "5 minutes"
        assert humanize_duration(timedelta(minutes=45)) == "45 minutes"

    def test_one_hour(self):
        """About one hour returns 'an hour'."""
        assert humanize_duration(timedelta(hours=1)) == "an hour"
        assert humanize_duration(timedelta(minutes=70)) == "an hour"

    def test_couple_hours(self):
        """Two hours returns 'a couple hours'."""
        assert humanize_duration(timedelta(hours=2)) == "a couple hours"

    def test_multiple_hours(self):
        """Multiple hours return 'about X hours'."""
        assert humanize_duration(timedelta(hours=5)) == "about 5 hours"
        assert humanize_duration(timedelta(hours=12)) == "about 12 hours"

    def test_one_day(self):
        """About one day returns 'a day'."""
        assert humanize_duration(timedelta(days=1)) == "a day"
        assert humanize_duration(timedelta(hours=28)) == "a day"

    def test_few_days(self):
        """Several days returns 'a few days'."""
        assert humanize_duration(timedelta(days=3)) == "a few days"
        assert humanize_duration(timedelta(days=5)) == "a few days"

    def test_about_a_week(self):
        """About a week returns 'about a week'."""
        assert humanize_duration(timedelta(days=7)) == "about a week"
        assert humanize_duration(timedelta(days=10)) == "about a week"

    def test_multiple_weeks(self):
        """Multiple weeks return 'about X weeks'."""
        assert humanize_duration(timedelta(days=21)) == "about 3 weeks"

    def test_negative_duration(self):
        """Negative durations return 'moments ago'."""
        assert humanize_duration(timedelta(hours=-1)) == "moments ago"


# =============================================================================
# Test: _select_pattern
# =============================================================================


class TestSelectPattern:
    """Tests for the _select_pattern() helper."""

    def test_returns_pattern_from_list(self):
        """Selected pattern is from the input list."""
        patterns = ["A", "B", "C"]
        result = _select_pattern(patterns, "any-seed")
        assert result in patterns

    def test_deterministic_for_same_seed(self):
        """Same seed always returns same pattern."""
        patterns = ["A", "B", "C"]
        result1 = _select_pattern(patterns, "consistent-seed")
        result2 = _select_pattern(patterns, "consistent-seed")
        assert result1 == result2

    def test_different_seeds_may_differ(self):
        """Different seeds may return different patterns."""
        patterns = ["A", "B", "C", "D", "E"]  # More options for variation
        results = set()
        for i in range(100):
            result = _select_pattern(patterns, f"seed-{i}")
            results.add(result)
        # With enough seeds, we should see variety
        assert len(results) > 1

    def test_empty_patterns_returns_placeholder(self):
        """Empty pattern list returns placeholder."""
        assert _select_pattern([], "any") == "{destination}"


# =============================================================================
# Test: navigate_language
# =============================================================================


class TestNavigateLanguage:
    """Tests for the navigate_language() function."""

    def test_explicit_switch_uses_switch_to_patterns(self):
        """Explicit switches use switch_to patterns."""
        switch = make_switch(switch_type="explicit", to_name="#new-channel")
        result = navigate_language(switch)

        # Should contain the destination
        assert "#new-channel" in result

        # Should use one of the switch_to patterns (check common words)
        has_switch_pattern = any(
            word in result.lower() for word in ["over in", "looking at", "in your"]
        )
        assert has_switch_pattern

    def test_return_switch_uses_return_to_patterns(self):
        """Return switches use return_to patterns."""
        switch = make_switch(switch_type="return", to_name="#old-channel")
        result = navigate_language(switch)

        # Should contain the destination
        assert "#old-channel" in result

        # Should use one of the return_to patterns (check common words)
        has_return_pattern = any(
            word in result.lower() for word in ["back in", "returning", "picking up"]
        )
        assert has_return_pattern

    def test_return_switch_includes_time_away_over_hour(self):
        """Return switches include time-away for gaps > 1 hour."""
        switch = make_switch(
            switch_type="return",
            to_name="#channel",
            time_away=timedelta(hours=3),
        )
        result = navigate_language(switch, include_context=True)

        # Should include time reference
        assert "it's been" in result
        assert "hours" in result or "hour" in result

    def test_return_switch_excludes_time_away_under_hour(self):
        """Return switches exclude time-away for gaps < 1 hour."""
        switch = make_switch(
            switch_type="return",
            to_name="#channel",
            time_away=timedelta(minutes=30),
        )
        result = navigate_language(switch, include_context=True)

        # Should NOT include time reference
        assert "it's been" not in result

    def test_return_switch_respects_include_context_false(self):
        """Time-away excluded when include_context=False."""
        switch = make_switch(
            switch_type="return",
            to_name="#channel",
            time_away=timedelta(hours=5),
        )
        result = navigate_language(switch, include_context=False)

        # Should NOT include time reference
        assert "it's been" not in result

    def test_no_technical_identifiers_in_output(self):
        """Output contains no technical identifiers."""
        switch = make_switch(to_name="your Slack workspace")
        result = navigate_language(switch)

        # These should never appear
        assert "workspace_id" not in result
        assert "W123" not in result
        assert "integration:" not in result.lower()
        assert "source:" not in result.lower()


# =============================================================================
# Test: reference_language
# =============================================================================


class TestReferenceLanguage:
    """Tests for the reference_language() function."""

    def test_includes_location_and_observation(self):
        """Output includes both location and observation."""
        location = make_context(friendly_name="GitHub")
        result = reference_language(location, "there's a new PR")

        assert "GitHub" in result
        assert "PR" in result

    def test_uses_reference_patterns(self):
        """Uses reference patterns from dictionary."""
        location = make_context(friendly_name="#random")
        result = reference_language(location, "someone mentioned you")

        # Should use one of the reference patterns (check common words)
        has_reference_pattern = any(
            word in result.lower() for word in ["meanwhile", "over in", "in "]
        )
        assert has_reference_pattern

    def test_flows_naturally_with_i_see_pattern(self):
        """'I see...' pattern flows naturally into observation."""
        # Force a pattern that ends with "I see..."
        location = make_context(workspace_id="test-ws-for-i-see", friendly_name="GitHub")
        # Try several observations
        result = reference_language(location, "There's activity")

        # Should be grammatically smooth (lowercase after "I see...")
        # Either the pattern doesn't have "I see" or it flows well
        if "I see..." in result:
            # Observation should be lowercased
            assert "There's" not in result.split("I see...")[1] or "there's" in result

    def test_no_technical_identifiers_in_output(self):
        """Output contains no technical identifiers."""
        location = make_context(workspace_id="W123ABC", friendly_name="your calendar")
        result = reference_language(location, "you have a meeting")

        # Friendly name should appear, not workspace_id
        assert "your calendar" in result
        assert "W123ABC" not in result


# =============================================================================
# Test: Anti-Pattern Verification
# =============================================================================


class TestAntiPatterns:
    """Verify the module avoids anti-patterns from the spec."""

    def test_no_source_prefix(self):
        """Never outputs 'Source: ...'."""
        switch = make_switch(to_name="GitHub")
        result = navigate_language(switch)
        assert "Source:" not in result

    def test_no_integration_prefix(self):
        """Never outputs 'Integration: ...'."""
        switch = make_switch(to_name="#channel")
        result = navigate_language(switch)
        assert "Integration:" not in result

    def test_no_context_changed_to(self):
        """Never outputs 'Context changed to: ...'."""
        switch = make_switch(to_name="web chat")
        result = navigate_language(switch)
        assert "Context changed" not in result

    def test_no_raw_urls(self):
        """Never outputs raw URLs."""
        location = make_context(friendly_name="GitHub")
        result = reference_language(location, "check this out")
        assert "https://" not in result
        assert "http://" not in result
        assert "github.com" not in result
