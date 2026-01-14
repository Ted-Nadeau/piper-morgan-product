# Gameplan: Issue #577 - Google Calendar OAuth Credential Configuration in UI

**Issue**: #577
**Date**: 2026-01-11
**Status**: Ready for Implementation
**Pattern Reference**: #576 (Slack OAuth UI) - follow identical pattern
**Template Version**: v9.2

---

## Phase -1: Infrastructure Verification Checkpoint (MANDATORY)

### Part A: Current Understanding

Based on #576 implementation, I believe:

**Infrastructure Status**:
- [x] Web framework: FastAPI (verified)
- [x] Credential storage: KeychainService (verified working for Slack)
- [x] Settings routes: `web/api/routes/settings_integrations.py` (exists, has Slack endpoints)
- [x] Calendar integration: `services/integrations/calendar/` (exists)
- [x] Setup wizard: `templates/setup.html` (exists, has Slack credential form)
- [ ] Calendar config service: Need to verify keychain integration pattern

**My understanding of the task**:
- I believe we need to: Add Calendar OAuth credential UI following Slack pattern exactly
- I think this involves: 2 API endpoints, config service update, setup wizard form, settings page
- I assume the current state is: Calendar OAuth works but requires env vars or credentials.json

### Part A.2: Worktree Assessment

Worktrees ADD value when:
- [ ] Multiple agents will work in parallel - NO, single agent
- [ ] Task duration >30 minutes - YES, ~2.5 hours
- [ ] Multi-component work - NO, follows established pattern
- [ ] Exploratory/risky changes - NO, copy-paste-adapt

Worktrees ADD overhead when:
- [x] Single agent, sequential work - YES
- [ ] Small fixes (<15 min) - NO
- [x] Tightly coupled files requiring atomic commits - YES
- [ ] Time-critical work - NO

**Assessment**: **SKIP WORKTREE**
Rationale: Single agent, following established pattern, 6 files modified atomically. Worktree overhead exceeds benefit.

### Part B: PM Verification Required

**PM, please confirm**:

1. **Infrastructure matches assumptions?**
   - [ ] `services/integrations/calendar/config_service.py` exists
   - [ ] `services/integrations/calendar/oauth_handler.py` exists
   - [ ] Can follow Slack pattern exactly

2. **Any critical context missing?**
   - Known issues with Calendar OAuth?
   - Special Google requirements not in Slack pattern?

3. **Proceed/Revise Decision**:
   - [ ] **PROCEED** - Understanding correct
   - [ ] **REVISE** - Assumptions wrong
   - [ ] **CLARIFY** - Need more info on: ____________

---

## Phase 0: Initial Bookending - GitHub Investigation

### 0.1 Verify Issue and Pattern
```bash
gh issue view 577
# Confirm issue exists and requirements match gameplan
```

### 0.2 Verify Existing Infrastructure
```bash
# Check Calendar config service exists
ls -la services/integrations/calendar/

# Verify Slack pattern to copy
grep -n "app-credentials" web/api/routes/settings_integrations.py

# Check keychain keys convention
grep -r "slack_client" services/
```

### 0.3 GitHub Update - Investigation Started
```bash
gh issue comment 577 -b "## Investigation Started
- [ ] Infrastructure verified
- [ ] Slack pattern confirmed
- [ ] Calendar config service located"
```

---

## Phase 0.5: Frontend-Backend Contract Verification (MANDATORY)

### Purpose
Prevent path mismatches between new Calendar endpoints and frontend calls.

### Required Actions

#### 1. After Backend Routes Created, BEFORE Frontend Work
```bash
# Get endpoint paths from settings_integrations.py
grep -n "@router\." web/api/routes/settings_integrations.py | grep calendar

# Get mount prefix
grep -n "settings_integrations\|settings/integrations" web/app.py
```

#### 2. Calculate Full Paths
| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| save credentials | /calendar/app-credentials | /api/v1/settings/integrations | /api/v1/settings/integrations/calendar/app-credentials |
| get status | /calendar/app-credentials/status | /api/v1/settings/integrations | /api/v1/settings/integrations/calendar/app-credentials/status |

