# Memo: Architectural Decisions on Grammar Transformation and Conversational Glue

**From**: Chief Architect
**To**: Lead Developer
**CC**: PM (xian), CXO, PPM
**Date**: January 21, 2026
**Re**: Response to Grammar Transformation Placement (Jan 20) and LLM Layer Scheduling (Jan 21)

---

## Summary

This memo responds to your two recent questions with architectural decisions and provides accompanying artifacts for implementation.

---

## Decision 1: Grammar Transformation Issues Placement

**Your Question**: How should #619-627 (grammar compliance transformations) be organized?

**Decision**: Modified Option D (Hybrid with phase alignment)

| Priority | Issues | Placement | Rationale |
|----------|--------|-----------|-----------|
| Critical (4) | #619-622 | **MUX-V2** (explicit work) | Touch every user interaction |
| Important (5) | #623-627 | **Quality gates** (opportunistic) | Can wait for natural touch points |

### Why Not the Other Options?

- **Option A (Pure quality gates)**: Critical features like Intent Classification (#619) touch EVERY message. Can't wait for "reasons to touch it."
- **Option B (Dedicated epic)**: Creates unnecessary coordination overhead. MUX-V2 is already the integration phase.
- **Option C (Attach to MUX-VISION)**: MUX-VISION is conceptual foundation. Mixing in application work blurs phase boundaries. V1 is complete—let it stay clean.

### Action Items

1. **Create parent issue**: `GRAMMAR-COMPLIANCE: Feature Transformation Tracking` (attached)
2. **Link Critical issues to MUX-V2 milestone**
3. **Add "quality-gate" label to Important issues** for opportunistic tracking

---

## Decision 2: #595 Multi-Intent Fix

**Your Question**: Fix now (Option C, 6-8h) or wait for #427?

**Decision**: Option C—implement proper multi-intent parsing now.

### Reasoning

The key question is: Does this create technical debt, or advance toward target architecture?

**Answer**: It advances.

#427 (Unified Conversation Model) needs three components:
1. Multi-intent **detection** (decomposition)
2. Strategy **selection** (handle all, chain, or clarify)
3. **Execution**

If you implement proper multi-intent parsing now with a simple "handle all" strategy:
- The detection/decomposition logic is **reusable**—#427 needs it regardless
- Only strategy selection becomes more sophisticated later
- This is **advancement toward architecture**, not throwaway work

**Verdict**: 6-8h invested now accelerates #427 later. Alpha UX improves immediately.

**Sprint placement**: Can stay in X1 (MUX-TECH) or move to X2—your call based on bandwidth.

---

## Decision 3: Conversational Glue

**Your Question**: Where is conversational glue planned?

**Decision**: Gap exists. Filing planning issue `MUX-INTERACT-GLUE` (attached).

### The Gap

| Component | Current Coverage |
|-----------|-----------------|
| Context carry-over | ADR-024 (infrastructure exists) |
| Process-level context | ADR-049 (infrastructure exists) |
| Graph structure | ADR-050 (infrastructure exists) |
| **Topic transitions** | **Not planned** |
| **Acknowledgment patterns** | **Not planned** |
| **Conversational repair** | **Not planned** |

We have infrastructure (ADRs 024, 049, 050, 054, 055). We lack **interaction design**—how that infrastructure manifests in user experience.

### Placement

- **Phase**: MUX-INTERACT (4.4)
- **Sequence**: Complete before #427 (MUX-IMPLEMENT-CONVERSE-MODEL) begins
- **Nature**: Design/planning work, not implementation

The attached issue scopes the design questions and deliverables.

---

## Artifacts Attached

| Document | Purpose |
|----------|---------|
| `issue-grammar-compliance-parent.md` | Parent tracking issue for #619-627 |
| `issue-mux-interact-glue.md` | Planning issue for conversational glue design |

---

## Summary

| Question | Decision |
|----------|----------|
| Grammar transformation placement | Critical 4 → MUX-V2; Important 5 → quality gates |
| #595 multi-intent fix | Option C (proper fix, 6-8h)—advances architecture |
| Conversational glue | Gap exists; MUX-INTERACT-GLUE filed |

Good instinct surfacing these questions. The transformation work and the glue work are both real architectural concerns that needed explicit decisions.

---

*Filed: January 21, 2026, 8:10 AM PT*
