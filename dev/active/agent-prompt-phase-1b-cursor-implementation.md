# Cursor Agent Prompt: GREAT-3A Phase 1B - Notion Config Service Implementation

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 1B work.

## Mission
**Implement**: Create `services/integrations/notion/config_service.py` following Slack pattern, update router to use service injection.

## Context from Phase 1
**Chief Architect Decision**: Align Notion with Slack service injection pattern NOW (not defer to Phase 2).

**Why This Matters**:
- Plugin architecture requires pattern consistency
- Service injection superior for testability
- GREAT-3A's purpose: fix refactoring artifacts
- Technical debt addressed during refactoring

**Current State**: Notion uses static config (`config/notion_config.py`) instead of service injection pattern.

## Your Implementation Tasks

### Task 1: Create Notion Config Service

**File**: `services/integrations/notion/config_service.py`

**Use your Phase 1 template** with these adjustments:
- Follow Slack pattern exactly (you analyzed this)
- Environment variables: `NOTION_API_KEY`, `NOTION_ENVIRONMENT`, etc.
- Dataclass: `NotionConfig` with validation
- Service class: `NotionConfigService` with env loading
- Method: `is_configured()` for health checks

**Template from your Phase 1 report is ready to use** - implement it!

### Task 2: Update Notion Router

**File**: `services/integrations/notion/notion_integration_router.py`

**Changes**:
```python
# BEFORE
def __init__(self):
    self.spatial_notion = NotionMCPAdapter()

# AFTER
def __init__(self, config_service=None):
    self.config_service = config_service

    if self.use_spatial:
        if config_service:
            self.spatial_notion = NotionMCPAdapter(config_service)
        else:
            self.spatial_notion = NotionMCPAdapter()  # Graceful degradation
```

**Add import**:
```python
from typing import Optional
from .config_service import NotionConfigService
```

### Task 3: Preserve Legacy Config

**DO NOT DELETE**: `config/notion_config.py` (keep as fallback during migration)

**Add note in new file**:
```python
# Note: Replaces static config/notion_config.py with service injection pattern
# Legacy file preserved for backward compatibility during migration
```

### Task 4: Update NotionMCPAdapter (If Needed)

**Check**: Does `services/integrations/mcp/notion_adapter.py` need updating?

```bash
# Check current adapter __init__
grep -A 20 "def __init__" services/integrations/mcp/notion_adapter.py

# If adapter accepts config, update signature:
def __init__(self, config_service: Optional[NotionConfigService] = None):
    if config_service:
        self.config = config_service.get_config()
    else:
        # Fallback to static config
        from config.notion_config import NotionConfig
        self.config = NotionConfig()
```

### Task 5: Test Pattern Works

```bash
# Test 1: Import works
python -c "from services.integrations.notion.config_service import NotionConfigService; print('Import OK')"

# Test 2: Config service instantiates
python -c "from services.integrations.notion.config_service import NotionConfigService; c = NotionConfigService(); print('Service OK')"

# Test 3: Router accepts config
python -c "from services.integrations.notion.notion_integration_router import NotionIntegrationRouter; r = NotionIntegrationRouter(); print('Router OK')"

# Test 4: Router with config
python -c "from services.integrations.notion.config_service import NotionConfigService; from services.integrations.notion.notion_integration_router import NotionIntegrationRouter; c = NotionConfigService(); r = NotionIntegrationRouter(c); print('Integration OK')"
```

## Implementation Order

1. **Create config_service.py** (new file, safe)
2. **Update router signature** (add optional param, backward compatible)
3. **Update router config flow** (use config if provided)
4. **Test all scenarios** (with/without config)
5. **Check adapter integration** (update if needed)

## Backward Compatibility

**Critical**: Existing code must still work during migration!

```python
# Old usage (still works)
router = NotionIntegrationRouter()

# New usage (preferred)
config = NotionConfigService()
router = NotionIntegrationRouter(config)
```

## Deliverable

Create: `dev/2025/10/02/phase-1b-cursor-notion-implementation.md`

Include:
1. **Files Created**: config_service.py implementation
2. **Files Modified**: Router changes with diffs
3. **Test Results**: All 4 test commands passing
4. **Adapter Changes**: If NotionMCPAdapter updated
5. **Validation**: Pattern matches Slack exactly

## Time Estimate
30 minutes for complete implementation + testing

## Success Criteria
- [ ] config_service.py created following Slack pattern
- [ ] Router accepts config_service parameter
- [ ] Router uses config when provided
- [ ] Graceful degradation when config missing
- [ ] All test commands pass
- [ ] Backward compatibility maintained
- [ ] Pattern matches Slack (verified)

---

**Deploy at 2:15 PM**
**Coordinate with Code on pattern audit findings**
