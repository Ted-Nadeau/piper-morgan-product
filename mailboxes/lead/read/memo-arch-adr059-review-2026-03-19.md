# Memo: Architectural Review — ADR-059 Workflow Dispatcher

**To**: Lead Developer
**CC**: PM (xian)
**From**: Chief Architect
**Date**: 2026-03-19
**Re**: Review of ADR-059 — Workflow Dispatcher and Offer System Consolidation
**Status**: APPROVED with guidance on three questions

---

## Overall Assessment

This is a clean ADR that correctly diagnoses a real structural problem. Three independent offer/acceptance systems racing for control of user affirmations is exactly the kind of composition bug that Pattern-062 (Assembly Assumption) predicts — each system works correctly in isolation, the composition produces a broken experience. The #922 bug is the symptom; the lack of a unified dispatch point is the cause.

The three-part approach (remove onboarding, add dispatcher, reconcile offer types) is correctly sequenced: simplify first, then structure, then consolidate. Gall's Law is the right reference. The PM's instinct to remove onboarding rather than fix it within a broken architecture is sound — you can't debug a race condition by making one of the racers faster.

The ADR is approved. Here's my guidance on the three questions, plus a few implementation notes.

---

## Question 1: New Component or Fold into WorkflowOfferService?

**Answer: New component. Your recommendation is correct.**

The reasoning is separation of concerns, and you already articulated it well: `WorkflowOfferService` handles offer *presentation* (should I offer? what do I say? have I offered too recently?). The dispatcher handles offer *acceptance routing* (the user said yes — what do I launch?). These are different lifecycle stages with different responsibilities.

Folding dispatch into `WorkflowOfferService` would create a god object that manages both sides of the offer/acceptance interaction. When you eventually need to change throttling logic, you'd be editing the same file that contains routing logic. When you add a new workflow type, you'd be touching presentation and dispatch in the same place.

The action registry analogy is apt. `action_registry.py` maps `action → handler`. `workflow_dispatcher.py` maps `workflow_type → entry_point`. Same pattern, same separation rationale.

One naming note: `workflow_dispatcher.py` is fine for now. If it eventually absorbs resume routing (Q3), the name still fits. If it grows beyond dispatch into lifecycle management, that's a signal to split again — but that's a future concern.

---

## Question 2: Onboarding Registration Cleanup?

**Answer: Option (a) now, as you recommend. But with a specific cleanup scope.**

Remove the registration entirely. Don't leave dead code or "on ice" stubs in the registry — that creates confusion about whether the system is active. The `# ADR-059: onboarding on ice` comment on skipped tests is the right approach for tests, because tests document intent. But in the runtime code, dead registrations are just noise.

Specific cleanup scope:

