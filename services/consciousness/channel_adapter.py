"""
Channel Personality Adapter (#426 MUX-IMPLEMENT-CONSISTENT)

Ensures Piper maintains consistent identity while adapting
communication style to each channel's context.

Design principle: "Same Colleague, Different Room"
- Slack DM = quick hallway chat
- Slack Channel = team meeting
- Web Chat = at their desk
- CLI = in the server room

The PERSONALITY adapts. The IDENTITY never changes.

Core identity anchors (never change):
- First person ("I", never "Piper")
- Colleague tone (not assistant, not servant)
- Honest uncertainty expression
- No surveillance language

What adapts:
- Verbosity (terse → detailed)
- Formality (casual → professional)
- Emoji usage
- Opening style
- Response length
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from services.shared_types import InteractionSpace


class Verbosity(str, Enum):
    """How much Piper says."""

    TERSE = "terse"  # CLI: bare facts
    BRIEF = "brief"  # Slack DM: quick and casual
    STANDARD = "standard"  # Slack Channel: professional completeness
    DETAILED = "detailed"  # Web: full exploration


class Formality(str, Enum):
    """How Piper says it."""

    CASUAL = "casual"  # CLI, Slack DM: relaxed colleague
    CONVERSATIONAL = "conversational"  # Web: warm and engaged
    PROFESSIONAL = "professional"  # Slack Channel: polished


class OpeningStyle(str, Enum):
    """How Piper starts the conversation."""

    MINIMAL = "minimal"  # CLI: straight to content
    GREETING = "greeting"  # Web: "Good morning!"
    CONTEXTUAL = "contextual"  # Slack Channel: acknowledge context


@dataclass(frozen=True)
class ChannelPersonality:
    """
    Personality parameters for a channel.

    These control HOW Piper communicates, not WHAT Piper says.
    The core message stays the same; the delivery adapts.
    """

    verbosity: Verbosity
    formality: Formality
    emoji_allowed: bool
    max_response_lines: int  # Soft limit, not hard cutoff
    opening_style: OpeningStyle
    # Additional guidance
    bullet_style: str  # "dash", "bullet", "none"
    include_follow_up: bool  # "How does that sound?"


# Channel personality configurations
# These encode the "Same Colleague, Different Room" principle
CHANNEL_PERSONALITIES: dict[InteractionSpace, ChannelPersonality] = {
    #
    # CLI: Server room. Terse, no fluff, power user.
    # "3 tasks due. 2 meetings. 1 PR waiting."
    #
    InteractionSpace.CLI: ChannelPersonality(
        verbosity=Verbosity.TERSE,
        formality=Formality.CASUAL,
        emoji_allowed=False,
        max_response_lines=5,
        opening_style=OpeningStyle.MINIMAL,
        bullet_style="none",
        include_follow_up=False,
    ),
    #
    # Slack DM: Hallway chat. Brief, personal, casual.
    # "You've got 3 tasks today:\n• Finish Henderson proposal..."
    #
    InteractionSpace.SLACK_DM: ChannelPersonality(
        verbosity=Verbosity.BRIEF,
        formality=Formality.CASUAL,
        emoji_allowed=True,
        max_response_lines=10,
        opening_style=OpeningStyle.MINIMAL,
        bullet_style="bullet",
        include_follow_up=False,
    ),
    #
    # Slack Channel: Team meeting. Professional, contextual.
    # Others are watching - be polished but not stiff.
    #
    InteractionSpace.SLACK_CHANNEL: ChannelPersonality(
        verbosity=Verbosity.STANDARD,
        formality=Formality.PROFESSIONAL,
        emoji_allowed=True,
        max_response_lines=15,
        opening_style=OpeningStyle.CONTEXTUAL,
        bullet_style="bullet",
        include_follow_up=False,
    ),
    #
    # Web Chat: At the desk. Detailed, warm, exploratory.
    # "Good morning! Here's what I see on your radar..."
    #
    InteractionSpace.WEB_CHAT: ChannelPersonality(
        verbosity=Verbosity.DETAILED,
        formality=Formality.CONVERSATIONAL,
        emoji_allowed=False,
        max_response_lines=30,
        opening_style=OpeningStyle.GREETING,
        bullet_style="dash",
        include_follow_up=True,
    ),
    #
    # API: Structured, neutral. For programmatic access.
    #
    InteractionSpace.API: ChannelPersonality(
        verbosity=Verbosity.STANDARD,
        formality=Formality.PROFESSIONAL,
        emoji_allowed=False,
        max_response_lines=20,
        opening_style=OpeningStyle.MINIMAL,
        bullet_style="dash",
        include_follow_up=False,
    ),
    #
    # Unknown: Safe default (Web Chat style)
    #
    InteractionSpace.UNKNOWN: ChannelPersonality(
        verbosity=Verbosity.STANDARD,
        formality=Formality.CONVERSATIONAL,
        emoji_allowed=False,
        max_response_lines=20,
        opening_style=OpeningStyle.GREETING,
        bullet_style="dash",
        include_follow_up=True,
    ),
}


def get_channel_personality(
    channel: InteractionSpace,
) -> ChannelPersonality:
    """
    Get the personality configuration for a channel.

    Args:
        channel: The interaction space

    Returns:
        ChannelPersonality with appropriate settings
    """
    return CHANNEL_PERSONALITIES.get(
        channel,
        CHANNEL_PERSONALITIES[InteractionSpace.UNKNOWN],
    )


def adapt_verbosity(text: str, personality: ChannelPersonality) -> str:
    """
    Adapt text verbosity to match channel personality.

    Args:
        text: The narrative text
        personality: Channel personality settings

    Returns:
        Text adapted for verbosity level
    """
    if personality.verbosity == Verbosity.TERSE:
        return _make_terse(text)
    elif personality.verbosity == Verbosity.BRIEF:
        return _make_brief(text)
    elif personality.verbosity == Verbosity.DETAILED:
        # Detailed is the natural state - no reduction needed
        return text
    else:  # STANDARD
        return _make_standard(text)


def _make_terse(text: str) -> str:
    """
    Make text terse for CLI.

    Removes:
    - Greetings and closings
    - Filler phrases
    - Explanatory context
    - Follow-up questions

    Keeps:
    - Core facts
    - Numbers and data
    - Action items
    """
    lines = text.split("\n")
    terse_lines = []

    # Phrases that add warmth but not information
    skip_patterns = [
        "Good morning",
        "Good afternoon",
        "Good evening",
        "Here's what",
        "I noticed",
        "It looks like",
        "Based on what I",
        "How does that sound",
        "Let me know",
        "Anything you'd like",
        "Would you like",
        "Let me share",
        "Let me tell",
        "Looks like",
        "Productive day",
        "Does this capture",
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip lines that are purely social
        skip = False
        for pattern in skip_patterns:
            if line.startswith(pattern):
                skip = True
                break

        if not skip:
            # Remove filler phrases from within lines
            line = _remove_filler(line)
            if line:
                terse_lines.append(line)

    return "\n".join(terse_lines[:5])  # Hard limit for CLI


def _make_brief(text: str) -> str:
    """
    Make text brief for Slack DM.

    Keeps warmth but removes:
    - Extended explanations
    - Multiple alternatives
    - Detailed context
    """
    lines = text.split("\n")
    brief_lines = []

    # Keep first greeting if present
    if lines and _is_greeting(lines[0]):
        brief_lines.append(lines[0].strip())
        lines = lines[1:]

    # Keep substantive lines
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Skip follow-up questions in brief mode
        if _is_follow_up(line):
            continue

        brief_lines.append(line)

    return "\n".join(brief_lines[:10])  # Soft limit for Slack DM


def _make_standard(text: str) -> str:
    """
    Make text standard for Slack Channel.

    Professional but not verbose.
    """
    lines = text.split("\n")
    standard_lines = []

    for line in lines:
        line = line.strip()
        if not line:
            continue
        standard_lines.append(line)

    return "\n".join(standard_lines[:15])  # Soft limit for channel


def _is_greeting(line: str) -> bool:
    """Check if line is a greeting."""
    greetings = [
        "Good morning",
        "Good afternoon",
        "Good evening",
        "Hi!",
        "Hey!",
        "Let me share",
        "Let me tell",
        "Here's what",
    ]
    return any(line.startswith(g) for g in greetings)


def _is_follow_up(line: str) -> bool:
    """Check if line is a follow-up question."""
    follow_ups = [
        "How does that sound",
        "Let me know",
        "Anything you'd like",
        "Would you like",
        "Want me to",
        "Does this capture",
        "Anything to change",
        "Anything you'd",
    ]
    return any(line.startswith(f) for f in follow_ups)


def _remove_filler(line: str) -> str:
    """Remove filler phrases from a line."""
    fillers = [
        "I think ",
        "It seems like ",
        "From what I can see, ",
        "Looking at your context, ",
        "Based on what I'm seeing, ",
    ]
    result = line
    for filler in fillers:
        if result.startswith(filler):
            result = result[len(filler) :]
            # Capitalize first letter
            if result:
                result = result[0].upper() + result[1:]
    return result


def strip_emojis(text: str) -> str:
    """
    Remove emojis from text.

    Used for channels where emojis aren't appropriate (CLI, Web).
    """
    import re

    # Unicode emoji pattern
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map symbols
        "\U0001f1e0-\U0001f1ff"  # flags
        "\U00002702-\U000027b0"  # dingbats
        "\U000024c2-\U0001f251"  # enclosed characters
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub("", text).strip()


def adjust_formality(text: str, formality: Formality) -> str:
    """
    Adjust text formality.

    Args:
        text: The narrative text
        formality: Target formality level

    Returns:
        Text with adjusted formality
    """
    if formality == Formality.CASUAL:
        return _make_casual(text)
    elif formality == Formality.PROFESSIONAL:
        return _make_professional(text)
    else:  # CONVERSATIONAL - default state
        return text


def _make_casual(text: str) -> str:
    """Make text more casual."""
    # Use contractions
    replacements = [
        ("I have", "I've"),
        ("I am", "I'm"),
        ("you are", "you're"),
        ("you have", "you've"),
        ("do not", "don't"),
        ("does not", "doesn't"),
        ("cannot", "can't"),
        ("will not", "won't"),
        ("would not", "wouldn't"),
        ("could not", "couldn't"),
        ("should not", "shouldn't"),
        ("is not", "isn't"),
        ("are not", "aren't"),
        ("was not", "wasn't"),
        ("were not", "weren't"),
        ("has not", "hasn't"),
        ("have not", "haven't"),
        ("had not", "hadn't"),
        ("it is", "it's"),
        ("that is", "that's"),
        ("there is", "there's"),
        ("here is", "here's"),
        ("what is", "what's"),
        ("who is", "who's"),
        ("let us", "let's"),
    ]
    result = text
    for formal, casual in replacements:
        result = result.replace(formal, casual)
        # Also handle capitalized versions
        result = result.replace(formal.capitalize(), casual.capitalize())
    return result


def _make_professional(text: str) -> str:
    """Make text more professional."""
    # For professional, we keep it as-is but ensure no overly casual phrases
    casual_phrases = [
        ("Hey!", "Hello,"),
        ("Hey there!", "Hello,"),
        ("yeah", "yes"),
        ("gonna", "going to"),
        ("wanna", "want to"),
        ("gotta", "have to"),
        ("kinda", "kind of"),
        ("sorta", "sort of"),
    ]
    result = text
    for casual, professional in casual_phrases:
        result = result.replace(casual, professional)
        result = result.replace(casual.capitalize(), professional.capitalize())
    return result


def adapt_opening(text: str, personality: ChannelPersonality) -> str:
    """
    Adapt the opening style based on channel.

    Args:
        text: The narrative text
        personality: Channel personality settings

    Returns:
        Text with appropriate opening
    """
    lines = text.split("\n")
    if not lines:
        return text

    first_line = lines[0].strip()

    if personality.opening_style == OpeningStyle.MINIMAL:
        # Remove greeting, go straight to content
        if _is_greeting(first_line):
            lines = lines[1:]
            return "\n".join(lines).strip()

    elif personality.opening_style == OpeningStyle.CONTEXTUAL:
        # Keep or add contextual opening
        if _is_greeting(first_line):
            # Replace with contextual
            lines[0] = "Here's what I see:"
            return "\n".join(lines)

    # GREETING style or no change needed
    return text


def adapt_closing(text: str, personality: ChannelPersonality) -> str:
    """
    Adapt the closing based on channel.

    Args:
        text: The narrative text
        personality: Channel personality settings

    Returns:
        Text with appropriate closing
    """
    if not personality.include_follow_up:
        # Remove follow-up questions
        lines = text.split("\n")
        result_lines = [line for line in lines if not _is_follow_up(line.strip())]
        return "\n".join(result_lines).rstrip()

    return text


def adapt_bullets(text: str, personality: ChannelPersonality) -> str:
    """
    Adapt bullet style based on channel.

    Args:
        text: The narrative text
        personality: Channel personality settings

    Returns:
        Text with appropriate bullet style
    """
    if personality.bullet_style == "none":
        # Remove bullets, use commas or newlines
        text = text.replace("• ", "")
        text = text.replace("- ", "")
        text = text.replace("* ", "")
    elif personality.bullet_style == "bullet":
        # Use bullet points
        text = text.replace("- ", "• ")
        text = text.replace("* ", "• ")
    elif personality.bullet_style == "dash":
        # Use dashes
        text = text.replace("• ", "- ")
        text = text.replace("* ", "- ")

    return text


def adapt_for_channel(
    text: str,
    channel: InteractionSpace,
) -> str:
    """
    Adapt text for a specific channel.

    This is the main entry point for channel adaptation.
    Applies all personality transformations in the right order.

    Args:
        text: The narrative text
        channel: The interaction space

    Returns:
        Text adapted for the channel
    """
    personality = get_channel_personality(channel)

    # Apply transformations in order
    result = text

    # 1. Opening style
    result = adapt_opening(result, personality)

    # 2. Verbosity (most impactful)
    result = adapt_verbosity(result, personality)

    # 3. Formality
    result = adjust_formality(result, personality.formality)

    # 4. Emoji handling
    if not personality.emoji_allowed:
        result = strip_emojis(result)

    # 5. Bullet style
    result = adapt_bullets(result, personality)

    # 6. Closing style
    result = adapt_closing(result, personality)

    return result.strip()
