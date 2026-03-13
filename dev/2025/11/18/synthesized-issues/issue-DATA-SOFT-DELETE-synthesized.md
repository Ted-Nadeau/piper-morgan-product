# DATA-SOFT-DELETE - Implement Soft Delete Strategy Across Domain Models

**Priority**: P1 (Compliance requirement)
**Labels**: `database`, `compliance`, `data-safety`, `priority: high`
**Milestone**: MVP - Data Management
**Epic**: Data Safety & Compliance
**Related**: Issue #321 (Audit field standardization), ADR-TBD (soft delete strategy)

---

## Problem Statement

### Current State
**Hard deletion everywhere**: When records are deleted, they're permanently removed from the database with no recovery mechanism.

**Current delete pattern**:
```python
# Services currently use hard deletes
await session.delete(conversation)
await session.commit()
# Record is GONE - cannot recover, no audit trail
```

**Consequences**:
- ❌ **Data loss**: No recovery if user deletes by mistake
- ❌ **Broken audit trails**: References to deleted entities lost
- ❌ **Compliance violations**: GDPR "right to be forgotten" requires proof of deletion + retention
- ❌ **Referential integrity issues**: Foreign key relationships break when parents deleted
- ❌ **Analytics blind spots**: Cannot analyze deletion patterns or user behavior
- ❌ **SOC2 audit failure**: Lost audit evidence for deleted records

### Root Cause
Domain models inherit from basic `Base` class without soft delete fields. Repositories use `session.delete()` directly, no soft delete infrastructure exists.

**Existing partial implementation**:
- `audit_logs` table has `deleted_at` field (unused elsewhere)
- Issue #321 proposes `AuditedModel` but doesn't specify delete behavior
- No repository pattern for soft delete filtering

### Impact
- **Blocks**: GDPR compliance, SOC2 certification, enterprise adoption
- **User Impact**: Deleted data cannot be recovered; support burden for "I deleted it by accident!"
- **Technical Debt**: Every hard delete makes future soft delete migration harder
- **Strategic Context**: Must implement before production data or regret it

---

## Goal

**Primary Objective**: Implement transparent soft delete pattern across all domain models, enabling data recovery, compliance audits, and GDPR-compliant "right to be forgotten" workflows.

**Example User Experience**:
```
Before: User deletes conversation accidentally → Lost forever ❌
After: User deletes conversation → Soft-deleted, can restore within 90 days ✅
After 90 days: Automatically hard-deleted for GDPR compliance ✅
```

**Not In Scope** (explicitly):
- ❌ Archive tables (separate schema, not in scope)
- ❌ Full-text search on deleted records (deferred)
- ❌ Permanent deletion API for users (admin-only hard delete first)
- ❌ GDPR anonymization service (Phase 2, post-MVP)
- ❌ Cascade behavior automation (manual for now)

---

## What Already Exists

