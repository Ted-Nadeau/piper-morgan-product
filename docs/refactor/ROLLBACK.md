# Rollback Procedures

**Created**: 2025-11-03 16:28 PM PT
**Purpose**: Safety procedures for domain model refactoring

---

## Quick Rollback (Abort Entire Refactoring)

**If something goes wrong and you need to start over**:

```bash
# Return to main branch
git checkout main

# Delete feature branch
git branch -D foundation/item-list-primitives

# Verify you're back to baseline
git log --oneline -1
# Should show commit: 47596b71e2c1e94a872e5cad7c9a41918f4a2821
```

**Result**: All refactoring work discarded, back to known-good state

---

## Per-Phase Rollback

**If a specific phase needs to be reverted**:

### Phase 1 Rollback (Primitives Creation)
```bash
# If primitives creation has issues
git log --oneline  # Find commit before Phase 1 changes
git reset --hard <commit-hash>

# Or revert specific commits
git revert <phase-1-commit-hash>
```

**What gets rolled back**:
- services/domain/primitives.py (deleted)
- services/database/models/primitives.py (deleted)
- Migration for items table (reverted)
- Tests for primitives (deleted)

### Phase 2 Rollback (Todo Refactoring)
```bash
# Revert Todo extending Item
git revert <phase-2-commit-hash>
```

**What gets rolled back**:
- Todo class changes (back to standalone)
- TodoDB changes (back to single table)
- .title references (back from .text)
- Repository changes

### Phase 3 Rollback (Service Layer)
```bash
git revert <phase-3-commit-hash>
```

**What gets rolled back**:
- ItemService creation
- TodoService changes
- Service layer refactoring

### Phase 4 Rollback (Integration)
```bash
git revert <phase-4-commit-hash>
```

**What gets rolled back**:
- API updates
- Handler updates
- Integration changes

---

## Database Rollback

**If database migration causes issues**:

### Downgrade Last Migration
```bash
# Check current migration
alembic current

# Downgrade one step
alembic downgrade -1

# Verify
alembic current
```

### Full Database Reset (Nuclear Option)
```bash
# WARNING: Loses all data!

# Drop all tables
alembic downgrade base

# Re-run all migrations up to before items table
alembic upgrade <migration-before-items>
```

---

## Recovery Plan

### Scenario 1: Tests Broken After Phase
**Symptoms**: Tests that passed before now fail

**Recovery**:
1. Run git diff to see what changed
2. Identify breaking change
3. Either fix forward or revert phase
4. Re-run tests to verify

### Scenario 2: Migration Failed
**Symptoms**: Database migration errors

**Recovery**:
1. Check alembic current (what migration is active)
2. alembic downgrade -1 (undo last migration)
3. Fix migration script
4. alembic upgrade head (try again)

### Scenario 3: API Broken
**Symptoms**: API endpoints return errors

**Recovery**:
1. Check API compatibility layer
2. Verify title→text mapping working
3. Roll back Phase 4 if needed
4. Fix compatibility, try again

### Scenario 4: Complete Disaster
**Symptoms**: Everything broken, can't fix forward

**Recovery**:
```bash
# Nuclear option: start over
git checkout main
git branch -D foundation/item-list-primitives

# Database: reset to known state
alembic downgrade base
alembic upgrade head

# Verify system works
pytest tests/ --ignore=tests/integration/test_api_degradation_integration.py
```

---

## Commit Strategy for Safe Rollback

**Each phase should have atomic commits**:

```bash
# Phase 1 example
git commit -m "feat(domain): Add Item primitive class"
git commit -m "feat(database): Add ItemDB model"
git commit -m "feat(migration): Create items table"
git commit -m "test(domain): Add Item primitive tests"

# This allows reverting individual pieces
```

**Never combine multiple phases in one commit!**

---

## Backup Locations

**Pre-refactoring state**:
- Branch: main
- Commit: 47596b71e2c1e94a872e5cad7c9a41918f4a2821
- Date: 2025-11-03 16:28 PM PT

**Baseline Artifacts**:
- Test output: docs/refactor/baseline-test-*.txt
- Current state: docs/refactor/CURRENT-STATE-SUMMARY.md
- Code snapshots: docs/refactor/current-*.txt

**To restore exact baseline**:
```bash
git checkout 47596b71e2c1e94a872e5cad7c9a41918f4a2821
# You're now in "detached HEAD" state at exact baseline

# To make this permanent:
git checkout -b recovery-baseline
```

---

## Communication During Rollback

**If rolling back**:
1. Document WHY in session log
2. Note what went wrong
3. What evidence led to decision
4. Plan for retry (if applicable)

**Template**:
```markdown
## Rollback Event - Phase X

**Time**: [timestamp]
**Phase Rolled Back**: [phase number and name]
**Reason**: [specific issue encountered]
**Evidence**: [error messages, test failures, etc.]

**Recovery Action Taken**:
- [commands run]
- [result]

**Next Steps**:
- [plan to fix issue]
- [when to retry]
```

---

## Prevention > Recovery

**To minimize need for rollbacks**:
1. ✅ Test each phase thoroughly before proceeding
2. ✅ Commit frequently with clear messages
3. ✅ Run tests after each commit
4. ✅ Document changes as you go
5. ✅ Follow gameplan phases strictly (no shortcuts)

**Red Flags to Stop and Consider Rollback**:
- 🚨 More than 3 test failures after a change
- 🚨 Can't figure out why something broke
- 🚨 Database migration errors
- 🚨 API returns 500 errors
- 🚨 Lost more than 30 minutes debugging

---

## Success Metric

**Best rollback is one you never need!**

Careful, methodical progress >>> fast, broken progress

---

*Rollback procedures documented. Hope we never need them!*
