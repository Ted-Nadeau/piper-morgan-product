# Phase 2: Smoke Test Marking & Discovery (#277)

**Status**: Ready to Execute
**Assigned to**: Code Agent (Claude Haiku - cost optimization)
**Priority**: P2
**Estimated Effort**: 5-9 hours (can split into sub-sessions)

---

## 🎯 Objective

Expand smoke test coverage from 13 tests (1.8%) to ~100+ tests (15%+), ensuring the full smoke suite executes in <5 seconds total.

**Definition of Done**:
- ✅ ~100-120 tests marked with `@pytest.mark.smoke`
- ✅ Smoke suite execution time verified <5 seconds
- ✅ All marked tests pass
- ✅ Documentation updated with selection criteria

---

## 📋 Work Breakdown

### Phase 2a: Audit & Profiling (2-3 hours)

**Objective**: Identify which tests are fast enough (<500ms) to be smoke candidates.

**Steps**:

1. **Create a profiling script** (`scripts/profile_tests.py`):
   ```python
   # Run each unit test individually and record execution time
   # Output: JSON file with test names and timings
   # Include: test_path, function_name, execution_time_ms, status (pass/fail)
   # Filter to tests in tests/unit/ (705 tests)
   ```

2. **Execute profiling**:
   ```bash
   python scripts/profile_tests.py > test_profile.json
   time: ~10-15 minutes
   ```

3. **Analyze results**:
   ```bash
   # Count tests by speed band
   python -c "
   import json
   with open('test_profile.json') as f:
       tests = json.load(f)

   fast = [t for t in tests if t['time_ms'] < 500]
   medium = [t for t in tests if 500 <= t['time_ms'] < 1000]
   slow = [t for t in tests if t['time_ms'] >= 1000]

   print(f'Fast (<500ms): {len(fast)}')
   print(f'Medium (500-1000ms): {len(medium)}')
   print(f'Slow (>1000ms): {len(slow)}')
   "
   ```

4. **Output**:
   - Identify ~100-150 candidates with <500ms execution
   - Create list of candidates: `dev/2025/12/09/smoke-test-candidates.txt`

**Success Criteria**:
- Profiling completes without errors
- Candidates identified with confirmed <500ms performance
- Documentation shows criteria applied

---

### Phase 2b: Marking & Validation (2-3 hours)

**Objective**: Add `@pytest.mark.smoke` to identified candidates and verify suite performance.

**Steps**:

1. **Mark selected candidates**:
   - Open each test file from candidate list
   - Add `@pytest.mark.smoke` decorator to identified test functions
   - Avoid double-marking (check for existing decorators)
   - Pattern: `@pytest.mark.smoke` immediately before `def test_*`

2. **Update existing smoke tests** (if needed):
   - Verify current 13 smoke tests in `test_slack_components.py` still execute <500ms
   - Check if any need to be moved to `@pytest.mark.unit` if they're >500ms

3. **Validation run**:
   ```bash
   # Full smoke suite
   python -m pytest -m smoke -v --tb=short

   # Measure execution time
   time python -m pytest -m smoke -q

   # Target: <5 seconds total
   # If >5s: identify slowest tests and consider removal/optimization
   ```

4. **Count verification**:
   ```bash
   # Count marked tests
   grep -r "@pytest.mark.smoke" tests/ --include="*.py" | wc -l
   # Target: ~100-120 marked tests
   ```

**Success Criteria**:
- 100-120 tests marked with `@pytest.mark.smoke`
- Full smoke suite runs in <5 seconds
- All marked tests pass without errors
- No regressions in existing tests

---

### Phase 2c: Documentation & Summary (1 hour)

**Objective**: Document selection criteria and create final report.

**Tasks**:

1. **Create smoke test selection criteria document**:
   - File: `dev/2025/12/09/SMOKE-TEST-SELECTION-CRITERIA.md`
   - Content:
     - Why these tests were selected
     - Execution time thresholds used
     - Category breakdown (what types of tests are included)
     - Examples of included vs excluded tests
     - Rationale for boundaries (why <500ms threshold)

2. **Create test marking summary**:
   - File: `dev/2025/12/09/PHASE-2-COMPLETION-REPORT.md`
   - Content:
     - Before/after comparison (13 → ~110 tests)
     - Coverage improvement (1.8% → ~15%)
     - Execution time (baseline → <5 seconds)
     - Any issues encountered
     - Recommendations for next steps

3. **Update pytest.ini documentation**:
   - Add comment explaining smoke test purpose and criteria
   - Reference the selection criteria document

**Success Criteria**:
- Both documents created and comprehensive
- Clear rationale documented
- Ready for handoff to Phase 4 (Epic coordination)

---

## 🎯 Key Constraints & Guidance

### Selection Criteria

**Include in smoke suite**:
- ✅ Tests with <500ms execution time
- ✅ Unit tests (no database dependencies preferred)
- ✅ Pure logic tests (validators, helpers, data models)
- ✅ Critical path tests (as identified)
- ✅ Tests with no external dependencies (no HTTP, no DB, no file I/O)

