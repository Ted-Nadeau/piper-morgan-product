"""
Tests for conversation summarizer.

Part of #664 MEM-ADR054-P4: Memory Integration.
"""

import pytest

from services.domain.models import ConversationTurn
from services.memory.conversation_summarizer import (
    NEGATIVE_SIGNALS,
    POSITIVE_SIGNALS,
    ConversationSummarizer,
    ConversationSummaryResult,
)

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture
def summarizer():
    """Default summarizer instance."""
    return ConversationSummarizer()


def make_turn(
    user_message: str = "",
    assistant_response: str = "",
    entities: list = None,
    intent: str = None,
) -> ConversationTurn:
    """Helper to create conversation turns."""
    return ConversationTurn(
        user_message=user_message,
        assistant_response=assistant_response,
        entities=entities or [],
        intent=intent,
    )


# =============================================================================
# ConversationSummaryResult Tests
# =============================================================================


class TestConversationSummaryResult:
    """Tests for ConversationSummaryResult dataclass."""

    def test_default_values(self):
        """Test default values."""
        result = ConversationSummaryResult(topic="Test topic")
        assert result.topic == "Test topic"
        assert result.entities == []
        assert result.outcome is None
        assert result.sentiment == "neutral"

    def test_to_dict(self):
        """Test serialization."""
        result = ConversationSummaryResult(
            topic="Discussed project",
            entities=["#123", "@alice"],
            outcome="completed",
            sentiment="positive",
        )
        d = result.to_dict()
        assert d["topic"] == "Discussed project"
        assert d["entities"] == ["#123", "@alice"]
        assert d["outcome"] == "completed"
        assert d["sentiment"] == "positive"


# =============================================================================
# Topic Extraction Tests
# =============================================================================


class TestTopicExtraction:
    """Tests for topic extraction."""

    def test_uses_first_meaningful_message(self, summarizer):
        """First user message with content becomes topic."""
        turns = [
            make_turn(user_message="Help me with sprint planning"),
            make_turn(user_message="What about the deadline?"),
        ]
        result = summarizer.summarize(turns)
        assert "sprint planning" in result.topic

    def test_skips_trivial_messages(self, summarizer):
        """Trivial messages like 'hi' are skipped."""
        turns = [
            make_turn(user_message="hi"),
            make_turn(user_message="Help me with the API"),
        ]
        result = summarizer.summarize(turns)
        assert "API" in result.topic

    def test_truncates_long_messages(self, summarizer):
        """Long messages are truncated."""
        long_message = "A" * 200
        turns = [make_turn(user_message=long_message)]
        result = summarizer.summarize(turns)
        assert len(result.topic) <= 103  # 100 + "..."

    def test_falls_back_to_intent(self, summarizer):
        """Falls back to intent if no meaningful message."""
        turns = [
            make_turn(user_message="hi", intent="greeting"),
            make_turn(user_message="ok", intent="acknowledgment"),
        ]
        result = summarizer.summarize(turns)
        assert "Intent:" in result.topic

    def test_empty_conversation(self, summarizer):
        """Handles empty conversation."""
        result = summarizer.summarize([])
        assert result.topic == "Empty conversation"
        assert result.sentiment == "neutral"

    def test_removes_markdown_formatting(self, summarizer):
        """Markdown formatting is cleaned."""
        turns = [make_turn(user_message="Help me with **bold** text")]
        result = summarizer.summarize(turns)
        assert "**" not in result.topic
        assert "bold" in result.topic

    def test_replaces_urls(self, summarizer):
        """URLs are replaced with placeholder."""
        turns = [make_turn(user_message="Check out https://example.com/page")]
        result = summarizer.summarize(turns)
        assert "https://" not in result.topic
        assert "[link]" in result.topic


# =============================================================================
# Entity Extraction Tests
# =============================================================================


