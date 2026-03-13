# Code Agent Prompt: Sprint A7 Groups 1-2 (Critical Fixes + CORE-USER)

**Agent**: Code (Lead Developer)
**Date**: Thursday, October 23, 2025
**Time**: 8:00 AM - 11:30 AM (~1h 45min actual)
**Issues**: #257, #258, #259, #260, #261 (5 issues)
**Gameplan**: `/mnt/user-data/uploads/sprint-a7-gameplan-polish-buffer-v2.md`

---

## Mission

Execute Groups 1-2 of Sprint A7 following Chief Architect's execution order:

1. **Group 1: Critical Fixes** (2 issues, ~45 min) → **EXECUTE FIRST**
   - Unblock everything else
   - Fix security TODOs

2. **Group 2: CORE-USER** (3 issues, ~1 hour) → **EXECUTE SECOND**
   - Foundation for multi-user testing
   - Alpha users table + migration

**Why This Order**: Chief Architect determined Critical Fixes unblock dependencies and CORE-USER provides foundation for all remaining work.

---

## Group 1: Critical Fixes (~45 min actual) ⭐ **START HERE**

### Issue #257: CORE-KNOW-BOUNDARY-COMPLETE
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/257

**Objective**: Complete BoundaryEnforcer integration

**Tasks**:
1. Find 5 TODOs in `services/knowledge/knowledge_graph_service.py`
2. Wire boundary checks into all knowledge graph queries
3. Ensure boundary enforcement works for:
   - Regular users (boundaries enforced)
   - Superusers (can bypass boundaries)
   - Admins (boundaries still enforced)

**Testing** (Run after implementation):
```bash
# Boundary enforcement tests
pytest tests/integration/test_knowledge_boundaries.py -v
pytest tests/integration/test_boundary_enforcement.py -v
```

**Expected Outcome**:
- All 5 TODOs resolved
- Boundary checks wired into queries
- Tests passing (boundary enforcement working)

**Estimated**: 2-3h → **Likely**: 30 min

---

### Issue #258: CORE-AUTH-CONTAINER
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/258

**Objective**: Fix JWT dependency injection

**Tasks**:
1. Find 3 TODOs in auth services
2. Create `AuthContainer` for proper dependency injection
3. Fix circular dependencies if any
4. Wire JWT service through container

**Testing** (Run after implementation):
```bash
# JWT DI tests
pytest tests/integration/test_auth_container.py -v
pytest tests/integration/test_jwt_dependency_injection.py -v
```

**Expected Outcome**:
- All 3 TODOs resolved
- AuthContainer implemented
- No circular dependencies
- JWT service properly injected
- Tests passing

**Estimated**: 1-2h → **Likely**: 15 min

---

## ⏸️ CHECKPOINT 1: After Group 1 Complete

**Stop and verify before proceeding to Group 2**:

1. ✅ Issue #257 complete (boundary TODOs resolved)
2. ✅ Issue #258 complete (auth container working)
3. ✅ Tests passing (boundary + JWT DI)
4. ✅ No regressions (existing tests still pass)

**Report to PM**:
- Group 1 complete
- Time taken (actual vs estimated)
- Any issues encountered
- Ready for Group 2

---

## Group 2: CORE-USER (~1 hour actual) ⭐ **EXECUTE SECOND**

### Issue #259: CORE-USER-ALPHA-TABLE
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/259

**Objective**: Create alpha_users table (Chief Architect: separate table for clean isolation)

**Tasks**:
1. Create Alembic migration:
```bash
cd /home/christian/Development/piper-morgan
alembic revision -m "create_alpha_users_table"
```

