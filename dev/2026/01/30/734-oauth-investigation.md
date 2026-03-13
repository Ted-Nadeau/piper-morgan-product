# OAuth State Infrastructure Investigation Report

**Issue**: #734 - Multi-Tenancy Isolation
**Phase**: Phase 2 (OAuth Investigation, per gameplan Phase -1)
**Date**: 2026-01-30
**Investigator**: Lead Developer (Opus)

---

## Executive Summary

OAuth state infrastructure exists but **lacks user identity**. Current state contains only CSRF nonce. Callbacks cannot identify which user initiated the OAuth flow, resulting in tokens being stored globally.

**Key Finding**: OAuth initiation routes are **unauthenticated** - they don't even have access to `current_user`. This is the root cause.

---

## Current State Analysis

### Google Calendar OAuth

**State Generation** (`services/integrations/calendar/oauth_handler.py:84-112`):

```python
def generate_authorization_url(self) -> Tuple[str, str]:
    state = secrets.token_urlsafe(32)  # Only CSRF nonce
    _PENDING_STATES[state] = time.time()  # Store timestamp only
    # ...
    return auth_url, state
```

**State Storage**: Module-level dict `_PENDING_STATES: Dict[str, float]`
- Key: state token (random string)
- Value: creation timestamp (float)
- **No user information stored**

