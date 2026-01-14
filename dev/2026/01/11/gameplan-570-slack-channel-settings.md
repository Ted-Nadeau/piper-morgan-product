# Gameplan: Issue #570 - Slack Channel Selection Settings

**Date**: 2026-01-11
**Issue**: #570
**Template Version**: v9.3
**Status**: Ready for Implementation
**Estimated Effort**: Medium (~3 hours)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Slack settings page exists: `templates/settings_slack.html` (connect/disconnect only)
- [x] Slack client has `list_channels()`: `services/integrations/slack/slack_client.py:226`
- [x] OAuth has `channels:read` scope: `services/integrations/slack/oauth_handler.py:89`
- [x] No preferences endpoints exist yet
- [x] No user-level integration settings table exists (but `ProjectIntegrationDB` pattern available)

**My understanding of the task**:
- Add 3 API endpoints for Slack preferences (channels list, get prefs, save prefs)
- Add UI to existing `settings_slack.html` for channel selection
- Store preferences in new `user_integration_settings` table or similar

### Part A.2: Work Characteristics Assessment

**Assessment**:
- [x] **SKIP WORKTREE** - Single agent, medium effort, sequential phases

### Part B: PM Verification Required

**PM, please confirm**:
1. [x] New table for user integration settings is acceptable
2. [x] `list_channels()` method already exists in Slack client
3. [ ] Any critical context I'm missing?

### Part C: Proceed/Revise Decision
- [ ] **PROCEED** - Understanding correct
- [ ] **REVISE** - Assumptions wrong
- [ ] **CLARIFY** - Need more context

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

1. **GitHub Issue Verification**: ✅ #570 exists, template-compliant

2. **Codebase Investigation**:
   ```bash
   # Verified:
   # - settings_slack.html exists (connect/disconnect UI)
   # - slack_client.list_channels() exists
   # - channels:read scope in OAuth
   # - No preferences endpoints yet
   ```

3. **Update GitHub Issue** (progressive bookending):
   ```bash
   gh issue comment 570 -b "## Status: Implementation Starting
   - [x] Gameplan approved
   - [x] Infrastructure verified
   - [ ] Phase 1: Backend API
   - [ ] Phase 2: Frontend UI
   - [ ] Phase 3: Testing"
   ```

---

## Phase 0.5: Frontend-Backend Contract Verification

### Existing Endpoints (verified)
| Endpoint | Path | Status |
|----------|------|--------|
| Connect Slack | GET /api/v1/settings/integrations/slack/connect | ✅ Exists |
| Disconnect Slack | POST /api/v1/settings/integrations/slack/disconnect | ✅ Exists |

### New Endpoints (to create)
| Endpoint | Path | Purpose |
|----------|------|---------|
| List Channels | GET /api/v1/settings/integrations/slack/channels | Fetch available Slack channels |
| Get Preferences | GET /api/v1/settings/integrations/slack/preferences | Load saved preferences |
| Save Preferences | POST /api/v1/settings/integrations/slack/preferences | Save preferences |

---

## Phase 1: Backend Implementation (1.5 hours)

### Objective
Create API endpoints for channel listing and preferences management.

### 1.1 Database Model (if needed)

**Option A**: Add to existing `user_api_keys` or users table (simpler)
**Option B**: Create new `user_integration_settings` table (cleaner)

**Decision**: Use Option A - store as JSON in a new column or use existing pattern.

Actually, let's check if we can store in the OAuth token metadata or create minimal storage:

```python
# Store in user_api_keys.metadata or create simple key-value:
# Key: f"slack_preferences:{user_id}"
# Value: JSON {"notification_channel": "C123", "monitored_channels": ["C123", "C456"]}
```

**Simplest approach**: Store preferences in the Slack token record or a simple JSONB column.

### 1.2 API Endpoints

**File**: `web/api/routes/settings_integrations.py`

