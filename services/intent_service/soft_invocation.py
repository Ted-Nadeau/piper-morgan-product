"""
Soft workflow invocation from natural language.

Issue #767: GLUE-SOFTINVOKE — Detect implied workflow needs in natural
conversation and offer relevant capabilities softly.

Instead of requiring explicit commands ("/standup", "start project setup"),
this module detects natural expressions of need and generates soft offers:

    User: "I need to get the team together Tuesday"
    Piper: [normal response] + "I could help set up a meeting. Want me to find a time?"

Architecture:
- SoftInvocationDetector: Pattern-based detection of implied workflow needs
- WorkflowOffer: Data model for a soft offer
- SoftInvocationResult: Detection result with throttle info
- WorkflowOfferService: Offer generation, formatting, throttling via ProactivityGate
"""

import re
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import structlog

from services.domain.models import Intent
from services.trust.proactivity_gate import ProactivityGate, TrustStage

logger = structlog.get_logger(__name__)

# --- Constants ---

# Maximum offers per exchange window (requirement: max 2 per 5 exchanges)
MAX_OFFERS_PER_WINDOW = 2
EXCHANGE_WINDOW_SIZE = 5


# --- Data Models ---


@dataclass(frozen=True)
class WorkflowOffer:
    """A soft offer to start a workflow."""

    workflow_type: str  # e.g., "meeting", "standup", "project_setup", "status_check"
    offer_message: str  # "I could help set up a meeting. Want me to find a time?"
    decline_message: str  # "No worries, just let me know if you change your mind."
    confidence: float  # Pattern match confidence (0.0-1.0)
    trigger_pattern: str = ""  # Which pattern group matched


@dataclass
class SoftInvocationResult:
    """Result of soft invocation detection."""

    has_offer: bool
    offer: Optional[WorkflowOffer] = None
    throttled: bool = False  # True if offer was suppressed
    reason: str = ""  # Why offer was/wasn't generated


@dataclass
class OfferWindow:
    """Tracks offers within a sliding exchange window."""

    offer_turns: List[int] = field(default_factory=list)  # Turn numbers with offers

    def count_in_window(self, current_turn: int) -> int:
        """Count offers in the last EXCHANGE_WINDOW_SIZE turns."""
        window_start = max(0, current_turn - EXCHANGE_WINDOW_SIZE)
        return sum(1 for t in self.offer_turns if t >= window_start)

    def record_offer(self, turn: int) -> None:
        """Record that an offer was made at this turn."""
        self.offer_turns.append(turn)


# --- Pattern Definitions ---

# Each entry: (compiled patterns, workflow_type, offer_message, decline_message)
# Patterns are intentionally conservative to avoid false positives.

_SOFT_TRIGGER_PATTERNS: List[Tuple[List[re.Pattern], str, str, str]] = []


