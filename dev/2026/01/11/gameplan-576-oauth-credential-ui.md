# Gameplan: Issue #576 - OAuth App Credential Configuration in UI

**Date**: 2026-01-11
**Issue**: #576
**Template Version**: v9.3
**Status**: Ready for PM Approval
**Estimated Effort**: Medium (~4 hours)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] KeychainService exists: `services/infrastructure/keychain_service.py`
- [x] KeychainService has `store_api_key()` and `get_api_key()` methods
- [x] SlackConfigService exists with 4-layer priority (env > user config > keychain > defaults)
- [x] Setup wizard exists: `templates/setup.html`
- [x] Slack settings page exists: `templates/settings_slack.html`
- [x] Settings integrations routes exist: `web/api/routes/settings_integrations.py`

**My understanding of the task**:
- Add 2 new API endpoints for app credential management
- Update SlackConfigService to read client_id/client_secret from keychain
- Add credential form to setup wizard (shown before Connect button if not configured)
- Add credential management section to settings page
- Store credentials securely in keychain, never expose in responses

### Part A.2: Work Characteristics Assessment

**Assessment**:
- [x] **SKIP WORKTREE** - Single agent, medium effort, sequential phases

### Part B: PM Verification Required

**PM, please confirm**:
1. [x] Keychain storage for app credentials is acceptable security approach
2. [ ] Setup wizard modification approach (form before Connect) is correct UX
3. [ ] Settings page should allow updating credentials (not just viewing status)
4. [ ] Any critical context I'm missing?

### Part C: Proceed/Revise Decision
- [ ] **PROCEED** - Understanding correct
- [ ] **REVISE** - Assumptions wrong
- [ ] **CLARIFY** - Need more context

---

## Phase 0.6: Data Flow & Integration Verification

### User Context Propagation

| Layer | Needs user_id? | Source of value |
|-------|----------------|-----------------|
| Route handler (POST /slack/app-credentials) | [x] Yes | `Depends(get_current_user)` |
| KeychainService.store_api_key() | [ ] No | Stores globally (not per-user) |

**Note**: Slack app credentials are app-level, not user-level. They're stored globally in keychain, not per-user. The user_id dependency is for authentication only.

### Integration Points Checklist

| Caller | Callee | Import Path Verified? | Method Verified? |
|--------|--------|----------------------|------------------|
| settings_integrations.py | KeychainService | [x] `services.infrastructure.keychain_service` | [x] `store_api_key`, `get_api_key` |
| settings_integrations.py | SlackConfigService | [x] `services.integrations.slack.config_service` | [x] `get_config()` |
| SlackConfigService | KeychainService | [x] Already verified in #575 | [x] `get_api_key` |

**Verification**:
```bash
python -c "from services.infrastructure.keychain_service import KeychainService; print('OK')"
python -c "from services.integrations.slack.config_service import SlackConfigService; print('OK')"
```

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

When credentials are saved successfully:

| Side Effect | Storage | Value | Verified? |
|-------------|---------|-------|-----------|
| client_id stored | Keychain (slack_client_id) | user input | [ ] |
| client_secret stored | Keychain (slack_client_secret) | user input | [ ] |
| SlackConfigService returns credentials | get_config().client_id | from keychain | [ ] |

### Downstream Behavior Changes

| Feature | Before Credentials Saved | After Credentials Saved |
|---------|-------------------------|------------------------|
| Setup wizard Connect button | Hidden | Visible |
| GET /slack/oauth/start | Returns 503 error | Returns auth_url |
| Settings App Config status | "Not configured" | "Configured" |

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: ✅ #576 exists, template-compliant

2. **Codebase Investigation**:
   - Verify KeychainService API
   - Verify current SlackConfigService._load_config() structure
   - Verify setup.html Step 2 structure
   - Verify settings_slack.html structure

3. **Update GitHub Issue** (progressive bookending):
   ```bash
   gh issue comment 576 -b "## Status: Implementation Starting
   - [x] Gameplan approved
   - [x] Infrastructure verified
   - [ ] Phase 1: Backend API
   - [ ] Phase 2: Setup Wizard UI
   - [ ] Phase 3: Settings Page UI
   - [ ] Phase 4: Testing"
   ```

---