### Infrastructure ✅
- `AuditedModel` base class being designed (Issue #321)
- Alembic migration framework operational
- Repository pattern partially in place
- Audit logging infrastructure exists
- `deleted_at` field pattern (in audit_logs table)

### What's Missing ❌
- Soft delete fields (`deleted_at`, `deleted_by`) on domain models
- Soft delete filtering in repository queries
- `soft_delete()` and `restore()` methods
- Migration script for all tables
- API endpoints for restore
- Partial unique indexes (for deleted records re-registration)
- Hard delete cleanup job
- GDPR compliance service (Phase 2)

---

## Requirements

### Phase 0: Design Review
- [ ] Review Issue #321 `AuditedModel` design
- [ ] Confirm soft delete fields: `deleted_at` (datetime), `deleted_by` (FK)
- [ ] Confirm cascade behavior (cascade soft deletes vs orphan)
- [ ] Identify all domain tables inheriting AuditedModel

### Phase 1: Base Model Enhancement
**Objective**: Add soft delete support to AuditedModel base class

**Tasks**:
- [ ] Update `services/database/models.py` - AuditedModel class
- [ ] Add `deleted_at` column (DateTime, nullable)
- [ ] Add `deleted_by` column (Integer FK to users.id)
- [ ] Add `@hybrid_property is_deleted` for queries
- [ ] Add `soft_delete(user_id)` method
- [ ] Add `restore(user_id)` method
- [ ] Add `is_deleted` property for filtering
- [ ] Unit test soft delete/restore methods

**Deliverables**:
- Updated AuditedModel with soft delete support
- Unit tests covering soft delete/restore
- Code examples for model usage

### Phase 2: Repository Pattern Updates
**Objective**: Make repositories soft-delete aware

**Tasks**:
- [ ] Update `BaseRepository` class
- [ ] Add `include_deleted: bool = False` parameter to constructor
- [ ] Implement `_apply_soft_delete_filter()` method
- [ ] Update `find_by_id()` to filter deleted records
- [ ] Update `find_all()` to filter deleted records
- [ ] Add `soft_delete(id, user_id)` method
- [ ] Add `restore(id, user_id)` method
- [ ] Add `find_deleted(id)` method for admin restores
- [ ] Add audit logging for soft delete/restore actions
- [ ] Unit test repository soft delete behavior

**Deliverables**:
- Updated BaseRepository class
- Unit tests for all repository methods
- Documentation on repository usage

### Phase 3: Database Migration
**Objective**: Add soft delete columns to all existing tables

**Tasks**:
- [ ] Create Alembic migration: `XXX_add_soft_delete_columns.py`
- [ ] Add `deleted_at` column to all AuditedModel tables:
  - users, lists, list_items, intents, workflows, tasks
  - conversations, conversation_turns, patterns
  - knowledge_nodes, knowledge_edges, uploaded_files
  - (and any other domain tables)
- [ ] Add `deleted_by` column with FK to users.id
- [ ] Create index on `deleted_at` for filtering performance
- [ ] Create partial unique indexes for unique constraints (email, etc.)
- [ ] Test migration up and down
- [ ] Verify no data loss

**Deliverables**:
- Migration file (`alembic/versions/XXX_*.py`)
- Index creation DDL
- Migration test evidence

### Phase 4: Application Updates
**Objective**: Replace hard deletes with soft deletes throughout codebase

**Tasks**:
- [ ] Audit all `session.delete()` calls in codebase
- [ ] Replace with `repository.soft_delete(id, user_id)` calls
- [ ] Update all delete endpoints in API to use soft delete
- [ ] Add `/api/v1/{resource}/{id}/restore` endpoints for soft-deleted items
- [ ] Update API documentation for delete/restore behavior
- [ ] Handle cascade deletes (soft delete parents/children relationship)
- [ ] Handle unique constraint violations (re-registering with deleted email)
- [ ] End-to-end testing of delete → restore workflow

**Deliverables**:
- All hard deletes replaced with soft deletes
- Restore endpoints implemented
- API documentation updated
- Integration tests for delete/restore

### Phase 5: Cleanup & Retention
**Objective**: Permanent deletion after retention period for GDPR compliance

**Tasks**:
- [ ] Create `services/maintenance/soft_delete_cleaner.py`
- [ ] Implement `clean_expired_deletions(retention_days=90)`
- [ ] Permanent deletion of records soft-deleted >90 days
- [ ] Audit logging before permanent deletion
- [ ] Schedule cleanup job (runs weekly)
- [ ] Monitor for compliance
- [ ] Documentation on retention policy

**Deliverables**:
- SoftDeleteCleaner service
- Scheduled cleanup job configuration
- Retention policy documentation

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Comprehensive testing completed
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] Session log completed

---

## Acceptance Criteria

### Model Updates
- [ ] `deleted_at` (DateTime, nullable) column exists on all models
- [ ] `deleted_by` (Integer FK) column exists on all models
- [ ] `is_deleted` property returns True when `deleted_at` is not null
- [ ] `soft_delete(user_id)` method sets `deleted_at` and `deleted_by`
- [ ] `restore(user_id)` method clears `deleted_at` and `deleted_by`

