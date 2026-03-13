# Code Agent Prompt: PROOF-2 - GREAT-2 Test Precision

**Date**: October 14, 2025, 7:25 AM
**Phase**: PROOF-2 (GREAT-2 Test Precision)
**Duration**: 2-3 hours estimated, **30-60 min actual** (based on yesterday's efficiency)
**Priority**: MEDIUM (Stage 3: Precision track)
**Agent**: Code Agent

---

## Mission

Fix permissive test patterns in GREAT-2 (Spatial Intelligence) test suite and verify documentation accuracy. Apply proven PROOF-1/3 pattern for efficiency.

**From PROOF-0**: Slack spatial files claimed "20+ files", found 8-10 files - needs correction.

---

## Critical Reminder: Post-Compaction Protocol

**AFTER ANY COMPACTION/SUMMARY**:
1. ✅ Re-verify the actual assignment before concluding
2. ✅ If discrepancies found during verification, MUST FIX THEM
3. ✅ Don't decide corrections are "optional" or "minor"
4. ✅ Complete the assigned work fully

**Assignment**: Fix permissive test patterns AND correct documentation discrepancies

---

## Context from PROOF-0

### Current State
**From reconnaissance report**:
- **Slack Spatial Files**: Claimed "20+ files", actual 8-10 files
- **GitHub Router**: Verified 23 methods, deprecation logic present ✅
- **Service Status**: 75% complete, operational ✅
- **Impact**: Low - spatial system works, but documentation overstated

### What Needs Work
1. **Permissive Test Patterns**: Fix assertions that accept multiple outcomes
2. **File Count Correction**: Update "20+ files" to "~10 files"
3. **Test Coverage Verification**: Ensure spatial intelligence has adequate tests
4. **Documentation Accuracy**: Correct any other exaggerations

---

## Investigation Phase (20 minutes)

### Step 1: Find GREAT-2 Test Files

Using Serena and bash, locate all GREAT-2 related test files:

```bash
# Find test files related to spatial intelligence
find tests/ -name "*spatial*" -o -name "*router*" | grep -v __pycache__

# Find GREAT-2 specific tests
grep -r "GREAT-2" tests/ --include="*.py" | cut -d: -f1 | sort -u

# Check for GitHub/Slack router tests
ls tests/integrations/
ls tests/services/
```

**Expected locations**:
- tests/integrations/test_github_router.py
- tests/integrations/test_slack_spatial.py
- tests/services/test_spatial_*.py

### Step 2: Identify Permissive Patterns

Scan test files for permissive assertions:

```bash
# Find permissive status code checks
grep -r "status_code in \[" tests/ --include="*.py"
grep -r "status.*in.*\[" tests/ --include="*.py"

# Find permissive response checks
grep -r "in \[.*200.*404" tests/ --include="*.py"

# Find permissive result checks
grep -r "assert.*in \[" tests/ --include="*.py" | head -20
```

**Permissive patterns to fix**:
```python
# Bad: Accepts either success or failure
assert response.status_code in [200, 404]
assert result in ["success", "error", "pending"]

# Good: Expects specific outcome
assert response.status_code == 200, "Should succeed"
assert result == "success", "Should complete successfully"
```

### Step 3: Count Slack Spatial Files

Verify the actual count:

```bash
# Count Slack spatial files
find services/integrations/slack/ -name "spatial_*.py" | wc -l

# List them explicitly
ls -la services/integrations/slack/spatial_*.py

# Check for related files
ls services/integrations/slack/ | grep -E "(spatial|attention|workspace|navigation)"
```

**From PROOF-0**: Found 6 spatial_*.py files + attention_model.py + workspace_navigator.py = ~8-10 files

### Step 4: Locate GREAT-2 Documentation

Find files claiming "20+ files":

```bash
# Find GREAT-2 completion reports
find dev/2025/ -name "*GREAT-2*" -o -name "*great-2*"

# Search for "20+ files" claim
grep -r "20+ files\|20 files" dev/2025/ docs/ --include="*.md"

# Check GREAT-2A investigation specifically
find . -name "*GREAT-2A*" -o -name "*great-2a*"
```

**Expected to find**:
- GREAT-2A-Investigation.md (contains "20+ files" claim)
- GREAT-2 completion reports

---

## Fixing Phase (30 minutes)

### Step 1: Fix Permissive Test Patterns

**For each test file with permissive patterns**:

1. **Read the test**:
```python
# Example permissive test
def test_github_router_dispatch():
    response = router.dispatch(request)
    assert response.status_code in [200, 404]  # BAD: accepts failure
```

2. **Determine correct expectation**:
- What SHOULD the test verify?
- Success case: 200
- Failure case: 404
- If testing both, split into two tests

3. **Fix the assertion**:
```python
# Fixed: Precise expectation
def test_github_router_dispatch_success():
    response = router.dispatch(valid_request)
    assert response.status_code == 200, "Should succeed with valid request"

def test_github_router_dispatch_not_found():
    response = router.dispatch(invalid_request)
    assert response.status_code == 404, "Should return not found for invalid request"
```

**Pattern for fixes**:
```python
# Before (permissive)
assert result in [value1, value2]

# After (precise) - if testing success
assert result == value1, "Expected successful result"

# Or split into two tests if both are valid scenarios
def test_scenario_1():
    assert result == value1, "Scenario 1 outcome"

def test_scenario_2():
    assert result == value2, "Scenario 2 outcome"
```

### Step 2: Update Slack Spatial File Count

**In GREAT-2A-Investigation.md** (or wherever "20+ files" appears):

**Find and replace**:
```markdown
<!-- Before -->
- Slack has 20+ spatial intelligence files

<!-- After -->
- Slack has ~10 spatial intelligence files:
  - 6 spatial_*.py modules (core spatial logic)
  - attention_model.py (attention tracking)
  - workspace_navigator.py (navigation)
  - Plus supporting test files

(Verified October 14, 2025 via PROOF-2)
```

**Add verification note**:
```markdown
### File Count Verification (October 14, 2025)

**Slack Spatial Implementation**:
- Core spatial modules: 6 files (spatial_*.py pattern)
- Supporting modules: 2 files (attention_model.py, workspace_navigator.py)
- Total implementation: ~8-10 files
- **Previous claim**: "20+ files" - Updated based on actual count

**Note**: Original estimate may have included test files or planned features.
```

### Step 3: Verify Test Coverage

**Check if spatial intelligence has adequate test coverage**:

```python
# Use Serena or pytest to count tests
pytest --collect-only tests/integrations/ | grep -c "test_"

# Or count manually
find tests/ -name "test_*spatial*.py" -exec grep -c "def test_" {} +
```

**Assess coverage**:
- GitHub router: How many tests?
- Slack spatial: How many tests?
- Spatial attention: How many tests?
- Deprecation logic: How many tests?

**If coverage gaps found**:
- Document what's missing
- Don't create new tests (out of scope)
- Note for future work

### Step 4: Create Test Precision Report

**File**: `dev/2025/10/14/proof-2-test-precision-fixes.md`

**Track all changes**:
```markdown
# PROOF-2: Test Precision Fixes

## Tests Fixed

### [Test File 1]
- **Line X**: Changed `assert status in [200, 404]` → `assert status == 200`
- **Reason**: Test should expect success
- **Impact**: More precise failure detection

### [Test File 2]
- **Line Y**: Split permissive test into two tests
- **Before**: One test accepting multiple outcomes
- **After**: Two tests with precise expectations

## Total Changes
- X tests fixed
- Y lines changed
- Z new tests created (from splits)
```

---

## Verification Phase (15 minutes)

### Step 1: Run All Tests

```bash
# Run full test suite
pytest tests/ -v

# Focus on spatial/router tests
pytest tests/integrations/ -v -k "spatial or router"

# Check if any tests now fail
# (New failures = tests were permissive and hiding issues!)
```

**If tests fail after fixes**:
- GOOD! The permissive assertions were hiding real issues
- Document what broke
- Fix the underlying code or update test expectations
- This is cathedral building - finding edge cases

### Step 2: Verify Documentation Updates

```bash
# Confirm file count updated
grep -r "20+ files" dev/ docs/

# Should find nothing if correction was successful
# If found, update those files too
```

### Step 3: Create Evidence Package

**File**: `dev/2025/10/14/proof-2-evidence.md`

**Contents**:
- List of permissive patterns found
- List of fixes applied
- Test results before/after
- File count verification (Slack spatial: ~10 files)
- Coverage assessment

---

## Output Phase (10 minutes)

### Create PROOF-2 Completion Report

**File**: `dev/2025/10/14/proof-2-great-2-completion.md`

**Structure**:
```markdown
# PROOF-2: GREAT-2 Test Precision

**Date**: October 14, 2025, 7:25 AM
**Agent**: Code Agent
**Duration**: [Actual time]

---

## Mission Accomplished

Fixed permissive test patterns and corrected documentation accuracy for GREAT-2.

---

## Tests Fixed

### Permissive Patterns
- **Found**: [X] permissive assertions
- **Fixed**: [X] tests made precise
- **Split**: [Y] tests split for clarity

### Examples
[List key examples of before/after]

---

## Documentation Corrected

### Slack Spatial Files
- **Claimed**: "20+ files"
- **Actual**: ~10 files (6 spatial_*.py + 2 supporting)
- **Updated**: GREAT-2A-Investigation.md with verification note

---

## Test Results

### Before Fixes
- [X] tests passing (some permissive)

### After Fixes
- [Y] tests passing (all precise)
- [Z] new failures exposed (real issues found!)

---

## Coverage Assessment

**Spatial Intelligence Tests**:
- GitHub router: [X] tests
- Slack spatial: [Y] tests
- Attention model: [Z] tests
- Deprecation logic: [W] tests

**Total**: [N] tests covering spatial intelligence

**Gaps** (if any): [Document missing coverage]

---

## Files Modified

- [x] tests/integrations/[file] - Fixed permissive patterns
- [x] dev/2025/XX/GREAT-2A-Investigation.md - Corrected file count
- [x] [other files]

**Total Changes**: [X] files, [Y] tests fixed

---

## Next Steps

- [ ] Commit test precision fixes
- [ ] Ready for PROOF-4 (Multi-User validation)
- [ ] Test precision: 100% ✅

---

**Completion Time**: [timestamp]
**Status**: PROOF-2 Complete ✅
```

---

## Commit Strategy

```bash
# Stage test fixes
git add tests/

# Stage documentation corrections
git add dev/2025/
git add docs/ # if any docs updated

# Stage completion reports
git add dev/2025/10/14/proof-2-*.md

# Commit
git commit -m "test(PROOF-2): Fix permissive test patterns in GREAT-2 suite

Fixed permissive assertions that accepted multiple outcomes, making tests
more precise and revealing real issues.

Changes:
- Fixed [X] permissive test patterns in spatial intelligence tests
- Split [Y] tests for clarity (one assertion per test)
- Updated GREAT-2 documentation (Slack files: 20+ → ~10 actual)
- Verified test coverage for spatial intelligence

Test Results:
- Before: [X] passing (some permissive)
- After: [Y] passing, [Z] exposed real issues
- Coverage: [N] tests for spatial intelligence

Documentation:
- Corrected Slack spatial file count with verification
- Added evidence of actual file counts

Part of: CORE-CRAFT-PROOF epic, Stage 3 (Precision)
Method: Cathedral building - precise expectations reveal edge cases"

# Push
git push origin main
```

---

## Success Criteria

### Investigation Complete ✅
- [ ] All GREAT-2 test files located
- [ ] Permissive patterns identified
- [ ] Slack spatial files counted
- [ ] Documentation located

### Fixes Applied ✅
- [ ] All permissive patterns fixed
- [ ] Tests split where appropriate
- [ ] Documentation file count corrected
- [ ] Verification notes added

### Testing Complete ✅
- [ ] All tests run after fixes
- [ ] New failures documented (if any)
- [ ] Coverage assessed
- [ ] Results verified

### Committed ✅
- [ ] All changes staged
- [ ] Descriptive commit message
- [ ] Pushed to main
- [ ] Completion report created

---

## Time Budget

**Based on Yesterday's Efficiency**:

**Optimistic**: 30 minutes (applying PROOF-3 pattern)
- Investigation: 10 min
- Fixes: 15 min
- Verification: 5 min

**Realistic**: 45 minutes
- Investigation: 15 min
- Fixes: 20 min
- Verification: 10 min

**Pessimistic**: 60 minutes
- Investigation: 20 min
- Fixes: 30 min
- Verification: 10 min

**Target Completion**: 8:10-8:25 AM

---

## What NOT to Do

- ❌ Don't skip fixing permissive patterns found
- ❌ Don't decide file count correction is "optional"
- ❌ Don't create extensive new tests (just fix existing)
- ❌ Don't ignore test failures (they reveal real issues)

## What TO Do

- ✅ Fix EVERY permissive pattern found
- ✅ Make assertions precise and specific
- ✅ Correct documentation file counts
- ✅ Document any real issues exposed by fixes
- ✅ Run full test suite to verify
- ✅ Apply post-compaction protocol

---

## Context

**Yesterday's Success**: Stage 2 complete in 4.5 hours (vs 8-12 estimated)
**Today's Goal**: Stage 3 complete with same efficiency
**This Task**: First of 5 Stage 3 tasks

**Why PROOF-2 Matters**:
- Permissive tests hide real issues
- Cathedral building reveals edge cases
- Precise tests = better quality
- Documentation accuracy maintained

**What Comes After**:
- PROOF-4: Multi-User validation
- PROOF-5: Performance benchmarking
- PROOF-6: Spatial Intelligence verification
- PROOF-7: Documentation links

---

**PROOF-2 Start Time**: 7:25 AM
**Expected Completion**: 8:10-8:25 AM (30-60 minutes)
**Status**: Ready for Code Agent execution

**LET'S MAKE TESTS PRECISE! 🎯✅**

---

*"Permissive tests are bugs waiting to be found."*
*- PROOF-2 Philosophy*
