"""Tests for post-setup orientation modal (#549).

Tests verify that orientation modal HTML, CSS, and JS are present in home.html
to support the post-setup orientation flow per Issue #549 FTUX requirements.
"""

from pathlib import Path

import pytest


class TestOrientationModal:
    """Verify orientation modal rendering and behavior."""

    @pytest.fixture
    def home_template_content(self) -> str:
        """Load home.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "home.html"
        return template_path.read_text()

    def test_orientation_modal_renders(self, home_template_content):
        """Verify orientation modal HTML is present in home template."""
        assert "orientation-modal" in home_template_content
        assert "You're all set!" in home_template_content
        assert "orientation-suggestions" in home_template_content

    def test_orientation_has_required_elements(self, home_template_content):
        """Verify all required orientation elements exist."""
        # Check suggestion elements
        assert "suggestion-github" in home_template_content
        assert "suggestion-calendar" in home_template_content
        # Check JavaScript function
        assert "dismissOrientation" in home_template_content
        # Check accessibility attributes
        assert 'role="dialog"' in home_template_content
        assert 'aria-modal="true"' in home_template_content
        assert 'aria-labelledby="orientation-title"' in home_template_content

    def test_orientation_conditional_suggestions(self, home_template_content):
        """Verify suggestions are conditional on integration status."""
        # GitHub and Calendar suggestions should exist (hidden by default)
        assert "suggestion-github" in home_template_content
        assert "suggestion-calendar" in home_template_content
        # Always-available todo suggestion should be visible
        assert "Add a todo" in home_template_content
        # Check that conditional suggestions are hidden by default
        assert (
            'id="suggestion-github" class="orientation-suggestion hidden"' in home_template_content
        )
        assert (
            'id="suggestion-calendar" class="orientation-suggestion hidden"'
            in home_template_content
        )


class TestOrientationKeyboardAccessibility:
    """Verify keyboard accessibility for orientation modal."""

    @pytest.fixture
    def home_template_content(self) -> str:
        """Load home.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "home.html"
        return template_path.read_text()

    def test_escape_key_handler_exists(self, home_template_content):
        """Escape key closes orientation modal."""
        assert "Escape" in home_template_content
        assert "e.key === 'Escape'" in home_template_content


class TestOrientationIntegrationEndpoint:
    """Verify integration health endpoint usage."""

    @pytest.fixture
    def home_template_content(self) -> str:
        """Load home.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "home.html"
        return template_path.read_text()

    def test_uses_correct_integration_endpoint(self, home_template_content):
        """Uses /api/v1/integrations/health endpoint (not /status)."""
        assert "/api/v1/integrations/health" in home_template_content
        # Should NOT use incorrect /status endpoint
        assert "/api/v1/integrations/status" not in home_template_content
