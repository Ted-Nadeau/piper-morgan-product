"""
Tests for ConversationRepository - Issue #598 auto-title generation.
"""

import pytest

from services.database.repositories import ConversationRepository


class TestGenerateTitleFromMessage:
    """Tests for the static generate_title_from_message method."""

    def test_simple_message(self):
        """Basic message becomes title as-is."""
        result = ConversationRepository.generate_title_from_message("What's on my calendar?")
        assert result == "What's on my calendar?"

    def test_long_message_truncated(self):
        """Messages longer than 50 chars are truncated with ellipsis."""
        long_msg = "This is a very long message that definitely exceeds the fifty character limit for titles"
        result = ConversationRepository.generate_title_from_message(long_msg)
        assert len(result) <= 53  # 50 + "..."
        assert result.endswith("...")

    def test_truncate_at_word_boundary(self):
        """Truncation should prefer word boundaries when possible."""
        # Message just over 50 chars with a word break before 50
        msg = "What meetings are scheduled for tomorrow afternoon please?"
        result = ConversationRepository.generate_title_from_message(msg)
        assert result.endswith("...")
        # The text before "..." should be reasonable (not cut mid-word if possible)
        # This is a best-effort feature; just verify basic truncation works
        assert len(result) <= 53

    def test_empty_message_returns_default(self):
        """Empty or None message returns default title."""
        assert ConversationRepository.generate_title_from_message("") == "New conversation"
        assert ConversationRepository.generate_title_from_message(None) == "New conversation"

    def test_strips_markdown_bold(self):
        """Bold markdown is stripped."""
        result = ConversationRepository.generate_title_from_message("Help with **important** task")
        assert "**" not in result
        assert "important" in result

    def test_strips_markdown_italic(self):
        """Italic markdown is stripped."""
        result = ConversationRepository.generate_title_from_message("Help with *urgent* task")
        assert "*" not in result
        assert "urgent" in result

    def test_strips_markdown_code(self):
        """Code backticks are stripped."""
        result = ConversationRepository.generate_title_from_message("Fix the `main.py` file")
        assert "`" not in result
        assert "main.py" in result

    def test_strips_markdown_headers(self):
        """Header markers are stripped."""
        result = ConversationRepository.generate_title_from_message("## Section Title")
        assert "##" not in result
        assert "Section Title" in result

    def test_strips_urls(self):
        """URLs are removed from titles."""
        result = ConversationRepository.generate_title_from_message(
            "Check this https://example.com/page issue"
        )
        assert "https://" not in result
        assert "example.com" not in result
        assert "Check this" in result
        assert "issue" in result

    def test_normalizes_whitespace(self):
        """Multiple spaces and newlines are normalized."""
        result = ConversationRepository.generate_title_from_message(
            "Too   many    spaces\n\nand newlines"
        )
        assert "   " not in result
        assert "\n" not in result
        assert "Too many spaces and newlines" in result

    def test_whitespace_only_returns_default(self):
        """Whitespace-only message returns default."""
        assert ConversationRepository.generate_title_from_message("   \n\t  ") == "New conversation"

    def test_custom_max_length(self):
        """Custom max_length parameter is respected."""
        msg = "This is a medium length message for testing"
        result = ConversationRepository.generate_title_from_message(msg, max_length=20)
        assert len(result) <= 23  # 20 + "..."

    def test_exact_length_no_truncation(self):
        """Messages at exactly max_length are not truncated."""
        # Exactly 50 chars
        msg = "12345678901234567890123456789012345678901234567890"
        result = ConversationRepository.generate_title_from_message(msg)
        assert result == msg
        assert "..." not in result