### Repository Pattern
- [ ] `BaseRepository` auto-filters soft-deleted records by default
- [ ] `include_deleted=True` parameter includes deleted records (admin queries)
- [ ] `soft_delete(id, user_id)` marks record as deleted
- [ ] `restore(id, user_id)` restores soft-deleted record
- [ ] Audit logging on all soft delete/restore operations
- [ ] Foreign key constraints remain valid for deleted records

### Migration
- [ ] All AuditedModel tables have soft delete columns
- [ ] Indexes created on `deleted_at` columns
- [ ] Partial unique indexes for unique constraints
- [ ] Migration tested up and down
- [ ] Zero data loss verified

### Application Layer
- [ ] All hard deletes replaced with soft deletes
- [ ] DELETE endpoints return soft delete result
- [ ] POST `/api/v1/{resource}/{id}/restore` endpoints exist
- [ ] API documentation updated
- [ ] Delete/restore operations audit-logged

### Testing
- [ ] Unit tests for model soft delete/restore (>10 tests)
- [ ] Unit tests for repository soft delete pattern (>10 tests)
- [ ] Integration tests for delete→restore workflows
- [ ] Migration tests (up/down)
- [ ] API endpoint tests (delete, restore, list)
- [ ] Edge case tests (cascade behavior, unique constraints)
- [ ] Cleanup job tests

### Documentation
- [ ] Soft delete strategy documented
- [ ] Repository usage guide with examples
- [ ] API documentation (delete vs restore semantics)
- [ ] Migration guide for developers
- [ ] Retention policy documented (90 days)
- [ ] GDPR compliance notes
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| AuditedModel soft delete fields | ❌ | [commit] |
| soft_delete() and restore() methods | ❌ | [commit] |
| BaseRepository soft delete logic | ❌ | [commit] |
| Migration created | ❌ | [migration file] |
| Indexes created | ❌ | [migration output] |
| All hard deletes replaced | ❌ | [commits] |
| API restore endpoints | ❌ | [commits] |
| Model unit tests | ❌ | [test output] |
| Repository unit tests | ❌ | [test output] |
| Integration tests | ❌ | [test output] |
| SoftDeleteCleaner job | ❌ | [commit] |
| Documentation completed | ❌ | [doc files] |

**Definition of COMPLETE**:
- ✅ All soft delete fields added to models
- ✅ All hard deletes replaced with soft deletes
- ✅ Restore functionality fully tested
- ✅ Cleanup job scheduled and working
- ✅ 100% test coverage for soft delete logic
- ✅ GDPR retention policy implemented

**NOT complete means**:
- ❌ "Models updated, but not all hard deletes replaced"
- ❌ "Soft delete works, but cleanup job deferred"
- ❌ "Most tables support soft delete, a few didn't"
- ❌ Any rationalization of incompleteness

---

## Testing Strategy

### Unit Tests: Model Soft Delete
```python
# tests/unit/services/database/test_soft_delete_models.py

def test_soft_delete_sets_deleted_at_and_deleted_by():
    conversation = Conversation(...)
    conversation.soft_delete(user_id=123)

    assert conversation.deleted_at is not None
    assert conversation.deleted_by == 123
    assert conversation.is_deleted is True

def test_restore_clears_deleted_fields():
    conversation = Conversation(...)
    conversation.soft_delete(user_id=123)
    conversation.restore(user_id=456)

    assert conversation.deleted_at is None
    assert conversation.deleted_by is None
    assert conversation.is_deleted is False
```

