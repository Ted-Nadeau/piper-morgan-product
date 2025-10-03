# Claude Code Agent Prompt: GREAT-3A Phase 1C - GitHub Router Alignment

## Mission
**Fix GitHub**: Wire existing GitHubConfigService to router for service injection pattern compliance.

## Context from Phase 1B Audit
Your audit found:
- ✅ GitHubConfigService EXISTS at `services/integrations/github/config_service.py`
- ❌ GitHubIntegrationRouter DOESN'T USE IT (creates config internally or uses env directly)
- Pattern: Partial implementation (service exists but not wired to router)

**This is the quick win** - service already complete, just needs router integration.

## Your Tasks

### Task 1: Verify Current Router Pattern

```bash
cd ~/Development/piper-morgan

# Check current router __init__ signature
grep -A 30 "def __init__" services/integrations/github/github_integration_router.py

# Check if router has any config usage
grep "config" services/integrations/github/github_integration_router.py | head -20

# Verify GitHubConfigService is ready
grep -A 20 "class GitHubConfigService" services/integrations/github/config_service.py
```

**Document**: How does router currently get config (if at all)?

### Task 2: Update Router to Accept Config Service

**File**: `services/integrations/github/github_integration_router.py`

**Pattern to Follow** (from Slack):
```python
from typing import Optional
from .config_service import GitHubConfigService

class GitHubIntegrationRouter:
    def __init__(self, config_service: Optional[GitHubConfigService] = None):
        """Initialize router with feature flag checking and config service"""

        # Store config service
        self.config_service = config_service or GitHubConfigService()

        # Use config throughout router as needed
        # Example: self.config_service.get_config().github_token
```

**Implementation**:
1. Add import for GitHubConfigService
2. Add optional config_service parameter to __init__
3. Store config service (create default if not provided)
4. Replace any direct env access with config service usage

### Task 3: Update Config Usage in Router

**Find and replace direct environment access**:

```bash
# Find direct os.getenv usage in router
grep "os.getenv\|os.environ" services/integrations/github/github_integration_router.py

# Replace with config service pattern
# OLD: os.getenv("GITHUB_TOKEN")
# NEW: self.config_service.get_config().github_token
```

**Check all router methods** that might use config:
- Authentication methods
- API calls
- Feature flag checks
- Health checks

### Task 4: Maintain Backward Compatibility

**Critical**: Existing code must work without changes!

```python
# Old usage (should still work)
router = GitHubIntegrationRouter()

# New usage (preferred)
config = GitHubConfigService()
router = GitHubIntegrationRouter(config)
```

**Default behavior**: If no config_service provided, create one internally.

### Task 5: Test Implementation

```bash
# Test 1: Import works
python -c "from services.integrations.github.github_integration_router import GitHubIntegrationRouter; print('Import OK')"

# Test 2: Router instantiates (no param)
python -c "from services.integrations.github.github_integration_router import GitHubIntegrationRouter; r = GitHubIntegrationRouter(); print('Router OK')"

# Test 3: Router with explicit config
python -c "from services.integrations.github.config_service import GitHubConfigService; from services.integrations.github.github_integration_router import GitHubIntegrationRouter; c = GitHubConfigService(); r = GitHubIntegrationRouter(c); print('Integration OK')"

# Test 4: Config service is actually used
python -c "from services.integrations.github.github_integration_router import GitHubIntegrationRouter; r = GitHubIntegrationRouter(); print('Config service:', r.config_service); print('Has config:', hasattr(r, 'config_service'))"
```

### Task 6: Verify Pattern Compliance

**Check against Slack pattern**:
- ✅ Router has config_service attribute
- ✅ Router accepts optional config_service parameter
- ✅ Router creates default config if none provided
- ✅ Router uses config_service for configuration access
- ✅ Backward compatibility maintained

## Deliverable

Create: `dev/2025/10/02/phase-1c-code-github-alignment.md`

Include:
1. **Current Pattern Analysis**: How router gets config now
2. **Changes Made**: Diffs showing router updates
3. **Test Results**: All 4 test commands passing
4. **Pattern Compliance**: Verification against Slack pattern
5. **Backward Compatibility**: Proof existing usage still works

## Time Estimate
30 minutes

## Success Criteria
- [ ] Router accepts config_service parameter
- [ ] Router uses GitHubConfigService internally
- [ ] All direct env access replaced with config service
- [ ] Backward compatibility maintained
- [ ] All test commands pass
- [ ] Pattern matches Slack/Notion

---

**Deploy at 3:50 PM**
**Coordinate with Cursor on test suite creation**
