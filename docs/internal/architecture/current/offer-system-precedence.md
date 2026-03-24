# Offer System Precedence — How Piper Makes and Fulfills Offers

**Issue**: #926 Gate 3 (Architectural Integrity)
**Date**: 2026-03-24
**Author**: Lead Developer

---

## Overview

Piper has three mechanisms for making offers to users and handling their acceptance. This document defines their ownership, precedence, and interaction rules.

---

## The Three Systems

### 1. Workflow Dispatcher (Registered Workflows)

**Owner**: `services/intent_service/workflow_dispatcher.py`

**What it does**: Routes user acceptance of structured workflow offers (e.g., "Would you like me to help schedule a meeting?" → user says "Yes" → dispatcher routes to the meeting slot-filling entry point).

**Registry**: `WORKFLOW_REGISTRY` — a dict of `workflow_type → WorkflowEntry`. Each entry has:
- `entry_point`: async function to start the workflow
- `resume_point`: optional async function to resume a paused workflow
- `description`: human-readable capability description

**When it fires**: When `detect_offer_response()` detects an acceptance AND the pending offer matches a registered workflow type.

**Precedence**: **Highest for registered workflows.** If a workflow type is registered, the dispatcher owns the acceptance path. No other system should handle it.

### 2. Soft Invocation Detector (Conversational Offers)

**Owner**: `services/intent_service/soft_invocation.py`

**What it does**: Detects natural-language opportunities to offer capabilities during conversation. For example, if a user mentions being busy, Piper might offer "Would you like me to help prioritize your tasks?"

**Registry gate** (#923): Before making an offer, checks `get_registered_workflows()` to verify the offered capability actually exists. Prevents offering things Piper can't do.

**When it fires**: After handler processing, applied via `_apply_soft_offer()` in intent_service.py. Only fires when:
- Trust stage is BUILDING or higher (new users don't get offers)
- No soft offer was already made this turn
- The registry gate confirms the capability exists

**Precedence**: **Lower than dispatcher.** Soft invocation creates offers; the dispatcher fulfills them. Soft invocation never handles acceptance — it only proposes.

### 3. Contextual Offers (Handler-Embedded)

**Owner**: Individual canonical handlers (e.g., `_format_integration_setup_guidance()`)

**What it does**: Handlers embed offers directly in their response text. For example, a setup guidance handler might include "Would you like guidance on setting up a specific integration?"

**When it fires**: During handler execution. The offer text is part of the response, not a separate system.

**Precedence**: **Lowest and most fragile.** These offers have no structured acceptance path — the user's "yes" goes through normal intent classification, which may or may not route back to the right handler. This is the pattern that caused #922 (dead-end acceptances).

---

## Precedence Order

```
User sends message
  │
  ├── Is this an acceptance of a pending offer?
  │     └── YES → Workflow Dispatcher handles it (if registered type)
  │               └── Not registered? → Falls to floor (conversational response)
  │
  ├── Process intent normally (classifier → handler)
  │
  └── After processing: Should we make a new offer?
        └── Soft Invocation Detector checks:
              1. Trust stage ≥ BUILDING?
              2. Registry gate: is the capability registered?
              3. No offer already made this turn?
              └── All yes → Attach offer to response
```

## Rules

1. **Only the dispatcher fulfills registered workflow acceptances.** No handler should try to catch "yes" independently.

2. **Only registered capabilities can be offered.** The registry gate (#923) prevents soft invocation from offering things the dispatcher can't fulfill.

3. **Contextual offers in handler text should be migrated to soft invocation.** Handler-embedded offers bypass the registry gate and have no structured acceptance path. As handlers are updated, move offers to the soft invocation system.

4. **One offer per turn.** Soft invocation checks whether an offer was already made. Multiple offers per response is confusing.

5. **Unknown acceptance → floor.** If a user says "yes" but there's no pending offer or the offer type isn't registered, the conversational floor handles it naturally rather than dead-ending.

---

## ADR References

- **ADR-059**: Workflow dispatcher and offer consolidation
- **#922**: Conversation continuity broken (root cause: three competing offer systems)
- **#923**: Capability awareness gap (fix: registry gate in soft invocation)

---

*Lead Developer | March 24, 2026*