2. Implement migration with this schema:
```sql
CREATE TABLE alpha_users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    migration_status VARCHAR(20) DEFAULT 'active',
    migration_date TIMESTAMP NULL,
    prod_user_id UUID REFERENCES users(id) NULL,
    preferences JSONB DEFAULT '{}'::jsonb,
    CONSTRAINT valid_migration_status CHECK (migration_status IN ('active', 'migrated', 'declined'))
);

-- Indexes for common queries
CREATE INDEX idx_alpha_users_migration_status ON alpha_users(migration_status);
CREATE INDEX idx_alpha_users_prod_user ON alpha_users(prod_user_id) WHERE prod_user_id IS NOT NULL;
```

3. Run migration:
```bash
alembic upgrade head
```

4. Create SQLAlchemy model in `models/alpha_user.py`

**Testing** (Run after implementation):
```bash
# Table creation tests
pytest tests/integration/test_alpha_users_table.py -v
pytest tests/integration/test_alpha_users_model.py -v
```

**Expected Outcome**:
- Alembic migration created
- alpha_users table exists
- SQLAlchemy model working
- Tests passing

**Estimated**: 1-2h → **Likely**: 20 min

---

### Issue #260: CORE-USER-MIGRATION
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/260

**Objective**: Alpha→Production migration tool (CLI)

**Tasks**:
1. Create CLI command in `main.py`:
```python
@app.command()
def migrate_user(
    alpha_user_id: str,
    preview: bool = typer.Option(False, "--preview", help="Preview migration without changes"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simulate migration with rollback")
):
    """Migrate alpha user to production"""
    # Implementation
```

2. Implement migration service in `services/user/alpha_migration_service.py`:
   - Lift and shift all user data:
     - User record (alpha_users → users)
     - API keys (preserve OS keychain)
     - Conversations/messages
     - Knowledge graph (nodes + edges + embeddings)
     - Audit logs
     - Preferences (JSONB → structured)
   - Preview mode (show what will migrate)
   - Dry-run mode (rollback at end)
   - Track migration in audit logs

3. Update migration_status in alpha_users table

**Testing** (Run after implementation):
```bash
# Migration tool tests
pytest tests/integration/test_alpha_migration.py -v
pytest tests/integration/test_migration_preview.py -v
pytest tests/integration/test_migration_rollback.py -v
```

**Expected Outcome**:
- CLI command working: `python main.py migrate-user <id>`
- Preview mode working (no changes)
- Dry-run mode working (with rollback)
- Migration preserves all relationships
- Tests passing

**Estimated**: 2-3h → **Likely**: 20 min

---

### Issue #261: CORE-USER-XIAN
**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/261

**Objective**: Migrate xian superuser (Chief Architect: keep it simple)

**Tasks**:
1. Create xian superuser in users table:
```sql
INSERT INTO users (id, username, email, role, created_at)
VALUES (
  gen_random_uuid(),  -- or specific UUID
  'xian',
  'xian@piper-morgan.dev',
  'superuser',
  NOW()
);
```

2. Migrate legacy data:
   - Move API keys from `config/PIPER.user.md` → database (via UserAPIKeyService)
   - Associate orphaned knowledge nodes: `UPDATE knowledge_nodes SET user_id = <xian_id> WHERE user_id IS NULL`
   - Associate orphaned conversations
   - Track migration in metadata

3. Update hardcoded references:
   - Search codebase for hardcoded "xian"
   - Replace with user lookup: `user_service.get_user_by_username("xian")`

4. Archive legacy config:
```bash
mkdir -p config/archive
mv config/PIPER.user.md config/archive/PIPER.user.md.legacy
echo "This config was migrated to database on 2025-10-23" > config/archive/README.md
```

**Testing** (Run after implementation):
```bash
# xian superuser tests
pytest tests/integration/test_xian_superuser.py -v
pytest tests/integration/test_superuser_powers.py -v
pytest tests/integration/test_legacy_data_migration.py -v
```

**Expected Outcome**:
- xian superuser exists in database
- xian has superuser role (can bypass boundaries)
- Legacy data accessible via xian account
- No hardcoded references remain
- Legacy config archived (not deleted)
- Tests passing

**Estimated**: 1-2h → **Likely**: 20 min

---

## ⏸️ CHECKPOINT 2: After Group 2 Complete

