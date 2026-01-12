# Gameplan: Issue #573 - GitHub Repository Preferences

**Issue**: #573 ENHANCE-SETTINGS-GITHUB
**Created**: 2026-01-11
**Status**: Ready for Implementation
**Estimated Effort**: Medium (~45 min)
**Template Version**: 9.3

---

## Overview

Add GitHub repository selection preferences to the GitHub settings page, allowing users to choose which repositories Piper can access and designate a default repository.

**Assessment**: Follows 95% pattern from #572 (Notion workspace preferences) - same architecture.

---

## Phase -1: Infrastructure Verification (5 min)

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI
- [x] Settings page: `templates/settings_github.html` (exists)
- [x] GitHub token integration: PAT-based (via keychain)
- [ ] Repository list endpoint: Does NOT exist
- [ ] Preferences storage: Does NOT exist (will use file-based like #572)

**My understanding of the task**:
- Need to add `GET /github/repositories` endpoint (calls GitHub API)
- Need to add `POST /github/preferences` endpoint (saves selection)
- Need to add `GET /github/preferences` endpoint (loads selection)
- Need to add UI section for repository selection

### Part A.2: Worktree Assessment

**Assessment**: **SKIP WORKTREE** - Single agent, sequential work.

### Part B: PM Verification Required

**PM, please confirm**:
- [ ] Infrastructure assumptions correct
- [ ] Scope appropriate (follows #572 pattern)
- [ ] Proceed with implementation

---

## Phase 0: Investigation (10 min)

### Objective
Verify GitHub API capabilities and confirm pattern from #572.

### Investigation Tasks

1. **GitHub API check**:
   - Verify `/user/repos` endpoint for listing repositories
   - Check required token scopes (repo or public_repo)
   - Understand response format

2. **Preference storage pattern**:
   - Confirm file-based storage at `data/github_preferences.json`
   - Same pattern as Notion (#572), Calendar (#571), Slack (#570)

3. **Settings page review**:
   - Check `templates/settings_github.html` structure
   - Identify where to add repository selection UI

### Key Technical Decisions

| Decision | Options | Recommendation |
|----------|---------|----------------|
| Preference storage | Database / File-based | File-based (same as #572) |
| Default repository | Separate field / Flag in array | Separate field |
| Multi-select UI | Checkboxes / Multi-select dropdown | Checkboxes (like #572) |

---

## Phase 0.5: Frontend-Backend Contract (5 min)

### API Contracts

**Get Repository List**:
```
GET /api/v1/settings/integrations/github/repositories

Response (200):
{
  "repositories": [
    {
      "id": 123456789,
      "name": "piper-morgan-product",
      "full_name": "mediajunkie/piper-morgan-product",
      "description": "Piper Morgan AI Assistant",
      "selected": true
    },
    {
      "id": 987654321,
      "name": "other-project",
      "full_name": "mediajunkie/other-project",
      "description": "",
      "selected": false
    }
  ]
}

Response (401): { "error": "GitHub not connected" }
```

**Save GitHub Preferences**:
```
POST /api/v1/settings/integrations/github/preferences
Content-Type: application/json

Body:
{
  "selected_repositories": ["mediajunkie/piper-morgan-product", "mediajunkie/other-project"],
  "default_repository": "mediajunkie/piper-morgan-product"
}

Response (200):
{
  "selected_repositories": ["mediajunkie/piper-morgan-product", "mediajunkie/other-project"],
  "default_repository": "mediajunkie/piper-morgan-product"
}
```

**Get GitHub Preferences**:
```
GET /api/v1/settings/integrations/github/preferences

Response (200):
{
  "selected_repositories": ["mediajunkie/piper-morgan-product", "mediajunkie/other-project"],
  "default_repository": "mediajunkie/piper-morgan-product"
}
```

---

## Phase 0.6: Data Flow & Integration Verification

### Data Flow
```
User clicks "Refresh Repositories"
  → GET /github/repositories
  → KeychainService gets GitHub token
  → GitHub API /user/repos
  → Merge with saved preferences
  → Return to UI

User saves preferences
  → POST /github/preferences
  → Store in file (data/github_preferences.json)
  → Return success
```

---

## Phase 0.7: Conversation Design

**Assessment**: **N/A** - Not a conversational feature.

---

## Phase 0.8: Post-Completion Integration

**Assessment**: **MINIMAL** - Self-contained settings feature.

---

## Phase 1: Backend - Repository List Endpoint (30 min)

### 1.1 Add Pydantic Models

**File**: `web/api/routes/settings_integrations.py`

```python
# After Notion models section

# ============================================================================
# Pydantic Models for GitHub Repository Preferences (Issue #573)
# ============================================================================

class GitHubRepositoryInfo(BaseModel):
    """GitHub repository representation."""
    id: int
    name: str
    full_name: str
    description: str = ""
    selected: bool = False

class GitHubRepositoryListResponse(BaseModel):
    """Response containing list of GitHub repositories."""
    repositories: List[GitHubRepositoryInfo]

class GitHubPreferencesRequest(BaseModel):
    """Request body for saving GitHub preferences."""
    selected_repositories: List[str]  # full_name format
    default_repository: str

class GitHubPreferencesResponse(BaseModel):
    """Response containing GitHub preferences."""
    selected_repositories: List[str] = []
    default_repository: Optional[str] = None
```

### 1.2 Add File Storage Helpers

```python
# Simple file-based storage for GitHub preferences (Issue #573)
GITHUB_PREFERENCES_FILE = "data/github_preferences.json"

def _load_github_preferences() -> dict:
    """Load all GitHub preferences from file."""
    try:
        if os.path.exists(GITHUB_PREFERENCES_FILE):
            with open(GITHUB_PREFERENCES_FILE, "r") as f:
                return json.load(f)
    except Exception as e:
        logger.warning("github_preferences_load_failed", error=str(e))
    return {}

def _save_github_preferences(prefs: dict) -> None:
    """Save all GitHub preferences to file."""
    try:
        os.makedirs(os.path.dirname(GITHUB_PREFERENCES_FILE), exist_ok=True)
        with open(GITHUB_PREFERENCES_FILE, "w") as f:
            json.dump(prefs, f, indent=2)
    except Exception as e:
        logger.error("github_preferences_save_failed", error=str(e))
```

### 1.3 Create Repository List Endpoint

```python
@router.get("/github/repositories", response_model=GitHubRepositoryListResponse)
async def get_github_repositories(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get list of accessible GitHub repositories for the user.

    Returns repository IDs, names, and current selection status.
    Requires a connected GitHub account.
    Issue #573: GitHub repository preferences
    """
    import aiohttp
    from services.infrastructure.keychain_service import KeychainService

    try:
        keychain = KeychainService()
        token = keychain.get_api_key("github")

        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="GitHub not connected. Please add your token first.",
            )

        # Fetch repositories from GitHub API
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://api.github.com/user/repos",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/vnd.github.v3+json",
                    "X-GitHub-Api-Version": "2022-11-28",
                },
                params={"per_page": 100, "sort": "updated"},
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error("github_repository_list_failed", status=response.status, error=error_text)
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Failed to fetch repositories from GitHub: {response.status}",
                    )

                data = await response.json()

        # Load user's saved preferences
        all_prefs = _load_github_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})
        selected_repos = user_prefs.get("selected_repositories", [])

        # Build repository list with selection status
        repositories = []
        for repo in data:
            full_name = repo.get("full_name", "")
            repositories.append(
                GitHubRepositoryInfo(
                    id=repo.get("id", 0),
                    name=repo.get("name", ""),
                    full_name=full_name,
                    description=repo.get("description") or "",
                    selected=full_name in selected_repos if selected_repos else False,
                )
            )

        logger.info(
            "github_repositories_fetched", count=len(repositories), user_id=str(current_user.sub)
        )

        return GitHubRepositoryListResponse(repositories=repositories)

    except HTTPException:
        raise
    except Exception as e:
        logger.error("github_repository_list_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch repository list: {str(e)}",
        )
```

---

## Phase 2: Backend - Preferences Endpoints (20 min)

### 2.1 Get Preferences Endpoint

```python
@router.get("/github/preferences", response_model=GitHubPreferencesResponse)
async def get_github_preferences(current_user: JWTClaims = Depends(get_current_user)):
    """
    Get saved GitHub preferences for the current user.

    Returns selected repositories and default repository designation.
    Issue #573: GitHub repository preferences
    """
    try:
        all_prefs = _load_github_preferences()
        user_prefs = all_prefs.get(str(current_user.sub), {})

        logger.info("github_preferences_loaded", user_id=str(current_user.sub))

        return GitHubPreferencesResponse(
            selected_repositories=user_prefs.get("selected_repositories", []),
            default_repository=user_prefs.get("default_repository"),
        )

    except Exception as e:
        logger.error("github_preferences_load_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to load GitHub preferences: {str(e)}",
        )
```

### 2.2 Save Preferences Endpoint

```python
@router.post("/github/preferences", response_model=GitHubPreferencesResponse)
async def save_github_preferences(
    preferences: GitHubPreferencesRequest,
    current_user: JWTClaims = Depends(get_current_user),
):
    """
    Save GitHub preferences for the current user.

    Stores selected repositories and default repository designation.
    Issue #573: GitHub repository preferences
    """
    try:
        all_prefs = _load_github_preferences()

        # Store preferences for this user
        user_prefs = {
            "selected_repositories": preferences.selected_repositories,
            "default_repository": preferences.default_repository,
        }

        all_prefs[str(current_user.sub)] = user_prefs
        _save_github_preferences(all_prefs)

        logger.info(
            "github_preferences_saved",
            user_id=str(current_user.sub),
            selected_count=len(preferences.selected_repositories),
            default_repository=preferences.default_repository,
        )

        return GitHubPreferencesResponse(
            selected_repositories=preferences.selected_repositories,
            default_repository=preferences.default_repository,
        )

    except Exception as e:
        logger.error("github_preferences_save_error", error=str(e), exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save GitHub preferences: {str(e)}",
        )
```

---

## Phase 3: Frontend - Repository Selection UI (45 min)

### 3.1 Add CSS

**File**: `templates/settings_github.html`

Add CSS for repository selection (same pattern as #572 database selection).

### 3.2 Add HTML Section

Add after token configuration section:

```html
<!-- Repository Selection Card (Issue #573) -->
<div class="repository-selection-card" id="repository-selection-card" style="display: none;">
    <h3>📦 Repository Selection</h3>
    <p class="description">
        Choose which GitHub repositories Piper can access. Selected repositories will be used for issue tracking and code reference.
    </p>

    <div class="repository-list" id="repository-list">
        <div class="repository-list-loading">
            <span class="loading-spinner"></span> Loading repositories...
        </div>
    </div>

    <div class="default-repository-section">
        <label for="default-repository-select">Default Repository:</label>
        <select id="default-repository-select">
            <option value="">Select a default repository...</option>
        </select>
    </div>

    <div class="repository-selection-buttons">
        <button class="btn btn-primary" onclick="saveGitHubPreferences()">
            Save Preferences
        </button>
        <button class="btn btn-secondary" onclick="refreshRepositoryList()">
            Refresh List
        </button>
    </div>
</div>
```

### 3.3 Add JavaScript

Add functions for repository list handling (mirror #572 pattern).

---

## Phase 4: Testing (20 min)

### 4.1 Unit Tests

**File**: `tests/unit/web/api/routes/test_settings_github_preferences.py`

```python
class TestGetGitHubRepositories:
    """Tests for GET /api/v1/settings/integrations/github/repositories"""

    @pytest.mark.asyncio
    async def test_returns_401_when_not_connected(self):
        """Should return 401 when no token configured"""

    @pytest.mark.asyncio
    async def test_returns_repository_list_when_connected(self):
        """Should return list of repositories when connected"""

class TestGetGitHubPreferences:
    """Tests for GET /api/v1/settings/integrations/github/preferences"""

    @pytest.mark.asyncio
    async def test_returns_empty_preferences_when_not_saved(self):
        """Should return empty preferences when user has no saved preferences"""

    @pytest.mark.asyncio
    async def test_returns_saved_preferences(self):
        """Should return saved preferences for the user"""

class TestSaveGitHubPreferences:
    """Tests for POST /api/v1/settings/integrations/github/preferences"""

    @pytest.mark.asyncio
    async def test_saves_preferences_successfully(self):
        """Should save preferences and return them"""

    @pytest.mark.asyncio
    async def test_preserves_other_users_preferences(self):
        """Should not affect other users' preferences"""
```

### 4.2 Run Tests
```bash
python -m pytest tests/unit/web/api/routes/test_settings_github_preferences.py -xvs
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
feat(#573): Add GitHub repository preferences to settings

Allows users to select which GitHub repositories Piper can access
and designate a default repository for issue tracking.

Changes:
- Add GET /github/repositories endpoint (lists accessible repositories)
- Add POST/GET /github/preferences endpoints (save/load selection)
- Add repository selection UI to settings page
- Add N tests for new endpoints

Same pattern as #572 (Notion), #571 (Calendar), and #570 (Slack).

Issue: #573

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

---

## STOP Conditions

Stop immediately and escalate if:
- GitHub API doesn't return repository list
- Token scope insufficient for repository listing
- Settings page template doesn't exist or is incompatible
- Tests fail for any reason

---

## Risk Assessment

**Low Risk**: Nearly identical pattern to #572 (Notion workspace preferences).

**Key Differences from #572**:
- GitHub uses PAT token (not API key)
- GitHub API endpoint is `/user/repos` (not `search`)
- Response structure differs (full_name vs id for database)
- Repository IDs are integers (database IDs are strings)

---

## Files to Create/Modify Summary

| File | Changes |
|------|---------|
| `web/api/routes/settings_integrations.py` | Add 3 new endpoints + models + file helpers |
| `templates/settings_github.html` | Add repository selection UI section |
| `tests/unit/web/api/routes/test_settings_github_preferences.py` | New test file |

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-11 | Initial gameplan (template v9.3) |

---

_Gameplan created: 2026-01-11_
_Template version: 9.3_
