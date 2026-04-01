# Memo: Architectural Review — Workflow Hijack Implementation Proposal

**To**: Lead Developer
**CC**: PPM, PM (xian)
**From**: Chief Architect
**Date**: 2026-03-13
**Re**: Review of implementation proposal for #888, #889
**Input docs**: Lead Dev proposal (2026-03-13), PPM binding direction (2026-03-13), ADR-049, Architect Emeritus assessment
**Status**: APPROVED with guidance on four open questions

---

## Overall Assessment

The proposal is sound. The structural assessment is correct — ProcessRegistry doesn't need redesign. The 5-phase sequencing is right (shared infrastructure → per-workflow). The code examples are concrete and consistent with existing patterns. I'm approving this for implementation with answers to your four questions below.

One high-level observation before the specifics: the proposal does a good job distinguishing between what changes at the registry level (escape commands, dispatch logic) and what changes at the handler level (offer-first activation, standup completion). That separation is exactly right. Keep that boundary clean during implementation.

---

## Question 1: OFFERED State Placement

**Your lean**: Onboarding-specific, since standup doesn't need it.

**My answer: Onboarding-specific. Agreed.**

The reasoning is straightforward. OFFERED is an activation-pattern concept — it answers the question "has this workflow been proposed to the user but not yet accepted?" That question only arises for workflows with offer-first activation. Standup is explicit-invocation, so it will never enter an OFFERED state.

Promoting OFFERED to a registry-level concept would mean the ProcessRegistry needs to understand activation semantics, which it currently doesn't and shouldn't. The registry's job is dispatch: "is there an active process? route to it." Whether a process is in OFFERED vs. INITIATED vs. GATHERING is the handler's internal concern.

**Implementation note**: The OFFERED state must be explicitly non-active from the registry's perspective. When `OnboardingProcessAdapter.check_active()` is called and the session is in OFFERED state, it should return `False`. The registry should never see it. This means the offer-acceptance logic lives in `conversation_handler._check_portfolio_onboarding()`, not in the process dispatch path — which is where it belongs anyway, since the offer is a greeting-flow concern.

One thing to be careful about: make sure `check_active()` returns `False` for OFFERED *and* DECLINED, not just terminal states. Enumerate the non-active states explicitly rather than relying on "not in terminal_states" logic. That's less fragile.

---

## Question 2: SUSPENDED State Placement

**Your lean**: Per-workflow, since suspension semantics differ.

**My answer: Split concern. State is per-workflow. Discovery is registry-level.**

You're right that suspension semantics differ — onboarding saves project data, standup saves partial standup content. The SUSPENDED state belongs in each workflow's state machine because what "suspended" means is handler-specific.

But the *discovery* of suspended workflows needs to be a registry concern. Your Phase 5 proposes `check_suspended_processes()` on the registry, which is correct. The registry needs to be able to answer: "does this user have any suspended workflows?" without knowing what "suspended" means for each one.

This means the GuidedProcess protocol needs one more method beyond `suspend()`:

```python
async def has_suspended_session(self, user_id) -> Optional[SuspendedInfo]
```

Where `SuspendedInfo` is a lightweight data class (process_type, suspended_at, human-readable description like "portfolio onboarding" or "morning standup"). The registry iterates handlers and asks each one. The handler knows how to check its own state machine for SUSPENDED sessions.

This keeps the registry as a dumb aggregator — it doesn't interpret suspension, it just asks and relays. Clean separation.

**Protocol addition summary**: Two new methods on GuidedProcess, not one:
1. `suspend(user_id, session_id) -> None` (you already have this)
2. `has_suspended_session(user_id) -> Optional[SuspendedInfo]` (new)

---

## Question 3: Escape Command Matching

**Your lean**: Exact match on stripped, lowercased message.

**My answer: Exact match. Correct.**

PPM said "keywords," and the right interpretation is: the entire message, stripped and lowercased, must be one of the escape commands. "cancel" escapes. "cancel my standup" does not — that's potentially a meaningful instruction to the handler about *what* to cancel or *how*.

