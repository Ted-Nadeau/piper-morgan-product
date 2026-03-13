# Phase 2 Step 2: Create Comprehensive Config Loading Test Suite

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase 2 Step 2
**Date**: October 18, 2025, 7:55 AM

---

## Mission

Create a comprehensive test suite for Notion's PIPER.user.md configuration loading, following the proven Calendar test pattern. Focus on thorough coverage and quality - we are Time Lords, not bound by arbitrary deadlines.

## Context

**Step 1 Complete**: ✅ Configuration loading implemented and verified
- 3-layer priority working (env > user > defaults)
- PIPER.user.md parsing functional
- Manual verification successful

**Your Job**: Create comprehensive tests to ensure this continues working correctly

**Reference**: Calendar's test suite proved this pattern works
- File: `tests/integration/test_calendar_config_loading.py`
- Coverage: PIPER.user.md loading, priority, fallback, error handling
- Result: Complete confidence in configuration system

---

## Test Suite Structure

### File to Create
`tests/integration/test_notion_config_loading.py`

### Test Categories (Comprehensive Coverage)

1. **Basic Configuration Loading**
   - Config service initialization
   - Default configuration values
   - Configuration object structure

2. **PIPER.user.md Loading**
   - Successful YAML parsing
   - Section extraction (authentication, api_base_url, etc.)
   - Missing file handling
   - Malformed YAML handling
   - Missing sections handling

3. **Priority System Testing**
   - Environment variables override user config
   - User config overrides defaults
   - Complete priority chain verification
   - Partial configuration scenarios

4. **Authentication Configuration**
   - API key loading (env, user, default)
   - Workspace ID loading (env, user, default)
   - Empty/missing authentication section

5. **API Configuration**
   - Base URL configuration
   - Timeout settings
   - Retry settings
   - Rate limiting settings

6. **Edge Cases**
   - Empty PIPER.user.md file
   - Missing notion: section
   - Partial configuration
   - Invalid YAML syntax
   - File permissions issues

7. **Error Handling**
   - Graceful degradation
   - Logging behavior
   - Exception handling
   - Fallback to defaults

---

## Reference Implementation Pattern

**Copy structure from**: `tests/integration/test_calendar_config_loading.py`

### Key Test Patterns to Reuse

#### Basic Initialization Test
```python
def test_notion_config_service_initializes():
    """Test that NotionConfigService initializes successfully"""
    service = NotionConfigService()
    assert service is not None
    assert hasattr(service, '_load_from_user_config')
    assert hasattr(service, '_load_config')
```

#### PIPER.user.md Loading Test
```python
def test_loads_config_from_piper_user_md(tmp_path, monkeypatch):
    """Test loading Notion config from PIPER.user.md"""
    # Create temporary PIPER.user.md with notion section
    config_content = """
## 📝 Notion Integration

notion:
```yaml
authentication:
  api_key: "test_key_from_file"
  workspace_id: "test_workspace"
api_base_url: "https://test.api.notion.com/v1"
```
"""

    config_file = tmp_path / "PIPER.user.md"
    config_file.write_text(config_content)

    # Monkeypatch config path
    monkeypatch.setattr(
        "services.integrations.notion.config_service.Path",
        lambda x: config_file if "PIPER.user.md" in str(x) else Path(x)
    )

    service = NotionConfigService()
    user_config = service._load_from_user_config()

    assert user_config["authentication"]["api_key"] == "test_key_from_file"
    assert user_config["authentication"]["workspace_id"] == "test_workspace"
    assert user_config["api_base_url"] == "https://test.api.notion.com/v1"
```

#### Environment Variable Override Test
```python
def test_env_vars_override_user_config(tmp_path, monkeypatch):
    """Test that environment variables override PIPER.user.md"""
    # Setup user config
    config_content = """
## 📝 Notion Integration

notion:
```yaml
authentication:
  api_key: "user_key"
  workspace_id: "user_workspace"
