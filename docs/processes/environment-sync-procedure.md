# Environment Synchronization Procedure

**Purpose**: Keep all environments in sync
**Frequency**: After every migration
**Owner**: Developer who created migration

---

## Environments

**Development** (Local):
- Database: `piper_morgan` (local Docker)
- Purpose: Active development
- Migration timing: Immediate

**Test** (CI):
- Database: Test containers
- Purpose: Automated testing
- Migration timing: On PR

**Staging** (If exists):
- Database: Staging server
- Purpose: Pre-production testing
- Migration timing: After test passes

**Production** (Live):
- Database: Production server
- Purpose: Live alpha testing
- Migration timing: After staging verification

---

## Sync Process

### Step 1: Check Current State

```bash
# For each environment:
alembic current
python main.py status

# Document:
# - Current migration hash
# - Database version
# - Application version
```

**Record in**: `docs/environments/environment-status.md`

### Step 2: Apply Migration

**Order**: Dev → Test → Staging → Production

**For each environment**:
1. Backup database
2. Apply migration
3. Verify application works
4. Run tests
5. Document completion

### Step 3: Verify Sync

```bash
# Check all environments show same migration
# Dev:
alembic current

# Test:
# (via CI logs)

# Staging:
ssh staging "cd piper-morgan && alembic current"

# Production:
ssh production "cd piper-morgan && alembic current"

# All should show: [same migration hash]
```

### Step 4: Update Status

**File**: `docs/environments/environment-status.md`

```markdown
# Environment Status

**Last Updated**: November 12, 2025

| Environment | Migration | App Version | Database Size | Status |
|-------------|-----------|-------------|---------------|--------|
| Development | abc123    | 0.8.0       | 25 MB         | ✓      |
| Test        | abc123    | 0.8.0       | 15 MB         | ✓      |
| Staging     | abc123    | 0.8.0       | 50 MB         | ✓      |
| Production  | abc123    | 0.8.0       | 100 MB        | ✓      |
```

---

## Out-of-Sync Recovery

**If environments get out of sync**:

### Identify Drift
```bash
# Compare migration history
alembic history

# Check which migration each environment is on
# Document the differences
```

### Resolve Drift
```bash
# Option 1: Bring lagging environment forward
alembic upgrade head

# Option 2: Rollback leading environment
alembic downgrade [target_hash]

# Option 3: Fresh migration
# (nuclear option - last resort)
alembic downgrade base
alembic upgrade head
```

### Prevent Future Drift
- Run sync procedure after every migration
- Check status before starting work
- Document all manual database changes
- Use migration for ALL schema changes

---

_Created: November 12, 2025_
_Issue: #289_
