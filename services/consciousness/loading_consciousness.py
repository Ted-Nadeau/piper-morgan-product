"""
Consciousness Wrapper for Loading State Messages

Transforms loading messages into conscious narrative expression.
Part of Consciousness Rollout Wave 1 (#630)

Issue: #630 CONSCIOUSNESS-TRANSFORM: Loading States
Framework: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

from typing import Dict

from services.consciousness.validation import validate_mvc

# Consciousness-enhanced loading messages
# Each message follows MVC: Identity, Humility (where appropriate), Transparency
CONSCIOUS_LOADING_MESSAGES: Dict[str, Dict[str, str]] = {
    "workflow_execution": {
        "starting": "I'm starting the workflow now...",
        "in_progress": "Working through the steps - this might take a moment...",
        "completing": "Almost done, just finishing up...",
        "completed": "Done! Here's what I found.",
        "failed": "I ran into a problem with the workflow. Let me know if you'd like me to try again.",
        "timeout": "This is taking longer than expected. Want me to keep trying, or should we try something else?",
    },
    "llm_query": {
        "starting": "I'm thinking about your question...",
        "in_progress": "Working on this - give me a moment...",
        "completing": "Almost have your answer...",
        "completed": "Here's what I came up with.",
        "failed": "I had trouble processing that. Could you try rephrasing?",
        "timeout": "This is taking a while. Should I keep working on it?",
    },
    "github_api": {
        "starting": "I'm checking GitHub for you...",
        "in_progress": "Looking through your GitHub data...",
        "completing": "Found what I was looking for...",
        "completed": "Here's what I found on GitHub.",
        "failed": "I couldn't reach GitHub right now. Want me to try again?",
        "timeout": "GitHub is taking a while to respond. Should I keep waiting?",
    },
    "slack_api": {
        "starting": "I'm connecting to Slack...",
        "in_progress": "Sending your message to Slack...",
        "completing": "Just confirming it went through...",
        "completed": "Message sent! It should appear in Slack now.",
        "failed": "I couldn't send that to Slack. Want me to try again?",
        "timeout": "Slack is being slow. Should I keep trying?",
    },
    "database_query": {
        "starting": "I'm looking that up for you...",
        "in_progress": "Searching through the data...",
        "completing": "Found some results, organizing them...",
        "completed": "Here's what I found.",
        "failed": "I had trouble with the search. Let me know if you'd like me to try again.",
        "timeout": "This search is taking longer than expected. Should I keep going?",
    },
    "file_processing": {
        "starting": "I'm opening that file now...",
        "in_progress": "Reading through the content...",
        "completing": "Almost done processing...",
        "completed": "I've gone through the file. Here's what I found.",
        "failed": "I had trouble with that file. Is it in a format I can read?",
        "timeout": "This file is taking a while. It might be large - should I keep going?",
    },
    "knowledge_search": {
        "starting": "I'm searching for that...",
        "in_progress": "Looking through what I know...",
        "completing": "Found some things, ranking by relevance...",
        "completed": "Here's what I found that might help.",
        "failed": "I couldn't find what you're looking for. Could you try different terms?",
        "timeout": "This search is taking longer than I expected. Want me to keep looking?",
    },
    "intent_processing": {
        "starting": "I'm understanding what you need...",
        "in_progress": "Working out how to help...",
        "completing": "Got it, preparing my response...",
        "completed": "Here's what I can do.",
        "failed": "I'm not sure I understood that. Could you say it differently?",
        "timeout": "I'm still processing - give me another moment?",
    },
    "analysis": {
        "starting": "I'm starting to analyze this...",
        "in_progress": "Looking at the data and finding patterns...",
        "completing": "Almost done, putting together insights...",
        "completed": "Here's what I found in my analysis.",
        "failed": "I had trouble analyzing that. Is there something specific you'd like me to focus on?",
        "timeout": "This analysis is taking a while. Should I continue or try a simpler approach?",
    },
    "generation": {
        "starting": "I'm working on creating that for you...",
        "in_progress": "Generating content - this takes a bit...",
        "completing": "Almost ready, just reviewing...",
        "completed": "Here's what I created for you.",
        "failed": "I had trouble generating that. Want to try with different parameters?",
        "timeout": "This is taking longer than expected. Should I keep going?",
    },
}


def get_conscious_loading_message(operation_type: str, state: str) -> str:
    """
    Get a consciousness-enhanced loading message.

    Args:
        operation_type: Type of operation (e.g., "workflow_execution", "llm_query")
        state: Loading state (e.g., "starting", "in_progress", "completed")

    Returns:
        Conscious loading message string
    """
    # Normalize inputs
    op_type = operation_type.lower().replace("-", "_")
    state_key = state.lower().replace("-", "_")

    # Get messages for operation type
    messages = CONSCIOUS_LOADING_MESSAGES.get(op_type)
    if not messages:
        # Fallback to generic conscious message
        return _get_generic_conscious_message(state_key)

    # Get message for state
    message = messages.get(state_key)
    if not message:
        return _get_generic_conscious_message(state_key)

    return message


def _get_generic_conscious_message(state: str) -> str:
    """Get generic conscious message for unknown operation types."""
    generic_messages = {
        "starting": "I'm getting started on this...",
        "in_progress": "Working on it...",
        "completing": "Almost there...",
        "completed": "Done! Here's what I have.",
        "failed": "I ran into a problem. Want me to try again?",
        "timeout": "This is taking a while. Should I keep going?",
    }
    return generic_messages.get(state, "Working on it...")


def format_progress_conscious(
    operation_type: str,
    state: str,
    progress_percent: int = None,
    current_step: str = None,
    total_steps: int = None,
    current_step_number: int = None,
) -> str:
    """
    Format a progress update with consciousness.

    Combines the base message with progress details in a natural way.

    Args:
        operation_type: Type of operation
        state: Loading state
        progress_percent: Optional percentage complete
        current_step: Optional description of current step
        total_steps: Optional total number of steps
        current_step_number: Optional current step number

    Returns:
        Conscious progress message
    """
    base_message = get_conscious_loading_message(operation_type, state)

    # Add progress details naturally
    if progress_percent is not None and state == "in_progress":
        if progress_percent < 25:
            base_message = f"I'm just getting started... {base_message}"
        elif progress_percent < 50:
            base_message = f"Making progress... {base_message}"
        elif progress_percent < 75:
            base_message = f"More than halfway there. {base_message}"
        else:
            base_message = f"Almost done ({progress_percent}%). {base_message}"

    # Add step information naturally
    if current_step and total_steps and current_step_number:
        step_info = f" (Step {current_step_number} of {total_steps}: {current_step})"
        base_message = base_message.rstrip(".!") + step_info

    return base_message


def validate_loading_message(message: str) -> bool:
    """
    Validate that a loading message meets consciousness standards.

    For loading messages, we relax some MVC requirements since they're
    status updates, not full responses. We mainly check for Identity Voice.
    """
    # Loading messages should have "I" or "I'm"
    has_identity = "I'" in message or "I " in message or message.startswith("I")

    return has_identity
