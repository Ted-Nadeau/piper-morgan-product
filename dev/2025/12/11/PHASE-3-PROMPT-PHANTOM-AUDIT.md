# Phase 3: Phantom Test Audit & Cleanup (#351)

**Status**: Ready to Execute
**Assigned to**: Code Agent (Claude Haiku - background work)
**Priority**: P2 (can run parallel with Phase 2)
**Estimated Effort**: 1-1.5 hours (lower friction than Phase 2)

---

## 🎯 Objective

Audit and make decisions on disabled/manual/skipped test files, ensuring test hygiene and clearing up any ambiguity about intentional vs accidental test state.

**Definition of Done**:
- ✅ All 3 intentionally disabled/manual test files reviewed
- ✅ Decision documented for each: re-enable, archive, or delete
- ✅ 5 skipped tests reviewed and status confirmed
- ✅ Cleanup executed (if any deletions/re-enablements needed)
- ✅ Comprehensive audit report created

---

## 📋 Files to Review

### File 1: Service Container Tests (Currently Disabled)

**Path**: `/Users/xian/Development/piper-morgan/tests/unit/services/disabled_test_service_container.py`

**Status**: Intentionally disabled (prefixed with `disabled_`)

**What to do**:
1. Read entire file content
2. Understand what it tests (service initialization, lifecycle, registry)
3. Assess quality: Is the code complete and functional?
4. Determine: Is this worth re-enabling?
5. Document decision with reasoning

**Decision Options**:
- **Option A - Re-enable**: Rename to `test_service_container.py`, add to smoke suite candidates
  - Pro: Service lifecycle is critical path
  - Con: May add testing burden if already covered elsewhere
- **Option B - Archive**: Move to `tests/archive/test_service_container.py`
  - Pro: Preserves code for reference
  - Con: Clutters archive directory
- **Option C - Delete**: Remove the file entirely
  - Pro: Clean slate
  - Con: Loss of reference code

**Expected Outcome**:
- Read file → Assess quality → Make decision → Document with evidence → Execute (if deletion/move needed)
- Time: 15-20 minutes

---

### File 2: Manual Adapter Creation Test

**Path**: `/Users/xian/Development/piper-morgan/tests/unit/adapters/manual_adapter_create.py`

**Status**: Exploratory/manual test (prefixed with `manual_`)

**What to do**:
1. Read entire file content
2. Understand what it demonstrates (adapter pattern example)
3. Assess: Is this educational reference or dead code?
4. Determine: Should this be formal test or external reference?
5. Document decision with reasoning

**Decision Options**:
- **Option A - Convert to formal test**: Rename to `test_adapter_create.py`
  - Pro: Becomes part of test suite
  - Con: Needs pytest fixtures/setup
- **Option B - Keep as manual reference**: Leave as-is in adapters/
  - Pro: Available for manual exploration
  - Con: Could confuse other developers
- **Option C - Move to docs**: Convert to documentation example
  - Pro: Clear educational purpose
  - Con: Requires refactoring as code example

**Expected Outcome**:
- Read file → Assess purpose → Make decision → Document with evidence → Execute (if conversion needed)
- Time: 15-20 minutes

---

### File 3 & Beyond: Skipped Tests

**Location**: `tests/unit/services/integrations/slack/` (5 tests with `@pytest.mark.skip`)

**Status**: Intentionally skipped (marked with decorator)

**What to do**:
1. Find all skipped tests: `grep -r "@pytest.mark.skip" tests/unit/`
2. For each, read the skip reason and surrounding code
3. Assess: Is the skip reason still valid? Has the feature been implemented?
4. Determine: Re-enable, keep skipped, or delete
5. Document each decision

**Expected Outcome**:
- Verify skip reason is documented
- Confirm external tracking (mentioned as "piper-morgan-ygy")
- No action needed if properly tracked
- Time: 15 minutes (mostly reading)

---

## 📋 Work Steps

### Step 1: Audit Phase (30-45 minutes)

**For each file/group**:

1. **Read the file**:
   - Understand what's being tested
   - Check for quality, completeness, documentation
   - Identify dependencies and assumptions

2. **Assess**:
   - Is this code complete? (Yes/No)
   - Is this code quality good? (Yes/No)
   - Is the purpose clear? (Yes/No)
   - Should this be part of the active test suite? (Yes/No)

3. **Document assessment**:
   ```markdown
   ## File: [path]
   **Current Status**: [enabled/disabled/skipped]
   **Content**: [brief description]
   **Quality**: [complete/incomplete, good/poor]
   **Recommendation**: [re-enable/archive/delete/keep-as-is]
   **Reasoning**: [why this decision]
   ```

### Step 2: Decision & Documentation (15-30 minutes)

Create comprehensive audit report: `dev/2025/12/09/PHASE-3-PHANTOM-AUDIT-REPORT.md`

**Report structure**:
```markdown
# Phantom Test Audit Report

## Summary
- Files reviewed: 3
- Skipped test groups: 5
- Decisions made: [count]
- Action items: [count]

## File-by-File Analysis

### 1. disabled_test_service_container.py
**Status**: [decision + reasoning]
**Action**: [re-enable/archive/delete]

### 2. manual_adapter_create.py
**Status**: [decision + reasoning]
**Action**: [convert/keep/move]

### 3. Skipped Tests (Slack Integration)
**Status**: [all confirmed tracked/ready to implement/abandon]
**Action**: [keep skipped/re-enable/delete]

## Patterns Identified
- [any observations about test structure/quality]

## Recommendations
- [any improvements to test hygiene]
```

