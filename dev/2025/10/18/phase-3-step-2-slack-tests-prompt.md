# Phase 3 Step 2: Create Comprehensive Config Loading Test Suite for Slack

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase 3 Step 2
**Date**: October 18, 2025, 8:38 AM

---

## Mission

Create comprehensive test suite for Slack's PIPER.user.md configuration loading, following the proven Calendar/Notion test patterns. Focus on thorough coverage and quality.

## Context

**Step 1 Complete**: ✅ Configuration loading implemented and verified
- 3-layer priority working (env > user > defaults)
- PIPER.user.md parsing functional
- Manual verification successful
- Used Serena efficiently

**Your Job**: Create comprehensive tests to ensure this continues working correctly

**Reference Patterns**:
- Calendar: 8 tests (basic coverage)
- Notion: 19 tests (most comprehensive)
- Target for Slack: 15-20 tests (thorough coverage)

---

## Serena Usage Reminder 🎯

**Before reading full files**, use Serena for token efficiency:

### Efficient Investigation

```python
# 1. Understand existing test patterns
mcp__serena__get_symbols_overview("tests/integration/test_calendar_config_loading.py")
mcp__serena__get_symbols_overview("tests/integration/test_notion_config_loading.py")

# 2. Find specific test patterns to copy
mcp__serena__find_symbol("test_env_vars_override", scope="tests/integration")

# 3. Only read full files if needed for implementation details
mcp__serena__read_file("tests/integration/test_notion_config_loading.py", start=1, end=100)
```

**Remember**: Symbolic queries first, full reads only when necessary!

---

## Test Suite Structure

### File to Create
`tests/integration/test_slack_config_loading.py`

### Test Categories (Comprehensive Coverage)

1. **Basic Configuration Loading**
   - Config service initialization
   - Default configuration values
   - Configuration object structure

