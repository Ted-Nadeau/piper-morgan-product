# Code Agent Prompt: Issue #262 - UUID Migration (Option 1B: Merge Tables)

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first:
- `docs/briefing/PROJECT.md` - What Piper Morgan is
- `docs/briefing/BRIEFING-CURRENT-STATE.md` - Current epic and focus
- `docs/briefing/BRIEFING-ESSENTIAL-AGENT.md` - Your role requirements
- `docs/briefing/METHODOLOGY.md` - Inchworm Protocol

---

## Task Overview

**Issue**: #262 - CORE-USER-ID-MIGRATION
**Also Resolves**: #291 - CORE-ALPHA-TOKEN-BLACKLIST-FK
**Priority**: P2 - Blocks alpha testing work
**Original Estimate**: 2-3 days
**Revised Estimate**: 10-16 hours (~1-2 days)
**Date**: November 8, 2025, 7:09 PM PT

**Critical Discovery**: The `users` table is **EMPTY** (0 records) - This simplifies the migration significantly!

**PM Decision**: **Option 1B** (merge alpha_users into users) - Cleaner architecture

**Goal**: Migrate users.id from VARCHAR to UUID, merge alpha_users table, fix token_blacklist FK constraint

---

## Gameplan to Execute

**Source**: `gameplan-262-uuid-migration-simplified.md` (680 lines)

**Phases**:
- **Phase -1**: Pre-Flight Verification (30 min) - Confirm empty table, PM decision (1B)
- **Phase 0**: Backup and Safety (30 min) - Full backup + rollback script
- **Phase 1**: Database Schema Migration (2-3 hours) - Alembic migration + merge tables
- **Phase 2**: Model Updates (2 hours) - SQLAlchemy models to UUID
- **Phase 3**: Code Updates (4-6 hours) - Type hints (152 files!)
- **Phase 4**: Test Updates (3-4 hours) - Test fixtures (104 files!)
- **Phase 5**: Integration Testing (1-2 hours) - E2E validation + #291 verification
- **Phase Z**: Completion & Handoff (30 min) - Documentation, PR, evidence

**Total Estimated**: 14 hours across Saturday + Sunday

---

## Critical Requirements

### 1. Phase -1 Verification MANDATORY

Before making ANY changes:
- Verify users table is EMPTY (0 records)
- Verify alpha_users has 1 record (xian)
- Document current database state
- Create pre-migration snapshot

**STOP if**:
- users table has records (gameplan assumptions invalid)
- alpha_users has more than 1 record (complexity increase)
- Database state differs significantly from investigation

### 2. Option 1B: Merge Tables Strategy

**PM Decision Confirmed**: Merge alpha_users into users (cleaner architecture)

**Implementation**:
1. Migrate UUID to users.id
2. Add is_alpha flag to users table
3. Copy xian record from alpha_users → users (with is_alpha=true)
4. Drop alpha_users table
5. Update all references

**Result**: Single users table with UUID id and is_alpha flag

### 3. Issue #291 Integration MANDATORY

**Token Blacklist FK constraint** must be added during this migration:

```python
# In Alembic migration (Phase 1)
op.create_foreign_key('token_blacklist_user_id_fkey',
    'token_blacklist', 'users', ['user_id'], ['id'],
    ondelete='CASCADE'
)
```

**In models (Phase 2)**:
```python
class TokenBlacklist(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="blacklisted_tokens")
```

**Test cascade behavior (Phase 5)**: Delete user → blacklist entries deleted

### 4. Automated Updates Provided

**Use the provided scripts** (in gameplan):
- `scripts/update_type_hints.py` - Updates 152 files with user_id: str → user_id: UUID
- `scripts/update_tests.py` - Updates 104 test files with UUID fixtures

**Don't update manually** - automation prevents errors!

### 5. Testing Requirements

