# Memo: Conversational Glue — Chief Architect Review Request

**To**: Chief Architect
**From**: PPM
**Date**: February 1, 2026
**Re**: Technical and Architecture Requirements for Conversational Glue

---

## Summary

External research on conversational AI best practices has been synthesized into implementation requirements. Gap analysis identifies 19 requirements with significant gaps against current Piper Morgan state.

**Your review is needed on technical feasibility and architecture alignment before M0 sprint begins.**

---

## Documents Attached

1. **conversational-glue-implementation-guide.md** — Full reference (see sections below)
2. **conversational-glue-gap-analysis.md** — Full gap analysis (read in full)

---

## What to Review

### In Implementation Guide

| Section | Focus |
|---------|-------|
| **Section 9: Technical Requirements** | Capability gaps in intent classification, conversation state, response generation, workflow engine |
| **Section 11: Architecture Requirements** | New/extended data models, service interfaces, integration points |

### In Gap Analysis

The full gap matrix with effort estimates. Key tables:
- P0 gaps (15-25 days) — MVP critical
- P1 gaps (20-32 days) — MVP important
- Existing issues to link/update

---

## Key Architecture Questions

1. **Confidence Scoring**: Pre-classifier currently returns binary match. Adding numeric confidence (0-1) requires changes to `pre_classifier.py` and downstream. Feasible in M0 timeframe?

2. **Multi-Intent Extension**: `IntentClassificationResult` needs to support `List[Intent]`. What's the impact on existing handlers that expect single intent?

3. **Conversation Context Service**: New service proposed:
   ```python
   class ConversationContextService:
       async def get_context(session_id) -> ConversationContext
       async def extract_entities(message, context) -> List[Entity]
       async def resolve_reference(reference, context) -> Entity
       async def detect_topic_shift(message, context) -> TopicShiftResult
   ```
   Does this align with existing architecture, or does it overlap with something already built?

4. **Memory Hierarchy**: Implementation guide proposes 3-tier memory (short-term verbatim, medium-term summarized, long-term extracted). ADR-054 designed this but implementation status unclear. What's actually built?

5. **Trust-Proactivity Wiring**: ADR-053 computed trust (453 tests). What's required to wire trust level into response generation?

---

## Existing Work to Verify

| Issue | Question |
|-------|----------|
| #427 MUX-IMPLEMENT-CONVERSE-MODEL | Does Phase 2 (follow-ups) cover GLUE-FOLLOWUP requirements? |
| #595 Multi-intent handling | Current status? Can we build on it or start fresh? |
| Pattern-011 Context Resolution | How complete is anaphoric resolution? |

---

## Proposed Data Models

From implementation guide Section 11:

```python
class ConversationContext:
    session_id: str
    current_topic: Optional[str]
    current_lens: Optional[str]  # What aspect user is asking about
    extracted_entities: List[Entity]
    recent_turns: List[Turn]
    parked_workflows: List[WorkflowState]
    detected_tone: ToneSignal

class Entity:
    type: EntityType  # PROJECT, PERSON, MEETING, ISSUE, etc.
    value: str
    reference_id: Optional[str]  # Link to actual object
    first_mentioned: datetime
    last_mentioned: datetime

class IntentClassificationResult:
    intents: List[Intent]  # Changed from single
    confidence: float
    requires_clarification: bool
```

**Question**: Do these conflict with existing models, or can they extend what's there?

---

## Timeline

- **M0 Sprint**: Starting now (15-25 days)
- **Your feedback needed**: Before implementation begins
- **Key dependency**: Architecture decisions on confidence scoring and multi-intent

---

## No Action Required On

- UX/voice/personality (CXO reviewing)
- Product prioritization (PPM domain)
- Issue creation (drafts ready)

---

*Please reply with technical assessment or flag architectural concerns.*
