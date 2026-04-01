# Implementation Proposal: Workflow Hijack Fixes (#888, #889)

**To**: Chief Architect
**From**: Lead Developer
**Date**: 2026-03-13
**Re**: ProcessRegistry structural assessment + implementation plan
**Input docs**: PPM memo (2026-03-13), ADR-049, ProcessRegistry code review
**Status**: Requesting review before implementation

---

## Structural Assessment: Does ProcessRegistry Need Redesign?

**Short answer: No.** The current design accommodates all PPM-directed changes without structural modification. Here's why:

### Current Architecture (ADR-049)

```
User message
  → IntentService._check_active_guided_process()
    → ProcessRegistry.check_active_processes()
      → for handler in priority order:
          → handler.check_active(user_id, session_id)  # Is there an active session?
          → handler.handle_message(user_id, session_id, message)  # Let it claim
      → ProcessCheckResult.not_handled()  # No active process → normal classification
```

The hijack bug is NOT a ProcessRegistry design flaw. The registry correctly implements ADR-049's "active process = process handles message" rule. The problem is:

1. **Onboarding auto-activates** during greeting handling (in `conversation_handler._check_portfolio_onboarding()`), creating a session immediately. Once active, the registry correctly routes all subsequent messages to it — but the user never consented.

2. **Neither adapter checks for escape commands** before claiming. The `handle_message()` methods unconditionally route to the underlying handlers. Escape recognition happens (partially) inside the individual handlers' pattern matching, but there's no registry-level escape hatch.

3. **No timeout mechanism exists.** ADR-049's mitigation table says "timeout releases" but this was never implemented. The `cleanup_expired()` mentioned in the ADR doesn't exist in the registry.

### What Fits Within Current Design

| PPM Decision | Where It Lands | Structural Change? |
|---|---|---|
| Escape commands at registry level | `ProcessRegistry.check_active_processes()` | No — add pre-check before `handle_message()` |
| Timeout auto-suspend | `ProcessRegistry.check_active_processes()` + adapters | No — add timestamp check in `check_active()` |
| Offer-first onboarding | `conversation_handler._check_portfolio_onboarding()` | No — change activation flow, not registry |
| Save/resume state | Already exists in managers | No — state persistence already works |
| Standup completion signals | `StandupConversationHandler` | No — extend existing pattern matching |

**The registry is a sound dispatch mechanism. The bugs are in the edges: activation policy, escape handling, and timeout — all implementable within the current GuidedProcess protocol.**

---

## Implementation Plan

### Phase 1: Registry-Level Escape Commands (Shared Infrastructure)

**File**: `services/process/registry.py`

Add escape command detection to `check_active_processes()`, BEFORE calling `handle_message()`:

```python
# New constant
ESCAPE_COMMANDS = {"cancel", "exit", "stop", "skip", "never mind"}

async def check_active_processes(self, user_id, session_id, message):
    for handler in self._handlers:
        is_active = await handler.check_active(user_id, session_id)
        if is_active:
            # NEW: Check for escape commands BEFORE routing to handler
            if self._is_escape_command(message):
                await handler.suspend(user_id, session_id)  # New protocol method
                return ProcessCheckResult.escaped(
                    process_type=handler.process_type,
                    response_message=f"No problem — I've paused {handler.process_type.value}. We can pick it up anytime."
                )
            # Existing: route to handler
            result = await handler.handle_message(user_id, session_id, message)
            ...
```

This requires extending the `GuidedProcess` protocol with one new method:

```python
async def suspend(self, user_id, session_id) -> None:
    """Suspend the active session, preserving state for later resumption."""
```

And adding `ProcessCheckResult.escaped()` factory (trivial — parallel to `handled_by()`).

**Why at the registry level**: PPM explicitly said "recognized by the ProcessRegistry directly, not passed to the workflow handler for interpretation." This is the right call — it's a guaranteed escape hatch that no individual handler can break.

### Phase 2: Timeout Auto-Suspend

**Files**: Adapters (`services/process/adapters.py`)

Add timestamp tracking to `check_active()`:

```python
# OnboardingProcessAdapter.check_active()
ONBOARDING_TIMEOUT_MINUTES = 30

async def check_active(self, user_id, session_id) -> bool:
    session = ...  # existing lookup
    if not session or session.state in terminal_states:
        return False

    # NEW: Check timeout
    if session.last_activity_at:
        elapsed = datetime.utcnow() - session.last_activity_at
        if elapsed > timedelta(minutes=ONBOARDING_TIMEOUT_MINUTES):
            await self._suspend_session(session)
            return False  # No longer active — will fall through to classification

    return True
```

Similarly for `StandupProcessAdapter` with 15-minute timeout.

**Where last_activity_at comes from**: Both managers already track `updated_at` on their session/conversation objects. We use that, or add explicit `last_activity_at` if needed.

**On return after timeout**: The resume-offer happens via a new check in `_check_portfolio_onboarding()` (onboarding) or greeting handling (standup) — "We didn't finish X earlier — want to pick it up?" This is the re-entry mechanism.

### Phase 3: Offer-First Onboarding Activation (#888)

