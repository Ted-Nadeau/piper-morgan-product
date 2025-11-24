# Skip Test Audit Framework

**Date:** 2025-11-20
**Total Skipped Tests:** 197
**Context:** Post-P0 fixes, preparing for P1 work

---

## The Skip Taxonomy

### ✅ LEGITIMATE SKIPS (Keep)

**1. TDD - Test Before Implementation**
```python
@pytest.mark.skip(reason="Pre-existing TDD test suite - tracked in piper-morgan-ygy")
```
- **Why legitimate:** Test defines specification, implementation follows
- **Action required:** None (track in bead)
- **Audit check:** Verify bead exists and is active

**2. External Dependencies Not Available**
```python
@pytest.mark.skipif(not os.getenv("OPENAI_API_KEY"), reason="OPENAI_API_KEY not set")
```
- **Why legitimate:** Can't test without API key/network/hardware
- **Action required:** None
- **Audit check:** Verify tests pass when dependency available

**3. Deprecated Functionality**
```python
@pytest.mark.skip(reason="Preferences JSONB column removed in Issue #262 schema migration.")
```
- **Why legitimate:** Feature intentionally removed from product
- **Action required:** Document why feature removed
- **Audit check:** Should tests be deleted instead? (See "Zombie Tests" below)

**4. Environment-Specific**
```python
@pytest.mark.skipif(sys.platform != "linux", reason="Linux-specific test")
```
- **Why legitimate:** Platform-specific functionality
- **Action required:** None
- **Audit check:** Verify runs on target platform

---

### 🚨 PROBLEMATIC SKIPS (Fix or Remove)

**5. "Temporarily Disabled" - Red Flag!**
```python
@pytest.mark.skip(reason="Temporarily disabled - complex mocking issue with spatial adapter")
@pytest.mark.skip(reason="Temporarily disabled - duplicate event detection issue")
@pytest.mark.skip(reason="Temporarily disabled - async/await issue in spatial adapter")
```
- **Why problematic:** "Temporary" that becomes permanent
- **Actual problem:** Implementation bug or test flakiness being hidden
- **Action required:** Fix the underlying issue OR convert to tracked bug
- **Audit check:** How long has it been "temporary"? Git blame shows when added

**6. Implementation Bugs Masked as Skips**
```python
@pytest.mark.skip(reason="Pre-existing failure - tracked in piper-morgan-dw0")
```
- **Status:** This one is GOOD - it's tracked!
- **Why concerning if NOT tracked:** Hiding broken functionality
- **Action required:** Verify bead exists and is prioritized
- **Audit check:** Is bead still open? Is it being worked on?

**7. Zombie Tests - Should Be DELETED**
```python
@pytest.mark.skip(
    reason="OrchestrationEngine._analyze_file method no longer exists - implementation refactored"
)
```
- **Why problematic:** Test for deleted code clutters test suite
- **Action required:** DELETE the test, don't skip it
- **Audit check:** If implementation doesn't exist, why keep the test?

**8. Flaky Tests - Intermittent Failures**
```python
# Usually don't have explicit "flaky" in reason, but show up as sometimes passing
@pytest.mark.skip(reason="Test fails intermittently on CI")
```
- **Why problematic:** Indicates non-deterministic behavior (race condition, timing, etc.)
- **Action required:** Fix the flakiness OR use @pytest.mark.flaky(retries=3)
- **Audit check:** Does test pass locally but fail in CI? Timing issue?

---

## Audit Process

### Step 1: Categorize All Skips

```bash
# Generate skip report
grep -r "@pytest.mark.skip\|@pytest.mark.xfail" tests/ --include="*.py" -B2 -A2 > skip_analysis.txt

# Count by category
grep "Temporarily disabled" skip_analysis.txt | wc -l
grep "Pre-existing TDD" skip_analysis.txt | wc -l
grep "no longer exists" skip_analysis.txt | wc -l
grep "tracked in piper-morgan" skip_analysis.txt | wc -l
```

### Step 2: For Each Skip, Ask:

**Decision Tree:**
```
Is functionality still in product?
├─ NO → DELETE test (zombie)
└─ YES → Is implementation complete?
    ├─ NO → Keep skip, verify bead tracking (TDD)
    └─ YES → Does test pass when unskipped?
        ├─ YES → REMOVE skip, add to active suite
        └─ NO → Is failure tracked in bead?
            ├─ YES → Keep skip with bead reference
            └─ NO → RED FLAG - create bead OR fix immediately
```

### Step 3: Git Blame for "Temporary" Skips

```bash
# Find when "temporary" skips were added
git log -S "Temporarily disabled" --all -- tests/
```

