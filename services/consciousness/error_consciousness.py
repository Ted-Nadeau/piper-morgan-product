"""
Consciousness Wrapper for Error Messages

Enhances error messages with consciousness expression patterns.
Part of Consciousness Rollout Wave 1 (#631)

Issue: #631 CONSCIOUSNESS-TRANSFORM: Error Messages
Framework: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

from enum import Enum
from typing import Dict, Optional

from services.consciousness.validation import validate_mvc


class ErrorSeverity(str, Enum):
    """Error severity levels for appropriate user messaging."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


def format_error_conscious(
    message: str,
    recovery: str,
    severity: str,
    context: Optional[str] = None,
) -> str:
    """
    Format an error message with consciousness.

    Transforms from:
        "Hmm, i can't connect to the database right now. I'll keep trying to reconnect."

    To:
        "I ran into something while connecting: I can't reach the database right now.
         Let me keep trying to reconnect. Does that work, or would you like to try
         something else?"

    Args:
        message: The error message
        recovery: Recovery suggestion
        severity: Error severity level
        context: Optional context of what was being done

    Returns:
        Conscious error message
    """
    sections = []

    # Build opening with identity + context
    if context:
        sections.append(f"I ran into something while {context.lower()}:")
    else:
        sections.append("I ran into something:")

    # Add the error explanation with epistemic humility
    explanation = _add_humility(message)
    sections.append(explanation)

    # Add recovery with dialogue invitation
    recovery_with_dialogue = _add_dialogue_invitation(recovery, severity)
    sections.append(recovery_with_dialogue)

    narrative = " ".join(sections)

    # Validate MVC
    mvc_result = validate_mvc(narrative)
    if not mvc_result.passes:
        narrative = _fix_mvc_gaps(narrative, mvc_result)

    return narrative


def format_conversational_error_conscious(
    message: str,
    recovery: str,
    severity: str,
    context: Optional[str] = None,
) -> str:
    """
    Format error for chat/conversational interface with consciousness.

    More concise than full error format, suitable for chat bubbles.

    Args:
        message: The error message
        recovery: Recovery suggestion
        severity: Error severity level
        context: Optional context

    Returns:
        Conversational conscious error message
    """
    # Severity-appropriate opening
    if severity == ErrorSeverity.INFO.value or severity == ErrorSeverity.INFO:
        opening = "Heads up:"
    elif severity == ErrorSeverity.WARNING.value or severity == ErrorSeverity.WARNING:
        opening = "I noticed something:"
    elif severity == ErrorSeverity.CRITICAL.value or severity == ErrorSeverity.CRITICAL:
        opening = "I need to let you know:"
    else:
        opening = "I ran into something:"

    # Context integration
    if context:
        opening = f"{opening} while {context.lower()},"

    # Build message
    explanation = message.lower() if not message[0].isupper() else message
    recovery_short = _shorten_recovery(recovery)

    # Add dialogue invitation based on severity
    if severity in (
        ErrorSeverity.ERROR.value,
        ErrorSeverity.ERROR,
        ErrorSeverity.CRITICAL.value,
        ErrorSeverity.CRITICAL,
    ):
        invitation = " Want me to try again, or should we try something different?"
    else:
        invitation = " Let me know if you need anything else."

    return f"{opening} {explanation} {recovery_short}{invitation}"


def enhance_error_pattern(
    pattern_response: Dict[str, str],
    context: Optional[str] = None,
) -> Dict[str, str]:
    """
    Enhance an existing error pattern response with consciousness.

    Takes the existing error pattern dict and adds consciousness elements.

    Args:
        pattern_response: Dict with 'message', 'recovery', 'severity', 'category'
        context: Optional context

    Returns:
        Enhanced pattern response dict
    """
    enhanced = pattern_response.copy()

    # Ensure message has identity voice
    message = enhanced.get("message", "")
    if not _has_identity(message):
        if message.startswith("I ") or message.startswith("I'"):
            pass  # Already has identity
        elif message.lower().startswith("the "):
            message = "I'm seeing that t" + message[2:]
        else:
            message = "I " + message[0].lower() + message[1:]
        enhanced["message"] = message

    # Ensure recovery has dialogue invitation
    recovery = enhanced.get("recovery", "")
    if not _has_invitation(recovery):
        recovery = recovery.rstrip(".")
        recovery += ". Let me know if that helps or if you'd like to try something else."
        enhanced["recovery"] = recovery

    return enhanced


def _add_humility(message: str) -> str:
    """Add epistemic humility to error message if needed."""
    humility_phrases = ["it looks like", "it seems", "I think", "appears"]

    # Check if already has humility
    message_lower = message.lower()
    for phrase in humility_phrases:
        if phrase in message_lower:
            return message

    # Add appropriate humility
    if message.lower().startswith("i can't"):
        return message.replace("I can't", "It looks like I can't", 1)
    elif message.lower().startswith("i'm having"):
        return message  # Already sounds humble
    elif message.lower().startswith("the "):
        return "It looks like " + message[0].lower() + message[1:]

    return message


def _add_dialogue_invitation(recovery: str, severity: str) -> str:
    """Add dialogue invitation to recovery suggestion."""
    # Check if already has invitation
    invitation_patterns = ["?", "let me know", "would you", "should I"]
    recovery_lower = recovery.lower()
    for pattern in invitation_patterns:
        if pattern in recovery_lower:
            return recovery

    # Add appropriate invitation based on severity
    recovery = recovery.rstrip(".")

    if severity in (
        ErrorSeverity.ERROR.value,
        ErrorSeverity.ERROR,
        ErrorSeverity.CRITICAL.value,
        ErrorSeverity.CRITICAL,
    ):
        return f"{recovery}. Would you like me to try again?"
    elif severity in (ErrorSeverity.WARNING.value, ErrorSeverity.WARNING):
        return f"{recovery}. Does that help?"
    else:
        return f"{recovery}. Let me know if you need anything else."


def _shorten_recovery(recovery: str) -> str:
    """Shorten recovery suggestion for conversational format."""
    # Take first sentence only
    sentences = recovery.split(". ")
    if len(sentences) > 1:
        return sentences[0] + "."
    return recovery


def _has_identity(text: str) -> bool:
    """Check if text has identity voice (I statements)."""
    return "I " in text or "I'" in text or text.startswith("I")


def _has_invitation(text: str) -> bool:
    """Check if text has dialogue invitation."""
    invitation_patterns = ["?", "let me know", "would you", "should I", "want me"]
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in invitation_patterns)


def _fix_mvc_gaps(narrative: str, mvc_result) -> str:
    """Fix any missing MVC requirements."""
    fixed = narrative

    if "identity" in mvc_result.missing:
        if not fixed.startswith("I"):
            fixed = "I ran into something. " + fixed

    if "uncertainty" in mvc_result.missing:
        fixed = fixed.replace("can't", "can't seem to", 1)

    if "invitation" in mvc_result.missing:
        fixed = fixed.rstrip(".") + ". Would you like me to try again?"

    if "attribution" in mvc_result.missing:
        # For errors, attribution is about what we were trying to do
        pass  # Usually covered by context parameter

    return fixed