class TestEntityExtraction:
    """Tests for entity extraction."""

    def test_aggregates_entities_from_all_turns(self, summarizer):
        """Entities are collected from all turns."""
        turns = [
            make_turn(entities=["#123", "@alice"]),
            make_turn(entities=["#456", "@bob"]),
        ]
        result = summarizer.summarize(turns)
        assert set(result.entities) == {"#123", "@alice", "#456", "@bob"}

    def test_deduplicates_entities(self, summarizer):
        """Duplicate entities are removed."""
        turns = [
            make_turn(entities=["#123", "@alice"]),
            make_turn(entities=["#123", "@bob"]),  # #123 duplicated
        ]
        result = summarizer.summarize(turns)
        assert result.entities.count("#123") == 1

    def test_preserves_order(self, summarizer):
        """Entity order is preserved (first occurrence)."""
        turns = [
            make_turn(entities=["#1", "#2"]),
            make_turn(entities=["#3"]),
        ]
        result = summarizer.summarize(turns)
        assert result.entities == ["#1", "#2", "#3"]

    def test_handles_no_entities(self, summarizer):
        """Handles conversations with no entities."""
        turns = [make_turn(user_message="Hello")]
        result = summarizer.summarize(turns)
        assert result.entities == []


# =============================================================================
# Outcome Inference Tests
# =============================================================================


class TestOutcomeInference:
    """Tests for outcome inference."""

    def test_detects_completion(self, summarizer):
        """Detects completion signals."""
        turns = [
            make_turn(user_message="Help me", assistant_response="Here's how"),
            make_turn(user_message="Thanks, that's done!", assistant_response="Great!"),
        ]
        result = summarizer.summarize(turns)
        assert result.outcome == "completed"

    def test_detects_blocked(self, summarizer):
        """Detects blocked signals."""
        turns = [
            make_turn(user_message="Help me", assistant_response="Try this"),
            make_turn(
                user_message="It doesn't work, I'm stuck",
                assistant_response="Let me help",
            ),
        ]
        result = summarizer.summarize(turns)
        assert result.outcome == "blocked"

    def test_detects_progress(self, summarizer):
        """Detects in-progress signals."""
        turns = [
            make_turn(user_message="Help me", assistant_response="Here's step 1"),
            make_turn(
                user_message="I'll continue tomorrow",
                assistant_response="See you then",
            ),
        ]
        result = summarizer.summarize(turns)
        assert result.outcome == "in_progress"

    def test_returns_none_when_unclear(self, summarizer):
        """Returns None when outcome is unclear."""
        turns = [
            make_turn(user_message="What's the weather?", assistant_response="Sunny"),
        ]
        result = summarizer.summarize(turns)
        assert result.outcome is None

    def test_completion_takes_precedence(self, summarizer):
        """Completion signals override others."""
        turns = [
            make_turn(
                user_message="It was broken but now it's fixed, thanks!",
                assistant_response="Glad it works!",
            ),
        ]
        result = summarizer.summarize(turns)
        assert result.outcome == "completed"


# =============================================================================
# Sentiment Detection Tests
# =============================================================================


class TestSentimentDetection:
    """Tests for sentiment detection."""

    def test_detects_positive_sentiment(self, summarizer):
        """Detects positive sentiment."""
        turns = [
            make_turn(
                user_message="Thanks! That's perfect, exactly what I needed!",
                assistant_response="You're welcome!",
            ),
            make_turn(
                user_message="This is great, really helpful",
                assistant_response="Glad I could help!",
            ),
        ]
        result = summarizer.summarize(turns)
        assert result.sentiment == "positive"

    def test_detects_negative_sentiment(self, summarizer):
        """Detects negative sentiment."""
        turns = [
            make_turn(
                user_message="This is frustrating, it's not working",
                assistant_response="Let me help",
            ),
            make_turn(
                user_message="Still broken, this is annoying",
                assistant_response="Sorry about that",
            ),
        ]
        result = summarizer.summarize(turns)
        assert result.sentiment == "negative"

    def test_defaults_to_neutral(self, summarizer):
        """Defaults to neutral sentiment."""
        turns = [
            make_turn(
                user_message="What's the status of issue 123?",
                assistant_response="It's open",
            ),
        ]
        result = summarizer.summarize(turns)
        assert result.sentiment == "neutral"

    def test_requires_multiple_signals(self, summarizer):
        """Requires multiple signals to override neutral."""
        turns = [
            make_turn(
                user_message="Thanks",  # Single positive
                assistant_response="You're welcome",
            ),
        ]
        result = summarizer.summarize(turns)
        assert result.sentiment == "neutral"  # Not enough signals

    def test_positive_wins_tie(self, summarizer):
        """With equal signals, sentiment is neutral."""
        turns = [
            make_turn(
                user_message="Thanks, but this is broken",  # 1 positive, 1 negative
                assistant_response="Let me fix it",
            ),
        ]
        result = summarizer.summarize(turns)
        assert result.sentiment == "neutral"


