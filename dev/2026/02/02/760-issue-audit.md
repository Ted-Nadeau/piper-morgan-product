# Audit: #760 Issue - slack_workspaces table for team_id → user_id mapping

**Date**: 2026-02-02
**Document**: GitHub Issue #760
**Type**: Technical Debt / Infrastructure Enhancement

---

## Issue Quality Check

| Requirement | Status | Notes |
|-------------|--------|-------|
| Problem Statement | ✅ | Clear explanation of why env var breaks for multi-user |
| Current State | ✅ | Alpha workaround documented |
| When Critical | ✅ | Trigger conditions defined |
| Proposed Solution | ✅ | SQL, model, repository, integration points |
| Acceptance Criteria | ✅ | 6 checkboxes |
| Effort Estimate | ✅ | 2-3 hours |
| Dependencies | ✅ | #759 listed as blocker |
| Priority | ✅ | Low until multi-user |

**Issue Quality**: EXCELLENT - Ready for gameplan creation.

---

## Investigation Results

### 1. OAuth Handler Location ✅

**File**: `services/integrations/slack/oauth_handler.py`
**Method**: `SlackOAuthHandler._store_workspace_tokens()` (lines 502-577)

**Current Implementation**:
- Already accepts `user_id: Optional[str] = None` parameter (Issue #734)
- Stores tokens in keychain with user-scoped keys: `slack_bot_{user_id}`, `slack_user_{user_id}`
- Creates `workspace_config` dict with `user_id` field
- **BUT**: workspace_config is only logged, NOT persisted to database

**Key Code**:
```python
workspace_config = {
    "workspace_id": workspace_id,
    "workspace_name": workspace_data["workspace_name"],
    ...
    "user_id": user_id,  # Issue #734: Track owning user
}
# This would typically go to database or secure storage
logger.info(f"Workspace configuration stored: {workspace_config}")  # Only logged!
```

**Hook Point**: After line 577, add DB persistence call.

### 2. Webhook Router Current Implementation ✅

**File**: `services/integrations/slack/webhook_router.py`
**Method**: `SlackWebhookRouter._get_connector_user_id()` (lines 102-113)

**Current Implementation**:
```python
def _get_connector_user_id(self) -> Optional[str]:
    """Get the user_id that owns the Slack integration.

    For alpha: Uses SLACK_CONNECTOR_USER_ID env var.
    Future (#760): Will query slack_workspaces table by team_id.
    """
    return os.getenv("SLACK_CONNECTOR_USER_ID")
```

**Call Chain**:
1. `_process_event_callback()` extracts `team_id` from event (line 802)
2. All event handlers receive `team_id`: `_process_message_event(event, team_id)`, etc.
3. `_get_connector_user_id()` called but ignores `team_id` (uses env var)

**Required Change**: Update `_get_connector_user_id(self, team_id: str)` to query database.

### 3. Async Context in Webhook Router ✅

**Current State**: Webhook router has NO database access.

**Comparison**: Other routes (auth.py, setup.py, files.py) all use:
```python
from services.database.session_factory import AsyncSessionFactory
async with AsyncSessionFactory.session_scope_fresh() as session:
    # DB operations
```

**Required**: Add `AsyncSessionFactory` import and wrap DB query in context manager.

**Complexity Factor**: Method `_get_connector_user_id()` is currently sync. Need to make async or handle carefully.

### 4. Existing Patterns ✅

**No direct pattern exists** for "lookup entity owner by external ID" in this codebase.

**Closest patterns**:
- `UserService.get_user_by_email()` - in-memory lookup by email
- File repository lookups by `owner_id` - but these go the other direction (user_id → files)

**Recommendation**: Create new `SlackWorkspaceRepository` with `get_user_by_team_id(team_id: str) -> Optional[str]` method.

---

## Refined Effort Analysis

### Component Breakdown (Updated)

| Component | Estimated Effort | Complexity | Notes |
|-----------|------------------|------------|-------|
| 1. Alembic Migration | 15 min | Low | `slack_workspaces` table with team_id, user_id, installed_at |
| 2. SQLAlchemy Model | 15 min | Low | `SlackWorkspace` model in models.py |
| 3. Repository Class | 25 min | Low | New `SlackWorkspaceRepository` with `get_user_by_team_id()` and `save_workspace()` |
| 4. OAuth Handler Update | 20 min | Low | Add repository call after workspace_config is built |
| 5. Webhook Router Update | 35 min | Medium | Make `_get_connector_user_id` async, add DB query, update all callers |
| 6. Unit Tests | 30 min | Low | Repository tests, mocked DB |
| 7. Integration Tests | 30 min | Medium | End-to-end OAuth flow → webhook flow |

**Total Estimate**: 2.5-3 hours (aligned with issue estimate)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Async conversion breaks callers | Low | Medium | Audit all `_get_connector_user_id()` callers |
| DB connection pool exhaustion in webhook | Low | High | Use `session_scope_fresh()` with short scope |
| Migration on existing production DB | Low | Low | Table is additive, no existing data |
| OAuth flow doesn't pass user_id | Medium | Medium | OAuth callback already has user context |

---

## Dependency Check

- **#759 (SEC-RBAC foundation)**: ✅ CLOSED - Already merged
- **Database infrastructure**: ✅ PostgreSQL running, Alembic configured
- **User model**: ✅ Exists with UUID primary key

**No blocking dependencies.**

---

## Recommendation

**Issue is well-specified and ready for implementation.**

**When to do it**:
- **If staying single-user alpha**: Can defer indefinitely (env var works)
- **If adding second alpha tester**: Must do BEFORE they connect Slack
- **If going to beta**: Required for multi-tenancy

**Effort is reasonable**: 2.5-3 hours of focused work, no architectural risk.
