"""Tests for UI/template consciousness wrapper. Issue #638."""

import pytest


class TestEmptyStateConsciousness:
    """Test consciousness wrapper for empty states."""

    def test_empty_state_is_inviting(self):
        """Empty states should be inviting, not clinical."""
        from services.consciousness.ui_consciousness import format_empty_state_conscious

        output = format_empty_state_conscious("todos")
        # Should NOT be clinical like "No items found"
        assert "No" not in output or "?" in output
        assert "yet" in output.lower() or "start" in output.lower() or "?" in output

    def test_empty_state_offers_action(self):
        """Empty states should suggest what to do."""
        from services.consciousness.ui_consciousness import format_empty_state_conscious

        output = format_empty_state_conscious("files")
        assert "?" in output or "upload" in output.lower() or "add" in output.lower()

    def test_empty_state_for_different_types(self):
        """Different entity types should have appropriate messages."""
        from services.consciousness.ui_consciousness import format_empty_state_conscious

        todos = format_empty_state_conscious("todos")
        files = format_empty_state_conscious("files")
        projects = format_empty_state_conscious("projects")

        # Each should be distinct and appropriate
        assert todos != files != projects

    def test_empty_state_case_insensitive(self):
        """Entity type should be case insensitive."""
        from services.consciousness.ui_consciousness import format_empty_state_conscious

        lower = format_empty_state_conscious("todos")
        upper = format_empty_state_conscious("TODOS")
        mixed = format_empty_state_conscious("Todos")

        assert lower == upper == mixed

    def test_empty_state_unknown_type_has_default(self):
        """Unknown entity type should use friendly default."""
        from services.consciousness.ui_consciousness import format_empty_state_conscious

        output = format_empty_state_conscious("unknownthing")
        assert "?" in output or "yet" in output.lower()
        assert len(output) > 10  # Not empty


class TestConfirmationConsciousness:
    """Test consciousness wrapper for confirmations."""

    def test_delete_confirmation_is_clear(self):
        """Delete confirmation should be clear but not scary."""
        from services.consciousness.ui_consciousness import format_delete_confirmation_conscious

        output = format_delete_confirmation_conscious("todo", "Buy groceries")
        assert "remove" in output.lower() or "delete" in output.lower()
        assert "?" in output

    def test_delete_confirmation_names_item(self):
        """Delete confirmation should name the item."""
        from services.consciousness.ui_consciousness import format_delete_confirmation_conscious

        output = format_delete_confirmation_conscious("file", "report.pdf")
        assert "report.pdf" in output

    def test_delete_confirmation_without_name(self):
        """Delete confirmation without item name should still work."""
        from services.consciousness.ui_consciousness import format_delete_confirmation_conscious

        output = format_delete_confirmation_conscious("project")
        assert "project" in output.lower()
        assert "?" in output

    def test_delete_confirmation_warns_irreversible(self):
        """Delete confirmation should warn about permanence."""
        from services.consciousness.ui_consciousness import format_delete_confirmation_conscious

        output = format_delete_confirmation_conscious("todo", "Test item")
        assert (
            "undo" in output.lower()
            or "permanent" in output.lower()
            or "can't be" in output.lower()
        )


class TestToastConsciousness:
    """Test consciousness wrapper for toast messages."""

    def test_success_toast_has_identity(self):
        """Success toast should acknowledge warmly."""
        from services.consciousness.ui_consciousness import format_toast_success_conscious

        output = format_toast_success_conscious("saved", "your settings")
        assert "I" in output or "done" in output.lower() or "saved" in output.lower()

    def test_success_toast_confirms_action(self):
        """Success toast should confirm what happened."""
        from services.consciousness.ui_consciousness import format_toast_success_conscious

        output = format_toast_success_conscious("created", "the project")
        assert "created" in output.lower() or "done" in output.lower()

    def test_error_toast_offers_help(self):
        """Error toast should offer recovery."""
        from services.consciousness.ui_consciousness import format_toast_error_conscious

        output = format_toast_error_conscious("save your changes")
        assert "?" in output or "try" in output.lower()

    def test_error_toast_not_blaming(self):
        """Error toast should not blame the user."""
        from services.consciousness.ui_consciousness import format_toast_error_conscious

        output = format_toast_error_conscious("upload the file")
        # Should not say "you failed" or similar
        assert "you failed" not in output.lower()
        assert "your fault" not in output.lower()

    def test_delete_toast_confirms_action(self):
        """Delete toast should confirm the action."""
        from services.consciousness.ui_consciousness import format_toast_delete_conscious

        output = format_toast_delete_conscious("todo")
        assert "removed" in output.lower() or "deleted" in output.lower()

    def test_delete_toast_is_reassuring(self):
        """Delete toast should be reassuring (done, not scary)."""
        from services.consciousness.ui_consciousness import format_toast_delete_conscious

        output = format_toast_delete_conscious("file")
        # Should feel complete, not ominous
        assert (
            "gone" in output.lower() or "removed" in output.lower() or "deleted" in output.lower()
        )


class TestButtonLabelConsciousness:
    """Test consciousness wrapper for button labels."""

    def test_delete_button_is_clear(self):
        """Delete button should be clear."""
        from services.consciousness.ui_consciousness import format_button_label_conscious

        output = format_button_label_conscious("delete")
        assert "remove" in output.lower() or "delete" in output.lower()

    def test_cancel_button_is_casual(self):
        """Cancel button should feel casual."""
        from services.consciousness.ui_consciousness import format_button_label_conscious

        output = format_button_label_conscious("cancel")
        assert "never mind" in output.lower() or "cancel" in output.lower()

    def test_save_button_is_action_oriented(self):
        """Save button should be action-oriented."""
        from services.consciousness.ui_consciousness import format_button_label_conscious

        output = format_button_label_conscious("save")
        assert "save" in output.lower()

    def test_unknown_action_returns_titled(self):
        """Unknown action should return title-cased version."""
        from services.consciousness.ui_consciousness import format_button_label_conscious

        output = format_button_label_conscious("foobar")
        assert output == "Foobar"


class TestEmptyStateTitle:
    """Test consciousness wrapper for empty state titles."""

    def test_empty_state_title_for_todos(self):
        """Empty state title for todos should be inviting."""
        from services.consciousness.ui_consciousness import format_empty_state_title_conscious

        output = format_empty_state_title_conscious("todos")
        assert len(output) > 0
        assert "no" not in output.lower() or "yet" in output.lower()

    def test_empty_state_title_for_files(self):
        """Empty state title for files should be inviting."""
        from services.consciousness.ui_consciousness import format_empty_state_title_conscious

        output = format_empty_state_title_conscious("files")
        assert len(output) > 0


class TestEmptyStateHelpers:
    """Test helper functions for empty state components."""

    def test_get_empty_state_icon(self):
        """Should return appropriate icon for entity type."""
        from services.consciousness.ui_consciousness import get_empty_state_icon

        todos_icon = get_empty_state_icon("todos")
        files_icon = get_empty_state_icon("files")

        assert todos_icon is not None
        assert files_icon is not None
        assert todos_icon != files_icon

    def test_get_empty_state_cta(self):
        """Should return appropriate CTA text for entity type."""
        from services.consciousness.ui_consciousness import get_empty_state_cta

        todos_cta = get_empty_state_cta("todos")
        files_cta = get_empty_state_cta("files")

        assert (
            "add" in todos_cta.lower()
            or "create" in todos_cta.lower()
            or "new" in todos_cta.lower()
        )
        assert "upload" in files_cta.lower() or "add" in files_cta.lower()
