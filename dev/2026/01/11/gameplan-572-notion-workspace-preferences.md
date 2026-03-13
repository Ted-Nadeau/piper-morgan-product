# Gameplan: Issue #572 - Notion Workspace Preferences

**Issue**: #572 ENHANCE-SETTINGS-NOTION
**Created**: 2026-01-11
**Status**: IMPLEMENTED
**Estimated Effort**: Medium (~2 hours)
**Actual Effort**: ~45 min
**Template Version**: 9.3

---

## Overview

Add Notion database selection preferences to the Notion settings page, allowing users to choose which databases Piper can access and designate a default database for task creation.

**Assessment**: Follows 95% pattern from #571 (Calendar sync preferences) - same architecture.

---

## Phase -1: Infrastructure Verification (5 min)

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Settings page: `templates/settings_notion.html` (exists)
- [x] Notion API key integration: #579 (complete)
- [ ] Database list endpoint: Does NOT exist
- [ ] Preferences storage: Does NOT exist (will use file-based like #571)

**My understanding of the task**:
- Need to add `GET /notion/databases` endpoint (calls Notion API search)
- Need to add `POST /notion/preferences` endpoint (saves selection)
- Need to add `GET /notion/preferences` endpoint (loads selection)
- Need to add UI section for database selection

### Part A.2: Worktree Assessment

**Assessment**: **SKIP WORKTREE** - Single agent, sequential work.

### Part B: PM Verification Required

**PM, please confirm**:
- [ ] Infrastructure assumptions correct
- [ ] Scope appropriate (follows #571 pattern)
- [ ] Proceed with implementation

---

## Phase 0: Investigation (10 min)

### Objective
Verify Notion API capabilities and confirm pattern from #571.

### Investigation Tasks

1. **Notion API check**:
   - Verify `search` endpoint with `filter: {property: "object", value: "database"}`
   - Check required API permissions
   - Understand response format

2. **Preference storage pattern**:
   - Confirm file-based storage at `data/notion_preferences.json`
   - Same pattern as Slack (#570) and Calendar (#571)

3. **Settings page review**:
   - Check `templates/settings_notion.html` structure
   - Identify where to add database selection UI

### Key Technical Decisions

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Preference storage | Database / File-based | File-based (same as #571) |
| Default database | Separate field / Flag in array | Separate field |
| Multi-select UI | Checkboxes / Multi-select dropdown | Checkboxes (like #571) |

---

## Phase 0.5: Frontend-Backend Contract (5 min)

### API Contracts

**Get Database List**:
```
GET /api/v1/settings/integrations/notion/databases

Response (200):
{
  "databases": [
    {
      "id": "abc123",
      "name": "Work Tasks",
      "description": "Team task tracker",
      "selected": true
    },
    {
      "id": "def456",
      "name": "Project Notes",
      "description": "",
      "selected": false
    }
  ]
}

Response (401): { "error": "Notion not connected" }
```

**Save Notion Preferences**:
```
POST /api/v1/settings/integrations/notion/preferences
Content-Type: application/json

Body:
{
  "selected_databases": ["abc123", "def456"],
  "default_database": "abc123"
}

Response (200):
{
  "success": true,
  "message": "Notion preferences saved"
}
```

**Get Notion Preferences**:
```
GET /api/v1/settings/integrations/notion/preferences

Response (200):
{
  "selected_databases": ["abc123", "def456"],
  "default_database": "abc123"
}
```

---

## Phase 0.6: Data Flow & Integration Verification

### Data Flow
```
User clicks "Refresh Databases"
  → GET /notion/databases
  → NotionConfigService gets API key
  → Notion API search (filter: database)
  → Merge with saved preferences
  → Return to UI

User saves preferences
  → POST /notion/preferences
  → Store in file (data/notion_preferences.json)
  → Return success
```

---

## Phase 0.7: Conversation Design

**Assessment**: **N/A** - Not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

**Assessment**: **MINIMAL** - Self-contained settings feature.

---

## Phase 1: Backend - Database List Endpoint (30 min)

### 1.1 Add Pydantic Models

**File**: `web/api/routes/settings_integrations.py`

```python
# After Calendar models section

# ============================================================================
# Pydantic Models for Notion Workspace Preferences (Issue #572)
# ============================================================================

class NotionDatabaseInfo(BaseModel):
    """Notion database representation."""
    id: str
    name: str
    description: str = ""
    selected: bool = False

class NotionDatabaseListResponse(BaseModel):
    """Response containing list of Notion databases."""
    databases: List[NotionDatabaseInfo]

class NotionPreferencesRequest(BaseModel):
    """Request body for saving Notion preferences."""
    selected_databases: List[str]
    default_database: str

class NotionPreferencesResponse(BaseModel):
    """Response containing Notion preferences."""
    selected_databases: List[str] = []
    default_database: Optional[str] = None
```

### 1.2 Add File Storage Helpers

```python
# Simple file-based storage for Notion preferences (Issue #572)
NOTION_PREFERENCES_FILE = "data/notion_preferences.json"

def _load_notion_preferences() -> dict:
    """Load all Notion preferences from file."""
    try:
        if os.path.exists(NOTION_PREFERENCES_FILE):
            with open(NOTION_PREFERENCES_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.warning("notion_preferences_load_failed", error=str(e))
    return {}

def _save_notion_preferences(prefs: dict) -> None:
    """Save all Notion preferences to file."""
    try:
        os.makedirs(os.path.dirname(NOTION_PREFERENCES_FILE), exist_ok=True)
        with open(NOTION_PREFERENCES_FILE, "w") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        logger.error("notion_preferences_save_failed", error=str(e))
```

### 1.3 Create Database List Endpoint

```python
@router.get("/notion/databases", response_model=NotionDatabaseListResponse)
async def get_notion_databases(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get list of available Notion databases for the user.

    Returns database IDs, names, and current selection status.
    Requires a connected Notion account.
    Issue #572: Notion workspace preferences
    """
    import aiohttp
    from services.integrations.notion.config_service import NotionConfigService

    try:
        config_service = NotionConfigService()
        config = config_service.get_config()
        api_key = config.api_key

        if not api_key:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Notion not connected. Please add your API key first.",
            )

        # Fetch databases from Notion API
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.notion.com/v1/search",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                json={
                    "filter": {"property": "object", "value": "database"}
                },
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error("notion_database_list_failed", status=response.status, error=error_text)
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Failed to fetch databases from Notion: {response.status}",
                    )

                data = await response.json()

        # Load user's saved preferences
        all_prefs = _load_notion_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})
        selected_databases = user_prefs.get("selected_databases", [])

        # Build database list with selection status
        databases = []
        for db in data.get("results", []):
            db_id = db.get("id", "")
            # Get title from title property
            title_prop = db.get("title", [])
            name = title_prop[0].get("plain_text", "Unnamed Database") if title_prop else "Unnamed Database"
            # Get description if available
            description = db.get("description", [])
            desc_text = description[0].get("plain_text", "") if description else ""

            databases.append(
                NotionDatabaseInfo(
                    id=db_id,
                    name=name,
                    description=desc_text,
                    selected=db_id in selected_databases if selected_databases else False,
                )
            )

        logger.info("notion_databases_fetched", count=len(databases), user_id=str(current_user.sub))

        return NotionDatabaseListResponse(databases=databases)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("notion_database_list_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch database list: {str(e)}",
        )
```

---

## Phase 2: Backend - Preferences Endpoints (20 min)

### 2.1 Get Preferences Endpoint

```python
@router.get("/notion/preferences", response_model=NotionPreferencesResponse)
async def get_notion_preferences(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get saved Notion preferences for the current user.

    Returns selected databases and default database designation.
    Issue #572: Notion workspace preferences
    """
    try:
        all_prefs = _load_notion_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})

        logger.info("notion_preferences_loaded", user_id=str(current_user.sub))

        return NotionPreferencesResponse(
            selected_databases=user_prefs.get("selected_databases", []),
            default_database=user_prefs.get("default_database"),
        )

    except Exception as e:
        logger.error("notion_preferences_load_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load Notion preferences: {str(e)}",
        )
```

### 2.2 Save Preferences Endpoint

```python
@router.post("/notion/preferences", response_model=NotionPreferencesResponse)
async def save_notion_preferences(
    preferences: NotionPreferencesRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save Notion preferences for the current user.

    Stores selected databases and default database designation.
    Issue #572: Notion workspace preferences
    """
    try:
        all_prefs = _load_notion_preferences()

        # Store preferences for this user
        user_prefs = {
            "selected_databases": preferences.selected_databases,
            "default_database": preferences.default_database,
        }

        all_prefs[str(current_user.sub)] = user_prefs
        _save_notion_preferences(all_prefs)

        logger.info(
            "notion_preferences_saved",
            user_id=str(current_user.sub),
            selected_count=len(preferences.selected_databases),
            default_database=preferences.default_database,
        )

        return NotionPreferencesResponse(
            selected_databases=preferences.selected_databases,
            default_database=preferences.default_database,
        )

    except Exception as e:
        logger.error("notion_preferences_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save Notion preferences: {str(e)}",
        )
```

---

## Phase 3: Frontend - Database Selection UI (45 min)

### 3.1 Add CSS

**File**: `templates/settings_notion.html`

Add CSS for database selection (same pattern as #571 calendar selection).

### 3.2 Add HTML Section

Add after API key configuration section:

```html
<!-- Database Selection Card (Issue #572) -->
<div class="database-selection-card" id="database-selection-card" style="display: none;">
    <h3>📚 Database Selection</h3>
    <p class="description">
        Choose which Notion databases Piper can access. Selected databases will be used for task creation and notes.
    </p>

    <div class="database-list" id="database-list">
        <div class="database-list-loading">
            <span class="loading-spinner"></span> Loading databases...
        </div>
    </div>

    <div class="default-database-section">
        <label for="default-database-select">Default Database:</label>
        <select id="default-database-select">
            <option value="">Select a default database...</option>
        </select>
    </div>

    <div class="database-selection-buttons">
        <button class="btn btn-primary" onclick="saveNotionPreferences()">
            Save Preferences
        </button>
        <button class="btn btn-secondary" onclick="refreshDatabaseList()">
            Refresh List
        </button>
    </div>
</div>
```

### 3.3 Add JavaScript

Add functions for database list handling (mirror #571 pattern).

---

## Phase 4: Testing (20 min)

### 4.1 Unit Tests

**File**: `tests/unit/web/api/routes/test_settings_notion_preferences.py`

```python
class TestGetNotionDatabases:
    """Tests for GET /api/v1/settings/integrations/notion/databases"""

    @pytest.mark.asyncio
    async def test_returns_401_when_not_connected(self):
        """Should return 401 when no API key configured"""

    @pytest.mark.asyncio
    async def test_returns_database_list_when_connected(self):
        """Should return list of databases when connected"""

class TestGetNotionPreferences:
    """Tests for GET /api/v1/settings/integrations/notion/preferences"""

    @pytest.mark.asyncio
    async def test_returns_empty_preferences_when_not_saved(self):
        """Should return empty preferences when user has no saved preferences"""

    @pytest.mark.asyncio
    async def test_returns_saved_preferences(self):
        """Should return saved preferences for the user"""

class TestSaveNotionPreferences:
    """Tests for POST /api/v1/settings/integrations/notion/preferences"""

    @pytest.mark.asyncio
    async def test_saves_preferences_successfully(self):
        """Should save preferences and return them"""

    @pytest.mark.asyncio
    async def test_preserves_other_users_preferences(self):
        """Should not affect other users' preferences"""
```

### 4.2 Run Tests
```bash
python -m pytest tests/unit/web/api/routes/test_settings_notion_preferences.py -xvs
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
feat(#572): Add Notion workspace preferences to settings

Allows users to select which Notion databases Piper can access
and designate a default database for task creation.

Changes:
- Add GET /notion/databases endpoint (lists available databases)
- Add POST/GET /notion/preferences endpoints (save/load selection)
- Add database selection UI to settings page
- Add N tests for new endpoints

Same pattern as #571 (Calendar) and #570 (Slack).

Issue: #572

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## STOP Conditions

Stop immediately and escalate if:
- Notion API doesn't return database list via search endpoint
- API key scope insufficient for database listing
- NotionConfigService doesn't exist or has different structure
- Settings page template doesn't exist or is incompatible
- Tests fail for any reason

---

## Risk Assessment

**Low Risk**: Nearly identical pattern to #571 (Calendar sync preferences).

**Key Differences from #571**:
- Notion uses API key (not OAuth refresh token)
- Notion API endpoint is `search` with filter (not `calendarList`)
- Response structure differs (title array vs summary string)

---

## Files to Create/Modify Summary

| File | Changes |
|------|---------|
| `web/api/routes/settings_integrations.py` | Add 3 new endpoints + models + file helpers |
| `templates/settings_notion.html` | Add database selection UI section |
| `tests/unit/web/api/routes/test_settings_notion_preferences.py` | New test file |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-11 | Initial gameplan (template v9.3) |

---

_Gameplan created: 2026-01-11_
_Template version: 9.3_
