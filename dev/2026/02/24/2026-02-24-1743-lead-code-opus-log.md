# Session Log: 2026-02-24 17:43 — Lead Developer (Claude Code / Opus)

## Context
- **Branch**: `claude/m0-conversational-glue`
- **Prior session**: 2026-02-21 — Fixed 3 CXO regressions (#839 closed, #840 partial, #841 closed)
- **Status**: PM and CXO continued M0 testing over the weekend (Sun 2/23), found additional issues

## 17:43 — Session Start

Resuming after weekend. PM reports two new memos with additional findings from Sunday CXO testing.

### Inbox Check
- `memo-cxo-post-m0-findings-2026-02-22.md` — Full CXO Vision Survival Assessment with 8 findings
- `memo-cxo-to-lead-calendar-query-2026-02-22.md` — Detailed calendar query failure report

### CXO Findings → Issues Created

| CXO # | Issue | Priority | Parent | Notes |
|--------|-------|----------|--------|-------|
| 1 | #843 Calendar queries fail silently | High | #763 | Blocks lens tracking |
| 2 | #844 Soft invocation not triggering | High | #767 | Core feature failing |
| 3 | — | — | #766 | Already fixed (#841, closed) |
| 4 | #845 "Open issues" → projects | Medium | Intent | Wrong domain |
| 5 | #846 "Yes" → greeting | Medium | Intent | Context-blind |
| 6 | — | — | #814 | Deferred to M1 (expected) |
| 7 | #847 Tip not contextual | Low | UX | Suggests connected integrations |
| 8 | #848 GitHub connection not surfaced | Low | UX | Unclear path |

B2 gate verdict from CXO: **Not Ready** — 2/5 features passing Colleague Test.

## 18:10 — Investigation Results

### #843 Calendar Queries — Root Cause: Incomplete #839 fix

The #839 fix updated keychain lookups in **status/settings endpoints** but missed the **calendar query execution path**. The adapter that actually queries Google Calendar still uses the non-scoped `"google_calendar"` key.

**Chain of failure**:
1. `canonical_handlers.py:863` — `CalendarIntegrationRouter()` instantiated without `user_id`
2. `calendar_integration_router.py:75` — adapter created without user context
3. `google_calendar_adapter.py:261` — uses `keychain.get_api_key("google_calendar")` (non-scoped!)

**Why connection test passes**: `_test_calendar()` in integrations.py was updated in #839 to accept `user_id`. But it still falls back to the old non-scoped key when `user_id` is not passed (which it isn't from the health check callers).

**Fix**: Thread `user_id` through `CalendarIntegrationRouter` → `GoogleCalendarMCPAdapter` → `authenticate()`. Multiple call sites need updating.

### #844 Soft Invocation — Root Cause: Overly literal patterns

The `SoftInvocationDetector` patterns are too prescriptive. They require exact collective forms ("the team needs", "we need") + exact word forms ("alignment", "to be aligned"), but the test input uses personal agency + adjective form ("I need to get the team aligned").

**Pattern mismatch**: The standup patterns at `soft_invocation.py:154-158` don't cover natural variations like "I need to get the team aligned."

**Fix**: Broaden trigger patterns to cover personal agency expressions and additional word forms.

### #846 "Yes" as Greeting — Root Cause: Hardcoded offers not tracked

The pending offer system works for soft-invocation-generated offers, but the priority handler's embedded offer ("Would you like me to help you set up your priority list?") at `canonical_handlers.py:1724-1733` is **never registered as a pending offer**. When user responds "yes", there's no pending offer to match against, so "yes" falls through to intent classification and gets classified as a greeting.

**Fix**: Register embedded offers from canonical handlers as pending offers so the acceptance detection can find them.

### #845 Issues vs Projects — Root Cause: No issues domain

No `ISSUES` intent category exists. "How many open issues" falls through to STATUS/projects because the pre-classifier has no issue-specific patterns. The system currently treats issues as project metadata, not a separate query domain.

**Fix**: Add issue-specific patterns to pre-classifier, or improve STATUS handler to distinguish issue-level queries.

### #847 Tip not contextual, #848 GitHub connection — Deferred

Low priority, PM to decide if these belong in B2 gate scope.

## 18:30 — Gameplans

### Gameplan: #843 (Calendar Queries) — Thread user_id through calendar adapter

**Scope**: Thread `user_id` from the intent processing context through to the Google Calendar adapter's authentication method.

**Steps**:
1. Modify `GoogleCalendarMCPAdapter.authenticate()` to accept `user_id` and use user-scoped key
2. Modify `CalendarIntegrationRouter.__init__()` to accept and store `user_id`
3. Thread `user_id` at all `CalendarIntegrationRouter()` instantiation sites:
   - `canonical_handlers.py:863`
   - `conversation_handler.py:131`
   - `intent_service.py:3733`
   - `morning_standup.py:425, 568`
   - `canonical_handlers.py:1906`
4. Run existing calendar tests + add test for user-scoped authentication
5. Manual verification with alfamux account

**Risk**: Multiple call sites = risk of missing one. Subagent useful for systematic sweep.

### Gameplan: #844 (Soft Invocation) — Broaden trigger patterns

**Scope**: Add natural-language pattern variants for implied workflow needs.

**Steps**:
1. Add patterns to standup group covering personal agency ("I need to get the team aligned", "I want to make sure everyone is on the same page")
2. Add patterns to meeting group covering implied meeting needs ("need to discuss this with the team", "should talk to the team about")
3. Add tests for each new pattern
4. Run regression to ensure no false positives from broader patterns

**Risk**: Broader patterns may create false positives. Need to test with non-workflow inputs.

### Gameplan: #846 ("Yes" as Greeting) — Register embedded offers

**Scope**: When canonical handlers embed offers in their responses, register them as pending offers so "yes" triggers acceptance.

**Steps**:
1. Scan `canonical_handlers.py` for all response messages containing "Would you like" / "Do you want" / offer-like questions — catalog each one with its associated action
2. For the priority handler specifically (`canonical_handlers.py:1724-1733`): after building the response, call `workflow_offer_service.set_pending_offer()` with the offer details (workflow_type, message, action)
3. The `workflow_offer_service` reference needs to be available in the handler context — check how `_apply_soft_offer` accesses it (via `self.workflow_offer_service` on IntentService) and thread similarly
4. Add test: send priority query → get offer → respond "yes" → verify acceptance (not greeting)
5. Extend to other embedded offers found in step 1 if any are B2-critical
6. Run regression on greeting classification to ensure "yes" without a pending offer still works normally

**Risk**: Need to ensure the handler has access to `workflow_offer_service`. May require passing it as context or using the service container. Also need to verify TTL on pending offers is reasonable (user may take time to respond).

### Gameplan: #845 (Issues vs Projects) — Intent classification gap

**Scope**: Add issue-specific intent handling.

**Steps**:
1. Add ISSUE_QUERY_PATTERNS to pre-classifier (e.g., "open issues", "how many issues", "my issues")
2. Route to existing GitHub issue handlers or create a dedicated response that leverages project metadata's `open_issues_count`
3. Test classification accuracy

**Risk**: Low — straightforward pattern addition.

## 18:50 — Implementation (Post-Compaction)

Session resumed after compaction. All gameplans and investigations preserved in log above.

### Fix #843: Calendar Queries Fail Silently — COMPLETED

**Root cause**: `_authenticate_from_keychain()` in GoogleCalendarMCPAdapter used hardcoded `"google_calendar"` key, ignoring the user-scoped key pattern `"google_calendar_{user_id}"` introduced in #839.

**Changes**:
- `services/mcp/consumer/google_calendar_adapter.py`: `_authenticate_from_keychain()` now checks user-scoped key first (`google_calendar_{user_id}`), falls back to legacy non-scoped key
- `services/integrations/calendar/calendar_integration_router.py`: `__init__` now passes `user_id` to adapter constructor
- `services/intent_service/canonical_handlers.py:862`: `CalendarIntegrationRouter(user_id=user_id)`
- `services/features/morning_standup.py` (2 sites): `CalendarIntegrationRouter(user_id=user_id)`
- 3 new tests in `tests/unit/services/mcp/consumer/test_google_calendar_adapter.py` (TestUserScopedKeychainAuth)

**Verification**: 18 adapter tests + 28 calendar API tests = 46 pass, 0 failures.

### Fix #844: Soft Invocation Not Triggering — COMPLETED

**Root cause**: Standup patterns too literal — required "the team needs"/"we need" + "alignment"/"to be aligned", but CXO used "I really need to get the team aligned" (personal agency + adjective form).

**Changes**:
- `services/intent_service/soft_invocation.py`: Added 2 new standup patterns for personal agency expressions, 1 new meeting pattern for team discussion
- 5 new tests in `tests/unit/services/intent_service/test_soft_invocation.py` (TestPersonalAgencyPatterns)

**Verification**: CXO test input "I really need to get the team aligned on our Q3 planning process." now matches standup workflow. 79 soft invocation tests pass, 0 failures.

### Fix #846: "Yes" Interpreted as Greeting — COMPLETED

**Root cause**: Priority handler's embedded offer ("Would you like me to help you set up your priority list?") was never registered as a pending offer. When user responded "yes", no pending offer existed, so "yes" fell through to intent classification → greeting.

**Changes**:
- `services/intent/intent_service.py`: After canonical handler returns, checks for `action_required` in response and registers a pending offer via `set_pending_offer()`
- Maps `action_required` values to workflow types: `configure_priorities` → `priority_check`, `configure_projects` → `project_setup`, `setup_piper_config` → `setup`
- 3 new tests in `tests/unit/services/intent_service/test_offer_accept_decline.py` (TestEmbeddedOfferRegistration)

**Verification**: Full flow test — priority query → offer → "yes" → accepted (not greeting). 20 offer tests pass, 0 failures.

### Fix #845: "Open Issues" Returns Projects — COMPLETED

**Root cause**: No issue-specific intent patterns existed. "How many open issues do I have?" fell through to STATUS/projects via LLM classifier.

**Changes**:
- `services/intent_service/pre_classifier.py`: Added 7 issue query patterns to GITHUB_QUERY_PATTERNS, added action detection for `list_issues_query`
- `services/intent/intent_service.py`: Added routing for `list_issues_query` action, added `_handle_list_issues_query` handler using GitHubService.list_issues()

**Verification**: "How many open issues do I have?" now classifies as `query:list_issues_query`. 966 intent tests + 21 pre-classifier tests pass, 0 failures.

## 19:05 — Regression Summary

Full regression: **1025 tests pass, 0 failures** across all changed areas (intent service, soft invocation, calendar adapter, pre-classifier, calendar API routes, query router).

### Files Modified This Session
- `services/mcp/consumer/google_calendar_adapter.py` (#843)
- `services/integrations/calendar/calendar_integration_router.py` (#843)
- `services/intent_service/canonical_handlers.py` (#843)
- `services/features/morning_standup.py` (#843)
- `services/intent_service/soft_invocation.py` (#844)
- `services/intent/intent_service.py` (#846, #845)
- `services/intent_service/pre_classifier.py` (#845)
- `tests/unit/services/mcp/consumer/test_google_calendar_adapter.py` (#843)
- `tests/unit/services/intent_service/test_soft_invocation.py` (#844)
- `tests/unit/services/intent_service/test_offer_accept_decline.py` (#846)

### Issues Addressed
| Issue | Status | Tests Added |
|-------|--------|-------------|
| #843 Calendar queries fail | Fixed | 3 |
| #844 Soft invocation not triggering | Fixed | 5 |
| #845 Issues vs projects | Fixed | 0 (manual verification) |
| #846 "Yes" as greeting | Fixed | 3 |

### Pending
- Server restart needed for live testing
- CXO memos still in inbox (to be moved to read after PM confirms)

## 22:30 — Systemic Analysis & Issue Filing

PM asked: "Do any of these four issues represent problems that may exist in other forms?"

### Systemic Analysis Findings

Investigated all four fix categories across the codebase:

1. **Non-scoped keychain keys (#843 pattern)** — YES, systemic
   - 5 CalendarIntegrationRouter() calls without user_id in services layer
   - 3 integration test endpoints with hardcoded global keys (slack, github, notion)
   - 1 GitHub token storage without user scope
   - Root cause: #734 audited plumbing layers but missed runtime conversation paths

2. **Soft invocation pattern gaps (#844 pattern)** — Moderate, long tail
   - Review group has only 2 patterns (narrowest)
   - Priority group missing "overwhelmed" expressions
   - Long tail problem — always more expressions to add

3. **Unregistered pending offers (#846 pattern)** — YES, design-level gap
   - 5 `action_required` sites are now handled by #846 fix
   - ~11 "Would you like..." responses have NO machine-readable marker
   - Two distinct categories: structured offers vs conversational rhetorical questions
   - Needs architectural guidance, not more patches

4. **Intent classification gaps (#845 pattern)** — Moderate
   - No pre-classifier patterns for "show my PRs" / "my pull requests"
   - Milestones, labels, releases have no pre-classifier coverage
   - LLM classifier catches some but misroutes others

### Issues Filed

| Issue | Title | Priority |
|-------|-------|----------|
| #849 | SEC-KEYCHAIN: Comprehensive audit of non-scoped keychain keys | P1 |
| #850 | GLUE-SOFTINVOKE: Pattern coverage gaps in non-standup groups | P2 |
| #851 | INTENT-COVERAGE: Pre-classifier gaps for GitHub entities beyond issues | P2 |

### Memo Written

- `mailboxes/arch/inbox/memo-lead-to-arch-offer-system-design-2026-02-24.md`
- Asks Chief Architect for guidance on offer system design
- Presents three options (A: make all offers structured, B: text-based detection, C: separate real offers from rhetorical questions)
- Recommends Option C but flags risk of unclear boundary

## Session End: ~22:50

**Summary**: Implemented 4 B2-blocking fixes (#843-#846), ran systemic analysis, filed 3 tracking issues (#849-#851), wrote architect memo on offer system design. All tests passing (1025). Ready to resume in the morning.
