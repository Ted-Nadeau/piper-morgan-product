# Gameplan: #527 ALPHA-SETUP-NOTION

**Issue**: Add Notion integration to setup wizard
**Priority**: Alpha Critical
**Created**: 2025-12-31 17:55
**Author**: Claude Code (Opus)

---

## Executive Summary

Add Notion API key configuration to the existing setup wizard infrastructure, following established patterns from OpenAI/Anthropic key handling. The wizard already has a proven UI pattern (input + validate + keychain) and backend API pattern (`/setup/validate-key`, `/setup/check-keychain`, etc.).

**Key insight from investigation**: The existing infrastructure is well-designed but currently only handles LLM API keys. Notion is the first "integration" (as opposed to "AI provider") to be added to setup, so we'll establish the pattern for #528 (Slack) and #529 (Calendar).

---

## Phase -1: Investigation Summary

### Existing Infrastructure

**CLI Wizard** (`scripts/setup_wizard.py`):
- Modular with phases: preflight → system checks → database → user creation → API keys
- Uses `_collect_single_api_key()` helper with keychain, env var, and manual entry
- Current providers: openai, anthropic, gemini, github
- Pattern: `UserAPIKeyService.store_user_key()` for persistence

**Web Wizard** (`web/api/routes/setup.py` + `templates/setup.html` + `setup.js`):
- 4-step flow: System → API Keys → Account → Complete
- Uses `/setup/validate-key`, `/setup/check-keychain/{provider}`, `/setup/use-keychain`
- Keys validated via `UserAPIKeyService.store_user_key(validate=True, store=False)`
- State tracked in JS: `apiKeys`, `keychainKeys`

**Notion Config** (`services/integrations/notion/config_service.py`):
- Loads from: env vars (`NOTION_API_KEY`) → `PIPER.user.md` → defaults
- `NotionConfigService.is_configured()` → checks if API key exists
- `NotionIntegrationRouter.test_connection()` → delegates to Notion SDK

**Issues Identified**:
1. **Validation gap**: Setup wizard uses `ApiKeyValidateRequest` with hardcoded providers: `["openai", "anthropic", "github"]` - needs `notion` added
2. **Storage gap**: `UserAPIKeyService` may not handle `notion` as a provider - need to verify
3. **Test connection gap**: Need to wire Notion's `test_connection()` to setup validation
4. **No workspace selection**: Issue #527 says "Default database/workspace selection saved" - need UI for this

---

## Acceptance Criteria (from issue)

- [ ] User can enter Notion API key in setup wizard
- [ ] Connection test validates key works
- [ ] ~~Default database/workspace selection saved~~ **DEFERRED to #537** (premature, not MVP)
- [ ] **NEW**: Workspace name displayed after successful validation
- [ ] Error messages guide troubleshooting
- [ ] **NEW**: Dashboard "Configure" button redirects to setup wizard (Option A per PM)

---

## Phase 0: TDD Test Scaffolding

**File**: `tests/unit/web/api/routes/test_setup_notion.py`

```python
"""
Unit tests for Notion integration in setup wizard
Issue #527: ALPHA-SETUP-NOTION
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

pytestmark = pytest.mark.unit


class TestNotionKeyValidation:
    """Tests for Notion API key validation in setup wizard"""

    @pytest.mark.asyncio
    async def test_validate_notion_key_success(self):
        """Valid Notion key should return valid=True"""
        # Given: A valid Notion API key
        # When: POST /setup/validate-key with provider=notion
        # Then: Response has valid=True, message confirms access
        pass

    @pytest.mark.asyncio
    async def test_validate_notion_key_invalid(self):
        """Invalid Notion key should return valid=False with guidance"""
        pass

    @pytest.mark.asyncio
    async def test_validate_notion_key_wrong_format(self):
        """Notion key with wrong format should return clear error"""
        pass


class TestNotionKeychainCheck:
    """Tests for Notion keychain integration"""

    @pytest.mark.asyncio
    async def test_check_keychain_notion_exists(self):
        """Should return exists=True when Notion key in keychain"""
        pass

    @pytest.mark.asyncio
    async def test_use_keychain_notion_success(self):
        """Should retrieve and validate Notion key from keychain"""
        pass


class TestNotionWorkspaceInfo:
    """Tests for Notion workspace information display"""

    @pytest.mark.asyncio
    async def test_validation_returns_workspace_name(self):
        """Should return workspace name after successful validation"""
        pass

    @pytest.mark.asyncio
    async def test_workspace_name_displayed_in_status(self):
        """Should display workspace name in validation status message"""
        pass


class TestNotionSetupComplete:
    """Tests for Notion key storage on setup completion"""

    @pytest.mark.asyncio
    async def test_complete_stores_notion_key(self):
        """Setup completion should store Notion key securely"""
        pass
```

**Test count target**: 10-12 tests

---

## Phase 1: Backend - Extend Setup API

### 1.1 Add Notion to Provider Validation

**File**: `web/api/routes/setup.py`