### Unit Tests: Repository Filtering
```python
# tests/unit/services/domain/repositories/test_soft_delete_filtering.py

@pytest.mark.asyncio
async def test_find_by_id_excludes_deleted_by_default(db_session):
    # Create and soft-delete a conversation
    conv = await conversation_repo.create(...)
    await conversation_repo.soft_delete(conv.id, user_id=123)

    # find_by_id should not find deleted record
    result = await conversation_repo.find_by_id(conv.id)
    assert result is None

@pytest.mark.asyncio
async def test_find_by_id_includes_deleted_when_flag_set(db_session):
    # Create and soft-delete a conversation
    conv = await conversation_repo.create(...)
    await conversation_repo.soft_delete(conv.id, user_id=123)

    # find_by_id with include_deleted should find it
    repo = ConversationRepository(db_session, include_deleted=True)
    result = await repo.find_by_id(conv.id)
    assert result is not None
    assert result.is_deleted
```

### Integration Tests: Delete/Restore Workflow
```python
# tests/integration/test_soft_delete_workflow.py

@pytest.mark.asyncio
async def test_delete_and_restore_conversation():
    # Create conversation
    conv = await conversation_repo.create(user_id=1, content="test")
    conv_id = conv.id

    # Soft delete
    await conversation_repo.soft_delete(conv_id, user_id=1)

    # Verify deleted
    result = await conversation_repo.find_by_id(conv_id)
    assert result is None

    # Verify can find with include_deleted
    repo_with_deleted = ConversationRepository(db_session, include_deleted=True)
    result = await repo_with_deleted.find_by_id(conv_id)
    assert result.is_deleted

    # Restore
    await conversation_repo.restore(conv_id, user_id=1)

    # Verify restored
    result = await conversation_repo.find_by_id(conv_id)
    assert result is not None
    assert not result.is_deleted
```

### API Tests: Restore Endpoint
```python
# tests/integration/test_soft_delete_api.py

@pytest.mark.asyncio
async def test_delete_conversation_via_api(client, auth_headers):
    # Create conversation
    response = await client.post(
        "/api/v1/conversations",
        json={"content": "test"},
        headers=auth_headers
    )
    conv_id = response.json()["id"]

    # Delete via API
    response = await client.delete(
        f"/api/v1/conversations/{conv_id}",
        headers=auth_headers
    )
    assert response.status_code == 200

    # Verify soft-deleted
    response = await client.get(
        f"/api/v1/conversations/{conv_id}",
        headers=auth_headers
    )
    assert response.status_code == 404  # Not found (soft deleted)

@pytest.mark.asyncio
async def test_restore_conversation_via_api(client, auth_headers):
    # Create and delete conversation
    conv = await create_and_delete_conversation()
    conv_id = conv.id

    # Restore via API
    response = await client.post(
        f"/api/v1/conversations/{conv_id}/restore",
        headers=auth_headers
    )
    assert response.status_code == 200

    # Verify restored
    response = await client.get(
        f"/api/v1/conversations/{conv_id}",
        headers=auth_headers
    )
    assert response.status_code == 200
```

---

## Success Metrics

### Quantitative
- **Coverage**: 100% of domain models support soft delete
- **Hard deletes eliminated**: 0 hard deletes in codebase
- **Test coverage**: >90% for soft delete logic
- **Recovery time**: <1 second for restore operations
- **Retention enforcement**: 100% of records >90 days soft-deleted → hard-deleted

### Qualitative
- Developers find soft delete pattern intuitive
- Support team has fewer "I deleted it by accident" tickets
- Compliance team confirms GDPR readiness
- No performance regression from filtering deleted records

---

## STOP Conditions

**STOP immediately and escalate if**:
- Soft delete breaks foreign key constraints (use `ON DELETE SET NULL` if needed)
- Query performance degrades >10% (index `deleted_at` column, check query plans)
- Any data loss during migration (verify before/after record counts)
- Restore operations fail (test rollback procedure)
- Cascade delete behavior breaks relationships (document cascade rules explicitly)

**When stopped**: Document the issue, propose solution (index, constraint modification, cascade rule), wait for PM decision.

---

## Effort Estimate

