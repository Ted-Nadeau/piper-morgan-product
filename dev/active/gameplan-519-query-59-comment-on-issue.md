# Gameplan: Issue #519 - Query #59: Comment on Issue

**GitHub Issue**: #519 (partial - completing remaining query)
**Date**: December 27, 2025
**Lead Developer**: Opus 4.5
**Status**: READY FOR APPROVAL

---

## Query in Scope

| Query # | User Query            | What's Needed                           |
| ------- | --------------------- | --------------------------------------- |
| #59     | "Comment on issue #X" | Add `add_comment()` to router + handler |

---

## Phase 0: Infrastructure Verification

### Current State (Verified)

| Component               | Status         | Location                                                    |
| ----------------------- | -------------- | ----------------------------------------------------------- |
| GitHubIntegrationRouter | ✅ Exists      | `services/integrations/github/github_integration_router.py` |
| get_issue()             | ✅ Exists      | Lines 183-201                                               |
| update_issue()          | ✅ Exists      | Lines 219-232                                               |
| create_issue()          | ✅ Exists      | Lines 209-217                                               |
| add_comment()           | ❌ **Missing** | Needs to be added                                           |

### Architecture Understanding

```
Router Pattern:
GitHubIntegrationRouter.add_comment(repo, issue_number, body)
    → _get_integration("add_comment")
        → GitHubMCPSpatialAdapter.add_comment() OR
        → GitHubSpatialIntelligence.add_comment()
```

**Key Finding**: The `_call_github_api()` in MCP adapter only does GET requests. We need to add POST capability for comments.

### What Needs to Be Added

1. **Router Layer** (`github_integration_router.py`):

   - Add `add_comment(repo_name, issue_number, body)` method

2. **Adapter Layer** (`github_adapter.py`):

   - Add `_post_github_api()` method for POST requests
   - Add `add_comment()` method using POST

3. **Intent Handler** (`intent_service.py`):

   - Add `_handle_comment_issue_query()` handler
   - Parse issue number and comment body from query

4. **Pre-Classifier** (`pre_classifier.py`):
   - Add patterns for "comment on issue #X"

---

## Phase 1: Router + Adapter Extension

### 1.1 Add POST capability to MCP Adapter

**File**: `services/mcp/consumer/11github_adapter.py`

```python
async def _post_github_api(
    self, endpoint: str, data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Make GitHub API POST call"""
    try:
        if not self._session:
            logger.warning("GitHub API session not configured")
            return None

        url = f"{self._github_api_base}/{endpoint}"
        async with self._session.post(url, json=data) as response:
            if response.status in (200, 201):
                return await response.json()
            elif response.status == 401:
                logger.error("GitHub API authentication failed")
                return None
            elif response.status == 403:
                logger.error("GitHub API rate limit exceeded")
                return None
            else:
                logger.error(f"GitHub API error: {response.status}")
                return None

    except Exception as e:
        logger.error(f"Error calling GitHub API: {e}")
        return None

async def add_comment(
    self, repo_name: str, issue_number: int, body: str
) -> Optional[Dict[str, Any]]:
    """Add comment to GitHub issue"""
    endpoint = f"repos/{repo_name}/issues/{issue_number}/comments"
    return await self._post_github_api(endpoint, {"body": body})
```

### 1.2 Add Router Method

**File**: `services/integrations/github/github_integration_router.py`

```python
async def add_comment(
    self, repo_name: str, issue_number: int, body: str
) -> Dict[str, Any]:
    """Add comment to GitHub issue."""
    return await self._get_integration("add_comment").add_comment(
        repo_name, issue_number, body
    )
```

---

## Phase 2: Intent Handler

### 2.1 Add Handler

**File**: `services/intent/intent_service.py`

Follow pattern from `_handle_close_issue_query()`:

- Parse issue number from query
- Extract comment body (everything after "saying" or "with message")
- Call `GitHubIntegrationRouter.add_comment()`
- Return confirmation

### 2.2 Add Pre-Classifier Patterns

**File**: `services/intent_service/pre_classifier.py`

Add to `GITHUB_QUERY_PATTERNS`:

```python
r"\bcomment on issue\s*#?\d+\b",
r"\badd comment to issue\s*#?\d+\b",
r"\breply to issue\s*#?\d+\b",
r"\bcomment\s+#?\d+\b",
```

---

## Phase 3: Tests (Following Issue #521 Discipline)

### 3.1 Router Tests

**File**: `tests/unit/services/integrations/github/test_github_integration_router.py`

- Test `add_comment()` calls adapter correctly
- Test error handling

### 3.2 Handler Tests

**File**: `tests/unit/services/intent_service/test_github_query_handlers.py`

Add:

1. `TestCommentIssueRouting` (2 tests) - routing integration
2. `TestCommentIssueResults` (3 tests) - handler logic
3. `TestPreClassifierRoutingIntegration` additions (2 tests)

---

## Acceptance Criteria

- [ ] `add_comment()` method added to GitHubIntegrationRouter
- [ ] `_post_github_api()` and `add_comment()` added to MCP adapter
- [ ] `_handle_comment_issue_query()` handler implemented
- [ ] Pre-classifier patterns added for comment queries
- [ ] 7+ tests added (router + handler + routing)
- [ ] All tests passing
- [ ] No regressions

---

## STOP Conditions

- MCP adapter doesn't have session configured → graceful degradation
- POST requests require different auth → escalate
- Rate limiting concerns → add to documentation

---

## Manual Testing Note

⚠️ Same blocker as other GitHub queries - needs GitHub project setup UI

---

## Estimated Effort

| Component           | Lines | Complexity |
| ------------------- | ----- | ---------- |
| Adapter POST        | ~25   | Low        |
| Adapter add_comment | ~10   | Low        |
| Router method       | ~5    | Low        |
| Intent handler      | ~100  | Medium     |
| Pre-classifier      | ~5    | Low        |
| Tests               | ~150  | Medium     |
| **Total**           | ~295  | Medium     |

---

**Status**: READY FOR APPROVAL
