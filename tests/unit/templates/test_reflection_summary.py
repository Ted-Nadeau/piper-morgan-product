"""
Unit tests for Reflection Summary Component (#424 MUX-IMPLEMENT-COMPOST)

Tests the reflection_summary.html component for:
- Opener rotation (never same twice in row)
- Insight count limits (2-4)
- Confidence-based language
- Trust-gating (Stage 3+)
- D3 compliance (no surveillance language)
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def reflection_html():
    """Load the reflection summary component HTML."""
    component_path = Path("templates/components/reflection_summary.html")
    return component_path.read_text()


@pytest.fixture
def soup(reflection_html):
    """Parse the component HTML."""
    return BeautifulSoup(reflection_html, "html.parser")


class TestReflectionSummaryTemplate:
    """Tests for template structure."""

    def test_template_exists(self, soup):
        """Template element should exist with correct ID."""
        template = soup.find("template", id="reflection-summary-template")
        assert template is not None

    def test_insight_template_exists(self, soup):
        """Insight template element should exist."""
        template = soup.find("template", id="reflection-insight-template")
        assert template is not None

    def test_template_has_summary_class(self, soup):
        """Template should contain reflection-summary element."""
        template = soup.find("template", id="reflection-summary-template")
        summary = template.find("div", class_="reflection-summary")
        assert summary is not None

    def test_template_has_opener(self, soup):
        """Template should have opener element."""
        template = soup.find("template", id="reflection-summary-template")
        opener = template.find(class_="reflection-opener")
        assert opener is not None


class TestReflectionSummaryTrustGating:
    """Tests for trust gating (Stage 3+)."""

    def test_has_trust_gating_attribute(self, soup):
        """Summary should have data-min-stage attribute."""
        template = soup.find("template", id="reflection-summary-template")
        summary = template.find("div", class_="reflection-summary")
        assert summary.has_attr("data-min-stage")
        assert summary["data-min-stage"] == "3"

    def test_starts_with_trust_hidden(self, soup):
        """Summary should start with trust-hidden class."""
        template = soup.find("template", id="reflection-summary-template")
        summary = template.find("div", class_="reflection-summary")
        assert "trust-hidden" in summary.get("class", [])

    def test_trust_hidden_style_exists(self, reflection_html):
        """Trust-hidden CSS should hide the element."""
        assert ".reflection-summary.trust-hidden" in reflection_html
        assert "display: none" in reflection_html


class TestReflectionOpeners:
    """Tests for opener rotation (D3 compliance)."""

    def test_openers_defined(self, reflection_html):
        """Should have multiple openers defined."""
        assert "REFLECTION_OPENERS" in reflection_html

    def test_openers_from_d3_spec(self, reflection_html):
        """Openers should match D3 spec."""
        # From D3: "Vary reflection phrasing"
        expected_openers = [
            "Having had some time to reflect",
            "Something occurred to me",
            "I've been thinking",
            "Looking back at our work together",
        ]
        for opener_fragment in expected_openers:
            assert opener_fragment in reflection_html, f"Missing opener: {opener_fragment}"

    def test_last_opener_tracking(self, reflection_html):
        """Should track last opener to prevent repeats."""
        assert "lastOpenerIndex" in reflection_html

    def test_rotation_logic_exists(self, reflection_html):
        """Should have rotation logic that avoids immediate repeats."""
        assert "getRotatedOpener" in reflection_html
        # Check for the do-while pattern that prevents repeats
        assert "while (newIndex === lastOpenerIndex" in reflection_html


class TestReflectionInsightLimits:
    """Tests for insight count limits (D3: 2-4 max)."""

    def test_min_insights_defined(self, reflection_html):
        """Should have minimum insights constant."""
        assert "MIN_INSIGHTS" in reflection_html
        assert "MIN_INSIGHTS = 2" in reflection_html

    def test_max_insights_defined(self, reflection_html):
        """Should have maximum insights constant."""
        assert "MAX_INSIGHTS" in reflection_html
        assert "MAX_INSIGHTS = 4" in reflection_html

    def test_insights_sliced_to_max(self, reflection_html):
        """Should slice insights to MAX_INSIGHTS."""
        assert "slice(0, MAX_INSIGHTS)" in reflection_html


class TestReflectionConfidenceLanguage:
    """Tests for confidence-based language (D3 compliance)."""

    def test_confidence_language_defined(self, reflection_html):
        """Should have confidence language thresholds."""
        assert "CONFIDENCE_LANGUAGE" in reflection_html

    def test_high_confidence_no_qualifier(self, reflection_html):
        """High confidence (0.8+) should have no prefix qualifier."""
        # D3: "No qualifier needed" for high confidence
        assert "high:" in reflection_html
        # The prefix should be empty for high confidence
        assert 'prefix: ""' in reflection_html

    def test_medium_confidence_qualifier(self, reflection_html):
        """Medium confidence (0.6-0.8) should use 'I think...'."""
        # D3: "I think..." for medium confidence
        assert '"I think "' in reflection_html

    def test_low_confidence_qualifier(self, reflection_html):
        """Low confidence (0.4-0.6) should use 'I'm not sure...'."""
        # D3: "I'm not sure, but..." for low confidence
        assert "I'm not sure" in reflection_html

    def test_confidence_thresholds(self, reflection_html):
        """Should use correct confidence thresholds."""
        # D3: 0.8+ high, 0.6-0.8 medium, below 0.6 low
        assert "confidence >= 0.8" in reflection_html
        assert "confidence >= 0.6" in reflection_html


