# Audit Cascade: Issues #247, #739, #738 — Issue → Gameplan Gate

**Date**: 2026-03-13
**Auditor**: Lead Developer (Claude Code Opus)
**Template**: `.github/ISSUE_TEMPLATE/feature.md`

---

## Issue #247: BUG-TEST-ASYNC — AsyncSessionFactory event loop conflicts

### Audit Matrix: #247 against feature.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Title with label | ✅ | `BUG-TEST-ASYNC: AsyncSessionFactory causes event loop conflicts` |
| Priority | ❌ | Not specified |
| Labels | ❌ | No labels assigned |
| Milestone | ✅ | MVP |
| Problem Statement | ✅ | Clear root cause: global db singleton bound to first event loop |
| Impact | ⚠️ | Implied (3 perf tests skip) but not structured per template |
| Goal | ⚠️ | Solution described but not framed as "Primary Objective" |
| What Already Exists | ✅ | Well documented — fix IS implemented |
| Requirements/Phases | ⚠️ | Solution implemented but issue says "FIX IMPLEMENTED" when tests still fail |
| Acceptance Criteria | ❌ | No explicit acceptance criteria |
| Testing Strategy | ⚠️ | Tests exist but blocked by conftest fixture |
| Completion Matrix | ❌ | Not present |
| STOP Conditions | ❌ | Not present |

### Action Items Before Execution

Since this is a **trivial fix** (conftest exclusion), I'm fixing directly rather than full gameplan:

1. **Fix**: Add `performance` to `mock_token_blacklist` keyword exclusion in `tests/conftest.py`
2. **Verify**: Run all 3 performance tests
3. **Update issue**: Add acceptance criteria + evidence
4. **Close**: With test output evidence

### Risk Assessment: LOW
- 2-line code change in test infrastructure only
- No production code affected
- Clear, isolated fix

---

## Issue #739: TEST-FIX — test_response_handler_observability Complex Mocking

### Audit Matrix: #739 against feature.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Title with label | ✅ | `TEST-FIX: Fix test_response_handler_observability Complex Mocking` |
| Priority | ❌ | Not specified |
| Labels | ❌ | No labels assigned |
| Milestone | ✅ | MVP |
| Problem Statement | ✅ | Well documented — complex mocking sync issues with spatial adapter |
| Impact | ⚠️ | 1 skipped test, but impact not structured |
| Goal | ⚠️ | Two fix options described but no clear "Primary Objective" |
| What Already Exists | ✅ | Test exists but is skipped |
| Requirements/Phases | ⚠️ | Two options listed but no phases |
| Acceptance Criteria | ❌ | Not present |
| Testing Strategy | N/A | This IS a test fix |
| Completion Matrix | ❌ | Not present |
| STOP Conditions | ❌ | Not present |

### Action Items Before Execution

Investigation found the test is an **integration test masquerading as a unit test**. Fix:

1. **Rewrite** test to mock `_get_slack_context_from_spatial_event` as a whole method instead of adapter internals
2. **Fix** workflow result structure to match what `_format_response_content` expects
3. **Remove** `@pytest.mark.skip` decorator
4. **Verify**: Test passes
5. **Update issue**: Add evidence
6. **Close**: With test output

### Risk Assessment: LOW
- Test-only change
- Existing test passes (monitoring_intent_bypass, error_observability) stay unchanged
- Mocking at higher level is simpler than current approach

---

## Issue #738: TEST-INFRA — Enable Attention System Time Simulation Tests

### Audit Matrix: #738 against feature.md

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Title with label | ✅ | `TEST-INFRA: Enable Attention System Time Simulation Tests (3 tests)` |
| Priority | ❌ | Not specified |
| Labels | ❌ | No labels assigned |
| Milestone | ✅ | MVP |
| Problem Statement | ✅ | Clear root cause: `default_factory=datetime.now` captures real function at class definition |
| Impact | ⚠️ | 3 skipped tests, but not structured |
| Goal | ⚠️ | Two fix options described (freezegun vs injectable clock) |
| What Already Exists | ✅ | Tests exist but are skipped |
| Requirements/Phases | ⚠️ | Options listed but no phases with tasks |
| Acceptance Criteria | ❌ | Not present |
| Testing Strategy | ⚠️ | Tests themselves are the deliverable |
| Completion Matrix | ❌ | Not present |
| STOP Conditions | ❌ | Not present |

### Action Items Before Execution

freezegun not installed. Using **injectable clock pattern** (Option B):

1. **Modify** `AttentionEvent` dataclass: make `created_at`/`last_updated` accept explicit values OR use a clock factory
2. **Modify** `AttentionModel.create_attention_event()` to accept optional `clock` parameter
3. **Update** `get_current_intensity()` to use injected `now` or `datetime.now()`
4. **Fix** skipped tests to inject controlled time via the new mechanism
5. **Address** additional test-specific issues (context attribute, memory_store setup)
6. **Verify**: All 3 tests pass
7. **Update issue + close**

### Risk Assessment: MEDIUM
- Modifies production code (`attention_model.py`)
- But: only adds optional parameter — all existing callers unaffected (default behavior preserved)
- 3 tests have additional issues beyond time simulation

---

## Audit Summary

| Issue | Template Compliance | Fix Complexity | Approach |
|-------|-------------------|----------------|----------|
| #247 | Partial — missing AC, completion matrix | Trivial (~2 lines) | Direct fix, skip gameplan |
| #739 | Partial — missing AC, completion matrix | Small (test rewrite) | Direct fix, skip gameplan |
| #738 | Partial — missing AC, completion matrix | Medium (prod + test) | Mini-gameplan below |

All three issues were filed as tracking stubs rather than full feature.md-compliant issues. Given the PM directive to execute ("work on those three actionable items"), I'm proceeding with execution and will update each issue with proper evidence at closure.

---

## Mini-Gameplan: #738 (requires production code change)

### Phase 1: Injectable Clock in AttentionEvent
- Add `_clock` class variable to `AttentionModel` (default: `datetime.now`)
- Pass clock to `create_attention_event()` for `created_at`/`last_updated`
- Update `get_current_intensity()` to accept optional `now` parameter

### Phase 2: Fix Skipped Tests
- Test 3 (pattern learning): Inject clock → events get mocked timestamps
- Test 4 (overload): Pre-populate SpatialMemory records before `learn_spatial_pattern`
- Test 5 (cross-workspace): Work with actual AttentionEvent fields, not assumed `context` attribute

### Phase 3: Verify
- All 3 previously-skipped tests pass
- All existing attention tests still pass (regression check)
