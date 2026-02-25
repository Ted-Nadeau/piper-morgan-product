"""Tests for Notion configuration loading from PIPER.user.md.

Implements test coverage for NotionConfigService YAML loading functionality,
ensuring proper configuration priority order: env vars > PIPER.user.md > defaults.

Pattern based on Calendar configuration loading tests.

Issue #782: Updated to pass user_id parameter (required by Issue #734).
"""

import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from services.integrations.notion.config_service import (
    NotionConfig,
    NotionConfigService,
    NotionEnvironment,
)

# Test user ID for multi-tenancy (Issue #734)
TEST_USER_ID = "test_user_notion_config"


@pytest.fixture(autouse=True)
def isolate_config_service():
    """Isolate config service from external dependencies during tests.

    Issue #782: Config service has multiple fallback sources:
    1. Environment variables
    2. PIPER.user.md file
    3. Keychain service

    This fixture ensures tests aren't affected by real credentials.
    """
    # Clear any NOTION env vars that might interfere
    original_env = {}
    notion_vars = [k for k in os.environ if k.startswith("NOTION")]
    for var in notion_vars:
        original_env[var] = os.environ.pop(var)

    # Mock keychain to return None
    with patch("services.infrastructure.keychain_service.KeychainService") as mock:
        mock_instance = MagicMock()
        mock_instance.get_api_key.return_value = None
        mock.return_value = mock_instance
        yield mock

    # Restore original env vars
    os.environ.update(original_env)


class TestNotionConfigLoading:
    """Test NotionConfigService configuration loading from PIPER.user.md."""

    def test_loads_from_piper_user_md(self, tmp_path):
        """Test that config loads from PIPER.user.md when present."""
        # Create temporary PIPER.user.md with notion config
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
# Test Configuration

## 📝 Notion Integration

Configure Notion API integration.

```yaml
notion:
  authentication:
    api_key: "test_key_from_file"
    workspace_id: "test_workspace_from_file"
  api_base_url: "https://test.api.notion.com/v1"
  timeout_seconds: 60
  max_retries: 5
  requests_per_minute: 50
```

