"""Tests for Context Matcher"""
import pytest
from datetime import datetime, time

from services.learning.context_matcher import ContextMatcher


class TestContextMatcher:
    """Test ContextMatcher pattern matching"""

    @pytest.mark.asyncio
    async def test_empty_pattern_context_matches(self):
        """Empty pattern context should match any current context"""
        result = await ContextMatcher.matches({}, {"anything": "here"})
        assert result is True

    @pytest.mark.asyncio
    async def test_empty_current_context_with_pattern(self):
        """Empty current context should fail if pattern has triggers"""
        pattern_context = {"trigger_time": "after standup"}
        current_context = {}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is False

    @pytest.mark.asyncio
    async def test_temporal_standup_match(self):
        """Test 'after standup' temporal matching"""
        pattern_context = {"trigger_time": "after standup"}
        current_context = {"current_event": "standup_complete"}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True

    @pytest.mark.asyncio
    async def test_temporal_eod_match(self):
        """Test 'end of day' temporal matching"""
        pattern_context = {"trigger_time": "end of day"}
        current_context = {"current_event": "eod"}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True

    @pytest.mark.asyncio
    async def test_temporal_eod_variant(self):
        """Test 'eod' matches 'end_of_day' event"""
        pattern_context = {"trigger_time": "eod"}
        current_context = {"current_event": "end_of_day"}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True

    @pytest.mark.asyncio
    async def test_temporal_no_match(self):
        """Test temporal trigger doesn't match wrong event"""
        pattern_context = {"trigger_time": "after standup"}
        current_context = {"current_event": "meeting_complete"}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is False

    @pytest.mark.asyncio
    async def test_temporal_morning_time_match(self):
        """Test morning time matching"""
        pattern_context = {"trigger_time": "9am"}
        current_context = {"current_time": datetime(2025, 11, 14, 9, 30)}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True

    @pytest.mark.asyncio
    async def test_temporal_morning_keyword_match(self):
        """Test 'morning' keyword matches morning hours"""
        pattern_context = {"trigger_time": "morning"}
        current_context = {"current_time": datetime(2025, 11, 14, 10, 0)}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True

    @pytest.mark.asyncio
    async def test_temporal_time_no_match(self):
        """Test time trigger doesn't match afternoon"""
        pattern_context = {"trigger_time": "9am"}
        current_context = {"current_time": datetime(2025, 11, 14, 14, 0)}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is False

    @pytest.mark.asyncio
    async def test_sequential_after_action(self):
        """Test sequential 'after action' matching"""
        pattern_context = {"after_action": "create_github_issue"}
        current_context = {"last_action": "create_github_issue"}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True

    @pytest.mark.asyncio
    async def test_sequential_wrong_action(self):
        """Test sequential trigger doesn't match wrong action"""
        pattern_context = {"after_action": "create_github_issue"}
        current_context = {"last_action": "update_notion"}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is False

    @pytest.mark.asyncio
    async def test_sequential_missing_action(self):
        """Test sequential trigger fails when no last_action"""
        pattern_context = {"after_action": "create_github_issue"}
        current_context = {}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is False

    @pytest.mark.asyncio
    async def test_intent_matching(self):
        """Test intent-based matching"""
        pattern_context = {"trigger_intent": "GITHUB_ISSUE_CREATE"}
        current_context = {"intent": "GITHUB_ISSUE_CREATE"}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True

    @pytest.mark.asyncio
    async def test_intent_wrong_match(self):
        """Test intent trigger doesn't match wrong intent"""
        pattern_context = {"trigger_intent": "GITHUB_ISSUE_CREATE"}
        current_context = {"intent": "STATUS_CHECK"}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is False

    @pytest.mark.asyncio
    async def test_intent_missing(self):
        """Test intent trigger fails when no intent in context"""
        pattern_context = {"trigger_intent": "GITHUB_ISSUE_CREATE"}
        current_context = {}

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is False

    @pytest.mark.asyncio
    async def test_multiple_conditions_all_match(self):
        """Test all conditions must match"""
        pattern_context = {
            "trigger_time": "after standup",
            "trigger_intent": "STATUS_CHECK",
        }
        current_context = {
            "current_event": "standup_complete",
            "intent": "STATUS_CHECK",
        }

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True

    @pytest.mark.asyncio
    async def test_multiple_conditions_one_fails(self):
        """Test any failing condition returns False"""
        pattern_context = {
            "trigger_time": "after standup",
            "trigger_intent": "STATUS_CHECK",
        }
        current_context = {
            "current_event": "standup_complete",
            "intent": "DIFFERENT_INTENT",  # Wrong intent
        }

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is False

    @pytest.mark.asyncio
    async def test_multiple_conditions_all_types(self):
        """Test all trigger types together"""
        pattern_context = {
            "trigger_time": "after standup",
            "after_action": "create_github_issue",
            "trigger_intent": "STATUS_CHECK",
        }
        current_context = {
            "current_event": "standup_complete",
            "last_action": "create_github_issue",
            "intent": "STATUS_CHECK",
        }

        result = await ContextMatcher.matches(pattern_context, current_context)
        assert result is True


class TestCheckTemporal:
    """Test _check_temporal helper method"""

    def test_standup_event_match(self):
        """Test standup event matching"""
        result = ContextMatcher._check_temporal(
            "after standup", {"current_event": "standup_complete"}
        )
        assert result is True

    def test_case_insensitive_matching(self):
        """Test case-insensitive event matching"""
        result = ContextMatcher._check_temporal(
            "AFTER STANDUP", {"current_event": "Standup_Complete"}
        )
        assert result is True

    def test_eod_variations(self):
        """Test various end-of-day trigger formats"""
        # Test "eod" trigger
        assert ContextMatcher._check_temporal("eod", {"current_event": "eod"})
        assert ContextMatcher._check_temporal(
            "eod", {"current_event": "end_of_day"}
        )

        # Test "end of day" trigger
        assert ContextMatcher._check_temporal(
            "end of day", {"current_event": "eod"}
        )
        assert ContextMatcher._check_temporal(
            "end of day", {"current_event": "end_of_day"}
        )

    def test_no_match_returns_false(self):
        """Test unmatched triggers return False"""
        result = ContextMatcher._check_temporal(
            "after standup", {"current_event": "meeting_complete"}
        )
        assert result is False

    def test_missing_event_returns_false(self):
        """Test missing current_event returns False"""
        result = ContextMatcher._check_temporal("after standup", {})
        assert result is False

    def test_morning_time_range(self):
        """Test morning time range (7-11am)"""
        # Should match
        assert ContextMatcher._check_temporal(
            "morning", {"current_time": datetime(2025, 11, 14, 7, 0)}
        )
        assert ContextMatcher._check_temporal(
            "morning", {"current_time": datetime(2025, 11, 14, 9, 0)}
        )
        assert ContextMatcher._check_temporal(
            "morning", {"current_time": datetime(2025, 11, 14, 11, 0)}
        )

        # Should not match
        assert not ContextMatcher._check_temporal(
            "morning", {"current_time": datetime(2025, 11, 14, 6, 59)}
        )
        assert not ContextMatcher._check_temporal(
            "morning", {"current_time": datetime(2025, 11, 14, 12, 0)}
        )


class TestCalculateSimilarity:
    """Test _calculate_similarity helper method (placeholder for future)"""

    def test_returns_default_similarity(self):
        """Test placeholder returns 1.0 for alpha"""
        result = ContextMatcher._calculate_similarity({}, {})
        assert result == 1.0