**Incremental Testing MANDATORY**:
```bash
# After Phase 1 (database)
psql -c "\d users"  # Verify UUID type
psql -c "\d token_blacklist"  # Verify FK exists

# After Phase 2 (models)
python -c "from services.database.models import User; print(User.__table__.columns['id'].type)"

# After Phase 3 (code)
pytest tests/database/ -v  # Database tests

# After Phase 4 (tests)
pytest tests/auth/ -v      # Auth critical path
pytest tests/services/ -v  # Service layer
pytest tests/ -v           # Full suite

# After Phase 5 (integration)
# Manual auth flow test (with Cursor)
```

### 6. Evidence Required

**Must provide**:
- [ ] Database schema showing UUID type (\d users output)
- [ ] FK constraint exists (\d token_blacklist output)
- [ ] No orphaned records (SQL query results)
- [ ] All tests passing (pytest output with counts)
- [ ] Auth flow working (manual test results)
- [ ] Cascade delete working (test results)
- [ ] Performance acceptable (EXPLAIN ANALYZE results)
- [ ] Git commit with proper message

---

## Success Criteria

**Must Achieve for #262**:
- ✅ users.id is UUID type (not VARCHAR)
- ✅ users.is_alpha column added
- ✅ alpha_users table merged into users (1 record migrated)
- ✅ All FK columns updated to UUID type
- ✅ Models use UUID type
- ✅ Type hints updated (152 files)
- ✅ Tests updated and passing (104 files)
- ✅ Auth flow works with UUIDs
- ✅ Performance acceptable (no degradation)

**Must Achieve for #291** (integrated):
- ✅ token_blacklist.user_id has FK constraint
- ✅ FK references users.id (UUID)
- ✅ ON DELETE CASCADE works
- ✅ Model relationship re-enabled
- ✅ Cascade delete tested and working

**Test Requirements**:
- Database tests passing
- Auth tests passing (15/15 or better)
- Service tests passing
- Full test suite passing (all previous + new)
- Integration test for cascade delete

---

## Anti-80% Safeguards

### MANDATORY Verification Steps

**Before declaring Phase 1 complete**:
1. Run \d users and verify UUID type
2. Run \d token_blacklist and verify FK exists
3. Test migration on backup database first
4. Document any errors or issues encountered

**Before declaring Phase 2 complete**:
1. Verify all model classes updated
2. Check that UUID import added to all models
3. Confirm relationships re-enabled
4. No circular import errors

**Before declaring Phase 3 complete**:
1. Verify automation script ran successfully
2. Spot-check 10 random files for correct updates
3. Search for remaining "user_id: str" (should be 0)
4. All service methods updated

**Before declaring Phase 4 complete**:
1. Verify automation script ran successfully
2. All test files have UUID fixtures
3. No hardcoded string IDs remain
4. pytest tests/ runs without import errors

**Before declaring Phase 5 complete**:
1. Manual auth flow tested end-to-end
2. Token blacklist cascade delete tested
3. Performance checks completed
4. No regressions detected

**Before declaring complete overall**:
1. BOTH Issue #262 AND Issue #291 verified complete
2. Full test suite passing (with counts)
3. Database schema verified (screenshots)
4. Auth flow working (evidence)
5. Cascade behavior working (test results)
6. Session log comprehensive
7. Evidence package complete

---

## Methodology Reminders

### Inchworm Protocol
1. **Verify** current state (Phase -1)
2. **Backup** everything (Phase 0)
3. **Implement** database changes (Phase 1)
4. **Update** models (Phase 2)
5. **Migrate** code (Phase 3)
6. **Fix** tests (Phase 4)
7. **Validate** integration (Phase 5)
8. **Document** completion (Phase Z)

**Complete each phase 100% before proceeding** - No 75% pattern!

### Stop Conditions

Stop immediately if:
- users table has records (investigate before proceeding)
- Backup fails (cannot proceed without backup)
- Alembic migration fails (rollback and investigate)
- Tests fail after Phase 1-2 (fix before proceeding)
- Performance degrades significantly (investigate)
- Any FK constraint violations (fix before proceeding)

---

## Risk Assessment

**Risk Level**: Medium (High impact but good mitigation) ⚠️

