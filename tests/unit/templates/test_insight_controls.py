"""
Unit tests for Insight Controls Component (#424 MUX-IMPLEMENT-COMPOST)

Tests the insight_controls.html component for:
- Correction flow (D2)
- Deletion flow (D2)
- Reset flow (D2)
- No guilt language
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def controls_html():
    """Load the insight controls component HTML."""
    component_path = Path("templates/components/insight_controls.html")
    return component_path.read_text()


@pytest.fixture
def soup(controls_html):
    """Parse the component HTML."""
    return BeautifulSoup(controls_html, "html.parser")


class TestInsightControlsTemplates:
    """Tests for template structure."""

    def test_correction_template_exists(self, soup):
        """Correction dialog template should exist."""
        template = soup.find("template", id="correction-dialog-template")
        assert template is not None

    def test_delete_template_exists(self, soup):
        """Delete dialog template should exist."""
        template = soup.find("template", id="delete-dialog-template")
        assert template is not None

    def test_reset_template_exists(self, soup):
        """Reset dialog template should exist."""
        template = soup.find("template", id="reset-dialog-template")
        assert template is not None


class TestCorrectionFlow:
    """Tests for correction flow (D2)."""

    def test_correction_shows_before(self, soup):
        """Correction should show 'before' value."""
        template = soup.find("template", id="correction-dialog-template")
        before = template.find(class_="correction-value")
        assert before is not None
        assert "before" in before.get("class", [])

    def test_correction_has_input(self, soup):
        """Correction should have input for new value."""
        template = soup.find("template", id="correction-dialog-template")
        input_el = template.find(class_="correction-input")
        assert input_el is not None

    def test_correction_has_cancel(self, soup):
        """Correction should have cancel button."""
        template = soup.find("template", id="correction-dialog-template")
        cancel = template.find(class_="cancel")
        assert cancel is not None

    def test_correction_has_submit(self, soup):
        """Correction should have submit button."""
        template = soup.find("template", id="correction-dialog-template")
        submit = template.find(class_="submit")
        assert submit is not None

    def test_correction_response_d2(self, controls_html):
        """Correction response should match D2 spec."""
        # D2: "Thanks, I'll remember that"
        assert "I'll remember that" in controls_html


class TestDeletionFlow:
    """Tests for deletion flow (D2)."""

    def test_delete_has_warning(self, soup):
        """Delete should have warning element."""
        template = soup.find("template", id="delete-dialog-template")
        warning = template.find(class_="delete-warning")
        assert warning is not None

    def test_delete_is_permanent(self, controls_html):
        """Delete should clearly state it's permanent."""
        # D2: "This deletion is permanent"
        assert "permanent" in controls_html.lower()

    def test_delete_cannot_recover(self, controls_html):
        """Delete should state it cannot be recovered."""
        assert "cannot recover" in controls_html.lower() or "can't undo" in controls_html.lower()

    def test_delete_shows_preview(self, soup):
        """Delete should show what will be deleted."""
        template = soup.find("template", id="delete-dialog-template")
        preview = template.find(class_="delete-insight-preview")
        assert preview is not None

    def test_delete_response_d2(self, controls_html):
        """Delete response should match D2 spec."""
        # D2: "Got it, that's gone"
        assert "that's gone" in controls_html.lower()


class TestResetFlow:
    """Tests for reset flow (D2)."""

    def test_reset_shows_what_deleted(self, soup):
        """Reset should show what will be deleted."""
        template = soup.find("template", id="reset-dialog-template")
        reset_list = template.find(class_="reset-list")
        assert reset_list is not None

    def test_reset_requires_typing(self, controls_html):
        """Reset should require typing 'RESET'."""
        # D2: 'Type "RESET" to confirm'
        assert "RESET" in controls_html
        assert "Type" in controls_html

    def test_reset_input_exists(self, soup):
        """Reset should have confirmation input."""
        template = soup.find("template", id="reset-dialog-template")
        input_el = template.find(class_="reset-confirm-input")
        assert input_el is not None

    def test_reset_button_initially_disabled(self, soup):
        """Reset submit button should be initially disabled."""
        template = soup.find("template", id="reset-dialog-template")
        submit = template.find(class_="submit")
        assert submit.has_attr("disabled")

    def test_reset_response_d2(self, controls_html):
        """Reset response should match D2 spec."""
        # D2: "Starting fresh"
        assert "Starting fresh" in controls_html

    def test_reset_lists_items(self, controls_html):
        """Reset should list what will be deleted."""
        assert "learned preferences" in controls_html.lower()
        assert "pattern observations" in controls_html.lower()


