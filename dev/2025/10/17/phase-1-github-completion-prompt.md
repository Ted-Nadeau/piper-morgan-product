# Phase 1 Step 1.2: Complete GitHub MCP Implementation

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - GitHub Completion (90%→100%)
**Duration**: 2-3 hours estimated
**Date**: October 17, 2025, 2:15 PM

---

## Mission

Complete the GitHub MCP implementation by wiring the existing MCP adapter to GitHubIntegrationRouter. GitHub has a MAJOR advantage over Calendar - its config service already reads from PIPER.user.md! We just need to connect the pieces.

## Context

**Phase -1 Discovery Found**:
- GitHub MCP adapter EXISTS at `services/mcp/consumer/github_adapter.py` (23KB, ~1000 lines)
- GitHub integration router EXISTS at `services/integrations/github/github_integration_router.py` (278 lines)
- GitHub config service ALREADY reads from PIPER.user.md ✅
- Status: 90% complete - just needs wiring!

**Calendar Pattern Established** (just completed):
- Feature flag pattern: `USE_SPATIAL_<SERVICE>`
- Service injection in router constructor
- Conditional adapter initialization based on feature flag
- Graceful fallback when adapter not available

**Why This Matters**:
- GitHub is easier than Calendar (config already works!)
- Second tool-based MCP implementation validates pattern
- Completes Phase 1 (both high-value integrations done)

---

## Your Deliverables

### 1. Verify GitHub MCP Adapter Exists and Analyze (30 minutes)

**Location**: `services/mcp/consumer/github_adapter.py`

**Analysis Required**:
```bash
# Verify file exists
ls -lh services/mcp/consumer/github_adapter.py

# Check class structure
grep -n "^class " services/mcp/consumer/github_adapter.py

# Check method signatures
grep -n "async def\|def " services/mcp/consumer/github_adapter.py

# Check base class
grep -n "BaseSpatialAdapter" services/mcp/consumer/github_adapter.py
```

