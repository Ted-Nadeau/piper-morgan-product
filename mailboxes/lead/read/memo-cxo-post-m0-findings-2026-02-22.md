# Memo: Post-M0 CXO Review — Complete Findings

**From**: Chief Experience Officer
**To**: Lead Developer
**CC**: PM, Chief Architect
**Date**: February 22, 2026
**Re**: Vision Survival Assessment findings — issues to address before B2 gate
**Priority**: High

---

## Executive Summary

Post-M0 live testing conducted Feb 21-22 with PM facilitation. Two of five M0 features pass the Colleague Test; one fails; two could not be tested due to infrastructure issues.

**Bottom line**: M0 is partially working but not ready for B2 gate. The conversational glue is holding in some places and broken in others.

---

## Test Results Summary

| Feature | Issue | Result | Notes |
|---------|-------|--------|-------|
| #766 GLUE-MAINPROJ | Portfolio onboarding | ✅ **Pass** | Main project asked once at end with easy opt-out |
| #764 GLUE-MULTIINTENT | Intent orchestration | ✅ **Pass** | "Projects + time" query answered coherently |
| #767 GLUE-SOFTINVOKE | Soft workflow invocation | ❌ **Fail** | Implied needs not recognized |
| #763 GLUE-FOLLOWUP | Lens tracking | ⏸️ **Blocked** | Calendar queries failing |
| #765 GLUE-SLOTFILL | Natural slot filling | ⏸️ **Not tested** | No working workflow to test against |

---

## Issues Discovered

### Critical (Blocks Testing)

#### Issue 1: Calendar Query Failure
**Severity**: High
**Observed**: Feb 22, alfamux account

- Calendar connection test in Settings: "Test Passed"
- All calendar queries return: "I wasn't able to check on your calendar right now, but I'll keep trying"
- Tested: "What's on my calendar tomorrow?", "What's on my calendar monday?", "Can you see my calendar?"

**Impact**: Cannot test #763 (lens tracking) without working domain queries.

**Likely cause**: Intent routing, calendar service invocation, or response generation — not OAuth/API layer (since connection test passes).

---

### M0 Feature Issues

#### Issue 2: Soft Invocation Not Triggering (#767)
**Severity**: High — feature not working as designed

**Test input**: "I really need to get the team aligned on our Q3 planning process."

**Expected** (per PDR-002): Piper offers to help ("Would you like me to schedule a sync?" or "I could draft talking points")

**Actual**: Generic priority guidance with no recognition of implied workflow need

**This is the core purpose of #767** — detecting implied needs and offering help. The feature appears not to be triggering.

---

#### Issue 3: Information Flows Forward Violation (#766 related)
**Severity**: Medium

**Test input**: "Yes, I have another one called Dynamic Atlas."
**Piper response**: "Sure! What other project would you like to tell me about?"

User had to repeat the project name. Slot-filling extraction didn't parse name embedded in sentence.

**Principle violated**: "Never ask for information the user already provided."

---

### Intent Classification Issues

#### Issue 4: "Open Issues" Query Returns Projects
**Severity**: Medium

**Input**: "How many open issues do I have?"
**Output**: "You're working on 4 active projects: Decision Reviews, OneJob..."

Wrong domain. Asked about issues, got projects.

---

#### Issue 5: "Yes" Interpreted as Greeting
**Severity**: Medium

**Context**: Piper asked "Would you like me to help you set up your priority list?"
**Input**: "yes"
**Output**: "I'm doing well, thanks for asking! I've been keeping an eye on your projects."

Confirmation interpreted as "how are you?" — conversation derailed.

---

### Setup/Guidance Issues

#### Issue 6: "Help Me Connect" Requests Fail
**Severity**: Medium (covered by #814, deferred to M1)

**Inputs**: "Can you help me connect my calendar?", "Can you help me connect my Github?"
**Output**: Timestamp only, or generic priority guidance

No routing to setup assistance. (Note: #814 was intentionally deferred to M1, so this is expected current behavior.)

---

#### Issue 7: Tip Not Contextual
**Severity**: Low

**Observed**: Piper says "Tip: Connect your calendar and GitHub for more personalized guidance" to a user who HAS calendar connected.

Tip should be conditional on actual integration state.

---

#### Issue 8: GitHub Connection Not Surfaced
**Severity**: Low-Medium

It's unclear how users connect GitHub repositories to projects. The UI may not expose this, or it may not be wired up.

---

## Regressions Found and Fixed (Feb 21)

For completeness, these were found Feb 21 and reportedly fixed:

1. **Calendar settings showing connected for new account** (multi-tenancy)
2. **Conversation not appearing in history sidebar**

---

## Colleague Test Assessment

| Interaction | Natural or Weird? |
|-------------|-------------------|
| Main project question at end | ✅ Natural |
| Multi-intent response | ✅ Natural |
| Ignoring project name in sentence | ❌ Weird — "I just told you" |
| Generic response to implied need | ❌ Weird — colleague would offer to help |
| "Yes" becoming greeting response | ❌ Weird — conversation derailed |
| Tip to connect what's already connected | ❌ Weird — colleague would know |

---

## Recommendations

### Before B2 Gate

1. **Fix calendar query failure** — Blocks lens tracking test
2. **Investigate soft invocation** (#767) — Feature not triggering
3. **Fix slot extraction** — Parse names embedded in sentences
4. **Fix "yes" classification** — Context-aware confirmation handling

### For M1 (Already Planned)

5. **#814 Setup assistance** — "Help me connect X" routing
6. **Contextual tips** — Don't suggest connecting what's connected
7. **GitHub connection UX** — Surface in UI

### UX Polish (Lower Priority)

8. **Remove header tagline** — "AI Product Management Assistant / I can create GitHub issues..." contradicts colleague framing
9. **Replace blank prompt** — "What can I help you with?" → Recognition Interface pattern

---

## B2 Readiness Assessment

**Current verdict**: **Not Ready**

| Criterion | Status |
|-----------|--------|
| Features implemented | 5/5 ✅ |
| Features passing Colleague Test | 2/5 ⚠️ |
| Infrastructure stable | ❌ Calendar broken |
| Vision preserved (not flattened) | Partial — soft invocation not working |

**Recommended path**: Fix issues 1-4, retest, then reassess.

---

## Attachments

Session logs with full test transcripts:
- `2026-02-21-1201-cxo-opus-log.md`
- `2026-02-22-1445-cxo-opus-log.md`

Previous memos (regression reports):
- `memo-cxo-to-lead-regressions-2026-02-21.md`
- `memo-cxo-to-lead-calendar-query-2026-02-22.md`

---

*CXO Post-M0 Vision Survival Assessment — Testing Paused Pending Fixes*