**Overall Size**: Large

**Breakdown by Phase**:
- Phase 0 (Design review): 1 hour
- Phase 1 (Model enhancement): 4 hours
- Phase 2 (Repository updates): 6 hours
- Phase 3 (Migration): 4 hours
- Phase 4 (Application updates): 10 hours
- Phase 5 (Cleanup/retention): 6 hours
- Testing: 12 hours
- Documentation: 4 hours

**Total**: 47 hours (1 week for single developer)

**Complexity Notes**:
- High impact - touches all domain models
- Cascade behavior needs careful design
- Migration is large but relatively straightforward
- Testing must be comprehensive (compliance-critical)
- Post-MVP: GDPR anonymization service (separate work)

---

## Dependencies

### Required (Must be complete first)
- [ ] Issue #321 `AuditedModel` design finalized
- [ ] PostgreSQL database operational
- [ ] Alembic migrations working
- [ ] All domain models created

### Optional (Nice to have)
- [ ] Audit logging infrastructure (exists)
- [ ] Performance monitoring (for query impact)

---

## Related Documentation

- **Architecture**:
  - ADR-TBD: Soft delete strategy (to be created)
  - Issue #321: Audit field standardization
- **Compliance**:
  - GDPR Article 17: Right to erasure
  - SOC2: Audit trail requirements
- **Code**:
  - `services/database/models.py` - Domain models
  - `services/domain/repositories/` - Repository pattern
  - `alembic/` - Migration framework

---

## Evidence Section

[This section is filled in during/after implementation]

### Migration Evidence
```sql
-- Verify soft delete columns added
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'conversations' AND column_name IN ('deleted_at', 'deleted_by');

-- Output should show both columns exist
-- deleted_at: timestamp without time zone, nullable
-- deleted_by: integer, nullable (FK)
```

### Test Results
```
Test Summary for Soft Delete Implementation:
- Model soft delete: 10 tests PASSED ✅
- Repository filtering: 8 tests PASSED ✅
- Integration workflow: 6 tests PASSED ✅
- API endpoints: 8 tests PASSED ✅
- Migration: 4 tests PASSED ✅

Total: 36 tests PASSED, 0 FAILED ✅
```

---

## Completion Checklist

Before requesting PM review:
- [ ] All domain models support soft delete ✅
- [ ] All hard deletes replaced with soft deletes ✅
- [ ] Migration created and tested ✅
- [ ] Restore endpoints implemented and tested ✅
- [ ] All tests passing (>95% coverage) ✅
- [ ] Documentation complete ✅
- [ ] GDPR retention policy in place ✅
- [ ] Session log completed ✅

**Status**: Not Started

---

## Notes for Implementation

**From Pair Issues #333 and #336**:
- Both issues identified same problem from different angles
- #333 focused on compliance, #336 on implementation patterns
- Synthesized approach combines both perspectives
- Prioritize cascade behavior definition early

**Cascade Delete Decision Needed**:
- **Question**: When parent soft-deleted, cascade to children?
- **Option A**: Cascade (soft delete all children too)
- **Option B**: Orphan (leave children active, FK still valid)
- **Recommendation**: Cascade for owned children (list → list_items), orphan for references
- **Decision needed from PM**

**Unique Constraint Edge Case**:
```sql
-- User deletes account (soft delete)
-- User re-registers with same email → constraint violation!

-- Solution: Partial unique index
CREATE UNIQUE INDEX idx_users_email_unique
ON users(email)
WHERE deleted_at IS NULL;
```

---

**Remember**:
- Soft delete is safer than hard delete - always choose soft
- Every query now filters deleted records - index on `deleted_at`
- Cascade behavior must be explicit and tested
- GDPR compliance requires both soft delete AND hard delete after retention
- Phase 2 GDPR anonymization service is separate work

---

_Issue created: November 20, 2025_
_Last updated: November 20, 2025_
_Synthesized from: #333 + #336_
