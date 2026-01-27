"""
Tests for Place domain model (#684 MUX-NAV-PLACES).

Tests the Place dataclass including:
- Basic instantiation
- Staleness detection
- Narrative generation (anti-flattening)
- Atmosphere properties
- Ownership metadata
"""

from datetime import datetime, timedelta, timezone

import pytest

from services.domain.models import Place
from services.mux.ownership import OwnershipCategory
from services.shared_types import HardnessLevel, PlaceConfidence, PlaceType


class TestPlaceCreation:
    """Test Place instantiation."""

    def test_minimal_place(self):
        """Place can be created with required fields."""
        place = Place(
            id="test-1",
            place_type=PlaceType.ISSUE_TRACKING,
            name="test repo",
            confidence=PlaceConfidence.HIGH,
            summary="I see some activity",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
        )
        assert place.id == "test-1"
        assert place.place_type == PlaceType.ISSUE_TRACKING
        assert place.name == "test repo"

    def test_place_with_details(self):
        """Place can include detailed data."""
        place = Place(
            id="test-2",
            place_type=PlaceType.TEMPORAL,
            name="your calendar",
            confidence=PlaceConfidence.MEDIUM,
            summary="I see 3 meetings today",
            source_url="https://calendar.google.com",
            hardness=HardnessLevel.HARD,
            details={"meetings": [{"title": "Standup", "time": "9:00 AM"}]},
        )
        assert place.details is not None
        assert "meetings" in place.details

    def test_place_ownership_is_federated(self):
        """Place ownership is always FEDERATED (external observation)."""
        place = Place(
            id="test-3",
            place_type=PlaceType.DOCUMENTATION,
            name="docs workspace",
            confidence=PlaceConfidence.LOW,
            summary="I see some pages",
            source_url="https://notion.so",
            hardness=HardnessLevel.SOFT,
        )
        assert place.ownership.category == OwnershipCategory.FEDERATED


class TestPlaceTypes:
    """Test all PlaceType values."""

    def test_issue_tracking_type(self):
        """ISSUE_TRACKING for GitHub, JIRA, etc."""
        assert PlaceType.ISSUE_TRACKING == "issue_tracking"

    def test_communication_type(self):
        """COMMUNICATION for Slack messages, email, etc."""
        assert PlaceType.COMMUNICATION == "communication"

    def test_temporal_type(self):
        """TEMPORAL for Calendar, meetings, etc."""
        assert PlaceType.TEMPORAL == "temporal"

    def test_documentation_type(self):
        """DOCUMENTATION for Notion, Confluence, etc."""
        assert PlaceType.DOCUMENTATION == "documentation"


class TestPlaceConfidence:
    """Test confidence levels."""

    def test_high_confidence(self):
        """HIGH for inline summary display."""
        assert PlaceConfidence.HIGH == "high"

    def test_medium_confidence(self):
        """MEDIUM for offer-to-expand display."""
        assert PlaceConfidence.MEDIUM == "medium"

    def test_low_confidence(self):
        """LOW for redirect-to-source display."""
        assert PlaceConfidence.LOW == "low"


class TestPlaceStaleness:
    """Test staleness detection."""

    def test_is_stale_when_no_last_fetched(self):
        """Place is stale if never fetched."""
        place = Place(
            id="stale-1",
            place_type=PlaceType.ISSUE_TRACKING,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
            last_fetched=None,
        )
        assert place.is_stale() is True

    def test_is_not_stale_when_recent(self):
        """Place is not stale if recently fetched."""
        place = Place(
            id="fresh-1",
            place_type=PlaceType.ISSUE_TRACKING,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
            last_fetched=datetime.now(timezone.utc),
        )
        assert place.is_stale() is False

    def test_is_stale_after_threshold(self):
        """Place is stale after max_age_minutes."""
        old_time = datetime.now(timezone.utc) - timedelta(minutes=10)
        place = Place(
            id="old-1",
            place_type=PlaceType.ISSUE_TRACKING,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
            last_fetched=old_time,
        )
        assert place.is_stale(max_age_minutes=5) is True
        assert place.is_stale(max_age_minutes=15) is False


