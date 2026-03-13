# Gameplan: #718 BUG - lifecycle_state columns missing from database tables

**Issue**: #718
**Type**: Bug fix (database schema)
**Priority**: P2 (blocks MUX lifecycle UI testing)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Infrastructure Status**:
- [x] Database: PostgreSQL (docker, port 5433)
- [x] Migrations: Alembic
- [x] ORM: SQLAlchemy
- [x] Models: `services/domain/models.py`

**My understanding of the task**:
- Four models have `lifecycle_state: Optional[LifecycleState]` in Python
- Corresponding database tables lack the column
- Need Alembic migration to add `lifecycle_state VARCHAR(50) NULL` to 4 tables

**Affected tables** (from issue):
| Model | Line in models.py | DB Table |
|-------|-------------------|----------|
| Feature | ~204 | features |
| WorkItem | ~274 | work_items |
| Project | ~353 | projects |
| Todo | ~1352 | todo_items |

### Part A.2: Work Characteristics

**Worktree Assessment**:
- [ ] Multiple agents in parallel → No, single migration
- [ ] Duration >30 min → No, straightforward migration
- [x] Single agent, sequential work
- [x] Small fix (<15 min expected)

**Decision**: **SKIP WORKTREE** - Single Alembic migration, atomic change

### Part B: PM Verification Required

**PM, please confirm**:
1. Tables exist? `docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\dt"`
2. LifecycleState enum values? (need for column constraint if desired)
3. Any existing data in these tables that might be affected?

### Part C: Proceed/Revise

- [ ] **PROCEED** - After PM confirms tables exist
- [ ] **REVISE** - If tables don't exist or schema is different
- [ ] **CLARIFY** - If enum values needed for CHECK constraint

---

## Phase 0: Investigation

### Verify Current Schema

```bash
# Check model definitions
grep -n "lifecycle_state" services/domain/models.py

# Check existing migrations
ls -la alembic/versions/

# Verify tables exist without column
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d features"
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d work_items"
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d projects"
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d todo_items"
```

### Verify LifecycleState Enum

```bash
grep -A 20 "class LifecycleState" services/shared_types.py
```

---

## Phase 1: Create Alembic Migration

### Step 1: Generate Migration

```bash
cd /Users/xian/Development/piper-morgan
alembic revision -m "add_lifecycle_state_to_entity_tables"
```

### Step 2: Edit Migration

Migration content:
```python
"""add_lifecycle_state_to_entity_tables

Revision ID: [auto-generated]
Revises: [previous]
Create Date: 2026-01-27
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '[auto]'
down_revision = '[previous]'
branch_labels = None
depends_on = None

def upgrade():
    # Add lifecycle_state to all four entity tables
    # Using VARCHAR(50) to store enum string values
    # NULL allowed - existing rows unaffected

    op.add_column('features',
        sa.Column('lifecycle_state', sa.String(50), nullable=True))

    op.add_column('work_items',
        sa.Column('lifecycle_state', sa.String(50), nullable=True))

    op.add_column('projects',
        sa.Column('lifecycle_state', sa.String(50), nullable=True))

    op.add_column('todo_items',
        sa.Column('lifecycle_state', sa.String(50), nullable=True))

def downgrade():
    op.drop_column('features', 'lifecycle_state')
    op.drop_column('work_items', 'lifecycle_state')
    op.drop_column('projects', 'lifecycle_state')
    op.drop_column('todo_items', 'lifecycle_state')
```

---

## Phase 2: Apply and Verify Migration

### Step 1: Run Migration

```bash
alembic upgrade head
```

### Step 2: Verify Columns Exist

```bash
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d features" | grep lifecycle
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d work_items" | grep lifecycle
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d projects" | grep lifecycle
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d todo_items" | grep lifecycle
```

### Step 3: Test Data Insertion

```bash
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "
UPDATE projects SET lifecycle_state = 'ACTIVE' WHERE id = (SELECT id FROM projects LIMIT 1);
SELECT id, name, lifecycle_state FROM projects WHERE lifecycle_state IS NOT NULL;
"
```

---

## Phase 3: Application Verification

### Step 1: Verify Models Still Work

```bash
PYTHONPATH=. python -c "
from services.domain.models import Project, Feature, WorkItem, Todo
from services.shared_types import LifecycleState

# Verify model has attribute
p = Project.__new__(Project)
p.lifecycle_state = LifecycleState.ACTIVE
print(f'Project lifecycle_state: {p.lifecycle_state}')
"
```

### Step 2: Run Existing Tests

```bash
PYTHONPATH=. python -m pytest tests/unit/services/domain/ -v --tb=short
```

---

## Phase Z: Completion

### Acceptance Criteria Verification

- [ ] All four tables have `lifecycle_state` column (verified with `\d`)
- [ ] Column is nullable (existing rows unaffected)
- [ ] Column accepts valid LifecycleState values
- [ ] Domain tests pass
- [ ] No regressions

### Evidence Required

1. Migration file created
2. `alembic upgrade head` output
3. `\d table_name` showing column for all 4 tables
4. Test UPDATE/SELECT showing value persistence
5. pytest output for domain tests

---

## STOP Conditions

- Migration fails on any table
- Existing data corrupted
- Application fails to start after migration
- Model/DB mismatch remains after migration

---

## Effort Estimate

**Size**: Small
- Migration creation: trivial
- Verification: small
- Total: ~30 min

---

## Notes

- Using VARCHAR(50) rather than PostgreSQL ENUM for flexibility
- All columns nullable to avoid breaking existing rows
- Downgrade drops columns (data loss acceptable for dev)