def _compile_patterns() -> List[Tuple[List[re.Pattern], str, str, str]]:
    """Compile pattern definitions. Called once at module load."""
    raw = [
        # Meeting / scheduling needs
        (
            [
                r"\b(?:i need to|we need to|should|let'?s)\b.*\b(?:get\b.*\btogether|meet|sync up|catch up|huddle)\b",
                r"\b(?:i need to|we need to|should|let'?s)\b.*\b(?:schedule|set up|plan)\b.*\b(?:meeting|call|sync)\b",
                r"\bwe should\b.*\b(?:talk about|discuss|go over)\b",
                r"\b(?:can someone|can we|could we)\b.*\b(?:meet|get\b.*\btogether|sync)\b",
            ],
            "meeting",
            "I could help set up a meeting. Want me to find a time?",
            "No worries, just let me know if you change your mind.",
        ),
        # Project organization / structure needs
        (
            [
                r"\b(?:this|the) project is (?:getting|becoming)\b.*\b(?:complicated|messy|disorganized|unwieldy|out of hand)\b",
                r"\b(?:i need to|we need to|help me)\b.*\b(?:organize|structure|plan out)\b",
                r"\bthings are (?:getting|becoming)\b.*\b(?:complicated|messy|scattered|disorganized)\b",
                r"\b(?:i don'?t know|not sure)\b.*\b(?:where to start|how to organize|how to structure)\b",
            ],
            "project_setup",
            "I could help organize things. Want to set up some structure?",
            "Got it, no worries. I'm here if you need help later.",
        ),
        # Status / deadline concerns
        (
            [
                r"\b(?:i'?m worried|i'?m concerned|worried|nervous)\b.*\b(?:deadline|timeline|schedule|behind|late)\b",
                r"\b(?:i don'?t know|not sure)\b.*\b(?:where (?:things|we) stand|progress|how (?:things|we) are doing)\b",
                r"\bare we (?:on track|behind|going to make)\b",
                r"\bhow (?:are things|is the project|are we)\b.*\b(?:going|progressing|looking)\b",
            ],
            "status_check",
            "Want me to pull up the project status so we can see where things stand?",
            "No problem. Just ask whenever you want an update.",
        ),
        # Team alignment / standup needs
        (
            [
                r"\b(?:the team needs|we need)\b.*\b(?:alignment|to be aligned|to sync|coordination)\b",
                r"\b(?:everyone|the team|people) (?:seems?|are|is)\b.*\b(?:out of sync|disconnected|not aligned|on different pages)\b",
                r"\bwe should (?:do|have|start)\b.*\b(?:standup|check-in|daily sync)\b",
            ],
            "standup",
            "A standup could help with that. Want me to start one?",
            "Sure thing. Let me know if you change your mind.",
        ),
        # Review / feedback needs
        (
            [
                r"\b(?:can someone|could someone|someone needs to|need someone to)\b.*\b(?:review|look at|check|give feedback)\b",
                r"\b(?:i need|we need)\b.*\b(?:feedback|review|second opinion|another set of eyes)\b",
            ],
            "review",
            "I could help coordinate a review. Want me to set that up?",
            "No worries, just let me know when you're ready.",
        ),
        # Priority / focus needs
        (
            [
                r"\b(?:i don'?t know|not sure)\b.*\b(?:what to (?:focus on|work on|prioritize)|my priorities)\b",
                r"\b(?:too many|so many)\b.*\b(?:things|tasks|priorities|items)\b.*\b(?:to do|going on|happening)\b",
                r"\bwhat should i\b.*\b(?:focus on|work on|do (?:first|next))\b",
            ],
            "priority_check",
            "I can help sort out priorities. Want me to take a look at what's on your plate?",
            "Okay, just let me know when you want to dig in.",
        ),
        # Reminder / tracking needs
        (
            [
                r"\bi keep forgetting\b.*\b(?:to|about)\b",
                r"\bi always forget\b.*\b(?:to|about)\b",
                r"\b(?:i need to|don'?t let me forget to)\b.*\b(?:remember|follow up|check back)\b",
            ],
            "reminder",
            "I can help you keep track of that. Want me to set a reminder?",
            "No problem. Just mention it again if you need a nudge.",
        ),
    ]

    compiled = []
    for patterns, workflow_type, offer_msg, decline_msg in raw:
        compiled_patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        compiled.append((compiled_patterns, workflow_type, offer_msg, decline_msg))
    return compiled


_SOFT_TRIGGER_PATTERNS = _compile_patterns()

# Accept/decline detection patterns
ACCEPT_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"^(?:yes|yeah|yep|yup|sure|please|okay|ok|go ahead|do it|let'?s do it|sounds good|sounds great|that would be great|please do|yes please)\.?!?$",
        r"^(?:yes|yeah|sure|please|go ahead),?\s",
        r"\byes,?\s*(?:please|go ahead|do it|that would)\b",
        r"\bsure,?\s*(?:let'?s|go ahead|please)\b",
    ]
]

DECLINE_PATTERNS = [
    re.compile(p, re.IGNORECASE)
    for p in [
        r"^(?:no|nah|nope|not now|not right now|never mind|i'?m good|no thanks|no thank you|just venting|skip)\.?!?$",
        r"^(?:no|nah),?\s",
        r"\b(?:not (?:now|right now|yet|today)|maybe later|i'?m (?:good|fine|okay)|just (?:venting|thinking|wondering))\b",
        r"\bno,?\s*(?:thanks|thank you|i'?m good|that'?s okay)\b",
    ]
]


# --- SoftInvocationDetector ---


class SoftInvocationDetector:
    """
    Detects implied workflow needs in natural conversation.

    Uses pattern matching against compiled expression groups.
    Each group maps to a workflow type with a pre-written offer message.
    """

    def detect(self, message: str) -> SoftInvocationResult:
        """
        Check if a message implies a workflow need.

        Args:
            message: User's message text

        Returns:
            SoftInvocationResult with offer if pattern matched
        """
        if not message or len(message) < 10:
            return SoftInvocationResult(
                has_offer=False,
                reason="Message too short for soft invocation",
            )

        clean = message.strip().lower()

        for compiled_patterns, workflow_type, offer_msg, decline_msg in _SOFT_TRIGGER_PATTERNS:
            for pattern in compiled_patterns:
                if pattern.search(clean):
                    offer = WorkflowOffer(
                        workflow_type=workflow_type,
                        offer_message=offer_msg,
                        decline_message=decline_msg,
                        confidence=0.7,
                        trigger_pattern=pattern.pattern,
                    )
                    logger.debug(
                        "soft_invocation_detected",
                        workflow_type=workflow_type,
                        pattern=pattern.pattern,
                        message_preview=message[:50],
                    )
                    return SoftInvocationResult(
                        has_offer=True,
                        offer=offer,
                        reason=f"Matched {workflow_type} pattern",
                    )

        return SoftInvocationResult(
            has_offer=False,
            reason="No soft invocation patterns matched",
        )


