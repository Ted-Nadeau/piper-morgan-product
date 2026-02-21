"""
Unified formality framework (#838).

Provides the shared formality scale and mapping functions per Chief Architect
design decision (2026-02-21). All tone/formality systems converge on a
continuous warmth scale (0.0 = professional, 1.0 = warm) with three
presentation labels.

See: mailboxes/arch/inbox/2026-02-18-unified-formality-system-memo.md
"""

from typing import Dict

# Warmth scale: 0.0 (professional) → 1.0 (warm)
# This matches PersonalityProfile.warmth_level and OnboardingGrammarContext.warmth_level.

DEFAULT_WARMTH = 0.5  # Balanced — used when no user preference is set

# Maximum context adjustment (±0.2) per architect decision
MAX_CONTEXT_ADJUSTMENT = 0.2

# Onboarding tier → warmth level mapping
ONBOARDING_TIER_TO_WARMTH: Dict[str, float] = {
    "warm": 0.8,
    "conversational": 0.5,
    "professional": 0.2,
}


def formality_label(warmth: float) -> str:
    """Map warmth level to presentation label.

    Args:
        warmth: Warmth level (0.0 = professional, 1.0 = warm)

    Returns:
        "warm", "balanced", or "professional"
    """
    if warmth >= 0.67:
        return "warm"
    elif warmth >= 0.33:
        return "balanced"
    else:
        return "professional"


def apply_context_adjustment(baseline: float, adjustment: float) -> float:
    """Apply context adjustment to baseline, clamped to ±MAX_CONTEXT_ADJUSTMENT.

    Args:
        baseline: User's warmth baseline (0.0-1.0)
        adjustment: Context modifier (positive = warmer, negative = cooler)

    Returns:
        Adjusted warmth, clamped to [0.0, 1.0]
    """
    clamped_adjustment = max(-MAX_CONTEXT_ADJUSTMENT, min(MAX_CONTEXT_ADJUSTMENT, adjustment))
    return max(0.0, min(1.0, baseline + clamped_adjustment))