# =============================================================================
# Custom Configuration Tests
# =============================================================================


class TestCustomConfiguration:
    """Tests for custom summarizer configuration."""

    def test_custom_max_topic_length(self):
        """Custom max topic length is respected."""
        summarizer = ConversationSummarizer(max_topic_length=20)
        turns = [make_turn(user_message="A very long message that should be truncated")]
        result = summarizer.summarize(turns)
        assert len(result.topic) <= 23  # 20 + "..."

    def test_custom_positive_signals(self):
        """Custom positive signals work."""
        custom_positive = {"hooray", "yay"}
        summarizer = ConversationSummarizer(positive_signals=custom_positive)
        turns = [
            make_turn(user_message="Hooray! Yay!", assistant_response="Great!"),
            make_turn(user_message="Hooray again!", assistant_response="Awesome!"),
        ]
        result = summarizer.summarize(turns)
        assert result.sentiment == "positive"

    def test_custom_negative_signals(self):
        """Custom negative signals work."""
        custom_negative = {"bummer", "ugh"}
        summarizer = ConversationSummarizer(negative_signals=custom_negative)
        turns = [
            make_turn(user_message="Bummer, ugh", assistant_response="Sorry"),
            make_turn(user_message="Ugh, bummer", assistant_response="I understand"),
        ]
        result = summarizer.summarize(turns)
        assert result.sentiment == "negative"


# =============================================================================
# Edge Cases
# =============================================================================


class TestEdgeCases:
    """Tests for edge cases."""

    def test_handles_empty_messages(self, summarizer):
        """Handles turns with empty messages."""
        turns = [
            make_turn(user_message="", assistant_response="Hello!"),
            make_turn(user_message="Hi there", assistant_response=""),
        ]
        result = summarizer.summarize(turns)
        assert result.topic == "Hi there"

    def test_handles_whitespace_only(self, summarizer):
        """Handles whitespace-only messages."""
        turns = [
            make_turn(user_message="   ", assistant_response="Hello"),
            make_turn(user_message="Real message", assistant_response="Response"),
        ]
        result = summarizer.summarize(turns)
        assert "Real message" in result.topic

    def test_handles_special_characters(self, summarizer):
        """Handles special characters in messages."""
        turns = [
            make_turn(user_message="Help with @user's #issue-123 (urgent!)"),
        ]
        result = summarizer.summarize(turns)
        assert "@user" in result.topic or "issue" in result.topic


# =============================================================================
# Signal Word List Tests
# =============================================================================


class TestSignalWordLists:
    """Tests for signal word lists."""

    def test_positive_signals_exist(self):
        """Positive signals are defined."""
        assert len(POSITIVE_SIGNALS) > 0
        assert "thanks" in POSITIVE_SIGNALS
        assert "great" in POSITIVE_SIGNALS

    def test_negative_signals_exist(self):
        """Negative signals are defined."""
        assert len(NEGATIVE_SIGNALS) > 0
        assert "frustrated" in NEGATIVE_SIGNALS
        assert "broken" in NEGATIVE_SIGNALS