#### 3. Verify Paths Work (Server Running)
```bash
# Test each endpoint BEFORE writing frontend
curl -s http://localhost:8001/api/v1/settings/integrations/calendar/app-credentials/status
# Must NOT return {"detail":"Not Found"}
```

#### 4. Static File Verification
```bash
# Verify JS file location
ls -la web/static/js/setup.js
# Confirm this is where Calendar JS will go
```

### STOP Condition
- If ANY endpoint returns 404 → fix backend before frontend
- If paths differ from Slack pattern → investigate why

---

## Phase 1: Backend API (45 min)

### 1.1 Add Request/Response Models

**File**: `web/api/routes/settings_integrations.py`

```python
class CalendarAppCredentialsRequest(BaseModel):
    client_id: str
    client_secret: str

class CalendarAppCredentialsStatus(BaseModel):
    configured: bool
    has_client_id: bool
    has_client_secret: bool
```

### 1.2 Add API Endpoints

**File**: `web/api/routes/settings_integrations.py`

Add after Slack endpoints (follow same pattern):

```python
@router.post("/calendar/app-credentials")
async def save_calendar_app_credentials(
    credentials: CalendarAppCredentialsRequest,
    current_user: JWTClaims = Depends(get_current_user),
) -> Dict[str, Any]:
    """Save Google Calendar OAuth app credentials to keychain."""
    keychain = KeychainService()
    keychain.store_api_key("google_calendar_client_id", credentials.client_id.strip())
    keychain.store_api_key("google_calendar_client_secret", credentials.client_secret.strip())

    logger.info("calendar_app_credentials_saved", user_id=current_user.sub)
    return {"success": True, "message": "Calendar app credentials saved"}


@router.get("/calendar/app-credentials/status")
async def get_calendar_app_credentials_status(
    current_user: JWTClaims = Depends(get_current_user),
) -> CalendarAppCredentialsStatus:
    """Check if Google Calendar OAuth app credentials are configured."""
    from services.integrations.calendar.config_service import CalendarConfigService

    config_service = CalendarConfigService()
    config = config_service.get_config()

    has_client_id = bool(config.client_id)
    has_client_secret = bool(config.client_secret)

    return CalendarAppCredentialsStatus(
        configured=has_client_id and has_client_secret,
        has_client_id=has_client_id,
        has_client_secret=has_client_secret,
    )
```

### 1.3 Update CalendarConfigService

**File**: `services/integrations/calendar/config_service.py`

Add keychain fallback for client_id and client_secret (same pattern as SlackConfigService):

```python
def get_config(self) -> CalendarConfig:
    # ... existing code ...

    # Add keychain fallback for OAuth app credentials
    if not client_id:
        keychain = KeychainService()
        client_id = keychain.get_api_key("google_calendar_client_id") or ""
    if not client_secret:
        keychain = KeychainService()
        client_secret = keychain.get_api_key("google_calendar_client_secret") or ""
```

### 1.4 Verification
```bash
# Restart server and test endpoints
curl -X GET http://localhost:8001/api/v1/settings/integrations/calendar/app-credentials/status
# Expected: {"configured": false, "has_client_id": false, "has_client_secret": false}
```

### 1.5 Progressive Bookend
```bash
gh issue comment 577 -b "✓ Phase 1 Complete: Backend API
- POST /calendar/app-credentials endpoint added
- GET /calendar/app-credentials/status endpoint added
- CalendarConfigService updated with keychain fallback
- Endpoints verified working (curl output attached)"
```

---

## Phase 2: Setup Wizard UI (45 min)

### 2.1 Add Credential Form to setup.html

**File**: `templates/setup.html`

Find the Calendar integration section and add (after the Slack pattern):

```html
<!-- Google Calendar App Configuration -->
<div id="calendarAppConfig" class="app-config-section" style="display: none;">
    <h4>Configure Google Calendar App</h4>
    <p class="help-text">
        Create OAuth credentials in
        <a href="https://console.cloud.google.com/apis/credentials" target="_blank">Google Cloud Console</a>.
        Choose "OAuth 2.0 Client ID" → "Web application".
    </p>
    <div class="form-group">
        <label for="calendarClientId">Client ID</label>
        <input type="text" id="calendarClientId" placeholder="xxxx.apps.googleusercontent.com">
    </div>
    <div class="form-group">
        <label for="calendarClientSecret">Client Secret</label>
        <input type="password" id="calendarClientSecret" placeholder="GOCSPX-...">
    </div>
    <button type="button" onclick="saveCalendarAppCredentials()" class="btn btn-secondary">
        Save Credentials
    </button>
    <div id="calendarCredentialStatus" class="status-message"></div>
</div>
```

