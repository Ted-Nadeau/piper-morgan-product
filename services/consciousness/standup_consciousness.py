"""
Consciousness Wrapper for Morning Standup Responses.

Transforms standup data into conscious narrative expression.
Part of Issue #632: Consciousness Integration for Morning Standup.

Uses the consciousness framework patterns to make standup output
feel like Piper is present, aware, and engaged in dialogue.

MVC (Minimum Viable Consciousness) Requirements:
1. Identity Voice - has "I" statement
2. Epistemic Humility - has uncertainty/hedge
3. Dialogue Opening - has invitation
4. Source Transparency - has attribution

Issue: #632 Consciousness Integration
ADR: ADR-056 Consciousness Expression Patterns
"""

from typing import Dict, List

from services.consciousness.validation import validate_mvc


def format_standup_greeting_conscious(sources: List[str]) -> str:
    """
    Format standup greeting with consciousness.

    Transforms from:
        "Good morning! Here's your standup summary."

    To:
        "I pulled together your standup by looking at your GitHub
         activity and recent conversations. Here's what I found..."

    Args:
        sources: List of data sources consulted (e.g., ["GitHub", "Calendar"])

    Returns:
        Conscious greeting string with identity and source attribution
    """
    if not sources:
        return (
            "I put together your morning standup. I didn't have specific "
            "data sources to check, so here's what I have based on our conversations."
        )

    if len(sources) == 1:
        source_text = f"your {sources[0]}"
    elif len(sources) == 2:
        source_text = f"your {sources[0]} and {sources[1]}"
    else:
        source_text = f"your {', '.join(sources[:-1])}, and {sources[-1]}"

    return (
        f"I pulled together your morning standup by looking at {source_text}. "
        "Here's what I found..."
    )


def format_accomplishments_conscious(accomplishments: List[str]) -> str:
    """
    Format yesterday's accomplishments with consciousness.

    Transforms from:
        "Yesterday you completed:
         - Fixed bug #123
         - Added feature"

    To:
        "Looking at yesterday, I see you made good progress.
         You knocked out the bug fix for #123, and you also
         got that new feature added. Solid work."

    Args:
        accomplishments: List of accomplishment strings

    Returns:
        Conscious accomplishments narrative with identity voice
    """
    if not accomplishments:
        return (
            "I didn't spot any specific accomplishments from yesterday in the data. "
            "That could mean a quieter day, or perhaps there's something worth "
            "capturing that I missed."
        )

    if len(accomplishments) == 1:
        return (
            f"Looking at yesterday, I found one thing that stood out: "
            f"you got '{accomplishments[0]}' done. Nice progress."
        )

    # Multiple accomplishments
    items = []
    for i, acc in enumerate(accomplishments[:5]):  # Limit to 5 for readability
        if i == 0:
            items.append(f"you completed '{acc}'")
        elif i == len(accomplishments) - 1 or i == 4:
            items.append(f"and '{acc}'")
        else:
            items.append(f"'{acc}'")

    items_text = ", ".join(items)

    if len(accomplishments) > 5:
        extra = len(accomplishments) - 5
        items_text += f", plus {extra} more items"

    return f"Looking at yesterday, I found some solid progress. {items_text.capitalize()}."


def format_priorities_conscious(priorities: List[str]) -> str:
    """
    Format today's priorities with consciousness.

    Transforms from:
        "Today's priorities:
         1. Continue work
         2. Review feedback"

    To:
        "For today, I think the focus should be on continuing
         the work in progress. There's also the feedback review
         that looks like it needs attention."

    Args:
        priorities: List of priority strings for today

    Returns:
        Conscious priorities narrative with reasoning
    """
    if not priorities:
        return (
            "I don't see any specific priorities set for today. "
            "Would you like to think through what's most important?"
        )

    if len(priorities) == 1:
        return (
            f"For today, I think '{priorities[0]}' seems like the main focus. "
            "Does that feel right?"
        )

    # Multiple priorities
    main_priority = priorities[0]
    others = priorities[1:]

    if len(others) == 1:
        other_text = f"There's also '{others[0]}' that looks like it needs attention."
    else:
        other_items = [f"'{p}'" for p in others[:3]]
        other_text = (
            f"There's also {', '.join(other_items[:-1])} and {other_items[-1]} "
            "that look like they need attention."
        )

    return (
        f"For today, I think '{main_priority}' should probably be the main focus. " f"{other_text}"
    )


