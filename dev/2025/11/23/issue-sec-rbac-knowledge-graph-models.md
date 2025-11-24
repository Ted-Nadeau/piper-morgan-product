# Issue: Complete SEC-RBAC Migration for KnowledgeGraph Models

**Date**: November 23-24, 2025
**Priority**: P2 (Post-Alpha)
**Related**: Issue #357 (SEC-RBAC Phase 1), Issue #378 (ALPHA-DEPLOY-PROD)
**Type**: Bug/Migration Completion

---

## Problem Statement

During Issue #378 deployment preparation, discovered incomplete SEC-RBAC migration in KnowledgeGraph models. Database has `owner_id` columns but models.py doesn't define them, causing schema/model mismatch.

---

## Root Cause

FileRepository systematic session_id → owner_id migration revealed broader pattern: multiple models have database schema updated but Python models not updated.

---

## Affected Models

From `services/database/models.py`:

### 1. KnowledgeNodeDB (lines 621-635)
```python
class KnowledgeNodeDB(Base):
    __tablename__ = "knowledge_nodes"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    node_type = Column(Enum(NodeType), nullable=False)
    description = Column(Text)
    node_metadata = Column(JSON, default=dict)
    properties = Column(JSON, default=dict)
    session_id = Column(String)  # ❌ Should have owner_id too
    # Database HAS owner_id (added by migration) but model doesn't define it
```

**Problem**:
- Database table has `owner_id` column (from SEC-RBAC migrations)
- Model only defines `session_id`
- Causes AttributeError when trying to filter by owner_id

### 2. KnowledgeEdgeDB (likely same issue)
- Need to verify if database has owner_id
- Need to add to model if present

### 3. LearningPatternFeedback (needs investigation)
- Determine if this should have owner_id
- Add if needed for multi-user privacy

---

## Evidence

**From FileRepository fix session** (Nov 23, 2025):
```
AttributeError: type object 'UploadedFileDB' has no attribute 'session_id'
```

**Pattern**: Database migrations ran successfully, but models.py not updated to reflect new schema.

---

## Required Changes

### Phase 1: Verify Database Schema
```bash
docker exec -it piper-postgres psql -U piper -d piper_morgan
\d knowledge_nodes  # Check if owner_id exists
\d knowledge_edges  # Check if owner_id exists
\d learning_pattern_feedback  # Check structure
```

### Phase 2: Update Models
For each affected model:
1. Add `owner_id = Column(String, ForeignKey('users.id'), nullable=True)`
2. Keep `session_id` for backward compatibility (nullable)
3. Add comment explaining migration status

### Phase 3: Update Repositories
Search for usage of session_id in:
- `services/knowledge/`
- `services/learning/`
- Any repository querying these tables

Change filtering from `session_id` to `owner_id`.

### Phase 4: Update Tests
- Search tests using KnowledgeGraph
- Add `create_test_user()` calls (pattern from FileRepository fix)
- Update assertions to check owner_id

---

## Acceptance Criteria

- [ ] KnowledgeNodeDB model has owner_id column defined
- [ ] KnowledgeEdgeDB model has owner_id column defined (if applicable)
- [ ] LearningPatternFeedback assessed and updated if needed
- [ ] All repositories query owner_id instead of session_id
- [ ] All tests pass with new schema
- [ ] No AttributeError when filtering by owner_id
- [ ] Database schema matches model definitions

---

## Risk Assessment

**Impact**: LOW - Knowledge graph not critical for alpha testing
**Urgency**: LOW - Can defer until post-alpha
**Complexity**: MEDIUM - Similar to FileRepository fix (systematic migration)

**Decision**: Defer to post-alpha. Michelle's testing doesn't depend on knowledge graph features.

---

## Related Work

**Completed in Issue #378**:
- ✅ FileRepository: 8 methods migrated from session_id → owner_id
- ✅ Test fixtures: create_test_user() helper for FK constraints
- ✅ Migrations: Cleaned broken migrations, merged heads

**Pattern Discovered**: Incomplete migration where database schema updated but Python models not synchronized.

---

## Recommendations

1. **Create GitHub issue** for tracking
2. **Label**: P2-post-alpha, bug, SEC-RBAC
3. **Milestone**: S1 (Sprint 1 post-alpha)
4. **Blocked by**: None (can work independently)
5. **Blocks**: SEC-RBAC Phase 2 (comprehensive RBAC across all resources)

---

## Testing Strategy

When implementing:

1. Use `mcp__serena__find_symbol` to locate all KnowledgeGraph usage
2. Run systematic find/replace: session_id → owner_id (with context awareness)
3. Add test coverage for multi-user scenarios
4. Verify no console errors when creating/querying knowledge nodes
5. Regression test: Ensure existing knowledge graph queries still work

---

**Priority**: P2 (not blocking alpha)
**Effort**: 2-3 hours (based on FileRepository fix timing)
**Recommended Timing**: After first alpha testing cycle (Dec 2025)

---

_Created: November 24, 2025, 2:05 AM_
_Created by: Lead Developer (Claude Code, role: lead-sonnet)_
_Related Issues: #357, #378_