**Document**:
- Class name: [verify it's GitHubMCPAdapter or similar]
- Base class: [should be BaseSpatialAdapter]
- Constructor signature: [verify it accepts config_service]
- Key methods: [list async methods for GitHub operations]
- Tools available: [what GitHub operations does it support?]

**Expected Methods** (based on GitHub operations):
- `authenticate()` - GitHub API authentication
- `get_repository_info()` - Repository metadata
- `list_issues()` - List issues
- `get_issue()` - Get specific issue
- `create_issue()` - Create new issue
- `update_issue()` - Update issue
- Similar for PRs, commits, etc.

---

### 2. Add GitHub Feature Flag (15 minutes)

**File**: `config/feature_flags.py` (or wherever feature flags are defined)

**Add Flag**:
```python
# GitHub MCP Integration
USE_SPATIAL_GITHUB = os.getenv("USE_SPATIAL_GITHUB", "true").lower() == "true"
```

**Pattern**: Follow Calendar's `USE_SPATIAL_CALENDAR` pattern

**Verify**:
```bash
# Check if feature_flags.py exists
find . -name "feature_flags.py" -type f

# If exists, add to it
# If not, check where Calendar feature flag is defined
grep -r "USE_SPATIAL_CALENDAR" . --include="*.py"
```

---

### 3. Wire MCP Adapter to GitHubIntegrationRouter (1-2 hours)

**File**: `services/integrations/github/github_integration_router.py`

**Current State Analysis**:
```python
# Read current implementation
# Should be ~278 lines, may have legacy GitHub client usage
```

**Required Changes**:

#### Step 3.1: Add Imports

```python
from config.feature_flags import USE_SPATIAL_GITHUB
from services.mcp.consumer.github_adapter import GitHubMCPAdapter
from services.integrations.github.config_service import GitHubConfigService
```

#### Step 3.2: Update Constructor

**Add MCP adapter initialization** (follow Calendar pattern):

```python
class GitHubIntegrationRouter:
    """Router for GitHub integration with MCP adapter support."""

    def __init__(self, config_service: Optional[GitHubConfigService] = None):
        """Initialize GitHub integration router.

        Args:
            config_service: Optional config service for dependency injection
        """
        # Config service (injected or default)
        self.config_service = config_service or GitHubConfigService()

        # MCP adapter (if enabled via feature flag)
        self.mcp_adapter: Optional[GitHubMCPAdapter] = None
        if USE_SPATIAL_GITHUB:
            try:
                self.mcp_adapter = GitHubMCPAdapter(self.config_service)
            except Exception as e:
                # Graceful fallback if MCP adapter fails to initialize
                print(f"Warning: GitHub MCP adapter failed to initialize: {e}")
                self.mcp_adapter = None

        # Legacy client (keep for backward compatibility)
        # [existing legacy GitHub client initialization if present]
```

#### Step 3.3: Add Delegation Methods

**For each GitHub operation, add delegation logic**:

```python
async def get_issue(self, repo: str, issue_number: int) -> Dict[str, Any]:
    """Get GitHub issue, preferring MCP adapter if available.

    Args:
        repo: Repository name (owner/repo format)
        issue_number: Issue number

    Returns:
        Issue data dictionary
    """
    # Prefer MCP adapter if available
    if self.mcp_adapter:
        try:
            return await self.mcp_adapter.get_issue(repo, issue_number)
        except Exception as e:
            print(f"MCP adapter failed, falling back to legacy: {e}")
            # Fall through to legacy

    # Legacy path
    if hasattr(self, 'legacy_client'):
        return await self.legacy_client.get_issue(repo, issue_number)

    raise RuntimeError("No GitHub integration available (MCP disabled, legacy not configured)")

async def create_issue(
    self,
    repo: str,
    title: str,
    body: str,
    labels: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Create GitHub issue, preferring MCP adapter if available."""
    if self.mcp_adapter:
        try:
            return await self.mcp_adapter.create_issue(repo, title, body, labels)
        except Exception as e:
            print(f"MCP adapter failed, falling back to legacy: {e}")

    if hasattr(self, 'legacy_client'):
        return await self.legacy_client.create_issue(repo, title, body, labels)

    raise RuntimeError("No GitHub integration available")

# Similar pattern for:
# - list_issues()
# - update_issue()
# - get_pull_requests()
# - create_pull_request()
# - get_repository_info()
# etc.
```

**Pattern**:
1. Try MCP adapter first (if available)
2. Fall back to legacy client (if configured)
3. Raise error if neither available

---

### 4. Update Tests (1 hour)

**File**: `tests/integration/test_github_integration.py` (or create if doesn't exist)

**Test Coverage Required**:

```python
"""Tests for GitHub MCP integration."""

import pytest
from unittest.mock import Mock, patch, AsyncMock

from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.github.config_service import GitHubConfigService


class TestGitHubIntegrationRouter:
    """Test GitHubIntegrationRouter with MCP adapter."""

    def test_initialization_with_mcp_enabled(self):
        """Test router initializes with MCP adapter when feature flag enabled."""
        with patch('services.integrations.github.github_integration_router.USE_SPATIAL_GITHUB', True):
            router = GitHubIntegrationRouter()
            assert router.mcp_adapter is not None
            assert hasattr(router.mcp_adapter, 'get_issue')

    def test_initialization_with_mcp_disabled(self):
        """Test router initializes without MCP adapter when feature flag disabled."""
        with patch('services.integrations.github.github_integration_router.USE_SPATIAL_GITHUB', False):
            router = GitHubIntegrationRouter()
            assert router.mcp_adapter is None

    def test_service_injection(self):
        """Test config service injection."""
        config_service = GitHubConfigService()
        router = GitHubIntegrationRouter(config_service)
        assert router.config_service is config_service

    @pytest.mark.asyncio
    async def test_get_issue_uses_mcp_adapter(self):
        """Test get_issue delegates to MCP adapter when available."""
        with patch('services.integrations.github.github_integration_router.USE_SPATIAL_GITHUB', True):
            router = GitHubIntegrationRouter()

            # Mock MCP adapter method
            router.mcp_adapter.get_issue = AsyncMock(return_value={"number": 123, "title": "Test"})

            result = await router.get_issue("owner/repo", 123)

            assert result["number"] == 123
            router.mcp_adapter.get_issue.assert_called_once_with("owner/repo", 123)

    @pytest.mark.asyncio
    async def test_fallback_when_mcp_fails(self):
        """Test graceful fallback to legacy when MCP fails."""
        with patch('services.integrations.github.github_integration_router.USE_SPATIAL_GITHUB', True):
            router = GitHubIntegrationRouter()

            # Mock MCP adapter to raise exception
            router.mcp_adapter.get_issue = AsyncMock(side_effect=Exception("API error"))

            # Mock legacy client
            router.legacy_client = Mock()
            router.legacy_client.get_issue = AsyncMock(return_value={"number": 123})

            result = await router.get_issue("owner/repo", 123)

            # Should fall back to legacy
            assert result["number"] == 123
            router.legacy_client.get_issue.assert_called_once()


class TestGitHubMCPAdapter:
    """Test GitHubMCPAdapter directly."""

    def test_initialization(self):
        """Test MCP adapter initialization."""
        from services.mcp.consumer.github_adapter import GitHubMCPAdapter

        adapter = GitHubMCPAdapter()
        assert adapter is not None
        assert hasattr(adapter, 'authenticate')

    def test_config_service_injection(self):
        """Test config service injection."""
        from services.mcp.consumer.github_adapter import GitHubMCPAdapter

        config_service = GitHubConfigService()
        adapter = GitHubMCPAdapter(config_service)
        assert adapter.config_service is config_service


class TestGitHubFeatureFlags:
    """Test GitHub feature flags."""

    def test_use_spatial_github_default_true(self):
        """Test USE_SPATIAL_GITHUB defaults to true."""
        import importlib
        import config.feature_flags as ff
        importlib.reload(ff)

        assert ff.USE_SPATIAL_GITHUB is True

    def test_use_spatial_github_env_override(self, monkeypatch):
        """Test USE_SPATIAL_GITHUB can be overridden by environment."""
        monkeypatch.setenv("USE_SPATIAL_GITHUB", "false")

        import importlib
        import config.feature_flags as ff
        importlib.reload(ff)

        assert ff.USE_SPATIAL_GITHUB is False
```

**Run Tests**:
```bash
# Run new tests
pytest tests/integration/test_github_integration.py -v

# Check for any existing GitHub tests that might break
pytest tests/ -k github -v
```

---

### 5. Verify No Regression (30 minutes)

**Critical**: Ensure existing GitHub functionality still works

```bash
# Run full test suite
pytest tests/ -v

# Specifically check:
# - OrchestrationEngine GitHub operations
# - Any GitHub issue creation tests
# - GitHub config service tests
# - GitHub plugin tests

# Look for test failures
pytest tests/ -k github --tb=short
```

**If tests fail**:
1. Check if legacy GitHub client is properly preserved
2. Verify feature flag defaults to true
3. Check graceful fallback logic
4. Ensure config service still works

---

### 6. Documentation Update (30 minutes)

#### Update ADR-037

**Add GitHub completion section**:

```markdown
## Implementation Status

### Calendar MCP
- Status: ✅ 100% Complete
- Configuration: PIPER.user.md + env vars + defaults
- Pattern: Tool-based with service injection
- Reference: services/integrations/calendar/

### GitHub MCP
- Status: ✅ 100% Complete
- Configuration: PIPER.user.md (already existed)
- Pattern: Tool-based with MCP adapter delegation
- Reference: services/integrations/github/
- MCP Adapter: services/mcp/consumer/github_adapter.py
- Wiring: Feature flag + graceful fallback

Both integrations now follow tool-based MCP pattern per ADR-037.
```

#### Create GitHub MCP Integration Guide

**File**: `docs/integrations/github-mcp-integration.md`

```markdown
# GitHub MCP Integration

## Overview

GitHub integration uses MCP adapter for all GitHub operations, with graceful fallback to legacy client for backward compatibility.

## Architecture

- **MCP Adapter**: services/mcp/consumer/github_adapter.py
- **Integration Router**: services/integrations/github/github_integration_router.py
- **Config Service**: services/integrations/github/config_service.py
- **Feature Flag**: USE_SPATIAL_GITHUB (default: true)

## Configuration

GitHub configuration already reads from PIPER.user.md:

```yaml
github:
  token: "ghp_your_token_here"
  default_repo: "owner/repo"
  timeout: 30
```

Priority order:
1. Environment variables (GITHUB_TOKEN, etc.)
2. PIPER.user.md
3. Defaults

## Usage

```python
from services.integrations.github.github_integration_router import GitHubIntegrationRouter

# Initialize router (MCP adapter loaded automatically if feature flag enabled)
router = GitHubIntegrationRouter()

# Use GitHub operations (automatically uses MCP adapter)
issue = await router.get_issue("owner/repo", 123)
new_issue = await router.create_issue("owner/repo", "Title", "Body")
```

## Feature Flag

Control MCP adapter usage:

```bash
# Enable MCP adapter (default)
export USE_SPATIAL_GITHUB=true

# Disable MCP adapter (use legacy client)
export USE_SPATIAL_GITHUB=false
```

## Troubleshooting

[Common issues and solutions]
```

---

## Success Criteria

GitHub completion is **100%** when:

- [ ] GitHub MCP adapter verified at services/mcp/consumer/github_adapter.py
- [ ] USE_SPATIAL_GITHUB feature flag added
- [ ] GitHubIntegrationRouter updated with MCP adapter initialization
- [ ] Delegation methods added for GitHub operations
- [ ] Graceful fallback to legacy client implemented
- [ ] Comprehensive test coverage (6+ tests)
- [ ] All existing tests still pass (no regression)
- [ ] Documentation updated (ADR-037 + integration guide)
- [ ] Can verify GitHub operations use MCP adapter:
  ```bash
  # Test with MCP enabled (default)
  python -c "from services.integrations.github.github_integration_router import GitHubIntegrationRouter; r = GitHubIntegrationRouter(); print(r.mcp_adapter)"
  # Should show GitHubMCPAdapter instance
  ```

---

## Evidence Required

For completion, provide:

1. **MCP Adapter Analysis** - Confirm GitHubMCPAdapter exists and methods
2. **Feature Flag** - Show USE_SPATIAL_GITHUB added
3. **Router Changes** - Show MCP adapter wiring in GitHubIntegrationRouter
4. **Test Results** - All tests passing (new + existing)
5. **Documentation** - ADR-037 updated + integration guide created
6. **Manual Verification** - MCP adapter loads and is used

---

## Time Budget

- **Total**: 2-3 hours
- **Adapter verification**: 30 min
- **Feature flag**: 15 min
- **Router wiring**: 1-2 hours
- **Tests**: 1 hour
- **Verification**: 30 min
- **Documentation**: 30 min

---

## Key Differences from Calendar

**Advantages**:
- ✅ Config already reads from PIPER.user.md (no YAML work needed!)
- ✅ MCP adapter already exists (23KB, complete)
- ✅ Just needs wiring (not implementation)

**Approach**:
- Focus on delegation pattern (MCP first, legacy fallback)
- Preserve backward compatibility (legacy client still works)
- Feature flag control (can disable MCP if needed)

---

## Remember

- MCP adapter already exists - don't recreate it!
- Config already works - don't modify CalendarConfigService!
- Preserve legacy client - don't break existing functionality
- Graceful fallback - system must work if MCP fails
- Test thoroughly - ensure no regression

---

**Ready to complete GitHub MCP to 100%!** 🎯

**Key Insight**: GitHub is actually EASIER than Calendar because config and adapter already exist - we just need to wire them together!
