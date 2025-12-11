# T2 Sprint Execution Sequence

**Date**: December 9, 2025 - 5:03 PM
**Sprint**: T2 - Test Polish
**Status**: Ready to Execute

---

## Immediate Actions (Today - 20 minutes)

These are **infrastructure fixes** that unblock everything else:

```bash
# 1. Start PostgreSQL (enables all database tests)
docker-compose up -d

# 2. Create test database schema (unblocks #349 - 53 tests)
alembic upgrade head

# 3. Verify test collection works (confirms #384 fixed)
python -m pytest --collect-only tests/

# 4. Verify async_transaction tests pass (confirms #349 fixed)
python -m pytest tests/unit/ -k async_transaction -v
```

**Impact**:
- ✅ #384 fixed (pytest collection)
- ✅ #349 fixed (async_transaction tests now pass)
- ✅ All 53 blocked tests unblocked

---

## T2 Sprint Execution Sequence

### **Phase 1: Quick Wins (1-2 hours) - Start Tomorrow**

#### **#473: Fix pytest.ini Config Warnings** ⭐ DO FIRST
**Time**: 30 minutes | **Priority**: P1 | **Blocker**: No

**What**:
- Remove lines 30-31 from `pytest.ini` (deprecated asyncio options)
- Keep line 27 (`asyncio_mode = auto`)
- Verify no warnings on test run

**Why First**:
1. Unblocks visual feedback (no more warnings cluttering output)
2. Improves developer experience immediately
3. Takes only 30 minutes
4. Enables clean baseline for remaining work

**Files**: `pytest.ini` (2 lines to remove)

**Verification**:
```bash
python -m pytest --co tests/ 2>&1 | grep -c "PytestConfigWarning"
# Should return 0 after fix
```

---

### **Phase 2: Foundation Work (4-6 hours) - After Phase 1**

#### **#277: Smoke Test Marking & Discovery**
**Time**: 4-6 hours | **Priority**: P2 | **Blocker**: No

**Breakdown**:
1. **Audit Phase** (1-2 hours):
   - Identify fast unit tests (<0.1s each)
   - Target: ~100-120 tests to mark
   - Focus areas: `tests/unit/` (most likely candidates)
   - Look for: simple validators, helpers, data models

2. **Marking Phase** (1-2 hours):
   - Add `@pytest.mark.smoke` to identified tests
   - Ensure no duplicates (avoid double-marking)
   - Update any existing smoke tests that need moving

3. **Validation Phase** (1-2 hours):
   - Run full smoke suite: `pytest -m smoke -v`
   - Measure total time (target: <5 seconds)
   - If >5s, identify slowest tests and optimize or remove from smoke

**Commands**:
```bash
# Find candidates (unit tests, likely fast)
find tests/unit/ -name "test_*.py" -type f | wc -l

# Run smoke suite after marking
python -m pytest -m smoke -v --tb=short

# Measure time
time python -m pytest -m smoke -q
```

**Why After Phase 1**:
- Phase 1 cleanup gives clean baseline
- Can measure smoke suite properly
- Smoke marking depends on working test infrastructure

**Success Criteria**:
- ~100+ tests marked with @pytest.mark.smoke
- Smoke suite runs in <5 seconds
- All marked tests pass
- Documentation updated

---

### **Phase 3: Background Maintenance (8-12 hours) - Parallel with Phase 2**

#### **#351: Phantom Test Audit & Cleanup**
**Time**: 8-12 hours | **Priority**: P2 | **Blocker**: No

**Why Parallel**:
- Doesn't depend on other T2 work
- Can happen while smoke tests are being marked
- Slow, methodical review work (good for background effort)

**Breakdown**:
1. **Audit** (4-6 hours):
   - Review each of 44 phantom test files
   - Decide for each: Keep, Delete, or Fix
   - Reference: `dev/2025/11/20/comprehensive_test_inventory.md`

2. **Categorize** (1-2 hours):
   - Intentional (archive directory) → Leave alone
   - Dead code → Delete
   - Incomplete tests → Either fix or delete
   - Non-test files (fixtures, constants) → Rename or move

3. **Cleanup** (2-3 hours):
   - Delete identified dead code
   - Rename non-test files (remove `test_` prefix if not tests)
   - Update pytest configuration if needed
   - Update test inventory documentation

**Strategy**:
```
For each phantom test file:
1. Read the file
2. Check for @pytest.mark decorators
3. Search for "def test_" functions
4. If none found:
   - Check git history (was it intentionally removed?)
   - Check if it's in archive/ (intentional)
   - Check if it's config/fixtures (rename?)
   - Decide: keep, delete, or fix
5. Document decision
6. Execute (delete, rename, or add tests)
```

**Example Decisions**:
- `/tests/archive/test_*.py` → Keep (intentional archive)
- `/tests/intent/test_constants.py` → Rename to `constants.py` (not a test file)
- `/tests/integration/test_performance_baseline.py` → Delete (incomplete, no tests)
- `/tests/fixtures/test_configs.py` → Rename to `conftest.py` or similar

