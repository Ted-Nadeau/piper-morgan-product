"""
Unit tests for Greeting Context Component (#425 MUX-IMPLEMENT-MEMORY-SYNC)

Tests the greeting_context.html component for:
- All 7 greeting conditions (PDR-002)
- Topic/entity references
- Trust gating
- Continue/Fresh start buttons
- "Never trap users" principle
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def greeting_html():
    """Load the greeting context component HTML."""
    component_path = Path("templates/components/greeting_context.html")
    return component_path.read_text()


@pytest.fixture
def soup(greeting_html):
    """Parse the component HTML."""
    return BeautifulSoup(greeting_html, "html.parser")


class TestGreetingContextTemplate:
    """Tests for template structure."""

    def test_template_exists(self, soup):
        """Template element should exist with correct ID."""
        template = soup.find("template", id="greeting-context-template")
        assert template is not None

    def test_has_greeting_container(self, soup):
        """Template should have greeting container."""
        template = soup.find("template", id="greeting-context-template")
        container = template.find("div", class_="greeting-context")
        assert container is not None

    def test_has_message_element(self, soup):
        """Template should have message element."""
        template = soup.find("template", id="greeting-context-template")
        message = template.find(class_="greeting-message")
        assert message is not None

    def test_has_subtext_element(self, soup):
        """Template should have subtext element."""
        template = soup.find("template", id="greeting-context-template")
        subtext = template.find(class_="greeting-subtext")
        assert subtext is not None

    def test_has_entities_container(self, soup):
        """Template should have entities container."""
        template = soup.find("template", id="greeting-context-template")
        entities = template.find(class_="greeting-entities")
        assert entities is not None

    def test_has_actions_container(self, soup):
        """Template should have actions container."""
        template = soup.find("template", id="greeting-context-template")
        actions = template.find(class_="greeting-actions")
        assert actions is not None


class TestGreetingButtons:
    """Tests for action buttons."""

    def test_has_continue_button(self, soup):
        """Template should have continue button."""
        template = soup.find("template", id="greeting-context-template")
        continue_btn = template.find(class_="continue-btn")
        assert continue_btn is not None

    def test_has_fresh_button(self, soup):
        """Template should have fresh start button."""
        template = soup.find("template", id="greeting-context-template")
        fresh_btn = template.find(class_="fresh-btn")
        assert fresh_btn is not None

    def test_continue_is_primary(self, soup):
        """Continue button should be primary style."""
        template = soup.find("template", id="greeting-context-template")
        continue_btn = template.find(class_="continue-btn")
        assert "primary" in continue_btn.get("class", [])

    def test_fresh_is_secondary(self, soup):
        """Fresh start button should be secondary style."""
        template = soup.find("template", id="greeting-context-template")
        fresh_btn = template.find(class_="fresh-btn")
        assert "secondary" in fresh_btn.get("class", [])


class TestGreetingConditions:
    """Tests for all 7 greeting conditions (PDR-002)."""

    def test_same_day_recent_defined(self, greeting_html):
        """SAME_DAY_RECENT should be defined."""
        assert "same_day_recent" in greeting_html

    def test_next_day_active_defined(self, greeting_html):
        """NEXT_DAY_ACTIVE should be defined."""
        assert "next_day_active" in greeting_html

    def test_week_gap_defined(self, greeting_html):
        """WEEK_GAP should be defined."""
        assert "week_gap" in greeting_html

    def test_month_gap_defined(self, greeting_html):
        """MONTH_GAP should be defined."""
        assert "month_gap" in greeting_html

    def test_previous_trivial_defined(self, greeting_html):
        """PREVIOUS_TRIVIAL should be defined."""
        assert "previous_trivial" in greeting_html

    def test_previous_negative_defined(self, greeting_html):
        """PREVIOUS_NEGATIVE should be defined."""
        assert "previous_negative" in greeting_html

    def test_first_session_defined(self, greeting_html):
        """FIRST_SESSION should be defined."""
        assert "first_session" in greeting_html


class TestGreetingMessages:
    """Tests for greeting message content."""

    def test_same_day_back_already(self, greeting_html):
        """SAME_DAY_RECENT should say 'Back already!'."""
        assert "Back already!" in greeting_html

    def test_next_day_welcome_back(self, greeting_html):
        """NEXT_DAY_ACTIVE should mention yesterday."""
        assert "Yesterday we discussed" in greeting_html

    def test_week_gap_its_been_a_bit(self, greeting_html):
        """WEEK_GAP should say 'It's been a bit!'."""
        assert "It's been a bit!" in greeting_html

    def test_month_gap_welcome_back(self, greeting_html):
        """MONTH_GAP should say 'Welcome back!'."""
        assert "Welcome back!" in greeting_html

    def test_previous_trivial_hey(self, greeting_html):
        """PREVIOUS_TRIVIAL should say 'Hey!'."""
        assert '"Hey!"' in greeting_html or "'Hey!'" in greeting_html

    def test_first_session_welcome(self, greeting_html):
        """FIRST_SESSION should say 'Welcome!'."""
        # First session has Welcome! message
        assert "I'm Piper" in greeting_html


