"""
Unit tests for Lifecycle Indicator Component (#423 MUX-IMPLEMENT-LIFECYCLE)

Tests the lifecycle_indicator.html component for all 8 stages.
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def lifecycle_html():
    """Load the lifecycle indicator component HTML."""
    component_path = Path("templates/components/lifecycle_indicator.html")
    return component_path.read_text()


@pytest.fixture
def soup(lifecycle_html):
    """Parse the component HTML."""
    return BeautifulSoup(lifecycle_html, "html.parser")


class TestLifecycleIndicatorTemplate:
    """Tests for template structure."""

    def test_template_exists(self, soup):
        """Template element should exist with correct ID."""
        template = soup.find("template", id="lifecycle-indicator-template")
        assert template is not None

    def test_template_has_indicator_class(self, soup):
        """Template should contain lifecycle-indicator element."""
        template = soup.find("template", id="lifecycle-indicator-template")
        indicator = template.find("div", class_="lifecycle-indicator")
        assert indicator is not None

    def test_data_attributes_present(self, soup):
        """Template should have required data attributes."""
        template = soup.find("template", id="lifecycle-indicator-template")
        indicator = template.find("div", class_="lifecycle-indicator")

        assert indicator.has_attr("data-lifecycle-stage")
        assert indicator.has_attr("data-compact")


class TestLifecycleStageColors:
    """Tests for stage colors (one per stage)."""

    @pytest.mark.parametrize(
        "stage,color",
        [
            ("emergent", "bfdbfe"),  # soft blue
            ("derived", "ddd6fe"),  # light purple
            ("noticed", "fef08a"),  # yellow
            ("proposed", "fed7aa"),  # orange
            ("ratified", "bbf7d0"),  # green
            ("deprecated", "e5e7eb"),  # gray
            ("archived", "f3f4f6"),  # light gray
            ("composted", "fde68a"),  # warm gold
        ],
    )
    def test_stage_has_color(self, lifecycle_html, stage, color):
        """Each stage should have its semantic color defined."""
        assert f'[data-lifecycle-stage="{stage}"]' in lifecycle_html
        assert color in lifecycle_html


class TestLifecycleExperiencePhrases:
    """Tests for experience phrases (must match backend)."""

    @pytest.mark.parametrize(
        "stage,phrase",
        [
            ("emergent", "I just noticed..."),
            ("derived", "I figured out from..."),
            ("noticed", "I'm aware of..."),
            ("proposed", "I think we should..."),
            ("ratified", "We're doing..."),
            ("deprecated", "This used to be..."),
            ("archived", "I remember when..."),
            ("composted", "I learned that..."),
        ],
    )
    def test_stage_has_experience_phrase(self, lifecycle_html, stage, phrase):
        """Each stage should have correct experience phrase."""
        assert f'{stage}: "{phrase}"' in lifecycle_html


class TestLifecycleIndicatorElements:
    """Tests for indicator elements."""

    def test_has_dot_element(self, soup):
        """Indicator should have colored dot."""
        template = soup.find("template", id="lifecycle-indicator-template")
        dot = template.find("span", class_="lifecycle-dot")
        assert dot is not None

    def test_has_phrase_element(self, soup):
        """Indicator should have phrase text element."""
        template = soup.find("template", id="lifecycle-indicator-template")
        phrase = template.find("span", class_="lifecycle-phrase")
        assert phrase is not None

    def test_has_tooltip_element(self, soup):
        """Indicator should have tooltip element."""
        template = soup.find("template", id="lifecycle-indicator-template")
        tooltip = template.find("span", class_="lifecycle-tooltip")
        assert tooltip is not None

    def test_has_forward_element(self, soup):
        """Indicator should have forward-looking message element."""
        template = soup.find("template", id="lifecycle-indicator-template")
        forward = template.find("span", class_="lifecycle-forward")
        assert forward is not None


class TestLifecycleIndicatorAccessibility:
    """Tests for accessibility."""

    def test_indicator_has_role(self, soup):
        """Indicator should have status role."""
        template = soup.find("template", id="lifecycle-indicator-template")
        indicator = template.find("div", class_="lifecycle-indicator")
        assert indicator.get("role") == "status"

    def test_indicator_is_focusable(self, soup):
        """Indicator should be keyboard focusable for tooltip."""
        template = soup.find("template", id="lifecycle-indicator-template")
        indicator = template.find("div", class_="lifecycle-indicator")
        assert indicator.get("tabindex") == "0"

    def test_indicator_has_aria_label(self, soup):
        """Indicator should have aria-label attribute."""
        template = soup.find("template", id="lifecycle-indicator-template")
        indicator = template.find("div", class_="lifecycle-indicator")
        assert indicator.has_attr("aria-label")

    def test_dot_is_hidden_from_screen_readers(self, soup):
        """Dot should be decorative (aria-hidden)."""
        template = soup.find("template", id="lifecycle-indicator-template")
        dot = template.find("span", class_="lifecycle-dot")
        assert dot.get("aria-hidden") == "true"

    def test_tooltip_has_role(self, soup):
        """Tooltip should have tooltip role."""
        template = soup.find("template", id="lifecycle-indicator-template")
        tooltip = template.find("span", class_="lifecycle-tooltip")
        assert tooltip.get("role") == "tooltip"


class TestLifecycleCompactMode:
    """Tests for compact mode styling."""

    def test_compact_mode_hides_phrase(self, lifecycle_html):
        """Compact mode should hide phrase text."""
        assert '[data-compact="true"] .lifecycle-phrase' in lifecycle_html
        assert "display: none" in lifecycle_html


class TestLifecycleJavaScript:
    """Tests for JavaScript API."""

    def test_lifecycle_indicator_namespace(self, lifecycle_html):
        """Should create LifecycleIndicator namespace."""
        assert "window.LifecycleIndicator" in lifecycle_html

    def test_create_function_exposed(self, lifecycle_html):
        """Should expose create function."""
        assert "create: createIndicator" in lifecycle_html

    def test_update_function_exposed(self, lifecycle_html):
        """Should expose update function."""
        assert "update: updateIndicator" in lifecycle_html

    def test_get_phrase_function_exposed(self, lifecycle_html):
        """Should expose getPhrase function."""
        assert "getPhrase: getExperiencePhrase" in lifecycle_html

    def test_get_color_function_exposed(self, lifecycle_html):
        """Should expose getColor function."""
        assert "getColor: getStageColor" in lifecycle_html

    def test_get_stages_function_exposed(self, lifecycle_html):
        """Should expose getStages function."""
        assert "getStages: getStages" in lifecycle_html

    def test_phrases_object_exposed(self, lifecycle_html):
        """Should expose PHRASES constant."""
        assert "PHRASES: EXPERIENCE_PHRASES" in lifecycle_html

    def test_colors_object_exposed(self, lifecycle_html):
        """Should expose COLORS constant."""
        assert "COLORS: STAGE_COLORS" in lifecycle_html


class TestLifecycleNoTechnicalLabels:
    """Tests to ensure no technical labels appear in user-facing text."""

    def test_no_uppercase_stage_names(self, lifecycle_html):
        """User-facing text should not contain UPPERCASE stage names."""
        # These technical labels should NOT appear in experience phrases or tooltips
        technical_labels = [
            "EMERGENT",
            "DERIVED",
            "NOTICED",
            "PROPOSED",
            "RATIFIED",
            "DEPRECATED",
            "ARCHIVED",
            "COMPOSTED",
        ]

        # Check that technical labels don't appear in the JavaScript strings
        # (they appear in CSS selectors which is fine)
        js_section = lifecycle_html.split("<script>")[1].split("</script>")[0]

        for label in technical_labels:
            # Should not appear in user-facing strings (inside quotes)
            assert (
                f'"{label}"' not in js_section
            ), f"Technical label {label} found in JavaScript strings"
            assert (
                f"'{label}'" not in js_section
            ), f"Technical label {label} found in JavaScript strings"


class TestLifecycleForwardMessages:
    """Tests for forward-looking messages."""

    def test_proposed_has_forward_message(self, lifecycle_html):
        """Proposed stage should show awaiting decision."""
        assert "proposed:" in lifecycle_html.lower()
        assert "awaiting decision" in lifecycle_html

    def test_ratified_has_forward_message(self, lifecycle_html):
        """Ratified stage should show in progress."""
        assert "ratified:" in lifecycle_html.lower()
        assert "in progress" in lifecycle_html


# ============================================================
# Lifecycle Detail Card Tests (#423 Phase 2)
# ============================================================


@pytest.fixture
def lifecycle_detail_html():
    """Load the lifecycle detail component HTML."""
    component_path = Path("templates/components/lifecycle_detail.html")
    return component_path.read_text()


@pytest.fixture
def detail_soup(lifecycle_detail_html):
    """Parse the detail component HTML."""
    return BeautifulSoup(lifecycle_detail_html, "html.parser")


class TestLifecycleDetailTemplate:
    """Tests for detail card template structure."""

    def test_detail_template_exists(self, detail_soup):
        """Detail template should exist."""
        template = detail_soup.find("template", id="lifecycle-detail-template")
        assert template is not None

    def test_step_template_exists(self, detail_soup):
        """Step template should exist."""
        template = detail_soup.find("template", id="lifecycle-step-template")
        assert template is not None

    def test_detail_has_journey_container(self, detail_soup):
        """Detail should have journey container."""
        template = detail_soup.find("template", id="lifecycle-detail-template")
        journey = template.find("div", class_="lifecycle-journey")
        assert journey is not None


class TestLifecycleDetailAccessibility:
    """Tests for detail card accessibility."""

    def test_detail_has_region_role(self, detail_soup):
        """Detail should have region role."""
        template = detail_soup.find("template", id="lifecycle-detail-template")
        detail = template.find("div", class_="lifecycle-detail")
        assert detail.get("role") == "region"

    def test_journey_has_list_role(self, detail_soup):
        """Journey should have list role."""
        template = detail_soup.find("template", id="lifecycle-detail-template")
        journey = template.find("div", class_="lifecycle-journey")
        assert journey.get("role") == "list"

    def test_step_has_listitem_role(self, detail_soup):
        """Step should have listitem role."""
        template = detail_soup.find("template", id="lifecycle-step-template")
        step = template.find("div", class_="lifecycle-step")
        assert step.get("role") == "listitem"

    def test_has_live_region(self, detail_soup):
        """Detail should have ARIA live region for updates."""
        template = detail_soup.find("template", id="lifecycle-detail-template")
        announcement = template.find(attrs={"aria-live": "polite"})
        assert announcement is not None


class TestLifecycleDetailStyling:
    """Tests for detail card styling."""

    def test_past_stages_have_styling(self, lifecycle_detail_html):
        """Past stages should have distinct styling."""
        assert '[data-status="past"]' in lifecycle_detail_html

    def test_current_stage_highlighted(self, lifecycle_detail_html):
        """Current stage should be highlighted."""
        assert '[data-status="current"]' in lifecycle_detail_html
        # Should have background highlight
        assert "background:" in lifecycle_detail_html

    def test_future_stages_grayed(self, lifecycle_detail_html):
        """Future stages should be grayed out."""
        assert '[data-status="future"]' in lifecycle_detail_html
        assert "opacity" in lifecycle_detail_html


class TestLifecycleDetailJavaScript:
    """Tests for detail card JavaScript."""

    def test_lifecycle_detail_namespace(self, lifecycle_detail_html):
        """Should create LifecycleDetail namespace."""
        assert "window.LifecycleDetail" in lifecycle_detail_html

    def test_create_function_exposed(self, lifecycle_detail_html):
        """Should expose create function."""
        assert "create: createDetail" in lifecycle_detail_html

    def test_update_function_exposed(self, lifecycle_detail_html):
        """Should expose update function."""
        assert "update: updateDetail" in lifecycle_detail_html

    def test_stage_order_constant(self, lifecycle_detail_html):
        """Should have correct stage order."""
        assert "STAGE_ORDER" in lifecycle_detail_html
        # Verify order is correct
        assert "'emergent'" in lifecycle_detail_html
        assert "'composted'" in lifecycle_detail_html

    def test_forward_messages_defined(self, lifecycle_detail_html):
        """Should have forward-looking messages."""
        assert "FORWARD_MESSAGES" in lifecycle_detail_html
        assert "Still forming" in lifecycle_detail_html
        assert "tracking progress" in lifecycle_detail_html


# ============================================================
# Lifecycle Notification Tests (#423 Phase 4)
# ============================================================


@pytest.fixture
def lifecycle_notification_html():
    """Load the lifecycle notification component HTML."""
    component_path = Path("templates/components/lifecycle_notification.html")
    return component_path.read_text()


@pytest.fixture
def notification_soup(lifecycle_notification_html):
    """Parse the notification component HTML."""
    return BeautifulSoup(lifecycle_notification_html, "html.parser")


class TestLifecycleNotificationTemplate:
    """Tests for notification component template."""

    def test_notification_container_exists(self, notification_soup):
        """Notification container should exist."""
        container = notification_soup.find("div", id="lifecycle-notifications")
        assert container is not None

    def test_notification_template_exists(self, notification_soup):
        """Notification template should exist."""
        template = notification_soup.find("template", id="lifecycle-notification-template")
        assert template is not None

    def test_notification_has_content_elements(self, notification_soup):
        """Notification should have title and message elements."""
        template = notification_soup.find("template", id="lifecycle-notification-template")
        title = template.find(class_="lifecycle-notification-title")
        message = template.find(class_="lifecycle-notification-message")
        assert title is not None
        assert message is not None

    def test_notification_has_dismiss_button(self, notification_soup):
        """Notification should have dismiss button."""
        template = notification_soup.find("template", id="lifecycle-notification-template")
        dismiss = template.find(class_="lifecycle-notification-dismiss")
        assert dismiss is not None


class TestLifecycleNotificationTrustGating:
    """Tests for notification trust gating."""

    def test_container_has_trust_gating(self, notification_soup):
        """Container should have trust-gating attribute."""
        container = notification_soup.find("div", id="lifecycle-notifications")
        assert container.has_attr("data-min-stage")
        assert container["data-min-stage"] == "3"

    def test_container_starts_hidden(self, notification_soup):
        """Container should start with trust-hidden class."""
        container = notification_soup.find("div", id="lifecycle-notifications")
        assert "trust-hidden" in container.get("class", [])

    def test_trust_hidden_style_exists(self, lifecycle_notification_html):
        """Trust-hidden CSS should hide the container."""
        assert ".lifecycle-notifications.trust-hidden" in lifecycle_notification_html
        assert "display: none" in lifecycle_notification_html


class TestLifecycleNotificationTransitions:
    """Tests for transition messages."""

    def test_transition_messages_defined(self, lifecycle_notification_html):
        """Should have transition messages object."""
        assert "TRANSITION_MESSAGES" in lifecycle_notification_html

    @pytest.mark.parametrize(
        "transition,message",
        [
            ("emergent_derived", "discovered a connection"),
            ("emergent_noticed", "is now on my radar"),
            ("derived_noticed", "tracking this now"),
            ("proposed_ratified", "is happening now"),
            ("ratified_archived", "complete, keeping for reference"),
            ("archived_composted", "became a learning"),
        ],
    )
    def test_transition_has_message(self, lifecycle_notification_html, transition, message):
        """Each transition should have natural language message."""
        assert transition in lifecycle_notification_html
        assert message in lifecycle_notification_html


class TestLifecycleNotificationAccessibility:
    """Tests for notification accessibility."""

    def test_container_has_aria_live(self, notification_soup):
        """Container should have aria-live for announcements."""
        container = notification_soup.find("div", id="lifecycle-notifications")
        assert container.get("aria-live") == "polite"

    def test_container_has_role(self, notification_soup):
        """Container should have region role."""
        container = notification_soup.find("div", id="lifecycle-notifications")
        assert container.get("role") == "region"

    def test_notification_has_alert_role(self, notification_soup):
        """Individual notification should have alert role."""
        template = notification_soup.find("template", id="lifecycle-notification-template")
        notification = template.find(class_="lifecycle-notification")
        assert notification.get("role") == "alert"

    def test_dismiss_has_aria_label(self, notification_soup):
        """Dismiss button should have aria-label."""
        template = notification_soup.find("template", id="lifecycle-notification-template")
        dismiss = template.find(class_="lifecycle-notification-dismiss")
        assert dismiss.has_attr("aria-label")


class TestLifecycleNotificationJavaScript:
    """Tests for notification JavaScript API."""

    def test_lifecycle_notification_namespace(self, lifecycle_notification_html):
        """Should create LifecycleNotification namespace."""
        assert "window.LifecycleNotification" in lifecycle_notification_html

    def test_show_function_exposed(self, lifecycle_notification_html):
        """Should expose show function."""
        assert "show: show" in lifecycle_notification_html

    def test_dismiss_function_exposed(self, lifecycle_notification_html):
        """Should expose dismiss function."""
        assert "dismiss: dismiss" in lifecycle_notification_html

    def test_clear_all_function_exposed(self, lifecycle_notification_html):
        """Should expose clearAll function."""
        assert "clearAll: clearAll" in lifecycle_notification_html

    def test_auto_dismiss_defined(self, lifecycle_notification_html):
        """Should have auto-dismiss timeout defined."""
        assert "AUTO_DISMISS_MS" in lifecycle_notification_html
        assert "5000" in lifecycle_notification_html


class TestLifecycleNotificationStyling:
    """Tests for notification styling."""

    def test_slide_in_animation(self, lifecycle_notification_html):
        """Should have slide-in animation."""
        assert "@keyframes slideIn" in lifecycle_notification_html

    def test_slide_out_animation(self, lifecycle_notification_html):
        """Should have slide-out animation."""
        assert "@keyframes slideOut" in lifecycle_notification_html

    def test_exiting_class_styling(self, lifecycle_notification_html):
        """Should have exiting class for animation."""
        assert ".lifecycle-notification.exiting" in lifecycle_notification_html

    def test_notification_positioned_fixed(self, lifecycle_notification_html):
        """Notifications should be fixed positioned."""
        assert "position: fixed" in lifecycle_notification_html