class TestDialogAccessibility:
    """Tests for dialog accessibility."""

    def test_correction_has_dialog_role(self, soup):
        """Correction dialog should have dialog role."""
        template = soup.find("template", id="correction-dialog-template")
        dialog = template.find(class_="insight-control-dialog")
        assert dialog.get("role") == "dialog"

    def test_delete_has_alertdialog_role(self, soup):
        """Delete dialog should have alertdialog role."""
        template = soup.find("template", id="delete-dialog-template")
        dialog = template.find(class_="insight-control-dialog")
        assert dialog.get("role") == "alertdialog"

    def test_reset_has_alertdialog_role(self, soup):
        """Reset dialog should have alertdialog role."""
        template = soup.find("template", id="reset-dialog-template")
        dialog = template.find(class_="insight-control-dialog")
        assert dialog.get("role") == "alertdialog"

    def test_dialogs_have_aria_modal(self, soup):
        """All dialogs should have aria-modal."""
        templates = [
            "correction-dialog-template",
            "delete-dialog-template",
            "reset-dialog-template",
        ]
        for template_id in templates:
            template = soup.find("template", id=template_id)
            dialog = template.find(class_="insight-control-dialog")
            assert dialog.get("aria-modal") == "true", f"{template_id} missing aria-modal"

    def test_dialogs_have_aria_labelledby(self, soup):
        """All dialogs should have aria-labelledby."""
        templates = [
            "correction-dialog-template",
            "delete-dialog-template",
            "reset-dialog-template",
        ]
        for template_id in templates:
            template = soup.find("template", id=template_id)
            dialog = template.find(class_="insight-control-dialog")
            assert dialog.has_attr("aria-labelledby"), f"{template_id} missing aria-labelledby"


class TestControlsJavaScript:
    """Tests for JavaScript API."""

    def test_insight_controls_namespace(self, controls_html):
        """Should create InsightControls namespace."""
        assert "window.InsightControls" in controls_html

    def test_open_correction_exposed(self, controls_html):
        """Should expose openCorrection function."""
        assert "openCorrection: openCorrection" in controls_html

    def test_open_delete_exposed(self, controls_html):
        """Should expose openDelete function."""
        assert "openDelete: openDelete" in controls_html

    def test_open_reset_exposed(self, controls_html):
        """Should expose openReset function."""
        assert "openReset: openReset" in controls_html

    def test_responses_exposed(self, controls_html):
        """Should expose RESPONSES constant."""
        assert "RESPONSES: RESPONSES" in controls_html

    def test_escape_closes_dialog(self, controls_html):
        """Dialogs should close on Escape key."""
        assert "Escape" in controls_html


class TestNoGuiltLanguage:
    """Tests to ensure no guilt language (D2)."""

    def test_no_are_you_sure(self, controls_html):
        """Should not use 'Are you sure?' phrasing."""
        # We have "?" in titles which is OK, but not "are you sure"
        assert "are you sure" not in controls_html.lower()

    def test_no_arguing(self, controls_html):
        """Should not argue with user decisions."""
        # D2: "Piper never argues with corrections"
        assert "but my data" not in controls_html.lower()
        assert "that contradicts" not in controls_html.lower()
        assert "my analysis shows" not in controls_html.lower()

    def test_no_guilt_on_delete(self, controls_html):
        """Delete flow should not guilt user."""
        # D2: "No Guilt: Don't make user feel bad for deleting"
        assert "you should" not in controls_html.lower()
        assert "you didn't" not in controls_html.lower()

    def test_no_secret_backup(self, controls_html):
        """Should not mention keeping backup."""
        # D2: "No Guilt: ... not secretly retain"
        assert "keep a backup" not in controls_html.lower()
        assert "archive" not in controls_html.lower() or "All project" in controls_html

    def test_cancel_not_judgmental(self, controls_html):
        """Cancel button text should be neutral."""
        # D2: Neutral acknowledgment only
        # Check that cancel buttons use neutral language
        assert "Keep it" in controls_html or "Cancel" in controls_html
        assert "Keep my learnings" in controls_html


class TestD2ResponsePatterns:
    """Tests for D2 response patterns."""

    def test_correction_response(self, controls_html):
        """Correction: 'Thanks, I'll remember that'."""
        assert "Thanks, I'll remember that" in controls_html

    def test_deletion_response(self, controls_html):
        """Deletion: 'Got it, that's gone'."""
        assert "Got it, that's gone" in controls_html

    def test_reset_response(self, controls_html):
        """Reset: 'Starting fresh'."""
        assert "Starting fresh" in controls_html

    def test_confirm_response(self, controls_html):
        """Confirm: 'Thanks for confirming!'."""
        assert "Thanks for confirming" in controls_html
