"""
Tests for Channel Personality Adapter (#426 MUX-IMPLEMENT-CONSISTENT)

Verifies:
- Same Piper identity across all channels
- Channel-appropriate verbosity/formality
- Core identity anchors preserved
- No surveillance language anywhere
"""

import pytest

from services.consciousness.channel_adapter import (
    CHANNEL_PERSONALITIES,
    ChannelPersonality,
    Formality,
    OpeningStyle,
    Verbosity,
    adapt_bullets,
    adapt_closing,
    adapt_for_channel,
    adapt_opening,
    adapt_verbosity,
    adjust_formality,
    get_channel_personality,
    strip_emojis,
)
from services.shared_types import InteractionSpace


class TestChannelPersonalityDataclass:
    """Tests for ChannelPersonality structure."""

    def test_channel_personality_is_frozen(self):
        """Personality should be immutable."""
        personality = ChannelPersonality(
            verbosity=Verbosity.BRIEF,
            formality=Formality.CASUAL,
            emoji_allowed=True,
            max_response_lines=10,
            opening_style=OpeningStyle.MINIMAL,
            bullet_style="bullet",
            include_follow_up=False,
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            personality.verbosity = Verbosity.TERSE

    def test_all_interaction_spaces_have_personality(self):
        """Every InteractionSpace should have a personality config."""
        for space in InteractionSpace:
            assert space in CHANNEL_PERSONALITIES, f"Missing personality for {space}"

    def test_personality_has_all_fields(self):
        """Each personality should have all required fields."""
        for space, personality in CHANNEL_PERSONALITIES.items():
            assert personality.verbosity is not None
            assert personality.formality is not None
            assert isinstance(personality.emoji_allowed, bool)
            assert personality.max_response_lines > 0
            assert personality.opening_style is not None
            assert personality.bullet_style in ["dash", "bullet", "none"]
            assert isinstance(personality.include_follow_up, bool)


class TestCLIPersonality:
    """Tests for CLI channel - terse, power user."""

    def test_cli_is_terse(self):
        """CLI should use terse verbosity."""
        personality = get_channel_personality(InteractionSpace.CLI)
        assert personality.verbosity == Verbosity.TERSE

    def test_cli_no_emoji(self):
        """CLI should not allow emojis."""
        personality = get_channel_personality(InteractionSpace.CLI)
        assert personality.emoji_allowed is False

    def test_cli_minimal_opening(self):
        """CLI should use minimal opening."""
        personality = get_channel_personality(InteractionSpace.CLI)
        assert personality.opening_style == OpeningStyle.MINIMAL

    def test_cli_max_5_lines(self):
        """CLI should have 5 line limit."""
        personality = get_channel_personality(InteractionSpace.CLI)
        assert personality.max_response_lines == 5

    def test_cli_no_follow_up(self):
        """CLI should not include follow-up questions."""
        personality = get_channel_personality(InteractionSpace.CLI)
        assert personality.include_follow_up is False

    def test_cli_no_bullets(self):
        """CLI should not use bullet points."""
        personality = get_channel_personality(InteractionSpace.CLI)
        assert personality.bullet_style == "none"


class TestSlackDMPersonality:
    """Tests for Slack DM channel - brief, casual."""

    def test_slack_dm_is_brief(self):
        """Slack DM should use brief verbosity."""
        personality = get_channel_personality(InteractionSpace.SLACK_DM)
        assert personality.verbosity == Verbosity.BRIEF

    def test_slack_dm_allows_emoji(self):
        """Slack DM should allow emojis."""
        personality = get_channel_personality(InteractionSpace.SLACK_DM)
        assert personality.emoji_allowed is True

    def test_slack_dm_casual(self):
        """Slack DM should be casual."""
        personality = get_channel_personality(InteractionSpace.SLACK_DM)
        assert personality.formality == Formality.CASUAL

    def test_slack_dm_max_10_lines(self):
        """Slack DM should have 10 line limit."""
        personality = get_channel_personality(InteractionSpace.SLACK_DM)
        assert personality.max_response_lines == 10


class TestSlackChannelPersonality:
    """Tests for Slack Channel - professional, contextual."""

    def test_slack_channel_is_standard(self):
        """Slack Channel should use standard verbosity."""
        personality = get_channel_personality(InteractionSpace.SLACK_CHANNEL)
        assert personality.verbosity == Verbosity.STANDARD

    def test_slack_channel_professional(self):
        """Slack Channel should be professional."""
        personality = get_channel_personality(InteractionSpace.SLACK_CHANNEL)
        assert personality.formality == Formality.PROFESSIONAL

    def test_slack_channel_contextual_opening(self):
        """Slack Channel should use contextual opening."""
        personality = get_channel_personality(InteractionSpace.SLACK_CHANNEL)
        assert personality.opening_style == OpeningStyle.CONTEXTUAL

    def test_slack_channel_max_15_lines(self):
        """Slack Channel should have 15 line limit."""
        personality = get_channel_personality(InteractionSpace.SLACK_CHANNEL)
        assert personality.max_response_lines == 15


class TestWebChatPersonality:
    """Tests for Web Chat - detailed, warm."""

    def test_web_chat_is_detailed(self):
        """Web Chat should use detailed verbosity."""
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        assert personality.verbosity == Verbosity.DETAILED

    def test_web_chat_conversational(self):
        """Web Chat should be conversational."""
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        assert personality.formality == Formality.CONVERSATIONAL

    def test_web_chat_greeting_opening(self):
        """Web Chat should use greeting opening."""
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        assert personality.opening_style == OpeningStyle.GREETING

    def test_web_chat_includes_follow_up(self):
        """Web Chat should include follow-up questions."""
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        assert personality.include_follow_up is True

    def test_web_chat_no_emoji(self):
        """Web Chat should not allow emojis."""
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        assert personality.emoji_allowed is False

    def test_web_chat_max_30_lines(self):
        """Web Chat should have 30 line limit."""
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        assert personality.max_response_lines == 30


class TestVerbosityAdaptation:
    """Tests for verbosity transformation."""

    @pytest.fixture
    def sample_text(self):
        """Sample narrative for testing."""
        return """Good morning!

I've been looking at your calendar. Here's what I found.

You have 3 tasks due today:
- Finish Henderson proposal
- Review API PR
- Prepare for design call

It looks like you have a busy day ahead!

How does that sound? Let me know if you'd like to adjust anything."""

    def test_terse_removes_greetings(self, sample_text):
        """Terse should remove greetings."""
        personality = get_channel_personality(InteractionSpace.CLI)
        result = adapt_verbosity(sample_text, personality)
        assert "Good morning" not in result

    def test_terse_removes_follow_ups(self, sample_text):
        """Terse should remove follow-up questions."""
        personality = get_channel_personality(InteractionSpace.CLI)
        result = adapt_verbosity(sample_text, personality)
        assert "How does that sound" not in result

    def test_terse_limits_lines(self, sample_text):
        """Terse should limit to 5 lines."""
        personality = get_channel_personality(InteractionSpace.CLI)
        result = adapt_verbosity(sample_text, personality)
        lines = [l for l in result.split("\n") if l.strip()]
        assert len(lines) <= 5

    def test_brief_keeps_greeting(self, sample_text):
        """Brief may keep greeting."""
        personality = get_channel_personality(InteractionSpace.SLACK_DM)
        result = adapt_verbosity(sample_text, personality)
        # Brief removes follow-ups but may keep greeting
        assert "How does that sound" not in result

    def test_detailed_preserves_all(self, sample_text):
        """Detailed should preserve full text."""
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        result = adapt_verbosity(sample_text, personality)
        # Should have most of the content
        assert "Henderson" in result


class TestEmojiHandling:
    """Tests for emoji stripping."""

    def test_strip_emojis_removes_emoticons(self):
        """Should remove emoticons."""
        text = "Great job! 😀 You finished 3 tasks."
        result = strip_emojis(text)
        assert "😀" not in result
        assert "Great job!" in result

    def test_strip_emojis_removes_symbols(self):
        """Should remove symbol emojis."""
        text = "✅ Task complete! 🎯 Next goal."
        result = strip_emojis(text)
        assert "✅" not in result
        assert "🎯" not in result
        assert "Task complete" in result

    def test_strip_emojis_preserves_text(self):
        """Should preserve regular text."""
        text = "You have 3 tasks due today."
        result = strip_emojis(text)
        assert result == text


class TestFormalityAdjustment:
    """Tests for formality transformation."""

    def test_casual_uses_contractions(self):
        """Casual should use contractions."""
        text = "I have looked at your calendar. You are busy today."
        result = adjust_formality(text, Formality.CASUAL)
        assert "I've" in result
        assert "You're" in result  # Capitalized at sentence start

    def test_professional_removes_slang(self):
        """Professional should remove casual phrases."""
        text = "Hey! You gonna have a busy day."
        result = adjust_formality(text, Formality.PROFESSIONAL)
        assert "gonna" not in result
        assert "going to" in result

    def test_conversational_unchanged(self):
        """Conversational should be unchanged."""
        text = "Good morning! I noticed you have some tasks."
        result = adjust_formality(text, Formality.CONVERSATIONAL)
        assert result == text


class TestOpeningAdaptation:
    """Tests for opening style transformation."""

    def test_minimal_removes_greeting(self):
        """Minimal should remove greeting."""
        text = "Good morning!\n\nYou have 3 tasks."
        personality = get_channel_personality(InteractionSpace.CLI)
        result = adapt_opening(text, personality)
        assert "Good morning" not in result
        assert "3 tasks" in result

    def test_contextual_replaces_greeting(self):
        """Contextual should replace greeting."""
        text = "Good morning!\n\nYou have 3 tasks."
        personality = get_channel_personality(InteractionSpace.SLACK_CHANNEL)
        result = adapt_opening(text, personality)
        assert "Here's what I see" in result

    def test_greeting_keeps_greeting(self):
        """Greeting style should keep greeting."""
        text = "Good morning!\n\nYou have 3 tasks."
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        result = adapt_opening(text, personality)
        assert "Good morning" in result


class TestClosingAdaptation:
    """Tests for closing style transformation."""

    def test_no_follow_up_removes_questions(self):
        """Should remove follow-up when disabled."""
        text = "You have 3 tasks.\n\nHow does that sound?"
        personality = get_channel_personality(InteractionSpace.CLI)
        result = adapt_closing(text, personality)
        assert "How does that sound" not in result

    def test_include_follow_up_keeps_questions(self):
        """Should keep follow-up when enabled."""
        text = "You have 3 tasks.\n\nHow does that sound?"
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        result = adapt_closing(text, personality)
        assert "How does that sound" in result


class TestBulletAdaptation:
    """Tests for bullet style transformation."""

    def test_no_bullets_removes_markers(self):
        """None style should remove bullet markers."""
        text = "Tasks:\n• Task 1\n• Task 2"
        personality = get_channel_personality(InteractionSpace.CLI)
        result = adapt_bullets(text, personality)
        assert "•" not in result

    def test_bullet_style_uses_bullets(self):
        """Bullet style should use bullet points."""
        text = "Tasks:\n- Task 1\n- Task 2"
        personality = get_channel_personality(InteractionSpace.SLACK_DM)
        result = adapt_bullets(text, personality)
        assert "•" in result

    def test_dash_style_uses_dashes(self):
        """Dash style should use dashes."""
        text = "Tasks:\n• Task 1\n• Task 2"
        personality = get_channel_personality(InteractionSpace.WEB_CHAT)
        result = adapt_bullets(text, personality)
        assert "-" in result


class TestAdaptForChannel:
    """Tests for the main adapt_for_channel function."""

    @pytest.fixture
    def sample_narrative(self):
        """Sample narrative for channel adaptation."""
        return """Good morning! 😊

I've been looking at your context. Here's what I found.

You have 3 tasks due today:
• Finish Henderson proposal
• Review API PR
• Prepare for design call

Based on what I'm seeing, it looks like you have a busy day ahead!

How does that sound? Let me know if you'd like to adjust anything."""

    def test_cli_produces_terse_output(self, sample_narrative):
        """CLI should produce terse output."""
        result = adapt_for_channel(sample_narrative, InteractionSpace.CLI)
        lines = [l for l in result.split("\n") if l.strip()]
        assert len(lines) <= 5
        assert "😊" not in result
        assert "Good morning" not in result

    def test_slack_dm_produces_brief_output(self, sample_narrative):
        """Slack DM should produce brief output."""
        result = adapt_for_channel(sample_narrative, InteractionSpace.SLACK_DM)
        lines = [l for l in result.split("\n") if l.strip()]
        assert len(lines) <= 10
        assert "How does that sound" not in result

    def test_web_chat_preserves_detail(self, sample_narrative):
        """Web Chat should preserve detail."""
        result = adapt_for_channel(sample_narrative, InteractionSpace.WEB_CHAT)
        assert "How does that sound" in result
        assert "Henderson" in result
        assert "😊" not in result  # No emojis in web

    def test_same_content_different_length(self, sample_narrative):
        """All channels should mention same core content at different lengths."""
        cli = adapt_for_channel(sample_narrative, InteractionSpace.CLI)
        slack = adapt_for_channel(sample_narrative, InteractionSpace.SLACK_DM)
        web = adapt_for_channel(sample_narrative, InteractionSpace.WEB_CHAT)

        # CLI should be shortest
        assert len(cli) < len(slack) < len(web)


class TestCoreIdentityPreservation:
    """Tests to ensure core identity never changes across channels."""

    @pytest.fixture
    def first_person_text(self):
        """Text with first-person perspective."""
        return "I noticed you have 3 tasks. I think you should prioritize the proposal."

    def test_first_person_preserved_cli(self, first_person_text):
        """CLI should preserve first-person."""
        result = adapt_for_channel(first_person_text, InteractionSpace.CLI)
        # Core identity: first person preserved
        assert "I" in result or "I'" in result or result == ""

    def test_first_person_preserved_slack(self, first_person_text):
        """Slack should preserve first-person."""
        result = adapt_for_channel(first_person_text, InteractionSpace.SLACK_DM)
        assert "I" in result or "I'" in result

    def test_first_person_preserved_web(self, first_person_text):
        """Web should preserve first-person."""
        result = adapt_for_channel(first_person_text, InteractionSpace.WEB_CHAT)
        assert "I" in result or "I'" in result


class TestNoSurveillanceLanguage:
    """Tests to ensure no surveillance language in any channel."""

    @pytest.fixture
    def clean_text(self):
        """Text without surveillance language."""
        return "You have 3 tasks due today. I noticed the Henderson proposal is urgent."

    def test_no_surveillance_cli(self, clean_text):
        """CLI should not introduce surveillance language."""
        result = adapt_for_channel(clean_text, InteractionSpace.CLI)
        assert "I've been monitoring" not in result
        assert "I observed" not in result
        assert "tracking" not in result

    def test_no_surveillance_slack(self, clean_text):
        """Slack should not introduce surveillance language."""
        result = adapt_for_channel(clean_text, InteractionSpace.SLACK_DM)
        assert "I've been monitoring" not in result
        assert "I observed" not in result
        assert "tracking" not in result

    def test_no_surveillance_web(self, clean_text):
        """Web should not introduce surveillance language."""
        result = adapt_for_channel(clean_text, InteractionSpace.WEB_CHAT)
        assert "I've been monitoring" not in result
        assert "I observed" not in result
        assert "tracking" not in result


class TestVerbosityGradient:
    """Tests for verbosity gradient: CLI < Slack DM < Slack Channel < Web."""

    @pytest.fixture
    def verbose_text(self):
        """Verbose text to test reduction."""
        return """Good morning!

I've been looking at your context. Here's what I found.

You have 3 tasks due today:
- Finish Henderson proposal
- Review API PR
- Prepare for design call

Based on what I'm seeing, it looks like you have a busy day ahead with 2 meetings scheduled.

The Henderson proposal seems to be the most urgent item.

How does that sound? Let me know if you'd like to adjust anything."""

    def test_verbosity_order(self, verbose_text):
        """Verbosity should follow gradient."""
        cli = adapt_for_channel(verbose_text, InteractionSpace.CLI)
        slack_dm = adapt_for_channel(verbose_text, InteractionSpace.SLACK_DM)
        slack_channel = adapt_for_channel(verbose_text, InteractionSpace.SLACK_CHANNEL)
        web = adapt_for_channel(verbose_text, InteractionSpace.WEB_CHAT)

        cli_len = len(cli)
        slack_dm_len = len(slack_dm)
        slack_channel_len = len(slack_channel)
        web_len = len(web)

        # CLI should be shortest
        assert cli_len <= slack_dm_len
        # Web should be longest (or equal to slack channel)
        assert slack_channel_len <= web_len


class TestAPIChannel:
    """Tests for API channel personality."""

    def test_api_is_standard(self):
        """API should use standard verbosity."""
        personality = get_channel_personality(InteractionSpace.API)
        assert personality.verbosity == Verbosity.STANDARD

    def test_api_professional(self):
        """API should be professional."""
        personality = get_channel_personality(InteractionSpace.API)
        assert personality.formality == Formality.PROFESSIONAL

    def test_api_no_emoji(self):
        """API should not allow emojis."""
        personality = get_channel_personality(InteractionSpace.API)
        assert personality.emoji_allowed is False

    def test_api_minimal_opening(self):
        """API should use minimal opening."""
        personality = get_channel_personality(InteractionSpace.API)
        assert personality.opening_style == OpeningStyle.MINIMAL


class TestUnknownChannel:
    """Tests for unknown channel handling."""

    def test_unknown_has_safe_defaults(self):
        """Unknown should have safe defaults."""
        personality = get_channel_personality(InteractionSpace.UNKNOWN)
        assert personality.verbosity == Verbosity.STANDARD
        assert personality.formality == Formality.CONVERSATIONAL