**State Verification** (`services/integrations/calendar/oauth_handler.py:114-129`):
```python
def _verify_state(self, state: str) -> bool:
    if state not in _PENDING_STATES:
        return False
    # Check expiration (5 minute default)
    if time.time() - created_at > self.STATE_EXPIRATION:
        return False
    return True
```
- Returns `bool` only
- **Cannot return user_id** (doesn't have it)

**Callback Handler** (`services/integrations/calendar/oauth_handler.py:131-163`):
```python
async def handle_oauth_callback(self, code: str, state: str) -> Dict:
    if not self._verify_state(state):
        raise ValueError("Invalid or expired state token")
    tokens = await self._exchange_code_for_tokens(code)
    user_info = await self._get_user_info(tokens.access_token)
    return {"tokens": tokens, "user": user_info}
```
- Gets `user_info` from Google (the external user's Google profile)
- **Does NOT know which internal Piper user initiated the flow**

### Slack OAuth

**State Generation** (`services/integrations/slack/oauth_handler.py:51-124`):

```python
def generate_authorization_url(self, scopes=None, user_scopes=None, redirect_uri=None):
    state = secrets.token_urlsafe(32)  # Only CSRF nonce
    self._oauth_states[state] = {
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=15),
        "scopes": scopes,
        "user_scopes": user_scopes,
        "redirect_uri": redirect_uri,
    }
    # ...
```

**State Storage**: Instance-level dict `self._oauth_states: Dict[str, Dict[str, Any]]`
- Key: state token (random string)
- Value: dict with `created_at`, `expires_at`, `scopes`, `user_scopes`, `redirect_uri`
- **No user_id stored**

**State Verification** (`services/integrations/slack/oauth_handler.py:181-196`):
```python
def _verify_oauth_state(self, state: str) -> bool:
    if state not in self._oauth_states:
        return False
    # Check expiration
    return True
```
- Returns `bool` only
- **Cannot return user_id**

**Token Storage** (`services/integrations/slack/oauth_handler.py:362-417`):
```python
async def _store_workspace_tokens(self, workspace_data, token_data):
    keychain = KeychainService()
    keychain.store_api_key("slack_bot", bot_token)  # No username parameter!
    keychain.store_api_key("slack_user", user_token)  # No username parameter!
```
- Stores globally (no `username` parameter = system-wide key)

---

## Route Analysis

### Setup Routes (Unauthenticated)

**File**: `web/api/routes/setup.py`

```python
@router.get("/slack/oauth/start")
async def start_slack_oauth():  # NO current_user dependency!
    # ...
    auth_url, state = handler.generate_authorization_url()
```

```python
@router.get("/calendar/oauth/start")
async def start_calendar_oauth():  # NO current_user dependency!
    # ...
    auth_url, state = handler.generate_authorization_url()
```

**Problem**: These routes don't require authentication, so they have no user context to pass.

### Settings Routes (Unauthenticated)

**File**: `web/api/routes/settings_integrations.py`

```python
@router.get("/slack/connect")
async def connect_slack():  # NO current_user dependency!
    # ...
    auth_url, state = oauth_handler.generate_authorization_url()
```

```python
@router.get("/calendar/connect")
async def connect_calendar():  # NO current_user dependency!
    # ...
    auth_url, state = handler.generate_authorization_url()
```

**Problem**: Same issue - no authentication, no user context.

---

## Required Changes

### 1. Add Authentication to OAuth Start Routes

**Before**:
```python
@router.get("/calendar/connect")
async def connect_calendar():
```

**After**:
```python
@router.get("/calendar/connect")
async def connect_calendar(current_user: JWTClaims = Depends(get_current_user)):
```

### 2. Update State Generation to Accept user_id

**Before** (Calendar):
```python
def generate_authorization_url(self) -> Tuple[str, str]:
    state = secrets.token_urlsafe(32)
```

**After**:
```python
def generate_authorization_url(self, user_id: str) -> Tuple[str, str]:
    state_data = {
        "user_id": user_id,
        "nonce": secrets.token_urlsafe(16),
        "return_url": "/settings/integrations"
    }
    state = base64.urlsafe_b64encode(json.dumps(state_data).encode()).decode().rstrip("=")
```

### 3. Update State Verification to Return user_id

**Before**:
```python
def _verify_state(self, state: str) -> bool:
```

**After**:
```python
def verify_state(self, state: str) -> str:
    """Verify state and return user_id, or raise ValueError."""
    decoded = json.loads(base64.urlsafe_b64decode(state + "=="))
    if "user_id" not in decoded:
        raise ValueError("State missing user_id")
    # Verify nonce from _PENDING_STATES
    if decoded["nonce"] not in _PENDING_NONCES:
        raise ValueError("Invalid nonce")
    return decoded["user_id"]
```

### 4. Update Token Storage to Use user_id

**Before**:
```python
keychain.store_api_key("slack_bot", bot_token)
```

**After**:
```python
user_api_key_service.store_user_key(
    user_id=user_id,
    provider="slack_bot",
    key=bot_token
)
```

---

## State Storage Comparison

| Aspect | Calendar | Slack |
|--------|----------|-------|
| Storage location | Module-level dict | Instance-level dict |
| Storage type | `Dict[str, float]` | `Dict[str, Dict]` |
| Expiration | 5 minutes | 15 minutes |
| Contains user_id | ❌ No | ❌ No |
| Contains nonce | ✅ (key itself) | ✅ (key itself) |
| Contains metadata | ❌ timestamp only | ✅ scopes, redirect_uri |

---

## Implementation Notes

### Nonce Handling Strategy

Two approaches for CSRF protection with user_id embedding:

**Option A: Keep separate nonce storage**
- State = JSON with `{user_id, nonce}`
- Nonce stored separately in `_PENDING_NONCES`
- Verify nonce in storage, extract user_id from state

**Option B: Sign the state** (recommended)
- State = JSON with `{user_id, nonce, timestamp}`
- Base64 encode with HMAC signature
- No server-side nonce storage needed
- Verify signature on callback

**Recommendation**: Option A is simpler for MVP, Option B scales better.

### Migration Consideration

- Existing states (currently pending) will fail validation after deploy
- Acceptable: OAuth states are short-lived (5-15 minutes)
- Users mid-flow will need to restart OAuth
- No persistent data migration needed

---

## Files to Modify (Phase 5 - OAuth State Redesign)

| File | Changes |
|------|---------|
| `services/integrations/calendar/oauth_handler.py` | State encoding/decoding, verify returns user_id |
| `services/integrations/slack/oauth_handler.py` | State encoding/decoding, verify returns user_id |
| `web/api/routes/setup.py` | Add authentication, pass user_id |
| `web/api/routes/settings_integrations.py` | Add authentication, pass user_id |

---

## Conclusion

OAuth state infrastructure is functional for CSRF protection but **fundamentally lacks user identity**. The fix requires:

1. Authenticating OAuth initiation routes (prerequisite)
2. Embedding user_id in OAuth state
3. Extracting user_id on callback
4. Using user_id for token storage

This is **not a bug fix** but a **design change** that affects both handlers and all routes that initiate OAuth.

---

_Investigation complete: 2026-01-30_
_Ready for: Phase 3 (RequestContext enforcement) then Phase 5 (OAuth State Redesign)_
