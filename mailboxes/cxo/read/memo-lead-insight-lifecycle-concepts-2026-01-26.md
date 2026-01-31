# Memo: Insight Lifecycle - Conceptual Questions

**From**: Lead Developer
**To**: PPM, CXO
**Date**: 2026-01-26
**Re**: Unresolved conceptual questions about Insight model lifecycle
**Related Issues**: #703 MUX-LIFECYCLE-UI, #685 MUX-LIFECYCLE-OBJECTS

---

## Context

As part of #703 MUX-LIFECYCLE-UI work, we completed a fresh analysis of which domain models have lifecycle infrastructure. This revealed a fundamental question about the Insight model that needs architectural guidance.

## Current State

### Models with Lifecycle Infrastructure

| Model | lifecycle_state | to_dict() wired | Status |
|-------|-----------------|-----------------|--------|
| WorkItem | Yes | Yes (#685) | Ready for UI |
| Feature | Yes | Yes (#705) | Ready for UI |
| Insight | No | N/A | **Needs decision** |

### The Insight Model Today

```python
# services/mux/composting_models.py
@dataclass
class Insight:
    content: str
    confidence: float  # 0.0-1.0
    evidence_sources: List[str]
    created_at: datetime
    # No lifecycle_state field
```

## The Conceptual Question

**Should Insights have their own lifecycle states?**

### Option A: Insights as "Composted Output"

Insights are the **output** of the composting process. They don't evolve through states—they emerge fully formed from composting. In this view:

- Insights are inherently "composted" (they are the result of composting)
- They don't need their own lifecycle—they **are** a lifecycle stage
- Adding lifecycle to insights would be circular (composted thing → composted state?)

**Analogy**: Insights are like photographs—snapshots that capture a moment, not objects that evolve.

### Option B: Insights as First-Class Entities

Insights could be treated as entities that evolve:

- EMERGENT: New insight generated
- NOTICED: Insight surfaced to user
- RATIFIED: User confirmed insight is valuable
- DEPRECATED: Insight no longer relevant
- COMPOSTED: Insight itself gets composted into meta-insights

**Analogy**: Insights are like documents—they can be draft, published, archived.

### Option C: Insights as "Lens Artifacts"

PM suggested this framing: Insights might be "the particle lens on what is otherwise a wave."

In this view:
- Insights are temporary crystallizations of continuous knowledge
- They don't persist as entities—they're windows into understanding
- The question isn't "where do insights live" but "when do we look through the lens"

**Analogy**: Insights are like measurements in quantum mechanics—they don't exist until observed.

## Technical Implications

### If Option A (No lifecycle)
- Insights remain as-is
- UI shows insights without lifecycle indicators
- Composting pipeline stays simple
- **Deferrable**: No code changes needed

### If Option B (Full lifecycle)
- Add lifecycle_state to Insight model
- Implement state transitions (who triggers them?)
- Need to define what causes transitions
- **Significant work**: Model changes + UI + business logic

### If Option C (Lens artifacts)
- Insights may be ephemeral (not persisted long-term)
- UI shows them differently (not as "objects" but as "views")
- May need different visualization approach
- **Rethink required**: Changes to how we think about insights, not just code

## Our Recommendation

**Start with Option A for MVP**, leaving the door open for Option B or C later.

Rationale:
1. WorkItem and Feature lifecycle covers the core MVP use case
2. Insights don't currently need lifecycle for any user-facing feature
3. The conceptual model isn't settled—better to defer than encode the wrong model
4. Option A is the simplest implementation (do nothing)

## Questions for PPM/CXO

1. **Does the "composted output" framing resonate?** Or should insights be treated as entities that evolve?

2. **What user experience would lifecycle indicators on insights serve?** Currently users don't interact with insights in ways that would benefit from lifecycle visibility.

3. **Is the "lens artifact" framing worth pursuing?** This might lead us to a different UI treatment entirely (not lifecycle indicators, but something else).

4. **Can we defer this decision?** We'd track it in #703 as "Phase 3: Future" and revisit when we have concrete user needs.

---

## Session Progress

This memo follows completion of:
- #705 MUX-LIFECYCLE-UI-B (Feature.to_dict) - COMPLETE
- #704 MUX-LIFECYCLE-UI-A (Morning Standup) - BLOCKED (STOP condition: standup doesn't render WorkItems)

The #704 STOP condition is a separate issue—see GitHub comment for details.

---

*Lead Developer, 2026-01-26*