**Risks**:
1. Data corruption (mitigated: full backup + empty table)
2. FK violations (mitigated: orphan checks + test on backup)
3. Code breaks (mitigated: incremental testing + automation)
4. Test failures (mitigated: phase-by-phase validation)
5. Performance issues (mitigated: index verification + benchmarks)

**Mitigation Strategy**:
- Full backup before starting (can restore)
- Test on backup database first
- Incremental testing at each phase
- Rollback script ready
- Can revert code changes (git)
- Cursor cross-validation

---

## Cursor Support Role

**Cursor Agent will provide parallel support**:

**During Your Work (Phases 0-3)**:
1. Evidence gathering (screenshots, metrics)
2. Cross-validation (verify your changes)
3. Documentation enhancement
4. Session notes enrichment

**After Your Phases (Phases 4-5)**:
1. Manual testing (auth flow end-to-end)
2. Validation (UUID changes work correctly)
3. Evidence package (screenshots, test results)
4. Completion report (professional summary)
5. Blog material (for "Building Piper Morgan")

**Coordination Pattern**: You implement → Cursor verifies → You proceed

**Communication**: Document your progress so Cursor can verify effectively

---

## Special Handling Required

### 1. Hardcoded "xian" ID

**File**: `services/features/issue_intelligence.py`

**Current**:
```python
user_id: str = "xian"
```

**Update to**:
```python
from uuid import UUID
user_id: UUID = UUID("3f4593ae-5bc9-468d-b08d-8c4c02a5b963")  # xian's UUID from alpha_users
```

### 2. audit_logs Table

**Has 7 records with VARCHAR user_ids** - investigate:
- Are they test data? (can delete)
- Do they reference real users? (need mapping)

**Recommended** (from gameplan): Delete if test data, then convert column

### 3. todo_items Table

**Has 19 records with owner_id** - investigate:
- Are these user references? (convert to UUID)
- Or something else? (leave as-is)

**Investigate before converting** - document findings

---

## Commit Message Template

```
feat(#262, #291): Complete UUID migration and restore token blacklist FK

BREAKING CHANGE: user_id is now UUID type instead of string

Issue #262 - UUID Migration:
- Convert users.id from VARCHAR(255) to UUID
- Add is_alpha flag for alpha user management
- Merge alpha_users table into users (cleaner architecture)
- Update all FK references to UUID type (9 tables affected)
- Update 152 files with UUID type hints
- Update 104 test files with UUID fixtures
- All tests passing (X/X)

Issue #291 - Token Blacklist FK:
- Restore token_blacklist.user_id foreign key constraint
- Add ON DELETE CASCADE behavior
- Re-enable model relationships
- Test cascade delete behavior
- FK constraint working correctly

Database Changes:
- users.id: VARCHAR(255) → UUID
- users.is_alpha: Added (boolean)
- alpha_users: Merged into users (1 record migrated)
- token_blacklist: FK constraint added
- 8 other tables: user_id columns converted to UUID

Testing:
- Database tests: passing
- Auth tests: passing
- Service tests: passing
- Integration tests: passing
- Cascade delete: verified working
- Performance: no degradation

Evidence:
- Session log: dev/2025/11/08/2025-11-08-[time]-code-issue-262-log.md
- Database schema: Verified UUID types
- FK constraints: Verified with \d commands
- Test results: X/X passing
- Manual testing: Auth flow working

Fixes #262
Fixes #291
```

---

## Session Log Requirements

Create session log: `dev/2025/11/08/2025-11-08-[time]-code-issue-262-log.md`

**Must Include**:
- Start/end timestamps for EACH phase
- Phase -1 verification results (database state)
- Phase 0 backup evidence (file sizes, locations)
- Phase 1 migration output (Alembic, SQL commands)
- Phase 2 model changes (files modified)
- Phase 3 automation results (files updated counts)
- Phase 4 test updates (files updated counts)
- Phase 5 integration results (test outputs, manual tests)
- Phase Z completion (evidence package)
- Any issues encountered and resolutions
- Decisions made during implementation
- STOP conditions checked
- Final verification checklist

