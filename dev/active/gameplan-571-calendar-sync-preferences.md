# Gameplan: Issue #571 - Calendar Sync Preferences

**Issue**: #571 ENHANCE-SETTINGS-CALENDAR
**Created**: 2026-01-11
**Status**: Ready for Implementation
**Estimated Effort**: Medium (~2 hours)
**Template Version**: 9.3

---

## Overview

Add calendar selection preferences to the Calendar settings page, allowing users to choose which Google calendars to sync and designate a primary calendar.

**Assessment**: This is NOT a 75% pattern - requires new endpoint and UI implementation.

---

## Phase -1: Infrastructure Verification (5 min)

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Settings page: `templates/settings_calendar.html` (exists, 27KB)
- [x] Calendar endpoints: `/calendar`, `/calendar/connect`, `/calendar/app-credentials`
- [ ] Calendar list endpoint: Does NOT exist
- [ ] Preferences storage: Does NOT exist

**My understanding of the task**:
- Need to add `GET /calendar/calendars` endpoint (calls Google API)
- Need to add `POST /calendar/preferences` endpoint (saves selection)
- Need to add UI section for calendar selection

### Part A.2: Worktree Assessment

**Assessment**: **SKIP WORKTREE** - Single agent, sequential work.

### Part B: PM Verification Required

**PM, please confirm**:
- [ ] Infrastructure assumptions correct
- [ ] Scope appropriate (new feature, not 75% pattern)
- [ ] Proceed with implementation

---

## Phase 0: Investigation (10 min)

### Objective
Understand Google Calendar API and preference storage pattern.

### Investigation Tasks

1. **Google Calendar API check**:
   - Verify `calendarList.list` API availability
   - Check required OAuth scopes
   - Understand response format

