"""
Unit tests for datetime utilities module.
Issue #750 (child of #747 - Timezone Support)

TDD Protocol: These tests written FIRST, before implementation.
"""

from datetime import datetime, timezone
from unittest.mock import patch

import pytest


class TestUtcNow:
    """Tests for utc_now() function."""

    def test_returns_datetime_object(self):
        """utc_now() should return a datetime object."""
        from services.utils.datetime_utils import utc_now

        result = utc_now()
        assert isinstance(result, datetime)

    def test_returns_timezone_aware_datetime(self):
        """utc_now() should return a timezone-aware datetime."""
        from services.utils.datetime_utils import utc_now

        result = utc_now()
        assert result.tzinfo is not None

    def test_returns_utc_timezone(self):
        """utc_now() should return datetime in UTC timezone."""
        from services.utils.datetime_utils import utc_now

        result = utc_now()
        assert result.tzinfo == timezone.utc

    def test_returns_current_time(self):
        """utc_now() should return approximately current time."""
        from services.utils.datetime_utils import utc_now

        before = datetime.now(timezone.utc)
        result = utc_now()
        after = datetime.now(timezone.utc)

        assert before <= result <= after


class TestEnsureUtc:
    """Tests for ensure_utc() function."""

    def test_converts_naive_datetime_to_utc(self):
        """ensure_utc() should convert naive datetime to UTC-aware."""
        from services.utils.datetime_utils import ensure_utc

        naive = datetime(2026, 1, 15, 12, 30, 45)
        result = ensure_utc(naive)

        assert result.tzinfo == timezone.utc
        assert result.year == 2026
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 12
        assert result.minute == 30
        assert result.second == 45

    def test_preserves_utc_aware_datetime(self):
        """ensure_utc() should pass through already UTC-aware datetime unchanged."""
        from services.utils.datetime_utils import ensure_utc

        aware = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        result = ensure_utc(aware)

        assert result == aware
        assert result.tzinfo == timezone.utc

    def test_converts_other_timezone_to_utc(self):
        """ensure_utc() should convert other timezone to UTC."""
        from services.utils.datetime_utils import ensure_utc

        # Create a datetime in UTC+5
        plus_five = timezone(offset=__import__("datetime").timedelta(hours=5))
        aware = datetime(2026, 1, 15, 17, 30, 45, tzinfo=plus_five)  # 5:30 PM UTC+5

        result = ensure_utc(aware)

        assert result.tzinfo == timezone.utc
        # 5:30 PM UTC+5 = 12:30 PM UTC
        assert result.hour == 12
        assert result.minute == 30

    def test_handles_none_gracefully(self):
        """ensure_utc() should return None if given None."""
        from services.utils.datetime_utils import ensure_utc

        result = ensure_utc(None)
        assert result is None


class TestIsTimezoneAware:
    """Tests for is_timezone_aware() function."""

    def test_returns_true_for_utc_aware(self):
        """is_timezone_aware() should return True for UTC-aware datetime."""
        from services.utils.datetime_utils import is_timezone_aware

        aware = datetime(2026, 1, 15, 12, 30, 45, tzinfo=timezone.utc)
        assert is_timezone_aware(aware) is True

    def test_returns_true_for_other_timezone(self):
        """is_timezone_aware() should return True for any timezone-aware datetime."""
        from services.utils.datetime_utils import is_timezone_aware

        plus_five = timezone(offset=__import__("datetime").timedelta(hours=5))
        aware = datetime(2026, 1, 15, 12, 30, 45, tzinfo=plus_five)
        assert is_timezone_aware(aware) is True

    def test_returns_false_for_naive(self):
        """is_timezone_aware() should return False for naive datetime."""
        from services.utils.datetime_utils import is_timezone_aware

        naive = datetime(2026, 1, 15, 12, 30, 45)
        assert is_timezone_aware(naive) is False

    def test_returns_false_for_none(self):
        """is_timezone_aware() should return False for None."""
        from services.utils.datetime_utils import is_timezone_aware

        assert is_timezone_aware(None) is False


class TestUtcNowCallable:
    """Tests for utc_now as a callable for SQLAlchemy defaults."""

    def test_can_be_used_as_default_callable(self):
        """utc_now should work as a SQLAlchemy column default."""
        from services.utils.datetime_utils import utc_now

        # Simulate SQLAlchemy calling the default
        result1 = utc_now()
        result2 = utc_now()

        # Each call should return a new datetime
        assert isinstance(result1, datetime)
        assert isinstance(result2, datetime)
        # They should be very close but potentially different
        assert result1.tzinfo == timezone.utc
        assert result2.tzinfo == timezone.utc


class TestNoDeprecationWarnings:
    """Tests verifying no deprecated datetime methods are used."""

    def test_utc_now_does_not_use_utcnow(self):
        """utc_now() should not use deprecated datetime.now(timezone.utc)."""
        import warnings

        from services.utils.datetime_utils import utc_now

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", DeprecationWarning)
            utc_now()
            # Filter for utcnow deprecation warnings
            utcnow_warnings = [warning for warning in w if "utcnow" in str(warning.message).lower()]
            assert len(utcnow_warnings) == 0, f"Found deprecation warnings: {utcnow_warnings}"

    def test_ensure_utc_does_not_use_utcnow(self):
        """ensure_utc() should not use deprecated datetime.now(timezone.utc)."""
        import warnings

        from services.utils.datetime_utils import ensure_utc

        naive = datetime(2026, 1, 15, 12, 30, 45)

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always", DeprecationWarning)
            ensure_utc(naive)
            utcnow_warnings = [warning for warning in w if "utcnow" in str(warning.message).lower()]
            assert len(utcnow_warnings) == 0, f"Found deprecation warnings: {utcnow_warnings}"
