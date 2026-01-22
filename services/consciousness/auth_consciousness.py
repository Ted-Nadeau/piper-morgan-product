"""
Consciousness Wrapper for Authentication and Settings

Transforms auth/settings messages into warm, helpful expression.
Issue: #637 CONSCIOUSNESS-TRANSFORM: Settings/Auth
ADR: ADR-056 Consciousness Expression Patterns

These transformations apply the MVC (Me-Voice-Curiosity) principles:
- Me: Identity presence ("I've", "I'll")
- Voice: Warm, conversational tone
- Curiosity: Offer next steps, invite dialogue
"""

from typing import Optional


def format_login_success_conscious(username: Optional[str] = None) -> str:
    """
    Format login success with warmth.

    Transforms from:
        "Login successful"

    To:
        "Welcome back, alice! You're all set."

    Args:
        username: Optional username to personalize the greeting

    Returns:
        Warm welcome message with identity presence
    """
    if username:
        return f"Welcome back, {username}! You're all set."
    return "Welcome back! You're all set."


def format_logout_success_conscious() -> str:
    """
    Format logout success with acknowledgment.

    Transforms from:
        "Logged out successfully"

    To:
        "You're logged out. See you next time!"

    Returns:
        Friendly farewell with acknowledgment
    """
    return "You're logged out. See you next time!"


def format_session_expired_conscious() -> str:
    """
    Format session expired with recovery path.

    Transforms from:
        "Session expired"

    To:
        "Your session timed out - mind logging in again?
         I'll pick up where we left off."

    Returns:
        Helpful message with recovery invitation
    """
    return "Your session timed out - mind logging in again? " "I'll pick up where we left off."


def format_invalid_credentials_conscious() -> str:
    """
    Format invalid credentials helpfully, not accusingly.

    Transforms from:
        "Invalid username or password"

    To:
        "Hmm, those credentials didn't work.
         Want to try again, or need help resetting your password?"

    Security Note: This is for display purposes only. API error details
    should remain generic to prevent user enumeration attacks.

    Returns:
        Helpful message without blame, offering recovery paths
    """
    return (
        "Hmm, those credentials didn't work. "
        "Want to try again, or need help resetting your password?"
    )


def format_settings_saved_conscious(setting_name: Optional[str] = None) -> str:
    """
    Format settings saved confirmation.

    Transforms from:
        "Settings updated"

    To:
        "I've saved your theme settings. They'll take effect right away."

    Args:
        setting_name: Optional setting name to include (underscores replaced with spaces)

    Returns:
        Confirmation with identity presence and effect timing
    """
    if setting_name:
        # Replace underscores with spaces for readable names
        readable = setting_name.replace("_", " ")
        return f"I've saved your {readable} settings. They'll take effect right away."
    return "I've saved your settings. They'll take effect right away."


def format_account_inactive_conscious() -> str:
    """
    Format account inactive message helpfully.

    Transforms from:
        "Account is inactive. Please contact administrator."

    To:
        "Your account isn't active right now.
         Need help getting access? Contact the administrator."

    Returns:
        Helpful message with clear recovery path
    """
    return (
        "Your account isn't active right now. "
        "Need help getting access? Contact the administrator."
    )


def format_password_changed_conscious() -> str:
    """
    Format password change success.

    Transforms from:
        "Password changed successfully. Please log in with your new password."

    To:
        "Your password has been updated. You're all set!"

    Returns:
        Confirmation with positive closure
    """
    return "Your password has been updated. You're all set!"