## Phase 0.5: Frontend-Backend Contract Verification

### Existing Endpoints (verified)
| Endpoint | Path | Status |
|----------|------|--------|
| Start Slack OAuth | GET /api/v1/setup/slack/oauth/start | ✅ Exists (now validates credentials) |
| Slack OAuth Callback | GET /api/v1/setup/slack/oauth/callback | ✅ Exists |
| Slack Status | GET /api/v1/setup/slack/status | ✅ Exists |

### New Endpoints (to create)
| Endpoint | Path | Purpose |
|----------|------|---------|
| Save App Credentials | POST /api/v1/settings/integrations/slack/app-credentials | Store client_id and client_secret in keychain |
| Get Credentials Status | GET /api/v1/settings/integrations/slack/app-credentials/status | Check if credentials configured (boolean only) |

### Request/Response Contracts

**POST /slack/app-credentials**
```json
// Request
{
  "client_id": "string (required)",
  "client_secret": "string (required)"
}

// Response (success)
{
  "success": true,
  "message": "Slack app credentials saved securely"
}

// Response (error)
{
  "detail": "Both client_id and client_secret are required"
}
```

**GET /slack/app-credentials/status**
```json
// Response
{
  "configured": true,  // or false
  "has_client_id": true,
  "has_client_secret": true
}
// NOTE: Never return actual credential values
```

---

## Phase 1: Backend API (1 hour)

### Objective
Create API endpoints for credential management and update config service.

### 1.1 Update SlackConfigService

**File**: `services/integrations/slack/config_service.py`