**Exclude from smoke suite**:
- ❌ Tests >500ms execution time
- ❌ Tests with database dependencies (even with fixtures)
- ❌ Tests with network I/O
- ❌ Tests that are flaky or skip frequently
- ❌ Manual tests (prefixed with `manual_`)
- ❌ Tests in `/tests/archive/` or `/tests/manual/`

### High-Value Quick Wins

**Start with these** (likely all <500ms):

1. **Analysis tests** (`tests/unit/services/analysis/`)
   - `test_analyzer_factory.py` - 5 tests
   - `test_document_analyzer.py` - analyzer logic
   - `test_token_counter.py` - simple math

2. **UI Messages tests** (`tests/unit/services/ui_messages/`)
   - `test_template_renderer.py` - rendering logic
   - `test_loading_states.py` - state validation
   - 4 files total, ~24 tests

3. **Data Model tests** (`tests/unit/services/personality/`)
   - `test_preference_detection.py` - validators
   - `test_personality_profile.py` - data validation
   - 5 files total, ~18 tests

**Total quick wins**: ~47 tests, ~30-45 minutes to mark

---

## 📊 Progress Tracking

### Checkpoint 1: Profiling Complete
- [ ] `scripts/profile_tests.py` created and runs without errors
- [ ] Execution time: <20 minutes for full 705 tests
- [ ] Output JSON created with test timings
- [ ] Candidates identified: target 100-150 tests <500ms

### Checkpoint 2: Marking Complete
- [ ] All candidates marked with `@pytest.mark.smoke`
- [ ] Smoke suite verified: `pytest -m smoke` passes
- [ ] Execution time verified: <5 seconds
- [ ] Count verified: ~100-120 marked tests

### Checkpoint 3: Documentation Complete
- [ ] Selection criteria document created
- [ ] Completion report created
- [ ] pytest.ini updated with documentation
- [ ] Ready for Phase 4 handoff

---

## 🔍 Testing & Validation

**Before considering work complete**, verify:

```bash
# 1. Can still run individual test files
pytest tests/unit/services/analysis/test_analyzer_factory.py -v

# 2. Smoke suite exists and runs
pytest -m smoke --collect-only | head -20

# 3. Smoke suite executes in target time
time pytest -m smoke -q
# Should show: completed in ~2-5 seconds

# 4. Unit test suite still works
pytest tests/unit/ --co | grep "test session"
# Should show all tests collect without errors

# 5. No tests marked as both smoke and something else unintended
grep -r "@pytest.mark.smoke" tests/ -A1 | grep "@pytest.mark" | grep -v smoke
# Should return nothing or only approved dual-markers
```

---

## 📝 Important Notes

1. **Don't over-optimize**: If a test is just slightly >500ms (e.g., 550ms), consider including it if it's critical path. Use judgment.

2. **Avoid double-marking**: Check before adding `@pytest.mark.smoke` that the test doesn't already have it elsewhere.

3. **Git workflow**: Work on `production` branch (current). Create commits after marking each section of tests.

4. **Communication**: If execution time won't fit in <5s, file a beads issue. Don't skip marking - let PM decide priority.

5. **Parallel work**: Phase 3 (phantom audit) can run in parallel. Don't wait for this phase to complete.

---

## 📚 Reference Files

**Current Smoke Tests** (examples):
- `/Users/xian/Development/piper-morgan/tests/unit/test_slack_components.py` - 13 tests, all marked

**Candidate Test Files** (by ease):
- `/tests/unit/services/analysis/test_analyzer_factory.py` - START HERE
- `/tests/unit/services/ui_messages/test_template_renderer.py`
- `/tests/unit/services/personality/test_preference_detection.py`

**Configuration**:
- `/Users/xian/Development/piper-morgan/pytest.ini` - Line 4: smoke marker definition
- `/Users/xian/Development/piper-morgan/scripts/run_smoke_tests.py` - Smoke test runner

**Documentation Reference**:
- `/Users/xian/Development/piper-morgan/dev/2025/12/09/T2-SPRINT-EXECUTION-SEQUENCE.md` - Full plan
- `/Users/xian/Development/piper-morgan/dev/2025/12/09/TRIAGE-A11-SPRINT-CLOSURE.md` - Context

---

## ✅ Completion Checklist

Before marking this phase as complete:

- [ ] Profiling script created and profiling data collected
- [ ] 100-120 tests marked with `@pytest.mark.smoke`
- [ ] Smoke suite runs in <5 seconds
- [ ] All marked tests pass
- [ ] Selection criteria documented
- [ ] Completion report created
- [ ] No other test failures introduced
- [ ] Commits created with clear messages
- [ ] Session log updated with results

---

**Status**: Ready for Code Agent execution
**Model Recommendation**: Haiku (cost-optimized for high-velocity marking work)
**Parallel Work**: Phase 3 (phantom audit) can start immediately