def detect_offer_response(message: str) -> Optional[str]:
    """
    Detect if a message is accepting or declining a previous offer.

    Args:
        message: User's response message

    Returns:
        "accept" if accepting, "decline" if declining, None if neither
    """
    if not message:
        return None

    clean = message.strip()

    for pattern in ACCEPT_PATTERNS:
        if pattern.search(clean):
            return "accept"

    for pattern in DECLINE_PATTERNS:
        if pattern.search(clean):
            return "decline"

    return None


# --- WorkflowOfferService ---


class WorkflowOfferService:
    """
    Manages soft workflow offers with ProactivityGate integration.

    Handles:
    - ProactivityGate trust-stage checking
    - Exchange window throttling (max 2 per 5 exchanges)
    - Natural offer formatting with decline paths
    """

    def __init__(self, proactivity_gate: Optional[ProactivityGate] = None):
        self.proactivity_gate = proactivity_gate or ProactivityGate()
        self._offer_windows: Dict[str, OfferWindow] = {}  # session_id → window

    def should_offer(
        self,
        trust_stage: TrustStage,
        session_id: str,
        current_turn: int,
        suggestions_this_session: int,
    ) -> Tuple[bool, str]:
        """
        Check if an offer should be presented right now.

        Checks:
        1. ProactivityGate allows hints at this trust stage
        2. Exchange window not saturated (< MAX_OFFERS_PER_WINDOW in last EXCHANGE_WINDOW_SIZE)
        3. Session-level limit not reached

        Args:
            trust_stage: User's current trust stage
            session_id: Current session ID
            current_turn: Current conversation turn number
            suggestions_this_session: Total suggestions already offered this session

        Returns:
            Tuple of (should_offer, reason)
        """
        # Check ProactivityGate — use can_offer_capability_hints for soft offers
        # (softer than can_proactive_suggest, available at Stage 2+)
        if not self.proactivity_gate.can_offer_capability_hints(trust_stage):
            return False, f"Trust stage {trust_stage.name} doesn't allow hints"

        # Check session-level limit directly (don't use should_suggest_now
        # which also checks can_proactive_suggest, blocking Stage 2 users)
        max_allowed = self.proactivity_gate.get_max_suggestions_per_session(trust_stage)
        if suggestions_this_session >= max_allowed:
            return False, "Session suggestion limit reached"

        # Check exchange window throttling
        window = self._offer_windows.get(session_id)
        if window is None:
            window = OfferWindow()
            self._offer_windows[session_id] = window

        offers_in_window = window.count_in_window(current_turn)
        if offers_in_window >= MAX_OFFERS_PER_WINDOW:
            return (
                False,
                f"Exchange window saturated ({offers_in_window}/{MAX_OFFERS_PER_WINDOW} in last {EXCHANGE_WINDOW_SIZE} turns)",
            )

        return True, "Offer allowed"

    def record_offer(self, session_id: str, turn: int) -> None:
        """Record that an offer was made."""
        window = self._offer_windows.get(session_id)
        if window is None:
            window = OfferWindow()
            self._offer_windows[session_id] = window
        window.record_offer(turn)

    def format_offer(self, offer: WorkflowOffer, base_response: str) -> str:
        """
        Append a soft offer to the base response with a natural transition.

        Args:
            offer: The workflow offer to append
            base_response: The existing response message

        Returns:
            Combined message with offer appended
        """
        # Natural transition between response and offer
        transition = "\n\n"
        return f"{base_response.rstrip()}{transition}{offer.offer_message}"

    def format_acceptance(self, workflow_type: str) -> str:
        """Generate a natural workflow start message."""
        starts = {
            "meeting": "Great! Let me help set that up.",
            "project_setup": "Let's get things organized.",
            "status_check": "Let me pull that up for you.",
            "standup": "Let's do a quick standup.",
            "review": "I'll help coordinate that.",
            "priority_check": "Let me take a look at what you've got going on.",
            "reminder": "I'll keep track of that for you.",
        }
        return starts.get(workflow_type, "Let me help with that.")

    def format_decline(self, offer: WorkflowOffer) -> str:
        """Generate a graceful decline acknowledgment."""
        return offer.decline_message
