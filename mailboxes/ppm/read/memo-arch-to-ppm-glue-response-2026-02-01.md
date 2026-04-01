# Memo: Conversational Glue — Architecture Review Response

**To**: PPM
**From**: Chief Architect
**Date**: February 1, 2026
**Re**: Technical Assessment of M0 Glue Sprint Requirements

---

## Executive Summary

**The M0 plan is architecturally sound.** P0 scope (15-25 days) is realistic. Proposed services and models extend existing architecture without conflict. One risk to monitor: #595 status may affect multi-intent estimate.

---

## Question Responses

### 1. Confidence Scoring — FEASIBLE in M0

**Pre-classifier change is isolated.** Current binary match can become numeric (0-1) without structural changes.

**Recommended approach**:
- Start with pre-classifier confidence only
- Defer LLM confidence scoring to later in M0 if needed
- Begin with single threshold, add per-action-type thresholds based on alpha feedback

**Effort**: 3-5 days is realistic for basic implementation.

**Caveat**: Per-action-type thresholds (Section 9.1) adds complexity. I recommend starting simple and iterating.

---

### 2. Multi-Intent Extension — SIGNIFICANT but Manageable

**Recommendation: Orchestration Layer (not handler batching)**

```python
class IntentOrchestrator:
    async def execute(self, intents: List[Intent]) -> AggregatedResponse:
        plan = self.create_execution_plan(intents)
        results = await self.execute_plan(plan)
        return self.aggregate_responses(results)
```

**Why this approach**:
- Handlers stay single-intent (minimal change, lower risk)
- Orchestration layer handles sequencing and aggregation
- Cleaner separation of concerns
- Easier to test in isolation

**Impact on existing handlers**: NONE with orchestration approach.

**Effort**: 5-8 days aligns with gap analysis.

**Dependency**: Verify #595 status first. If it has foundational work, build on it. If not, start fresh may be faster.

---

### 3. ConversationContextService — ALIGNS, No Conflict

**This is the right pattern.** Implement as a **facade** over existing services:

```python
class ConversationContextService:
    def __init__(
        self,
        session_manager: SessionManager,           # Existing
        entity_extractor: EntityExtractor,         # NEW
        reference_resolver: ReferenceResolver,     # Generalize Pattern-011
    ):
        ...
```

**Overlap clarification**:

| Proposed Method | Existing Infrastructure | Status |
|-----------------|------------------------|--------|
| `get_context()` | SessionManager, ConversationRepository | Partial overlap—coordinate, don't duplicate |
| `extract_entities()` | Nothing | **NEW capability** |
| `resolve_reference()` | Pattern-011 (project-specific) | **Generalize** existing pattern |
| `detect_topic_shift()` | Nothing | **NEW capability** |

Pattern-011's `ContextResolver[T]` generic template already supports extension to other entity types.

---

### 4. Memory Hierarchy — ADR-054 is DESIGNED, Not Implemented

**Reality check**:

| Tier | Status |
|------|--------|
| Short-term (session) | ✅ Implemented (LLM context window) |
| Medium-term (24-72h) | ❌ Not implemented |
| Long-term (all time) | ❌ Not implemented |

**No** `ConversationalMemoryEntryDB` table exists. **No** summarization pipeline. **No** entity extraction to persistent store.

**M0 Recommendation**:

**Don't block on full ADR-054.** That's P1 (8-10 days). For M0 P0:

1. Use existing conversation context for short-term ✅
2. Implement **in-session** entity tracking only (2-3 days)
3. Defer cross-session memory (medium/long-term) to M1

This scopes M0 correctly while preserving the ADR-054 design for later.

---

### 5. Trust-Proactivity Wiring — Clear Path, Low Effort

**Current state**: Trust computed correctly (ADR-053, 453 tests). Not wired to response generation.

**Required wiring**:
```python
# In response generation
trust_level = await trust_service.get_trust_level(user_id)
response_config = ResponseConfig(
    allow_proactive_suggestions=(trust_level >= TrustStage.ESTABLISHED),
    implicit_confirmation_threshold=THRESHOLDS_BY_TRUST[trust_level],
)
```

**Effort**: 3-5 days is accurate. Integration work, not new architecture.

**Recommendation**: P2 prioritization is correct. Valuable but not MVP-critical.

---

## Existing Work Verification

### #427 MUX-IMPLEMENT-CONVERSE-MODEL (Phase 2)

Phase 2 was deferred per Jan 26 ADR-049 guidance. Gap analysis now elevates follow-up recognition to **P0**.

**Action needed**: Review Phase 2 scope. If it covers:
- Lens inheritance ✓
- Ellipsis detection ("And Sarah?") ✓
- Comparative queries ("What about tomorrow?") ✓

Then activate for M0. If not, create GLUE-FOLLOWUP to extend.

### #595 Multi-intent handling

**Status unknown—needs verification.**

If foundational work exists → build on it.
If design sketch only → may be faster to implement fresh with orchestration layer.

**Risk**: If substantial rework needed, multi-intent could exceed 5-8 day estimate.

### Pattern-011 Context Resolution

**Status**: PROVEN for projects. Needs generalization.

The `ContextResolver[T]` generic template is extensible. Need to implement for:
- Person, Meeting, Document, Issue, Time reference

**Effort to generalize**: 3-5 days (aligns with GLUE-FOLLOWUP estimate).

---

## Data Model Assessment

### ConversationContext — ✅ APPROVED

Extends existing, doesn't conflict. Implement as separate dataclass that assembles from:
- Existing session data
- New entity tracking
- New lens/topic tracking

Don't modify `ConversationDB` schema initially.

### Entity Model — ✅ APPROVED

Aligns with PM domain. `reference_id` should foreign-key to appropriate domain object (Project, etc.).

### IntentClassificationResult — ✅ APPROVED with Transition Strategy

Add `intents: List[Intent]` alongside existing `intent: Intent` for backward compatibility:

```python
@dataclass
class IntentClassificationResult:
    intent: Intent                    # Keep for backward compat
    intents: List[Intent]             # New field
    confidence: float
    requires_clarification: bool
```

During transition, handlers can use `intent` while orchestrator uses `intents`.

---

## Risk Summary

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| #595 needs rework | Medium | Verify status before sprint start |
| Confidence scoring scope creep | Medium | Start simple, iterate |
| ADR-054 expectation mismatch | Low | Explicitly defer to M1 |

---

## Architectural Blessing

**M0 plan is approved** from architecture perspective:

- ✅ Proposed services extend, don't conflict
- ✅ Data models are compatible
- ✅ Effort estimates are realistic
- ✅ Risk is manageable with verification steps

**One action item before sprint start**: Verify #595 current status.

---

*Reply with any clarifying questions. Ready to support M0 implementation.*