- **Remove**: `OnboardingProcessAdapter` registration from ProcessRegistry
- **Remove**: Onboarding offer detection at intent_service.py line 596-601
- **Comment out / disable (don't delete)**: The handler and state machine code in `services/onboarding/`. This preserves the implementation for potential re-enabling without cluttering the active code paths.
- **Skip tests**: With `# ADR-059: onboarding on ice` as you proposed

The reason to comment out rather than delete the handler code: onboarding *will* come back. The offer-first pattern we designed for #888 is still the right activation model. When it returns, it should be re-enabled on top of the dispatcher, not rebuilt from scratch. But it shouldn't be importable or accidentally triggered in the meantime.

**On option (c)** — a generic "workflow in progress" adapter: this is the right long-term direction, but building it now would be speculative. You don't yet know what the adapter interface needs to look like because only one workflow (meeting slot-filling) is currently functional. Wait until you have two or three dispatcher-launched workflows, then extract the common pattern. Premature abstraction risk otherwise.

---

## Question 3: Resume Offers Through Dispatcher?

**Answer: Yes, route through dispatcher. Your recommendation is correct.**

A resume is semantically "start workflow X with pre-existing state." The dispatcher already maps `workflow_type → entry_point`. Adding a `resume_session` parameter (or a `context` dict that can include a session reference) is a natural extension.

The alternative — keeping resume as a separate mechanism — perpetuates exactly the problem this ADR exists to solve: multiple independent systems detecting affirmations and racing for control. If "yes" after a resume offer goes through a different code path than "yes" after a fresh offer, you've rebuilt the race condition with one fewer participant.

Implementation suggestion: the `WorkflowEntry` dataclass could include an optional `resume_point` alongside `entry_point`:

```python
@dataclass
class WorkflowEntry:
    entry_point: Callable  # fresh start
    resume_point: Callable | None = None  # resume with existing state
    requires_context: list[str] = field(default_factory=list)
```

If `resume_point` is None, resume falls back to `entry_point` with the session context. If it's defined, it handles resume-specific logic (like presenting saved state before continuing). This keeps resume as a dispatch concern without requiring every workflow to implement resume handling.

---

## Additional Implementation Notes

### Pipeline Position Fix

The ADR correctly identifies that the core bug is pipeline position: line 448 (soft offer detection) runs before line 596 (onboarding offer detection). The dispatcher fixes this by creating a single acceptance detection point that routes to the correct handler.

Make sure the refactored pipeline has exactly one place where affirmation detection happens. If `detect_offer_response()` runs at line 448 and the dispatcher is called there, then line 596 should be gone entirely (it will be, since onboarding is removed). But verify that no other acceptance detection survives elsewhere in the pipeline. The whole point is one detection, one dispatch.

### Floor as Default for Unknown Workflow Types

The ADR specifies that unknown workflow types route to the floor. This is correct and consistent with the floor-first architecture from #911. The dispatcher's fallback is the floor, not a dead end. This means:

```python
if entry is None:
    return route_to_floor(workflow_type, session_id)
```

This is good. But also log it — an unknown workflow type reaching the dispatcher means something offered a workflow that doesn't have a handler. That's a wiring bug (Pattern-062 again), and the log entry is how you'll catch it.

### Relationship to #888/#889

The onboarding removal in ADR-059 Phase A supersedes part of the #888 hijack fix work. The #888 issue was about making onboarding offer-first and adding escape commands. If onboarding is removed entirely, #888 is partially moot — the offer-first pattern is still the right design for when onboarding returns, but there's nothing to implement it on right now.

The escape command work from #888 (registry-level escape detection) is still relevant for standup (#889) and any future guided workflows. That infrastructure should still be built per the implementation proposal I reviewed on March 13.

Flag this explicitly when closing or updating #888 — "onboarding removed per ADR-059; offer-first pattern preserved for re-enabling; escape command infrastructure still needed for #889 and future workflows."

### The "Extension Without Integration" Pattern

The ADR references the CIO's identification of this as a sub-pattern of Assembly Assumption. I'd go further: this is worth naming explicitly as a pattern in the catalog. The mechanism is specific and recurring — adding a new entry to a map/registry/enum without verifying that all downstream consumers handle the new entry. Six bugs from the same structural cause is a pattern, not a coincidence.

If the Lead Dev or CIO wants to formalize this, I'd suggest **Pattern-063: Extension Without Integration** — parent pattern Assembly Assumption (062), specific to registry/enum/map additions. Mitigation: every addition to a dispatch structure requires a downstream wiring check (same principle as the wiring pass, but at the individual-change level).

Not blocking for ADR-059, but worth capturing.

---

## Decision Summary

| Question | Decision | Rationale |
|----------|----------|-----------|
| Q1: Dispatcher placement | New component (`workflow_dispatcher.py`) | Presentation and routing are different concerns |
| Q2: Onboarding cleanup | Option (a): remove registration, comment out handler code | Clean runtime, preserve for re-enabling |
| Q3: Resume through dispatcher | Yes, with optional `resume_point` on WorkflowEntry | One detection, one dispatch — no parallel paths |

**Verdict**: ADR-059 approved. Proceed with implementation.

---

*Chief Architect | March 19, 2026*
