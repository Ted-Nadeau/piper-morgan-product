"""Tests for Piper intro panel in setup wizard (#547).

Tests verify that the setup.html template contains the required
Piper introduction panel elements per Issue #547 FTUX requirements.
"""

from pathlib import Path

import pytest


class TestSetupIntroPanel:
    """Test setup intro panel is present in template with required elements."""

    @pytest.fixture
    def setup_template_content(self) -> str:
        """Load setup.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "setup.html"
        return template_path.read_text()

    def test_setup_intro_panel_renders(self, setup_template_content):
        """Verify intro panel HTML is present in setup template."""
        assert "piper-intro" in setup_template_content
        assert "Hi, I'm Piper Morgan" in setup_template_content
        assert "Let's get started" in setup_template_content

    def test_setup_intro_has_required_elements(self, setup_template_content):
        """Verify all required intro elements exist."""
        assert "piper-intro-cta" in setup_template_content  # CTA button
        assert "dismissPiperIntro" in setup_template_content  # JS function
        assert 'role="region"' in setup_template_content  # Accessibility