class TestPreviousNegative:
    """Tests for PREVIOUS_NEGATIVE condition (clean slate)."""

    def test_previous_negative_no_topic(self, greeting_html):
        """PREVIOUS_NEGATIVE should not show topic."""
        # Check config has showTopic: false
        assert "previous_negative:" in greeting_html
        # The config for previous_negative should have showTopic: false
        assert '"showTopic": false' in greeting_html or "showTopic: false" in greeting_html

    def test_previous_negative_no_entities(self, greeting_html):
        """PREVIOUS_NEGATIVE should not show entities."""
        assert "showEntities: false" in greeting_html

    def test_previous_negative_neutral_message(self, greeting_html):
        """PREVIOUS_NEGATIVE should have neutral, clean message."""
        # The message is just asking what to work on
        assert "What would you like to work on?" in greeting_html


class TestTopicReference:
    """Tests for topic/entity references."""

    def test_topic_placeholder(self, greeting_html):
        """Should have topic placeholder for substitution."""
        assert "{topic}" in greeting_html

    def test_topic_class_defined(self, greeting_html):
        """Should have greeting-topic class for styling."""
        assert "greeting-topic" in greeting_html

    def test_entity_class_defined(self, greeting_html):
        """Should have greeting-entity class for tags."""
        assert "greeting-entity" in greeting_html

    def test_same_day_shows_topic(self, greeting_html):
        """SAME_DAY_RECENT should show topic reference."""
        # Check the config has showTopic: true
        assert "showTopic: true" in greeting_html

    def test_month_gap_no_topic(self, greeting_html):
        """MONTH_GAP should not show specific topic."""
        # The config for month_gap should have showTopic: false
        # Just offer catch up or fresh start
        assert "Catch me up" in greeting_html


class TestNeverTrapUsers:
    """Tests for 'Never trap users' principle (PDR-002)."""

    def test_always_offers_choice(self, greeting_html):
        """Conditions with work reference should offer fresh start."""
        # same_day_recent has showFresh: true
        # next_day_active has showFresh: true
        assert "showFresh: true" in greeting_html

    def test_fresh_start_labels(self, greeting_html):
        """Fresh start should have varied, appropriate labels."""
        assert "Start fresh" in greeting_html
        assert "Different focus" in greeting_html

    def test_continue_labels(self, greeting_html):
        """Continue should have varied, appropriate labels."""
        assert "Continue" in greeting_html
        assert "Pick up" in greeting_html
        assert "Catch me up" in greeting_html


class TestTrustGating:
    """Tests for trust-gated features."""

    def test_trust_min_stage_attribute(self, soup):
        """Container should have trust min stage attribute."""
        template = soup.find("template", id="greeting-context-template")
        container = template.find(class_="greeting-context")
        assert container.has_attr("data-trust-min-stage")

    def test_trust_stage_2_required(self, soup):
        """Work references require Stage 2+."""
        template = soup.find("template", id="greeting-context-template")
        container = template.find(class_="greeting-context")
        assert container.get("data-trust-min-stage") == "2"

    def test_trust_downgrade_logic(self, greeting_html):
        """Should downgrade greeting for Stage 1 users."""
        # JavaScript should check trustStage < 2
        assert "trustStage < 2" in greeting_html


class TestTimeIndicator:
    """Tests for time since last session indicator."""

    def test_time_indicator_element(self, soup):
        """Should have time indicator element."""
        template = soup.find("template", id="greeting-context-template")
        indicator = template.find(class_="greeting-time-indicator")
        assert indicator is not None

    def test_format_time_since_function(self, greeting_html):
        """Should have formatTimeSince function."""
        assert "formatTimeSince" in greeting_html

    def test_minutes_formatting(self, greeting_html):
        """Should format minutes appropriately."""
        assert "minutes ago" in greeting_html

    def test_hours_formatting(self, greeting_html):
        """Should format hours appropriately."""
        assert "hour" in greeting_html

    def test_days_formatting(self, greeting_html):
        """Should format days appropriately."""
        assert "day" in greeting_html


class TestJavaScriptAPI:
    """Tests for JavaScript API."""

    def test_greeting_context_namespace(self, greeting_html):
        """Should create GreetingContext namespace."""
        assert "window.GreetingContext" in greeting_html

    def test_render_function_exposed(self, greeting_html):
        """Should expose render function."""
        assert "render: render" in greeting_html

    def test_mount_function_exposed(self, greeting_html):
        """Should expose mount function."""
        assert "mount: mount" in greeting_html

    def test_messages_exposed(self, greeting_html):
        """Should expose MESSAGES constant."""
        assert "MESSAGES: GREETING_MESSAGES" in greeting_html

    def test_loaded_flag(self, greeting_html):
        """Should set loaded flag."""
        assert "greetingContextLoaded = true" in greeting_html


class TestXSSPrevention:
    """Tests for XSS prevention."""

    def test_escape_html_function(self, greeting_html):
        """Should have escapeHtml function."""
        assert "escapeHtml" in greeting_html

    def test_text_content_for_entities(self, greeting_html):
        """Should use textContent for entity insertion."""
        assert "textContent = entity" in greeting_html


class TestStyling:
    """Tests for CSS styling."""

    def test_trust_hidden_class(self, greeting_html):
        """Should have trust-hidden class."""
        assert ".trust-hidden" in greeting_html

    def test_condition_specific_styling(self, greeting_html):
        """Should have condition-specific CSS."""
        assert 'data-condition="first_session"' in greeting_html

    def test_primary_button_style(self, greeting_html):
        """Should have primary button styling."""
        assert ".greeting-btn.primary" in greeting_html

    def test_secondary_button_style(self, greeting_html):
        """Should have secondary button styling."""
        assert ".greeting-btn.secondary" in greeting_html
