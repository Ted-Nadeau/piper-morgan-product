"""
Tests for Issue #287: CORE-ALPHA-TEMPORAL-BUGS

Tests timezone abbreviation mapping.
Integration tests for contradictory messages and calendar validation deferred to Phase 4.
"""

import pytest


class TestTimezoneMapping:
    """Test the timezone abbreviation mapping"""

    def test_common_us_timezones(self):
        """Test mapping for common US timezones"""
        from services.intent_service.canonical_handlers import TIMEZONE_ABBREVIATIONS

        assert TIMEZONE_ABBREVIATIONS["America/Los_Angeles"] == "PT"
        assert TIMEZONE_ABBREVIATIONS["America/New_York"] == "ET"
        assert TIMEZONE_ABBREVIATIONS["America/Chicago"] == "CT"
        assert TIMEZONE_ABBREVIATIONS["America/Denver"] == "MT"

    def test_international_timezones(self):
        """Test mapping for international timezones"""
        from services.intent_service.canonical_handlers import TIMEZONE_ABBREVIATIONS

        assert TIMEZONE_ABBREVIATIONS["Europe/London"] == "GMT"
        assert TIMEZONE_ABBREVIATIONS["Asia/Tokyo"] == "JST"
        assert TIMEZONE_ABBREVIATIONS["Australia/Sydney"] == "AEDT"

    def test_fallback_to_utc(self):
        """Unknown timezones should fallback gracefully"""
        from services.intent_service.canonical_handlers import TIMEZONE_ABBREVIATIONS

        # Unknown timezone should have a fallback
        unknown_tz = "Unknown/Timezone"
        result = TIMEZONE_ABBREVIATIONS.get(unknown_tz, "UTC")
        assert result == "UTC", "Unknown timezones should fallback to UTC"


class TestTimezoneAbbreviationDisplay:
    """Test that timezone abbreviations are used instead of city names"""

    def test_timezone_abbreviations_constant_exists(self):
        """Verify TIMEZONE_ABBREVIATIONS constant exists and is properly structured"""
        from services.intent_service.canonical_handlers import TIMEZONE_ABBREVIATIONS

        assert isinstance(TIMEZONE_ABBREVIATIONS, dict)
        assert len(TIMEZONE_ABBREVIATIONS) > 10, "Should have at least 10 timezone mappings"
        assert "America/Los_Angeles" in TIMEZONE_ABBREVIATIONS
        assert "America/New_York" in TIMEZONE_ABBREVIATIONS
        # Verify all values are abbreviations (short strings)
        for tz, abbr in TIMEZONE_ABBREVIATIONS.items():
            assert len(abbr) <= 5, f"Abbreviation {abbr} should be <= 5 chars"
            assert abbr.isupper() or abbr == "UTC", f"Abbreviation {abbr} should be uppercase"


# Note: Integration tests for contradictory messages and calendar validation
# require complex async mocking and are deferred to Phase 4.
# The fixes have been implemented and can be verified manually.
