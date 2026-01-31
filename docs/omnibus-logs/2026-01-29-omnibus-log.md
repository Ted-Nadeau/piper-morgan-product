# Omnibus Log: January 29, 2026

**Synthesized**: January 30, 2026
**Source Logs**: 3
**Day Rating**: LIGHT-DAY (Alpha Bug Triage + Root Causes Found)

---

## Day Overview

A lighter day focused on continued alpha testing and bug triage. The Lead Developer found root causes for several bugs from Jan 28, applied fixes, and deployed parallel agents for deeper investigation. PM had a brief morning check-in before meetings consumed the day.

### Source Logs

| Time | Role | Duration | Lines | Focus |
|------|------|----------|-------|-------|
| 6:41 AM | Lead Developer | ~2 hrs | 403 | Bug triage, root causes, parallel agents |
| 8:41 AM | Docs Management | ~25 min | 61 | Jan 28 omnibus creation |
| 8:44 AM | Chief of Staff | ~17 min | 102 | Brief morning check-in |

---

## Key Accomplishments

### 1. Bug Root Causes Found

**Conversation persistence (#731)** — FIXED & VERIFIED:
- When users type directly in chat (without "+ New Chat"), no conversation was created in DB
- Fix: Auto-create conversation record in `/api/v1/intent` before processing
- **Verified working** by PM at 8:19 AM

**Projects unique constraint (#736)** — FIXED:
- Root cause of #733 (projects not saving): unique constraint on `name` is GLOBAL, not per-user
- Different users couldn't have projects with same name ("Decision Reviews" already existed from previous user)
- Fix: Migration to composite constraint `(owner_id, name)`
- Migration applied and tested

**History button (#729, #732, #735)**:
- Trust gate was too high (stage 2 → lowered to stage 1)
- But real issue: `HistorySidebar.mount()` never called
- Component included but DOM element never created
- PM question: May be duplicate functionality with left sidebar

**Multi-tenancy gaps (#734)**:
- CRITICAL: Calendar/integration tokens stored globally without user_id prefix
- alfamux user saw previous user's calendar events
- Fix requires threading user_id through ALL storage AND retrieval calls
- Issue created with detailed fix plan

### 2. Parallel Agent Investigation

PM headed to meetings, Lead Dev launched 3 parallel agents:

| Agent | Task | Result |
|-------|------|--------|
| Fix #736 | Migration for composite unique constraint | ✅ Complete, tested |
| Session singleton | Why onboarding sessions disappear | Hypothesis ready, needs runtime verification |
| Terminal log analysis | Review warnings for additional issues | ✅ No new issues needed |

### 3. Documentation

**Jan 28 omnibus created** (Docs agent):
- Synthesized 4 source logs (729 lines)
- Captured MIXED-DAY rating
- Documented the P0 bug discovery and 75% pattern lesson

---

## GitHub Activity

### Issues Closed: 0

No issues formally closed (fixes applied, awaiting verification).

### Issues Created: 7

| Issue | Title | Priority |
|-------|-------|----------|
| #731 | Conversations not persisting when typing directly | P1 |
| #732 | History button trust-gated at wrong level | P2 |
| #733 | Debug: Projects not saving during onboarding | P1 |
| #734 | CRITICAL: Calendar tokens leak between users | P0 |
| #735 | Finish: Mount History sidebar component | P2 |
| #736 | Projects table unique constraint is global | P1 |

*Note: #720-730 were created late Jan 28 (after midnight UTC) but appear as Jan 29 in GitHub.*

---

## Patterns & Observations

### Multi-Tenancy Incomplete

Two critical multi-tenancy bugs found:
1. **#734**: Integration tokens (calendar, GitHub, Slack) stored globally
2. **#736**: Projects unique constraint global instead of per-user

The Oct 2025 multi-user implementation was incomplete — some paths use user scoping, others don't.

### Onboarding Flow Complexity

The onboarding conversation flow has multiple failure points:
1. Only triggers on GREETING intent (not "help me set up projects")
2. Session lookup can fail between messages (singleton issue suspected)
3. Persistence depends on `state == "complete"` AND `captured_projects` in context

Debug logging added to trace exact failure point.

### Two Sidebar Features?

PM asked about History button: "the tab for opening and closing the chat history sidebar works just fine"

There appear to be TWO sidebar features:
1. **Left sidebar** — conversation list (works)
2. **Right History sidebar** (#425) — search, date grouping (never mounted)

May be duplicate functionality needing PM decision.

---

## Cross-Session Threads

### From Jan 28

- 11 bugs found during E2E testing → 7 more issues created Jan 29
- P0 (#728) projects not saving → root cause found (#736 constraint)
- Multi-user gaps → #734 calendar leak discovered

### Pending for Tomorrow

- HOSR review of Cindy/Ted meeting notes
- Roadmap discussion with Lead Dev (after more alpha impressions)
- Continue E2E testing
- pipermorgan.ai website discussion with CXO (when time allows)

---

## Files Changed

### Modified
- `web/api/routes/intent.py` — Auto-create conversation before processing
- `services/onboarding/portfolio_handler.py` — Debug logging
- `services/intent/intent_service.py` — Debug logging for persistence
- `templates/components/navigation.html` — History trust gate 2→1
- `services/database/models.py` — Composite unique constraint

### Created
- `alembic/versions/3c85fd899ece_fix_projects_unique_constraint_736.py`
- `docs/omnibus-logs/2026-01-28-omnibus-log.md`

---

## Metrics

| Metric | Value |
|--------|-------|
| Issues Closed | 0 |
| Issues Created | 7 (#731-736, some timestamped Jan 29) |
| Fixes Applied | 3 (#731, #732, #736) |
| Fixes Verified | 1 (#731) |
| Test Suite | 5253 passed, 24 skipped |
| Parallel Agents | 3 |

---

## Tomorrow's Focus

1. **Verify #736 fix** — Re-test project onboarding with migration applied
2. **Session singleton debug** — Add manager ID to lookup, trace instance mismatch
3. **#734 triage** — Multi-tenancy fix for integration tokens
4. **Continue E2E testing** — More alpha flows to validate

---

*Day rating: LIGHT-DAY — Progress on root causes but PM's day consumed by meetings. Key fixes applied, awaiting verification.*