```python
@router.get("/slack/channels")
async def get_slack_channels(current_user: JWTClaims = Depends(get_current_user)):
    """Fetch available Slack channels for the user."""
    # Use existing slack_client.list_channels()
    # Return simplified channel list: [{id, name, is_private}]

@router.get("/slack/preferences")
async def get_slack_preferences(current_user: JWTClaims = Depends(get_current_user)):
    """Get saved Slack preferences."""
    # Load from storage
    # Return: {notification_channel, monitored_channels, default_response_channel}

@router.post("/slack/preferences")
async def save_slack_preferences(
    preferences: SlackPreferencesRequest,
    current_user: JWTClaims = Depends(get_current_user)
):
    """Save Slack preferences."""
    # Validate channel IDs exist
    # Save to storage
    # Return success
```

### 1.3 Request/Response Models

```python
class SlackChannel(BaseModel):
    id: str
    name: str
    is_private: bool = False

class SlackChannelsResponse(BaseModel):
    channels: List[SlackChannel]

class SlackPreferencesRequest(BaseModel):
    notification_channel: Optional[str] = None
    monitored_channels: List[str] = []
    default_response_channel: Optional[str] = None

class SlackPreferencesResponse(BaseModel):
    notification_channel: Optional[str] = None
    monitored_channels: List[str] = []
    default_response_channel: Optional[str] = None
```

### Tasks
- [ ] Add `SlackChannel`, `SlackPreferencesRequest`, `SlackPreferencesResponse` models
- [ ] Add `GET /slack/channels` endpoint
- [ ] Add `GET /slack/preferences` endpoint
- [ ] Add `POST /slack/preferences` endpoint
- [ ] Decide on storage mechanism (simplest: JSON file or Redis, or DB column)

### Deliverables
- 3 new API endpoints working
- Channel list returns from Slack API

### Progressive Bookending
```bash
gh issue comment 570 -b "✓ Phase 1 Complete: Backend API
- GET /slack/channels returns channel list
- GET /slack/preferences returns saved prefs
- POST /slack/preferences saves prefs
- Storage: [mechanism chosen]"
```

---

## Phase 2: Frontend Implementation (1 hour)

### Objective
Add channel selection UI to existing Slack settings page.

### 2.1 UI Components to Add

After the existing connect/disconnect section, add:

```html
<!-- Channel Settings (only shown when connected) -->
<div class="settings-card" id="channel-settings" style="display: none;">
  <h3>Channel Settings</h3>

  <!-- Notification Channel -->
  <div class="form-group">
    <label>Notification Channel</label>
    <select id="notification-channel">
      <option value="">Select channel...</option>
    </select>
    <p class="help-text">Where Piper sends notifications</p>
  </div>

  <!-- Monitored Channels -->
  <div class="form-group">
    <label>Monitored Channels</label>
    <div id="monitored-channels-list">
      <!-- Checkboxes populated dynamically -->
    </div>
    <p class="help-text">Channels Piper listens for mentions</p>
  </div>

  <!-- Default Response Channel -->
  <div class="form-group">
    <label>Default Response Channel</label>
    <select id="default-response-channel">
      <option value="">Select channel...</option>
    </select>
    <p class="help-text">Where Piper responds by default</p>
  </div>

  <!-- Save Button -->
  <button class="btn btn-primary" onclick="saveSlackPreferences()">
    Save Settings
  </button>
</div>
```

### 2.2 JavaScript Functions

```javascript
// Load channels and preferences when connected
async function loadChannelSettings() {
  // Fetch channels
  const channelsRes = await fetch('/api/v1/settings/integrations/slack/channels');
  const channels = await channelsRes.json();

  // Fetch preferences
  const prefsRes = await fetch('/api/v1/settings/integrations/slack/preferences');
  const prefs = await prefsRes.json();

  // Populate dropdowns and checkboxes
  populateChannelDropdowns(channels.channels);
  populateMonitoredCheckboxes(channels.channels, prefs.monitored_channels);

  // Set selected values
  setSelectedPreferences(prefs);

  // Show settings section
  document.getElementById('channel-settings').style.display = 'block';
}

async function saveSlackPreferences() {
  const prefs = {
    notification_channel: document.getElementById('notification-channel').value,
    monitored_channels: getSelectedMonitoredChannels(),
    default_response_channel: document.getElementById('default-response-channel').value
  };

  const res = await fetch('/api/v1/settings/integrations/slack/preferences', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(prefs)
  });

  if (res.ok) {
    showToast('success', 'Slack settings saved', 'Settings Saved');
  } else {
    showToast('error', 'Failed to save settings', 'Error');
  }
}
```