class TestPlaceStalenessIndicator:
    """Test human-readable staleness."""

    def test_unknown_when_no_last_fetched(self):
        """Returns 'unknown' if never fetched."""
        place = Place(
            id="ind-1",
            place_type=PlaceType.ISSUE_TRACKING,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
            last_fetched=None,
        )
        assert place.get_staleness_indicator() == "unknown"

    def test_just_now_when_recent(self):
        """Returns 'just now' for very recent."""
        place = Place(
            id="ind-2",
            place_type=PlaceType.ISSUE_TRACKING,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
            last_fetched=datetime.now(timezone.utc),
        )
        assert place.get_staleness_indicator() == "just now"

    def test_minutes_ago(self):
        """Returns 'X min ago' for recent."""
        place = Place(
            id="ind-3",
            place_type=PlaceType.ISSUE_TRACKING,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
            last_fetched=datetime.now(timezone.utc) - timedelta(minutes=3),
        )
        indicator = place.get_staleness_indicator()
        assert "min ago" in indicator


class TestPlaceNarration:
    """Test anti-flattening narrative generation."""

    def test_narrative_includes_place_name(self):
        """Narrative starts with 'Over in {name}'."""
        place = Place(
            id="nar-1",
            place_type=PlaceType.ISSUE_TRACKING,
            name="piper-morgan repository",
            confidence=PlaceConfidence.HIGH,
            summary="I see 3 PRs waiting",
            source_url="https://github.com",
            hardness=HardnessLevel.HARD,
            last_fetched=datetime.now(timezone.utc),
        )
        narrative = place.narrate()
        assert "Over in piper-morgan repository" in narrative

    def test_narrative_includes_summary(self):
        """Narrative includes the summary."""
        place = Place(
            id="nar-2",
            place_type=PlaceType.TEMPORAL,
            name="your calendar",
            confidence=PlaceConfidence.HIGH,
            summary="I see 2 meetings today",
            source_url="https://calendar.google.com",
            hardness=HardnessLevel.HARD,
            last_fetched=datetime.now(timezone.utc),
        )
        narrative = place.narrate()
        assert "I see 2 meetings today" in narrative

    def test_narrative_uses_pipers_perspective(self):
        """Narrative uses 'I see' not 'API returned'."""
        place = Place(
            id="nar-3",
            place_type=PlaceType.ISSUE_TRACKING,
            name="GitHub",
            confidence=PlaceConfidence.HIGH,
            summary="I see activity",
            source_url="https://github.com",
            hardness=HardnessLevel.HARD,
            last_fetched=datetime.now(timezone.utc),
        )
        narrative = place.narrate()
        # Anti-flattening: no API language
        assert "API" not in narrative
        assert "returned" not in narrative
        assert "data" not in narrative


class TestPlaceAtmosphere:
    """Test atmosphere property for each type."""

    def test_issue_tracking_atmosphere(self):
        """ISSUE_TRACKING has collaborative atmosphere."""
        place = Place(
            id="atm-1",
            place_type=PlaceType.ISSUE_TRACKING,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
        )
        assert "collaborative" in place.atmosphere

    def test_communication_atmosphere(self):
        """COMMUNICATION has conversational atmosphere."""
        place = Place(
            id="atm-2",
            place_type=PlaceType.COMMUNICATION,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.MEDIUM,
        )
        assert "conversational" in place.atmosphere

    def test_temporal_atmosphere(self):
        """TEMPORAL has time-bounded atmosphere."""
        place = Place(
            id="atm-3",
            place_type=PlaceType.TEMPORAL,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.HARD,
        )
        assert "time-bounded" in place.atmosphere

    def test_documentation_atmosphere(self):
        """DOCUMENTATION has reference atmosphere."""
        place = Place(
            id="atm-4",
            place_type=PlaceType.DOCUMENTATION,
            name="test",
            confidence=PlaceConfidence.HIGH,
            summary="test",
            source_url="https://example.com",
            hardness=HardnessLevel.SOFT,
        )
        assert "reference" in place.atmosphere


class TestPlaceHardness:
    """Test trust-gated visibility via hardness."""

    def test_hardness_values_accepted(self):
        """All HardnessLevel values work."""
        for hardness in HardnessLevel:
            place = Place(
                id=f"hard-{hardness.name}",
                place_type=PlaceType.ISSUE_TRACKING,
                name="test",
                confidence=PlaceConfidence.HIGH,
                summary="test",
                source_url="https://example.com",
                hardness=hardness,
            )
            assert place.hardness == hardness