**Success Criteria**:
- All 44 phantom files reviewed
- Clear decisions documented for each
- Cleanup executed
- Test inventory updated
- No pytest collection warnings about phantom tests

---

### **Phase 4: Coordination (2-3 hours) - After Phase 2-3 Complete**

#### **#341: Epic Coordination & Summary**
**Time**: 2-3 hours | **Priority**: P2 | **Blocker**: No

**What**:
- Update #341 epic with T2 completion status
- Document what was done in Phases 1-3
- Identify any follow-up work for future sprints
- Update test infrastructure documentation

**Why Last**:
- Aggregates findings from all other phases
- Can't complete until other work is done

---

## Recommended Weekly Schedule

### **Day 1 (Today/Tomorrow AM)**
- ✅ **Phase 1: Immediate Infrastructure** (20 min)
- ✅ **Phase 2a: Audit for Smoke Tests** (1-2 hours)

### **Day 2**
- 🔄 **Phase 3a: Phantom Audit** (4 hours, background)
- 🔄 **Phase 2b: Smoke Marking** (2 hours)

### **Day 3**
- 🔄 **Phase 3b: Phantom Cleanup** (3-4 hours, continue)
- ✅ **Phase 2c: Smoke Validation** (1-2 hours)

### **Day 4**
- 🔄 **Phase 3c: Phantom Finalization** (1-2 hours)
- ✅ **Phase 1 (config warnings)** (30 min, if deferred)

### **Day 5**
- ✅ **Phase 4: Epic Coordination** (2-3 hours)

---

## Total Effort Breakdown

| Phase | Work | Hours | Critical? |
|-------|------|-------|-----------|
| **Phase 1** | Infrastructure fixes | 0.3h | 🔴 YES |
| **Phase 1** | Config cleanup (#473) | 0.5h | 🟡 High impact |
| **Phase 2** | Smoke test marking (#277) | 4-6h | 🟡 Medium |
| **Phase 3** | Phantom audit (#351) | 8-12h | 🟢 No |
| **Phase 4** | Epic coordination (#341) | 2-3h | 🟢 No |
| | | | |
| **TOTAL** | | **15-22h** | |

---

## Why This Sequence?

1. **Phase 1 First** (20 min)
   - Unblocks everything
   - Infrastructure fix (not code)
   - Enables clean baseline

2. **Phase 2a: Audit** (1-2h)
   - Quick investigation phase
   - Informs what to mark
   - Can happen immediately after Phase 1

3. **Phase 2 in Parallel with Phase 3**
   - Phase 2 is active work (marking, validating)
   - Phase 3 is background work (auditing, cleaning)
   - Both can happen simultaneously
   - Different context/focus areas

4. **Config Warnings** (#473)
   - Could be Phase 1, but low friction
   - Can move to any slot
   - 30 min win whenever convenient

5. **Phase 4 Last**
   - Coordination role (summarizes other phases)
   - Requires completion of other work
   - Creates final documentation

---

## Decision Points Along the Way

**After Phase 1** (Infrastructure):
- ✅ Proceed if tests collect successfully and async_transaction tests pass
- 🔴 Stop if database issues remain

**After Phase 2a** (Smoke Audit):
- ✅ Proceed with marking if >50 fast tests identified
- 🟡 Adjust target if <50 tests found

**After Phase 2 Complete** (Smoke Suite):
- ✅ Proceed if suite runs in <5 seconds
- 🟡 If >5s, identify which tests to remove/optimize

**After Phase 3 Complete** (Phantom Cleanup):
- ✅ Verify pytest collection shows no phantom warnings
- ✅ Update documentation with decisions

---

## Key Success Metrics

| Goal | Target | How to Verify |
|------|--------|---------------|
| Infrastructure works | All tests collect | `pytest --co tests/` returns 0 errors |
| Smoke suite fast | <5 seconds | `time pytest -m smoke -q` |
| Smoke coverage | 100+ tests marked | `pytest -m smoke --co` shows count |
| Phantom cleanup | 44 files resolved | All decisions documented |
| Config clean | 0 warnings | `pytest --co 2>&1 \| grep ConfigWarning \| wc -l` = 0 |

---

## Next Steps

1. ✅ Run Phase 1 immediately (20 min)
   - PostgreSQL start + migrations
   - Verify tests collect

2. 📋 Tomorrow morning:
   - Fix pytest.ini warnings (#473) - 30 min
   - Start smoke test audit (#277a) - 1-2 hours
   - Begin phantom audit in background (#351) - 4 hours

3. 🔄 Iterative:
   - Smoke marking + validation (#277bc) - 3-4 hours
   - Phantom cleanup (#351b) - 3-4 hours
   - Epic coordination (#341) - 2-3 hours

---

**Status**: Ready to execute. Recommend starting with Phase 1 infrastructure fixes today.
