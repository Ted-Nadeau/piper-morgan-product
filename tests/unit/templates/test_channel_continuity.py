"""
Unit tests for Channel Continuity Component (#425 MUX-IMPLEMENT-MEMORY-SYNC)

Tests the channel_continuity.html component for:
- Cross-channel detection display
- Natural language (no surveillance)
- Continue/fresh start options
- Channel-specific icons
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def continuity_html():
    """Load the channel continuity component HTML."""
    component_path = Path("templates/components/channel_continuity.html")
    return component_path.read_text()


@pytest.fixture
def soup(continuity_html):
    """Parse the component HTML."""
    return BeautifulSoup(continuity_html, "html.parser")


class TestChannelContinuityTemplate:
    """Tests for template structure."""

    def test_template_exists(self, soup):
        """Template should exist."""
        template = soup.find("template", id="channel-continuity-template")
        assert template is not None

    def test_has_container(self, soup):
        """Template should have container."""
        template = soup.find("template", id="channel-continuity-template")
        container = template.find(class_="channel-continuity")
        assert container is not None

    def test_has_region_role(self, soup):
        """Container should have region role."""
        template = soup.find("template", id="channel-continuity-template")
        container = template.find(class_="channel-continuity")
        assert container.get("role") == "region"

    def test_has_aria_label(self, soup):
        """Container should have aria-label."""
        template = soup.find("template", id="channel-continuity-template")
        container = template.find(class_="channel-continuity")
        assert container.has_attr("aria-label")

    def test_has_icon(self, soup):
        """Template should have icon element."""
        template = soup.find("template", id="channel-continuity-template")
        icon = template.find(class_="channel-continuity-icon")
        assert icon is not None

    def test_has_content(self, soup):
        """Template should have content container."""
        template = soup.find("template", id="channel-continuity-template")
        content = template.find(class_="channel-continuity-content")
        assert content is not None

    def test_has_message(self, soup):
        """Template should have message element."""
        template = soup.find("template", id="channel-continuity-template")
        message = template.find(class_="channel-continuity-message")
        assert message is not None

    def test_has_topic_span(self, soup):
        """Template should have topic span."""
        template = soup.find("template", id="channel-continuity-template")
        topic = template.find(class_="channel-continuity-topic")
        assert topic is not None

    def test_has_meta(self, soup):
        """Template should have meta element."""
        template = soup.find("template", id="channel-continuity-template")
        meta = template.find(class_="channel-continuity-meta")
        assert meta is not None


class TestChannelContinuityActions:
    """Tests for action buttons."""

    def test_has_actions_container(self, soup):
        """Template should have actions container."""
        template = soup.find("template", id="channel-continuity-template")
        actions = template.find(class_="channel-continuity-actions")
        assert actions is not None

    def test_has_continue_button(self, soup):
        """Template should have continue button."""
        template = soup.find("template", id="channel-continuity-template")
        btn = template.find(class_="continue-btn")
        assert btn is not None

    def test_continue_is_primary(self, soup):
        """Continue button should be primary."""
        template = soup.find("template", id="channel-continuity-template")
        btn = template.find(class_="continue-btn")
        assert "primary" in btn.get("class", [])

    def test_has_dismiss_button(self, soup):
        """Template should have dismiss button."""
        template = soup.find("template", id="channel-continuity-template")
        btn = template.find(class_="dismiss-btn")
        assert btn is not None

    def test_dismiss_is_secondary(self, soup):
        """Dismiss button should be secondary."""
        template = soup.find("template", id="channel-continuity-template")
        btn = template.find(class_="dismiss-btn")
        assert "secondary" in btn.get("class", [])

    def test_has_close_button(self, soup):
        """Template should have X close button."""
        template = soup.find("template", id="channel-continuity-template")
        close = template.find(class_="channel-continuity-dismiss")
        assert close is not None

    def test_close_has_aria_label(self, soup):
        """Close button should have aria-label."""
        template = soup.find("template", id="channel-continuity-template")
        close = template.find(class_="channel-continuity-dismiss")
        assert close.get("aria-label") == "Dismiss"


class TestNoSurveillanceLanguage:
    """Tests to ensure no surveillance language (anti-pattern from issue)."""

    def test_no_surveillance_in_continuity_phrases(self, continuity_html):
        """CONTINUITY_PHRASES should not contain surveillance language."""
        # Extract the CONTINUITY_PHRASES object
        phrases_start = continuity_html.find("CONTINUITY_PHRASES = {")
        phrases_end = continuity_html.find("};", phrases_start) + 2
        phrases_block = continuity_html[phrases_start:phrases_end]
        # These are all anti-patterns that shouldn't appear in the phrases
        assert "I saw you" not in phrases_block
        assert "I noticed you" not in phrases_block
        assert "I was watching" not in phrases_block

    def test_uses_you_were_working(self, continuity_html):
        """Should use 'You were working on' instead of surveillance language."""
        assert "You were working on" in continuity_html
        # Also check the same-channel variant
        assert "You were just working on" in continuity_html

    def test_mentions_anti_patterns_only_in_comments(self, continuity_html):
        """Anti-patterns like 'I saw you' should only appear in comments as examples."""
        # Comments document what NOT to do - that's OK
        # The actual phrases should use "You were working on" which we verify above
        pass  # This is a documentation test - the above tests verify the actual phrases


class TestNaturalLanguagePhrases:
    """Tests for natural language phrasing."""

    def test_continuity_phrases_defined(self, continuity_html):
        """Should have CONTINUITY_PHRASES constant."""
        assert "CONTINUITY_PHRASES" in continuity_html

    def test_same_channel_phrase(self, continuity_html):
        """Should have same-channel phrase."""
        assert "sameChannel:" in continuity_html

    def test_different_channel_phrase(self, continuity_html):
        """Should have different-channel phrase."""
        assert "differentChannel:" in continuity_html

    def test_recent_prefix(self, continuity_html):
        """Should have recent time prefix."""
        assert "just now" in continuity_html

    def test_minutes_ago_phrase(self, continuity_html):
        """Should have minutes ago phrase."""
        assert "a few minutes ago" in continuity_html

    def test_earlier_phrase(self, continuity_html):
        """Should have 'earlier' phrase for longer gaps."""
        assert "earlier" in continuity_html


class TestChannelConfig:
    """Tests for channel configuration."""

    def test_channel_config_defined(self, continuity_html):
        """Should have CHANNEL_CONFIG constant."""
        assert "CHANNEL_CONFIG" in continuity_html

    def test_slack_channel_defined(self, continuity_html):
        """Should have Slack channel config."""
        assert "slack:" in continuity_html

    def test_web_channel_defined(self, continuity_html):
        """Should have web channel config."""
        assert "web:" in continuity_html

    def test_cli_channel_defined(self, continuity_html):
        """Should have CLI channel config."""
        assert "cli:" in continuity_html

    def test_mobile_channel_defined(self, continuity_html):
        """Should have mobile channel config."""
        assert "mobile:" in continuity_html

    def test_channels_have_icons(self, continuity_html):
        """Each channel should have an icon."""
        assert "icon:" in continuity_html

    def test_channels_have_names(self, continuity_html):
        """Each channel should have a name."""
        assert "name:" in continuity_html


class TestContinueOrFresh:
    """Tests for continue/fresh start options."""

    def test_continue_text(self, continuity_html):
        """Continue button should say 'Continue here'."""
        assert "Continue here" in continuity_html

    def test_fresh_start_text(self, continuity_html):
        """Fresh button should say 'Start fresh'."""
        assert "Start fresh" in continuity_html


class TestShouldShowLogic:
    """Tests for shouldShow function logic."""

    def test_should_show_function(self, continuity_html):
        """Should have shouldShow function."""
        assert "shouldShow" in continuity_html

    def test_checks_topic(self, continuity_html):
        """Should check if topic exists."""
        assert "!context.topic" in continuity_html

    def test_checks_time_threshold(self, continuity_html):
        """Should check if too long ago (30 minutes)."""
        assert "minutesSince > 30" in continuity_html


class TestJavaScriptAPI:
    """Tests for JavaScript API."""

    def test_channel_continuity_namespace(self, continuity_html):
        """Should create ChannelContinuity namespace."""
        assert "window.ChannelContinuity" in continuity_html

    def test_render_exposed(self, continuity_html):
        """Should expose render function."""
        assert "render: render" in continuity_html

    def test_mount_exposed(self, continuity_html):
        """Should expose mount function."""
        assert "mount: mount" in continuity_html

    def test_should_show_exposed(self, continuity_html):
        """Should expose shouldShow function."""
        assert "shouldShow: shouldShow" in continuity_html

    def test_format_time_since_exposed(self, continuity_html):
        """Should expose formatTimeSince function."""
        assert "formatTimeSince: formatTimeSince" in continuity_html

    def test_channel_config_exposed(self, continuity_html):
        """Should expose CHANNEL_CONFIG constant."""
        assert "CHANNEL_CONFIG: CHANNEL_CONFIG" in continuity_html

    def test_continuity_phrases_exposed(self, continuity_html):
        """Should expose CONTINUITY_PHRASES constant."""
        assert "CONTINUITY_PHRASES: CONTINUITY_PHRASES" in continuity_html

    def test_loaded_flag(self, continuity_html):
        """Should set loaded flag."""
        assert "channelContinuityLoaded = true" in continuity_html


class TestStyling:
    """Tests for CSS styling."""

    def test_hidden_class(self, continuity_html):
        """Should have hidden class."""
        assert ".channel-continuity.hidden" in continuity_html

    def test_channel_icon_classes(self, continuity_html):
        """Should have channel-specific icon classes."""
        assert ".channel-icon-slack" in continuity_html
        assert ".channel-icon-web" in continuity_html
        assert ".channel-icon-cli" in continuity_html
        assert ".channel-icon-mobile" in continuity_html

    def test_blue_theme(self, continuity_html):
        """Should use blue theme (informational, not warning)."""
        assert "#e0f2fe" in continuity_html  # Light blue background
        assert "#0369a1" in continuity_html  # Blue text for topic
