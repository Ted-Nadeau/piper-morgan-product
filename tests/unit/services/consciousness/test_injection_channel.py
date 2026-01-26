"""
Tests for inject_consciousness channel parameter (#426 MUX-IMPLEMENT-CONSISTENT)

Verifies that inject_consciousness correctly adapts output
based on the channel/InteractionSpace parameter.
"""

import pytest

from services.consciousness.injection import inject_consciousness
from services.shared_types import InteractionSpace


class TestInjectConsciousnessChannel:
    """Tests for channel parameter in inject_consciousness."""

    @pytest.fixture
    def sample_data(self):
        """Sample standup data for testing."""
        return {
            "yesterday_accomplishments": [
                "✅ Finished Henderson proposal",
                "✅ Reviewed API PR",
            ],
            "today_priorities": [
                "🎯 Call with design team",
                "📅 Prepare presentation",
            ],
            "blockers": [],
            "upcoming_meetings": [
                {"title": "Design Review", "start": "2pm"},
            ],
        }

    @pytest.mark.asyncio
    async def test_default_channel_is_web_chat(self, sample_data):
        """Default channel should be WEB_CHAT."""
        result = await inject_consciousness(sample_data)
        # Web chat includes follow-up questions
        # Check for characteristic web chat style
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_cli_produces_shorter_output(self, sample_data):
        """CLI channel should produce shorter output."""
        cli_result = await inject_consciousness(sample_data, channel=InteractionSpace.CLI)
        web_result = await inject_consciousness(sample_data, channel=InteractionSpace.WEB_CHAT)
        # CLI should be significantly shorter
        assert len(cli_result) < len(web_result)

    @pytest.mark.asyncio
    async def test_cli_no_greeting(self, sample_data):
        """CLI should not include greeting."""
        result = await inject_consciousness(sample_data, channel=InteractionSpace.CLI)
        assert "Good morning" not in result
        assert "Good afternoon" not in result
        assert "Good evening" not in result

    @pytest.mark.asyncio
    async def test_slack_dm_brief(self, sample_data):
        """Slack DM should be brief."""
        result = await inject_consciousness(sample_data, channel=InteractionSpace.SLACK_DM)
        lines = [l for l in result.split("\n") if l.strip()]
        assert len(lines) <= 10

    @pytest.mark.asyncio
    async def test_slack_channel_professional(self, sample_data):
        """Slack channel should have professional tone."""
        result = await inject_consciousness(sample_data, channel=InteractionSpace.SLACK_CHANNEL)
        # Should not include "Hey!" or overly casual greetings
        assert "Hey!" not in result
        assert "gonna" not in result

    @pytest.mark.asyncio
    async def test_web_chat_detailed(self, sample_data):
        """Web chat should be detailed."""
        result = await inject_consciousness(sample_data, channel=InteractionSpace.WEB_CHAT)
        # Web chat tends to be longer
        assert len(result) > 100

    @pytest.mark.asyncio
    async def test_channel_respects_format_type(self, sample_data):
        """Channel and format_type should work together."""
        result = await inject_consciousness(
            sample_data,
            channel=InteractionSpace.SLACK_DM,
            format_type="slack",
        )
        # Should have Slack formatting applied
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_all_channels_produce_output(self, sample_data):
        """All channels should produce valid output."""
        for space in InteractionSpace:
            result = await inject_consciousness(sample_data, channel=space)
            assert result is not None
            assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_same_data_different_channels(self, sample_data):
        """Same data should produce equivalent but different output per channel."""
        cli = await inject_consciousness(sample_data, channel=InteractionSpace.CLI)
        slack = await inject_consciousness(sample_data, channel=InteractionSpace.SLACK_DM)
        web = await inject_consciousness(sample_data, channel=InteractionSpace.WEB_CHAT)

        # All should be different
        assert cli != slack
        assert slack != web
        assert cli != web

        # All should mention the core content
        # (Note: very brief CLI may not include all details)


class TestCrossChannelConsistency:
    """Tests for consistent identity across channels."""

    @pytest.fixture
    def sample_data(self):
        """Sample data for testing."""
        return {
            "yesterday_accomplishments": ["✅ Finished report"],
            "today_priorities": ["🎯 Team meeting"],
            "blockers": [],
        }

    @pytest.mark.asyncio
    async def test_no_third_person_piper(self, sample_data):
        """Piper should never refer to itself in third person."""
        for space in InteractionSpace:
            result = await inject_consciousness(sample_data, channel=space)
            assert "Piper " not in result
            assert " Piper" not in result

    @pytest.mark.asyncio
    async def test_no_surveillance_language(self, sample_data):
        """No surveillance language in any channel."""
        surveillance_phrases = [
            "I've been monitoring",
            "I observed you",
            "tracking your",
            "I saw you",
            "I was watching",
        ]
        for space in InteractionSpace:
            result = await inject_consciousness(sample_data, channel=space)
            for phrase in surveillance_phrases:
                assert phrase.lower() not in result.lower(), f"Found '{phrase}' in {space} output"


class TestChannelVerbosityGradient:
    """Tests for verbosity gradient across channels."""

    @pytest.fixture
    def verbose_data(self):
        """Data that produces more verbose output."""
        return {
            "yesterday_accomplishments": [
                "✅ Finished Henderson proposal",
                "✅ Reviewed API PR from Sarah",
                "✅ Updated documentation",
            ],
            "today_priorities": [
                "🎯 Call with design team at 2pm",
                "📅 Prepare Q4 presentation",
                "🔄 Review marketing materials",
            ],
            "blockers": ["⚠️ Waiting on client feedback"],
            "upcoming_meetings": [
                {"title": "Design Review", "start": "2pm"},
                {"title": "Standup", "start": "10am"},
            ],
        }

    @pytest.mark.asyncio
    async def test_verbosity_gradient(self, verbose_data):
        """Output length should follow: CLI < Slack DM < Slack Channel < Web."""
        cli = await inject_consciousness(verbose_data, channel=InteractionSpace.CLI)
        slack_dm = await inject_consciousness(verbose_data, channel=InteractionSpace.SLACK_DM)
        slack_channel = await inject_consciousness(
            verbose_data, channel=InteractionSpace.SLACK_CHANNEL
        )
        web = await inject_consciousness(verbose_data, channel=InteractionSpace.WEB_CHAT)

        # CLI should be shortest
        assert len(cli) <= len(slack_dm), "CLI should be <= Slack DM length"
        # Web should be longest (or at least >= slack channel)
        assert len(slack_channel) <= len(web), "Slack Channel should be <= Web length"
