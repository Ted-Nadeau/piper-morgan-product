# Memo: Orientation System Architecture Decision

**From**: Chief Architect
**To**: Lead Developer
**CC**: PM (xian), PPM, CXO
**Date**: January 23, 2026
**Re**: #410 MUX-INTERACT-CANONICAL-ENHANCE - Architectural Guidance
**Priority**: High (unblocking)

---

## Summary

Build **Option A structure with Option D framing**. Orientation is "Piper perceiving the current Situation through multiple lenses"—that's the grammar in action. No complex infrastructure needed; the alignment comes from how we think about and document it.

---

## Decision: Modified Option D (Grammar-Aware but Pragmatic)

### The Key Insight

Orientation IS a composite Perception in our grammar. The five pillars map directly to our lens infrastructure:

| Pillar | Grammar Mapping | Lens | Source |
|--------|-----------------|------|--------|
| Identity | Entity (Piper as perceiver) | Self-awareness | Static + relationship context |
| Temporal | Moment timing | Temporal | ConsciousnessContext + calendar |
| Spatial | Place context | Contextual | PlaceDetector + SpatialIntentContext |
| Agency | Priority perception | Priority | UserContext.priorities |
| Prediction | Anticipation | Causal (anticipating mode) | Capability awareness |

**Orientation is not a new bounded context.** It's Piper applying multiple lenses to perceive the current Situation.

---

## Recommended Implementation

### Location

`services/mux/orientation.py` — Part of MUX/consciousness domain, not a new bounded context.

### Structure

```python
# services/mux/orientation.py

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class OrientationPillarType(Enum):
    IDENTITY = "identity"
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    AGENCY = "agency"
    PREDICTION = "prediction"

@dataclass
class OrientationPillar:
    """
    A single pillar of Piper's orientation - a perception through one lens.

    Grammar alignment: Each pillar is Piper perceiving one aspect
    of the current Situation.
    """
    pillar_type: OrientationPillarType
    lens_applied: str  # Which lens produced this perception
    perception: str    # What Piper perceives
    confidence: float
    source_context: str  # Where this came from (for debugging/audit)

@dataclass
class OrientationState:
    """
    Piper's composite perception of the current Situation.

    Grammar alignment: This is how Piper (Entity) perceives the
    current Situation through multiple lenses simultaneously.
    The five pillars are five lenses applied in parallel.

    See: ADR-055 (Object Model), consciousness-philosophy.md
    """
    identity: OrientationPillar      # Lens: self-awareness
    temporal: OrientationPillar      # Lens: temporal
    spatial: OrientationPillar       # Lens: contextual + place
    agency: OrientationPillar        # Lens: priority
    prediction: OrientationPillar    # Lens: causal (anticipating)

    situation_frame: Optional[str] = None  # The Situation being perceived
    trust_context: Optional["TrustContext"] = None  # From ProactivityGate

    @classmethod
    def gather(
        cls,
        user_context: "UserContext",
        consciousness_context: "ConsciousnessContext",
        place: "PlaceType",
        spatial_context: Optional["SpatialIntentContext"] = None,
        trust_context: Optional["TrustContext"] = None
    ) -> "OrientationState":
        """
        Gather orientation by applying lenses to available context.

        This is the grammar in action: Piper perceives the Situation
        through multiple lenses to understand where it is.
        """
        return cls(
            identity=cls._perceive_identity(),
            temporal=cls._perceive_temporal(consciousness_context),
            spatial=cls._perceive_spatial(place, spatial_context),
            agency=cls._perceive_agency(user_context),
            prediction=cls._perceive_prediction(user_context),
            trust_context=trust_context
        )

    @staticmethod
    def _perceive_identity() -> OrientationPillar:
        """Identity pillar - who Piper is in this context."""
        ...

    # ... other _perceive_* methods
```

### Why This Works

| Concern | How Addressed |
|---------|---------------|
| Simple to implement now | Structurally identical to Option A |
| Grammar-aligned | Framing, naming, docstrings make connection explicit |
| No rewrite needed later | This IS the reference implementation of composite perception |
| Uses existing systems | Gathers from PlaceDetector, ConsciousnessContext, UserContext |
| No duplication | Orientation is derived/computed, not a new source of truth |

---

## Answers to Your Specific Questions

### Q1: Bounded Context?

**Answer**: Orientation belongs in the **MUX/consciousness domain**, not as a new bounded context.

Rationale: Orientation is how Piper perceives—it's part of consciousness, not a separate concern. Location `services/mux/orientation.py` keeps it with related MUX infrastructure.

### Q2: Grammar Alignment?

**Answer**: Implement grammar-aware Option A now. No refactor needed later.

The key insight: Grammar alignment comes from **framing**, not infrastructure complexity. By naming things correctly (pillars as lenses, gather as perception) and documenting the connection to ADR-055, you're building the grammar-aligned version. When ADR-055 matures further, this becomes a reference implementation, not a legacy artifact.

### Q3: Context Proliferation?

**Answer**: Not concerned, IF orientation is clearly positioned as **derived/computed**.

The distinction:
- **Source contexts** (UserContext, ConsciousnessContext): Hold authoritative data
- **Derived contexts** (OrientationState): Compute views over source contexts

OrientationState gathers and interprets; it doesn't own data. This is healthy—it's the same pattern as how lenses work over spatial dimensions.

### Q4: Integration Point?

**Answer**: Compute orientation **after place detection, before handler dispatch**.

```
Request
  → PlaceDetector
  → OrientationState.gather()    ← HERE
  → IntentClassifier
  → Handler
```

Orientation informs:
1. **Classification**: What Piper thinks you're asking (context for intent)
2. **Response framing**: How Piper should communicate (consciousness context)

The handler receives `OrientationState` and uses it for both recognition-based suggestions and response generation.

---

## Trust Integration

Since trust computation (#413) is complete and PM wants trust-aware surfacing integrated into #410:

Include `trust_context` in OrientationState as shown above. This allows orientation-informed responses to respect trust thresholds from ProactivityGate. The prediction pillar (what Piper can offer) should be filtered through trust levels.

---

## Implementation Guidance

### Do

- Frame OrientationState as "Piper perceiving the Situation"
- Use lens vocabulary in docstrings and comments
- Gather from existing systems; don't duplicate data
- Include trust_context for proactivity gating
- Write the "experience" paragraph at implementation checkpoint

### Don't

- Create a new bounded context or service layer
- Duplicate data that exists in UserContext or ConsciousnessContext
- Over-engineer the gather() method—start simple
- Forget to document the grammar connection

### The "Experience" Check

After implementation, verify: Does OrientationState help Piper **experience** where it is, or does it just **store** location data?

If the answer is "experience"—Piper perceives through lenses, understands the Situation, forms awareness—you've got it right.

---

## Summary

| Question | Answer |
|----------|--------|
| Which option? | Modified D: Option A structure + Option D framing |
| Bounded context? | No—part of MUX/consciousness domain |
| Location? | `services/mux/orientation.py` |
| Grammar alignment? | Yes, through framing and documentation |
| Integration point? | After PlaceDetector, before IntentClassifier |
| Trust integration? | Include trust_context field |

This should unblock #410. The architecture is sound—proceed with implementation.

---

*Filed: January 23, 2026, 5:24 PM PT*
