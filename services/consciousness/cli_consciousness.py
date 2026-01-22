"""
Consciousness Wrapper for CLI Output

Transforms CLI messages into conscious narrative expression.
Part of Consciousness Rollout Wave 2 (#633)

Issue: #633 CONSCIOUSNESS-TRANSFORM: CLI Output
Framework: #407 MUX-VISION-STANDUP-EXTRACT
"""

from typing import Optional


def format_startup_conscious() -> str:
    """Format startup message with consciousness."""
    return "Starting up... let me get everything ready."


def format_ready_conscious(url: str) -> str:
    """Format ready message with consciousness."""
    return f"I'm up and running! You can find me at {url}"


def format_shutdown_conscious() -> str:
    """Format shutdown message with consciousness."""
    return "Shutting down now. See you next time!"


def format_cli_success_conscious(action: str, detail: str) -> str:
    """Format success confirmation with consciousness."""
    return f"I've {action} {detail}."


def format_cli_error_conscious(error: str) -> str:
    """Format error message with consciousness and invitation."""
    return f"I ran into a problem: {error}. Want me to try again, or can I help troubleshoot?"


def format_cli_progress_conscious(task: str, current: int, total: int) -> str:
    """Format progress message with consciousness."""
    return f"Working on it... {task} ({current}/{total})"


def format_services_ready_conscious(count: int) -> str:
    """Format services ready message with consciousness."""
    return f"All {count} services initialized - I'm ready to help."
