# PERF-INDEX - Add Missing Composite Database Indexes

**Priority**: P1 (Performance cliff at scale)
**Labels**: `performance`, `database`, `priority: high`
**Milestone**: MVP Performance
**Epic**: Performance & Scalability
**Related**: ADR (database indexing strategy to be created)

**Discovered by**: Ted Nadeau (architectural review during GREAT-3)

---

## Problem Statement

### Current State
No composite indexes exist for common multi-column query patterns. Performance degrades catastrophically as data scales.

**Performance at Different Data Scales**:
| Query | 1K Records | 10K Records | 100K Records |
|-------|-----------|------------|------------|
| Conversation history (user_id, created_at) | ~200ms | ~2 seconds | ~20+ seconds ❌ |
| Conversation turns (conversation_id, turn_number) | ~150ms | ~1.5 seconds | ~15+ seconds ❌ |
| File browsing (user_id, upload_date) | ~150ms | ~1.5 seconds | ~15+ seconds ❌ |
| Pattern queries (user_id, category) | ~100ms | ~1 second | ~10+ seconds ❌ |
| Audit trail (entity_type, entity_id, created_at) | ~300ms | ~3 seconds | ~30+ seconds ❌ |

All queries use O(n) table scans instead of O(log n) index lookups.

### Root Cause
Tables created during initial implementation without composite indexes for multi-column WHERE clauses and JOIN operations. Discovery made during GREAT-3 architecture review by Ted Nadeau.

### Impact
- **Blocks**: Cannot scale to production data volumes
- **User Impact**: Response times > 10 seconds make product unusable at scale
- **Technical Debt**: Every day of development without indexes makes production migration harder
- **Strategic Context**: Must fix before performance testing or customer trials

---

## Goal

**Primary Objective**: Add 5 composite indexes covering all common query patterns, achieving 10x+ performance improvement on multi-column queries while maintaining zero downtime.

**Example User Experience**:
```
Before: "List my conversations" takes 20 seconds at 100K records ❌
After: "List my conversations" takes 200ms at 100K records ✅
```

**Not In Scope** (explicitly):
- ❌ Index optimization via EXPLAIN ANALYZE (can iterate later)
- ❌ Materialized views for complex queries (future optimization)
- ❌ Read replicas or sharding (infrastructure-level)
- ❌ Full-text search indexes (separate feature)

---

## What Already Exists

### Infrastructure ✅
- Alembic migration framework operational
- PostgreSQL 13+ (supports all index types)
- Existing performance monitoring in monitoring service
- Query logging configured

### What's Missing ❌
- Composite indexes on 5 key tables
- Performance baseline measurements
- Index performance validation
- Rollback testing for index migrations

---

## Requirements

### Phase 0: Performance Baseline
- [ ] Benchmark all 5 query patterns at 1K records (establish baseline)
- [ ] Document current execution plans (EXPLAIN ANALYZE output)
- [ ] Identify any existing indexes that might conflict

### Phase 1: Index Creation Migration
**Objective**: Create Alembic migration adding 5 composite indexes

**Tasks**:
- [ ] Create migration: `alembic/versions/XXX_add_performance_indexes.py`
- [ ] Index 1: `conversations(user_id, created_at DESC)` - Conversation history queries
- [ ] Index 2: `conversation_turns(conversation_id, turn_number)` - Sequential turn retrieval
- [ ] Index 3: `uploaded_files(user_id, upload_date DESC)` - File browsing/listing
- [ ] Index 4: `patterns(user_id, category)` - Pattern learning queries
- [ ] Index 5: `audit_logs(entity_type, entity_id, created_at DESC)` - Audit trail queries
- [ ] Test migration up: `alembic upgrade head`
- [ ] Test migration down: `alembic downgrade -1`

**Deliverables**:
- Migration file with all 5 indexes
- Index creation DDL verified

### Phase 2: Performance Validation
**Objective**: Verify 10x+ performance improvement and no query breakage

**Tasks**:
- [ ] Apply indexes to development database
- [ ] Benchmark all 5 query patterns again (post-index)
- [ ] Calculate improvement factor (should be 10x+)
- [ ] Run full test suite - verify no query breakage
- [ ] Test all 5 query patterns with edge cases (empty results, single result, all results)
- [ ] Verify index statistics updated (ANALYZE)

**Deliverables**:
- Performance benchmark report (`docs/database/index-performance.md`)
- Before/after comparison table
- Test output showing all tests passing

### Phase 3: Rollback Testing
**Objective**: Verify migration can be safely rolled back if needed