The risk of substring matching is false positives. A user saying "don't skip the blockers section" during standup should not trigger the "skip" escape. A user saying "can you stop generating and let me edit?" should not trigger "stop" as an escape from the workflow.

Exact match on the full normalized message is the conservative, correct choice. If alpha testing reveals that users naturally say "cancel this" or "I want to stop" and expect it to work, we can expand the list or add a small set of exact phrases. But start tight.

One addition to the canonical list: consider adding "quit" alongside "cancel", "exit", "stop", "skip", and "never mind". It's a natural synonym that users coming from CLI-flavored tools might reach for. But that's a minor suggestion, not a blocker.

**Implementation detail**: `_is_escape_command()` should normalize by stripping whitespace and lowercasing, then check membership in a frozenset. No regex, no tokenization, no stemming. Keep it dead simple.

---

## Question 4: ADR-049 Amendment vs. New ADR

**Your lean**: Amend ADR-049 since these are mitigations it already references.

**My answer: Amend ADR-049. Agreed.**

ADR-049 Section 4.2 (Risks and Mitigations) already says: "Explicit decline patterns always work; timeout releases." We're implementing what was specified. This isn't a new architectural decision — it's completing an existing one.

The amendment should:
1. Update the Risks and Mitigations table to mark escape commands and timeout as IMPLEMENTED (with issue references #888, #889)
2. Add the escape command list and matching semantics to the Implementation Notes section
3. Add the OFFERED and SUSPENDED states to the State Transitions diagram
4. Note the `suspend()` and `has_suspended_session()` protocol additions

Don't change the core Decision or Rationale sections — those are still correct. The amendment is about implementation details catching up to the design intent.

**Naming**: Mark the amendment with a date stamp in the Review History table, not a version number. ADR-049 is still ADR-049.

---

## Additional Architectural Notes

### On the `can_claim(message)` idea (from Emeritus Architect)

The predecessor suggested a `Workflow.can_claim(message)` method as a future extension point. I'd hold off on this for now. The escape command check at the registry level is sufficient for Layers A and B. If/when Layer C (off-topic detection) arrives, the claim-checking pattern may look quite different — it might involve an LLM call, a relevance score, or a confidence threshold. Designing `can_claim()` now without knowing what Layer C needs risks building the wrong abstraction.

File the idea in the off-topic detection issue spec when it's created. Don't pre-build it.

### On the "offer pending" implementation (Phase 3)

Your Option B (OFFERED state in the onboarding state machine) is the right choice over Option A (flag on user/session). State machines are your existing pattern for tracking workflow lifecycle. Adding a flag would create a parallel state-tracking mechanism that could drift out of sync with the state machine. One source of truth, and it's the state machine.

### Phasing confirmation

The 5-phase sequence is correct. Phases 1-2 (escape + timeout) are shared infrastructure that both #888 and #889 need. Phase 3 is #888-specific. Phase 4 is #889-specific. Phase 5 (re-entry) depends on all of the above. Ship in this order.

### Scope estimate

Predecessor estimated ~1-2 days focused work per issue. Based on the proposal's detail level, I'd say that's about right for #888. #889 may be slightly less since it inherits the registry-level infrastructure from #888. Total: 2-3 days for both, assuming no surprises in the standup state machine mapping ("yesterday/today/blockers" vs. current `GATHERING_PREFERENCES → GENERATING → REFINING → FINALIZING`).

Flag it if the standup state machine mismatch is bigger than it looks. That's the one area where I see potential hidden scope.

---

## Decision Summary

| Question | Decision | Rationale |
|----------|----------|-----------|
| OFFERED state | Onboarding-specific | Registry shouldn't know about activation semantics |
| SUSPENDED state | Per-workflow state, registry-level discovery | Semantics differ; discovery is universal |
| Escape matching | Exact match, stripped + lowercased | Conservative; expand later if alpha testing warrants |
| ADR-049 | Amend, don't replace | Implementing what was already designed |

**Verdict**: Approved for implementation. Proceed with Phase 1.

---

*Chief Architect | March 13, 2026*