**File**: `services/conversation/conversation_handler.py`

Change `_check_portfolio_onboarding()` from:

```python
# CURRENT: Auto-activates
if await detector.should_trigger(user_id):
    response = handler.start_onboarding(session_id, user_id)
    return response.message  # User is now IN the onboarding flow
```

To:

```python
# NEW: Offer-first
if await detector.should_trigger(user_id):
    # Don't create a session yet — just offer
    return (
        "Hey, I'm Piper! I notice you're new here. "
        "I can walk you through setting up your workspace — "
        "want to do that now, or would you rather just dive in?"
    )
    # Session creation happens ONLY when user accepts (next turn)
```

**Key subtlety**: The offer message must NOT create an onboarding session. If it does, we're back to the hijack — the next message gets routed to onboarding regardless of what the user says. The session should only be created when the user explicitly accepts.

This means we need a lightweight "offer pending" state — either:
- (A) A flag on the user/session (`onboarding_offered = True`) checked on the next greeting/message
- (B) A new `OFFERED` state in the onboarding state machine, before `INITIATED`

I recommend **(B)** — it's cleaner and the state machine already supports custom states. The `OFFERED` state would be non-active (ProcessRegistry ignores it), and transitions to `INITIATED` only on acceptance, or `DECLINED` on refusal.

### Phase 4: Standup Completion Enhancement (#889)

**File**: `services/standup/conversation_handler.py`

The existing `StandupConversationHandler` already has acceptance detection:
```python
acceptance_words = ["good", "done", "looks good", "perfect", "yes", "ok", "fine", "great", "thanks"]
```

Extend with PPM's required signals:
- Section skips: "skip", "nothing", "none", "skip blockers", "nothing blocked"
- Completion at any point: "done", "that's it", "ship it"
- Partial save on interrupt: Already handled by state persistence

The three-part structure (yesterday/today/blockers) needs explicit step tracking so we can save partials. Current standup state machine has `GATHERING_PREFERENCES → GENERATING → REFINING → FINALIZING` which doesn't map cleanly to the three-part model. May need adjustment — but that's handler-internal, not registry-level.

### Phase 5: Re-Entry Mechanism

**Files**: `conversation_handler.py`, adapters

On session start, check for suspended workflows:
```python
# In greeting/session-start handling
suspended = await registry.check_suspended_processes(user_id)
if suspended:
    return f"We didn't finish {suspended.process_type.value} earlier — want to pick that up?"
```

This requires a new registry method `check_suspended_processes()` and a `SUSPENDED` state in each workflow's state machine. Straightforward extension.

---

## Protocol Changes Summary

### GuidedProcess Protocol — 1 new method:

```python
async def suspend(self, user_id, session_id) -> None
```

### ProcessCheckResult — 1 new factory:

```python
@classmethod
def escaped(cls, process_type, response_message) -> ProcessCheckResult
```

### ProcessRegistry — 2 new methods:

```python
def _is_escape_command(self, message: str) -> bool
async def check_suspended_processes(self, user_id) -> Optional[ProcessCheckResult]
```

### State Machine Changes:

- Onboarding: Add `OFFERED` state (before INITIATED) and `SUSPENDED` state
- Standup: Add `SUSPENDED` state

---

## What This Does NOT Change

- ProcessRegistry's priority-order dispatch (unchanged)
- ADR-049's "active process = process handles message" rule (unchanged, but escape commands are now checked first)
- GuidedProcess protocol's existing 3 methods (unchanged, 1 added)
- Adapter pattern (unchanged)
- Singleton manager pattern (unchanged)

---

## Testing Strategy

1. **Registry escape tests**: Message "cancel" during active onboarding → ProcessCheckResult.escaped
2. **Timeout tests**: Stale session → check_active returns False
3. **Offer-first tests**: New user greeting → offer message, no session created
4. **Offer acceptance**: User says "yes" after offer → session created, onboarding starts
5. **Offer decline**: User says "no" after offer → no session, normal classification
6. **Re-entry test**: Suspended session + new session start → resume offer
7. **Canonical retest**: All 61 canonical queries should pass after implementation

---

## Questions for Architect

1. **OFFERED state placement**: Should `OFFERED` be a ProcessRegistry-level concept (any workflow can be in "offered" state) or specific to onboarding's state machine? I lean toward onboarding-specific since standup doesn't need it (explicit invocation only).

2. **SUSPENDED state**: Same question — registry-level or per-workflow? I lean toward per-workflow since suspension semantics differ (onboarding saves project data, standup saves partial standup content).

3. **Escape command matching**: Should `_is_escape_command()` be exact match on normalized message, or substring/fuzzy? PPM said "keywords" which implies exact match. "cancel my standup" probably shouldn't escape — but "cancel" alone should. Recommend: exact match on stripped, lowercased message.

4. **ADR-049 amendment**: Should I update ADR-049 to document the escape/timeout/offer-first patterns? Or create a new ADR for workflow lifecycle? I lean toward amending ADR-049 since these are mitigations it already references but were never implemented.

---

*Lead Developer | March 13, 2026*
