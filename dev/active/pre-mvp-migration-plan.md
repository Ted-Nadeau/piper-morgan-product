# Pre-MVP Database Migration Plan

**For**: Chief Architect + Lead QA Engineer
**From**: Research Code (Claude Code)
**Date**: 2025-11-19 17:30 PM PT
**Purpose**: Sequence and de-risk database migrations needed for MVP

---

## Executive Summary

**7 database migrations** needed to fix technical debt before MVP launch. This plan sequences migrations to:
- Minimize risk (test each migration independently)
- Avoid dependencies (migrations don't conflict)
- Enable parallel testing (QA can test while migrations happen)
- Provide rollback safety (every migration tested for rollback)

**Critical path**: 4 migrations BLOCK MVP (RBAC tables, encryption setup, audit fields, indexes)

**Timeline estimate**: 50-70 hours development + 30-40 hours testing = **10-14 days total**

---

## Migration Sequence

| # | Migration | Issue | Priority | Effort | Risk | Dependencies |
|---|-----------|-------|----------|--------|------|--------------|
| 1 | Add performance indexes | #320 | High | 4-6h | Low | None |
| 2 | Standardize audit fields | #321 | High | 12-16h | Medium | None |
| 3 | Add soft delete columns | #336 | Medium | 4-6h | Low | Migration #2 (extends AuditedModel) |
| 4 | Add RBAC tables | #323 | **CRITICAL** | 6-8h | Medium | None |
| 5 | Add encryption key management | #324 | **CRITICAL** | 8-10h | High | None |
| 6 | Add annotation fields | #329 | High | 4-6h | Low | Migration #2 (extends audit_logs) |
| 7 | Migration rollback testing framework | #338 | High | N/A | N/A | All above (validates them) |

**Sequencing rationale**:
- **Migration #1 (Indexes)** first: Low risk, immediate performance benefit, no schema changes
- **Migration #2 (Audit fields)** second: Foundation for #3 and #6
- **Migration #3 (Soft delete)** third: Extends audit fields from #2
- **Migration #4 (RBAC)** parallel with #5: Both critical, independent
- **Migration #5 (Encryption)** parallel with #4: Both critical, independent
- **Migration #6 (Annotations)** after #2: Extends audit_logs
- **Migration #7 (Testing)** last: Validates all previous migrations

---

## Migration 1: Add Performance Indexes (Issue #320)

### Purpose
Add composite indexes for common query patterns (user_id + created_at, etc.)

### Schema Changes

**Tables affected**: `conversations`, `conversation_turns`, `uploaded_files`, `patterns`

**Indexes to add**:
```sql
CREATE INDEX ix_conversations_user_created
ON conversations(user_id, created_at);

CREATE INDEX ix_conversation_turns_conversation_turn
ON conversation_turns(conversation_id, turn_number);

CREATE INDEX ix_uploaded_files_user_date
ON uploaded_files(user_id, upload_date);

CREATE INDEX ix_patterns_user_category
ON patterns(user_id, category);
```

### Migration Script

```python
# alembic/versions/001_add_performance_indexes.py
"""add_performance_indexes

Revision ID: 001_perf_indexes
Revises: <current_head>
Create Date: 2025-11-20
"""

from alembic import op

revision = '001_perf_indexes'
down_revision = '<current_head>'


def upgrade():
    """Add performance indexes"""
    # Conversations
    op.create_index(
        'ix_conversations_user_created',
        'conversations',
        ['user_id', 'created_at'],
        unique=False
    )

    # Conversation turns
    op.create_index(
        'ix_conversation_turns_conversation_turn',
        'conversation_turns',
        ['conversation_id', 'turn_number'],
        unique=False
    )

    # Uploaded files
    op.create_index(
        'ix_uploaded_files_user_date',
        'uploaded_files',
        ['user_id', 'upload_date'],
        unique=False
    )

    # Patterns
    op.create_index(
        'ix_patterns_user_category',
        'patterns',
        ['user_id', 'category'],
        unique=False
    )


def downgrade():
    """Remove performance indexes"""
    op.drop_index('ix_patterns_user_category', 'patterns')
    op.drop_index('ix_uploaded_files_user_date', 'uploaded_files')
    op.drop_index('ix_conversation_turns_conversation_turn', 'conversation_turns')
    op.drop_index('ix_conversations_user_created', 'conversations')
```

### Pre-Migration Checklist

- [ ] Backup database
- [ ] Benchmark query performance BEFORE migration
- [ ] Verify tables exist (`conversations`, `conversation_turns`, `uploaded_files`, `patterns`)
- [ ] Check disk space (indexes ~10% of table size)

### Execution

```bash
# 1. Backup
pg_dump -h localhost -p 5433 -U piper -d piper_morgan > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Benchmark BEFORE
psql -h localhost -p 5433 -U piper -d piper_morgan -c "
EXPLAIN ANALYZE
SELECT * FROM conversations
WHERE user_id = '<test_user_id>'
ORDER BY created_at DESC
LIMIT 50;
" > benchmark_before_migration_001.txt

# 3. Run migration
alembic upgrade head

# 4. Benchmark AFTER
psql -h localhost -p 5433 -U piper -d piper_morgan -c "
EXPLAIN ANALYZE
SELECT * FROM conversations
WHERE user_id = '<test_user_id>'
ORDER BY created_at DESC
LIMIT 50;
" > benchmark_after_migration_001.txt

# 5. Compare results
diff benchmark_before_migration_001.txt benchmark_after_migration_001.txt
```

### Validation

- [ ] All 4 indexes created successfully
- [ ] EXPLAIN ANALYZE shows index usage (not sequential scan)
- [ ] Query time improved (target: 200ms → 20ms for 1K records)
- [ ] No application errors (indexes are additive, no breaking changes)

### Rollback Test

```bash
# Downgrade migration
alembic downgrade -1

# Verify indexes removed
psql -h localhost -p 5433 -U piper -d piper_morgan -c "\d conversations"
# Should NOT show ix_conversations_user_created

# Re-upgrade to test idempotency
alembic upgrade head
```

### Risk Level: **LOW**

**Why**: Indexes are additive (don't change schema), can be dropped if issues occur.

**Downtime**: None (indexes can be created concurrently in PostgreSQL with `CONCURRENTLY` keyword if needed)

---

## Migration 2: Standardize Audit Fields (Issue #321)

### Purpose
Add missing audit fields (`created_by`, `updated_by`, `deleted_at`, `deleted_by`) to all domain models.

### Schema Changes

**Tables affected**: All 26+ domain tables

**Fields to add**:
```sql
ALTER TABLE <table> ADD COLUMN created_by INTEGER REFERENCES users(id);
ALTER TABLE <table> ADD COLUMN updated_by INTEGER REFERENCES users(id);
ALTER TABLE <table> ADD COLUMN deleted_at TIMESTAMP;
ALTER TABLE <table> ADD COLUMN deleted_by INTEGER REFERENCES users(id);
```

### Migration Script (Abbreviated)

```python
# alembic/versions/002_standardize_audit_fields.py
"""standardize_audit_fields

Revision ID: 002_audit_fields
Revises: 001_perf_indexes
Create Date: 2025-11-20
"""

import sqlalchemy as sa
from alembic import op

revision = '002_audit_fields'
down_revision = '001_perf_indexes'


TABLES_TO_UPDATE = [
    'lists', 'list_items', 'intents', 'workflows', 'tasks',
    'features', 'products', 'stakeholders', 'work_items',
    'projects', 'project_integrations', 'learned_patterns',
    'knowledge_nodes', 'knowledge_edges', 'uploaded_files',
    'conversations', 'conversation_turns',
    # ... all domain tables
]


def upgrade():
    """Add audit fields to all tables"""
    for table in TABLES_TO_UPDATE:
        # Add created_by (nullable initially)
        op.add_column(table, sa.Column('created_by', sa.Integer(), nullable=True))
        op.create_foreign_key(
            f'{table}_created_by_fkey',
            table, 'users',
            ['created_by'], ['id']
        )

        # Add updated_by
        op.add_column(table, sa.Column('updated_by', sa.Integer(), nullable=True))
        op.create_foreign_key(
            f'{table}_updated_by_fkey',
            table, 'users',
            ['updated_by'], ['id']
        )

        # Add deleted_at
        op.add_column(table, sa.Column('deleted_at', sa.DateTime(), nullable=True))

        # Add deleted_by
        op.add_column(table, sa.Column('deleted_by', sa.Integer(), nullable=True))
        op.create_foreign_key(
            f'{table}_deleted_by_fkey',
            table, 'users',
            ['deleted_by'], ['id']
        )

        # Create index for deleted_at (for soft delete queries)
        op.create_index(
            f'ix_{table}_deleted_at',
            table,
            ['deleted_at']
        )


def downgrade():
    """Remove audit fields"""
    for table in TABLES_TO_UPDATE:
        op.drop_index(f'ix_{table}_deleted_at', table)
        op.drop_constraint(f'{table}_deleted_by_fkey', table, type_='foreignkey')
        op.drop_column(table, 'deleted_by')
        op.drop_column(table, 'deleted_at')
        op.drop_constraint(f'{table}_updated_by_fkey', table, type_='foreignkey')
        op.drop_column(table, 'updated_by')
        op.drop_constraint(f'{table}_created_by_fkey', table, type_='foreignkey')
        op.drop_column(table, 'created_by')
```

### Data Backfill

**Challenge**: Existing records have no `created_by` value.

**Solution**: Backfill with "system" user ID (create if doesn't exist).

```python
# Part of migration upgrade()
def upgrade():
    # ... add columns above ...

    # Create system user if doesn't exist
    op.execute("""
        INSERT INTO users (id, email, password_hash, created_at)
        VALUES (0, 'system@piper.internal', '<hashed>', NOW())
        ON CONFLICT (id) DO NOTHING;
    """)

    # Backfill created_by for existing records
    for table in TABLES_TO_UPDATE:
        op.execute(f"""
            UPDATE {table}
            SET created_by = 0
            WHERE created_by IS NULL;
        """)

    # Now make created_by NOT NULL
    for table in TABLES_TO_UPDATE:
        op.alter_column(table, 'created_by', nullable=False)
```

### Pre-Migration Checklist

- [ ] Backup database
- [ ] Verify all tables exist
- [ ] Check for existing audit columns (some may already have `created_at`)
- [ ] Disk space check (4 new columns × 26 tables)

### Validation

- [ ] All tables have 4 new columns
- [ ] Foreign keys created successfully
- [ ] Existing data backfilled (created_by = 0)
- [ ] Indexes created for deleted_at
- [ ] No application errors

### Rollback Test

```bash
alembic downgrade -1

# Verify columns removed
psql -h localhost -p 5433 -U piper -d piper_morgan -c "\d lists"
# Should NOT show created_by, updated_by, deleted_at, deleted_by
```

### Risk Level: **MEDIUM**

**Why**: Adds columns to ALL tables, modifies schema significantly, requires data backfill.

**Mitigation**: Extensive testing in staging, rollback tested.

**Downtime**: Potentially 5-10 minutes for large tables (lock during ALTER TABLE).

---

## Migration 3: Add Soft Delete Columns (Issue #336)

**Note**: This migration is **INCLUDED in Migration #2** above (deleted_at, deleted_by fields).

**No separate migration needed** - soft delete functionality is part of standardized audit fields.

**Code changes required** (not migrations):
- Update `BaseRepository` to filter `deleted_at IS NULL`
- Add `soft_delete()` and `restore()` methods
- Update API endpoints

---

## Migration 4: Add RBAC Tables (Issue #323) ⚠️ CRITICAL

### Purpose
Add Role, Permission, and UserRole tables for role-based access control.

### Schema Changes

**New tables**:
```sql
CREATE TABLE roles (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP
);

CREATE TABLE user_roles (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    role_id INTEGER REFERENCES roles(id) NOT NULL,
    assigned_at TIMESTAMP NOT NULL,
    assigned_by INTEGER REFERENCES users(id),
    UNIQUE(user_id, role_id)
);
```

### Migration Script

```python
# alembic/versions/004_add_rbac_tables.py
"""add_rbac_tables

Revision ID: 004_rbac_tables
Revises: 002_audit_fields
Create Date: 2025-11-21
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '004_rbac_tables'
down_revision = '002_audit_fields'


def upgrade():
    """Add RBAC tables"""
    # Roles table
    op.create_table(
        'roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(50), unique=True, nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('permissions', postgresql.JSONB(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime())
    )

    # User roles table
    op.create_table(
        'user_roles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.Column('assigned_at', sa.DateTime(), nullable=False),
        sa.Column('assigned_by', sa.Integer()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id']),
        sa.ForeignKeyConstraint(['assigned_by'], ['users.id']),
        sa.UniqueConstraint('user_id', 'role_id', name='uq_user_role')
    )

    # Indexes
    op.create_index('ix_user_roles_user_id', 'user_roles', ['user_id'])
    op.create_index('ix_user_roles_role_id', 'user_roles', ['role_id'])

    # Seed default roles
    op.execute("""
        INSERT INTO roles (id, name, description, permissions, created_at) VALUES
        (1, 'admin', 'Administrator with full access', '{"*": ["*"]}', NOW()),
        (2, 'user', 'Standard user with own-data access', '{"own_resources": ["read", "write"]}', NOW());
    """)

    # Assign all existing users to 'user' role
    op.execute("""
        INSERT INTO user_roles (user_id, role_id, assigned_at, assigned_by)
        SELECT id, 2, NOW(), 0 FROM users;
    """)


def downgrade():
    """Remove RBAC tables"""
    op.drop_index('ix_user_roles_role_id', 'user_roles')
    op.drop_index('ix_user_roles_user_id', 'user_roles')
    op.drop_table('user_roles')
    op.drop_table('roles')
```

### Pre-Migration Checklist

- [ ] Backup database
- [ ] Verify `users` table exists
- [ ] Define permission schema (JSON structure)

### Validation

- [ ] `roles` table created with 2 default roles
- [ ] `user_roles` table created
- [ ] All existing users assigned 'user' role
- [ ] Foreign keys enforced
- [ ] Unique constraint on (user_id, role_id)

### Rollback Test

```bash
alembic downgrade -1

# Verify tables removed
psql -h localhost -p 5433 -U piper -d piper_morgan -c "\dt"
# Should NOT show 'roles' or 'user_roles'
```

### Risk Level: **MEDIUM**

**Why**: New tables (not modifying existing schema), but critical for authorization.

**Downtime**: None (additive changes).

---

## Migration 5: Add Encryption Key Management (Issue #324) ⚠️ CRITICAL

### Purpose
Set up encryption infrastructure (key storage, encrypted columns).

### Schema Changes

**New table**:
```sql
CREATE TABLE encryption_keys (
    id INTEGER PRIMARY KEY,
    key_name VARCHAR(50) UNIQUE NOT NULL,
    encrypted_key BYTEA NOT NULL,  -- Encrypted with master key
    created_at TIMESTAMP NOT NULL,
    rotated_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);
```

**Modified columns** (convert to encrypted):
- `conversations.content` → Encrypted TEXT
- `uploaded_files.file_content` → Encrypted BYTEA
- `patterns.pattern_data` → Encrypted JSONB

### Migration Script (Simplified - Full version in Issue #324)

```python
# alembic/versions/005_add_encryption.py
"""add_encryption

Revision ID: 005_encryption
Revises: 004_rbac_tables  # Can run parallel to #004
Create Date: 2025-11-21
"""

from alembic import op
import sqlalchemy as sa

revision = '005_encryption'
down_revision = '002_audit_fields'  # Independent of RBAC


def upgrade():
    """Add encryption infrastructure"""
    # Create encryption_keys table
    op.create_table(
        'encryption_keys',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('key_name', sa.String(50), unique=True, nullable=False),
        sa.Column('encrypted_key', sa.LargeBinary(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('rotated_at', sa.DateTime()),
        sa.Column('is_active', sa.Boolean(), default=True)
    )

    # Generate and store initial encryption key
    # NOTE: This should use environment variable for master key
    op.execute("""
        INSERT INTO encryption_keys (id, key_name, encrypted_key, created_at, is_active)
        VALUES (1, 'data_encryption_key_v1', '<generated_key>', NOW(), TRUE);
    """)

    # Add encrypted columns (rename existing, add encrypted versions)
    # conversations.content
    op.alter_column('conversations', 'content', new_column_name='content_plaintext')
    op.add_column('conversations', sa.Column('content', sa.Text()))  # Will be encrypted

    # Encrypt existing data (migration task, not in schema change)
    # This would be done via Python script, not SQL


def downgrade():
    """Remove encryption infrastructure"""
    # Revert conversations
    op.drop_column('conversations', 'content')
    op.alter_column('conversations', 'content_plaintext', new_column_name='content')

    # Drop encryption_keys table
    op.drop_table('encryption_keys')
```

### Data Encryption Task

**Separate script** (not migration):
```python
# scripts/encrypt_existing_data.py
async def encrypt_existing_conversations():
    """Encrypt all existing conversation content"""
    encryption_service = FieldEncryption(key=os.getenv('MASTER_KEY'))

    async for conversation in get_all_conversations():
        if conversation.content_plaintext:
            encrypted = encryption_service.encrypt(conversation.content_plaintext)
            await update_conversation(conversation.id, content=encrypted)
            conversation.content_plaintext = None  # Clear plaintext
```

### Pre-Migration Checklist

- [ ] Backup database (CRITICAL - contains plaintext before encryption)
- [ ] Generate master key (store in environment variable)
- [ ] Test encryption/decryption with sample data
- [ ] Estimate encryption time (1000 records/sec?)

### Validation

- [ ] `encryption_keys` table created
- [ ] Initial key generated and stored
- [ ] Encrypted columns added
- [ ] Existing data encrypted successfully
- [ ] Decryption works (application can read encrypted data)

### Rollback Test

**WARNING**: Rollback will DECRYPT data (lose encryption).

```bash
# Downgrade migration
alembic downgrade -1

# Verify plaintext restored
# THIS IS RISKY - ensure backed up!
```

### Risk Level: **HIGH**

**Why**: Modifies existing data, requires encryption key management, can't easily rollback (lose encrypted data).

**Mitigation**:
- Extensive testing in staging
- Multiple backups before production migration
- Gradual rollout (encrypt new data first, then existing)

**Downtime**: Potentially 30+ minutes for large datasets (encrypting existing records).

---

## Migration 6: Add Annotation Fields (Issue #329)

### Purpose
Extend `audit_logs` table with annotation fields (annotation, annotation_type, expected_outcome, actual_outcome).

### Schema Changes

**Table affected**: `audit_logs`

**Fields to add**:
```sql
ALTER TABLE audit_logs ADD COLUMN annotation TEXT;
ALTER TABLE audit_logs ADD COLUMN annotation_type VARCHAR(50);
ALTER TABLE audit_logs ADD COLUMN expected_outcome TEXT;
ALTER TABLE audit_logs ADD COLUMN actual_outcome TEXT;
ALTER TABLE audit_logs ADD COLUMN related_metrics JSONB;
```

### Migration Script

```python
# alembic/versions/006_add_annotation_fields.py
"""add_annotation_fields

Revision ID: 006_annotation_fields
Revises: 002_audit_fields
Create Date: 2025-11-22
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '006_annotation_fields'
down_revision = '002_audit_fields'


def upgrade():
    """Add annotation fields to audit_logs"""
    op.add_column('audit_logs', sa.Column('annotation', sa.Text()))
    op.add_column('audit_logs', sa.Column('annotation_type', sa.String(50)))
    op.add_column('audit_logs', sa.Column('expected_outcome', sa.Text()))
    op.add_column('audit_logs', sa.Column('actual_outcome', sa.Text()))
    op.add_column('audit_logs', sa.Column('related_metrics', postgresql.JSONB()))

    # Index for querying annotations
    op.create_index('ix_audit_logs_annotation_type', 'audit_logs', ['annotation_type'])


def downgrade():
    """Remove annotation fields"""
    op.drop_index('ix_audit_logs_annotation_type', 'audit_logs')
    op.drop_column('audit_logs', 'related_metrics')
    op.drop_column('audit_logs', 'actual_outcome')
    op.drop_column('audit_logs', 'expected_outcome')
    op.drop_column('audit_logs', 'annotation_type')
    op.drop_column('audit_logs', 'annotation')
```

### Pre-Migration Checklist

- [ ] Backup database
- [ ] Verify `audit_logs` table exists (should exist from earlier work)
- [ ] Define annotation_type enum values

### Validation

- [ ] 5 new columns added to audit_logs
- [ ] Index created for annotation_type
- [ ] Existing audit_logs records unchanged (new columns NULL)

### Rollback Test

```bash
alembic downgrade -1
# Verify columns removed
psql -h localhost -p 5433 -U piper -d piper_morgan -c "\d audit_logs"
```

### Risk Level: **LOW**

**Why**: Additive changes to single table, no data modification.

**Downtime**: None.

---

## Migration 7: Migration Rollback Testing Framework (Issue #338)

**Not a data migration** - Infrastructure for testing migrations #1-#6.

See Issue #338 for full testing framework. This validates all above migrations.

---

## Execution Timeline

### Week 1: Low-Risk Migrations

**Day 1-2**: Migration #1 (Indexes)
- Develop: 4 hours
- Test in staging: 2 hours
- Deploy to production: 1 hour
- **Total**: 7 hours

**Day 3-5**: Migration #2 (Audit Fields)
- Develop: 12 hours
- Test in staging: 4 hours
- Deploy to production: 2 hours
- **Total**: 18 hours

### Week 2: Critical Migrations (Parallel)

**Day 1-3**: Migration #4 (RBAC) - Engineer A
- Develop: 6 hours
- Test in staging: 2 hours
- **Total**: 8 hours

**Day 1-3**: Migration #5 (Encryption) - Engineer B
- Develop: 8 hours
- Test in staging: 2 hours
- **Total**: 10 hours

**Day 4**: Migration #6 (Annotations)
- Develop: 4 hours
- Test in staging: 2 hours
- **Total**: 6 hours

**Day 5**: Deploy #4, #5, #6 to production (sequentially for safety)
- RBAC deployment: 1 hour
- Encryption deployment: 2 hours (longer due to data encryption)
- Annotations deployment: 1 hour
- **Total**: 4 hours

### Week 3: Validation & Rollback Testing

**Day 1-3**: Migration #7 (Rollback Testing Framework)
- Develop framework: 20 hours
- Test all migrations: 10 hours
- **Total**: 30 hours

**Day 4-5**: Full regression testing with all migrations applied
- QA E2E testing: 16 hours

---

## Rollback Strategy

### General Rollback Procedure

```bash
# 1. Identify current revision
alembic current

# 2. Downgrade to specific revision
alembic downgrade <revision_id>

# 3. Validate rollback
pytest tests/migrations/test_rollback_validation.py

# 4. If rollback fails, restore from backup
psql -h localhost -p 5433 -U piper -d piper_morgan < backup_YYYYMMDD_HHMMSS.sql
```

### Per-Migration Rollback Complexity

| Migration | Rollback Complexity | Data Loss Risk |
|-----------|---------------------|----------------|
| #1 (Indexes) | **LOW** - Just drop indexes | None |
| #2 (Audit fields) | **MEDIUM** - Drop columns | Lose audit data (created_by, etc.) |
| #4 (RBAC) | **LOW** - Drop tables | Lose role assignments |
| #5 (Encryption) | **HIGH** - Decrypt data | Must decrypt before rollback |
| #6 (Annotations) | **LOW** - Drop columns | Lose annotations |

**Most critical**: Migration #5 (Encryption) - Must decrypt data BEFORE rollback or lose encrypted content.

---

## Monitoring & Validation

### During Migration

Monitor:
- Database CPU/Memory (ALTER TABLE can spike)
- Lock duration (long locks block queries)
- Application error rate (should be 0 during additive migrations)
- Query performance (before/after benchmarks)

### Post-Migration

Validate:
- Schema matches expected state (`\d <table>`)
- Data integrity checks (row counts, FK constraints)
- Application health checks (all endpoints return 200)
- Performance benchmarks met

---

## Contingency Plans

### If Migration Fails Midway

1. **DO NOT PANIC** - Database is in transaction (all-or-nothing)
2. Check error message (often permission or constraint issue)
3. Fix issue, retry migration
4. If can't fix, rollback to previous revision
5. If rollback fails, restore from backup

### If Production Issues After Migration

1. Identify if migration-related (check logs, metrics)
2. If critical, rollback migration (tested in staging first)
3. If rollback not possible, apply hotfix migration
4. Schedule proper fix for next maintenance window

---

## Communication Plan

### Before Each Migration

**Email to team** (24 hours before):
- Which migration (#1, #2, etc.)
- Estimated downtime (if any)
- What's changing (indexes, schema, etc.)
- Rollback plan

### During Migration

**Slack updates**:
- "Starting Migration #1 (Indexes) at 2:00 PM"
- "Migration #1: 50% complete (2/4 indexes)"
- "Migration #1: Complete. Validating..."
- "Migration #1: ✅ Success. No downtime."

### After Migration

**Post-mortem** (if issues occurred):
- What went wrong?
- How was it fixed?
- How to prevent in future?

---

## Success Criteria

**All migrations complete** when:

1. ✅ All 6 migrations deployed to production
2. ✅ Rollback tested for each migration (in staging)
3. ✅ No data loss
4. ✅ Performance benchmarks met (Migration #1)
5. ✅ Security tests passing (Migrations #4, #5)
6. ✅ Compliance tests passing (Migrations #2, #6)
7. ✅ Zero application errors post-migration
8. ✅ Automated migration testing framework operational (Migration #7)

---

**Prepared by**: Research Code (Claude Code)
**Date**: 2025-11-19 17:30 PM PT
**Next Review**: With Chief Architect before execution
**Estimated Total Time**: 50-70 hours development + 30-40 hours testing = **10-14 days**

**Related Documents**:
- `qa-pre-mvp-technical-debt-report.md`
- `qa-test-coverage-gaps.md`
- `mvp-acceptance-criteria.md`
- `architect-database-design-decisions.md`