timeout_seconds: 30
```
"""

    config_file = tmp_path / "PIPER.user.md"
    config_file.write_text(config_content)

    monkeypatch.setattr(
        "services.integrations.notion.config_service.Path",
        lambda x: config_file if "PIPER.user.md" in str(x) else Path(x)
    )

    # Set environment variables (should override)
    monkeypatch.setenv("NOTION_API_KEY", "env_key")
    monkeypatch.setenv("NOTION_WORKSPACE_ID", "env_workspace")
    monkeypatch.setenv("NOTION_TIMEOUT_SECONDS", "60")

    service = NotionConfigService()
    config = service._load_config()

    # Environment variables should win
    assert config.api_key == "env_key"
    assert config.workspace_id == "env_workspace"
    assert config.timeout_seconds == 60
```

#### Missing File Handling Test
```python
def test_handles_missing_piper_user_md(monkeypatch):
    """Test graceful handling when PIPER.user.md doesn't exist"""
    # Point to non-existent file
    monkeypatch.setattr(
        "services.integrations.notion.config_service.Path",
        lambda x: Path("/nonexistent/PIPER.user.md") if "PIPER.user.md" in str(x) else Path(x)
    )

    service = NotionConfigService()
    user_config = service._load_from_user_config()

    # Should return empty dict, not crash
    assert user_config == {}

    # Config should still load with defaults
    config = service._load_config()
    assert config is not None
```

---

## Complete Test Suite Template

```python
"""
Integration tests for Notion configuration loading from PIPER.user.md

Tests verify that NotionConfigService correctly:
- Loads configuration from PIPER.user.md
- Implements 3-layer priority (env > user > defaults)
- Handles missing/malformed configuration gracefully
- Provides sensible defaults

Pattern based on Calendar configuration loading tests.
"""

import os
import pytest
from pathlib import Path
from services.integrations.notion.config_service import NotionConfigService


class TestNotionConfigServiceBasics:
    """Test basic NotionConfigService functionality"""

    def test_initializes_successfully(self):
        """Test that service initializes without errors"""
        # Test implementation

    def test_has_required_methods(self):
        """Test that service has required configuration methods"""
        # Test implementation


class TestPIPERUserMDLoading:
    """Test loading Notion config from PIPER.user.md"""

    def test_loads_authentication_config(self, tmp_path, monkeypatch):
        """Test loading authentication section from PIPER.user.md"""
        # Test implementation

    def test_loads_api_config(self, tmp_path, monkeypatch):
        """Test loading API configuration from PIPER.user.md"""
        # Test implementation

    def test_handles_missing_file(self, monkeypatch):
        """Test graceful handling of missing PIPER.user.md"""
        # Test implementation

    def test_handles_missing_notion_section(self, tmp_path, monkeypatch):
        """Test handling when notion: section is missing"""
        # Test implementation

    def test_handles_malformed_yaml(self, tmp_path, monkeypatch):
        """Test graceful handling of invalid YAML"""
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
        """Test partial environment variable override (some fields only)"""
        # Test implementation


class TestAuthenticationConfig:
    """Test authentication configuration loading"""

    def test_api_key_from_env(self, monkeypatch):
        """Test loading API key from environment variable"""
        # Test implementation

    def test_api_key_from_user_config(self, tmp_path, monkeypatch):
        """Test loading API key from PIPER.user.md"""
        # Test implementation

    def test_workspace_id_loading(self, tmp_path, monkeypatch):
        """Test workspace ID loads correctly"""
        # Test implementation

    def test_missing_authentication_section(self, tmp_path, monkeypatch):
        """Test handling of missing authentication section"""
        # Test implementation


class TestAPIConfig:
    """Test API configuration loading"""

    def test_base_url_configuration(self, tmp_path, monkeypatch):
        """Test API base URL configuration"""
        # Test implementation

    def test_timeout_configuration(self, tmp_path, monkeypatch):
        """Test timeout settings"""
        # Test implementation

    def test_retry_configuration(self, tmp_path, monkeypatch):
        """Test max retries configuration"""
        # Test implementation

    def test_rate_limit_configuration(self, tmp_path, monkeypatch):
        """Test rate limit configuration"""
        # Test implementation


class TestEdgeCases:
    """Test edge cases and error conditions"""

    def test_empty_piper_user_md(self, tmp_path, monkeypatch):
        """Test handling of empty PIPER.user.md file"""
        # Test implementation

    def test_notion_section_with_no_content(self, tmp_path, monkeypatch):
        """Test notion: section with no YAML block"""
        # Test implementation

    def test_partial_configuration(self, tmp_path, monkeypatch):
        """Test handling of partially specified configuration"""
        # Test implementation


# Add fixtures if needed
@pytest.fixture
def sample_notion_config():
    """Provide sample Notion configuration for testing"""
    return {
        "authentication": {
            "api_key": "test_api_key",
            "workspace_id": "test_workspace"
        },
        "api_base_url": "https://api.notion.com/v1",
        "timeout_seconds": 30,
        "max_retries": 3,
        "requests_per_minute": 30
    }
```

