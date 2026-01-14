# Gameplan: Issue #579 - Notion API Key Configuration in UI

**Issue**: #579 ENHANCE-NOTION-KEY-UI
**Created**: 2026-01-11
**Status**: Ready for Implementation
**Estimated Effort**: Small (~30 min - likely 75% pattern)
**Template Version**: 9.3

---

## Overview

Add keychain fallback to NotionConfigService so UI-saved API keys are loaded correctly.

**Pre-Investigation Finding**: Based on #578 pattern, endpoints already exist:
- `POST /api/v1/settings/integrations/notion/save` - saves via UserAPIKeyService
- `GET /api/v1/settings/integrations/notion` - checks status
- `POST /api/v1/settings/integrations/notion/disconnect` - removes key
- Settings page: `templates/settings_notion.html` - likely has UI

**Expected Gap**: `NotionConfigService._load_config()` doesn't check keychain.

---

## Phase -1: Infrastructure Verification (5 min)

### Part A: Chief Architect's Current Understanding

Based on #578 investigation, I believe:

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Database: PostgreSQL (port 5433)
- [x] Testing framework: pytest
- [x] Existing endpoints: `/notion/save`, `/notion`, `/notion/disconnect` (from Issue #540)
- [x] KeychainService: via `UserAPIKeyService` (provider="notion", user_id="system")

**My understanding of the task**:
- I believe we need to: Add keychain fallback to NotionConfigService (same as #578)
- I think this involves: ~10 lines in config service + tests
- I assume the current state is: UI exists, save works, but config service doesn't load from keychain

### Part A.2: Worktree Assessment

**Assessment**: **SKIP WORKTREE** - Single agent, ~30 min, sequential work.

### Part B: PM Verification Required

**PM, please confirm**:
- [x] Infrastructure assumptions correct
- [x] Task scope appropriate (likely 75% pattern)
- [x] Proceed with implementation

### Part C: Verification Checklist

```bash
# 1. Verify NotionConfigService exists
ls -la services/integrations/notion/config_service.py

# 2. Verify settings_notion.html exists
ls -la templates/settings_notion.html

# 3. Verify endpoints exist
grep -n "/notion" web/api/routes/settings_integrations.py
```

---

## Phase 0: Investigation (5 min)

### Objective
Confirm 75% pattern and identify exact gap.

### Investigation Tasks

1. **Confirm save endpoint uses UserAPIKeyService** (already verified):
   - Endpoint: `POST /notion/save` (line 902)
   - Storage: `UserAPIKeyService.store_user_key(provider="notion", user_id="system")`

2. **Check NotionConfigService._load_config()** (already verified):
   - Line 162: Only checks `os.getenv("NOTION_API_KEY")` and `auth_config.get("api_key")`
   - No keychain fallback

3. **Check settings_notion.html for existing UI**:
   ```bash
   grep -n "api.key\|save\|token" templates/settings_notion.html
   ```

### Key Finding
Gap is exactly the same as #578: Need to add keychain fallback to config service.

---

## Phase 0.5: Frontend-Backend Contract (2 min)

### Existing Contract (Already Implemented)

**Save Key**:
```
POST /api/v1/settings/integrations/notion/save
Content-Type: application/x-www-form-urlencoded

Body: api_key=secret_xxxxx

Response (200):
{
  "success": true,
  "workspace": "My Workspace",
  "message": "Connected to My Workspace"
}
```

**Get Status**:
```
GET /api/v1/settings/integrations/notion

Response (200):
{
  "configured": true,
  "valid": true,
  "workspace_name": "My Workspace"
}
```

---

## Phase 0.6: Data Flow & Integration Verification

### Applicability Assessment
- [x] Single-layer changes ✓

**Assessment**: **SKIP** - Single-layer feature (Config Service → Keychain).

---

## Phase 0.7: Conversation Design

**Assessment**: **N/A** - Not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

**Assessment**: **MINIMAL** - API key stored in keychain only, no database changes for this fix.

---

## Phase 1: Add Keychain Fallback to NotionConfigService (15 min)

### 1.1 Modify _load_config() Method

**File**: `services/integrations/notion/config_service.py`

Find the `_load_config()` method and add keychain fallback after env var check:

```python
def _load_config(self) -> NotionConfig:
    # ... existing code ...

    # Get API key with fallback chain: env var > user config > keychain
    api_key = os.getenv("NOTION_API_KEY", auth_config.get("api_key", ""))

    # Issue #579: Fallback to keychain if not found
    if not api_key:
        try:
            from services.infrastructure.keychain_service import KeychainService
            keychain = KeychainService()
            # Note: UserAPIKeyService stores with provider="notion", user_id="system"
            api_key = keychain.get_api_key("notion", username="system") or ""
        except Exception:
            pass  # Keychain not available

    return NotionConfig(
        api_key=api_key,
        # ... rest unchanged ...
    )
```

### 1.2 Understanding the Storage Pattern

Notion uses `UserAPIKeyService` which calls:
```python
keychain.store_api_key(provider, api_key, username=user_id)
# → keychain.store_api_key("notion", api_key, username="system")
```

So retrieval is:
```python
keychain.get_api_key("notion", username="system")
```

This is different from GitHub which used:
```python
keychain.store_api_key("github_token", token)
keychain.get_api_key("github_token")
```

Need to check KeychainService API to understand this pattern.

---

## Phase 2: Verify Existing UI (5 min)

### Objective
Confirm settings page UI already exists (likely from #540).

### Verification
```bash
# Check settings_notion.html for form elements
grep -n "input\|button\|save" templates/settings_notion.html | head -20
```

If UI exists, no changes needed. If not, follow #578 pattern.

---

## Phase 3: Testing (10 min)

### 3.1 Add Tests for Keychain Fallback

**File**: `tests/unit/web/api/routes/test_settings_notion.py` (extend if exists)

```python
class TestNotionConfigServiceKeychainFallback:
    """Tests for NotionConfigService keychain fallback (Issue #579)"""

    def test_get_config_returns_env_var_first(self):
        """Should return env var API key when available"""
        # ...

    def test_get_config_falls_back_to_keychain(self):
        """Should fall back to keychain when no env var is set"""
        # ...

    def test_get_config_returns_empty_when_nothing_configured(self):
        """Should return empty when neither env var nor keychain has key"""
        # ...

    def test_get_config_handles_keychain_error_gracefully(self):
        """Should handle keychain errors gracefully"""
        # ...
```

### 3.2 Run Tests
```bash
python -m pytest tests/unit/web/api/routes/test_settings_notion.py -xvs
```

---

## Phase Z: Final Bookending (5 min)

### Checklist
- [ ] All tests pass
- [ ] Pre-commit hooks pass
- [ ] Commit with proper message
- [ ] Update GitHub issue with evidence
- [ ] Request PM closure

### Commit Message Template
```
feat(#579): Add keychain fallback to NotionConfigService

Completes the 75% pattern - UI and save endpoints existed but config
service didn't check keychain, only env vars.

Changes:
- Add keychain fallback to _load_config() in NotionConfigService
- Priority: env vars > PIPER.user.md > keychain
- Add N tests for keychain fallback behavior

Same pattern as #578 (GitHub). Notion uses UserAPIKeyService which
stores with provider="notion", username="system".

Issue: #579

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## STOP Conditions

Stop immediately and escalate if:
- NotionConfigService doesn't exist or has different structure
- KeychainService API doesn't support username parameter
- UserAPIKeyService stores keys differently than expected
- Tests fail for any reason
- **Import path doesn't exist** (v9.3)
- **Method name typo** (v9.3)
- **Required parameter not available at call site** (v9.3)

---

## Multi-Agent Deployment

**Assessment**: **SINGLE AGENT** - Simple, sequential work following established pattern.

---

## Risk Assessment

**Low Risk**: Identical pattern to #578.

**Key Difference from #578**:
- Notion uses `UserAPIKeyService` → `KeychainService.store_api_key(provider, key, username=user_id)`
- GitHub used `KeychainService.store_api_key(key_name, key)` directly
- Need to verify KeychainService.get_api_key() supports username parameter

---

## Files to Modify Summary

| File | Changes |
|------|---------|
| `services/integrations/notion/config_service.py` | Add keychain fallback (~10 lines) |
| `tests/unit/web/api/routes/test_settings_notion.py` | Add keychain fallback tests |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-11 | Initial gameplan (template v9.3) |

---

_Gameplan created: 2026-01-11_
_Template version: 9.3_