### Step 3: Execution (0-30 minutes, if needed)

**If deletions/moves/renames needed**:

1. **Backup** (if deleting):
   ```bash
   # Ensure git history preserves the file
   git log --follow -- [file] > [file].git-history.txt
   ```

2. **Execute action**:
   ```bash
   # Example: Move to archive
   mv tests/unit/services/disabled_test_service_container.py tests/archive/test_service_container.py

   # Example: Delete
   rm tests/unit/adapters/manual_adapter_create.py

   # Example: Rename (re-enable)
   mv tests/unit/services/disabled_test_service_container.py tests/unit/services/test_service_container.py
   ```

3. **Verify**:
   ```bash
   # Run collection to ensure no new errors
   pytest --collect-only tests/ 2>&1 | grep ERROR
   # Should return nothing
   ```

4. **Commit**:
   ```bash
   git add -A
   ./scripts/fix-newlines.sh
   git commit -m "chore(#351): Phantom test audit and cleanup - [specific actions]"
   ```

---

## 🎯 Key Points

### What "Phantom" Means

A "phantom" test is one that:
- Has `test_` prefix but is disabled/skipped/not collected
- Exists on disk but is not part of the active test suite
- May have been intentional (archived, manual) or accidental (forgotten)

### Why This Matters

- **Test hygiene**: Prevents confusion about test status
- **Maintenance burden**: Reduces dead code
- **Documentation**: Makes intentions clear to future developers
- **CI/CD clarity**: Removes ambiguity about what tests are supposed to run

### Not Covered in This Phase

This phase does NOT review:
- ❌ Tests in `/tests/archive/` (intentional archive)
- ❌ Tests in `/tests/manual/` (intentional manual tests)
- ❌ Tests prefixed with `manual_` in other locations (intentional)
- ❌ Very large test refactoring (out of scope)

Those are intentional test states and don't require cleanup.

---

## 📊 Expected Outcomes

**Best Case** (1 hour):
- All 3 files audited
- All decisions documented
- 1-2 files re-enabled or archived
- Report written
- No breakage introduced

**Moderate Case** (1.5 hours):
- All 3 files audited thoroughly
- Decisions require discussion or investigation
- Some file refactoring needed
- Report comprehensive with recommendations

**Complex Case** (2 hours):
- Files have many dependencies requiring investigation
- Decisions deferred pending lead dev review
- Comprehensive report with options presented

---

## ✅ Completion Checklist

Before marking Phase 3 complete:

- [ ] All 3 target files read and assessed
- [ ] All 5 skipped test groups reviewed
- [ ] Decision documented for each file
- [ ] Audit report created (`PHASE-3-PHANTOM-AUDIT-REPORT.md`)
- [ ] Any cleanup actions executed (if approved by lead dev)
- [ ] No new test collection errors introduced
- [ ] Commits created (if changes made)
- [ ] Session log updated with results

---

## 🔍 Verification

**After completion, verify**:

```bash
# 1. No unintended collection errors
pytest --collect-only tests/unit/ 2>&1 | grep ERROR
# Should return: nothing (no errors)

# 2. Disabled/manual files still not collected
pytest --collect-only tests/unit/ | grep "disabled_\|manual_"
# Should return: nothing (disabled/manual not listed)

# 3. If re-enabled: verify tests pass
pytest tests/unit/services/test_service_container.py -v
# (if service container was re-enabled)

# 4. Overall test count stable or increased (not decreased unexpectedly)
pytest --collect-only tests/unit/ | grep "collected"
```

---

## 📝 Important Notes

1. **Don't force decisions**: If unsure about a file, document the ambiguity. PM can decide during Phase 4.

2. **Preserve history**: Even if deleting files, git history preserves them. Use `git log --follow` to find them later.

3. **Low-risk work**: This phase has minimal breaking potential. Feel free to make decisions confidently.

4. **Documentation is key**: A well-documented decision is more valuable than the action itself.

5. **Can run in parallel**: This phase doesn't depend on Phase 2. Start as soon as Phase 2a completes.

---

## 📚 Reference Files

**Files to audit**:
- `/Users/xian/Development/piper-morgan/tests/unit/services/disabled_test_service_container.py`
- `/Users/xian/Development/piper-morgan/tests/unit/adapters/manual_adapter_create.py`
- `/Users/xian/Development/piper-morgan/tests/unit/services/integrations/slack/` (find @pytest.mark.skip)

**Search commands**:
```bash
# Find all disabled tests
find tests/ -name "disabled_*.py" -type f

# Find all manual tests
find tests/ -name "manual_*.py" -type f

# Find all skipped tests
grep -r "@pytest.mark.skip" tests/ --include="*.py"
```

**Previous inventory** (for reference):
- `/Users/xian/Development/piper-morgan/dev/2025/11/20/comprehensive_test_inventory.md`

---

**Status**: Ready for Code Agent execution
**Model Recommendation**: Haiku (minimal code generation, mostly reading/documentation)
**Parallel Work**: Can start immediately, runs independently of Phase 2