**Rule:** If "temporary" > 30 days, it's permanent. Either:
1. Fix the issue
2. Convert to tracked bug with bead
3. Delete if no longer relevant

### Step 4: Verify Bead Tracking

```bash
# Extract all bead references from skip reasons
grep -r "tracked in piper-morgan-" tests/ | grep -oE "piper-morgan-[a-z0-9]+" | sort -u

# Check each bead exists
for bead in $(grep -r "tracked in piper-morgan-" tests/ | grep -oE "piper-morgan-[a-z0-9]+" | sort -u); do
    ./bd status $bead 2>/dev/null || echo "❌ MISSING: $bead"
done
```

---

## Current Codebase Analysis

### Immediate Red Flags Found

**1. "Temporarily Disabled" Tests (4+ found)**
- Location: `tests/unit/test_slack_components.py`
- Reasons: "complex mocking issue", "duplicate event detection", "async/await issue", "context storage issue"
- **Status:** 🚨 These are masking real problems
- **Action:** Create beads for each OR fix immediately

**2. Zombie Tests (6+ found)**
- Location: `tests/unit/services/orchestration/test_orchestration_engine.py`
- Reason: "method no longer exists - implementation refactored"
- **Status:** 🧟 Should be DELETED
- **Action:** Remove these tests entirely

**3. Preferences Tests (2 found)**
- Location: `tests/integration/test_alpha_onboarding_e2e.py`
- Reason: "Preferences JSONB column removed in Issue #262"
- **Status:** ✅ Correctly documented, but consider deletion
- **Action:** Delete or redesign for current PersonalityProfile system

---

## Skip Hygiene Rules

### Rule 1: Every Skip Must Have a Clear Reason
```python
# ❌ BAD
@pytest.mark.skip

# ❌ BAD
@pytest.mark.skip(reason="Broken")

# ✅ GOOD
@pytest.mark.skip(reason="Pre-existing TDD test suite - tracked in piper-morgan-ygy")

# ✅ GOOD
@pytest.mark.skip(reason="Preferences JSONB column removed in Issue #262. Needs redesign for PersonalityProfile system.")
```

### Rule 2: "Temporary" Requires Bead Tracking
```python
# ❌ BAD - No tracking
@pytest.mark.skip(reason="Temporarily disabled - complex mocking issue")

# ✅ GOOD - Tracked with deadline
@pytest.mark.skip(reason="Mock serialization issues. Tracked in piper-morgan-23y - fix by 2025-11-25")
```

### Rule 3: Zombie Tests Get Deleted, Not Skipped
```python
# ❌ BAD - Keeping dead test
@pytest.mark.skip(reason="Method no longer exists")
def test_deleted_method():
    assert old_method() == "result"

# ✅ GOOD - Just delete the test!
# (test file doesn't contain test for deleted code)
```

### Rule 4: Implementation Bugs Get Beads, Not Just Skips
```python
# ❌ BAD - Hiding broken functionality
@pytest.mark.skip(reason="Test fails sometimes")

# ✅ GOOD - Tracked and visible
@pytest.mark.skip(reason="Flaky due to race condition in spatial adapter. Bead piper-morgan-xyz")
```

---

## Audit Checklist

Run this audit quarterly or after major refactors:

- [ ] **Count total skips:** `grep -r "@pytest.mark.skip" tests/ | wc -l`
- [ ] **Find "temporarily disabled":** `grep -r "Temporarily disabled" tests/`
  - [ ] Each one has bead OR is fixed immediately
- [ ] **Find zombie tests:** `grep -r "no longer exists\|deleted\|removed" tests/`
  - [ ] Delete these tests, don't skip them
- [ ] **Verify bead tracking:** All beads referenced in skips still exist
- [ ] **Check skip age:** Git blame on "temporary" skips > 30 days old
- [ ] **Unskip and test:** Randomly sample 10 skips, try unskipping - do they pass now?

---

## Metrics to Track

**Health Indicators:**
- **Skip Ratio:** Skipped / Total Tests (target: <5%)
- **Tracked Skip Ratio:** Skips with bead / Total Skips (target: >80% for non-TDD/non-external)
- **Zombie Tests:** Tests for deleted functionality (target: 0)
- **"Temporary" Age:** Days since skip added (target: <30 days)

**Current State:**
- Total Tests: ~2300
- Skipped: 197 (8.6% - above target)
- With Bead Tracking: ~30-40 (estimated)
- Zombies Found: 6+ (need deletion)
- "Temporarily Disabled": 4+ (need conversion to beads)

---