## Other Section
        """
        )

        # Patch Path to use temp file
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                # Load config
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Verify values from PIPER.user.md
                assert config.api_key == "test_key_from_file"
                assert config.workspace_id == "test_workspace_from_file"
                assert config.api_base_url == "https://test.api.notion.com/v1"
                assert config.timeout_seconds == 60
                assert config.max_retries == 5
                assert config.requests_per_minute == 50

    def test_env_vars_override_user_config(self, tmp_path):
        """Test that environment variables override PIPER.user.md."""
        # Create PIPER.user.md with one set of values
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  authentication:
    api_key: "user_config_key"
    workspace_id: "user_config_workspace"
  timeout_seconds: 30
  max_retries: 3
```
        """
        )

        # Set environment variables to override
        original_api_key = os.environ.get("NOTION_API_KEY")
        original_workspace_id = os.environ.get("NOTION_WORKSPACE_ID")
        original_timeout = os.environ.get("NOTION_TIMEOUT_SECONDS")

        os.environ["NOTION_API_KEY"] = "env_override_key"
        os.environ["NOTION_WORKSPACE_ID"] = "env_override_workspace"
        os.environ["NOTION_TIMEOUT_SECONDS"] = "90"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = NotionConfigService()
                    config = service.get_config(TEST_USER_ID)

                    # Verify env vars override user config
                    assert config.api_key == "env_override_key"
                    assert config.workspace_id == "env_override_workspace"
                    assert config.timeout_seconds == 90
                    # Verify non-overridden value still from user config
                    assert config.max_retries == 3
        finally:
            # Clean up environment
            if original_api_key is None:
                os.environ.pop("NOTION_API_KEY", None)
            else:
                os.environ["NOTION_API_KEY"] = original_api_key
            if original_workspace_id is None:
                os.environ.pop("NOTION_WORKSPACE_ID", None)
            else:
                os.environ["NOTION_WORKSPACE_ID"] = original_workspace_id
            if original_timeout is None:
                os.environ.pop("NOTION_TIMEOUT_SECONDS", None)
            else:
                os.environ["NOTION_TIMEOUT_SECONDS"] = original_timeout

    def test_defaults_when_no_config(self, tmp_path):
        """Test that defaults are used when neither PIPER.user.md nor env vars present."""
        # Create empty PIPER.user.md
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("# Empty config\n\nNo notion section here.")

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Verify defaults
                assert config.api_key == ""
                assert config.workspace_id == ""
                assert config.api_base_url == "https://api.notion.com/v1"
                assert config.timeout_seconds == 30
                assert config.max_retries == 3
                assert config.requests_per_minute == 30
                assert config.environment == NotionEnvironment.DEVELOPMENT

    def test_graceful_fallback_when_piper_missing(self, tmp_path):
        """Test graceful fallback when PIPER.user.md doesn't exist."""
        # Point to non-existent file
        with patch.object(Path, "exists", return_value=False):
            # Should not raise exception
            service = NotionConfigService()
            config = service.get_config(TEST_USER_ID)

            # Should use defaults
            assert config.api_key == ""
            assert config.timeout_seconds == 30
            assert config.max_retries == 3

    def test_graceful_fallback_when_yaml_malformed(self, tmp_path):
        """Test graceful fallback when PIPER.user.md has malformed YAML."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  bad: yaml: syntax: here:
  - invalid
  missing: quote
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                # Should not raise exception
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Should use defaults
                assert config.api_key == ""
                assert config.timeout_seconds == 30

    def test_authentication_section_parsing(self, tmp_path):
        """Test that authentication section is properly parsed from PIPER.user.md."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  authentication:
    api_key: "secret_test_api_key_123"
    workspace_id: "workspace_test_id_456"
  api_base_url: "https://custom.notion.api/v2"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Verify authentication section properly parsed
                assert config.api_key == "secret_test_api_key_123"
                assert config.workspace_id == "workspace_test_id_456"
                assert config.api_base_url == "https://custom.notion.api/v2"

    def test_missing_authentication_section(self, tmp_path):
        """Test handling when authentication section is missing from PIPER.user.md."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  timeout_seconds: 45
  max_retries: 5
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Should use defaults for authentication
                assert config.api_key == ""
                assert config.workspace_id == ""
                # But still load other config
                assert config.timeout_seconds == 45
                assert config.max_retries == 5

    def test_api_config_settings(self, tmp_path):
        """Test API configuration settings load correctly."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  api_base_url: "https://custom.api.notion.com/v1"
  timeout_seconds: 120
  max_retries: 10
  requests_per_minute: 60
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Verify API config
                assert config.api_base_url == "https://custom.api.notion.com/v1"
                assert config.timeout_seconds == 120
                assert config.max_retries == 10
                assert config.requests_per_minute == 60

    def test_environment_configuration(self, tmp_path):
        """Test environment setting from PIPER.user.md."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  environment: "production"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Verify environment parsed correctly
                assert config.environment == NotionEnvironment.PRODUCTION

    def test_env_var_environment_override(self, tmp_path):
        """Test that NOTION_ENVIRONMENT env var overrides PIPER.user.md."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  environment: "development"
