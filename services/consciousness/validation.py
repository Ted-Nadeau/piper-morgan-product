"""
Minimum Viable Consciousness (MVC) Validation

Validates that output meets the four MVC requirements:
1. Identity Voice - has "I" statement
2. Epistemic Humility - has uncertainty/hedge
3. Dialogue Opening - has invitation
4. Source Transparency - has attribution

Issue: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns
"""

import re
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class MVCResult:
    """Result of MVC validation."""

    passes: bool
    checks: Dict[str, bool]
    missing: List[str]
    suggestions: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        if self.passes:
            return "MVC: PASS (4/4)"
        return f"MVC: FAIL ({4 - len(self.missing)}/4) - Missing: {', '.join(self.missing)}"


# Validation patterns
IDENTITY_PATTERN = re.compile(r"\bI\b|\bI'm\b|\bI've\b|\bI'd\b", re.IGNORECASE)

UNCERTAINTY_PATTERN = re.compile(
    r"looks like|might|seems|I think|could be|I'm not sure|probably|appears|may be|"
    r"it appears|I believe|I suspect|possibly|perhaps",
    re.IGNORECASE,
)

INVITATION_PATTERN = re.compile(
    r"how does|what do you|would you|let me know|anything|does this|do you want|"
    r"shall I|should I|want me to|\?$",
    re.IGNORECASE | re.MULTILINE,
)

ATTRIBUTION_PATTERN = re.compile(
    r"checked|looked|looking at|found|see|based on|from|in GitHub|in your calendar|"
    r"I noticed|I see|your .+ shows|according to",
    re.IGNORECASE,
)


def validate_mvc(output: str) -> MVCResult:
    """
    Validate output meets Minimum Viable Consciousness requirements.

    Args:
        output: The text output to validate

    Returns:
        MVCResult with pass/fail status and details
    """
    checks = {
        "identity": bool(IDENTITY_PATTERN.search(output)),
        "uncertainty": bool(UNCERTAINTY_PATTERN.search(output)),
        "invitation": bool(INVITATION_PATTERN.search(output)),
        "attribution": bool(ATTRIBUTION_PATTERN.search(output)),
    }

    missing = [k for k, v in checks.items() if not v]

    suggestions = []
    if "identity" in missing:
        suggestions.append("Add an 'I' statement: 'I see...', 'I found...', 'I noticed...'")
    if "uncertainty" in missing:
        suggestions.append("Add uncertainty: 'It looks like...', 'I think...', 'might...'")
    if "invitation" in missing:
        suggestions.append("Add invitation: 'How does that sound?', 'Anything to adjust?'")
    if "attribution" in missing:
        suggestions.append("Add source: 'I checked GitHub...', 'Looking at your calendar...'")

    return MVCResult(
        passes=all(checks.values()),
        checks=checks,
        missing=missing,
        suggestions=suggestions,
    )


def has_identity(output: str) -> bool:
    """Check if output has identity voice (I statements)."""
    return bool(IDENTITY_PATTERN.search(output))


def has_uncertainty(output: str) -> bool:
    """Check if output has epistemic humility (hedging)."""
    return bool(UNCERTAINTY_PATTERN.search(output))


def has_invitation(output: str) -> bool:
    """Check if output has dialogue invitation."""
    return bool(INVITATION_PATTERN.search(output))


def has_attribution(output: str) -> bool:
    """Check if output has source transparency."""
    return bool(ATTRIBUTION_PATTERN.search(output))