## Recommended Actions (Priority Order)

### Immediate (This Week)
1. **Delete zombie tests** (6+ in test_orchestration_engine.py)
2. **Create beads for "temporarily disabled"** (4+ in test_slack_components.py)
3. **Verify all bead references** still exist

### Short-term (This Sprint)
4. **Audit preferences tests** - Delete or redesign for PersonalityProfile
5. **Review context_tracker skips** (piper-morgan-dw0) - Are they being worked on?
6. **Fix or document Slack spatial skips** (piper-morgan-1i5)

### Long-term (Next Quarter)
7. **Reduce skip ratio** from 8.6% to <5%
8. **Establish pre-commit hook** to enforce skip reason format
9. **Add skip age monitoring** to CI/CD metrics

---

## Conclusion

**Philosophy:** Skipped tests are **technical debt**. Every skip is:
- A feature you can't confidently deploy
- A bug you're deferring
- Code you can't refactor safely

**Golden Rules:**
1. **TDD skips are good** - They define future work
2. **External dependency skips are acceptable** - Can't control environment
3. **"Temporary" skips are red flags** - Track them or fix them
4. **Zombie skips are waste** - Delete dead code tests
5. **Every skip needs a bead or a deadline** - No hiding broken functionality

**Target State:** <5% skip ratio, 100% of non-TDD/non-external skips tracked in beads, 0 "temporary" skips older than 30 days.

---

## ACTUAL AUDIT RESULTS (2025-11-20)

### Numbers

| Category | Count | Status |
|----------|-------|--------|
| **Total Skipped Tests** | 197 | 8.6% of ~2300 tests |
| **"Temporarily Disabled"** | 5 | 🚨 RED FLAG - Need beads |
| **Zombie Tests** | 9 | 🧟 DELETE THESE |
| **Tracked in Beads** | 6 | ✅ Properly tracked |
| **External Dependencies** | 4 | ✅ Acceptable |
| **TDD Tests (Notion)** | 5+ | ⚠️ STALE - Implemented differently |

### Specific Findings

#### 🚨 RED FLAG #1: "Temporarily Disabled" (5 tests)
**Location:** `tests/unit/test_slack_components.py`

```python
@pytest.mark.skip(reason="Temporarily disabled - complex mocking issue with spatial adapter")
@pytest.mark.skip(reason="Temporarily disabled - duplicate event detection issue")
@pytest.mark.skip(reason="Temporarily disabled - async/await issue in spatial adapter")
@pytest.mark.skip(reason="Temporarily disabled - context storage issue in spatial adapter")
@pytest.mark.skip(reason="Temporarily disabled - SlackPipelineMetrics initialization issue")
```

**Problem:** These are hiding real implementation issues in Slack spatial adapter
**Action Required:** Create bead for each OR fix immediately
**Estimated Effort:** 4-8 hours to properly fix spatial adapter issues

---

#### 🧟 ZOMBIE ALERT: Tests for Deleted Code (9 tests)
**Location:** `tests/unit/services/orchestration/test_orchestration_engine.py`

```python
@pytest.mark.skip(reason="OrchestrationEngine._analyze_file method no longer exists")
@pytest.mark.skip(reason="OrchestrationEngine.task_handlers attribute no longer exists")
@pytest.mark.skip(reason="OrchestrationEngine._placeholder_handler method no longer exists")
# ... 6 more similar zombies
```

**Problem:** Tests for code that was refactored away
**Action Required:** DELETE THESE TESTS ENTIRELY
**Estimated Effort:** 10 minutes (just delete the test methods)

---

#### ⚠️ STALE TDD: Notion Config Tests (5+ tests)
**Location:** `tests/config/test_notion_user_config.py`

```python
@pytest.mark.skipif(NotionUserConfig is None, reason="NotionUserConfig not implemented yet")
```

**Problem:** Notion IS implemented, but via different approach than tests expected
**Root Cause:** Tests define `NotionUserConfig` class, but implementation uses different config pattern
**Action Required:** Either:
1. Implement NotionUserConfig as tests expect (if valuable)
2. DELETE tests and write new ones for actual implementation
3. Mark as "Abandoned feature - implemented differently"

**Investigation Needed:** Review Notion integration to determine if NotionUserConfig approach is still desired

---

#### ✅ PROPERLY TRACKED: Bead-Referenced Skips (6 tests)

**Beads Referenced:**
- `piper-morgan-dw0` - Context tracker failures (3 tests)
- `piper-morgan-ygy` - Attention scenarios TDD (2 tests)
- `piper-morgan-23y` - Slack workflow integration (1 test)
- `piper-morgan-1i5` - Slack spatial mapper (1 test)