**Tasks**:
- [ ] Create backup of production schema
- [ ] Apply migration: `alembic upgrade head`
- [ ] Verify indexes created: `SELECT * FROM pg_indexes`
- [ ] Rollback migration: `alembic downgrade -1`
- [ ] Verify indexes removed
- [ ] Verify no data loss

**Deliverables**:
- Rollback procedure documented
- Evidence of successful rollback

### Phase Z: Completion & Handoff
- [ ] All acceptance criteria met
- [ ] Performance targets achieved
- [ ] Documentation updated
- [ ] GitHub issue fully updated
- [ ] Session log completed

---

## Acceptance Criteria

### Indexes Created
- [ ] `conversations(user_id, created_at DESC)` exists in production
- [ ] `conversation_turns(conversation_id, turn_number)` exists
- [ ] `uploaded_files(user_id, upload_date DESC)` exists
- [ ] `patterns(user_id, category)` exists
- [ ] `audit_logs(entity_type, entity_id, created_at DESC)` exists

### Performance Targets (1K records)
- [ ] Conversation history query: <20ms (from 200ms)
- [ ] Conversation turns query: <15ms (from 150ms)
- [ ] File browsing query: <15ms (from 150ms)
- [ ] Pattern queries: <10ms (from 100ms)
- [ ] Audit trail query: <30ms (from 300ms)

### Performance Targets (100K records)
- [ ] Conversation history: <200ms (from 20+ seconds)
- [ ] Conversation turns: <150ms (from 15+ seconds)
- [ ] File browsing: <150ms (from 15+ seconds)
- [ ] Pattern queries: <100ms (from 10+ seconds)
- [ ] Audit trail: <300ms (from 30+ seconds)

### Testing
- [ ] All existing tests pass (no query breakage)
- [ ] 5 query patterns tested with various data volumes
- [ ] Migration up and down tested successfully
- [ ] Performance improvement measured at 1K and 100K records

### Documentation
- [ ] Performance benchmark report created
- [ ] Index strategy documented
- [ ] Migration procedure documented
- [ ] Rollback procedure documented
- [ ] Session log completed

---

## Completion Matrix

| Component | Status | Evidence Link |
|-----------|--------|---------------|
| Baseline performance measurement | ❌ | [EXPLAIN output] |
| Migration created | ❌ | [commit] |
| Indexes created in dev | ❌ | [pg_indexes output] |
| Post-index benchmarks | ❌ | [benchmark report] |
| Performance targets met | ❌ | [measurements] |
| All tests passing | ❌ | [test output] |
| Rollback tested | ❌ | [rollback log] |
| Documentation updated | ❌ | [doc files] |

**Definition of COMPLETE**:
- ✅ All 5 indexes created
- ✅ 10x+ performance improvement verified
- ✅ All tests passing
- ✅ Rollback tested and documented

**NOT complete means**:
- ❌ "4 of 5 indexes created"
- ❌ "Most queries faster but some still slow"
- ❌ "Performance improved but rollback not tested"

---

## Testing Strategy

### Performance Baseline Tests
```python
# tests/integration/test_database_performance.py

import time
import asyncio

@pytest.mark.asyncio
async def test_baseline_conversation_history_performance(db_session):
    """Measure baseline query time before indexes"""
    # Create 1000 test conversations
    await create_test_conversations(db_session, user_id="test-user", count=1000)

    # Time the query
    start = time.time()
    query = db_session.query(Conversation).filter(
        Conversation.user_id == "test-user"
    ).order_by(Conversation.created_at.desc())
    results = await query.all()
    elapsed = time.time() - start

    # Log baseline
    print(f"Conversation history query (1K records): {elapsed*1000:.2f}ms")
    assert len(results) == 1000
```

### Post-Index Performance Tests
```python
@pytest.mark.asyncio
async def test_indexed_conversation_history_performance(db_session):
    """Measure query time after indexes applied"""
    # Same test as above, but after indexes created
    # Should be 10x faster

    await create_test_conversations(db_session, user_id="test-user", count=1000)

    start = time.time()
    query = db_session.query(Conversation).filter(
        Conversation.user_id == "test-user"
    ).order_by(Conversation.created_at.desc())
    results = await query.all()
    elapsed = time.time() - start

    print(f"Conversation history query (indexed, 1K records): {elapsed*1000:.2f}ms")
    assert elapsed < 0.02  # Target: <20ms
```

