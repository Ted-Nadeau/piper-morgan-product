# Memo: Weekly Summary — CXO Perspective

**From**: Chief Experience Officer
**To**: Chief of Staff
**Date**: January 30, 2026
**Re**: Week of January 23-29, 2026 — UX Observations for Weekly Ship
**Filename**: `memo-from-cxo-to-exec-weekly-2026-01-30.md`

---

## Executive Summary

**The headline**: v0.8.5 released on January 27, completing the MUX-IMPLEMENT super epic. The grammar ("Entities experience Moments in Places") is now operational, not just conceptual.

**The sobering follow-up**: Alpha testing on January 28-29 exposed deep bugs including a P0 (projects never persist to database) and a critical multi-tenancy gap (user A could see user B's calendar events). Root causes found and fixes applied.

**From the CXO lens**: This week validated that our design foundations are sound while exposing that multi-user isolation was never fully implemented. The "conversation persistence" bug (#731, fixed and verified Jan 29) shows how conversational UX can mask underlying data failures.

---

## Day-by-Day Summary

| Day | Rating | Headline |
|-----|--------|----------|
| Jan 23 (Thu) | HIGH-COMPLEXITY | TRUST-LEVELS epic complete (359 tests), Jan 22 logging incident fixed |
| Jan 24 (Fri) | HIGH-COMPLEXITY | MUX-WIRE complete, Mobile PoC breakthrough, Gate #534 passed |
| Jan 25 (Sat) | HIGH-VELOCITY | MUX-IMPLEMENT P1-P3 sprint: 21 issues, 1000+ tests |
| Jan 26 (Sun) | HIGH-ALIGNMENT | Multi-advisor coordination, ADR-049/050 decisions |
| Jan 27 (Mon) | HIGH-VELOCITY | **v0.8.5 RELEASED** — MUX-IMPLEMENT complete |
| Jan 28 (Tue) | MIXED-DAY | Alpha docs ship-ready, then 11 bugs discovered in testing |
| Jan 29 (Wed) | LIGHT-DAY | Root causes found, critical multi-tenancy gap identified |

---

## Key Metrics (Jan 23-29)

| Metric | Value |
|--------|-------|
| Issues Closed | ~65+ |
| Tests Added | ~2,500+ |
| Epics Completed | 3 (TRUST-LEVELS, MUX-WIRE, MUX-IMPLEMENT) |
| Test Suite Final | 5,253 tests |
| Alpha Bugs Found | 11+ (Jan 28) + additional root causes (Jan 29) |
| Alpha Bugs Fixed | 10+ and continuing |

---

## UX-Significant Developments

### 1. MUX Vision Now Operational

The MUX grammar ("Entities experience Moments in Places") moved from documentation to running code:

- **Object model**: Entities with lifecycle states
- **Consciousness layer**: Warmth calibration, honest failure patterns
- **Trust computation**: ADR-053 fully implemented
- **Lifecycle visualization**: WorkItem and Feature lifecycle ready for UI

This is a major milestone. The design principles established in December are now testable in production.

### 2. Insight Lifecycle Conceptual Clarity

On January 27, CXO and PPM reached consensus on the Insight model question:

- **Decision**: Insights don't get entity lifecycle states
- **Rationale**: Insights are "composted output" — they emerge from processing, they don't progress through work stages
- **Design implication**: No lifecycle badges on insights; use freshness and confidence language instead

This prevents a category error (applying work progression states to knowledge artifacts) and keeps the model conceptually clean.

### 3. Mobile PoC Breakthrough

The Mobile 2.0 skunkworks reached tactile validation:

- **Root cause found**: IntentToast animation invisible due to Reanimated version mismatch
- **Fix applied**: January 24
- **Current status**: PM carrying device for "carry and note" validation
- **Core hypothesis under test**: Does entity-based gesture mapping feel intuitive?

### 4. Alpha Testing Reality Check (Jan 28-29)

Two days of alpha testing exposed fundamental issues:

**January 28** (11 bugs found):

| Bug | Impact | Lesson |
|-----|--------|--------|
| #728 (P0) | Projects never persist | Conversation-level "capture" ≠ database persistence |
| #724 | API keys stored wrong | Multi-user prefix/retrieve mismatch |
| #729 | History sidebar missing | Template include forgotten |

**January 29** (Root causes found):

| Bug | Root Cause | Fix |
|-----|------------|-----|
| #731 | Typing directly in chat → no conversation record created | Auto-create in `/api/v1/intent` — **VERIFIED WORKING** |
| #736 | Projects unique constraint is GLOBAL, not per-user | Migration to composite constraint `(owner_id, name)` |
| #734 | **CRITICAL**: Calendar tokens stored without user_id | User A could see User B's calendar events |

**Key insight from Jan 29**: The multi-tenancy gaps (#734) are more serious than individual bug fixes. The Oct 2025 multi-user work was incomplete — storage updated, retrieval paths missed. This needs systematic audit, not just reactive fixes.

---

## Concerns / Watch Items

### 1. Multi-Tenancy Isolation (CRITICAL)

January 29 revealed that integration tokens (calendar, etc.) are stored globally without user scoping. This means:
- User A could potentially see User B's calendar events
- The "multi-user" work from Oct 2025 was incomplete

**Recommendation**: Before expanding alpha testers, audit ALL user-scoped storage for storage/retrieval symmetry.

### 2. Verification Theater Risk

We have 5,253 tests passing. We also had:
- A P0 where projects simply didn't save
- A critical privacy bug where users could see each other's calendar events
- Conversation persistence that appeared to work but created no database records

**Recommendation**: Add E2E tests that verify database state after user flows, not just that handlers return success responses.

### 3. "Conversation Says X" Pattern

The conversation persistence bug (#731) is emblematic: Piper's conversation made it *look* like things were happening, but the database told a different story.

- User types in chat → Piper responds thoughtfully → no conversation record exists
- User completes onboarding → Piper says "I've captured your projects" → database has nothing

**Design implication**: We may need "verification receipts" — moments where Piper confirms actual database state, not just conversational intent.

---

## Design Implications Emerging

### From Alpha Testing

The bugs revealed a pattern: **surface-level verification passes, depth verification fails**.

This suggests:
1. Our UX testing needs "verify the artifact" steps, not just "verify the response" steps
2. Multi-user paths need dedicated test scenarios (not just "works for one user")
3. The consciousness layer's warmth may be masking data layer failures

### For Future Sprints

The MUX foundation is solid. The next challenges are:
1. **Multi-tenancy audit**: Systematic review of all user-scoped data
2. **E2E verification**: Tests that check database state, not just API responses
3. **Privacy validation**: Before adding testers, ensure user isolation is complete

---

## CXO Contributions This Week

| Date | Deliverable | Purpose |
|------|-------------|---------|
| Jan 23 | ADR-053 approval memo | Trust computation ratification |
| Jan 23 | Conversational glue design spec | #427 implementation guidance |
| Jan 23 | Orientation system response | #410 experience design |
| Jan 23 | Learning system response | #431 design docs approval |
| Jan 23 | Mobile skunkworks briefing | Project context document |
| Jan 23 | Weekly summary (Jan 16-22) | Previous week review |
| Jan 27 | Insight lifecycle response | Conceptual guidance for #703 |

---

## Recommendations for Weekly Ship

### Narrative Thread

**"The Grammar Becomes Real"** — MUX-IMPLEMENT completion represents the moment when months of design work became testable product. The grammar isn't just philosophy anymore; it's running code that shapes user experience.

### Sobering Note

Include the alpha testing lesson: our test suite creates confidence, but alpha testing creates truth. Two days of testing exposed not just bugs, but a critical multi-tenancy gap that could have led to user data exposure. The Jan 29 discovery that calendar tokens were stored globally is a near-miss we should acknowledge.

### Forward Look

- Multi-tenancy audit required before expanding alpha
- Mobile PoC validation in progress
- Pattern-045 gaps still present (alpha testing confirmed them again)
- Root causes found on Jan 29 — fixes verified — but systematic audit needed

---

## Items Still Tracking

| Item | Status | Notes |
|------|--------|-------|
| Pattern-045 (Discovery UX) | Gap remains | Alpha testing confirmed — new users hit walls |
| Conversational glue | Spec complete | Ready for #427 Phase 3 when unblocked |
| Stage 3→4 trust signal | Design needed | Awaiting intent patterns |
| Mobile PoC | In validation | PM carrying device through Jan 27-30 |
| Multi-tenancy audit | **NEW - CRITICAL** | #734 exposed global token storage |
| pipermorgan.ai website | Deferred | Discussion scheduled for tomorrow with Comms Chief |

---

*CXO Weekly Summary | January 23-29, 2026*
*Updated: January 30, 2026 6:15 PM — added January 29 omnibus data*