**Status:** ✅ These are properly tracked
**Action Required:** Verify beads are active and prioritized

**Verification Script:**
```bash
for bead in dw0 ygy 23y 1i5; do
    echo "Checking piper-morgan-$bead..."
    ./scripts/bd-safe status piper-morgan-$bead 2>&1 | head -3
done
```

---

### Priority Actions (Based on Audit)

#### Immediate (Today - 30 min)
1. **DELETE zombie tests** (9 tests in test_orchestration_engine.py)
   - Just delete the test methods, no investigation needed
   - Commit: "test: Remove zombie tests for deleted OrchestrationEngine methods"

#### This Week (2-4 hours)
2. **Create beads for "temporarily disabled"** (5 Slack tests)
   - Bead for spatial adapter mocking issues
   - Bead for SlackPipelineMetrics initialization
   - Convert skips to proper bead references

3. **Investigate Notion config tests** (5+ tests)
   - Review services/integrations/notion/
   - Determine if NotionUserConfig approach is still wanted
   - Either implement OR delete tests

#### This Sprint (8-16 hours)
4. **Fix Slack spatial adapter issues** (if beads prioritized)
   - Complex mocking issue
   - Async/await issue
   - Context storage issue
   - Duplicate event detection

5. **Review and prioritize bead-tracked skips**
   - piper-morgan-dw0 (context tracker)
   - piper-morgan-1i5 (spatial mapper)
   - piper-morgan-23y (workflow integration)

---

## Skip Test Health Score

**Current:** 62/100 (Poor)

**Breakdown:**
- ❌ Skip Ratio: 8.6% (target: <5%) = -20 points
- ❌ Zombie Tests: 9 (target: 0) = -10 points
- ⚠️ Temporarily Disabled: 5 (target: 0) = -15 points
- ⚠️ Stale TDD: 5+ (should be reviewed annually) = -5 points
- ✅ Tracked Skips: 6/~20 = 30% tracked (target: 80%) = -8 points
- ✅ External Dependencies: 4 (acceptable) = +0 points
- ✅ Proper Documentation: Most have clear reasons = +20 points

**Path to 85/100 (Good):**
1. Delete 9 zombie tests (+10 points) → 72/100
2. Convert 5 "temporarily disabled" to beads (+15 points) → 87/100
3. Review Notion tests (delete or implement) (+5 points) → 92/100

**Path to 95/100 (Excellent):**
4. Reduce skip ratio to <5% (fix ~80 skips) (+20 points) → 112/100 (capped at 100)

---

## Pre-commit Hook Proposal

Create `.pre-commit-hooks/check-skip-reasons.sh`:

```bash
#!/bin/bash
# Check that new skips have proper reasons

# Find new skip marks added in this commit
new_skips=$(git diff --cached --unified=0 | grep "^+.*@pytest.mark.skip" | grep -v "reason=")

if [ -n "$new_skips" ]; then
    echo "❌ ERROR: Skip without reason detected!"
    echo ""
    echo "All @pytest.mark.skip must include reason= parameter"
    echo ""
    echo "Found:"
    echo "$new_skips"
    echo ""
    echo "Fix with: @pytest.mark.skip(reason='Clear explanation')"
    exit 1
fi

# Check for "Temporarily disabled" without bead tracking
temp_disabled=$(git diff --cached --unified=0 | grep "^+.*Temporarily disabled" | grep -v "piper-morgan-")

if [ -n "$temp_disabled" ]; then
    echo "⚠️  WARNING: 'Temporarily disabled' without bead tracking!"
    echo ""
    echo "Please create a bead and reference it:"
    echo "@pytest.mark.skip(reason='Complex mocking issue. Tracked in piper-morgan-xyz')"
    echo ""
    echo "Or remove 'Temporarily' and just fix it!"
    exit 1
fi

echo "✅ Skip reasons look good!"
```

---

## Quarterly Audit Checklist

**Run this every 3 months:**

- [ ] Count skip ratio: Currently 8.6% → Target <5%
- [ ] Find and delete zombie tests: Found 9 → Deleted ___
- [ ] Age of "temporary" skips: None > 30 days old
- [ ] Verify all bead references: dw0, ygy, 23y, 1i5 → All active
- [ ] Review TDD skips: Are they still planned features?
- [ ] Sample unskip 10 tests: Do they pass now?
- [ ] Update skip health score: From 62 → Target 85+

**Last Audit:** 2025-11-20
**Next Audit:** 2026-02-20
**Audit Owner:** QA Team / Test Lead
