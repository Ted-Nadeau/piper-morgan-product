# Gameplan: Issue #378 - ALPHA-DEPLOY-PROD

**Issue**: #378 (ALPHA-DEPLOY-PROD)
**Date**: November 24, 2025, 2:10 AM
**Status**: READY TO EXECUTE
**Prerequisite**: ✅ Migration fixes complete (commit b30f2373)

---

## Executive Summary

Deploy all Nov 21-23 work (Issues #376, #377, #379, #357) to production branch for Michelle Hertzfeld's alpha testing arrival on Nov 24, 2025.

**User's Critical Requirement**: "378 not optional! alpha testers work on the production branch. they need a clean build (0.8.1) on prod to onboard."

---

## Problem Statement

Michelle needs a clean, working build on the `production` branch to begin alpha testing. Current blockers resolved:
- ✅ Broken migrations fixed (commit b30f2373)
- ✅ Test database can rebuild from scratch
- ✅ All unit tests passing (9/9)
- ✅ Migration heads merged (single head: cd320b81e4c6)

Production branch status: **498 commits behind main**

---

## Deployment Strategy

**Approach**: Clean merge from main → production (fast-forward preferred)

**Why**:
- Alpha needs latest features (UI, SEC-RBAC, 14 fixes from Issue #379)
- Main branch is stable (all tests passing)
- Fresh migration state (broken migrations removed)
- Documentation updated (Issue #377 complete)

---

## Pre-Deployment Checklist

### Phase 0: Verification (5 min)

**Main Branch State**:
- [x] All tests passing
- [x] Migrations clean (single head)
- [x] Git status clean
- [x] Latest commit: b30f2373 (SEC-RBAC migration fixes)

**Production Branch State** (needs verification):
```bash
git fetch origin production
git checkout production
git log --oneline -10  # Check current state
git status  # Check for uncommitted changes
```

**Database Considerations**:
- Is there a production database?
- If yes, does it need migrations?
- If no, will be created fresh (migrations will run)

---

## Execution Plan

### Phase 1: Prepare Main Branch (2 min)

**Objective**: Ensure main branch is deployment-ready

```bash
# Verify current state
git checkout main
git status  # Should be clean
git log --oneline -5  # Verify latest commits

# Run final test suite
python -m pytest tests/unit/ -x  # Stop on first failure

# Verify migration state
python -m alembic heads  # Should show single head
```

**Success Criteria**:
- ✅ Git status clean
- ✅ All tests pass
- ✅ Single migration head
- ✅ No uncommitted changes

---

### Phase 2: Production Branch Preparation (5 min)

**Objective**: Understand production branch state and prepare for merge

```bash
# Switch to production branch
git fetch origin production
git checkout production

# Check state
git log --oneline -10
git status
git diff main --stat  # See what's different

# Check for local changes
git stash list  # Should be empty
```

**Decision Point**:
- **If production is clean and behind main**: Proceed with fast-forward merge
- **If production has unique commits**: STOP - escalate to PM for strategy
- **If production has local changes**: STOP - need to understand why

---

### Phase 3: Merge and Deploy (3 min)

**Objective**: Merge main into production cleanly

**Option A: Fast-Forward Merge** (preferred if possible)
```bash
git checkout production
git merge main --ff-only  # Fast-forward only, fails if not possible
git push origin production
```

**Option B: Regular Merge** (if fast-forward not possible)
```bash
git checkout production
git merge main -m "chore: Merge main for alpha testing (Issues #376, #377, #379, #357)"
# Resolve conflicts if any (STOP and escalate if complex)
git push origin production
```

**Success Criteria**:
- ✅ Merge successful (no conflicts)
- ✅ Push successful to origin/production
- ✅ Production branch at same commit as main (or ahead)

---

### Phase 4: Post-Deployment Verification (5 min)

**Objective**: Verify production branch is working

```bash
# Verify production branch state
git checkout production
git log --oneline -5  # Should include recent commits

# Verify migration state
python -m alembic heads  # Should match main

# Run smoke tests
python -m pytest tests/unit/services/test_file_repository_migration.py -xvs
```

**Manual Verification** (if server deployed):
```bash
# Check server status
curl http://localhost:8001/health  # Or production URL

# Check key endpoints
curl http://localhost:8001/api/v1/lists
curl http://localhost:8001/api/v1/files
```

**Success Criteria**:
- ✅ Production branch matches main
- ✅ Migrations work
- ✅ Tests pass on production branch
- ✅ Server starts successfully (if tested)

---

## Rollback Plan

**If merge fails**:
```bash
git merge --abort
# Escalate to PM with evidence
```

**If push fails**:
```bash
# Already local only, no rollback needed
# Investigate error, fix, retry
```

**If post-deploy tests fail**:
```bash
git checkout production
git reset --hard origin/production  # Reset to pre-merge state
git push origin production --force  # WARNING: Only if push succeeded earlier
# Escalate to PM
```

---

## Success Criteria (Overall)

- [ ] Main branch clean and tested
- [ ] Production branch exists and accessible
- [ ] Merge successful (fast-forward or regular)
- [ ] Push successful to origin/production
- [ ] Tests pass on production branch
- [ ] Migration heads clean
- [ ] No conflicts or errors
- [ ] Michelle can clone production branch and run successfully

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Production has unique commits | Medium | High | STOP, escalate to PM |
| Merge conflicts | Low | Medium | STOP, analyze conflicts |
| Database migration issues | Low | High | Test migrations on fresh DB first |
| Production branch doesn't exist | Low | Low | Create from main |
| Tests fail on production | Low | High | Don't deploy, fix first |

---

## Timeline

| Phase | Duration | Total |
|-------|----------|-------|
| Phase 0: Verification | 5 min | 5 min |
| Phase 1: Prepare Main | 2 min | 7 min |
| Phase 2: Prepare Production | 5 min | 12 min |
| Phase 3: Merge & Deploy | 3 min | 15 min |
| Phase 4: Post-Deploy Verify | 5 min | 20 min |

**Total Estimated Time**: 20 minutes

---

## Evidence Requirements

1. **Git log** showing successful merge
2. **Push output** showing successful push to production
3. **Test output** showing all tests pass on production
4. **Migration heads** output showing clean state
5. **Git status** showing clean working tree

---

## Next Steps After Deployment

1. **Notify Michelle**: Production branch ready for cloning
2. **Update Issue #378**: Mark as complete with evidence
3. **Create follow-up issues**:
   - KnowledgeGraph model migration (already documented)
   - Any issues discovered during deployment
4. **Session wrap**: Document completion

---

## Notes

- **Production branch purpose**: Clean, stable releases for alpha testers
- **Main branch purpose**: Active development, PM's working branch
- **Deployment frequency**: Only push clean, tested updates to production
- **Michelle's workflow**: Clone production, not main

---

**Status**: Ready to execute
**Blocked by**: None (prerequisites met)
**Estimated Duration**: 20 minutes
**Risk Level**: Low (main branch stable)

---

_Created: November 24, 2025, 2:10 AM_
_Created by: Lead Developer (Claude Code, role: lead-sonnet)_
_Prerequisites: ✅ Migration fixes (b30f2373), ✅ Tests passing, ✅ Docs updated_
