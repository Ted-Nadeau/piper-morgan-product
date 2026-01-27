"""
Unit tests for Privacy Mode Component (#425 MUX-IMPLEMENT-MEMORY-SYNC)

Tests the privacy_mode.html component for:
- Start private session dialog
- Privacy mode banner
- Mark as private dialog
- Clear communication about privacy
- D2 compliance (honest, no theater)
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def privacy_html():
    """Load the privacy mode component HTML."""
    component_path = Path("templates/components/privacy_mode.html")
    return component_path.read_text()


@pytest.fixture
def soup(privacy_html):
    """Parse the component HTML."""
    return BeautifulSoup(privacy_html, "html.parser")


class TestPrivacyBannerTemplate:
    """Tests for privacy mode banner."""

    def test_banner_template_exists(self, soup):
        """Banner template should exist."""
        template = soup.find("template", id="privacy-banner-template")
        assert template is not None

    def test_has_banner_element(self, soup):
        """Template should have banner element."""
        template = soup.find("template", id="privacy-banner-template")
        banner = template.find(class_="privacy-mode-banner")
        assert banner is not None

    def test_banner_has_status_role(self, soup):
        """Banner should have status role for accessibility."""
        template = soup.find("template", id="privacy-banner-template")
        banner = template.find(class_="privacy-mode-banner")
        assert banner.get("role") == "status"

    def test_banner_has_aria_live(self, soup):
        """Banner should have aria-live for screen readers."""
        template = soup.find("template", id="privacy-banner-template")
        banner = template.find(class_="privacy-mode-banner")
        assert banner.get("aria-live") == "polite"

    def test_has_lock_icon(self, soup):
        """Banner should have lock icon."""
        template = soup.find("template", id="privacy-banner-template")
        icon = template.find(class_="privacy-mode-icon")
        assert icon is not None

    def test_has_info_text(self, soup):
        """Banner should have info text."""
        template = soup.find("template", id="privacy-banner-template")
        text = template.find(class_="privacy-mode-text")
        assert text is not None

    def test_has_end_button(self, soup):
        """Banner should have end session button."""
        template = soup.find("template", id="privacy-banner-template")
        btn = template.find(class_="privacy-mode-end-btn")
        assert btn is not None

    def test_banner_hidden_by_default(self, soup):
        """Banner should be hidden by default."""
        template = soup.find("template", id="privacy-banner-template")
        banner = template.find(class_="privacy-mode-banner")
        assert "hidden" in banner.get("class", [])


class TestPrivacyStartDialog:
    """Tests for start private session dialog."""

    def test_start_dialog_template_exists(self, soup):
        """Start dialog template should exist."""
        template = soup.find("template", id="privacy-start-dialog-template")
        assert template is not None

    def test_has_dialog_element(self, soup):
        """Template should have dialog element."""
        template = soup.find("template", id="privacy-start-dialog-template")
        dialog = template.find(class_="privacy-start-dialog")
        assert dialog is not None

    def test_dialog_has_role(self, soup):
        """Dialog should have dialog role."""
        template = soup.find("template", id="privacy-start-dialog-template")
        dialog = template.find(class_="privacy-start-dialog")
        assert dialog.get("role") == "dialog"

    def test_dialog_has_aria_modal(self, soup):
        """Dialog should have aria-modal."""
        template = soup.find("template", id="privacy-start-dialog-template")
        dialog = template.find(class_="privacy-start-dialog")
        assert dialog.get("aria-modal") == "true"

    def test_has_title(self, privacy_html):
        """Dialog should have title."""
        assert "Start private session?" in privacy_html

    def test_has_icon(self, soup):
        """Dialog should have icon."""
        template = soup.find("template", id="privacy-start-dialog-template")
        icon = template.find(class_="privacy-dialog-icon")
        assert icon is not None

    def test_has_description(self, soup):
        """Dialog should have description."""
        template = soup.find("template", id="privacy-start-dialog-template")
        desc = template.find(class_="privacy-dialog-description")
        assert desc is not None

    def test_has_what_means_section(self, soup):
        """Dialog should have 'what this means' section."""
        template = soup.find("template", id="privacy-start-dialog-template")
        section = template.find(class_="privacy-what-means")
        assert section is not None

    def test_has_cancel_button(self, soup):
        """Dialog should have cancel button."""
        template = soup.find("template", id="privacy-start-dialog-template")
        cancel = template.find(class_="cancel")
        assert cancel is not None

    def test_has_confirm_button(self, soup):
        """Dialog should have confirm button."""
        template = soup.find("template", id="privacy-start-dialog-template")
        confirm = template.find(class_="confirm")
        assert confirm is not None


class TestPrivacyMarkDialog:
    """Tests for mark as private dialog."""

    def test_mark_dialog_template_exists(self, soup):
        """Mark dialog template should exist."""
        template = soup.find("template", id="privacy-mark-dialog-template")
        assert template is not None

    def test_has_alertdialog_role(self, soup):
        """Mark dialog should have alertdialog role."""
        template = soup.find("template", id="privacy-mark-dialog-template")
        dialog = template.find(class_="privacy-mark-dialog")
        assert dialog.get("role") == "alertdialog"

    def test_has_preview_element(self, soup):
        """Mark dialog should have preview element."""
        template = soup.find("template", id="privacy-mark-dialog-template")
        preview = template.find(class_="privacy-mark-preview")
        assert preview is not None

    def test_has_mark_title(self, privacy_html):
        """Mark dialog should have title."""
        assert "Mark as private?" in privacy_html


class TestPrivacyToggle:
    """Tests for quick toggle button."""

    def test_toggle_template_exists(self, soup):
        """Toggle template should exist."""
        template = soup.find("template", id="privacy-toggle-template")
        assert template is not None

    def test_has_toggle_button(self, soup):
        """Template should have toggle button."""
        template = soup.find("template", id="privacy-toggle-template")
        toggle = template.find(class_="privacy-quick-toggle")
        assert toggle is not None

    def test_toggle_has_aria_pressed(self, soup):
        """Toggle should have aria-pressed."""
        template = soup.find("template", id="privacy-toggle-template")
        toggle = template.find(class_="privacy-quick-toggle")
        assert toggle.has_attr("aria-pressed")

    def test_toggle_has_icon(self, soup):
        """Toggle should have icon."""
        template = soup.find("template", id="privacy-toggle-template")
        icon = template.find(class_="privacy-toggle-icon")
        assert icon is not None

    def test_toggle_has_label(self, soup):
        """Toggle should have label."""
        template = soup.find("template", id="privacy-toggle-template")
        label = template.find(class_="privacy-toggle-label")
        assert label is not None


class TestHonestPrivacyCommunication:
    """Tests for honest privacy communication (D2 principle)."""

    def test_explains_no_history(self, privacy_html):
        """Should explain conversation won't appear in history."""
        assert "won't appear in your history" in privacy_html.lower()

    def test_explains_no_learning(self, privacy_html):
        """Should explain Piper won't learn from it."""
        assert "won't learn" in privacy_html.lower()

    def test_explains_no_context_forward(self, privacy_html):
        """Should explain no context carries forward."""
        assert "No context will carry forward" in privacy_html

    def test_banner_says_wont_be_remembered(self, privacy_html):
        """Banner should say conversation won't be remembered."""
        assert "won't be remembered" in privacy_html.lower()


