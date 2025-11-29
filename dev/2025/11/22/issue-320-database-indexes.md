# PERF-320: Add Missing Composite Database Indexes
**Priority**: P1 (Performance cliff at scale)
**Labels**: `performance`, `database`, `quick-win`, `scaling`
**Effort**: 4-6 hours
**Discovered by**: Ted Nadeau (architectural review)

---

## Problem

No composite indexes exist for common query patterns. Performance degrades catastrophically as data scales.

**Current state** (with 1K records):
- Conversation history query: ~200ms (table scan)
- File browsing: ~150ms (table scan)

**At 10K records**:
- Conversation history: ~2 seconds
- File browsing: ~1.5 seconds

**At 100K records**:
- Conversation history: ~20+ seconds (unusable)
- File browsing: ~15+ seconds (unusable)

## Solution

Add composite indexes for frequent query patterns:

```sql
-- 1. Conversation history (user's conversations by date)
CREATE INDEX idx_conversations_user_created
ON conversations(user_id, created_at DESC);

-- 2. Conversation turns (get turns in order)
CREATE INDEX idx_turns_conversation_number
ON conversation_turns(conversation_id, turn_number);

-- 3. File browsing (user's files by date)
CREATE INDEX idx_files_user_date
ON uploaded_files(user_id, upload_date DESC);

-- 4. Pattern learning (user's patterns by category)
CREATE INDEX idx_patterns_user_category
ON patterns(user_id, category);

-- 5. Audit trail (changes by entity)
CREATE INDEX idx_audit_entity_time
ON audit_logs(entity_type, entity_id, created_at DESC);
```

## Acceptance Criteria

- [ ] Create Alembic migration adding 5 composite indexes
- [ ] Benchmark query performance before indexes (baseline)
- [ ] Apply indexes to development database
- [ ] Benchmark query performance after indexes
- [ ] Verify 10x+ performance improvement on test data
- [ ] No breaking changes to existing queries
- [ ] Migration runs cleanly (up and down)

## Performance Targets

| Query | Current (1K rows) | Target (1K rows) | Target (100K rows) |
|-------|------------------|------------------|-------------------|
| User conversations | 200ms | 20ms | 200ms |
| Conversation turns | 150ms | 15ms | 150ms |
| User files | 150ms | 15ms | 150ms |
| User patterns | 100ms | 10ms | 100ms |
| Audit trail | 300ms | 30ms | 300ms |

## Implementation

```python
# alembic/versions/xxx_add_performance_indexes.py
def upgrade():
    # Add composite indexes
    op.create_index('idx_conversations_user_created',
                    'conversations',
                    ['user_id', 'created_at'])
    # ... etc

def downgrade():
    # Remove indexes
    op.drop_index('idx_conversations_user_created',
                  'conversations')
    # ... etc
```

## Testing

1. **Load test data** (1K, 10K, 100K records)
2. **Benchmark without indexes** (document baseline)
3. **Apply migration**
4. **Benchmark with indexes** (verify improvement)
5. **Test rollback** (migration down)
6. **Production simulation** (concurrent queries)

## Monitoring

After deployment, monitor:
- Query execution time (p50, p95, p99)
- Database CPU usage
- Index usage statistics (`pg_stat_user_indexes`)

---

*Quick win: 4-6 hours prevents performance catastrophe at scale*
