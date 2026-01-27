# Memo: PPM Response — ADR-049/050 Implementation Guidance

**From**: Principal Product Manager (PPM)
**To**: Lead Developer
**CC**: Chief Architect, PM (xian)
**Date**: January 26, 2026
**Re**: Response to ADR-049/050 Guidance Request

---

## Executive Summary

Both ADRs address real architectural needs. ADR-049 should be **approved and prioritized P1**. ADR-050 should proceed **incrementally**, with Phase 1 pulled forward only when a concrete use case demands it. **Close #427** with 2/4 criteria met; remaining work properly tracked.

---

## ADR-049: Two-Tier Intent Architecture

### Verdict: APPROVE

The problem is real: active conversational processes get derailed by re-classification. The solution (check for active context before classification) is architecturally sound.

### Answers to Questions

| Question | PPM Guidance |
|----------|--------------|
| **1. Approval** | Yes, approve. The pattern exists and works (PortfolioOnboardingManager). ADR-049 formalizes and generalizes it. |
| **2. Scope** | Yes, generalize. Cover all "active processes": onboarding, standup, planning, feedback, pending clarifications. Don't special-case each one separately. |
| **3. Priority** | **P1** (next sprint, not immediate). Rationale: Alpha testing proceeds; this is an edge case that's annoying but not blocking. Address before Beta. |
| **4. Alternative approaches** | ADR is correct to reject "better classification." This is architectural (process state), not classification accuracy. The intent classifier shouldn't need to know about every possible process state. |

### Implementation Notes

The generalized pattern should:
1. Define a `ConversationalProcess` protocol (or base class)
2. Maintain a registry of active processes per user/session
3. Check registry **before** `IntentClassifier.classify()`
4. Allow processes to "claim" certain inputs or return control to general classification

This is the "two-tier" architecture: **process tier first, intent tier second**.

---

## ADR-050: Conversation-as-Graph Model

### Verdict: PROCEED INCREMENTALLY

ADR-050 is accepted and Phase 0 (schema) is complete. Phases 1-3 represent substantial investment. Don't rush.

### Answers to Questions

| Question | PPM Guidance |
|----------|--------------|
| **1. Phase 1 timing** | Apply migration **when we have a concrete use case**, not speculatively. Likely trigger: Slack threading or explicit reference resolution work. |
| **2. Incremental vs big-bang** | **Incremental**. Phase 1 when needed, not before. The schema exists; we're not losing anything by waiting. |
| **3. Relationship to PDR-101** | PDR-101 is the vision document. ADR-050 is architectural implementation. They're connected, but ADR-050 can proceed phase-by-phase without full PDR-101 implementation. Don't block on PDR-101. |
| **4. Ted Nadeau POC** | **Lower priority** than current MUX work. It's a reference for future multi-party support, not immediate alpha needs. Schedule extraction when we actually start Phase 2 (Host Mode). |

### Phase Trigger Guidance

| Phase | Trigger | Likely Timing |
|-------|---------|---------------|
| Phase 1 (Participant Mode) | Slack thread structure needed, OR explicit reference resolution work | Pull forward if needed |
| Phase 2 (Host Mode) | Multi-view projections required | Beta+ |
| Phase 3 (Personal Agents) | Multi-party conversations | Post-Beta |

---

## #427 Closure

### Verdict: APPROVE CLOSURE

**Close #427 with 2/4 criteria met.** The remaining criteria have explicit architectural dependencies now tracked in #687 and #688. This is correct methodology.

| Criterion | Status | Notes |
|-----------|--------|-------|
| Multi-intent parsing | ✅ Complete | Works |
| Temporal follow-ups | ✅ Complete | Works |
| Active process not derailed | ⬜ Deferred | → #687 (ADR-049) |
| Reference resolution | ⬜ Deferred | → #688 (ADR-050 P1+) |

**Rationale**: 50% completion with proper tracking > 100% completion that blocks other work indefinitely. The deferred items are real dependencies, not scope creep.

---

## Roadmap Placement

| Issue | Priority | Placement | Rationale |
|-------|----------|-----------|-----------|
| **#687** (ADR-049 impl) | P1 | Next sprint | Affects UX quality; should be done before Beta |
| **#688** (ADR-050 P1-3) | P2 | Advanced layer | Pull forward Phase 1 only if specific need arises |

### Inchworm Position

Current: MUX-IMPLEMENT P3 completing
Next: MUX-IMPLEMENT P4 (Accessibility/Polish) → then #687 → then MUX-GATE assessment

#688 is not on the immediate inchworm path. It's catalogued for when we need it.

### Phasing Philosophy

**Foundation vs. Advanced Layer** (not "V1 vs V2"):

The object model doesn't change—we use more of it over time. MVP = foundation operational for single-user. Advanced = multi-party, sophisticated projections, deep memory.

| Foundation (MVP) | Advanced Layer (Post-MVP) |
|------------------|---------------------------|
| Schema/models in place | Full implementation depth |
| Single-user coherent | Multi-party operational |
| User notices gaps = fix now | Graceful degradation OK |
| Core loop works | Sophistication enhancements |

ADR-050 is a perfect example: Phase 0 (schema) is foundation. Phases 1-3 are increasing utilization of that same schema.

---

## Chief Architect Input Requested

This memo provides PPM product guidance. Chief Architect should confirm:

1. ADR-049 architectural approach (process registry pattern)
2. ADR-050 Phase 1 migration readiness
3. Any technical concerns with the incremental approach

---

## Summary

| Item | Decision |
|------|----------|
| ADR-049 | **Approve**, P1 priority, generalize to all active processes |
| ADR-050 | **Proceed incrementally**, Phase 1 when triggered by concrete need |
| #427 | **Close** with 2/4, remaining tracked in #687/#688 |
| #687 | Next sprint (P1) |
| #688 | Future roadmap (P2), pull forward Phase 1 if needed |

---

*Filed: 2026-01-26 2:00 PM PT*
*Re: Lead Developer Memo 2026-01-25*
