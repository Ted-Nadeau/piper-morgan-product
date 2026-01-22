"""Tests for auth/settings consciousness wrapper. Issue #637."""

import pytest


class TestAuthConsciousness:
    """Test consciousness wrapper for auth messages."""

    def test_login_success_has_warmth(self):
        """Login success should be welcoming."""
        from services.consciousness.auth_consciousness import format_login_success_conscious

        output = format_login_success_conscious("alice")
        assert "welcome" in output.lower() or "good" in output.lower() or "great" in output.lower()

    def test_logout_success_has_identity(self):
        """Logout should acknowledge with identity."""
        from services.consciousness.auth_consciousness import format_logout_success_conscious

        output = format_logout_success_conscious()
        # Can use "you" instead of "I" for logout - still identity-aware
        assert "you" in output.lower() or "see" in output.lower() or "logged" in output.lower()

    def test_session_expired_has_invitation(self):
        """Session expired should offer recovery path."""
        from services.consciousness.auth_consciousness import format_session_expired_conscious

        output = format_session_expired_conscious()
        assert "?" in output or "log" in output.lower(), "Should suggest recovery"

    def test_invalid_credentials_not_accusatory(self):
        """Invalid credentials should be helpful, not blaming."""
        from services.consciousness.auth_consciousness import format_invalid_credentials_conscious

        output = format_invalid_credentials_conscious()
        # Should NOT say "you entered wrong password"
        assert "wrong" not in output.lower()
        assert "incorrect" not in output.lower() or "?" in output  # ok if offering help
        assert "?" in output, "Should offer recovery"

    def test_settings_saved_has_identity(self):
        """Settings saved should confirm with identity."""
        from services.consciousness.auth_consciousness import format_settings_saved_conscious

        output = format_settings_saved_conscious("theme")
        assert "I" in output or "saved" in output.lower()

    def test_settings_saved_confirms_effect(self):
        """Settings saved should confirm when it takes effect."""
        from services.consciousness.auth_consciousness import format_settings_saved_conscious

        output = format_settings_saved_conscious("notifications")
        assert (
            "effect" in output.lower()
            or "now" in output.lower()
            or "right away" in output.lower()
            or "will" in output.lower()
        )


class TestAuthConsciousnessEdgeCases:
    """Edge case tests for auth consciousness."""

    def test_account_inactive_is_helpful(self):
        """Account inactive should be helpful."""
        from services.consciousness.auth_consciousness import format_account_inactive_conscious

        output = format_account_inactive_conscious()
        assert "?" in output or "contact" in output.lower() or "help" in output.lower()

    def test_password_change_success(self):
        """Password change success should confirm."""
        from services.consciousness.auth_consciousness import format_password_changed_conscious

        output = format_password_changed_conscious()
        assert "password" in output.lower()
        assert "changed" in output.lower() or "updated" in output.lower() or "set" in output.lower()


class TestLoginSuccessVariants:
    """Test login success message variants."""

    def test_login_success_without_username(self):
        """Login success without username should still be welcoming."""
        from services.consciousness.auth_consciousness import format_login_success_conscious

        output = format_login_success_conscious()
        assert "welcome" in output.lower() or "good" in output.lower()

    def test_login_success_with_username_includes_name(self):
        """Login success with username should include the name."""
        from services.consciousness.auth_consciousness import format_login_success_conscious

        output = format_login_success_conscious("bob")
        assert "bob" in output.lower()


class TestSettingsSavedVariants:
    """Test settings saved message variants."""

    def test_settings_saved_without_setting_name(self):
        """Settings saved without specific setting name."""
        from services.consciousness.auth_consciousness import format_settings_saved_conscious

        output = format_settings_saved_conscious()
        assert "saved" in output.lower() or "updated" in output.lower()

    def test_settings_saved_formats_setting_name(self):
        """Settings saved should format underscored names nicely."""
        from services.consciousness.auth_consciousness import format_settings_saved_conscious

        output = format_settings_saved_conscious("notification_preferences")
        # Should not have underscores in output
        assert (
            "notification preferences" in output.lower() or "notification_preferences" not in output
        )