Add keychain fallback for client_id and client_secret (same pattern as bot_token from #575):

```python
# In _load_config():
keychain_client_id = keychain.get_api_key("slack_client_id") or ""
keychain_client_secret = keychain.get_api_key("slack_client_secret") or ""

# 4-layer priority for each
client_id = os.getenv("SLACK_CLIENT_ID") or oauth_config.get("client_id") or keychain_client_id or ""
client_secret = os.getenv("SLACK_CLIENT_SECRET") or oauth_config.get("client_secret") or keychain_client_secret or ""
```

### 1.2 Add API Endpoints

**File**: `web/api/routes/settings_integrations.py`

```python
class SlackAppCredentialsRequest(BaseModel):
    """Request body for saving Slack app credentials."""
    client_id: str
    client_secret: str

class SlackAppCredentialsStatusResponse(BaseModel):
    """Response for credential status check."""
    configured: bool
    has_client_id: bool
    has_client_secret: bool

@router.post("/slack/app-credentials")
async def save_slack_app_credentials(
    credentials: SlackAppCredentialsRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """Save Slack app credentials to secure keychain storage."""
    # Validate both fields present
    # Store in keychain
    # Return success

@router.get("/slack/app-credentials/status", response_model=SlackAppCredentialsStatusResponse)
async def get_slack_app_credentials_status(
    current_user: JWTClaims = Depends(get_current_user),
):
    """Check if Slack app credentials are configured."""
    # Check keychain and config for credentials
    # Return boolean status only (never actual values)
```

### Tasks
- [ ] Update `SlackConfigService._load_config()` with keychain fallback for client_id/client_secret
- [ ] Add `SlackAppCredentialsRequest` Pydantic model
- [ ] Add `SlackAppCredentialsStatusResponse` Pydantic model
- [ ] Add `POST /slack/app-credentials` endpoint
- [ ] Add `GET /slack/app-credentials/status` endpoint
- [ ] Verify endpoints require authentication

### Deliverables
- Updated config service
- 2 new API endpoints working
- Test with curl to verify

### Progressive Bookending
```bash
gh issue comment 576 -b "✓ Phase 1 Complete: Backend API
- SlackConfigService now reads client_id/client_secret from keychain
- POST /slack/app-credentials saves to keychain
- GET /slack/app-credentials/status returns boolean status
- All endpoints require authentication"
```

---

## Phase 2: Setup Wizard UI (1.5 hours)

### Objective
Add credential configuration form to setup wizard before Connect button.

### 2.1 UI Flow

```
Step 2: Integrations
├── Slack Section
│   ├── IF credentials NOT configured:
│   │   ├── "Configure Slack App" card
│   │   ├── Help text with link to api.slack.com/apps
│   │   ├── client_id input field
│   │   ├── client_secret input field (password type)
│   │   ├── "Save Credentials" button
│   │   └── (Connect button hidden)
│   ├── IF credentials configured:
│   │   ├── Status: "✓ App credentials configured"
│   │   └── "Connect Slack" button (visible)
```

### 2.2 HTML Structure

**File**: `templates/setup.html`

```html
<!-- Slack App Configuration (shown if not configured) -->
<div id="slack-config-section" class="config-section" style="display: none;">
  <h4>Configure Slack App</h4>
  <p class="help-text">
    First, create a Slack app at
    <a href="https://api.slack.com/apps" target="_blank">api.slack.com/apps</a>
    and copy your credentials below.
  </p>
  <div class="form-group">
    <label for="slack-client-id">Client ID</label>
    <input type="text" id="slack-client-id" placeholder="Your Slack app's Client ID">
  </div>
  <div class="form-group">
    <label for="slack-client-secret">Client Secret</label>
    <input type="password" id="slack-client-secret" placeholder="Your Slack app's Client Secret">
  </div>
  <button class="btn btn-primary" onclick="saveSlackAppCredentials()">
    Save Credentials
  </button>
</div>

<!-- Connect button (shown after credentials configured) -->
<div id="slack-connect-section" style="display: none;">
  <p class="status-configured">✓ App credentials configured</p>
  <button class="btn btn-primary" onclick="connectSlack()">
    Connect Slack
  </button>
</div>
```

### 2.3 JavaScript Functions

```javascript
async function checkSlackCredentialsStatus() {
  const response = await fetch('/api/v1/settings/integrations/slack/app-credentials/status');
  const data = await response.json();

  if (data.configured) {
    document.getElementById('slack-config-section').style.display = 'none';
    document.getElementById('slack-connect-section').style.display = 'block';
  } else {
    document.getElementById('slack-config-section').style.display = 'block';
    document.getElementById('slack-connect-section').style.display = 'none';
  }
}

async function saveSlackAppCredentials() {
  const clientId = document.getElementById('slack-client-id').value.trim();
  const clientSecret = document.getElementById('slack-client-secret').value.trim();

  if (!clientId || !clientSecret) {
    showToast('error', 'Both Client ID and Client Secret are required');
    return;
  }

  const response = await fetch('/api/v1/settings/integrations/slack/app-credentials', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ client_id: clientId, client_secret: clientSecret })
  });

  if (response.ok) {
    showToast('success', 'Slack app credentials saved');
    checkSlackCredentialsStatus();  // Refresh UI
  } else {
    const error = await response.json();
    showToast('error', error.detail || 'Failed to save credentials');
  }
}
```

### Tasks
- [ ] Add CSS for config section and form groups
- [ ] Add HTML for credential configuration section
- [ ] Add HTML for connect section (shown after configured)
- [ ] Add `checkSlackCredentialsStatus()` function
- [ ] Add `saveSlackAppCredentials()` function
- [ ] Call `checkSlackCredentialsStatus()` on page load
- [ ] Verify form validation works

### Deliverables
- Credential form visible when not configured
- Connect button visible after credentials saved
- Toast feedback on save

### Progressive Bookending
```bash
gh issue comment 576 -b "✓ Phase 2 Complete: Setup Wizard UI
- Credential configuration form added
- Help text links to Slack app creation
- Form hidden after credentials saved
- Connect button appears when configured"
```

---

## Phase 3: Settings Page UI (1 hour)

### Objective
Add credential management section to Slack settings page.

### 3.1 UI Flow

```
Settings > Slack
├── Connection Status (existing)
├── App Configuration (NEW)
│   ├── Status indicator (configured/not configured)
│   ├── "Update Credentials" button (expandable form)
│   └── Help text
├── Channel Settings (from #570, shown when connected)
```

### 3.2 HTML Structure

**File**: `templates/settings_slack.html`

```html
<!-- App Configuration Section -->
<div class="settings-card" id="app-config-card">
  <h3>🔑 App Configuration</h3>

  <div id="app-config-status">
    <!-- Populated by JavaScript -->
  </div>

  <div id="app-config-form" style="display: none;">
    <p class="help-text">
      Update your Slack app credentials from
      <a href="https://api.slack.com/apps" target="_blank">api.slack.com/apps</a>
    </p>
    <div class="form-group">
      <label for="settings-slack-client-id">Client ID</label>
      <input type="text" id="settings-slack-client-id">
    </div>
    <div class="form-group">
      <label for="settings-slack-client-secret">Client Secret</label>
      <input type="password" id="settings-slack-client-secret">
    </div>
    <div class="button-group">
      <button class="btn btn-primary" onclick="updateSlackAppCredentials()">Save</button>
      <button class="btn btn-secondary" onclick="hideAppConfigForm()">Cancel</button>
    </div>
  </div>
</div>
```

### 3.3 JavaScript Functions

```javascript
async function loadAppConfigStatus() {
  const response = await fetch('/api/v1/settings/integrations/slack/app-credentials/status');
  const data = await response.json();

  const statusDiv = document.getElementById('app-config-status');
  if (data.configured) {
    statusDiv.innerHTML = `
      <p class="status-configured">✓ App credentials configured</p>
      <button class="btn btn-secondary" onclick="showAppConfigForm()">Update Credentials</button>
    `;
  } else {
    statusDiv.innerHTML = `
      <p class="status-not-configured">⚠️ App credentials not configured</p>
      <button class="btn btn-primary" onclick="showAppConfigForm()">Configure Now</button>
    `;
  }
}

function showAppConfigForm() {
  document.getElementById('app-config-form').style.display = 'block';
}

function hideAppConfigForm() {
  document.getElementById('app-config-form').style.display = 'none';
}

async function updateSlackAppCredentials() {
  // Same logic as saveSlackAppCredentials() but for settings page
  // On success: hideAppConfigForm(), loadAppConfigStatus()
}
```

### Tasks
- [ ] Add CSS for app configuration card
- [ ] Add HTML for app configuration section
- [ ] Add `loadAppConfigStatus()` function
- [ ] Add `showAppConfigForm()` and `hideAppConfigForm()` functions
- [ ] Add `updateSlackAppCredentials()` function
- [ ] Call `loadAppConfigStatus()` on page load
- [ ] Verify update flow works

### Deliverables
- App configuration section in settings
- Status indicator showing configured/not configured
- Update form with save/cancel

### Progressive Bookending
```bash
gh issue comment 576 -b "✓ Phase 3 Complete: Settings Page UI
- App Configuration section added
- Shows configured/not configured status
- Update form with save/cancel
- Consistent with setup wizard UX"
```

---

## Phase 4: Testing (30 min)

### Manual Testing Checklist

**Scenario 1**: Fresh Setup (no credentials)
1. [ ] Start with no Slack credentials in keychain/env/config
2. [ ] Go to setup wizard Step 2
3. [ ] Verify "Configure Slack App" form visible
4. [ ] Verify "Connect Slack" button NOT visible
5. [ ] Enter valid credentials, click Save
6. [ ] Verify success toast
7. [ ] Verify form hides, Connect button appears
8. [ ] Click Connect → OAuth flow starts (or clearer error if redirect_uri missing)

**Scenario 2**: Settings Page Update
1. [ ] With credentials configured, go to Settings → Slack
2. [ ] Verify "App Configuration" section shows "✓ Configured"
3. [ ] Click "Update Credentials"
4. [ ] Verify form expands
5. [ ] Enter new credentials, click Save
6. [ ] Verify success toast, form collapses
7. [ ] Verify status still shows configured

**Scenario 3**: Validation
1. [ ] In setup wizard, try to save with empty client_id
2. [ ] Verify error toast "Both fields required"
3. [ ] Try to save with empty client_secret
4. [ ] Verify error toast

**Scenario 4**: Persistence
1. [ ] Configure credentials via UI
2. [ ] Restart server
3. [ ] Check status endpoint returns `configured: true`
4. [ ] Verify OAuth flow still works

### Unit Tests

**File**: `tests/unit/web/api/routes/test_settings_integrations.py`

```python
def test_save_slack_app_credentials_success()
def test_save_slack_app_credentials_missing_client_id()
def test_save_slack_app_credentials_missing_client_secret()
def test_get_slack_app_credentials_status_configured()
def test_get_slack_app_credentials_status_not_configured()
def test_credentials_not_exposed_in_status_response()
def test_endpoints_require_authentication()
```

### Tasks
- [ ] Run all manual test scenarios
- [ ] Write unit tests for new endpoints
- [ ] Run unit tests, verify all pass
- [ ] Run Slack integration tests, verify no regressions

### Progressive Bookending
```bash
gh issue comment 576 -b "✓ Phase 4 Complete: Testing
- All manual scenarios pass
- Unit tests written and passing
- No regressions in existing tests"
```

---

## Phase Z: Final Bookending & Handoff

### Evidence Required
- [ ] Screenshot: Setup wizard with credential form
- [ ] Screenshot: Setup wizard after credentials saved (Connect visible)
- [ ] Screenshot: Settings page App Configuration section
- [ ] API test: POST /slack/app-credentials success
- [ ] API test: GET /slack/app-credentials/status returns correct boolean
- [ ] Test output: Unit tests passing

### Completion Matrix Update
Update GitHub issue #576 with all evidence.

### Commit
```bash
git add .
git commit -m "feat(#576): Add OAuth app credential configuration UI

- Add POST/GET endpoints for Slack app credentials
- Update SlackConfigService with keychain fallback for client_id/client_secret
- Add credential form to setup wizard
- Add App Configuration section to settings page
- Store credentials securely in keychain

Closes #576"
```

---

## Completion Matrix

| Criterion | Status | Evidence |
|-----------|--------|----------|
| SlackConfigService keychain for app creds | ❌ | - |
| POST /slack/app-credentials endpoint | ❌ | - |
| GET /slack/app-credentials/status endpoint | ❌ | - |
| Setup wizard credential form | ❌ | - |
| Setup wizard Connect button toggle | ❌ | - |
| Settings page App Configuration section | ❌ | - |
| Settings page update form | ❌ | - |
| Unit tests | ❌ | - |
| Manual tests pass | ❌ | - |
| No regressions | ❌ | - |

---

## STOP Conditions

- KeychainService cannot store these keys → Escalate
- Security concern with credential handling → Escalate
- Existing OAuth flow breaks → Escalate
- Setup wizard HTML structure incompatible → Escalate
- Settings page HTML structure incompatible → Escalate
- Import path doesn't exist → Fix before proceeding
- Method name wrong → Verify before calling

---

## Agent Deployment

**Single Agent Justification**:
- Sequential phases (backend must complete before frontend)
- Tightly coupled files (endpoints + UI call same service)
- Medium effort (~4 hours)
- No parallel work opportunities

**Worktree**: SKIP (single agent, sequential work)

---

## Verification Gates

- [ ] Phase 1: API endpoints return correct responses
- [ ] Phase 1: SlackConfigService reads from keychain
- [ ] Phase 2: Setup wizard shows correct UI state
- [ ] Phase 3: Settings page shows correct UI state
- [ ] Phase 4: All manual test scenarios pass
- [ ] Phase 4: Unit tests pass
- [ ] Phase 4: No regressions in existing Slack tests

---

## Test Scope Requirements

### Unit Tests
- [ ] `test_save_slack_app_credentials_success`
- [ ] `test_save_slack_app_credentials_missing_fields`
- [ ] `test_get_slack_app_credentials_status_configured`
- [ ] `test_get_slack_app_credentials_status_not_configured`
- [ ] `test_credentials_not_exposed_in_status`
- [ ] `test_endpoints_require_authentication`

### Wiring Tests (verify real integration, minimal mocking)
```python
# Verify keychain integration works end-to-end
def test_credential_roundtrip():
    keychain = KeychainService()
    keychain.store_api_key("slack_client_id", "test_id")

    config_service = SlackConfigService()
    config = config_service.get_config()
    assert config.client_id == "test_id"  # Proves real wiring
```

### Regression Tests
- [ ] Existing Slack OAuth tests still pass
- [ ] Existing Slack config tests still pass

---

## Notes

- Credentials stored with keys: `slack_client_id`, `slack_client_secret`
- Never return actual credential values in any API response
- Help text must link to https://api.slack.com/apps
- Follow existing toast/dialog patterns from other settings pages

---

*Gameplan created: 2026-01-11 10:09*
