## Problem

Test `test_security_fail_closed_on_error` in `tests/unit/services/auth/test_token_blacklist.py` generates a RuntimeWarning about an unawaited coroutine during execution.

## Warning Output

```
tests/unit/services/auth/test_token_blacklist.py::TestTokenBlacklistOperations::test_security_fail_closed_on_error
  /Users/xian/Development/piper-morgan/services/auth/token_blacklist.py:158: RuntimeWarning: coroutine 'AsyncMockMixin._execute_mock_call' was never awaited
    return await self._check_database(token_id)
```

## Root Cause

The test mocks `_check_database` method but doesn't configure it as an AsyncMock. When production code calls `await self._check_database(token_id)`, the mock returns a coroutine that isn't properly awaited.

**Test Location**: `tests/unit/services/auth/test_token_blacklist.py:168-178`

```python
async def test_security_fail_closed_on_error(self, mock_redis_factory, mock_db_session_factory):
    """Should fail closed (assume blacklisted) on errors"""
    # Make both Redis and DB fail
    mock_redis_factory.create_client = AsyncMock(side_effect=Exception("Connection error"))

    bl = TokenBlacklist(mock_redis_factory, mock_db_session_factory)
    bl._redis_available = False  # Simulate no Redis

    # Should return True (fail closed) on error
    result = await bl.is_blacklisted("any-token")
    assert result is True
```

## Impact

**Severity**: P3 - Test hygiene issue
- Test still passes functionally
- Warning indicates improper mock setup
- Not blocking any features
- Discovered during SLACK-SPATIAL Phase 1.2 investigation

## Proposed Fix

Configure `_check_database` as AsyncMock when testing error handling:

```python
async def test_security_fail_closed_on_error(self, mock_redis_factory, mock_db_session_factory):
    """Should fail closed (assume blacklisted) on errors"""
    # Make both Redis and DB fail
    mock_redis_factory.create_client = AsyncMock(side_effect=Exception("Connection error"))

    bl = TokenBlacklist(mock_redis_factory, mock_db_session_factory)
    bl._redis_available = False  # Simulate no Redis

    # Mock _check_database to raise exception (AsyncMock for proper await)
    bl._check_database = AsyncMock(side_effect=Exception("Database error"))

    # Should return True (fail closed) on error
    result = await bl.is_blacklisted("any-token")
    assert result is True
```

Alternative: Suppress the warning if the current behavior is intentional.

## Related Work

- **Investigation**: piper-morgan-otf (SLACK-SPATIAL Phase 1.2)
- **Report**: `dev/2025/11/20/token-blacklist-investigation-results.md`
- **Original Issue**: #281 (TokenBlacklist database session conflicts)

## Acceptance Criteria

- [ ] Test runs without RuntimeWarning
- [ ] Test still validates fail-closed behavior on errors
- [ ] All 17 auth tests continue to pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)
