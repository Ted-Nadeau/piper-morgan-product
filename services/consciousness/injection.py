"""
Consciousness Injection Pipeline

Transforms data-driven output into conscious narrative expression.

The pipeline:
1. Context Analysis - Understand the situation
2. Pattern Selection - Choose appropriate patterns
3. Narrative Construction - Build the arc
4. MVC Validation - Ensure requirements met

Issue: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

import random
from typing import Any, Dict, List, Optional

from services.consciousness.context import ConsciousnessContext, analyze_context
from services.consciousness.templates import (
    get_accomplishment_recognition,
    get_context_acknowledgment,
    get_dialogue_invitation,
    get_gentle_flagging,
    get_priority_framing,
    get_spatial_journey,
    get_summary_synthesis,
    get_temporal_greeting,
)
from services.consciousness.validation import MVCResult, validate_mvc


async def inject_consciousness(
    data: Dict[str, Any],
    context: Optional[ConsciousnessContext] = None,
    format_type: str = "narrative",
) -> str:
    """
    Transform data into conscious narrative expression.

    This is the main entry point for consciousness injection.

    Args:
        data: Dictionary containing feature data (e.g., StandupResult as dict)
        context: Pre-analyzed context (will analyze if not provided)
        format_type: Output format - "narrative" (default), "slack", or "markdown"

    Returns:
        Conscious narrative string
    """
    # Step 1: Context Analysis
    if context is None:
        context = analyze_context(data)

    # Step 2 & 3: Pattern Selection & Narrative Construction
    narrative = construct_narrative(data, context)

    # Step 4: MVC Validation
    mvc_result = validate_mvc(narrative)
    if not mvc_result.passes:
        narrative = fix_mvc_gaps(narrative, mvc_result)

    # Apply format-specific transformations
    if format_type == "slack":
        narrative = apply_slack_formatting(narrative)
    elif format_type == "markdown":
        narrative = apply_markdown_formatting(narrative)

    return narrative


def construct_narrative(
    data: Dict[str, Any],
    context: ConsciousnessContext,
) -> str:
    """
    Construct the narrative arc from data and context.

    Arc structure:
    1. Opening (greeting/acknowledgment)
    2. Journey (source navigation)
    3. Discovery (accomplishments, priorities)
    4. Concern (blockers, missing data)
    5. Closing (synthesis, invitation)
    """
    sections: List[str] = []

    # 1. OPENING
    if context.should_use_full_arc:
        opening = get_temporal_greeting(context.time_of_day)
    elif context.user_in_meeting:
        opening = get_context_acknowledgment("in_meeting")
    elif context.meeting_load == "heavy":
        opening = get_context_acknowledgment(
            "heavy_meeting_day",
            meeting_hours=context.meeting_hours,
            meeting_count=context.meeting_count,
        )
    else:
        opening = get_context_acknowledgment("general")
    sections.append(opening)

    # 2. JOURNEY (if multiple sources)
    if context.data_sources_count > 1:
        journey = get_spatial_journey(context.data_sources)
        if journey:
            sections.append(journey)

    # 3. DISCOVERY
    # Accomplishments
    accomplishments = data.get("yesterday_accomplishments", [])
    # Clean up emoji prefixes for natural language
    clean_accomplishments = [a.lstrip("✅📋🎯 ").strip() for a in accomplishments if a]
    accomplishment_text = get_accomplishment_recognition(clean_accomplishments)
    if accomplishment_text:
        sections.append(accomplishment_text)

    # Priorities
    priorities = data.get("today_priorities", [])
    clean_priorities = [p.lstrip("🎯📅🔄💡📄 ").strip() for p in priorities if p]
    priority_context = {
        "meeting_load": context.meeting_load,
        "meeting_count": context.meeting_count,
        "meeting_hours": context.meeting_hours,
    }
    priority_text = get_priority_framing(clean_priorities[:3], priority_context)
    if priority_text:
        sections.append(priority_text)

    # 4. CONCERN
    blockers = data.get("blockers", [])
    clean_blockers = [b.lstrip("⚠️🗓️ ").strip() for b in blockers if b]
    if clean_blockers:
        concern_text = get_gentle_flagging(clean_blockers)
        if concern_text:
            sections.append(concern_text)

    # 5. CLOSING
    summary_context = {
        "has_blockers": context.has_blockers,
        "has_accomplishments": context.has_accomplishments,
        "meeting_load": context.meeting_load,
    }
    summary = get_summary_synthesis(summary_context)
    sections.append(summary)

    invitation = get_dialogue_invitation()
    sections.append(invitation)

    # Join sections with appropriate spacing
    return "\n\n".join(sections)


def fix_mvc_gaps(narrative: str, mvc_result: MVCResult) -> str:
    """
    Fix MVC gaps in the narrative.

    Args:
        narrative: The narrative that failed MVC
        mvc_result: The MVC result showing what's missing

    Returns:
        Fixed narrative that passes MVC
    """
    fixed = narrative

    if "identity" in mvc_result.missing:
        # Prepend identity statement
        prefixes = [
            "I've been looking at your context. ",
            "Here's what I found. ",
            "I pulled together this summary. ",
        ]
        fixed = random.choice(prefixes) + fixed

    if "uncertainty" in mvc_result.missing:
        # Insert hedge near the beginning
        hedges = [
            "From what I can see, ",
            "It looks like ",
            "Based on what I'm seeing, ",
        ]
        # Find first sentence and prepend hedge
        if ". " in fixed:
            first_period = fixed.index(". ")
            # Insert after first sentence
            fixed = fixed[: first_period + 2] + random.choice(hedges) + fixed[first_period + 2 :]
        else:
            fixed = random.choice(hedges) + fixed

    if "attribution" in mvc_result.missing:
        # Add attribution near the beginning
        attributions = [
            "Based on your recent activity, ",
            "Looking at your context, ",
        ]
        fixed = random.choice(attributions) + fixed

    if "invitation" in mvc_result.missing:
        # Add invitation at end
        invitations = [
            "\n\nHow does that sound?",
            "\n\nAnything you'd like me to adjust?",
            "\n\nLet me know if you want to change anything.",
        ]
        fixed = fixed.rstrip() + random.choice(invitations)

    return fixed


def ensure_mvc(output: str) -> str:
    """
    Ensure output meets MVC, fixing gaps as needed.

    Convenience function for simple use cases.

    Args:
        output: The output to ensure MVC compliance

    Returns:
        MVC-compliant output
    """
    result = validate_mvc(output)
    if result.passes:
        return output
    return fix_mvc_gaps(output, result)


def apply_slack_formatting(narrative: str) -> str:
    """Apply Slack-specific formatting to narrative."""
    # Add subtle emoji markers without changing the narrative feel
    formatted = narrative

    # Bold key phrases for Slack
    formatted = formatted.replace("Good morning!", "*Good morning!*")
    formatted = formatted.replace("Afternoon check-in!", "*Afternoon check-in!*")

    return formatted


def apply_markdown_formatting(narrative: str) -> str:
    """Apply Markdown-specific formatting to narrative."""
    formatted = narrative

    # Add heading for first line
    lines = formatted.split("\n\n")
    if lines:
        lines[0] = f"## {lines[0]}"
        formatted = "\n\n".join(lines)

    return formatted
