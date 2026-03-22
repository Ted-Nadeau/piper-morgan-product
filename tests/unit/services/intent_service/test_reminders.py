"""
Tests for Issue #903: Basic Reminder System

Covers:
- Pre-classifier reminder patterns
- Reminder time parsing (natural language → datetime)
- Reminder text extraction (strip command phrases)
- Reminder handler creates time-annotated todo
- Context assembler surfaces due reminders
"""

import re
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.intent_service.temporal_utils import parse_reminder_time


# ---------------------------------------------------------------------------
# Pre-classifier pattern tests
# ---------------------------------------------------------------------------


class TestReminderPreClassifierPatterns:
    """Issue #903: Verify reminder patterns classify correctly."""

    @pytest.mark.parametrize(
        "message",
        [
            "remind me to review PRs tomorrow",
            "remind me about the standup meeting",
            "set a reminder to check deployment",
            "set reminder for team sync",
            "create a reminder to update the docs",
            "don't let me forget to submit the report",
            "I need to remember to call the vendor",
        ],
    )
    def test_reminder_patterns_match(self, message):
        result = PreClassifier._matches_patterns(
            message.lower(), PreClassifier.REMINDER_PATTERNS
        )
        assert result is True, f"Pattern should match: {message}"

    @pytest.mark.parametrize(
        "message",
        [
            "show my todos",
            "what's the weather tomorrow",
            "add todo: review PRs",
            "close issue #123",
        ],
    )
    def test_non_reminder_messages_do_not_match(self, message):
        result = PreClassifier._matches_patterns(
            message.lower(), PreClassifier.REMINDER_PATTERNS
        )
        assert result is False, f"Pattern should NOT match: {message}"


# ---------------------------------------------------------------------------
# Time parsing tests
# ---------------------------------------------------------------------------


class TestParseReminderTime:
    """Issue #903: Natural language time parsing for reminders."""

    def test_in_minutes(self):
        dt, label = parse_reminder_time("remind me in 30 minutes")
        assert dt is not None
        assert "30 minute" in label
        # Should be roughly 30 minutes from now
        expected = datetime.now() + timedelta(minutes=30)
        assert abs((dt - expected).total_seconds()) < 5

    def test_in_hours(self):
        dt, label = parse_reminder_time("remind me in 2 hours")
        assert dt is not None
        assert "2 hour" in label
        expected = datetime.now() + timedelta(hours=2)
        assert abs((dt - expected).total_seconds()) < 5

    def test_in_days(self):
        dt, label = parse_reminder_time("remind me in 3 days")
        assert dt is not None
        assert "3 day" in label
        expected = datetime.now() + timedelta(days=3)
        assert abs((dt - expected).total_seconds()) < 5

    def test_tomorrow_default_morning(self):
        dt, label = parse_reminder_time("remind me tomorrow")
        assert dt is not None
        assert "tomorrow" in label
        tomorrow = datetime.now() + timedelta(days=1)
        assert dt.day == tomorrow.day
        assert dt.hour == 9  # Default morning

    def test_tomorrow_afternoon(self):
        dt, label = parse_reminder_time("remind me tomorrow afternoon")
        assert dt is not None
        assert "afternoon" in label
        assert dt.hour == 14

    def test_tomorrow_at_specific_time(self):
        dt, label = parse_reminder_time("remind me tomorrow at 3pm")
        assert dt is not None
        tomorrow = datetime.now() + timedelta(days=1)
        assert dt.day == tomorrow.day
        assert dt.hour == 15

    def test_next_week(self):
        dt, label = parse_reminder_time("remind me next week")
        assert dt is not None
        assert "next week" in label
        assert dt.hour == 9  # Default morning
        # Should be at least 1 day ahead (next Monday), at most 8
        diff = dt - datetime.now()
        hours_ahead = diff.total_seconds() / 3600
        assert hours_ahead > 0  # Must be in the future

    def test_day_name(self):
        dt, label = parse_reminder_time("remind me next Monday")
        assert dt is not None
        assert "Monday" in label
        assert dt.weekday() == 0  # Monday

    def test_fallback_to_tomorrow(self):
        """When no time is detected, default to tomorrow morning."""
        dt, label = parse_reminder_time("remind me to do something")
        assert dt is not None
        assert "tomorrow" in label
        assert dt.hour == 9


# ---------------------------------------------------------------------------
# Text extraction tests
# ---------------------------------------------------------------------------