### 2.2 Add JavaScript Functions

**File**: `web/static/js/setup.js`

```javascript
async function checkCalendarCredentialsStatus() {
    try {
        const response = await fetch('/api/v1/settings/integrations/calendar/app-credentials/status');
        const data = await response.json();

        const configSection = document.getElementById('calendarAppConfig');
        const connectBtn = document.getElementById('calendarConnectBtn');

        if (data.configured) {
            configSection.style.display = 'none';
            if (connectBtn) connectBtn.style.display = 'block';
        } else {
            configSection.style.display = 'block';
            if (connectBtn) connectBtn.style.display = 'none';
        }
    } catch (error) {
        console.error('Failed to check Calendar credentials:', error);
    }
}

async function saveCalendarAppCredentials() {
    const clientId = document.getElementById('calendarClientId').value.trim();
    const clientSecret = document.getElementById('calendarClientSecret').value.trim();
    const statusEl = document.getElementById('calendarCredentialStatus');

    if (!clientId || !clientSecret) {
        statusEl.textContent = 'Both Client ID and Client Secret are required';
        statusEl.className = 'status-message error';
        return;
    }

    try {
        const response = await fetch('/api/v1/settings/integrations/calendar/app-credentials', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ client_id: clientId, client_secret: clientSecret })
        });

        const data = await response.json();

        if (data.success) {
            statusEl.textContent = 'Credentials saved successfully!';
            statusEl.className = 'status-message success';
            await checkCalendarCredentialsStatus();
        } else {
            statusEl.textContent = data.error || 'Failed to save credentials';
            statusEl.className = 'status-message error';
        }
    } catch (error) {
        statusEl.textContent = 'Failed to save credentials: ' + error.message;
        statusEl.className = 'status-message error';
    }
}
```

### 2.3 Initialize on Page Load

Add to `initializeIntegrations()` or equivalent:
```javascript
checkCalendarCredentialsStatus();
```

### 2.4 Progressive Bookend
```bash
gh issue comment 577 -b "✓ Phase 2 Complete: Setup Wizard UI
- Credential form added to setup.html
- JavaScript functions added to setup.js
- Initialization call added
- Manual test: form shows when credentials missing"
```

---

## Phase 3: Settings Page UI (30 min)

### 3.1 Create Settings Calendar Page

**File**: `templates/settings_calendar.html` (new file, copy from settings_slack.html)

Follow the exact pattern from `templates/settings_slack.html` App Configuration card.

### 3.2 Add Route

**File**: `web/api/routes/settings.py` or equivalent

```python
@router.get("/integrations/calendar", response_class=HTMLResponse)
async def settings_calendar_page(request: Request):
    return templates.TemplateResponse("settings_calendar.html", {"request": request})
```

### 3.3 Progressive Bookend
```bash
gh issue comment 577 -b "✓ Phase 3 Complete: Settings Page UI
- templates/settings_calendar.html created
- Route added to settings.py
- Manual test: settings page loads, can update credentials"
```

---

## Phase 4: Testing (30 min)

### 4.1 Unit Tests

**File**: `tests/unit/web/api/routes/test_settings_calendar.py` (new file)

```python
class TestCalendarAppCredentials:
    @pytest.mark.asyncio
    async def test_save_credentials_stores_in_keychain(self):
        # Follow test_settings_slack.py pattern

    @pytest.mark.asyncio
    async def test_get_status_returns_configured_when_both_present(self):
        # Follow test_settings_slack.py pattern

    @pytest.mark.asyncio
    async def test_get_status_never_exposes_credentials(self):
        # Security test - credentials not in response
```

### 4.2 Run Tests
```bash
python -m pytest tests/unit/web/api/routes/test_settings_calendar.py -xvs
```

