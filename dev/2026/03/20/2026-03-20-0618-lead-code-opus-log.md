# Session Log: 2026-03-20-0618-lead-code-opus

**Role**: Lead Developer
**Model**: Claude Code (Opus)
**Date**: Friday, March 20, 2026
**Start Time**: 6:18 AM

## Mailbox

Empty — no new messages.

## Context from Yesterday (2026-03-19)

- **ADR-059 implemented** (Phases A-E): Workflow dispatcher replacing three competing offer/acceptance systems
- Onboarding disabled (228 tests skipped), dispatcher created, soft offer refactored
- **6190 tests passed, 0 failures**
- PM's smoke tests were deferred to today
- 5 smoke test queries provided:
  1. "Good morning" — should NOT offer onboarding
  2. "What projects am I working on?" — should NOT launch interactive onboarding
  3. "What's blocking the milestone?" — should give real response (not stub label)
  4. "Find time for a 1:1 with the team lead" — should give conversational response (not data dump)
  5. "Check my calendar for conflicts" — should give single coherent response (not contradictory)

## Standing Directive

PM wants ongoing assessment: are we making real architectural progress or do we need a bigger step back?

---

## 6:18 AM — Session Start

PM starting smoke tests now. Standing by for results.

---

## 6:25 AM — Smoke Test Results

PM tested queries 1-4 (skipped 5 since 4 showed calendar not configured, confirming no data leakage).

### Results

| # | Query | Result | Verdict |
|---|-------|--------|---------|
| 1 | "Good morning" | Greeting + calendar summary + open-ended prompt. No onboarding offered. | ✅ PASS |
| 2 | "What projects am I working on?" | "No active projects configured" + offer to set up portfolio. No onboarding workflow launched. | ✅ PASS |
| 3 | "What's blocking the next milestone?" | First response reasonable (no priorities configured). Follow-up acceptance → non-sequitur "execution question" response. | ⚠️ MIXED |
| 4 | "Find time for 1:1 with engineering lead" | Calendar not configured message. Appropriate. | ✅ PASS |
| 5 | (skipped — moot given Q4 result) | — | — |

### Analysis of Query 3

The dead-end acceptance pattern persists but in a **different category**: the LLM generates ad-hoc offers ("Would you like me to set up your priority list?") that aren't registered workflow types. When user accepts, there's no dispatcher entry point — the acceptance falls through to a generic response.

This is **response quality**, not routing. The dispatcher handles registered workflow types correctly. The gap is that the LLM's conversational offers create implicit contracts the system can't fulfill.

**Assessment**: Smoke tests are a **qualified pass**. ADR-059 structural changes working. Remaining issue is a different problem category.

### PM Decision
- **New issue**, not #922. Different root cause, different fix.

---

## 7:46 AM — Capability Awareness Gap: Three Truths Problem

PM approved filing new issue. Key PM directive: "don't see it as laser surgery but as a new element that needs to play well with the existing constellation." Wary of "we just need to..." thinking (rightfully so).

### Discovery: Three Disconnected Capability Sources

Investigation revealed **three separate systems** that describe what Piper can do, none coordinated:

| Source | What It Says | Who Reads It | Count |
|--------|-------------|-------------|-------|
| **PIPER.md "System Capabilities"** | Document analysis, task mgmt, calendar, GitHub, Slack, Notion | LLM (via system prompt) | ~8 capabilities |
| **Soft invocation detection** (`soft_invocation.py`) | meeting, project_setup, status_check, standup, review, priority_check, reminder | Offer pipeline | 7 workflow types |
| **Workflow dispatcher registry** | meeting | Execution layer | 1 entry point |

**Root cause of query 3**: LLM reads PIPER.md → sees "Task Management: set priorities" → offers to help → user accepts → nothing fulfills it because neither soft invocation nor dispatcher registered that as a workflow.

This is **extension without integration** at the configuration/prompt layer. Same systemic pattern, different substrate.

### Approach: Reconcile, Don't Add

Rather than "project the registry into the prompt" (which would be a 4th source of truth), the fix must **reconcile the three existing sources** into a coherent picture where the LLM's offers match what the system can fulfill.

Filed as **#923**: Capability awareness gap — three disconnected sources of truth for what Piper can do.

Issue maps all 7 integration points. Key design principle: reconcile existing sources rather than adding a 4th. Registry-driven capability awareness so the prompt stays in sync with what's actually executable.

---

## 8:03 AM — #922 Closure Evidence

Added implementation evidence comment to #922 (closed yesterday without evidence — corrected per our process).

---

## 8:10 AM — M1 Status Review for PM