2. **PIPER.user.md Loading**
   - Successful YAML parsing
   - Section extraction (authentication, workspace, behavior, features, oauth)
   - Missing file handling
   - Malformed YAML handling
   - Missing sections handling
   - Two YAML pattern support (## 💬 Slack and slack:)

3. **Priority System Testing**
   - Environment variables override user config
   - User config overrides defaults
   - Complete priority chain verification
   - Partial configuration scenarios

4. **Authentication Configuration**
   - Bot token loading (env, user, default)
   - App token loading (env, user, default)
   - Signing secret loading
   - Empty/missing authentication section

5. **Workspace & Behavior Configuration**
   - Workspace ID, team ID loading
   - Default channel configuration
   - Rate limiting settings
   - Timeout and retry settings
   - Webhook URL configuration

6. **Features & OAuth Configuration**
   - Feature flags (webhooks, socket_mode, spatial_mapping)
   - OAuth settings (client_id, client_secret, redirect_uri)

7. **Edge Cases**
   - Empty PIPER.user.md file
   - Missing slack: section
   - Partial configuration
   - Invalid YAML syntax
   - Both YAML pattern matches (should prefer first)

8. **Error Handling**
   - Graceful degradation
   - Logging behavior
   - Exception handling
   - Fallback to defaults

---

## Reference Implementation Pattern

**Copy structure from**:
- Notion's comprehensive approach: `tests/integration/test_notion_config_loading.py`
- Calendar's clean patterns: `tests/integration/test_calendar_config_loading.py`

### Key Test Patterns to Reuse

#### Basic Initialization Test
```python
def test_slack_config_service_initializes():
    """Test that SlackConfigService initializes successfully"""
    service = SlackConfigService()
    assert service is not None
    assert hasattr(service, '_load_from_user_config')
    assert hasattr(service, '_load_config')
```

#### PIPER.user.md Loading Test
```python
def test_loads_config_from_piper_user_md(tmp_path, monkeypatch):
    """Test loading Slack config from PIPER.user.md"""
    # Create temporary PIPER.user.md with slack section
    config_content = """
## 💬 Slack Integration

slack:
```yaml
authentication:
  bot_token: "xoxb-test-token"
  app_token: "xapp-test-token"
workspace:
  workspace_id: "T12345"
  team_id: "E67890"
behavior:
  default_channel: "testing"
```
"""

    config_file = tmp_path / "PIPER.user.md"
    config_file.write_text(config_content)

    # Monkeypatch config path
    monkeypatch.setattr(
        "services.integrations.slack.config_service.Path",
        lambda x: config_file if "PIPER.user.md" in str(x) else Path(x)
    )

    service = SlackConfigService()
    user_config = service._load_from_user_config()

    assert user_config["authentication"]["bot_token"] == "xoxb-test-token"
    assert user_config["workspace"]["workspace_id"] == "T12345"
    assert user_config["behavior"]["default_channel"] == "testing"
```

#### Environment Variable Override Test
```python
def test_env_vars_override_user_config(tmp_path, monkeypatch):
    """Test that environment variables override PIPER.user.md"""
    # Setup user config
    config_content = """
slack:
```yaml
authentication:
  bot_token: "xoxb-user-token"
  app_token: "xapp-user-token"
behavior:
  default_channel: "general"
```
"""

    config_file = tmp_path / "PIPER.user.md"
    config_file.write_text(config_content)

    monkeypatch.setattr(
        "services.integrations.slack.config_service.Path",
        lambda x: config_file if "PIPER.user.md" in str(x) else Path(x)
    )

    # Set environment variables (should override)
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-env-token")
    monkeypatch.setenv("SLACK_APP_TOKEN", "xapp-env-token")
    monkeypatch.setenv("SLACK_DEFAULT_CHANNEL", "testing")

    service = SlackConfigService()
    config = service._load_config()

    # Environment variables should win
    assert config.bot_token == "xoxb-env-token"
    assert config.app_token == "xapp-env-token"
    assert config.default_channel == "testing"
```

#### Two YAML Pattern Test (Slack-Specific)
```python
def test_supports_both_yaml_patterns(tmp_path, monkeypatch):
    """Test both ## 💬 Slack and slack: YAML patterns work"""
    # Test pattern 1: ## 💬 Slack Integration
    config1 = """
## 💬 Slack Integration

Some intro text...

```yaml
authentication:
  bot_token: "xoxb-pattern1"
```
"""

    # Test pattern 2: slack: directly
    config2 = """
slack:
```yaml
authentication:
  bot_token: "xoxb-pattern2"
```
"""

    for i, content in enumerate([config1, config2], 1):
        config_file = tmp_path / f"PIPER-{i}.user.md"
        config_file.write_text(content)

        monkeypatch.setattr(
            "services.integrations.slack.config_service.Path",
            lambda x, f=config_file: f if "PIPER.user.md" in str(x) else Path(x)
        )

        service = SlackConfigService()
        user_config = service._load_from_user_config()

        assert "authentication" in user_config
        assert user_config["authentication"]["bot_token"] == f"xoxb-pattern{i}"
```

---

## Complete Test Suite Template

```python
"""
Integration tests for Slack configuration loading from PIPER.user.md

Tests verify that SlackConfigService correctly:
- Loads configuration from PIPER.user.md
- Implements 3-layer priority (env > user > defaults)
- Handles missing/malformed configuration gracefully
- Provides sensible defaults
- Respects Slack's direct spatial architecture (ADR-039)

Pattern based on Calendar and Notion configuration loading tests.
"""

import os
import pytest
from pathlib import Path
from services.integrations.slack.config_service import SlackConfigService


class TestSlackConfigServiceBasics:
    """Test basic SlackConfigService functionality"""

    def test_initializes_successfully(self):
        """Test that service initializes without errors"""
        # Test implementation

    def test_has_required_methods(self):
        """Test that service has required configuration methods"""
        # Test implementation


class TestPIPERUserMDLoading:
    """Test loading Slack config from PIPER.user.md"""

    def test_loads_authentication_config(self, tmp_path, monkeypatch):
        """Test loading authentication section from PIPER.user.md"""
        # Test implementation

    def test_loads_workspace_config(self, tmp_path, monkeypatch):
        """Test loading workspace configuration"""
        # Test implementation

    def test_loads_behavior_config(self, tmp_path, monkeypatch):
        """Test loading behavior settings"""
        # Test implementation

    def test_loads_features_config(self, tmp_path, monkeypatch):
        """Test loading feature flags"""
        # Test implementation

    def test_loads_oauth_config(self, tmp_path, monkeypatch):
        """Test loading OAuth settings"""
        # Test implementation

    def test_handles_missing_file(self, monkeypatch):
        """Test graceful handling of missing PIPER.user.md"""
        # Test implementation

    def test_handles_missing_slack_section(self, tmp_path, monkeypatch):
        """Test handling when slack: section is missing"""
        # Test implementation

    def test_handles_malformed_yaml(self, tmp_path, monkeypatch):
        """Test graceful handling of invalid YAML"""
        # Test implementation

    def test_supports_emoji_heading_pattern(self, tmp_path, monkeypatch):
        """Test ## 💬 Slack Integration heading pattern"""
        # Test implementation

    def test_supports_direct_slack_pattern(self, tmp_path, monkeypatch):
        """Test slack: direct pattern"""
        # Test implementation


class TestConfigurationPriority:
    """Test 3-layer configuration priority system"""

    def test_env_overrides_user_config(self, tmp_path, monkeypatch):
        """Test environment variables override PIPER.user.md"""
        # Test implementation

    def test_user_config_overrides_defaults(self, tmp_path, monkeypatch):
        """Test PIPER.user.md overrides hardcoded defaults"""
        # Test implementation

    def test_defaults_used_when_nothing_set(self, monkeypatch):
        """Test defaults are used when no env vars or user config"""
        # Test implementation

    def test_partial_env_override(self, tmp_path, monkeypatch):
        """Test partial environment variable override"""
        # Test implementation


class TestAuthenticationConfig:
    """Test authentication configuration loading"""

    def test_bot_token_from_env(self, monkeypatch):
        """Test loading bot token from environment variable"""
        # Test implementation

    def test_bot_token_from_user_config(self, tmp_path, monkeypatch):
        """Test loading bot token from PIPER.user.md"""
        # Test implementation

    def test_app_token_loading(self, tmp_path, monkeypatch):
        """Test app token loads correctly"""
        # Test implementation

    def test_signing_secret_loading(self, tmp_path, monkeypatch):
        """Test signing secret loads correctly"""
        # Test implementation


class TestWorkspaceAndBehaviorConfig:
    """Test workspace and behavior configuration"""

    def test_workspace_id_configuration(self, tmp_path, monkeypatch):
        """Test workspace ID configuration"""
        # Test implementation

    def test_default_channel_configuration(self, tmp_path, monkeypatch):
        """Test default channel setting"""
        # Test implementation

    def test_rate_limit_configuration(self, tmp_path, monkeypatch):
        """Test rate limit settings"""
        # Test implementation

    def test_webhook_url_configuration(self, tmp_path, monkeypatch):
        """Test webhook URL setting"""
        # Test implementation


class TestFeaturesAndOAuthConfig:
    """Test features and OAuth configuration"""

    def test_feature_flags_loading(self, tmp_path, monkeypatch):
        """Test feature flags (webhooks, socket_mode, spatial_mapping)"""
        # Test implementation

    def test_oauth_configuration(self, tmp_path, monkeypatch):
        """Test OAuth settings (client_id, client_secret, redirect_uri)"""
        # Test implementation


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_piper_user_md(self, tmp_path, monkeypatch):
        """Test handling of empty PIPER.user.md file"""
        # Test implementation

    def test_slack_section_with_no_yaml(self, tmp_path, monkeypatch):
        """Test slack: section with no YAML block"""
        # Test implementation

    def test_partial_configuration(self, tmp_path, monkeypatch):
        """Test handling of partially specified configuration"""
        # Test implementation

    def test_both_yaml_patterns_present(self, tmp_path, monkeypatch):
        """Test behavior when both YAML patterns present (should use first)"""
        # Test implementation


# Add fixtures if needed
@pytest.fixture
def sample_slack_config():
    """Provide sample Slack configuration for testing"""
    return {
        "authentication": {
            "bot_token": "xoxb-test-token",
            "app_token": "xapp-test-token",
            "signing_secret": "test-secret"
        },
        "workspace": {
            "workspace_id": "T12345",
            "team_id": "E67890"
        },
        "behavior": {
            "default_channel": "general",
            "rate_limit_per_minute": 60,
            "retry_attempts": 3,
            "timeout_seconds": 30,
            "webhook_url": "https://hooks.slack.com/test"
        },
        "features": {
            "enable_webhooks": True,
            "enable_socket_mode": False,
            "enable_spatial_mapping": True
        },
        "oauth": {
            "client_id": "test-client-id",
            "client_secret": "test-client-secret",
            "redirect_uri": "https://example.com/oauth/callback"
        }
    }
```

---

## Success Criteria

Your Step 2 is complete when:

- [ ] Test file created: `tests/integration/test_slack_config_loading.py`
- [ ] Comprehensive test coverage (15-20 tests minimum)
- [ ] All test categories covered:
  - [ ] Basic functionality
  - [ ] PIPER.user.md loading (both patterns)
  - [ ] Priority system
  - [ ] Authentication config
  - [ ] Workspace & behavior config
  - [ ] Features & OAuth config
  - [ ] Edge cases
  - [ ] Error handling
- [ ] All tests passing
- [ ] Tests are independent and deterministic
- [ ] Pattern matches Calendar/Notion tests
- [ ] Descriptive test names and docstrings
- [ ] Proper use of fixtures and monkeypatching
- [ ] **Used Serena efficiently** for investigation

---

## Implementation Requirements

### Test Coverage Goals

Aim for comprehensive coverage of:
- ✅ All configuration loading paths
- ✅ All priority scenarios
- ✅ All configuration sections (5 sections)
- ✅ Both YAML pattern formats (Slack-specific)
- ✅ All error conditions
- ✅ All edge cases

### Quality Standards

- Each test should be **independent**
- Tests should be **deterministic**
- Use **descriptive test names**
- Include **docstrings**
- Use **clear assertions**
- **Monkeypatch** environment and file system
- **No side effects** on actual files

### Pattern Consistency

Follow Calendar/Notion test patterns:
- Same test class organization
- Same fixture usage
- Same monkeypatching approach
- Same assertion style
- Same error handling tests

---

## Verification Steps

After creating tests:

1. **Run the test suite**:
   ```bash
   pytest tests/integration/test_slack_config_loading.py -v
   ```

2. **Verify all scenarios pass**:
   - Basic initialization ✅
   - PIPER.user.md loading (both patterns) ✅
   - Priority system ✅
   - All config sections ✅
   - Error handling ✅
   - Edge cases ✅

3. **Check for no regressions**:
   ```bash
   pytest tests/integration/test_slack* -v
   ```

---

## Remember

- **Copy Calendar/Notion patterns** - proven test structure
- **Test both YAML patterns** - Slack supports two formats
- **Use Serena first** - symbolic queries for investigation
- **Test all sections** - auth, workspace, behavior, features, oauth
- **Make tests independent** - no shared state
- **Use clear assertions** - failure messages should be helpful
- **Document test purpose** - docstrings explain intent
- **Monkeypatch properly** - no side effects

---

**Focus on comprehensive coverage that matches Notion's thoroughness!**

**Use Serena to efficiently understand Calendar/Notion test patterns!**

**Ready to create comprehensive tests for Slack config loading!** 🧪