### Tasks
- [ ] Add CSS for settings card and form groups
- [ ] Add HTML for channel settings section
- [ ] Add `loadChannelSettings()` function
- [ ] Add `saveSlackPreferences()` function
- [ ] Add helper functions (populate dropdowns, get selections)
- [ ] Call `loadChannelSettings()` when Slack is connected

### Deliverables
- Channel settings UI visible when Slack connected
- Dropdowns populated with channels
- Save button works

### Progressive Bookending
```bash
gh issue comment 570 -b "✓ Phase 2 Complete: Frontend UI
- Channel settings section added
- Dropdowns populate with Slack channels
- Checkboxes for monitored channels
- Save button with toast feedback"
```

---

## Phase 3: Testing & Polish (30 min)

### Manual Testing Checklist

**Scenario 1**: Fresh setup
1. [ ] Connect Slack integration
2. [ ] Verify channel settings section appears
3. [ ] Verify dropdowns populated with channels
4. [ ] Select channels and save
5. [ ] Verify success toast

**Scenario 2**: Load existing preferences
1. [ ] Refresh page
2. [ ] Verify saved selections persist
3. [ ] Verify checkboxes reflect saved state

**Scenario 3**: Disconnected state
1. [ ] Disconnect Slack
2. [ ] Verify channel settings hidden
3. [ ] Reconnect and verify settings reload

### Regression Tests
- [ ] Connect/disconnect still works
- [ ] Integration health page still works
- [ ] No console errors

### Progressive Bookending
```bash
gh issue comment 570 -b "✓ Phase 3 Complete: Testing
- All scenarios pass
- No regressions
- Ready for PM review"
```

---

## Phase Z: Final Bookending & Handoff

### Evidence Required
- [ ] Screenshot: Channel settings UI
- [ ] Screenshot: Populated dropdowns
- [ ] Screenshot: Save success toast
- [ ] API response: `/slack/channels` sample
- [ ] API response: `/slack/preferences` after save

### Completion Matrix Update
Update GitHub issue with all checkmarks and evidence.

---

## Completion Matrix

| Criterion | Status | Evidence |
|-----------|--------|----------|
| GET /slack/channels endpoint | ❌ | - |
| GET /slack/preferences endpoint | ❌ | - |
| POST /slack/preferences endpoint | ❌ | - |
| Storage mechanism | ❌ | - |
| Channel settings HTML | ❌ | - |
| Notification dropdown | ❌ | - |
| Monitored checkboxes | ❌ | - |
| Default response dropdown | ❌ | - |
| Save button | ❌ | - |
| Load existing prefs | ❌ | - |
| Manual tests pass | ❌ | - |
| No regressions | ❌ | - |

---

## STOP Conditions

- Slack OAuth token doesn't have `channels:read` scope → Check before proceeding
- `list_channels()` returns error → Debug Slack API issue
- Storage mechanism unclear → Simplify to file/Redis before adding DB table
- Existing settings page structure incompatible → Escalate

---

## Design Decision: Storage Mechanism

**Options**:
1. **Simple file/Redis**: Fast but not persistent across deploys
2. **New DB table**: Clean but requires migration
3. **Add column to existing table**: Quick but less clean
4. **Store in Slack token metadata**: If structure allows

**Recommendation**: Start with option 3 (add JSONB column to `user_api_keys` table for `integration_preferences`) or create simple `user_integration_preferences` table.

**PM Decision**: Which storage approach do you prefer?

---

## Notes

- Existing `slack_client.list_channels()` should work out of the box
- OAuth already requests `channels:read` scope
- Settings page exists, just needs channel section added
- Follow patterns from `integrations.html` for consistency

---

*Gameplan created: 2026-01-11 09:35*
