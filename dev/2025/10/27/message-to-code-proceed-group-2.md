# Code: Approved to Proceed to Group 2! 🚀

**Time**: 9:57 AM
**Status**: Group 1 APPROVED, proceed to Group 2 (CORE-USER)

---

## PM's Review Complete ✅

### Issue #257: APPROVED TO CLOSE ✅
- PM confirms: Algorithm optimization TODO (line 309) is OUT OF SCOPE
- Boundary work complete (4/4 TODOs fixed)
- **Status**: Ready to close
- **Action**: PM will update issue description with your evidence

### Issue #258: APPROVED TO CLOSE ✅
- AuthContainer complete, all criteria met
- All 17 tests passing, zero regressions
- **Status**: Ready to close
- **Action**: PM will update issue description with your evidence

### Issue #262: APPROVED TO CREATE ✅
- Pre-existing bug documented
- **Action**: Please create GitHub issue for adaptive_boundaries bug
- See attached instructions: [Create Issue #262 Message]
- **Priority**: Low (can be Sprint A8 or later)

---

## Proceed to Group 2: CORE-USER

**Approved**: ✅ YES, proceed immediately

**Issues** (3 total):
- #259: CORE-USER-ALPHA-TABLE (create alpha_users table)
- #260: CORE-USER-MIGRATION (migration tool)
- #261: CORE-USER-XIAN (migrate xian superuser)

---

## REVISED PROMPT (No Time Pressure!)

**IMPORTANT**: The original prompt had time estimates that created pressure. Here's the corrected version:

### Key Changes
- ❌ Removed ALL time estimates and "deadlines"
- ✅ Effort-based language (small/medium/large)
- ✅ Discovery required for each issue
- ✅ Stop conditions explicit
- ✅ Focus on thoroughness, not speed

---

## Group 2: CORE-USER (Medium effort)

### Discovery Phase FIRST

Before implementing ANYTHING, verify:

```bash
# Check database
psql -h localhost -p 5433 -U postgres -d piper -c "\dt users"
psql -h localhost -p 5433 -U postgres -d piper -c "\d users"  # Show schema

# Check Alembic
alembic current
alembic history

# Check if alpha_users exists
psql -h localhost -p 5433 -U postgres -d piper -c "\d alpha_users"

# Check if xian user exists
psql -h localhost -p 5433 -U postgres -d piper -c "SELECT * FROM users WHERE username = 'xian';"

# Check legacy config
cat config/PIPER.user.md
```

**Report findings before proceeding!**

---

### Issue #259: CORE-USER-ALPHA-TABLE

**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/259

**Objective**: Create alpha_users table (Chief Architect: separate table for clean isolation)

**Discovery Required**:
1. Read GitHub issue - confirm schema requirements
2. Verify PostgreSQL connection working
3. Check if table already exists
4. Review Alembic migration history

**Implementation** (only after discovery):

1. Create Alembic migration:
```bash
cd /home/christian/Development/piper-morgan
alembic revision -m "create_alpha_users_table"
```

2. Implement with Chief Architect's schema:
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

-- Indexes
CREATE INDEX idx_alpha_users_migration_status ON alpha_users(migration_status);
CREATE INDEX idx_alpha_users_prod_user ON alpha_users(prod_user_id) WHERE prod_user_id IS NOT NULL;
```

3. Run migration:
```bash
alembic upgrade head
```

4. Verify:
```bash
psql -h localhost -p 5433 -U postgres -d piper -c "\d alpha_users"
```

5. Create SQLAlchemy model (if needed)

**Testing**:
```bash
# Find relevant tests
find tests/ -name "*alpha*" -o -name "*user*"

# Run what exists
pytest tests/integration/test_alpha_users*.py -v
```

**Expected Outcome**:
- Alembic migration created and applied
- alpha_users table exists with correct schema
- Indexes created
- SQLAlchemy model working (if created)
- Tests passing

**STOP CONDITIONS**:
- Database connection fails
- Migration conflicts with existing schema
- Schema doesn't match Chief's spec

---

### Issue #260: CORE-USER-MIGRATION

**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/260

**Objective**: CLI tool for alpha→production user migration

**Discovery Required**:
1. Read GitHub issue - confirm CLI requirements
2. Check if migration tool already exists
3. Check main.py CLI structure
4. Identify data relationships to migrate

**Implementation** (only after discovery):

1. Add CLI command to main.py:
```python
@app.command()
def migrate_user(
    alpha_user_id: str,
    preview: bool = typer.Option(False, "--preview"),
    dry_run: bool = typer.Option(False, "--dry-run")
):
    """Migrate alpha user to production"""
    # Implementation
```

2. Create migration service: `services/user/alpha_migration_service.py`
   - Lift and shift ALL data:
     - User record (alpha_users → users)
     - API keys (preserve OS keychain refs)
     - Conversations/messages
     - Knowledge graph (nodes + edges + embeddings)
     - Audit logs
     - Preferences (JSONB → structured)

3. Implement modes:
   - **Preview**: Show what will migrate (no changes)
   - **Dry-run**: Simulate with rollback
   - **Normal**: Execute migration

4. Track in audit logs

**Testing**:
```bash
# Test CLI exists
python main.py --help | grep migrate

# Run migration tests
pytest tests/integration/test_alpha_migration*.py -v
```

**Expected Outcome**:
- CLI command working
- Preview mode shows plan
- Dry-run works with rollback
- Migration preserves relationships
- Tests passing

**STOP CONDITIONS**:
- Data model unclear
- Existing migration code conflicts
- Rollback mechanism too complex

---

### Issue #261: CORE-USER-XIAN

**URL**: https://github.com/mediajunkie/piper-morgan-product/issues/261

**Objective**: Migrate xian superuser (Chief: keep it simple)

**Discovery Required**:
1. Read GitHub issue
2. Check if xian already exists in database
3. Check legacy config (PIPER.user.md)
4. Find hardcoded "xian" references

**Implementation** (only after discovery):

1. Create xian superuser:
```sql
INSERT INTO users (id, username, email, role, created_at)
VALUES (
  gen_random_uuid(),
  'xian',
  'xian@piper-morgan.dev',
  'superuser',
  NOW()
);
```

2. Migrate legacy data (if exists):
   - API keys: config → database
   - Orphaned knowledge: `UPDATE knowledge_nodes SET user_id = <xian_id> WHERE user_id IS NULL`
   - Orphaned conversations
   - Track in metadata

3. Fix hardcoded references:
   - Search: `grep -rn '"xian"' services/`
   - Replace with: `user_service.get_user_by_username("xian")`

4. Archive legacy config:
```bash
mkdir -p config/archive
mv config/PIPER.user.md config/archive/PIPER.user.md.legacy
echo "Migrated to database on 2025-10-23" > config/archive/README.md
```

**Testing**:
```bash
# Verify xian exists
psql -h localhost -p 5433 -U postgres -d piper -c "SELECT * FROM users WHERE username = 'xian';"

# Check hardcoded refs
grep -rn '"xian"' services/ | grep -v "get_user_by_username"

# Run tests
pytest tests/integration/test_superuser*.py -v
```

**Expected Outcome**:
- xian superuser in database
- xian has superuser role
- Legacy data migrated
- No hardcoded refs
- Config archived (not deleted)
- Tests passing

**STOP CONDITIONS**:
- Legacy data format unexpected
- Superuser role doesn't exist
- Migration would lose data

---

## Checkpoint 2: After Group 2 Complete

**STOP and report**:

```markdown
## Group 2 Complete

### Issue #259: CORE-USER-ALPHA-TABLE
Status: [Complete / Blocked / Partial]
Evidence: [psql output showing table]
Tests: [pytest output]

### Issue #260: CORE-USER-MIGRATION
Status: [Complete / Blocked / Partial]
Evidence: [CLI help, test migration]
Tests: [pytest output]

### Issue #261: CORE-USER-XIAN
Status: [Complete / Blocked / Partial]
Evidence: [psql showing xian user]
Tests: [pytest output]

### Multi-User Isolation Tests
[Critical for Chief Architect]
Tests run: test_alpha_user_cannot_see_production_data, etc.
Results: [pass/fail counts]

### Regression Check
Command: pytest tests/ -v
Result: [total counts]
```

---

## Critical Reminders

### Chief Architect's Guidance
- **Separate alpha_users table** (NOT single table with flags)
- **Keep xian migration simple** (config → database, archive legacy)
- **JSONB for preferences** (flexibility in alpha)
- **Focus on multi-user isolation** (critical for Alpha Wave 2)

### Time Agnosticism
**DO NOT**:
- ❌ Worry about deadlines
- ❌ Rush to claim done
- ❌ Skip verification

**INSTEAD**:
- ✅ Focus on thoroughness
- ✅ Verify everything
- ✅ Document blockers
- ✅ Ask when uncertain

**Remember**: PM is a Time Lord. Effort matters, not clock time.

### Evidence Requirements
For EVERY claim:
- "Created X" → Show `ls -la` or `cat`
- "Table created" → Show `psql` output
- "Migration works" → Show actual run
- "Tests pass" → Show pytest output

---

## Before You Start

1. ✅ Read all three issue descriptions on GitHub
2. ✅ Run discovery commands
3. ✅ Report findings
4. ✅ THEN begin implementation

---

## Questions or Blockers?

**Stop and ask immediately if**:
- Database connection issues
- Schema doesn't match expectations
- Unclear what data to migrate
- Any uncertainty about scope

---

**Ready to execute!** 🚀

**Remember**:
- Discovery FIRST
- Test after EACH issue
- Evidence for ALL claims
- No time pressure
- Stop conditions matter

**Next**: After Group 2 complete, Cursor takes Groups 3-4 (CORE-UX + CORE-KEYS)
