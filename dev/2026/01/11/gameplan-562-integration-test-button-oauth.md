# Gameplan: Issue #562 - Integration Test Button Uses MCP Instead of OAuth

**Issue**: #562 BUG-INTEGRATION-TEST
**Created**: 2026-01-11
**Status**: Ready for Implementation
**Estimated Effort**: Small (~30 min)
**Template Version**: 9.3

---

## Overview

Fix the Integration Health Dashboard "Test" button to use stored OAuth tokens instead of MCP/spatial integration paths.

**Root Cause**: `_test_slack()`, `_test_notion()`, `_test_github()` use integration routers which prefer MCP over user-specific OAuth tokens. Calendar test is correct and serves as the pattern.

---

## Phase -1: Infrastructure Verification (5 min)

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Test endpoint: `POST /api/v1/integrations/test/{integration_name}`
- [x] Test functions: `web/api/routes/integrations.py` lines 406-514
- [x] Working pattern: `_test_calendar()` uses KeychainService correctly
- [x] Broken functions: `_test_slack()`, `_test_notion()`, `_test_github()`

**My understanding of the task**:
- Rewrite `_test_slack()` to use KeychainService + direct Slack API call
- Rewrite `_test_notion()` to use KeychainService/NotionConfigService + direct Notion API call
- Rewrite `_test_github()` to use KeychainService + direct GitHub API call
- Follow `_test_calendar()` pattern for all

### Part A.2: Worktree Assessment

**Assessment**: **SKIP WORKTREE** - Single agent, sequential work, small scope.

### Part B: PM Verification Required

**PM, please confirm**:
- [ ] Scope is correct (fix 3 test functions)
- [ ] Calendar pattern is the right approach
- [ ] Proceed with implementation

---

## Phase 0: Investigation (Already Complete)

Investigation completed during issue audit. Key findings:

### Code Path Traced
```
User clicks Test → testConnection(name) → POST /api/v1/integrations/test/{name}
  → _test_integration(name) → _test_slack() / _test_notion() / _test_github()
  → IntegrationRouter() → _get_preferred_integration() → MCP/spatial client
```

### Working Pattern (Calendar)
```python
async def _test_calendar() -> Dict[str, Any]:
    keychain = KeychainService()
    refresh_token = keychain.get_api_key("google_calendar")
    if not refresh_token:
        return {"success": False, "error": "Calendar not connected"}
    handler = GoogleCalendarOAuthHandler()
    tokens = await handler.refresh_access_token(refresh_token)
    return {"success": True} if tokens else {"success": False, "error": "Token invalid"}
```

### Broken Pattern (Slack/Notion/GitHub)
```python
async def _test_slack() -> Dict[str, Any]:
    router = SlackIntegrationRouter()  # Uses MCP, not user's OAuth
    result = await router.test_auth()
    return {"success": result.get("ok")}
```

---

## Phase 0.5: Frontend-Backend Contract

**No changes needed** - The API contract stays the same:
- `POST /api/v1/integrations/test/{integration_name}`
- Response: `{"success": bool, "message": str, "error_type": str?}`

---

## Phase 1: Fix _test_slack() (10 min)

**File**: `web/api/routes/integrations.py`

**Current** (lines 440-458):
```python
async def _test_slack() -> Dict[str, Any]:
    """Test Slack API connection"""
    try:
        from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
        router = SlackIntegrationRouter()
        result = await router.test_auth()
        # ... uses MCP path
```

**New** (follow Calendar pattern):
```python
async def _test_slack() -> Dict[str, Any]:
    """Test Slack API connection using stored OAuth token (Issue #562)"""
    try:
        import aiohttp
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        token = keychain.get_api_key("slack")

        if not token:
            return {
                "success": False,
                "error": "Slack not connected. Click Connect to authorize.",
                "error_type": "not_configured",
            }

        # Test with auth.test endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://slack.com/api/auth.test",
                headers={"Authorization": f"Bearer {token}"},
            ) as response:
                data = await response.json()

                if data.get("ok"):
                    return {"success": True}
                else:
                    return {
                        "success": False,
                        "error": data.get("error", "Token invalid"),
                        "error_type": "token_invalid",
                    }

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}
```

---

## Phase 2: Fix _test_notion() (10 min)

**Current** (lines 424-437):
```python
async def _test_notion() -> Dict[str, Any]:
    """Test Notion API connection"""
    try:
        from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
        router = NotionIntegrationRouter()
        # ... uses MCP path
```

**New**:
```python
async def _test_notion() -> Dict[str, Any]:
    """Test Notion API connection using stored API key (Issue #562)"""
    try:
        import aiohttp
        from services.integrations.notion.config_service import NotionConfigService

        config_service = NotionConfigService()
        config = config_service.get_config()
        api_key = config.api_key

        if not api_key:
            return {
                "success": False,
                "error": "Notion not connected. Please add your API key.",
                "error_type": "not_configured",
            }

        # Test with users/me endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.notion.com/v1/users/me",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28",
                },
            ) as response:
                if response.status == 200:
                    return {"success": True}
                else:
                    return {
                        "success": False,
                        "error": "API key invalid or expired",
                        "error_type": "api_key_invalid",
                    }

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}
```