### 4.3 Manual Testing Checklist

**Scenario 1**: Fresh Setup
- [ ] Start with no Calendar credentials configured
- [ ] Go to setup wizard
- [ ] See credential form (not Connect button)
- [ ] Enter credentials, click Save
- [ ] Form hides, Connect button appears

**Scenario 2**: Settings Update
- [ ] Go to Settings → Calendar
- [ ] See App Configuration section
- [ ] Update credentials
- [ ] Success message shown

**Scenario 3**: Persistence
- [ ] Configure credentials via UI
- [ ] Restart server
- [ ] Verify status endpoint returns configured=true

### 4.4 Progressive Bookend
```bash
gh issue comment 577 -b "✓ Phase 4 Complete: Testing
- 3 unit tests created and passing
- Manual testing checklist complete
- All scenarios verified"
```

---

## Phase Z: Final Bookending & Handoff

### Z.1 Final Verification
- [ ] All acceptance criteria from issue #577 met
- [ ] Completion matrix 100%
- [ ] No regressions to existing Calendar OAuth

### Z.2 Evidence Compilation
```bash
# Run full test suite
python -m pytest tests/unit/web/api/routes/test_settings_calendar.py -xvs

# Capture evidence
# - Test output
# - curl endpoint responses
# - Screenshots of UI if needed
```

### Z.3 GitHub Final Update
```bash
gh issue edit 577 --body "[update completion matrix with evidence]"

gh issue comment 577 -b "## Status: Complete - Awaiting PM Approval

### Evidence Summary
- [x] All acceptance criteria met
- [x] Tests passing: [paste test output]
- [x] No regressions: existing Calendar OAuth still works
- [x] Documentation: code comments added

### Completion Matrix
| Component | Status | Evidence |
|-----------|--------|----------|
| POST endpoint | ✅ | curl response |
| GET status endpoint | ✅ | curl response |
| CalendarConfigService | ✅ | test output |
| Setup wizard form | ✅ | manual test |
| Settings page | ✅ | manual test |
| Unit tests | ✅ | pytest output |

### Ready for PM Review
@PM - Please review and close if satisfied."
```

### Z.4 Session Log Update
- Document any discoveries
- Note any deviations from gameplan
- Flag anything for future work

---

## Completion Matrix

| Component | Status | Evidence |
|-----------|--------|----------|
| POST /calendar/app-credentials endpoint | ⏸️ | - |
| GET /calendar/app-credentials/status endpoint | ⏸️ | - |
| CalendarConfigService keychain integration | ⏸️ | - |
| Setup wizard credential form | ⏸️ | - |
| Settings page credential section | ⏸️ | - |
| Unit tests (3+) | ⏸️ | - |
| Manual testing complete | ⏸️ | - |

---

## Files to Modify

1. `web/api/routes/settings_integrations.py` - Add endpoints + models
2. `services/integrations/calendar/config_service.py` - Add keychain fallback
3. `templates/setup.html` - Add credential form
4. `web/static/js/setup.js` - Add JS functions
5. `templates/settings_calendar.html` - Create settings page
6. `web/api/routes/settings.py` - Add route (if needed)
7. `tests/unit/web/api/routes/test_settings_calendar.py` - Create tests

---

## Reference Files (Copy Patterns From)

- `web/api/routes/settings_integrations.py` - Slack credential endpoints
- `services/integrations/slack/config_service.py` - Keychain fallback pattern
- `templates/settings_slack.html` - App Configuration card
- `tests/unit/web/api/routes/test_settings_slack.py` - Test patterns

---

## STOP Conditions

- CalendarConfigService structure differs significantly from SlackConfigService
- Existing Calendar OAuth flow breaks after changes
- KeychainService errors on new key names
- Tests fail after implementation
- Phase 0.5 contract verification fails

---

## Notes

- Google OAuth requires exact redirect URI match - include instructions in help text
- Help text should mention required scopes: `calendar.readonly`, `userinfo.email`
- The legacy `credentials.json` pattern should continue to work as fallback
- Follow #576 pattern exactly for UI/UX consistency

---

_Gameplan created: 2026-01-11_
_Template version: v9.2_
