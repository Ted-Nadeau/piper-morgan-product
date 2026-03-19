# Session Log: 2026-03-19-0807-lead-code-opus

**Role**: Lead Developer
**Model**: Claude Code (Opus)
**Date**: Thursday, March 19, 2026
**Start Time**: 8:07 AM

## Mailbox

3 items in inbox:
1. `agent-360-questionnaire-draft-v0.1.md` — skimmed, not urgent today
2. `memo-cio-contract-gap-response-2026-03-16.md` — CIO validates "extend without verifying" pattern, recommends action registry (done), response quality smoke tests (file issue), floor routing from stubs (done), legacy removal discipline (codify)
3. `memo-ppm-floor-inversion-addendum-2026-03-16.md` — PPM says only Q40 needs classifier fix; rest handled by floor. Re-run canonical retest after Phase 2-3 migration.

**Key CIO takeaway**: "tests verify routing, not response quality" — need response quality smoke tests.

## PM Direction

- Audit cascade on #922 (conversation continuity bug)
- PM retesting later today
- PM wants us both watching: are we making real architectural progress or do we need a bigger step back?

## 8:07 AM — Audit Cascade: #922

### Finding: Three Offer/Acceptance Systems, No Conductor

The system has 3 independent mechanisms for "user said yes to an offer":
1. **Soft offer** (#824) — handles meetings with slot filling. All other types get generic acceptance + dead end.
2. **Onboarding offer** (#888) — would handle project setup, but soft offer system consumes the "Sure" first.
3. **Contextual offer** (#852) — one-turn memory on ConversationContext.

The soft offer system at line 449 has a switch with one case (`meeting`). When `project_setup` acceptance arrives, it returns "Let's get things organized" and does nothing. Onboarding offer check at line 596 never fires because soft offer already consumed the input.

This is "extend without verifying" again — `project_setup` was added to the workflow type map but nobody verified the acceptance path actually starts a workflow.

### Recommendation: Option B (structural)
Create a workflow dispatcher so soft offer becomes detect-and-dispatch instead of detect-and-handle. New workflow types shouldn't require modifying a switch statement.

### Meta-assessment for PM
Three systems solving the same problem (#824, #888, #852), built at different times, never unified. Floor inversion didn't cause this — it exposed it by making dead-end acceptances more visible. This needs design attention, not another patch.

Updated #922 with full audit cascade findings.

---

## 8:14 AM — PM Direction on #922

PM approves Option B (workflow dispatcher) but with important caveats:

### PM Decisions
1. **Remove onboarding logic** — put it on ice. Overdetermined for current stage. Simplify first (Gall's Law).
2. **Consider what we can learn from OpenClaw article** — thin Gateway/dispatcher pattern, no business logic in routing layer.
3. **ADR required** — track architectural decision properly.
4. **Chief Architect review** — PM asks whether we need arch guidance or can proceed.

### Methodological Note: Extension Without Integration

**This is now a recurring systemic pattern, not an isolated finding.**

Instances identified:
1. **Pre-classifier → handler contract gap** (#915, #916, #918, #919) — new patterns added to classifier without corresponding handler implementations
2. **Soft offer → workflow entry gap** (#922) — new workflow types added to type map without implementing their acceptance paths
3. **Three offer/acceptance systems** (#824, #888, #852) — same problem solved independently three times without reconciliation

**The mechanism**: A developer (human or AI) extends capability at one layer (adds a pattern, adds a type mapping, adds an acceptance system) without verifying that downstream layers complete the contract. Silent fallbacks absorb the gap, so tests pass but users see broken experiences.

**Why our process allows this**: Each feature is developed against its own issue with its own acceptance criteria. The criteria verify that the *new* feature works, but don't verify integration with *existing* features. There's no "composition test" — no check that says "when the user follows a multi-turn conversation path through features A → B → C, the experience is coherent."

**Proposed systematic corrections** (for PM/CIO discussion):
1. **Integration acceptance criteria**: Every issue that touches offer/acceptance, classification, or handler routing must include a multi-turn conversation test scenario, not just single-message routing.
2. **Composition audit at milestone boundaries**: Before closing a milestone, run a conversational walkthrough (like PM's QA testing) as a formal gate.
3. **Registry-enforced contracts**: The action registry pattern (#913) worked — it forces every action to declare a disposition. Apply the same pattern to workflow types: every workflow type in the offer map must have a registered entry point.
4. **Reduce system count**: When a new system is proposed that overlaps with an existing one, the default should be "extend the existing system" not "add a parallel system." Three offer mechanisms is two too many.

### My Response to PM's Three Questions

**1. Removing onboarding**: Strongly agree. Removes one of three competing systems, simplifies the reconciliation problem.

**2. OpenClaw article**: The "thin dispatcher, no business logic in routing" principle applies. Don't adopt their architecture wholesale — we're not building a multi-channel agent platform. But the dispatcher should be dumb plumbing: `workflow_type → entry_point` lookup, no switch statement.

**3. Chief Architect**: Recommend quick arch review on two questions before implementing:
   - Should dispatcher be new component or folded into WorkflowOfferService?
   - After removing onboarding, do soft offers and contextual offers serve genuinely different purposes?
   Then file ADR and implement.

---

## 8:41 AM — ADR-059 Drafted + Architect Query Sent

### ADR-059: Workflow Dispatcher and Offer System Consolidation
- Location: `docs/internal/architecture/current/adrs/adr-059-workflow-dispatcher-offer-consolidation.md`
- Three parts: (A) Remove onboarding, (B) Registry-based workflow dispatcher, (C) Reconcile soft/contextual offers
- Estimated ~5 hours implementation across 6 phases
- Three architectural questions posed to Chief Architect

### Architect Query
- Sent to `mailboxes/architect/inbox/query-adr-059-workflow-dispatcher-2026-03-19.md`
- Asks for review of Q1 (new component vs fold into WorkflowOfferService), Q2 (onboarding cleanup approach), Q3 (resume offers through dispatcher)
- Requested same-day turnaround

### Key Findings from Code Exploration
- Soft offer system: 8 workflow types detected, but only `meeting` has a real handler. Others dead-end.
- Onboarding: Has a bug — `handle_offer_response()` line 176 references `self.ACCEPTANCE_PATTERNS` (undefined). Should be `self.CONFIRM_PATTERNS`. Would cause AttributeError on acceptance.
- Contextual offer: Shares `detect_offer_response()` with soft offers. One-turn memory, always cleared.
- Resume offer: Separate frozenset matching at line 606. Fourth acceptance mechanism.
- Four acceptance detection points in the pipeline, competing for the same user input.

### Mailbox Status
- CIO memo: Read, filed to read/
- PPM addendum: Read, filed to read/
- HOSR questionnaire: Left in inbox per PM direction (will respond when time permits)

### Awaiting
- Chief Architect response on ADR-059
- PM retest of Q33/Q43/Q62 (later today)
