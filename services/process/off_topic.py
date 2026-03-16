"""
Off-topic detection for guided processes (Layer C).

Issue #899: Detect when user messages during a guided process are clearly
not responses to the current process prompt. Conservative approach: only
flag clear non-sequiturs, not ambiguous messages.

PPM decisions (2026-03-16):
- Conservative aggressiveness: flag but don't block ambiguous messages
- Regex-first approach (LLM fallback deferred to Phase 2)
- All 3 process types (onboarding, standup, slot-filling)
- Option A UX: auto-pause + answer their actual question

Architecture:
- Each process type has its own pattern set (what IS on-topic)
- Generic off-topic patterns catch clear non-sequiturs across all types
- Returns OffTopicResult with confidence and suggested response framing
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional, Tuple

import structlog

from services.process.registry import ProcessType

logger = structlog.get_logger(__name__)


class OffTopicConfidence(str, Enum):
    """How confident we are that a message is off-topic."""

    CLEAR = "clear"  # Definitely off-topic (e.g., "What's the weather?")
    LIKELY = "likely"  # Probably off-topic but some ambiguity
    UNCLEAR = "unclear"  # Can't tell — let the process handler decide


@dataclass
class OffTopicResult:
    """Result of off-topic analysis."""

    is_off_topic: bool
    confidence: OffTopicConfidence
    matched_pattern: Optional[str] = None  # Which pattern matched (for logging)


# ---- Generic off-topic patterns (clear non-sequiturs in ANY guided process) ----

# These are messages that are clearly not answering any process prompt.
# Conservative: only things that could never be a process response.
GENERIC_OFF_TOPIC_PATTERNS: List[Tuple[re.Pattern, str]] = [
    # Weather/time queries
    (
        re.compile(
            r"\b(?:what(?:'s| is) the weather|weather (?:forecast|today|tomorrow|outside)|is it raining)\b",
            re.I,
        ),
        "weather_query",
    ),
    (
        re.compile(r"\b(?:what time is it|what(?:'s| is) the time|current time)\b", re.I),
        "time_query",
    ),
    (re.compile(r"\b(?:what(?:'s| is) today(?:'s| s)? date|what day is it)\b", re.I), "date_query"),
    # Identity/capability queries about Piper
    (
        re.compile(r"\b(?:who are you|what are you|tell me about yourself)\b", re.I),
        "identity_query",
    ),
    (
        re.compile(
            r"\b(?:what can you (?:do|help)|show me your capabilities|your capabilities)\b", re.I
        ),
        "capability_query",
    ),
    # Unrelated commands/requests
    (
        re.compile(r"\b(?:tell me a joke|sing me a song|write me a poem)\b", re.I),
        "entertainment_request",
    ),
    (
        re.compile(r"\b(?:what(?:'s| is) the meaning of life|meaning of life)\b", re.I),
        "philosophical_query",
    ),
    (
        re.compile(r"\b(?:translate|convert|calculate)\b.*\b(?:to|into|from)\b", re.I),
        "utility_request",
    ),
    # Explicit topic changes
    (
        re.compile(
            r"^(?:by the way|btw|oh wait|actually|hey|so)\b[,.]?\s*(?:can you|could you|would you|do you)",
            re.I,
        ),
        "topic_change",
    ),
]


# ---- Process-specific on-topic patterns ----
# These define what IS relevant to each process. If a message matches
# on-topic patterns, it's NOT off-topic regardless of other signals.

ONBOARDING_ON_TOPIC_PATTERNS: List[re.Pattern] = [
    # Project names, repos, URLs (typical onboarding answers)
    re.compile(r"https?://", re.I),
    re.compile(r"github\.com|gitlab\.com|bitbucket", re.I),
    re.compile(r"\b(?:project|repo|repository|app|service|api|website|site)\b", re.I),
    # Affirmative/negative responses to prompts
    re.compile(
        r"^(?:yes|no|yeah|nah|sure|ok|okay|yep|nope|not really|none|nothing|that(?:'s| is) (?:it|all))\b",
        re.I,
    ),
    # Numbers (project counts, etc.)
    re.compile(r"^\d+$"),
    # Short names (likely project names) — max 3 words, no question marks
    re.compile(r"^[A-Za-z][\w-]*(?:\s+[A-Za-z][\w-]*){0,2}$"),
]

STANDUP_ON_TOPIC_PATTERNS: List[re.Pattern] = [
    # Work-related vocabulary
    re.compile(r"\b(?:working on|worked on|finished|completed|done|started|continuing)\b", re.I),
    re.compile(r"\b(?:blocked|blocker|stuck|waiting|depend|pending)\b", re.I),
    re.compile(r"\b(?:pr|pull request|merge|commit|deploy|release|ship)\b", re.I),
    re.compile(r"\b(?:bug|fix|feature|task|ticket|issue|story|sprint)\b", re.I),
    re.compile(r"\b(?:meeting|sync|standup|retro|review|planning)\b", re.I),
    re.compile(r"\b(?:today|yesterday|tomorrow|this week|last week)\b", re.I),
    # Affirmative/negative
    re.compile(
        r"^(?:yes|no|yeah|nah|sure|ok|okay|yep|nope|not really|none|nothing|that(?:'s| is) (?:it|all))\b",
        re.I,
    ),
]

SLOT_FILLING_ON_TOPIC_PATTERNS: List[re.Pattern] = [
    # Slot filling is very context-dependent — be very conservative
    # Almost any short direct answer could be a slot value
    re.compile(r"^.{1,100}$"),  # Short messages are likely slot values
    # Affirmative/negative
    re.compile(r"^(?:yes|no|yeah|nah|sure|ok|okay|yep|nope|not really|none|nothing)\b", re.I),
]

# Map process types to their on-topic patterns
_ON_TOPIC_PATTERNS = {
    ProcessType.ONBOARDING: ONBOARDING_ON_TOPIC_PATTERNS,
    ProcessType.STANDUP: STANDUP_ON_TOPIC_PATTERNS,
    ProcessType.SLOT_FILLING: SLOT_FILLING_ON_TOPIC_PATTERNS,
}


def detect_off_topic(
    message: str,
    process_type: ProcessType,
) -> OffTopicResult:
    """
    Determine if a message is off-topic for a given guided process.

    Issue #899: Conservative detection — only flag clear non-sequiturs.
    Under-detection is annoying but safe; over-detection breaks flow.

    Algorithm:
    1. Check on-topic patterns first — if message looks relevant, let it through
    2. Check generic off-topic patterns — if clear non-sequitur, flag it
    3. Default to UNCLEAR — let the process handler decide

    Args:
        message: The user's message
        process_type: Which guided process is active

    Returns:
        OffTopicResult with detection verdict
    """
    stripped = message.strip()

    # Empty or very short messages are never off-topic (could be "yes", "no", etc.)
    if len(stripped) < 3:
        return OffTopicResult(
            is_off_topic=False,
            confidence=OffTopicConfidence.CLEAR,
        )

    # Step 1: Check on-topic patterns — if it matches, it's on-topic
    on_topic_patterns = _ON_TOPIC_PATTERNS.get(process_type, [])
    for pattern in on_topic_patterns:
        if pattern.search(stripped):
            return OffTopicResult(
                is_off_topic=False,
                confidence=OffTopicConfidence.CLEAR,
            )

    # Step 2: Check generic off-topic patterns
    for pattern, pattern_name in GENERIC_OFF_TOPIC_PATTERNS:
        if pattern.search(stripped):
            logger.info(
                "off_topic_detected",
                process_type=process_type.value,
                pattern=pattern_name,
                message_preview=stripped[:50],
            )
            return OffTopicResult(
                is_off_topic=True,
                confidence=OffTopicConfidence.CLEAR,
                matched_pattern=pattern_name,
            )

    # Step 3: Default — unclear, let the handler decide
    return OffTopicResult(
        is_off_topic=False,
        confidence=OffTopicConfidence.UNCLEAR,
    )


def format_off_topic_pause_message(process_type: ProcessType) -> str:
    """
    Format the auto-pause message for Option A UX.

    Issue #899: PM decision — auto-pause + answer their question.
    "That doesn't seem related to [process]. I've paused it —
    you can say 'resume' to continue."
    """
    process_names = {
        ProcessType.ONBOARDING: "onboarding",
        ProcessType.STANDUP: "your standup",
        ProcessType.SLOT_FILLING: "what we were working on",
    }
    name = process_names.get(process_type, "the current process")

    return (
        f"That doesn't seem related to {name}, so I've paused it — "
        "you can say 'resume' to continue anytime."
    )
