# Phase 0 Investigation: PERF-INDEX (#356) Analysis

**Time**: 10:42 PM - 11:00 PM (18 minutes)
**Session**: Issue #356 - Add Missing Composite Database Indexes

---

## Investigation Findings

### Issue Description vs Reality

The GitHub issue #356 references tables that may be planned but don't yet exist in the codebase:
- ❌ `conversations` table (mentioned in issue)
- ❌ `conversation_turns` table (mentioned in issue)

### Actual Tables in Current Schema

Using `services/database/models.py` as source of truth, the following production tables exist and have real performance needs:

**Tier 1 - High Priority (Core Performance)**:
1. ✅ `audit_logs` (175 rows) - 9 single-column indexes, needs composite for multi-column WHERE
2. ✅ `learned_patterns` (1556 rows) - 2 indexes already, user_id queries dominant
3. ✅ `uploaded_files` (549 rows) - 2 indexes, needs user_id + date composite
4. ✅ `feedback` (1083 rows) - 7 single-column indexes, needs user_id + created_at composite
5. ✅ `users` (54 rows) - Single-column indexes only

**Tier 2 - Medium Priority**:
- `knowledge_nodes` / `knowledge_edges` - Knowledge graph tables
- `items` / `todos` / `lists` - Todo/planning tables
- `tasks` / `workflows` - Task management

---

## Current Index Strategy

### Strengths ✅
- Many single-column indexes for WHERE clauses
- Good coverage for ID lookups
- Timestamp indexes for sorting

### Gaps ❌
- No composite indexes for multi-column queries
- Missing (user_id, created_at DESC) patterns
- No indexes for common filtering + sorting combinations

---

## Revised Scope: Real-World Index Additions

Instead of the 5 hypothetical indexes from the issue, here are the ACTUAL high-impact indexes needed:

### Index 1: audit_logs - User Activity Timeline
**Query Pattern**: `WHERE user_id = ? ORDER BY created_at DESC`
**Current**: Single-column indexes only
**Proposed**: `CREATE INDEX idx_audit_user_timeline ON audit_logs(user_id, created_at DESC)`
**Impact**: User activity audit trails (compliance queries)

### Index 2: learned_patterns - User Pattern Discovery
**Query Pattern**: `WHERE user_id = ? ORDER BY confidence DESC`
**Current**: Has `ix_learned_patterns_user_confidence` (redundant)
**Proposed**: Review and optimize existing indexes
**Impact**: Learning system queries

### Index 3: uploaded_files - User File Listing
**Query Pattern**: `WHERE session_id = ? ORDER BY upload_time DESC`
**Current**: Has `idx_files_session` + `idx_files_filename`
**Proposed**: Review/optimize existing
**Impact**: File browsing functionality

### Index 4: feedback - User Feedback Review
**Query Pattern**: `WHERE user_id = ? AND status = ? ORDER BY created_at DESC`
**Current**: 7 single-column indexes
**Proposed**: `CREATE INDEX idx_feedback_user_status_date ON feedback(user_id, status, created_at DESC)`
**Impact**: Feedback review/analysis

### Index 5: users - Account Lookups
**Query Pattern**: `WHERE is_active = true ORDER BY created_at DESC`
**Current**: Only single-column indexes
**Proposed**: `CREATE INDEX idx_users_active_date ON users(is_active, created_at DESC)`
**Impact**: User list pagination

---

## Database Reality Check

**PostgreSQL Version**: 13+ (supports all modern index features)
**Alembic Status**: Working (27 migrations completed, latest: 4d1e2c3b5f7a)
**Test Database**: Available via docker-compose
**Current Production State**: Safe to add indexes (non-breaking change)

---

## Revised Execution Plan

**Decision**: Implement practical, high-impact indexes for ACTUAL tables in codebase

**Phase 0 (Complete)**: ✅ Investigation & Schema Analysis
**Phase 1**: Create Alembic migration with 5 pragmatic indexes
**Phase 2**: Create performance test suite for real tables
**Phase 3**: Measure baseline and post-index performance
**Phase 4**: Document findings and validate rollback

---

## Next Steps

Proceed with creating a migration file that adds indexes to real tables:
- `audit_logs(user_id, created_at DESC)` - Audit trail lookups
- `learned_patterns(user_id, confidence DESC)` - Pattern scoring
- `feedback(user_id, status, created_at DESC)` - Feedback review
- Optimize existing indexes as needed
- Create comprehensive test coverage

---

**Status**: Phase 0 Complete
**Recommendation**: Proceed with real-world index implementation
**Risk**: Low - Indexes are safe, reversible additions