**Changes**:
1. Update `ApiKeyValidateRequest.validate_provider()` to accept `notion`
2. Update `KeychainUseRequest.validate_provider()` to accept `notion`
3. Add Notion-specific validation logic in `validate_api_key()`

```python
# In ApiKeyValidateRequest.validate_provider()
if v not in ["openai", "anthropic", "github", "notion"]:
    raise ValueError("provider must be one of: openai, anthropic, github, notion")

# In validate_api_key() - add Notion handling
if req.provider == "notion":
    # Use NotionIntegrationRouter.test_connection()
    from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

    # Temporarily set the key in environment for test
    with patch.dict(os.environ, {"NOTION_API_KEY": req.api_key}):
        router = NotionIntegrationRouter()
        is_valid = await router.test_connection()

    if is_valid:
        return ApiKeyValidateResponse(
            provider=req.provider,
            valid=True,
            message="Valid (Notion workspace access confirmed)",
        )
    else:
        return ApiKeyValidateResponse(
            provider=req.provider,
            valid=False,
            message="Invalid API key or insufficient permissions",
        )
```

### 1.2 Return Workspace Name in Validation Response

**File**: `web/api/routes/setup.py`

**Changes**: Update `ApiKeyValidateResponse` and validation logic to include workspace name:

```python
# Update ApiKeyValidateResponse to include workspace_name
class ApiKeyValidateResponse(BaseModel):
    provider: str
    valid: bool
    message: str
    workspace_name: Optional[str] = None  # NEW: For Notion

# In validate_api_key() - fetch workspace info on success
if req.provider == "notion":
    # ... validation logic ...
    if is_valid:
        # Get workspace name from Notion API
        workspace_name = await get_notion_workspace_name(req.api_key)
        return ApiKeyValidateResponse(
            provider=req.provider,
            valid=True,
            message=f"Valid (Connected to '{workspace_name}')",
            workspace_name=workspace_name,
        )
```

**Note**: Database selection endpoints DEFERRED to #537 per PM decision.

### 1.3 Update Setup Complete to Handle Notion

**File**: `web/api/routes/setup.py`

**Changes to `SetupCompleteRequest`**:
```python
class SetupCompleteRequest(BaseModel):
    user_id: str
    openai_key: Optional[str] = None
    anthropic_key: Optional[str] = None
    notion_key: Optional[str] = None  # NEW
    # notion_default_database_id: DEFERRED to #537
```

---

## Phase 2: Backend - CLI Wizard Extension

### 2.1 Add Notion to CLI Wizard

**File**: `scripts/setup_wizard.py`

**Changes to `collect_and_validate_api_keys()`**:

```python
# After GitHub token section, add:

# Notion API key (optional)
print("\n   Notion API key (optional, press Enter to skip):")
print("   Get your API key at: https://www.notion.so/my-integrations")
notion_key = await _collect_single_api_key(
    user_id=user_id,
    service=service,
    provider="notion",
    env_var_name="NOTION_API_KEY",
    format_hint="secret_...",
    validation_msg="workspace access confirmed",
    is_required=False,
    skip_validation=False,  # We DO want to validate Notion
)
if notion_key:
    stored_keys["notion"] = notion_key

    # Offer database selection
    print("\n   Would you like to set a default Notion database?")
    set_default = input("   (y/n): ").strip().lower()
    if set_default == "y":
        await _select_notion_default_database(user_id, notion_key)
```

### 2.2 Add Notion Validation to UserAPIKeyService

**File**: `services/security/user_api_key_service.py`

**Verify or add** Notion to the supported providers:
- Check `validate_user_key()` handles `notion` provider
- Add Notion-specific validation using `NotionIntegrationRouter.test_connection()`

---

## Phase 3: Frontend - Web Setup Wizard

### 3.1 Add Notion Input to Step 2

**File**: `templates/setup.html`

**Add after Gemini section** (line ~198):

```html
<div class="form-group">
    <label for="notion-key">Notion API Key (optional)</label>
    <div class="key-validation">
        <input type="password" id="notion-key" placeholder="secret_..." />
        <button type="button" class="validate-key-btn" data-provider="notion">Validate</button>
        <button type="button" class="keychain-btn hidden" data-provider="notion">Use Keychain</button>
    </div>
    <div id="notion-status" class="validation-status"></div>
    <small><a href="https://www.notion.so/my-integrations" target="_blank">Get your Notion API key</a></small>
</div>

<!-- Database selection DEFERRED to #537 -->
```

### 3.2 Add Notion Handling to JavaScript

**File**: `web/static/js/setup.js`

**Changes**:

1. Add `notion` to state tracking:
```javascript
const apiKeys = { openai: null, anthropic: null, gemini: null, notion: null };
const keychainKeys = { openai: false, anthropic: false, gemini: false, notion: false };
```

2. Add to keychain check:
```javascript
const providers = ['openai', 'anthropic', 'gemini', 'notion'];
```

3. Update validation success to show workspace name (returned by API):
```javascript
// In validate key success handler
if (data.valid) {
    // Use workspace_name from response if available (Notion)
    const message = data.workspace_name
        ? `✓ Valid (Connected to '${data.workspace_name}')`
        : `✓ ${data.message}`;
    statusDiv.textContent = message;
    // ... rest of success handling
}
```

