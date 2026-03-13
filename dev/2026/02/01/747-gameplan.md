# Gameplan: #747 - Schema Drift Fix (DateTime vs timestamptz)

**Issue**: #747 - TECH-DEBT: Schema drift - DateTime vs timestamptz mismatches
**Created**: 2026-02-01
**Priority**: P3 (Low - housekeeping)

---

## Phase -1: Infrastructure Verification (N/A - Simplified)

**Work Characteristics Assessment**:
- [ ] Single agent, sequential work
- [ ] Small fix (<30 min estimated)
- [ ] Low risk - type annotations only, no data migration

**Assessment**: SKIP WORKTREE - Simple housekeeping task, overhead exceeds benefit.

**Infrastructure Known**:
- Database: PostgreSQL on port 5433
- ORM: SQLAlchemy with Alembic migrations
- Schema validation exists (#484)
- Models in `services/database/models/` and `services/personality/models.py`

---

## Phase 0: Investigation

### 0.1 Identify Affected Files

```bash
# Find the model definitions for flagged columns
grep -r "conversational_memory_entries\|knowledge_nodes" services/ --include="*.py" -l

# Check model definitions
grep -rn "class.*MemoryEntry\|timestamp.*=.*Column\|embedding_vector" services/ --include="*.py"
```

### 0.2 Count utcnow() Usages

```bash
# Find all deprecated utcnow() calls
grep -rn "datetime.utcnow\|\.utcnow()" . --include="*.py" | grep -v ".pyc\|__pycache__"
```

### 0.3 Verify embedding_vector Intent

```bash
# Check if pgvector is used
grep -rn "pgvector\|Vector\|ARRAY.*Float" services/ --include="*.py"
```

**Deliverable**: List of files to modify, count of utcnow() usages, decision on embedding_vector.

---

## Phase 0.5: Frontend-Backend Contract (N/A)

Not applicable - backend-only changes, no API contract changes.

---

## Phase 0.6: Data Flow & Integration (N/A)

Not applicable - type annotation changes only, no data flow changes.

---

## Phase 0.7: Conversation Design (N/A)

Not applicable - not a conversational feature.

---

## Phase 0.8: Post-Completion Integration (N/A)

Not applicable - no state changes, just type alignment.

---

## Phase 1: Fix DateTime Model Definitions

### 1.1 Update conversational_memory_entries Model

**File**: (to be identified in Phase 0)

**Change**:
```python
# Before
timestamp = Column(DateTime, ...)
created_at = Column(DateTime, ...)

# After
timestamp = Column(DateTime(timezone=True), ...)
created_at = Column(DateTime(timezone=True), ...)
```

### 1.2 Verify Schema Validation

```bash
# Run server to check schema validation output
python main.py 2>&1 | head -50
# Should show "Mismatches found: 1" (embedding_vector) or 0
```

**Deliverable**: Model files updated, schema validation passes.

---

## Phase 2: Replace Deprecated utcnow()

### 2.1 Find and Replace

```bash
# Generate replacement commands
grep -rn "datetime.utcnow()" . --include="*.py" | grep -v ".pyc"
```

**Pattern**:
```python
# Before
from datetime import datetime
datetime.utcnow()

# After (option A - if timezone-aware needed)
from datetime import datetime, UTC
datetime.now(UTC)

# After (option B - if naive datetime acceptable)
from datetime import datetime, timezone
datetime.now(timezone.utc)
```

### 2.2 Verify No Deprecation Warnings

```bash
PYTHONPATH=. python -W error::DeprecationWarning -c "import services; print('OK')"
# Or run tests and check for warnings
PYTHONPATH=. python -m pytest tests/unit/ -v 2>&1 | grep -i "deprecat"
```

**Deliverable**: All utcnow() replaced, no deprecation warnings.

---

## Phase 3: Document embedding_vector Decision

### 3.1 Investigate

```bash
# Check if mismatch is intentional
grep -rn "embedding_vector\|pgvector" services/ docs/ --include="*.py" --include="*.md"
```

### 3.2 Document

If intentional (pgvector requirement):
- Add comment to model explaining why JSON vs float8 array
- Update #747 issue noting this is expected

If NOT intentional:
- Create follow-up issue for embedding_vector alignment
- Note in #747 that this is separate scope

**Deliverable**: Documentation or follow-up issue.

---

## Phase Z: Final Verification & Handoff

### Z.1 Run Full Verification

```bash
# Schema validation
python main.py 2>&1 | grep -A20 "Schema Validation"

# Tests
PYTHONPATH=. python -m pytest tests/unit/ -v --tb=short 2>&1 | tail -20

# Deprecation check
PYTHONPATH=. python -m pytest tests/unit/ -v 2>&1 | grep -c "utcnow"
```

### Z.2 Update GitHub Issue

- Check all acceptance criteria boxes
- Fill in completion matrix with evidence
- Add evidence section with terminal output

### Z.3 Request PM Review

```
@PM - Issue #747 complete:
- DateTime models aligned with DB schema
- utcnow() calls replaced (count: X)
- embedding_vector documented/deferred
- Tests passing
- No deprecation warnings

Please review and close if satisfied.
```

---

## Acceptance Criteria

- [ ] Server starts with 0 schema mismatches (or 1 documented exception for embedding_vector)
- [ ] No `datetime.utcnow()` in codebase
- [ ] No deprecation warnings in test output
- [ ] embedding_vector mismatch documented or fixed
- [ ] Existing tests pass

---

## STOP Conditions

- DateTime(timezone=True) causes test failures → investigate before proceeding
- Changing models requires data migration → escalate to PM
- embedding_vector change would break pgvector → document and defer
- More than 50 utcnow() usages → assess scope with PM

---

## Effort Estimate

| Phase | Estimate |
|-------|----------|
| Phase 0 | 10 min |
| Phase 1 | 15 min |
| Phase 2 | 20 min |
| Phase 3 | 5 min |
| Phase Z | 10 min |
| **Total** | ~1 hour |

---

## Evidence Collection Points

1. After Phase 0: File list, utcnow count, embedding decision
2. After Phase 1: Schema validation output
3. After Phase 2: Grep showing 0 utcnow matches
4. After Phase Z: Full test output, issue update

---

*Gameplan ready for execution when scheduled.*
