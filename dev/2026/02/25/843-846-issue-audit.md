# Audit: #843-846 Issue Descriptions against e2e-bug template

**Template**: `.github/ISSUE_TEMPLATE/e2e-bug.md`
**Date**: 2026-02-25
**Auditor**: Lead Developer

---

## Issue #843: BUG: Calendar queries fail silently despite passing connection test

### Template Compliance

| # | Template Requirement | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Title format `[E2E] [Component]` | ❌ | Uses `BUG:` prefix, not `[E2E]` |
| 2 | Component named | ⚠️ | Implicit (calendar) but not in structured field |
| 3 | Brief summary | ✅ | Clear one-sentence summary |
| 4 | Steps to reproduce | ❌ | Missing. Only shows input/output examples |
| 5 | Reproducibility | ❌ | Not stated (Always? Sometimes?) |
| 6 | Expected behavior | ✅ | "Calendar queries should return actual events" |
| 7 | Actual behavior | ✅ | Specific response quoted |
| 8 | Environment - Browser | ❌ | Missing |
| 9 | Environment - OS | ❌ | Missing |
| 10 | Environment - Test Data State | ⚠️ | Account named (alfamux) but setup not described |
| 11 | Environment - URL | ❌ | Missing |
| 12 | Evidence - Screenshots | ❌ | Missing |
| 13 | Evidence - Console Errors | ❌ | Missing |
| 14 | Evidence - Network Logs | ❌ | Missing |
| 15 | Evidence - Backend Logs | ❌ | Missing — this is critical for silent failures |
| 16 | Initial Categorization | ❌ | Not categorized (Domain? Integration? Infrastructure?) |
| 17 | Severity | ❌ | No severity checkbox marked |
| 18 | Investigation Status | ❌ | Missing checklist |

**Score**: 3/18 ✅, 2/18 ⚠️, 13/18 ❌

### Root Cause Assessment

**Issue claims**: "Likely failure points: Intent routing, calendar service invocation, response generation, token retrieval"

**Investigation found**: The error message comes from `orchestrator.py:278` — the multi-intent orchestrator's failure branch. This means:
- Intent routing IS reaching the calendar handler (otherwise no orchestrator involvement)
- The handler itself is FAILING and the orchestrator catches it
- The "connection test passing" clue is important — connection test uses a different code path than actual query execution

**CRITICAL**: The issue's analysis section lists 4 possible causes but doesn't investigate any of them. It also speculates about #839 keychain (which doesn't exist — probably means #849). Our investigation found that keychain calls are internally consistent (f-string on both sides), so the failure is NOT keychain mismatch.

**Real root cause needs investigation**: The calendar handler is throwing an exception during query execution. We need to find WHERE in the handler pipeline it fails. Candidates:
- MCP adapter authentication (OAuth token refresh failure)
- MCP server connection (tool invocation failure)
- Date parsing / query construction
- Missing Google Calendar API scope

**Verdict**: Issue identifies symptoms but not root cause. The "Analysis" section is speculative without evidence.

### Acceptance Criteria Assessment

Current criteria:
1. "Calendar query returns actual events" — ⚠️ Tests symptom, not root cause
2. "Failure produces diagnostic log entries" — ✅ Good, addresses silent failure aspect
3. "Works for alfamux account specifically" — ❌ Too narrow; should work for all users

**Missing criteria**:
- Error path should not produce misleading "I'll keep trying" message
- Connection test should verify the same path as actual queries (or warn about gap)
- Root cause diagnostic should be logged with specific failure point

### Cross-Issue Analysis

#843 may overlap with **#849 Category A** (calendar user_id threading). If user_id wasn't being passed to the adapter before #849, the adapter would use `self._user_id = None`, causing the scoped key lookup to fail AND the fallback to try the legacy `"google_calendar"` key. If no legacy key exists (user set up after multi-tenancy), both lookups fail → authentication fails → handler throws → orchestrator catches → generic error message.

**This means #843 MAY already be fixed by #849.** This needs live testing to confirm.

---

## Issue #844: BUG: Soft invocation not triggering for implied workflow needs

### Template Compliance

| # | Template Requirement | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Title format `[E2E] [Component]` | ❌ | Uses `BUG:` prefix |
| 2 | Component named | ⚠️ | References #767 but no structured field |
| 3 | Brief summary | ✅ | Clear |
| 4 | Steps to reproduce | ❌ | Single input/output, no reproduction steps |
| 5 | Reproducibility | ❌ | Not stated |
| 6 | Expected behavior | ✅ | With example output |
| 7 | Actual behavior | ✅ | "Generic priority guidance response" |
| 8 | Environment - Browser | ❌ | Missing |
| 9 | Environment - OS | ❌ | Missing |
| 10 | Environment - Test Data State | ❌ | Missing |
| 11 | Environment - URL | ❌ | Missing |
| 12 | Evidence - Screenshots | ❌ | Missing |
| 13 | Evidence - Console Errors | ❌ | Missing |
| 14 | Evidence - Network Logs | ❌ | Missing |
| 15 | Evidence - Backend Logs | ❌ | Missing |
| 16 | Initial Categorization | ❌ | Not categorized |
| 17 | Severity | ❌ | No severity checkbox |
| 18 | Investigation Status | ❌ | Missing checklist |

