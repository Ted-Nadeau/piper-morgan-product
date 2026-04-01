# Memo: PPM Product Direction — Guided Workflow Escape and Activation

**To**: Lead Developer, Chief Architect
**CC**: CXO
**From**: PPM
**Date**: 2026-03-13
**Re**: Issues #888, #889 — Design decisions for workflow session capture
**Input docs**: Lead Dev UX guidance request (2026-03-12), CXO UX guidance memo (2026-03-13)
**Status**: APPROVED — Ready for implementation

---

## Purpose

This memo provides binding product direction on four design questions raised by the Lead Developer regarding guided workflow "hijack" behavior discovered during canonical retest (#884). CXO provided UX guidance; this memo synthesizes that guidance with product priorities and defines the implementation path.

---

## Decision Context

During M1 canonical testing, the Lead Developer discovered that the Onboarding and Standup workflows capture the user's session and never release it. The ProcessRegistry checks for active workflows before intent classification, and active workflows always claim incoming messages — regardless of user intent. This causes 8 canonical test failures and represents the most visible user-facing defect in the current build.

The engineering fix is well-scoped. These decisions address the user experience layer.

### Governing Principle

**The session belongs to the user, not the workflow.**

A workflow is a guest in the user's conversation. It holds the user's attention only while they are actively participating. The moment a user redirects — whether explicitly or implicitly — the workflow must yield.

This principle derives from PDR-001 (FTUX as First Recognition) and the Colleague Test: a human colleague in the same situation would recognize the topic change and respond accordingly. Piper must do the same.

This principle applies to all current and future guided workflows, not just onboarding and standup.

---

## Decisions

### 1. Escape Mechanism

**Decision: Layered approach — explicit commands + timeout now; off-topic detection as follow-on.**

Three layers, in order of implementation priority:

**Layer A — Explicit commands (ship with #888 and #889).**
The keywords "cancel", "exit", "stop", "skip", and "never mind" must always terminate or suspend an active workflow. These must be recognized by the ProcessRegistry directly, not passed to the workflow handler for interpretation. This is non-negotiable — it is the user's guaranteed escape hatch.

**Layer B — Timeout (ship with #888 and #889).**
If a user goes idle during an active workflow, the workflow auto-suspends after a defined interval. Recommended intervals:
- Standup: 15 minutes
- Onboarding: 30 minutes

On return, Piper offers to resume rather than assuming the workflow is still active.

**Layer C — Off-topic detection (separate issue, follow-on).**
When a message arrives during an active workflow, the system performs a lightweight relevance check: does this message plausibly continue the workflow, or has the user moved on? If off-topic is detected, Piper acknowledges the shift and offers a choice:

> "Sounds like you're asking about your calendar — let me check on that. We were in the middle of standup — want to come back to it after?"

**Scoping note:** Off-topic detection is reusable infrastructure that every future guided workflow will need. It must be a separate issue from #888/#889 to avoid either under-building it (onboarding-specific only) or scope-creeping the hijack fixes. Layers A and B provide a shippable fix; Layer C enhances it.

### 2. Re-entry After Escape

**Decision: Save state, offer to resume once, accept "no" gracefully.**

When a workflow is suspended (by escape, timeout, or future off-topic detection):

- **Save progress.** Piper remembers where the user left off. Completed steps remain completed — a user who configured GitHub during onboarding should not have to redo it.
- **Offer to resume once.** At the start of the next relevant interaction, Piper offers: "We didn't finish setting up your workspace earlier — want to pick that up?" This happens once, at conversation start, not mid-conversation.
- **Accept decline gracefully.** If the user declines or ignores the offer, the workflow remains available for explicit invocation but Piper does not bring it up again unprompted.
- **No "paused workflow" UI indicator at this stage.** The conversational offer-to-resume is sufficient. If alpha testing reveals confusion about workflow state, we revisit.

### 3. Workflow Activation

**Decision: Offer-first for onboarding. Explicit invocation for standup.**

**Onboarding (changed from auto-activate to offer-first):**

Piper's first interaction with a new user should be a welcome that offers — not imposes — the setup flow:

> "Hey, I'm Piper! I notice you're new here. I can walk you through setting up your workspace — want to do that now, or would you rather just dive in?"

If the user accepts, the guided onboarding workflow activates (with the escape mechanisms above). If the user declines, the workflow never activates. Piper functions with reduced capability where integrations haven't been configured and can make contextual suggestions later.

**Contextual nudge throttle:** Maximum 1 integration suggestion per session. Stop suggesting entirely after 3 declined suggestions across sessions. Example: "I notice you haven't connected GitHub yet — want me to help with that?"

**Standup (unchanged — explicit invocation only):**

Standup activates only when the user explicitly initiates it (`/standup`, "let's do standup", "morning standup", etc.). Piper does not auto-initiate standups.

**Implementation note:** The offer-first pattern means the onboarding handler's first turn is a yes/no question, not a data-gathering question. If the user says no, the handler must return control to intent classification immediately — it must not activate at all.

**Design principle for future workflows:** Offer-first should be the default activation pattern for any new guided workflow unless there is a specific, documented reason for auto-activation. Capture this in PDR-001 as an addendum.

### 4. Standup Scope and Completion

**Decision: Structural completion + "done" recognition + save partials.**

- Standup has a known three-part structure (yesterday / today / blockers). After collecting all three, Piper presents a summary and asks for confirmation: "Does that look right?"
- "Done", "that's it", "looks good", "ship it", and similar affirmative phrases are recognized as completion signals at any point — including mid-flow for partial standups.
- "Skip", "nothing", "none", "skip blockers", "nothing blocked" are recognized as section-skip signals.
- **Partial standups are saved when interrupted.** If a user provided yesterday and today but was interrupted before blockers, that data persists. On re-entry: "We had yesterday and today logged — want to add blockers, or save it as-is?"

---

## Implementation Sequence

| Priority | Issue | Scope | Sprint |
|----------|-------|-------|--------|
| 1 | **#888** (Onboarding hijack) | Convert to offer-first activation. Add explicit escape commands to ProcessRegistry. Add 30-min timeout. Instrument offer + completion events. | M1 |
| 2 | **#889** (Standup hijack) | Add explicit escape commands. Add 15-min timeout. Add structural completion + "done" recognition. Save partial standups. | M1 |
| 3 | **New issue** (Off-topic detection) | Reusable mechanism for detecting off-topic messages during active workflows. Layers onto #888 and #889. | M1 if capacity, M2 if not |

**Sequencing rationale:** #888 first because onboarding hits every new user and is a first-impression issue. #889 second because standup is user-initiated and affects a narrower set of interactions.

---

## Instrumentation Requirements

The shift to offer-first onboarding changes our measurement model. Lead Dev should instrument:

- **Onboarding offer events**: Offer shown, accepted, declined
- **Onboarding completion events**: Steps completed (which integrations configured), flow completed vs. abandoned
- **Escape events**: Which escape mechanism was used (explicit command, timeout, or future off-topic detection), at which workflow step
- **Re-entry events**: Resume offered, accepted, declined

This data tells us whether the onboarding flow is *attractive* (users choose to enter it) rather than merely *inescapable* (users can't avoid it). That's better signal.

---

## Architectural Note for Chief Architect

The CXO's "session belongs to the user" principle has implications for how ProcessRegistry claims messages. Currently, per ADR-049, "active process = process handles message." The mitigation for session trapping (explicit decline patterns + timeout) was specified but apparently never implemented.

Please assess whether the fixes above can be implemented within the current ProcessRegistry design, or whether a structural change is needed to make workflow-yields-to-user the default behavior rather than an opt-in per workflow. If structural, please flag scope implications for M1.

---

## What This Memo Does Not Cover

- The specific off-topic detection algorithm (that's the new issue's spec)
- Changes to ADR-049 (Architect's call)
- UI/visual indicators for workflow state (deferred unless alpha testing surfaces need)
- Other workflows beyond onboarding and standup (this establishes the pattern; future workflows follow it)

---

## Decision Record

| Question | Decision | Rationale |
|----------|----------|-----------|
| Escape mechanism | Explicit commands + timeout (now); off-topic detection (follow-on) | Layered approach: shippable fix first, sophistication second |
| Re-entry | Save state, offer once, accept no | Colleague behavior; don't nag |
| Activation | Offer-first (onboarding), explicit (standup) | PDR-001 alignment; session belongs to user |
| Standup completion | Structural + "done" signals + save partials | Natural conversation flow; don't discard useful data |
| Root principle | Session belongs to user, not workflow | Prerequisite for trust model; Colleague Test |

---

*PPM Memo | March 13, 2026*