Provided milestone status:
- **M1-labeled**: #902 (GitHub close/reopen), #903 (reminders), #904 (todo lifecycle) — all open
- **Recently filed**: #923 (capability awareness gap) — architectural, critical
- **Other active**: #911 (floor inversion), #910 (token test failure), #909 (hardcoded username), #908 (generic response signaling), #898 (classifier edge cases)

---

## 8:33 AM — #924: Chat Avatar Images

PM idea: add dolphin logo as Piper's avatar, colored initial circle for user. "Touch of joy."

### Audit Cascade

**Integration points identified:**
1. `appendMessage()` in chat.js — message creation (core change)
2. `.message-container` CSS — layout needs row wrapper for avatar + message
3. Widget template — hardcoded initial message needs avatar markup
4. History restore — uses `appendMessage()`, gets avatars automatically ✅
5. Timestamp tooltips — appended to container, still works ✅
6. User context — `window.currentUser.username` available from template ✅
7. Asset serving — `/assets/` mount already exists ✅

**What does NOT need changing:**
- No backend changes
- No API changes
- No test changes for service layer
- Inline chat template has no hardcoded messages (JS renders all)

### Implementation

Filed as **#924**. Implemented:

**Files modified:**
- `web/static/js/chat.js` — Added `createAvatar()`, `getAvatarColor()`, wrap messages in `message-row` with avatar
- `web/static/css/chat.css` — Avatar styling, row layout, moved alignment from message to row level
- `templates/components/chat-widget.html` — Added avatar to hardcoded initial bot message

**Files added:**
- `web/assets/piper-avatar.svg` — Color dolphin logo (copied from archive/new-pm-logo/pm-logo-color.svg)

**Design decisions:**
- Used color SVG (teal dolphin) — PM can swap for desaturated after design review
- User avatar: deterministic color from username hash (consistent across sessions)
- 32px avatars (28px on mobile)
- Piper avatar left of bot messages, user avatar right of user messages
- `aria-label` on user avatar for accessibility