2. **Preference storage pattern**:
   - Check how Slack stores channel preference (#570)
   - Determine if we use database or keychain

3. **UI pattern from #570**:
   - Review Slack channel selection UI
   - Apply same pattern for calendar selection

### Key Technical Decisions

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Preference storage | Database / Keychain / PIPER.user.md | Database (user-specific) |
| Primary calendar | Separate field / Flag in array | Separate field |
| Multi-select UI | Checkboxes / Multi-select dropdown | Checkboxes (like Slack) |

---

## Phase 0.5: Frontend-Backend Contract (5 min)

### API Contracts

**Get Calendar List**:
```
GET /api/v1/settings/integrations/calendar/calendars

Response (200):
{
  "calendars": [
    {
      "id": "primary",
      "name": "Work Calendar",
      "description": "Main work calendar",
      "primary": true,
      "selected": true
    },
    {
      "id": "personal@gmail.com",
      "name": "Personal",
      "description": "",
      "primary": false,
      "selected": false
    }
  ]
}

Response (401): { "error": "Calendar not connected" }
```

**Save Calendar Preferences**:
```
POST /api/v1/settings/integrations/calendar/preferences
Content-Type: application/json

Body:
{
  "selected_calendars": ["primary", "personal@gmail.com"],
  "primary_calendar": "primary"
}

Response (200):
{
  "success": true,
  "message": "Calendar preferences saved"
}
```

**Get Calendar Preferences**:
```
GET /api/v1/settings/integrations/calendar/preferences

Response (200):
{
  "selected_calendars": ["primary", "personal@gmail.com"],
  "primary_calendar": "primary"
}
```

---

## Phase 0.6: Data Flow & Integration Verification

### Data Flow
```
User clicks "Refresh Calendars"
  → GET /calendar/calendars
  → CalendarConfigService gets OAuth token
  → Google Calendar API calendarList.list
  → Merge with saved preferences
  → Return to UI

User saves preferences
  → POST /calendar/preferences
  → Store in database (user_preferences table? or new table?)
  → Return success
```

### Storage Decision
Need to determine storage location:
- Option A: `user_preferences` table (if exists)
- Option B: New `calendar_preferences` table
- Option C: Keychain (like credentials)

**Recommendation**: Check if `user_preferences` exists, use that. Otherwise, consider keychain for simplicity.

---

## Phase 0.7: Conversation Design

**Assessment**: **N/A** - Not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

**Assessment**: **MINIMAL** - Self-contained settings feature.

---

## Phase 1: Backend - Calendar List Endpoint (30 min)

### 1.1 Create Endpoint

**File**: `web/api/routes/settings_integrations.py`

```python
@router.get("/calendar/calendars")
async def get_calendar_list():
    """
    Get list of available Google calendars for the user.

    Returns calendar IDs, names, and current selection status.
    Issue #571: Calendar sync preferences
    """
    from services.infrastructure.keychain_service import KeychainService
    from services.integrations.calendar.calendar_service import CalendarService

    keychain = KeychainService()
    refresh_token = keychain.get_api_key("google_calendar")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Calendar not connected"
        )

    try:
        # Get calendars from Google API
        calendar_service = CalendarService()
        calendars = await calendar_service.list_calendars()

        # Merge with saved preferences
        preferences = await get_calendar_preferences_internal()

        return {
            "calendars": [
                {
                    "id": cal["id"],
                    "name": cal.get("summary", "Unnamed"),
                    "description": cal.get("description", ""),
                    "primary": cal.get("primary", False),
                    "selected": cal["id"] in preferences.get("selected_calendars", [])
                }
                for cal in calendars
            ]
        }
    except Exception as e:
        logger.error("calendar_list_error", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))
```

### 1.2 Add CalendarService.list_calendars()

**File**: `services/integrations/calendar/calendar_service.py`

Need to add method that calls Google Calendar API:
```python
async def list_calendars(self) -> List[Dict]:
    """Get list of calendars from Google Calendar API."""
    # Use calendarList.list endpoint
    # Return list of calendar objects
```

---

## Phase 2: Backend - Preferences Endpoints (30 min)

### 2.1 Save Preferences Endpoint

**File**: `web/api/routes/settings_integrations.py`

```python
class CalendarPreferencesRequest(BaseModel):
    selected_calendars: List[str]
    primary_calendar: str

@router.post("/calendar/preferences")
async def save_calendar_preferences(prefs: CalendarPreferencesRequest):
    """Save calendar sync preferences. Issue #571."""
    # Store preferences (keychain or database)
    # Return success
```

### 2.2 Get Preferences Endpoint

```python
@router.get("/calendar/preferences")
async def get_calendar_preferences():
    """Get saved calendar sync preferences. Issue #571."""
    # Load from storage
    # Return preferences
```

### 2.3 Storage Implementation

Decide on storage and implement:
- Keychain: `calendar_preferences` key with JSON value
- Database: User preferences table

---

## Phase 3: Frontend - Calendar Selection UI (45 min)

### 3.1 Add HTML Section

**File**: `templates/settings_calendar.html`

Add after OAuth status section:
```html
<!-- Calendar Selection Section (Issue #571) -->
<div class="settings-card" id="calendar-selection-card" style="display: none;">
    <h3>Calendar Selection</h3>
    <p>Choose which calendars to sync with Piper.</p>

    <div id="calendar-list-container">
        <div class="loading">Loading calendars...</div>
    </div>

    <div class="primary-calendar-section">
        <label>Primary Calendar:</label>
        <select id="primary-calendar-select">
            <!-- Populated by JS -->
        </select>
    </div>

    <div class="button-group">
        <button class="btn btn-primary" onclick="saveCalendarPreferences()">
            Save Preferences
        </button>
        <button class="btn btn-secondary" onclick="refreshCalendarList()">
            Refresh
        </button>
    </div>
</div>
```

### 3.2 Add JavaScript

```javascript
async function loadCalendarList() {
    const response = await fetch('/api/v1/settings/integrations/calendar/calendars');
    if (response.ok) {
        const data = await response.json();
        renderCalendarList(data.calendars);
    }
}

function renderCalendarList(calendars) {
    // Render checkboxes for each calendar
    // Populate primary dropdown
}

async function saveCalendarPreferences() {
    // Collect selected calendars
    // POST to /calendar/preferences
    // Show success/error toast
}
```

---

## Phase 4: Testing (20 min)

### 4.1 Unit Tests

**File**: `tests/unit/web/api/routes/test_settings_calendar_preferences.py`

```python
class TestCalendarListEndpoint:
    """Tests for GET /calendar/calendars"""

    @pytest.mark.asyncio
    async def test_returns_calendar_list_when_connected(self):
        """Should return list of calendars"""

    @pytest.mark.asyncio
    async def test_returns_401_when_not_connected(self):
        """Should return 401 if no OAuth token"""

class TestCalendarPreferencesEndpoint:
    """Tests for /calendar/preferences"""

    @pytest.mark.asyncio
    async def test_saves_preferences(self):
        """Should save calendar preferences"""

    @pytest.mark.asyncio
    async def test_loads_preferences(self):
        """Should load saved preferences"""
```

### 4.2 Run Tests
```bash
python -m pytest tests/unit/web/api/routes/test_settings_calendar_preferences.py -xvs
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
feat(#571): Add calendar sync preferences to settings

Allows users to select which Google calendars to sync and
designate a primary calendar for scheduling awareness.

Changes:
- Add GET /calendar/calendars endpoint (lists available calendars)
- Add POST/GET /calendar/preferences endpoints (save/load selection)
- Add calendar selection UI to settings page
- Add N tests for new endpoints

Issue: #571

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## STOP Conditions

Stop immediately and escalate if:
- Google Calendar API doesn't return calendar list
- OAuth token scope insufficient (need calendar.readonly)
- CalendarService doesn't exist or has different structure
- Preference storage pattern unclear
- Tests fail for any reason

---

## Risk Assessment

**Medium Risk**: New feature requiring Google API integration.

**Key Uncertainties**:
1. Does CalendarService exist with Google API access?
2. What OAuth scopes are already configured?
3. Preference storage location decision

**Mitigation**: Phase 0 investigation will clarify all uncertainties.

---

## Files to Create/Modify Summary

| File | Changes |
|------|---------|
| `web/api/routes/settings_integrations.py` | Add 3 new endpoints |
| `services/integrations/calendar/calendar_service.py` | Add list_calendars() method |
| `templates/settings_calendar.html` | Add selection UI section |
| `tests/unit/web/api/routes/test_settings_calendar_preferences.py` | New test file |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-11 | Initial gameplan (template v9.3) |

---

_Gameplan created: 2026-01-11_
_Template version: 9.3_
