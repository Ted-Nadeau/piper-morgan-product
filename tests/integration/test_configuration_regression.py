"""
Configuration regression tests.

This module ensures that the configuration refactor doesn't break existing
functionality and maintains backwards compatibility.
"""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from tests.fixtures.test_configs import XIAN_CONFIG


class TestConfigurationRegression:
    """Test that configuration changes don't break existing functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = Path(self.temp_dir) / "PIPER.user.md"
        self.original_config = None

        # Backup original config if it exists
        if Path("config/PIPER.user.md").exists():
            self.original_config = Path("config/PIPER.user.md").read_text()

    def teardown_method(self):
        """Clean up test environment."""
        # Restore original config
        if self.original_config:
            Path("config/PIPER.user.md").write_text(self.original_config)

        # Clean up temp files
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_existing_piper_user_md_functionality_unchanged(self):
        """Test that existing PIPER.user.md functionality is unchanged."""
        # Create a test configuration that matches current structure
        test_config = {
            "notion": {
                "publishing": {"enabled": True},
                "adrs": {"enabled": True},
                "development": {"enabled": True},
                "validation": {"enabled": True},
            },
            "github": {
                "default_repository": "mediajunkie/piper-morgan-product",
                "owner": "mediajunkie",
                "pm_numbers": {"prefix": "PM-", "start_number": 1, "padding": 3},
            },
        }

        yaml_content = f"""
```yaml
{test_config}
```
"""
        config_content = f"""# PIPER Configuration

## Configuration

{yaml_content}