---

## Phase 3: Fix _test_github() (10 min)

**Current** (lines 461-479):
```python
async def _test_github() -> Dict[str, Any]:
    """Test GitHub API connection"""
    try:
        from services.integrations.github.github_integration_router import GitHubIntegrationRouter
        router = GitHubIntegrationRouter()
        # ... uses MCP path
```

**New**:
```python
async def _test_github() -> Dict[str, Any]:
    """Test GitHub API connection using stored PAT (Issue #562)"""
    try:
        import aiohttp
        from services.infrastructure.keychain_service import KeychainService

        keychain = KeychainService()
        token = keychain.get_api_key("github")

        if not token:
            return {
                "success": False,
                "error": "GitHub not connected. Please add your token.",
                "error_type": "not_configured",
            }

        # Test with user endpoint
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
            ) as response:
                if response.status == 200:
                    return {"success": True}
                else:
                    return {
                        "success": False,
                        "error": "Token invalid or expired",
                        "error_type": "token_invalid",
                    }

    except Exception as e:
        return {"success": False, "error": str(e), "error_type": "connection_failed"}
```

---

## Phase 4: Testing (10 min)

### Manual Testing (Required)
1. [ ] Start server: `python main.py`
2. [ ] Go to `/settings/integrations`
3. [ ] Test each connected integration:
   - [ ] Slack: Click Test → Verify uses stored OAuth token
   - [ ] Notion: Click Test → Verify uses stored API key
   - [ ] GitHub: Click Test → Verify uses stored PAT
   - [ ] Calendar: Click Test → Verify still works (no changes)
4. [ ] Test disconnected state:
   - [ ] Disconnect Slack → Test shows "not connected" message
   - [ ] Disconnect Notion → Test shows "not connected" message
   - [ ] Disconnect GitHub → Test shows "not connected" message

### Unit Tests (Optional - time permitting)
If time permits, add tests to `tests/unit/web/api/routes/test_integrations.py`

---

## Phase Z: Completion (5 min)

### Checklist
- [ ] All 3 test functions rewritten
- [ ] Manual testing passes
- [ ] Pre-commit hooks pass
- [ ] Commit with proper message
- [ ] Update GitHub issue with evidence
- [ ] Request PM closure

### Commit Message Template
```
fix(#562): Use stored OAuth tokens for integration Test button

The Test button on the Integration Health Dashboard was using MCP/spatial
integration paths instead of user-specific OAuth tokens stored in keychain.

Changes:
- Rewrite _test_slack() to use KeychainService + Slack API auth.test
- Rewrite _test_notion() to use NotionConfigService + Notion API users/me
- Rewrite _test_github() to use KeychainService + GitHub API user endpoint
- All now follow the _test_calendar() pattern

Issue: #562

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## STOP Conditions

**STOP immediately and escalate if**:

1. **KeychainService returns None for connected integration**
   - Expected: Token should exist after OAuth connect flow
   - If None: May indicate OAuth storage bug (different issue)

2. **API endpoints return unexpected errors**
   - 401/403: Token validation working correctly (expected for bad tokens)
   - 5xx: Provider issue, not our bug
   - Other: May indicate API change, needs investigation

3. **Calendar test stops working**
   - We're not touching `_test_calendar()` - if it breaks, stop

4. **Integration router is still being called**
   - After fix, grep for `IntegrationRouter` in test functions should return 0 hits
   - If still present: Fix incomplete

5. **Tests require database access for user context**
   - Current test functions don't use `current_user`
   - If user context needed: Scope creep, escalate

6. **MCP/spatial mode is required for some integrations**
   - If `USE_SPATIAL_*` flags affect test behavior: Document and escalate
   - This fix assumes OAuth tokens are the source of truth for "connection status"

---

## Out of Scope (Do Not Chase)

1. **Refactoring integration routers** - Not fixing the router pattern, just bypassing it for tests
2. **Adding user context to tests** - Tests remain user-agnostic (single-user alpha)
3. **Changing the test endpoint contract** - Same request/response format
4. **Adding new test endpoints** - Only fixing existing `_test_*` functions
5. **Fixing MCP/spatial integration** - That's a separate concern
6. **Adding retry logic or timeout handling** - Keep it simple

---

## Risk Assessment

**Low Risk**:
- Following established pattern (`_test_calendar`)
- No contract changes
- No database changes
- Isolated to 3 functions

**Key Differences from Current**:
- Direct API calls instead of router delegation
- Uses KeychainService/ConfigService instead of router internals
- More explicit error messages

---

## Files to Modify Summary

| File | Changes |
|------|---------|
| `web/api/routes/integrations.py` | Rewrite `_test_slack()`, `_test_notion()`, `_test_github()` |

**Lines affected**: ~90 lines (3 functions × ~30 lines each)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-11 | Initial gameplan |

---

_Gameplan created: 2026-01-11_
_Template version: 9.3_