**Score**: 3/18 ✅, 1/18 ⚠️, 14/18 ❌

### Root Cause Assessment

**Issue claims**: "SoftInvocationDetector.detect() not matching input against trigger patterns" and "trigger patterns too narrow"

**Investigation found**: The OPPOSITE — patterns DO match "I really need to get the team aligned". The real bug is **pipeline gap**: `_apply_soft_offer()` is only called after canonical handlers and orchestrator, but NOT after STRATEGY/QUERY/EXECUTION/ANALYSIS/SYNTHESIS/LEARNING/UNKNOWN handlers. "Q3 planning process" gets classified as STRATEGY, which bypasses the soft offer injection entirely.

**Verdict**: Issue misidentifies the root cause. It assumes the problem is in detection (patterns), but the problem is in **application** (pipeline). The detection works; the result is never used.

### Acceptance Criteria Assessment

Current criteria:
1. "Specific input triggers soft offer" — ⚠️ Tests one case, not the structural gap
2. "Soft offers appear naturally for implied needs" — ⚠️ Vague, not measurable
3. "Colleague Test: response feels like helpful colleague" — ❌ Subjective, not automated

**Missing criteria**:
- `_apply_soft_offer()` must be called for ALL intent categories, not just canonical + orchestrator
- STRATEGY-classified messages should also receive soft offers
- Test coverage for soft offer injection in each handler path

### Cross-Issue Analysis

This overlaps with **#850** (GLUE-SOFTINVOKE coverage gaps) — #850 was filed about pattern gaps, but the real issue is pipeline gaps. The two issues should be consolidated or #844 should be reframed as the pipeline fix and #850 as the pattern expansion.

---

## Issue #845: BUG: 'Open issues' query classified as projects domain

### Template Compliance

| # | Template Requirement | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Title format `[E2E] [Component]` | ❌ | Uses `BUG:` prefix |
| 2 | Component named | ⚠️ | "Intent classification" mentioned in analysis |
| 3 | Brief summary | ✅ | Clear |
| 4 | Steps to reproduce | ❌ | No steps, just one input/output |
| 5 | Reproducibility | ❌ | Not stated |
| 6 | Expected behavior | ✅ | Two-option expected behavior (good) |
| 7 | Actual behavior | ✅ | Specific wrong output quoted |
| 8 | Environment - Browser | ❌ | Missing |
| 9 | Environment - OS | ❌ | Missing |
| 10 | Environment - Test Data State | ❌ | Missing (important — is GitHub connected?) |
| 11 | Environment - URL | ❌ | Missing |
| 12 | Evidence - Screenshots | ❌ | Missing |
| 13 | Evidence - Console Errors | ❌ | Missing |
| 14 | Evidence - Network Logs | ❌ | Missing |
| 15 | Evidence - Backend Logs | ❌ | Missing |
| 16 | Initial Categorization | ❌ | Not categorized |
| 17 | Severity | ❌ | No severity checkbox |
| 18 | Investigation Status | ❌ | Missing checklist |

**Score**: 3/18 ✅, 1/18 ⚠️, 14/18 ❌

### Root Cause Assessment

**Issue claims**: "Intent classifier conflating 'issues' with 'projects'" and "may need disambiguation logic"

**Investigation found**: The pre_classifier HAS correct patterns for `list_issues_query` in `GITHUB_QUERY_PATTERNS`. The `pre_classify()` method correctly classifies this input. BUT `_get_github_action()` (used by `detect_multiple_intents()`) is **missing the `list_issues_query` case** and falls through to default `review_issue_query`. When `review_issue_query` can't find an issue number in the input, it requires clarification, which cascades to projects.

**Verdict**: Issue correctly identifies the symptom (misclassification) but not the root cause (incomplete `_get_github_action()` method). It's not a "conflation" problem — it's a missing code path.

### Acceptance Criteria Assessment

Current criteria:
1. "Does NOT return project information" — ⚠️ Tests symptom only
2. "Classified in correct domain" — ✅ Good

**Missing criteria**:
- `_get_github_action()` must handle `list_issues_query` action
- `detect_multiple_intents()` must produce same classification as `pre_classify()` for this input
- Test: "How many open issues?" → action=`list_issues_query`, not `review_issue_query`
- A handler for `list_issues_query` must exist and produce useful output

### Cross-Issue Analysis

This overlaps with **#851** (INTENT-COVERAGE: Pre-classifier pattern gaps). #851 was filed about missing patterns for entity types, but #845's problem isn't a pattern gap — it's a routing gap inside an existing handler.

**Important**: Fixing `_get_github_action()` is necessary but not sufficient. There also needs to be a handler for `list_issues_query` that actually returns issue counts. If that handler doesn't exist, fixing the routing just moves the failure point.

---

## Issue #846: BUG: 'Yes' confirmation interpreted as greeting

### Template Compliance

