# Claude Code Agent Prompt: GREAT-3A Phase 1C Revision - GitHub Config Interface Standardization

## Mission
**Refactor GitHub**: Add standard config interface methods to GitHubConfigService while preserving GitHub-specific extensions.

## Context from Chief Architect Decision (4:26 PM)

**Ruling**: All config services MUST implement standard interface for plugin architecture consistency.

**Standard Interface Required**:
```python
class ConfigService:
    def get_config(self) -> dict:
        """Returns complete configuration dictionary"""

    def is_configured(self) -> bool:
        """Returns True if all required config present"""

    def _load_config(self) -> dict:
        """Private method to load from environment/files"""
```

**GitHub Extensions Allowed**: Keep existing methods (`get_client_configuration()`, `get_authentication_token()`) as extensions, but ADD the standard interface.

## Current State

**GitHubConfigService Currently Has**:
- `get_client_configuration()` - GitHub-specific
- `get_authentication_token()` - GitHub-specific
- `to_dict()` - GitHub-specific
- Other advanced methods

**GitHubConfigService Currently LACKS**:
- `get_config()` - REQUIRED standard method
- `is_configured()` - REQUIRED standard method
- `_load_config()` - REQUIRED standard method

## Your Tasks

### Task 1: Add get_config() Method

**File**: `services/integrations/github/config_service.py`

**Implementation**:
```python
def get_config(self) -> dict:
    """
    Returns complete configuration dictionary (standard interface).

    Implements standard config service interface for plugin architecture.
    Returns dictionary with all GitHub configuration.
    """
    return self.to_dict()  # Leverage existing method
```

**Rationale**: GitHub already has `to_dict()` that returns config as dict. Use it.

### Task 2: Add is_configured() Method

**Implementation**:
```python
def is_configured(self) -> bool:
    """
    Returns True if all required config present (standard interface).

    Implements standard config service interface for plugin architecture.
    Checks if GitHub authentication token is available.
    """
    try:
        token = self.get_authentication_token()
        return bool(token)
    except Exception:
        return False
```

**Rationale**: GitHub is configured if authentication token is available.

### Task 3: Add _load_config() Method

**Implementation**:
```python
def _load_config(self) -> dict:
    """
    Private method to load config from environment (standard interface).

    Implements standard config service interface for plugin architecture.
    GitHub's config loading is handled in __init__ and other methods.
    This method provides the standard interface by returning current config.
    """
    return self.get_config()
```

**Rationale**: GitHub loads config in __init__, this method provides standard interface.

### Task 4: Add Docstring Note

**Add to class docstring**:
```python
class GitHubConfigService:
    """
    Centralized GitHub configuration service implementing ADR-010 patterns.

    Implements standard config service interface for plugin architecture:
    - get_config() -> dict: Returns complete configuration
    - is_configured() -> bool: Validates required config present
    - _load_config() -> dict: Loads config from environment

    GitHub-specific extensions:
    - get_client_configuration(): Returns GitHubClientConfig object
    - get_authentication_token(): Returns GitHub auth token
    - to_dict(): Returns configuration as dictionary
    """
```

### Task 5: Verify Interface Compliance

**Check against Slack/Notion**:
```bash
# Compare method signatures
grep -A 3 "def get_config" services/integrations/slack/config_service.py
grep -A 3 "def get_config" services/integrations/notion/config_service.py
grep -A 3 "def get_config" services/integrations/github/config_service.py

# Verify all three have same methods
for integration in slack notion github; do
    echo "=== $integration ==="
    grep "def get_config\|def is_configured\|def _load_config" services/integrations/$integration/config_service.py
done
```

**Ensure**:
- Method names match exactly
- Return types consistent
- Docstrings follow same pattern

### Task 6: Update Router to Use Standard Interface

**File**: `services/integrations/github/github_integration_router.py`

**Check if router uses GitHub-specific methods**:
```bash
grep "get_client_configuration\|get_authentication_token" services/integrations/github/github_integration_router.py
```

**If yes, consider**:
- Can router use standard `get_config()` instead?
- Or keep GitHub-specific methods if needed?

**Goal**: Router should primarily use standard interface when possible.

### Task 7: Test Standard Interface

```bash
# Test 1: get_config() works
python -c "from services.integrations.github.config_service import GitHubConfigService; c = GitHubConfigService(); config = c.get_config(); print('get_config() returns:', type(config)); assert isinstance(config, dict)"

# Test 2: is_configured() works
python -c "from services.integrations.github.config_service import GitHubConfigService; c = GitHubConfigService(); configured = c.is_configured(); print('is_configured():', configured); assert isinstance(configured, bool)"

# Test 3: _load_config() works
python -c "from services.integrations.github.config_service import GitHubConfigService; c = GitHubConfigService(); config = c._load_config(); print('_load_config() returns:', type(config)); assert isinstance(config, dict)"

# Test 4: Extensions still work
python -c "from services.integrations.github.config_service import GitHubConfigService; c = GitHubConfigService(); client_config = c.get_client_configuration(); print('GitHub extensions still work:', client_config is not None)"
```

### Task 8: Run Cursor's Compliance Tests

```bash
# Run test suite on GitHub
pytest tests/integration/config_pattern_compliance/ -k github -v

# Should now pass ALL standard interface tests
# GitHub-specific methods are extras, not required by tests
```

## Deliverable

Create: `dev/2025/10/02/phase-1c-code-github-standardization.md`

Include:
1. **Standard Methods Added**: get_config(), is_configured(), _load_config()
2. **Implementation Details**: Code with explanations
3. **Extensions Preserved**: GitHub-specific methods still available
4. **Test Results**: All 4 test commands passing
5. **Compliance Tests**: Cursor's test suite results
6. **Interface Comparison**: Verify matches Slack/Notion

## Critical Requirements

- **DO NOT remove** GitHub's existing methods
- **DO add** standard interface methods
- **DO make** standard methods work correctly
- **DO preserve** backward compatibility
- **DO update** docstrings to document both interfaces

## Time Estimate
30 minutes

## Success Criteria
- [ ] get_config() method added and working
- [ ] is_configured() method added and working
- [ ] _load_config() method added and working
- [ ] GitHub extensions preserved
- [ ] All test commands pass
- [ ] Cursor's compliance tests pass
- [ ] Interface matches Slack/Notion standard

---

**Deploy at 4:28 PM**
**This completes GitHub standardization before moving to Calendar**