4. Update `completeSetup()` to include Notion:
```javascript
body: JSON.stringify({
    user_id: userId,
    openai_key: keychainKeys.openai ? null : apiKeys.openai,
    anthropic_key: keychainKeys.anthropic ? null : apiKeys.anthropic,
    notion_key: keychainKeys.notion ? null : apiKeys.notion
    // notion_default_database_id: DEFERRED to #537
})
```

### 3.3 Dashboard "Configure" Link (Option A)

**File**: `templates/integrations.html` (or wherever #530 dashboard lives)

**Changes**: Update Notion "Configure" button to redirect to setup wizard:

```html
<!-- Notion card configure button -->
<a href="/setup#step-2" class="btn btn-secondary">Configure</a>
```

**Note**: This is Option A (simple redirect). Full inline configuration is tracked in #537.

---

## Phase 4: Integration Testing

### 4.1 Manual Test Scenarios

| Scenario | Steps | Expected |
|----------|-------|----------|
| Valid Notion key | Enter valid key → Click Validate | Shows "✓ Valid (Connected to 'Workspace Name')" |
| Invalid Notion key | Enter invalid key → Click Validate | Shows "✗ Invalid API key or insufficient permissions" |
| Wrong format | Enter `sk-abc...` → Click Validate | Shows format error |
| Keychain | Existing key in keychain → Click "Use Keychain" | Key retrieved, shows valid with workspace name |
| Dashboard configure | Click "Configure" on Notion card | Redirects to /setup#step-2 |

### 4.2 Integration Test File

**File**: `tests/integration/test_setup_notion.py`

```python
"""
Integration tests for Notion setup wizard flow
Issue #527: ALPHA-SETUP-NOTION
"""
import pytest
from unittest.mock import AsyncMock, patch

pytestmark = pytest.mark.integration


class TestNotionSetupFlow:
    """Full flow tests for Notion in setup wizard"""

    @pytest.mark.asyncio
    async def test_full_notion_setup_flow(self):
        """Complete Notion setup: validate → select db → complete"""
        pass
```

---

## Phase 5: Error Message Quality

### Error Guidance Mapping

| Error Type | Message | Fix Suggestion |
|------------|---------|----------------|
| `invalid_key` | "Invalid Notion API key" | "Check your key at notion.so/my-integrations" |
| `wrong_format` | "Key format incorrect" | "Notion keys start with 'secret_' or 'ntn_'" |
| `no_permissions` | "Key lacks required permissions" | "Ensure integration has access to your workspace" |
| `rate_limited` | "Rate limited by Notion" | "Wait a moment and try again" |
| `network_error` | "Could not reach Notion API" | "Check your internet connection" |

---

## Completion Matrix

| Phase | Deliverable | Verification |
|-------|-------------|--------------|
| 0 | Test scaffolding | `pytest tests/unit/web/api/routes/test_setup_notion.py --collect-only` |
| 1 | Backend API endpoints | Tests pass, curl commands work |
| 2 | CLI wizard extension | `python main.py setup` offers Notion |
| 3 | Frontend integration | Manual test in browser |
| 4 | Integration tests | All tests pass |
| 5 | Error messages | Each error scenario tested |

**All phases MUST complete before issue closure.**

---

## STOP Conditions

- [ ] If `UserAPIKeyService` doesn't support `notion` provider, STOP and extend it first
- [ ] If `NotionIntegrationRouter.test_connection()` doesn't work standalone, STOP and fix
- [ ] If database listing requires OAuth (not just API key), STOP and reassess scope
- [ ] If tests fail, STOP and fix before proceeding

---

## Files to Modify

1. `web/api/routes/setup.py` - Backend API
2. `scripts/setup_wizard.py` - CLI wizard
3. `templates/setup.html` - Frontend template
4. `web/static/js/setup.js` - Frontend JavaScript
5. `templates/integrations.html` - Dashboard configure link
6. `services/security/user_api_key_service.py` - If needed for Notion support

## Files to Create

1. `tests/unit/web/api/routes/test_setup_notion.py` - Unit tests
2. `tests/integration/test_setup_notion.py` - Integration tests

---

## Estimated Effort (Simplified - No Database Selection)

| Phase | Time |
|-------|------|
| Phase 0 (Tests) | 25 min |
| Phase 1 (Backend) | 35 min |
| Phase 2 (CLI) | 25 min |
| Phase 3 (Frontend) | 35 min |
| Phase 4 (Integration) | 20 min |
| Phase 5 (Error polish) | 15 min |
| **Total** | ~2.5 hours |

---

## PM Decisions (Resolved)

1. **Database selection**: ~~Required~~ → **DEFERRED to #537** (premature, not MVP feature)

2. **Workspace info display**: ✅ **IN SCOPE** - Show workspace name after validation like "Connected to 'Acme Corp'"

3. **Integration with #530**: ✅ **Option A** - Dashboard "Configure" button redirects to setup wizard. Full inline config tracked in #537.