class TestReflectionDismiss:
    """Tests for dismiss behavior."""

    def test_has_dismiss_button(self, soup):
        """Should have dismiss button."""
        template = soup.find("template", id="reflection-summary-template")
        dismiss = template.find(class_="reflection-dismiss")
        assert dismiss is not None

    def test_dismiss_says_not_now(self, reflection_html):
        """Dismiss button should say 'Not now'."""
        # Check the HTML contains "Not now" in the dismiss button
        assert 'class="reflection-dismiss"' in reflection_html
        assert ">Not now<" in reflection_html

    def test_dismiss_function_exists(self, reflection_html):
        """Should have dismiss function."""
        assert "function dismiss(summary)" in reflection_html

    def test_dismiss_removes_element(self, reflection_html):
        """Dismiss should remove the element."""
        assert "summary.remove()" in reflection_html

    def test_dismiss_fires_event(self, reflection_html):
        """Dismiss should fire event."""
        assert "reflection-dismissed" in reflection_html


class TestReflectionActions:
    """Tests for action buttons."""

    def test_has_acknowledge_action(self, soup):
        """Should have acknowledge action button."""
        template = soup.find("template", id="reflection-summary-template")
        acknowledge = template.find(attrs={"data-action": "acknowledge"})
        assert acknowledge is not None

    def test_has_discuss_action(self, soup):
        """Should have discuss action button."""
        template = soup.find("template", id="reflection-summary-template")
        discuss = template.find(attrs={"data-action": "discuss"})
        assert discuss is not None

    def test_acknowledge_text(self, reflection_html):
        """Acknowledge button should have appropriate text."""
        # Check the HTML contains appropriate text for acknowledge action
        assert 'data-action="acknowledge"' in reflection_html
        assert "keep these in mind" in reflection_html.lower()


class TestReflectionAccessibility:
    """Tests for accessibility."""

    def test_summary_has_region_role(self, soup):
        """Summary should have region role."""
        template = soup.find("template", id="reflection-summary-template")
        summary = template.find("div", class_="reflection-summary")
        assert summary.get("role") == "region"

    def test_summary_has_aria_label(self, soup):
        """Summary should have aria-label."""
        template = soup.find("template", id="reflection-summary-template")
        summary = template.find("div", class_="reflection-summary")
        assert summary.has_attr("aria-label")

    def test_dismiss_has_aria_label(self, soup):
        """Dismiss button should have aria-label."""
        template = soup.find("template", id="reflection-summary-template")
        dismiss = template.find(class_="reflection-dismiss")
        assert dismiss.has_attr("aria-label")

    def test_insights_list_has_role(self, soup):
        """Insights container should have list role."""
        template = soup.find("template", id="reflection-summary-template")
        insights = template.find(class_="reflection-insights")
        assert insights.get("role") == "list"

    def test_has_aria_live_region(self, soup):
        """Should have ARIA live region for announcements."""
        template = soup.find("template", id="reflection-summary-template")
        announcement = template.find(attrs={"aria-live": "polite"})
        assert announcement is not None


class TestReflectionJavaScript:
    """Tests for JavaScript API."""

    def test_reflection_summary_namespace(self, reflection_html):
        """Should create ReflectionSummary namespace."""
        assert "window.ReflectionSummary" in reflection_html

    def test_create_function_exposed(self, reflection_html):
        """Should expose create function."""
        assert "create: create" in reflection_html

    def test_dismiss_function_exposed(self, reflection_html):
        """Should expose dismiss function."""
        assert "dismiss: dismiss" in reflection_html

    def test_init_function_exposed(self, reflection_html):
        """Should expose init function."""
        assert "init: init" in reflection_html

    def test_openers_exposed(self, reflection_html):
        """Should expose OPENERS constant."""
        assert "OPENERS: REFLECTION_OPENERS" in reflection_html


class TestReflectionNoSurveillanceLanguage:
    """Tests to ensure no surveillance language (D3 compliance)."""

    def test_no_monitoring_word(self, reflection_html):
        """Should not contain 'monitoring'."""
        # D3: Never use "I've been monitoring..."
        html_lower = reflection_html.lower()
        # Exclude comments from check
        js_section = reflection_html.split("<script>")[1].split("</script>")[0]
        assert "monitoring" not in js_section.lower()

    def test_no_observed_word(self, reflection_html):
        """Should not contain 'observed' in user-facing text."""
        # D3: Never use "Based on my observations..."
        js_section = reflection_html.split("<script>")[1].split("</script>")[0]
        # Check only in string literals (between quotes)
        assert '"observed' not in js_section.lower()
        assert "'observed" not in js_section.lower()

    def test_no_tracking_word(self, reflection_html):
        """Should not contain 'tracking' in user-facing text."""
        # D3: Never use "I've been tracking..."
        js_section = reflection_html.split("<script>")[1].split("</script>")[0]
        assert '"tracking' not in js_section.lower()
        assert "'tracking" not in js_section.lower()

    def test_no_detected_word(self, reflection_html):
        """Should not contain 'detected' in user-facing text."""
        # D3: Never use "I detected a pattern..."
        js_section = reflection_html.split("<script>")[1].split("</script>")[0]
        assert '"detected' not in js_section.lower()
        assert "'detected" not in js_section.lower()


class TestReflectionStyling:
    """Tests for component styling."""

    def test_warm_color_scheme(self, reflection_html):
        """Should use warm colors for reflection theme."""
        # Reflection should feel warm and contemplative
        assert "#fefdf5" in reflection_html or "#fdf6e3" in reflection_html  # Background
        assert "#d4a373" in reflection_html  # Accent color

    def test_border_left_accent(self, reflection_html):
        """Should have left border accent."""
        assert "border-left:" in reflection_html
