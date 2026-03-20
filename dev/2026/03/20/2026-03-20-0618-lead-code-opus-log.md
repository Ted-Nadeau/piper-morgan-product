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
