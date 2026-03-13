# Gameplan: #759 - Complete #734 Multi-Tenancy Migration

**Issue**: #759
**Date**: 2026-02-01
**Type**: Tech-Debt (Incomplete Migration)
**Blocks**: #758 (test collection failure)

---

## Phase -1: Infrastructure Verification

### Part A: Current Understanding

**Task**: Complete the #734 multi-tenancy migration by updating 12 call sites across 8 files to pass `user_id` to config service methods.

**Infrastructure**:
- Config services already require `user_id` (done in #734)
- Plugin interface `PluginInterface.is_configured()` lacks `user_id` parameter
- All 4 integration plugins call config services without `user_id`
- Clients, routers, and adapters also missing `user_id`

**Worktree Assessment**: SKIP WORKTREE - Changes touch multiple files but are mechanical (adding parameter threading). Single worktree is appropriate.

### Part B: PM Verification

- [ ] PM confirms understanding is correct
- [ ] PM confirms scope includes all 12 call sites

### Part C: Decision

- [ ] PROCEED with gameplan
- [ ] REVISE based on PM feedback

---

## Phase 0: Investigation

### 0.1: Call Site Analysis

Each call site needs a strategy for obtaining `user_id`:

| Category | Source of user_id | Strategy |
|----------|-------------------|----------|
| Plugins | Caller passes it | Add `user_id: Optional[str] = None` to interface |
| Slack Client | Constructor or method param | Add to constructor and/or methods |
| Slack Webhook Router | Request context | Extract from Slack user → internal user mapping |
| GitHub Integration Router | Request context | Extract from auth context |
| Notion Adapter | Constructor or method param | Add to constructor |
| Plugin Interface Base | Caller passes it | Add optional parameter |

### 0.2: User Context Sources

Where does `user_id` come from in each context?

1. **Web requests**: `current_user` from `get_current_user()` dependency
2. **Slack webhooks**: Slack user ID → need mapping to internal user
3. **CLI/standalone**: May not have user context (system operations)

### 0.3: Backward Compatibility Requirements

- `is_configured(user_id: Optional[str] = None)` - Optional for backward compat
- If `user_id` is None, behavior TBD:
  - Option A: Return False (not configured for unknown user)
  - Option B: Check system-wide config only
  - Option C: Raise error (require user_id)

**Recommendation**: Option A - Return False. This is safest and matches semantic of "is this configured for this user?"

---

## Phase 0.5: Frontend-Backend Contract

**N/A** - Backend-only change. No API contract changes.

---

## Phase 0.6: Data Flow Verification

### Call Chain Analysis

```
[Caller with user context]
    ↓
[Plugin.is_configured(user_id)]
    ↓
[ConfigService.is_configured(user_id)]
    ↓
[Keychain/DB lookup scoped to user_id]
```

### Data Sources

- User ID comes from JWT claims (`current_user.user_id`)
- Slack webhook: Slack user ID needs mapping (separate concern)

### Verification Commands

```bash
# Verify user context sources in integration code
grep -rn "get_current_user\|current_user" services/integrations/

# Verify method signatures require user_id
python -c "from services.integrations.calendar.config_service import CalendarConfigService; import inspect; print(inspect.signature(CalendarConfigService.is_configured))"

# Check if plugin interface has user_id
grep -n "user_id" services/plugins/plugin_interface.py
```

---

## Phase 0.7: Conversation Design

**N/A** - Not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

**N/A** - Bug fix / migration completion. No new state or features.

---

## Phase 1: Update Plugin Interface

### 1.1: Modify `PluginInterface`

File: `services/plugins/plugin_interface.py`

```python
# Before:
def is_configured(self) -> bool:
    ...

# After:
def is_configured(self, user_id: Optional[str] = None) -> bool:
    ...
```

### 1.2: Update Base Class Implementation

If there's a default implementation in `PluginInterface`, update it to pass `user_id` to config service.

---

## Phase 2: Update Plugin Implementations

### 2.1: CalendarPlugin

File: `services/integrations/calendar/calendar_plugin.py`

```python
# Before (line 65):
def is_configured(self) -> bool:
    return self.config_service.is_configured()

# After:
def is_configured(self, user_id: Optional[str] = None) -> bool:
    if user_id is None:
        return False  # Can't check config without user context
    return self.config_service.is_configured(user_id)
```

### 2.2: NotionPlugin

File: `services/integrations/notion/notion_plugin.py` (line 67)
Same pattern as CalendarPlugin.

### 2.3: GitHubPlugin

File: `services/integrations/github/github_plugin.py` (line 65)
Same pattern as CalendarPlugin.

### 2.4: SlackPlugin

File: `services/integrations/slack/slack_plugin.py` (line 68)
Same pattern as CalendarPlugin.

---

## Phase 3: Update Slack Client

File: `services/integrations/slack/slack_client.py`

### 3.1: Analyze Current Usage

Need to understand how SlackClient is instantiated and whether it has user context.

### 3.2: Add user_id to Constructor or Methods

```python
# Option A: Constructor
def __init__(self, config_service: SlackConfigService, user_id: str):
    self.user_id = user_id
    self.config = config_service.get_config(user_id)

# Option B: Method parameter
def send_message(self, channel: str, text: str, user_id: str):
    config = self.config_service.get_config(user_id)
    ...
```

### 3.3: Update Call Sites (lines 77, 89, 116)

Replace `self.config_service.get_config()` with `self.config_service.get_config(self.user_id)` or method parameter.

---

## Phase 4: Update Routers

### 4.1: Slack Webhook Router

File: `services/integrations/slack/webhook_router.py`
Lines: 230, 515, 687

**Challenge**: Slack webhooks contain `team_id` but no internal `user_id`. Need to determine which user's config to load.

**Strategy (Alpha-appropriate)**:
1. Add `_get_connector_user_id()` method that:
   - First checks `SLACK_CONNECTOR_USER_ID` environment variable
   - Falls back to None (graceful degradation)
2. Update `get_config()` calls to use connector user_id
3. If no connector user configured, log warning and use empty/default config

```python
def _get_connector_user_id(self) -> Optional[str]:
    """Get the user_id that owns the Slack integration.

    For alpha: Uses SLACK_CONNECTOR_USER_ID env var.
    Future: Will query slack_workspaces table by team_id.
    """
    return os.getenv("SLACK_CONNECTOR_USER_ID")

# Then in webhook handlers:
user_id = self._get_connector_user_id()
if user_id:
    config = self.config_service.get_config(user_id)
else:
    logger.warning("No SLACK_CONNECTOR_USER_ID configured, webhook may fail")
    # Graceful degradation - use empty config or skip user-scoped features
```

**Future work**: File issue for proper `slack_workspaces` table with `team_id` → `user_id` mapping.

### 4.2: GitHub Integration Router

File: `services/integrations/github/github_integration_router.py`
Line: 144

Extract user_id from request auth context.

---

## Phase 5: Update Adapter

### 5.1: Notion Adapter

File: `services/integrations/mcp/notion_adapter.py`
Line: 56

Add `user_id` to constructor or initialization method.

---

## Phase 6: Update Tests

### 6.1: Fix Test Imports

The test collection failure (#758) should be fixed once plugins accept optional `user_id`.

### 6.2: Update Existing Tests

Tests that call `is_configured()` need to pass `user_id` or mock appropriately.

---

## Phase 6.5: Wiring Integration Tests (Template v9.3 Requirement)

Per gameplan-template.md Issue #490 learning, tests must verify real wiring without mocking internals.

### Test 1: Import Chain Verification

```python
def test_plugin_import_chain():
    """Verify imports work without mocking."""
    from services.plugins.plugin_interface import PluginInterface
    from services.integrations.calendar.calendar_plugin import CalendarPlugin
    import inspect

    # Verify method signature accepts user_id
    sig = inspect.signature(CalendarPlugin.is_configured)
    assert 'user_id' in sig.parameters
```

### Test 2: Parameter Propagation

```python
def test_user_id_propagation():
    """Verify user_id flows to config service without TypeError."""
    from services.integrations.calendar.calendar_plugin import CalendarPlugin
    from services.integrations.calendar.config_service import CalendarConfigService

    plugin = CalendarPlugin(config_service=CalendarConfigService())
    # Should not raise TypeError for missing user_id
    result = plugin.is_configured(user_id="test-user")
    assert isinstance(result, bool)
```

### Test 3: All Plugins Accept user_id

```python
@pytest.mark.parametrize("plugin_class,config_class", [
    ("CalendarPlugin", "CalendarConfigService"),
    ("NotionPlugin", "NotionConfigService"),
    ("GitHubPlugin", "GitHubConfigService"),
    ("SlackPlugin", "SlackConfigService"),
])
def test_all_plugins_accept_user_id(plugin_class, config_class):
    """Verify all plugin is_configured methods accept user_id."""
    import inspect
    # Dynamic import and signature check
    ...
```

---

## Phase Z: Final Verification

### Acceptance Criteria

- [ ] All 12 call sites pass `user_id` to config service methods
- [ ] `PluginInterface.is_configured()` accepts optional `user_id`
- [ ] All 4 plugin implementations updated
- [ ] Slack client updated (3 call sites)
- [ ] Webhook routers updated (4 call sites)
- [ ] Notion adapter updated (1 call site)
- [ ] Plugin interface base class updated (1 call site)
- [ ] `pytest --collect-only` succeeds (no import errors)
- [ ] `pytest tests/unit/services/integrations/` passes
- [ ] `pytest tests/unit/services/plugins/` passes
- [ ] No hardcoded user_id values introduced

### STOP Conditions

1. If Slack user → internal user mapping doesn't exist → STOP, escalate
2. If plugin callers don't have user context → STOP, analyze call chain
3. If tests require complex mocking changes → Document scope, ask PM

### Test Scope Requirements

- [ ] Unit tests: `tests/unit/services/integrations/*/test_*.py` - verify plugin is_configured
- [ ] Unit tests: `tests/unit/services/plugins/test_*.py` - verify interface contract
- [ ] **Wiring tests**: Real import chain verification (Phase 6.5 above)
- [ ] Collection test: `pytest --collect-only` succeeds without errors

### Evidence Required

- [ ] Grep: `grep -r "\.is_configured()" services/integrations/ | grep -v "user_id"` returns empty
- [ ] Grep: `grep -r "\.get_config()" services/integrations/ | grep -v "user_id"` returns empty (excluding comments/docs)
- [ ] Collection: `pytest --collect-only 2>&1 | head -50` shows no errors
- [ ] Tests: `pytest tests/unit/services/integrations/ -xvs` full output showing pass
- [ ] Tests: `pytest tests/unit/services/plugins/ -xvs` full output showing pass

---

## Files to Modify

| File | Changes |
|------|---------|
| `services/plugins/plugin_interface.py` | Add `user_id` param to `is_configured()` |
| `services/integrations/calendar/calendar_plugin.py` | Update `is_configured()` |
| `services/integrations/notion/notion_plugin.py` | Update `is_configured()` |
| `services/integrations/github/github_plugin.py` | Update `is_configured()` |
| `services/integrations/slack/slack_plugin.py` | Update `is_configured()` |
| `services/integrations/slack/slack_client.py` | Add `user_id` to config calls |
| `services/integrations/slack/webhook_router.py` | Add `user_id` to config calls |
| `services/integrations/github/github_integration_router.py` | Add `user_id` to token call |
| `services/integrations/mcp/notion_adapter.py` | Add `user_id` to config call |

---

## Multi-Agent Deployment

**Single agent selected** - Rationale:
- Mechanical changes across multiple files
- Dependencies between changes (interface must change before implementations)
- Sequential execution required (can't parallelize)
- ~1.5 hour estimate fits single session
- No benefit from parallel approaches (all changes similar)

---

## Risk Assessment

| Risk | Mitigation |
|------|------------|
| Breaking existing callers of `is_configured()` | Optional parameter with default |
| Slack webhook user mapping missing | Investigate first, escalate if blocked |
| Test mocking complexity | Document and address incrementally |

---

## Estimated Scope

- Phase 1: 10 min (interface)
- Phase 2: 15 min (plugins)
- Phase 3: 15 min (slack client)
- Phase 4: 20 min (routers - includes investigation)
- Phase 5: 10 min (adapter)
- Phase 6: 15 min (tests)
- Phase Z: 10 min (verification)

**Total**: ~1.5 hours

---

## Open Questions (Resolved)

### 1. Slack Webhook User Mapping - RESEARCHED

**Finding**: No Slack workspace → internal user mapping exists in the database.

**Current state**:
- OAuth flow stores workspace config with `user_id` field (logged, not persisted to DB)
- Tokens stored with user-scoped keys: `f"slack_bot_{user_id}"`
- Config service retrieves with `user_id` parameter
- Webhook router receives `team_id` from Slack but has no way to lookup which user owns it

**ADR-058 section 7 guidance**: "System webhooks - Use 'connector user' stored at integration setup"

**Strategy for Phase 4.1 (Slack Webhook Router)**:

For alpha (single-user effectively), we have two options:

**Option A: Environment Variable Fallback** (Recommended for alpha)
- Add `SLACK_CONNECTOR_USER_ID` env var
- Webhook router uses this when `team_id` lookup not available
- Simple, works for alpha's limited multi-tenancy

**Option B: Workspace-User Table** (Future work)
- Create `slack_workspaces` table with `team_id` → `user_id` mapping
- Populate during OAuth callback
- Query during webhook handling
- Proper multi-tenant solution

**Decision**: Use Option A for now (alpha), file issue for Option B.

**Reasoning for deferral** (PM approved 2026-02-01):
- Alpha testers run individual instances (one user per instance)
- Env var correctly identifies "the user" when there's only one
- Zero cost during alpha phase
- #760 created to track proper solution before shared multi-user deployment
- Clean upgrade path: env var becomes fallback when table exists

### 2. System Operations - RESOLVED

Background tasks without user context should either:
- Use a "system user" for operations not tied to a specific user
- Accept that `is_configured()` returns False without user context (which is correct - can't check user config without user)

### 3. Test Mocking - RESOLVED

Config services in tests should be mocked to accept `user_id` parameter. The parameter is required but tests can pass a test user ID.