**Format**: Chronological, detailed, evidence-based

---

## Deliverables Checklist

Before declaring complete:

### Database
- [ ] Phase -1 verification documented (empty users confirmed)
- [ ] Phase 0 backup created (size verified)
- [ ] Rollback script created
- [ ] Alembic migration created and tested
- [ ] Migration run successfully
- [ ] users.id is UUID type (verified)
- [ ] users.is_alpha column added (verified)
- [ ] alpha_users merged (1 record migrated)
- [ ] All FK columns UUID type (verified)
- [ ] token_blacklist FK constraint added (verified)

### Code
- [ ] Phase 2 models updated
- [ ] UUID imports added
- [ ] Model relationships re-enabled
- [ ] Phase 3 automation ran successfully
- [ ] 152 files updated with UUID type hints
- [ ] Special cases handled (hardcoded IDs)
- [ ] No remaining "user_id: str" found

### Tests
- [ ] Phase 4 automation ran successfully
- [ ] 104 test files updated
- [ ] UUID fixtures created
- [ ] Database tests passing
- [ ] Auth tests passing
- [ ] Service tests passing
- [ ] Full test suite passing (counts documented)

### Integration
- [ ] Phase 5 manual auth flow tested
- [ ] Token blacklist cascade tested
- [ ] Performance verified (no degradation)
- [ ] #291 resolution verified

### Documentation
- [ ] Session log comprehensive
- [ ] Evidence package complete
- [ ] Commit created with proper message
- [ ] Both #262 and #291 documented as resolved

---

## Communication

**When complete**, provide PM with:
1. Session log link
2. Test results summary (with counts)
3. Evidence package (database schemas, FK constraints)
4. Manual testing results (auth flow, cascade delete)
5. Git commit hash
6. Any issues encountered
7. Confirmation that BOTH #262 and #291 are complete

**If blocked**, notify immediately with:
- What you tried
- What failed (error messages)
- Current state (what phase, what's working)
- Rollback status (can we rollback safely?)
- Recommendation (investigate, rollback, proceed differently)

**Progress Updates**: Document progress at end of each phase for Cursor verification

---

## Resources

**Gameplan**: `gameplan-262-uuid-migration-simplified.md` (680 lines)
**Template**: agent-prompt-template.md v10.2
**Methodology**: Inchworm Protocol (Phase -1 through Phase Z)
**Issue Descriptions**: `CORE-USER-ID-MIGRATION.md`, `CORE-ALPHA-TOKEN-BLACKLIST-FK.md`

---

## Timeline

**Saturday Evening (Tonight)**:
- Phases -1, 0: Verification + Backup (1 hour)
- Phase 1: Database migration (2-3 hours)
- Phase 2: Model updates (2 hours)
- **Stop point**: ~5-6 hours work, natural break

**Sunday**:
- Phase 3: Code updates (4-6 hours)
- Phase 4: Test updates (3-4 hours)
- Phase 5: Integration testing (1-2 hours)
- Phase Z: Completion (30 min)
- **Total**: ~8-12 hours

**Total Across Both Days**: 14 hours (within 16-hour estimate)

---

## Critical Reminders

1. **Empty users table** = Much safer migration (verified by Chief Architect)
2. **Option 1B confirmed** = Merge tables (PM decision)
3. **Issue #291 integrated** = Fix token blacklist FK as part of this work
4. **Automation provided** = Use scripts, don't do manually (152 + 104 files!)
5. **Test incrementally** = After each phase, verify before proceeding
6. **Full backup** = Can rollback at any point
7. **Cursor verifying** = Document your work for cross-validation
8. **Both issues complete** = #262 AND #291 resolved together

---

**Ready to Execute**: Follow gameplan phases systematically, test at each step, gather comprehensive evidence, coordinate with Cursor for verification.

**Start Time**: November 8, 2025, ~7:10 PM PT
**Expected Completion**: Sunday evening, November 9, 2025

🏰 **Execute with precision and systematic verification!**