**Stop and verify before handing off to Cursor**:

1. ✅ Issue #259 complete (alpha_users table created)
2. ✅ Issue #260 complete (migration tool working)
3. ✅ Issue #261 complete (xian superuser migrated)
4. ✅ Tests passing (multi-user isolation working)
5. ✅ No regressions (all existing tests pass)

**Critical Testing** (Chief Architect priorities):
```bash
# Multi-user isolation tests
pytest tests/integration/test_multi_user_isolation.py -v

# Specific tests:
# - test_alpha_user_cannot_see_production_data()
# - test_production_user_cannot_see_alpha_data()
# - test_user_migrations_preserve_isolation()
```

**Report to PM**:
- Groups 1-2 complete (5 issues done)
- Time taken (actual vs estimated)
- Test results (multi-user isolation verified)
- Ready to hand off to Cursor for Groups 3-4

---

## Success Criteria

**Groups 1-2 Complete When**:
- ✅ All 5 issues closed
- ✅ All TODOs resolved (8 total: 5 boundary + 3 auth)
- ✅ Critical tests passing:
  - Boundary enforcement
  - JWT dependency injection
  - Multi-user isolation
  - Alpha users table
  - Migration tool
  - xian superuser
- ✅ Zero regressions (existing tests pass)
- ✅ Foundation ready for Groups 3-4

---

## Important Notes

### Chief Architect's Guidance

**User Architecture**: Separate `alpha_users` table (NOT single table with flags)
- Rationale: Clean isolation, prevents test data contamination, user control

**xian Migration**: Keep it simple
- Config → database
- Archive legacy (don't delete)
- No over-engineering

**Database**: Lightweight Alembic
- One migration for alpha_users
- JSONB for preferences (flexibility in alpha)

**Testing**: Focus on multi-user isolation
- This is critical for Alpha Wave 2 launch
- Must verify alpha and production users are properly isolated

### Inchworm Protocol

- Complete Group 1 THEN checkpoint
- Complete Group 2 THEN checkpoint
- Test after each group (not at end)
- Verify before proceeding
- Report status to PM at each checkpoint

### Velocity Pattern

Based on Sprint A6 (88-95% faster):
- Estimated total: 3-7 hours
- Likely actual: 1h 45min (~75% faster)
- Pattern: Infrastructure leverage makes work faster

---

## Execution Checklist

**Phase 1: Critical Fixes** (45 min)
- [ ] Issue #257: CORE-KNOW-BOUNDARY-COMPLETE
- [ ] Issue #258: CORE-AUTH-CONTAINER
- [ ] Run boundary + JWT tests
- [ ] Checkpoint 1: Verify and report

**Phase 2: CORE-USER** (1 hour)
- [ ] Issue #259: CORE-USER-ALPHA-TABLE
- [ ] Issue #260: CORE-USER-MIGRATION
- [ ] Issue #261: CORE-USER-XIAN
- [ ] Run multi-user isolation tests
- [ ] Checkpoint 2: Verify and report

**Phase 3: Handoff**
- [ ] All 5 issues complete
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Ready for Cursor (Groups 3-4)

---

## GitHub Issue URLs

- #257: https://github.com/mediajunkie/piper-morgan-product/issues/257
- #258: https://github.com/mediajunkie/piper-morgan-product/issues/258
- #259: https://github.com/mediajunkie/piper-morgan-product/issues/259
- #260: https://github.com/mediajunkie/piper-morgan-product/issues/260
- #261: https://github.com/mediajunkie/piper-morgan-product/issues/261

---

## Contact Points

**Questions or Blockers**: Report to PM immediately
**Status Updates**: After each checkpoint
**Completion**: Full report with timing, test results, handoff notes

---

**Ready to execute!** 🚀

**Start Time**: 8:00 AM
**Expected Completion**: 9:45 AM
**Next Phase**: Cursor takes Groups 3-4 (CORE-UX + CORE-KEYS)