**Test results:** 149 passed, 1 pre-existing failure (#910), no new failures.

---

## PM Decisions Captured

1. **Smoke tests**: Qualified pass. Queries 1, 2, 4 passed. Query 3 revealed new bug category → filed #923.
2. **#922**: Closed with evidence (had been closed without evidence — corrected).
3. **#923 (capability awareness gap)**: Filed, audited, implemented, and closed same session. Registry-driven capability awareness.
4. **M1 order of operations**: Approved tier structure (architecture → quality → capabilities → PM-led).
5. **#911 (floor inversion)**: Closed as substantially complete (Phases 1-2). PM approved deferring Phases 3-4 to #925.
6. **#924 (chat avatars)**: Approved and implemented. Dolphin logo for Piper, colored initial for user.
7. **#908**: Audit cascade complete. Plan ready for morning execution.

## Issues Opened This Session

- **#923** — Capability awareness gap (filed and closed)
- **#924** — Chat avatars (filed and closed)
- **#925** — Floor inversion Phase 3-4 follow-up (deferred)

## Issues Closed This Session

- **#922** — Conversation continuity (evidence added)
- **#911** — Floor inversion (Phases 1-2 complete)
- **#923** — Capability awareness gap (implemented)
- **#924** — Chat avatars (implemented)

## Next Session Plan

Execute #908 (canonical handlers signal generic responses) per audit cascade plan:
- Phase 1: Add `is_generic_response` flag to handler return dicts
- Phase 2: Update safety net detection to check flag first
- Phase 3: Tests

After #908: proceed to #909 (remove hardcoded username), then #910 (pre-existing test failure).

---

## 9:02 AM — Session Resumed (Post-Compaction)

PM provided M1 open items TSV. 14 issues open. Proposed order of operations:
- **Tier 1** (architecture): #923 → #911 → #907
- **Tier 2** (quality): #908 → #909 → #910 → #898
- **Tier 3** (capabilities): #902 → #904 → #903 → #883
- **Tier 4** (PM-led): #706, #717, #375

PM approved. Proceeding with full audit cascade on each step. PM authorized autonomous execution with discretion to stop and confer on larger factors.

### Next: Audit Cascade on #923 — Capability Awareness Gap

---

## 9:15 AM — Audit Cascade: #923 Capability Awareness Gap

### Finding: Five Sources of Truth (Worse Than Thought)

| # | Source | Claims | Reality | Dynamic? |
|---|--------|--------|---------|----------|
| 1 | PIPER.md "System Capabilities" | 28 capabilities across 7 areas | Slack, Notion, Calendar mostly unimplemented | No |
| 2 | PIPER.md "Available Integrations" | GitHub, Slack, Calendar, Notion, MCP | Only GitHub confirmed active | No |
| 3 | Soft invocation detector | 7 workflow types | Only `meeting` has entry point | No |
| 4 | Workflow dispatcher registry | `meeting` only | Truth — this is what's real | Yes |
| 5 | ContextAssembler + canonical handlers | "development coordination, issue tracking, strategic planning" + PluginRegistry | Partially dynamic (plugins yes, core list hardcoded) | Partially |

### Root Cause Chain

```
PIPER.md says "Task Management: Set priorities and deadlines"
  → LLM reads this as real capability
    → User asks "What's blocking the milestone?"
      → LLM offers to set up priority list (because PIPER.md said it could)
        → User accepts
          → No dispatcher entry for "priority_check"
            → Falls through to floor
              → Floor says "What specific challenge?" (non-sequitur)
```

### Implementation Plan

**Phase A: Clean PIPER.md** — Remove aspirational capabilities. Only describe what's real.
- Strip Slack, Notion sections (not implemented)
- Calendar: mark as "when configured"
- Task Management: narrow to what actually works
- Remove "Available Integrations" redundant section or reconcile

**Phase B: Gate soft invocation on dispatcher registry** — The detector should only offer workflow types that have registered entry points. If `priority_check` isn't in the registry, don't offer it.

**Phase C: Make ContextAssembler registry-aware** — Replace hardcoded `["development coordination", "issue tracking", "strategic planning"]` with data derived from dispatcher registry + plugin registry.

**Phase D: Refine floor addendum** — The "NEVER say you can't do that" instruction is harmful when Piper genuinely can't. Distinguish between:
- Things Piper can execute (workflows) → offer them
- Things Piper can discuss (PM advice) → engage conversationally
- Things Piper can't do → be honest

**Phase E: Tests** — Verify alignment between all sources.

### Key Design Decision

Soft invocation is the critical gate. By filtering offers at detection time (Phase B), we prevent the entire downstream chain without touching the LLM or the floor. This is the **minimum viable fix** — everything else is defense in depth.

---

## 9:45 AM — #923 Implementation Complete

### Phases A-E executed successfully

**Phase A: Clean PIPER.md**
- Stripped aspirational capabilities (Slack, Notion, detailed Calendar, detailed Task Management)
- Added capability accuracy warning: "Every capability listed here MUST have a working implementation"
- Kept: Conversational PM guidance, GitHub, Meeting scheduling (when configured), Document analysis
- Removed "Available Integrations" duplicate section for Slack/Notion/MCP
- Replaced "Learning Capabilities" with "Conversational Strengths" (honest about what these are)
- Removed prescriptive "Default System Behaviors" section

**Phase B: Gate soft invocation on dispatcher registry**
- `SoftInvocationDetector.detect()` now checks `get_registered_workflows()` before offering
- Unregistered workflow types → `soft_invocation_suppressed` log event (telemetry preserved)
- Only `meeting` currently offered (the only registered type); 6 other types suppressed
- Key behavior: adding a workflow to the registry automatically enables offers

**Phase C: ContextAssembler + canonical_handlers registry-aware**
- Replaced hardcoded `["development coordination", "issue tracking", "strategic planning"]`
- Now: `["conversational PM guidance", "strategic thinking and prioritization frameworks"]` + workflow entries from dispatcher registry
- Dynamic: when meeting workflow is registered, capabilities include "Meeting scheduling via slot-filling"

**Phase D: Floor addendum refined**
- Removed "Never say you can't help" — harmful blanket instruction
- Removed "Do NOT say 'I don't have that capability yet' — ever"
- Added "Do NOT promise to do things you're unsure you can execute"
- Added "Do NOT offer to 'set up' or 'configure' features the user hasn't asked about"

**Phase E: Tests**
- 5 new registry gate tests (TestRegistryGate class)
- Updated 4 test files with registry mock fixtures (autouse)
- Updated capability assertions across 3 test files
- **Results: 2633 passed, 1 pre-existing failure, 3 skipped, 0 new failures**

---

## 10:15 AM — Audit Cascade: #911 Floor Inversion

### Finding: Mostly Done Already

| Phase | Categories | Status |
|-------|-----------|--------|
| Phase 1 | GUIDANCE, UNKNOWN | ✅ Complete |
| Phase 2 | IDENTITY (adjacent), DISCOVERY, TRUST, MEMORY, CONVERSATION (non-greeting) | ✅ Complete |
| Phase 3 | STATUS, PRIORITY (data-heavy) | ⏳ Pending — safety net active (generic → floor fallback) |
| Phase 4 | CONVERSATION greeting refactor | ⏳ Pending — has side effects (onboarding) |

**Action Gate** exists in `intent_service.py` (not a separate file). `_should_route_to_floor()` and `_requires_canonical_handler()` implement the routing.

**Context Assembler** handles IDENTITY/DISCOVERY, TRUST, MEMORY categories. Guidance has its own context assembly.

**Remaining work**: STATUS and PRIORITY could be routed to floor with data context, but currently the safety net (check for generic canonical response → fallback to floor) covers the worst cases. The canonical handlers for STATUS/PRIORITY make GitHub API calls and return structured data — floor routing would need that data assembled into context.

**Assessment**: This is in a **good-enough state for M1**. The safety net catches generic responses. The remaining migration (STATUS/PRIORITY to floor-first) is an optimization, not a bug fix. Can we defer the remaining phases to post-M1?

---

## 10:30 AM — Audit Cascade: #908 Generic Response Signaling

### Context Shift

With #911 Phases 1-2 complete and #923's registry gate in place, the scope of #908 has narrowed. The categories most likely to produce generic responses (GUIDANCE, DISCOVERY, TRUST, MEMORY, CONVERSATION non-greeting) are **already floor-routed**. They never hit the generic detection path.

### Current State

- `_GENERIC_CANONICAL_SIGNATURES`: 7 hardcoded strings (all GUIDANCE-related)
- `_is_generic_canonical_response()`: substring matching
- Safety net catches generic canonical responses → routes to floor
- Only fires for Action Gate pass-through categories: PORTFOLIO, EXECUTION, STATUS, PRIORITY, TEMPORAL, CONVERSATION.greeting, IDENTITY.core, GUIDANCE.setup

### What Remains Vulnerable

Categories still using canonical handlers that might return generic templates:
- **STATUS** (no projects configured) → template like "Here's your detailed project status:"
- **PRIORITY** (no priorities configured) → template like "Here are your priorities in detail:"
- **GUIDANCE.setup** → setup-specific template
- **TEMPORAL-calendar** (no calendar configured) → calendar-not-configured message

### Implementation Plan

**Pragmatic approach**: Add `is_generic_response` flag to canonical handler return dicts, but only for the handlers that are known to produce generic templates. Keep the signature list as fallback.

**Phase 1: Add flag to handler returns**
- Create helper function `_canonical_response(message, intent, *, is_generic=False, **kwargs)` to build canonical return dicts consistently
- Update STATUS, PRIORITY, and GUIDANCE.setup handlers to use it with `is_generic=True` where appropriate
- Detection logic checks flag first, falls back to signature list

**Phase 2: Update safety net**
- `_is_generic_canonical_response()` checks `result.get("is_generic_response", False)` first
- Falls back to signature matching for handlers not yet updated
- Log when signature fallback fires (telemetry for remaining migration)

**Phase 3: Tests**
- Test flag detection
- Test signature fallback still works
- Test that generic STATUS/PRIORITY routes to floor

### Integration Points
- `services/intent_service/canonical_handlers.py` — handler return dicts
- `services/intent/intent_service.py` — `_is_generic_canonical_response()` method
- Tests for both

### Risk Assessment
- **Low risk**: additive change, backward compatible (flag defaults to False)
- **Low blast radius**: existing signature list remains as fallback
- **Known complexity**: STATUS and PRIORITY handlers have multiple code paths — need to identify which paths produce generic vs. data-backed responses

---

### Files modified (13)
- `config/PIPER.md` — Reconciled with runtime truth
- `services/intent_service/soft_invocation.py` — Registry gate in detect()
- `services/intent_service/context_assembler.py` — Registry-derived capabilities
- `services/intent_service/canonical_handlers.py` — Registry-derived capabilities
- `services/intent_service/conversational_floor.py` — Refined floor addendum
- `tests/unit/services/intent_service/test_soft_invocation.py` — Registry mock + gate tests
- `tests/unit/services/intent_service/test_formality_soft_invocation.py` — Registry mock
- `tests/unit/services/intent_service/test_soft_invocation_integration.py` — Registry mock
- `tests/unit/services/intent_service/test_soft_invocation_colleague.py` — Registry mock
- `tests/unit/services/intent_service/test_canonical_handlers.py` — Updated assertions
- `tests/unit/services/intent_service/test_discovery_intent.py` — Updated assertions
- `tests/unit/services/intent_service/test_action_gate.py` — Updated assertions
- `dev/2026/03/20/2026-03-20-0618-lead-code-opus-log.md` — This log