---

## Implementation Requirements

### Test Coverage Goals

Aim for comprehensive coverage of:
- ✅ All configuration loading paths
- ✅ All priority scenarios
- ✅ All error conditions
- ✅ All edge cases
- ✅ Integration with actual NotionConfigService

### Quality Standards

- Each test should be **independent** (no shared state)
- Tests should be **deterministic** (same result every time)
- Use **descriptive test names** (explain what's being tested)
- Include **docstrings** explaining test purpose
- Use **assertions** that provide clear failure messages
- **Monkeypatch** environment and file system (no side effects)

### Pattern Consistency

Follow Calendar's test patterns exactly:
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
   pytest tests/integration/test_notion_config_loading.py -v
   ```

2. **Check coverage**:
   ```bash
   pytest tests/integration/test_notion_config_loading.py --cov=services.integrations.notion.config_service
   ```

3. **Verify all scenarios pass**:
   - Basic initialization ✅
   - PIPER.user.md loading ✅
   - Priority system ✅
   - Error handling ✅
   - Edge cases ✅

4. **Run with different Python versions** (if applicable):
   ```bash
   pytest tests/integration/test_notion_config_loading.py
   ```

---

## Success Criteria

Your Step 2 is complete when:

- [ ] Test file created: `tests/integration/test_notion_config_loading.py`
- [ ] Comprehensive test coverage (15+ tests minimum)
- [ ] All test categories covered:
  - [ ] Basic functionality
  - [ ] PIPER.user.md loading
  - [ ] Priority system
  - [ ] Authentication config
  - [ ] API config
  - [ ] Edge cases
  - [ ] Error handling
- [ ] All tests passing
- [ ] Tests are independent and deterministic
- [ ] Pattern matches Calendar tests
- [ ] Descriptive test names and docstrings
- [ ] Proper use of fixtures and monkeypatching

---

## Key Testing Principles

### Independence
Each test should set up its own environment and clean up after itself. Use `tmp_path` and `monkeypatch` fixtures.

### Clarity
Test names and docstrings should make the purpose immediately clear. Someone reading the test should understand what's being verified without looking at the implementation.

### Completeness
Cover not just the happy path, but also:
- Missing files/sections
- Invalid data
- Partial configurations
- Priority conflicts
- Edge cases

### Confidence
After these tests pass, we should have complete confidence that Notion's configuration loading works correctly in all scenarios.

---

## Remember

- **Copy Calendar's test structure** - proven pattern
- **Test all scenarios thoroughly** - we're Time Lords, not rushing
- **Make tests independent** - no shared state between tests
- **Use clear assertions** - failure messages should be helpful
- **Document test purpose** - docstrings explain intent
- **Monkeypatch properly** - no side effects on actual files

---

**Focus on thoroughness and quality, not arbitrary time limits.**

**Create a test suite that gives complete confidence in the configuration system.**

**Ready to create comprehensive tests for Notion config loading!** 🧪
