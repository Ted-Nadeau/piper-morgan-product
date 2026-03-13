# Session Log: 2026-02-21 10:24 — Lead Developer (Claude Code, Opus)

**Branch**: `claude/m0-conversational-glue`
**Sprint**: M0 Conversational Glue
**Previous session**: 2026-02-19

---

## 10:24 — Session Start

### Inbox Review (3 memos)

1. **Architect → Lead: Unified Formality Design (#823)**
   - All 5 design questions answered
   - Decision: PersonalityProfile = baseline, WarmthCalibration = modulator (±0.2 range)
   - Continuous 0.0-1.0 scale with presentation labels (warm/balanced/professional)
   - Load at request boundary, pass through pipeline
   - **Action**: Close #823, create FORM-UNIFIED issue for M1/M2
   - No code changes needed for alpha

2. **Docs → Lead: Entity Tokens Complete (#818)**
   - Section 5.8 added to Conversational Glue Implementation Guide
   - Clarifies entity echoing ≠ parrot confirmation
   - **Action**: Review if code changes needed, close #818 if docs-only suffices

3. **Docs → Lead: M0 Gate Blockers**
   - 4 issues remain: #813 (test bug), #814 (onboarding trigger), #818 (entity tokens), #823 (formality)
   - PM wants to close gate this weekend

### Current state: 4 issues to resolve before gate #779 closure

---

## 10:30 — #818 Closed (Docs-Only Resolution)

Verified section 5.8 exists in implementation guide. No code changes needed — entity echoing is correct behavior, not parrot confirmation. Description updated, comment added, issue closed. ✅

## 10:34 — #813 Fixed (Test Mock Bug)

**Root cause**: `mock_services` fixture set `conversation_manager = AsyncMock()` without configuring `get_conversation_context`. The bare AsyncMock propagated coroutine objects into `ConversationState.created_at`, crashing `_calculate_conversation_age()` when it tried `datetime - AsyncMock`.

**Fix**: Set `conversation_manager.get_conversation_context.return_value = None` in fixture. Forces code to take "create new" branch with real datetime defaults.

**Audit cascade**: Searched all test files for same bare AsyncMock pattern — only one instance. All 17 tests in file pass. Commit `ad56b1f6`. Issue closed. ✅

## 10:40 — #823 Closed, FORM-UNIFIED #838 Created

Closed #823 with architect resolution. Created **#838** (FORM-UNIFIED) with:
- Full architect design decisions baked in
- Acceptance criteria (10 items)
- Gameplan with 3 phases: Foundation (sequential) → Consumers (parallelizable) → Verification
- Subagent plan: 3 parallel subagents for Phase 2 (WarmthCalibration, SoftInvocation, SlotFilling)
- TDD cross-checking strategy

**PM to decide**: execute now or schedule for M1.

## 10:50 — #814 Design Memo to CXO+PPM

Wrote memo requesting design guidance for #814 (setup trigger from natural language).

Key insight from PM: users can't chat until initial setup wizard is complete. This eliminates System A (wizard) from conversational scope entirely. All "set up" messages in chat are either:
- **Portfolio setup** → trigger conversational onboarding (System B)
- **Integration reconfiguration** → warm redirect to settings/setup page

3 remaining design questions sent to CXO+PPM:
1. Should this block M0 gate or defer to M1?
2. What to say when user already has projects?
3. UX for integration reconfiguration (link vs soft offer)

Memos delivered to `mailboxes/cxo/inbox/` and `mailboxes/ppm/inbox/`.

### Current state: 2 of 4 blocking issues resolved (#818, #813). #823 closed with deferred implementation (#838). #814 awaiting product guidance.

---

## 10:55 — #838 Execution Started (PM directed: execute now)

PM directed: "Please execute #838 now while I get feedback re #814."

### Phase 1: Foundation (sequential)
- **1a**: Created `services/personality/formality.py` — `formality_label()`, `apply_context_adjustment()`, `ONBOARDING_TIER_TO_WARMTH`, constants
- **1b**: Added `formality_baseline: Optional[float]` to `RequestContext` in `services/domain/models.py`
- **1c**: Wired PersonalityProfile loading at request boundary in `intent_service.py`
- **1d**: Wired onboarding formality persistence in `_persist_onboarding_projects()`

### Phase 2: Consumers (3 parallel subagents)
- **Subagent A (WarmthCalibrator)**: Baseline-aware level determination with +1 context shift cap. SUPPORTIVE reserved for context triggers only. 30 new tests, all 42 pass.
- **Subagent B (SoftInvocation)**: Warm/balanced/professional offer and decline messages for all 7 workflow types. 33 new tests, all 128 pass.
- **Subagent C (SlotFilling)**: `_SLOT_MESSAGES` dict + `_slot_message()` helper for formality-tier system messages. 17 new tests, all 182 pass.

### Phase 2.5: Threading (lead)
Threaded `formality_baseline` through `_apply_soft_offer()` to `detect()`, `format_acceptance()`, `start_filling()`. Moved baseline loading to top of `_process_intent_internal()` so it's available before pending offer handling.

### Phase 3: Verification
- 1294 tests in affected directories — ALL PASS
- 900+ broader unit tests — ALL PASS (DB-dependent tests excluded due to Docker not running)
- 0 regressions

**Commit**: `9f795322`. Issue #838 closed with full evidence. ✅

### Current state: 3 of 4 blocking issues resolved (#818, #813, #823→#838). #814 awaiting product guidance.

---

## 12:04 — #814 Design Guidance Received (CXO + PPM)

Both advisors aligned on all three questions:
- **Q1**: Defer to M1 (not a gate blocker)
- **Q2**: Option C — acknowledge existing projects + offer choice
- **Q3**: Option B — warm redirect with continuity (CXO) + agency (PPM) — complementary

Updated #814 description with full design decisions, routing table, and implementation notes. PM assigned to M1.

## 12:12 — Session Paused

All 4 original M0 gate blockers resolved:
- **#818** ✅ Closed (docs-only)
- **#813** ✅ Closed (test mock fix, commit `ad56b1f6`)
- **#823→#838** ✅ Closed (FORM-UNIFIED implemented, commit `9f795322`)
- **#814** ✅ Deferred to M1 (CXO + PPM consensus)

PM and CXO reviewing experience for model-flattening before approving gate #779. Standing by for results or issues.

---

## 1:23 PM — Fresh Server for CXO Testing

Killed existing Piper process, started fresh `python main.py` on port 8001.

## 5:13 PM — CXO Testing Found 3 Regressions

PM reported regressions discovered during Post-M0 CXO review with fresh alpha account (`onemvp`). Read memo from CXO inbox.

### Issues Created
- **#839** (P1): Calendar settings showing connected for fresh alpha account
- **#840** (P1): Conversation not appearing in history sidebar
- **#841** (P2): Slot-filling fails to extract entity name from natural sentence ("Yes, I have another one called Dynamic Atlas")

### Investigations & Fixes

**#841 — Slot-filling extraction (CLOSED)**
- **Root cause**: `CONFIRM_PATTERNS` checked before `_extract_project_info()` in `_handle_gathering()`. "Yes" swallowed embedded project name.
- **Fix**: When CONFIRM_PATTERNS match, also attempt extraction. Added `source` key ("pattern" vs "fallback") to `_extract_project_info()` to distinguish real extractions from raw-text fallback.
- **Files**: `services/onboarding/portfolio_handler.py`
- **Tests**: 202 onboarding tests passing

**#839 — Calendar cross-user leakage (CLOSED)**
- **Root cause**: Tokens stored with user-scoped key (`google_calendar_{user_id}`) but retrieved with non-scoped key (`google_calendar`). Any user's token made all users appear connected.
- **Fix**: Updated 6 endpoints across 3 route files to use user-scoped keys. Added `current_user` dependency where missing. Setup wizard uses JWT cookie extraction with graceful fallback.
- **Files**: `web/api/routes/setup.py`, `web/api/routes/settings_integrations.py`, `web/api/routes/integrations.py`, 2 test files
- **Tests**: 314 web tests passing, 2 new scoping tests added

**#840 — Conversation history (OPEN — partial fix)**
- **Root cause**: `ensure_conversation_exists()` had `user_id or conversation_id` fallback creating conversations with wrong user_id → invisible in `list_for_user()`. Also identified multi-session coordination issue.
- **Fix**: Changed fallback to `user_id or "unknown"` with warning log. Multi-session coordination deferred — needs live testing.
- **Files**: `services/database/repositories.py`

### Regression Tests
- **5146 unit tests passing** (only pre-existing failures: `test_history_sidebar`, `test_demo_plugin`, DB-dependent tests)

## 6:35 PM — Session End

Restarted server for PM to resume testing Sunday.

### Day Summary
- **#838 FORM-UNIFIED**: Fully implemented and closed (80 new tests, commit `9f795322`)
- **#814**: Design decisions documented from CXO+PPM, deferred to M1
- **#839**: Fixed and closed (calendar cross-user data leakage)
- **#840**: Partially fixed (user_id fallback), open pending live testing
- **#841**: Fixed and closed (slot-filling extraction in onboarding)
- **M0 gate blockers**: All 4 resolved (#818, #813, #823→#838, #814→M1)
- **Discovered work**: 0 new issues beyond CXO findings

### Pending for Sunday
- PM resumes CXO testing with fixes in place
- #840 may need further investigation if conversations still don't appear
- Changes not yet committed (regression fixes) — commit when PM confirms testing results

---
