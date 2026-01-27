# Memo: ADR-049/050 Implementation Guidance Response

**From**: Chief Architect
**To**: Lead Developer
**CC**: PM (xian), PPM
**Date**: January 26, 2026
**Re**: Response to ADR-049 and ADR-050 Questions

---

## Executive Summary

ADR-049 is **MVP work—implement now**. ADR-050 Phases 1-3 are **V2—defer correctly**. #427 cannot close with 2/4 criteria because ADR-049 implementation is required for MVP.

---

## MVP vs. V2 Rubric

Before answering your specific questions, here's the rubric we established (with PPM) for what constitutes MVP vs. V2:

| Question | MVP (do now) | V2 (defer) |
|----------|--------------|------------|
| Does user notice the gap? | Yes—feels broken | No—graceful degradation |
| Schema or implementation? | Schema/models | Full implementation |
| Single-user or multi-party? | Single-user | Multi-party |
| Core loop or enhancement? | Core loop | Enhancements |

**Key principle**: Schema work is MVP. Implementation depth is negotiable.

---

## Decision: ADR-049 (Two-Tier Intent Architecture)

### Status: APPROVED

### Priority: MVP (P1) — Implement Now

### Rationale

User notices when onboarding derails. This is a **broken experience**, not graceful degradation. The rubric is clear: if the user notices the gap and it feels broken, it's MVP.

The pattern is already proven in PortfolioOnboardingManager. The work is generalizing it to cover:
- Portfolio onboarding (exists)
- Standup sessions
- Planning sessions
- Feedback sessions
- Pending clarifications

### Scope Guidance

For MVP, focus on the flows that alpha users will actually hit:
1. **Portfolio onboarding** - already working
2. **Standup sessions** - verify protection exists or add it
3. **Pending clarifications** - Piper asked a question, user responds

Planning and feedback sessions can wait until those features are more fully developed.

### Implementation Notes

- Update ADR-049 status to ACCEPTED
- The singleton manager pattern is appropriate
- Tier 1 check happens at start of `process_intent()` before any classification
- Process priority order per ADR is correct

---

## Decision: ADR-050 (Conversation-as-Graph)

### Phase 0 (Schema Design): ✅ Complete

No action needed.

### `parent_id` Threading: CONDITIONAL

Apply the migration **IF Slack integration needs it**. Don't apply speculatively.

If you're working on Slack threading and need `parent_id`, apply it then. Otherwise, leave it.

### Phases 1-3: V2 (DEFER)

Full implementation is post-MVP:
- Multi-view projections (timeline, tasks, decisions, questions)
- WhisperNode for private AI suggestions
- Advanced reference resolution ("that meeting from last week")

These are multi-party and sophisticated enhancement features. Single-user alpha doesn't need them.

**Reference resolution failure mode**: User can re-specify. This is graceful degradation, not broken experience.

### Ted's POC

Backlog. Reference material when we get to V2. No urgent extraction needed.

---

## Decision: #427 Closure

### Cannot Close with 2/4 Criteria

The criterion "Active process not derailed by re-classification" maps to ADR-049, which is MVP work.

**Options**:

1. **Implement ADR-049 and complete #427** (recommended)
   - ADR-049 implementation is bounded work
   - Closes #427 properly with 3/4 or 4/4

2. **Split #427**
   - Close current #427 with 2/4 + explicit "remaining work in #687"
   - #687 becomes the MVP issue for ADR-049
   - Less clean but acceptable if you need the closure for tracking

I recommend Option 1. The work is bounded, the pattern exists, and it's MVP.

---

## Decision: Roadmap Placement

| Issue | Placement | Rationale |
|-------|-----------|-----------|
| #687 (ADR-049 impl) | **Current sprint (MVP)** | User notices gap—MVP work |
| #688 (ADR-050 P1-3) | **V2** | Multi-party, advanced features |

#687 was incorrectly classified as V2. It's MVP. Promote it.

---

## Summary of Actions

| Item | Action | Owner |
|------|--------|-------|
| ADR-049 | Update status to ACCEPTED | Lead Dev |
| ADR-049 | Implement generalized two-tier intent | Lead Dev |
| #687 | Promote to current sprint | Lead Dev |
| #427 | Complete with ADR-049 implementation | Lead Dev |
| ADR-050 P1-3 | Defer to V2 | - |
| #688 | Keep in V2 backlog | - |

---

## Wiring Gap Memo (Acknowledgment)

Your wiring gap methodology memo is valuable. The pattern (services with tests but unreachable by users) should be:
- Added to the anti-pattern index
- Incorporated as a vertical slice checklist in development practice

No formal response needed—this is good methodology capture.

---

*Let me know if you have questions on any of these decisions.*