def format_blockers_conscious(blockers: List[str]) -> str:
    """
    Format blockers with consciousness and epistemic humility.

    Transforms from:
        "Blockers: None" or "Blockers:
         - Waiting on API access"

    To:
        "I didn't spot any blockers, but let me know if something's
         getting in your way." or "I noticed a potential blocker -
         you're waiting on API access. Might be worth following up."

    Args:
        blockers: List of blocker strings (empty list if none)

    Returns:
        Conscious blockers narrative with epistemic humility
    """
    if not blockers:
        return (
            "I didn't spot any blockers in the data, but let me know if something's "
            "getting in your way that I should know about."
        )

    if len(blockers) == 1:
        return (
            f"I noticed something that might be blocking progress: '{blockers[0]}'. "
            "Might be worth following up on that."
        )

    # Multiple blockers
    blocker_items = [f"'{b}'" for b in blockers[:3]]
    if len(blockers) > 3:
        blocker_items.append(f"and {len(blockers) - 3} more")

    blockers_text = ", ".join(blocker_items[:-1]) + f", and {blocker_items[-1]}"

    return (
        f"I noticed a few things that might be blocking progress: {blockers_text}. "
        "These seem worth addressing."
    )


def format_standup_closing_conscious(metrics: Dict) -> str:
    """
    Format standup closing with consciousness and dialogue invitation.

    Transforms from:
        "Generated in 1.2s. Estimated time saved: 15 minutes."

    To:
        "I put this together in about a second. Does this capture
         everything? Let me know if anything needs adjusting."

    Args:
        metrics: Dict with generation_time_ms, time_saved_minutes, etc.

    Returns:
        Conscious closing with dialogue invitation
    """
    generation_time = metrics.get("generation_time_ms", 0)
    time_saved = metrics.get("time_saved_minutes", 0)

    # Convert milliseconds to human-readable
    if generation_time < 1000:
        time_text = "less than a second"
    elif generation_time < 5000:
        time_text = "about a second"
    else:
        seconds = generation_time / 1000
        time_text = f"about {seconds:.0f} seconds"

    closing_parts = [f"I put this together in {time_text}."]

    if time_saved > 0:
        closing_parts.append(
            f"It looks like this might save you around {time_saved} minutes "
            "compared to gathering this yourself."
        )

    closing_parts.append("Does this capture everything? Anything you'd like to adjust?")

    return " ".join(closing_parts)


def format_full_standup_conscious(standup_data: Dict) -> str:
    """
    Format complete standup report with consciousness.

    Combines all sections into a coherent conscious narrative.
    Ensures the complete output passes MVC validation.

    Args:
        standup_data: Dict containing:
            - sources: List[str] - data sources consulted
            - yesterday_accomplishments: List[str] - what got done
            - today_priorities: List[str] - focus for today
            - blockers: List[str] - things blocking progress
            - metrics: Dict - generation stats

    Returns:
        Complete conscious standup narrative
    """
    sources = standup_data.get("sources", [])
    accomplishments = standup_data.get("yesterday_accomplishments", [])
    priorities = standup_data.get("today_priorities", [])
    blockers = standup_data.get("blockers", [])
    metrics = standup_data.get("metrics", {})

    sections = [
        format_standup_greeting_conscious(sources),
        "",  # Section separator
        "**Yesterday**",
        format_accomplishments_conscious(accomplishments),
        "",
        "**Today**",
        format_priorities_conscious(priorities),
        "",
        "**Blockers**",
        format_blockers_conscious(blockers),
        "",
        "---",
        format_standup_closing_conscious(metrics),
    ]

    narrative = "\n".join(sections)

    # Validate MVC and fix if needed
    mvc_result = validate_mvc(narrative)
    if not mvc_result.passes:
        narrative = _fix_mvc_gaps(narrative, mvc_result)

    return narrative


def _fix_mvc_gaps(narrative: str, mvc_result) -> str:
    """
    Fix any missing MVC requirements in the narrative.

    This is a safety net - the individual functions should already
    produce MVC-compliant output, but this ensures the combined
    narrative passes validation.

    Args:
        narrative: The current narrative text
        mvc_result: MVCResult from validation

    Returns:
        Fixed narrative with all MVC requirements met
    """
    fixed = narrative

    if "identity" in mvc_result.missing:
        fixed = "I put together your standup summary. " + fixed

    if "uncertainty" in mvc_result.missing:
        fixed = fixed.replace("the focus should be", "it looks like the focus should be")

    if "invitation" in mvc_result.missing:
        fixed = fixed.rstrip() + " Anything you'd like me to adjust?"

    if "attribution" in mvc_result.missing:
        fixed = "Looking at your recent activity, " + fixed

    return fixed