| # | Template Requirement | Status | Notes |
|---|---------------------|--------|-------|
| 1 | Title format `[E2E] [Component]` | ❌ | Uses `BUG:` prefix |
| 2 | Component named | ⚠️ | "Intent classification" in analysis but not structured |
| 3 | Brief summary | ✅ | Clear and specific |
| 4 | Steps to reproduce | ⚠️ | Context described (two-turn conversation) but not formal numbered steps |
| 5 | Reproducibility | ❌ | Not stated |
| 6 | Expected behavior | ✅ | Clear |
| 7 | Actual behavior | ✅ | Specific wrong response quoted |
| 8 | Environment - Browser | ❌ | Missing |
| 9 | Environment - OS | ❌ | Missing |
| 10 | Environment - Test Data State | ❌ | Missing (critical — offer state) |
| 11 | Environment - URL | ❌ | Missing |
| 12 | Evidence - Screenshots | ❌ | Missing |
| 13 | Evidence - Console Errors | ❌ | Missing |
| 14 | Evidence - Network Logs | ❌ | Missing |
| 15 | Evidence - Backend Logs | ❌ | Missing |
| 16 | Initial Categorization | ❌ | Not categorized |
| 17 | Severity | ❌ | No severity checkbox |
| 18 | Investigation Status | ❌ | Missing checklist |

**Score**: 3/18 ✅, 2/18 ⚠️, 13/18 ❌

### Root Cause Assessment

**Issue claims**: Four possible failure points including "intent classifier treating 'yes' as greeting without context" and "pending offer state not consulted"

**Investigation found**: The pending offer mechanism (WorkflowOfferService) works correctly in unit tests. `detect_offer_response("yes")` correctly returns "accept". The order of operations is correct (offer check BEFORE classification). BUT the pending offer is not found because:
1. **Composite key mismatch**: If user_id changes between Turn 1 (store) and Turn 2 (retrieve) — e.g., `alice:session` vs `anonymous:session` — the key doesn't match
2. **In-memory storage**: The `_pending_offers` dict doesn't survive instance restarts or multi-instance deployments

**Verdict**: Issue correctly suspects "pending offer state not consulted" but doesn't identify WHY. The mechanism exists and is wired correctly — the persistence is what's broken. This is a **state persistence** bug, not a **classification** bug.

### Acceptance Criteria Assessment

Current criteria:
1. "'yes' following offer is interpreted as confirmation" — ✅ Good outcome test
2. "Confirmation triggers the offered action" — ✅ Good end-to-end test
3. "Works for: 'yes', 'yeah', 'sure', 'ok'" — ⚠️ Tests variations but not the persistence root cause

**Missing criteria**:
- Pending offer survives across conversation turns (same session)
- Pending offer survives instance restart / multi-process routing
- Composite key is stable across turns (user_id doesn't change)
- Test: set offer on Turn 1 → retrieve on Turn 2 with same session → found

### Cross-Issue Analysis

This is exactly what **#852** (CONV-CONTEXT-OFFER) was designed to fix. The architect's `last_offer` on ConversationContext would persist offer state in the same store as conversation context (likely DB-backed), solving both the in-memory and key-mismatch problems.

**However**: #852 is designed as a broader conversation context enhancement, not specifically a persistence fix. The minimal fix for #846 is much smaller — ensure user_id is consistent across turns for the same session, or use session_id alone as the offer key.

---

## Cross-Issue Systemic Analysis

### Are these independent bugs?

**No.** They cluster into two deeper problems:

**Problem 1: Pipeline Incompleteness** (affects #844, #845)
- The intent processing pipeline has multiple handler branches (STRATEGY, QUERY, EXECUTION, etc.)
- Features like soft invocation (#844) and GitHub action routing (#845) are only wired into SOME branches
- When a feature works in one branch but not another, it looks like "the feature doesn't work" — but really the feature is partially wired

**Problem 2: State Continuity Across Turns** (affects #843, #846)
- #843: Calendar fails because user_id threading was incomplete (before #849 Category A fix) — state (user identity) didn't flow through the call chain
- #846: Offer state doesn't persist across turns because of key mismatch / in-memory storage
- Both are "the system can't remember context across boundaries" bugs

### What acceptance criteria should really look like

Instead of testing individual symptoms, criteria should test:
1. **Pipeline completeness**: Soft offers appear regardless of intent category
2. **Classification consistency**: `detect_multiple_intents()` matches `pre_classify()` for the same input
3. **State persistence**: Offers set on Turn N are retrievable on Turn N+1
4. **User identity continuity**: user_id is stable and consistent across all operations in a session

### Relationship to existing issues

| Bug | True Root Cause | Overlaps With |
|-----|----------------|---------------|
| #843 | Calendar handler failure (needs live test to determine if #849 fixed it) | #849 Category A |
| #844 | _apply_soft_offer() not called for non-canonical handlers | #850 (but #850 misidentifies as pattern gap) |
| #845 | _get_github_action() incomplete | #851 (but #851 misidentifies as pattern gap) |
| #846 | Pending offer persistence / key stability | #852 |