class TestReminderTextExtraction:
    """Issue #903: Extract actionable text from reminder messages."""

    def setup_method(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        self.handlers = TodoIntentHandlers()

    def test_remind_me_to(self):
        text = self.handlers._extract_reminder_text("remind me to review PRs")
        assert text == "review prs"

    def test_remind_me_about(self):
        text = self.handlers._extract_reminder_text("remind me about the team meeting")
        assert text == "the team meeting"

    def test_set_reminder_to(self):
        text = self.handlers._extract_reminder_text("set a reminder to deploy the fix")
        assert text == "deploy the fix"

    def test_dont_forget(self):
        text = self.handlers._extract_reminder_text(
            "don't let me forget to submit the report"
        )
        assert text == "submit the report"

    def test_strips_time_suffix(self):
        """Time expressions should be stripped from the todo text."""
        text = self.handlers._extract_reminder_text(
            "remind me to review PRs tomorrow"
        )
        assert text == "review prs"
        assert "tomorrow" not in (text or "")

    def test_strips_in_n_hours(self):
        text = self.handlers._extract_reminder_text(
            "remind me to check the deploy in 2 hours"
        )
        assert text == "check the deploy"

    def test_empty_after_strip(self):
        text = self.handlers._extract_reminder_text("remind me to")
        assert text is None

    def test_no_match(self):
        text = self.handlers._extract_reminder_text("show my todos")
        assert text is None


# ---------------------------------------------------------------------------
# Handler integration test
# ---------------------------------------------------------------------------


class TestReminderHandler:
    """Issue #903: Test reminder creation handler."""

    @pytest.fixture
    def todo_handlers(self):
        from services.intent_service.todo_handlers import TodoIntentHandlers

        handlers = TodoIntentHandlers()
        return handlers

    @pytest.mark.asyncio
    async def test_creates_reminder_with_time(self, todo_handlers):
        """Reminder handler should create a todo with reminder_date."""
        from services.domain.models import Intent, Todo
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me to review PRs tomorrow"},
        )

        mock_todo = Todo(
            id=str(uuid4()),
            text="review prs",
            priority="medium",
            status="pending",
            completed=False,
        )

        with patch.object(
            todo_handlers.todo_service,
            "create_todo",
            new_callable=AsyncMock,
            return_value=mock_todo,
        ) as mock_create:
            result = await todo_handlers.handle_create_reminder(
                intent, "session-1", uuid4()
            )

            assert mock_create.called
            call_kwargs = mock_create.call_args
            # Should have reminder_date set
            assert call_kwargs.kwargs.get("reminder_date") is not None
            # Response should confirm the reminder
            assert "remind you" in result.lower() or "review prs" in result.lower()

    @pytest.mark.asyncio
    async def test_reminder_with_no_text_returns_help(self, todo_handlers):
        """Missing reminder text should return helpful message."""
        from services.domain.models import Intent
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.EXECUTION,
            action="create_reminder",
            context={"original_message": "remind me to"},
        )

        result = await todo_handlers.handle_create_reminder(
            intent, "session-1", uuid4()
        )
        assert "didn't catch" in result.lower() or "try" in result.lower()


# ---------------------------------------------------------------------------
# Context assembler reminder surfacing
# ---------------------------------------------------------------------------


class TestReminderContextSurfacing:
    """Issue #903: Due reminders appear in conversation context."""

    @pytest.mark.asyncio
    async def test_due_reminders_in_context(self):
        """When user has due reminders, they should appear in CONVERSATION context."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()

        with patch(
            "services.intent_service.todo_handlers.TodoIntentHandlers"
        ) as MockHandlers:
            mock_instance = MagicMock()
            mock_instance.get_due_reminders = AsyncMock(
                return_value=["review PRs", "check deployment"]
            )
            MockHandlers.return_value = mock_instance

            context = await assembler.gather_context(
                "CONVERSATION", user_id=str(uuid4())
            )

            assert "due_reminders" in context
            assert len(context["due_reminders"]) == 2
            assert context["reminder_count"] == 2

    @pytest.mark.asyncio
    async def test_no_reminders_no_context(self):
        """When no reminders are due, context should be clean."""
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()

        with patch(
            "services.intent_service.todo_handlers.TodoIntentHandlers"
        ) as MockHandlers:
            mock_instance = MagicMock()
            mock_instance.get_due_reminders = AsyncMock(return_value=[])
            MockHandlers.return_value = mock_instance

            context = await assembler.gather_context(
                "CONVERSATION", user_id=str(uuid4())
            )

            assert "due_reminders" not in context