```
        """
        )

        # Set environment variable
        original_env = os.environ.get("NOTION_ENVIRONMENT")
        os.environ["NOTION_ENVIRONMENT"] = "staging"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = NotionConfigService()
                    config = service.get_config(TEST_USER_ID)

                    # Verify env var overrides user config
                    assert config.environment == NotionEnvironment.STAGING
        finally:
            # Clean up environment
            if original_env is None:
                os.environ.pop("NOTION_ENVIRONMENT", None)
            else:
                os.environ["NOTION_ENVIRONMENT"] = original_env

    def test_configuration_priority_order_comprehensive(self, tmp_path):
        """Test comprehensive scenario with all three config layers."""
        # Create PIPER.user.md with middle-priority values
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  authentication:
    api_key: "user_api_key"
    workspace_id: "user_workspace"
  timeout_seconds: 45
  max_retries: 5
  api_base_url: "https://user.notion.com/v1"
```
        """
        )

        # Set one environment variable to override
        original_api_key = os.environ.get("NOTION_API_KEY")
        os.environ["NOTION_API_KEY"] = "env_api_key"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = NotionConfigService()
                    config = service.get_config(TEST_USER_ID)

                    # Verify priority order:
                    # 1. api_key from env var (highest)
                    assert config.api_key == "env_api_key"

                    # 2. workspace_id from PIPER.user.md (middle)
                    assert config.workspace_id == "user_workspace"
                    assert config.timeout_seconds == 45
                    assert config.max_retries == 5
                    assert config.api_base_url == "https://user.notion.com/v1"

                    # 3. requests_per_minute from defaults (lowest)
                    assert config.requests_per_minute == 30
        finally:
            # Clean up environment
            if original_api_key is None:
                os.environ.pop("NOTION_API_KEY", None)
            else:
                os.environ["NOTION_API_KEY"] = original_api_key

    def test_partial_configuration(self, tmp_path):
        """Test handling of partially specified configuration."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  authentication:
    api_key: "partial_key"
  timeout_seconds: 60
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Verify partial config loads
                assert config.api_key == "partial_key"
                assert config.timeout_seconds == 60
                # Verify defaults for missing fields
                assert config.workspace_id == ""
                assert config.max_retries == 3
                assert config.requests_per_minute == 30

    def test_empty_piper_user_md_file(self, tmp_path):
        """Test handling of completely empty PIPER.user.md file."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("")

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Should use all defaults
                assert config.api_key == ""
                assert config.timeout_seconds == 30
                assert config.max_retries == 3

    def test_notion_section_with_no_yaml_block(self, tmp_path):
        """Test notion section exists but has no YAML block."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

This section exists but has no YAML configuration.

Just some text here.
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Should gracefully fall back to defaults
                assert config.api_key == ""
                assert config.timeout_seconds == 30

    def test_rate_limit_configuration(self, tmp_path):
        """Test rate limit configuration from PIPER.user.md."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  requests_per_minute: 100
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                config = service.get_config(TEST_USER_ID)

                # Verify rate limit loaded
                assert config.requests_per_minute == 100

    def test_env_var_rate_limit_override(self, tmp_path):
        """Test NOTION_RATE_LIMIT_RPM env var overrides user config."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  requests_per_minute: 50
```
        """
        )

        # Set environment variable
        original_rate_limit = os.environ.get("NOTION_RATE_LIMIT_RPM")
        os.environ["NOTION_RATE_LIMIT_RPM"] = "120"

        try:
            with patch.object(Path, "exists", return_value=True):
                with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                    service = NotionConfigService()
                    config = service.get_config(TEST_USER_ID)

                    # Verify env var overrides
                    assert config.requests_per_minute == 120
        finally:
            # Clean up environment
            if original_rate_limit is None:
                os.environ.pop("NOTION_RATE_LIMIT_RPM", None)
            else:
                os.environ["NOTION_RATE_LIMIT_RPM"] = original_rate_limit


class TestNotionConfigServiceBasics:
    """Test basic NotionConfigService functionality."""

    def test_service_initializes_successfully(self):
        """Test that NotionConfigService initializes without errors."""
        service = NotionConfigService()
        assert service is not None
        assert hasattr(service, "_load_from_user_config")
        assert hasattr(service, "_load_config")
        assert hasattr(service, "get_config")

    def test_config_caching(self):
        """Test that config is cached after first load."""
        service = NotionConfigService()

        # First call loads config
        config1 = service.get_config(TEST_USER_ID)

        # Second call should return same instance (cached)
        config2 = service.get_config(TEST_USER_ID)

        assert config1 is config2

    def test_is_configured_method(self, tmp_path):
        """Test is_configured method returns correct status."""
        # With API key
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text(
            """
## 📝 Notion Integration

```yaml
notion:
  authentication:
    api_key: "test_key"
```
        """
        )

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = NotionConfigService()
                assert service.is_configured(TEST_USER_ID) is True

        # Without API key (should return False)
        empty_config = tmp_path / "PIPER.empty.md"
        empty_config.write_text("")

        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=empty_config.read_text()):
                service2 = NotionConfigService()
                assert service2.is_configured(TEST_USER_ID) is False