class TestNoPrivacyTheater:
    """Tests to ensure no 'privacy theater' (false privacy claims)."""

    def test_no_lie_about_encryption(self, privacy_html):
        """Should not falsely claim encryption."""
        # We don't claim end-to-end encryption or similar
        # If we did, we'd need to actually implement it
        # This test just ensures we don't make false claims
        assert "encrypted" not in privacy_html.lower() or "not encrypted" in privacy_html.lower()

    def test_clear_about_what_private_means(self, privacy_html):
        """Should have 'what this means' explanation."""
        assert "What this means" in privacy_html


class TestJavaScriptAPI:
    """Tests for JavaScript API."""

    def test_privacy_mode_namespace(self, privacy_html):
        """Should create PrivacyMode namespace."""
        assert "window.PrivacyMode" in privacy_html

    def test_start_private_session_exposed(self, privacy_html):
        """Should expose startPrivateSession function."""
        assert "startPrivateSession: startPrivateSession" in privacy_html

    def test_end_private_session_exposed(self, privacy_html):
        """Should expose endPrivateSession function."""
        assert "endPrivateSession: endPrivateSession" in privacy_html

    def test_mark_as_private_exposed(self, privacy_html):
        """Should expose markAsPrivate function."""
        assert "markAsPrivate: markAsPrivate" in privacy_html

    def test_set_privacy_state_exposed(self, privacy_html):
        """Should expose setPrivacyState function."""
        assert "setPrivacyState: setPrivacyState" in privacy_html

    def test_get_privacy_state_exposed(self, privacy_html):
        """Should expose getPrivacyState function."""
        assert "getPrivacyState: getPrivacyState" in privacy_html

    def test_mount_banner_exposed(self, privacy_html):
        """Should expose mountBanner function."""
        assert "mountBanner: mountBanner" in privacy_html

    def test_create_quick_toggle_exposed(self, privacy_html):
        """Should expose createQuickToggle function."""
        assert "createQuickToggle: createQuickToggle" in privacy_html

    def test_loaded_flag(self, privacy_html):
        """Should set loaded flag."""
        assert "privacyModeLoaded = true" in privacy_html


class TestPrivacyStateEvent:
    """Tests for privacy state change event."""

    def test_dispatches_event(self, privacy_html):
        """Should dispatch privacyStateChange event."""
        assert "privacyStateChange" in privacy_html

    def test_event_includes_state(self, privacy_html):
        """Event should include isPrivate state."""
        assert "isPrivate: isPrivate" in privacy_html


class TestEscapeKeyClosing:
    """Tests for Escape key closing."""

    def test_escape_closes_dialog(self, privacy_html):
        """Should close on Escape key."""
        assert "Escape" in privacy_html


class TestStyling:
    """Tests for CSS styling."""

    def test_hidden_class(self, privacy_html):
        """Should have hidden class for banner."""
        assert ".privacy-mode-banner.hidden" in privacy_html

    def test_open_class(self, privacy_html):
        """Should have open class for dialog."""
        assert ".privacy-start-dialog.open" in privacy_html

    def test_active_toggle_class(self, privacy_html):
        """Should have active class for toggle."""
        assert ".privacy-quick-toggle.active" in privacy_html

    def test_red_theme_for_privacy(self, privacy_html):
        """Privacy elements should use red theme (for visibility)."""
        assert "#fef2f2" in privacy_html  # Light red background
        assert "#991b1b" in privacy_html  # Dark red text
