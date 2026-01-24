# Memo: Orientation System Architecture Decision Request

**From**: Lead Developer
**To**: Chief Architect
**CC**: PPM, CXO (at your discretion)
**Date**: 2026-01-23
**Re**: #410 MUX-INTERACT-CANONICAL-ENHANCE - Architectural question
**Response-Requested**: yes
**Priority**: High (blocking implementation)

---

## Summary

I'm implementing #410 (Evolve canonical queries to orientation system) and have reached an architectural decision point that requires your input. The question is whether OrientationState should be a new bounded context or should compose from/extend existing context systems.

---

## Background

### The Goal
Transform the five canonical query categories (Identity, Temporal, Status, Priority, Guidance) from reactive handlers into Piper's **orientation system** - an internal model Piper uses to understand "where it is" before responding. This enables recognition-based interaction (Nielsen's articulation barrier research: users recognize options rather than recall queries).

### The Five Orientation Pillars (from consciousness-philosophy.md)
1. **Identity**: "I'm Piper, your..."
2. **Temporal**: "Right now it's..."
3. **Spatial**: "You're working on..."
4. **Agency/Priority**: "Your focus seems to be..."
5. **Prediction/Guidance**: "I can help with..."

---

## Existing Context Systems I've Found

| System | Location | What It Holds |
|--------|----------|---------------|
| `UserContext` | `services/user_context_service.py` | user_id, organization, projects, priorities, preferences |
| `ConsciousnessContext` | `services/consciousness/context.py` | time_of_day, is_first_interaction, meeting_load, has_calendar_data, etc. |
| `IntentClassificationContext` | `services/intent_service/intent_types.py` | Classification-specific context |
| `SpatialIntentContext` | `services/intent_service/spatial_intent_classifier.py` | Spatial awareness for intent |
| `PlaceDetector` | `services/intent_service/place_detector.py` | Determines PlaceType (SLACK_DM, WEB_CHAT, etc.) |
| `OwnershipCategory` | `services/mux/ownership.py` | NATIVE/FEDERATED/SYNTHETIC knowledge relationship |

### Current Canonical Handler Context Usage
Canonical handlers currently:
- Import `user_context_service`
- Access `intent.spatial_context` when available
- Don't have unified orientation awareness

---

## The Architectural Options

### Option A: New Standalone OrientationState
Create `services/intent_service/orientation.py` with:
- `OrientationPillar` enum
- `OrientationState` dataclass
- `OrientationService` that **gathers** from existing systems

```python
@dataclass
class OrientationState:
    identity: PillarState      # from IDENTITY handler
    temporal: PillarState      # from UserContext + ConsciousnessContext
    spatial: PillarState       # from PlaceDetector + SpatialIntentContext
    agency: PillarState        # from UserContext.priorities
    prediction: PillarState    # from GUIDANCE handler capabilities
```

**Pros**: Clean separation, explicit five-pillar model, doesn't modify existing systems
**Cons**: Yet another context object, potential duplication, not aligned with grammar

### Option B: Extend UserContext
Add orientation pillars to existing `UserContext`:

```python
@dataclass
class UserContext:
    # Existing
    user_id: UUID
    projects: list
    priorities: list
    preferences: dict

    # New: Orientation Pillars
    orientation: Optional[OrientationState] = None
```

**Pros**: Single source of user context, less proliferation
**Cons**: Couples orientation to user-specific data, UserContext is already doing a lot

### Option C: Extend ConsciousnessContext
Add orientation pillars to existing `ConsciousnessContext`:

```python
@dataclass
class ConsciousnessContext:
    # Existing situational context...

    # New: Orientation Pillars
    orientation: Optional[OrientationState] = None
```

**Pros**: Aligns with consciousness philosophy, already used for response framing
**Cons**: ConsciousnessContext is currently situational, not identity-focused

### Option D: Grammar-Aligned Approach
Per ADR-055 and the grammar "Entities experience Moments in Places":
- Orientation is how **Piper (Entity)** perceives its current **Situation (Moment frame)** in the current **Place**
- Should use existing `Perception` infrastructure from ADR-055
- Orientation becomes a `PerceptionMode` or lens over existing data

```python
# Orientation as perception through the existing grammar
class OrientationPerception:
    """Piper's orientation is a Perception of the current Situation."""
    entity: EntityProtocol  # Piper
    situation: Situation     # Current frame
    place: PlaceProtocol     # Current context

    def perceive_orientation(self) -> OrientationState:
        # Uses existing infrastructure
```

**Pros**: Aligns with grammar, uses existing ADR-055 infrastructure, philosophically coherent
**Cons**: More complex, may require understanding ADR-055 deeply first

---

## My Preliminary Lean

I'm inclined toward **Option A** (standalone) for simplicity, with awareness of **Option D** (grammar-aligned) as the "right" long-term answer. But I don't want to create infrastructure that will need to be rewritten to align with the grammar later.

---

## Questions for Chief Architect

1. **Bounded Context**: Is "orientation" a new bounded context, or does it belong within an existing one (consciousness? user context? mux grammar)?

2. **Grammar Alignment**: Should I implement Option D now to align with ADR-055, or is Option A acceptable as a stepping stone with documented intention to refactor?

3. **Context Proliferation**: Are you concerned about the number of context objects? Should we consolidate?

4. **Integration Point**: Where should orientation computation be called in the intent processing pipeline?

---

## Additional Context

- Trust computation (#413) is now complete with `ProactivityGate` - PM has decided to integrate trust-aware surfacing in #410 rather than defer
- #411 (Recognition) and #412 (Intent-Bridge) depend on this orientation system
- The CXO is being consulted separately on the experience design implications

---

## Timeline

This is blocking #410 execution. A brief response with your architectural guidance would unblock implementation.

---

_Lead Developer_
_2026-01-23 ~5:00 PM_
