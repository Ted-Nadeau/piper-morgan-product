"""
Tests for SlackResponseContext.

Issue #620: GRAMMAR-TRANSFORM: Slack Integration
Phase 1: SlackResponseContext dataclass
"""

from datetime import datetime

import pytest

from services.integrations.slack.response_context import SlackResponseContext, _infer_valence
from services.integrations.slack.spatial_types import AttentionLevel, EmotionalValence
from services.shared_types import InteractionSpace


class TestSlackResponseContext:
    """Test SlackResponseContext dataclass."""

    def test_basic_creation(self):
        """Can create with minimal fields."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_DM,
            channel_id="D123",
        )
        assert ctx.place == InteractionSpace.SLACK_DM
        assert ctx.channel_id == "D123"
        assert ctx.attention_level == AttentionLevel.AMBIENT

    def test_full_creation(self):
        """Can create with all fields."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_CHANNEL,
            channel_id="C123",
            channel_name="general",
            is_thread=True,
            thread_ts="1234567890.123456",
            user_id="U123",
            user_display_name="Jesse",
            attention_level=AttentionLevel.DIRECT,
            is_direct_mention=True,
            recent_reactions=["thumbsup", "heart"],
            emotional_valence=EmotionalValence.POSITIVE,
            is_new_conversation=False,
            messages_in_thread=5,
        )
        assert ctx.channel_name == "general"
        assert ctx.is_thread is True
        assert ctx.user_display_name == "Jesse"
        assert ctx.messages_in_thread == 5


class TestFromSpatialContext:
    """Test from_spatial_context factory method."""

    def test_dm_detection(self):
        """Detects DM from is_dm flag."""
        ctx = SlackResponseContext.from_spatial_context(
            {
                "is_dm": True,
                "channel_id": "D123",
                "user_id": "U456",
            }
        )
        assert ctx.place == InteractionSpace.SLACK_DM
        assert ctx.channel_id == "D123"
        assert ctx.user_id == "U456"

    def test_channel_detection(self):
        """Detects channel from absence of is_dm."""
        ctx = SlackResponseContext.from_spatial_context(
            {
                "channel_id": "C123",
                "channel_name": "general",
            }
        )
        assert ctx.place == InteractionSpace.SLACK_CHANNEL
        assert ctx.channel_name == "general"

    def test_direct_mention_attention(self):
        """Direct mention sets DIRECT attention level."""
        ctx = SlackResponseContext.from_spatial_context(
            {
                "channel_id": "C123",
                "is_direct_mention": True,
            }
        )
        assert ctx.attention_level == AttentionLevel.DIRECT
        assert ctx.is_direct_mention is True

    def test_channel_mention_attention(self):
        """Channel mention sets FOCUSED attention level."""
        ctx = SlackResponseContext.from_spatial_context(
            {
                "channel_id": "C123",
                "is_channel_mention": True,
            }
        )
        assert ctx.attention_level == AttentionLevel.FOCUSED

    def test_thread_detection(self):
        """Detects thread from thread_ts."""
        ctx = SlackResponseContext.from_spatial_context(
            {
                "channel_id": "C123",
                "thread_ts": "1234567890.123456",
            }
        )
        assert ctx.is_thread is True
        assert ctx.thread_ts == "1234567890.123456"
        assert ctx.is_new_conversation is False

    def test_reactions_infer_valence(self):
        """Reactions infer emotional valence."""
        ctx = SlackResponseContext.from_spatial_context(
            {
                "channel_id": "C123",
                "recent_reactions": ["thumbsup", "heart"],
            }
        )
        assert ctx.emotional_valence == EmotionalValence.POSITIVE

    def test_handles_alternate_keys(self):
        """Handles alternate key names (channel vs channel_id)."""
        ctx = SlackResponseContext.from_spatial_context(
            {
                "channel": "C123",
                "user": "U456",
            }
        )
        assert ctx.channel_id == "C123"
        assert ctx.user_id == "U456"


class TestFormality:
    """Test formality determination."""

    def test_dm_is_casual(self):
        """DMs should be casual."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_DM,
            channel_id="D123",
        )
        assert ctx.get_formality() == "casual"

    def test_direct_mention_is_warm(self):
        """Direct mentions should be warm."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_CHANNEL,
            channel_id="C123",
            attention_level=AttentionLevel.DIRECT,
        )
        assert ctx.get_formality() == "warm"

    def test_channel_is_professional(self):
        """Regular channel messages should be professional."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_CHANNEL,
            channel_id="C123",
        )
        assert ctx.get_formality() == "professional"


class TestConciseness:
    """Test conciseness determination."""

    def test_channel_should_be_concise(self):
        """Channel responses should be concise."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_CHANNEL,
            channel_id="C123",
        )
        assert ctx.should_be_concise() is True

    def test_dm_can_be_detailed(self):
        """DM responses can be more detailed."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_DM,
            channel_id="D123",
        )
        assert ctx.should_be_concise() is False


class TestFrustrationDetection:
    """Test frustration signal detection."""

    def test_negative_valence_is_frustrated(self):
        """Negative emotional valence indicates frustration."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_DM,
            channel_id="D123",
            emotional_valence=EmotionalValence.NEGATIVE,
        )
        assert ctx.user_seems_frustrated() is True

    def test_many_thread_messages_is_frustrated(self):
        """Many messages in thread might indicate confusion."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_DM,
            channel_id="D123",
            is_new_conversation=False,
            messages_in_thread=5,
        )
        assert ctx.user_seems_frustrated() is True

    def test_normal_conversation_not_frustrated(self):
        """Normal conversation is not frustrated."""
        ctx = SlackResponseContext(
            place=InteractionSpace.SLACK_DM,
            channel_id="D123",
        )
        assert ctx.user_seems_frustrated() is False


class TestInferValence:
    """Test _infer_valence helper."""

    def test_empty_reactions_neutral(self):
        """Empty reactions return neutral."""
        assert _infer_valence([]) == EmotionalValence.NEUTRAL

    def test_positive_reactions(self):
        """Positive emoji returns positive."""
        assert _infer_valence(["thumbsup"]) == EmotionalValence.POSITIVE
        assert _infer_valence(["heart"]) == EmotionalValence.POSITIVE
        assert _infer_valence(["+1"]) == EmotionalValence.POSITIVE

    def test_negative_reactions(self):
        """Negative emoji returns negative."""
        assert _infer_valence(["thumbsdown"]) == EmotionalValence.NEGATIVE
        assert _infer_valence(["-1"]) == EmotionalValence.NEGATIVE
        assert _infer_valence(["x"]) == EmotionalValence.NEGATIVE

    def test_supportive_reactions(self):
        """Supportive emoji returns supportive."""
        assert _infer_valence(["muscle"]) == EmotionalValence.SUPPORTIVE
        assert _infer_valence(["pray"]) == EmotionalValence.SUPPORTIVE

    def test_first_match_wins(self):
        """First matched reaction determines valence."""
        # Order matters - negative first returns negative
        assert _infer_valence(["thumbsdown", "thumbsup"]) == EmotionalValence.NEGATIVE
        # Positive first returns positive
        assert _infer_valence(["thumbsup", "thumbsdown"]) == EmotionalValence.POSITIVE