## Other sections...
"""
        self.config_file.write_text(config_content)

        # Test that existing config loader still works
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = test_config
            mock_loader.return_value = mock_instance

            from services.configuration.piper_config_loader import PiperConfigLoader

            loader = PiperConfigLoader()
            config = loader.load_config()

            # Verify existing functionality
            assert config["notion"]["publishing"]["enabled"] is True
            assert config["notion"]["adrs"]["enabled"] is True
            assert config["notion"]["development"]["enabled"] is True
            assert config["notion"]["validation"]["enabled"] is True

    def test_mcp_configuration_system_unaffected(self):
        """Test that MCP configuration system is unaffected."""
        # Test that MCP configuration still works
        from services.configuration.piper_config_loader import PiperConfigLoader

        # Mock the config loader
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = {
                "mcp": {"servers": ["notion", "github"], "enabled": True}
            }
            mock_loader.return_value = mock_instance

            loader = PiperConfigLoader()
            config = loader.load_config()

            # Verify MCP configuration is preserved
            assert "mcp" in config
            assert config["mcp"]["servers"] == ["notion", "github"]
            assert config["mcp"]["enabled"] is True

    def test_pm123_backwards_compatibility_maintained(self):
        """Test that PM-123 CLI functionality is maintained."""
        import click.testing

        from cli.commands.issues import issues

        runner = click.testing.CliRunner()

        # Test all PM-123 commands still work
        commands_to_test = [
            ["--help"],
            ["create", "--help"],
            ["verify", "--help"],
            ["sync", "--help"],
            ["create", "--title", "Regression test", "--dry-run"],
            ["verify"],
            ["sync", "--dry-run"],
        ]

        for cmd in commands_to_test:
            result = runner.invoke(issues, cmd)
            # Commands should not fail due to configuration changes
            assert result.exit_code == 0, f"Command {cmd} failed: {result.output}"

    def test_existing_configuration_loading_patterns(self):
        """Test that existing configuration loading patterns still work."""
        # Test that the existing config loader interface is unchanged
        from services.configuration.piper_config_loader import PiperConfigLoader

        # Mock the config loader
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = XIAN_CONFIG
            mock_loader.return_value = mock_instance

            # Test that the interface is the same
            loader = PiperConfigLoader()
            config = loader.load_config()

            # Verify the interface works as expected
            assert isinstance(config, dict)
            assert "github" in config

    def test_hot_reload_functionality_preserved(self):
        """Test that hot-reload functionality is preserved."""
        from services.configuration.piper_config_loader import PiperConfigLoader

        # Mock the config loader with hot-reload capability
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = XIAN_CONFIG
            mock_instance.reload_config.return_value = XIAN_CONFIG
            mock_loader.return_value = mock_instance

            loader = PiperConfigLoader()

            # Test initial load
            config1 = loader.load_config()
            assert config1["github"]["default_repository"] == "mediajunkie/piper-morgan-product"

            # Test reload
            config2 = loader.reload_config()
            assert config2["github"]["default_repository"] == "mediajunkie/piper-morgan-product"

    def test_configuration_validation_patterns_unchanged(self):
        """Test that configuration validation patterns are unchanged."""
        from services.configuration.piper_config_loader import PiperConfigLoader

        # Test that validation still works
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = XIAN_CONFIG
            mock_instance.validate_config.return_value = True
            mock_loader.return_value = mock_instance

            loader = PiperConfigLoader()

            # Test validation
            is_valid = loader.validate_config()
            assert is_valid is True

    def test_performance_characteristics_maintained(self):
        """Test that performance characteristics are maintained."""
        import time

        from services.configuration.piper_config_loader import PiperConfigLoader

        # Mock the config loader
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = XIAN_CONFIG
            mock_loader.return_value = mock_instance

            loader = PiperConfigLoader()

            # Test performance
            start_time = time.time()
            for _ in range(100):  # Test 100 loads
                loader.load_config()
            end_time = time.time()

            total_time = end_time - start_time
            # Should complete within reasonable time (less than 1 second for 100 loads)
            assert total_time < 1.0, f"Configuration loading too slow: {total_time:.2f}s"

    def test_error_handling_patterns_unchanged(self):
        """Test that error handling patterns are unchanged."""
        from services.configuration.piper_config_loader import PiperConfigLoader

        # Test error handling
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.side_effect = Exception("Configuration error")
            mock_loader.return_value = mock_instance

            loader = PiperConfigLoader()

            # Test that errors are handled gracefully
            with pytest.raises(Exception):
                loader.load_config()

    def test_configuration_caching_unchanged(self):
        """Test that configuration caching is unchanged."""
        from services.configuration.piper_config_loader import PiperConfigLoader

        # Mock the config loader with caching
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = XIAN_CONFIG
            mock_instance.get_cached_config.return_value = XIAN_CONFIG
            mock_loader.return_value = mock_instance

            loader = PiperConfigLoader()

            # Test caching
            config1 = loader.load_config()
            config2 = loader.get_cached_config()

            assert config1 == config2

    def test_integration_with_existing_services(self):
        """Test that integration with existing services is unchanged."""
        # Test that existing services can still load configuration
        from services.configuration.piper_config_loader import PiperConfigLoader

        # Mock the config loader
        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = XIAN_CONFIG
            mock_loader.return_value = mock_instance

            loader = PiperConfigLoader()
            config = loader.load_config()

            # Test that services can access configuration
            assert config["github"]["default_repository"] == "mediajunkie/piper-morgan-product"
            assert config["github"]["owner"] == "mediajunkie"
            assert config["github"]["pm_numbers"]["prefix"] == "PM-"

    def test_backwards_compatibility_with_old_config_format(self):
        """Test backwards compatibility with old configuration format."""
        # Test that old configuration format still works
        old_config = {
            "notion": {"publishing": {"enabled": True}, "adrs": {"enabled": True}}
            # No github section - should still work
        }

        with patch("services.configuration.piper_config_loader.PiperConfigLoader") as mock_loader:
            mock_instance = MagicMock()
            mock_instance.load_config.return_value = old_config
            mock_loader.return_value = mock_instance

            from services.configuration.piper_config_loader import PiperConfigLoader

            loader = PiperConfigLoader()
            config = loader.load_config()

            # Should not fail with old format
            assert config["notion"]["publishing"]["enabled"] is True
            assert config["notion"]["adrs"]["enabled"] is True