### Migration Tests
```python
def test_index_migration_up_down(alembic_config):
    """Test migration can be applied and rolled back safely"""
    from alembic.command import upgrade, downgrade

    # Apply migration
    upgrade(alembic_config, 'head')

    # Verify indexes exist
    inspector = inspect(engine)
    indexes = inspector.get_indexes('conversations')
    assert any(ix['name'] == 'idx_conversations_user_created' for ix in indexes)

    # Rollback migration
    downgrade(alembic_config, '-1')

    # Verify indexes removed
    inspector = inspect(engine)
    indexes = inspector.get_indexes('conversations')
    assert not any(ix['name'] == 'idx_conversations_user_created' for ix in indexes)
```

### Query Plan Verification
```bash
# Before indexes
EXPLAIN ANALYZE
SELECT * FROM conversations
WHERE user_id = 'test-user'
ORDER BY created_at DESC;

# Should show: Seq Scan on conversations, ~200ms

# After indexes
EXPLAIN ANALYZE
SELECT * FROM conversations
WHERE user_id = 'test-user'
ORDER BY created_at DESC;

# Should show: Index Scan using idx_conversations_user_created, ~20ms
```

---

## Success Metrics

### Quantitative
- **Performance improvement**: 10x+ on all 5 queries
- **Query execution time at 100K records**: <300ms for all queries
- **Index creation time**: <5 seconds (negligible migration impact)
- **Test pass rate**: 100% (zero query breakage)

### Qualitative
- DBA confirms indexes are well-designed
- No unexpected query plan changes
- Rollback procedure works reliably
- Performance predictable across data volumes

---

## STOP Conditions

**STOP immediately and escalate if**:
- Index creation breaks existing queries (verify with EXPLAIN ANALYZE, don't skip)
- Performance improvement <5x (investigate missing or wrong indexes)
- Migration rollback fails (use manual procedure, document issue)
- Index creation takes >30 seconds (investigate if size is unexpected)
- Any test fails post-index (fix query, don't remove index)

**When stopped**: Document the issue, check index design with DBA, wait for PM decision.

---

## Effort Estimate

**Overall Size**: Small

**Breakdown by Phase**:
- Phase 0 (Baseline): 1 hour
- Phase 1 (Migration): 2 hours
- Phase 2 (Validation): 2 hours
- Phase 3 (Rollback testing): 1 hour

**Total**: 6 hours (0.75 days)

**Complexity Notes**:
- Low risk - indexes don't change data
- Can be safely applied/removed anytime
- Performance benefits immediate and measurable
- No application code changes needed

---

## Dependencies

### Required (Must be complete first)
- [ ] PostgreSQL database operational
- [ ] Alembic migrations working
- [ ] All tables created with current schema

### Optional (Nice to have)
- [ ] Performance monitoring tools (for ongoing tracking)
- [ ] Load testing environment (for stress testing)

---

## Related Documentation

- **Architecture**:
  - ADR (to be created): Database indexing strategy
- **Database**:
  - `services/database/models.py` - Domain models
  - Alembic migrations directory
- **Performance**:
  - `docs/database/schema.md` - Current schema documentation

---

## Evidence Section

[This section is filled in during/after implementation]

### Baseline Measurements
```
Conversation history (user_id, created_at DESC):
- 1K records: 200ms
- 10K records: 2000ms
- 100K records: 20000ms+

Conversation turns (conversation_id, turn_number):
- 1K records: 150ms
- 10K records: 1500ms
- 100K records: 15000ms+

[... other queries ...]
```

### Post-Index Measurements
```
Conversation history (user_id, created_at DESC):
- 1K records: 18ms (11x improvement)
- 10K records: 45ms (44x improvement)
- 100K records: 180ms (111x improvement)

[... other queries ...]
```

---

## Completion Checklist

Before requesting PM review:
- [ ] Baseline measurements recorded ✅
- [ ] Migration created and tested ✅
- [ ] Indexes verified in database ✅
- [ ] Performance targets achieved ✅
- [ ] All tests passing ✅
- [ ] Rollback tested ✅
- [ ] Documentation complete ✅
- [ ] Session log completed ✅

**Status**: Not Started

---

## Notes for Implementation

**From Ted Nadeau review**:
- This is a critical blocker for scale testing
- Should be done early in MVP development
- Consider full index analysis with DBA before production

**Performance Monitoring** (ongoing):
- Monitor index usage regularly
- Watch for query plan regressions
- Document any new slow queries discovered

---

**Remember**:
- Indexes are safe - apply liberally, remove if needed
- Always verify with EXPLAIN ANALYZE
- Performance must be measured, not guessed
- Document both before and after states

---

_Issue created: November 20, 2025_
_Last updated: November 20, 2025_
_Synthesized from: #320 + #356_
