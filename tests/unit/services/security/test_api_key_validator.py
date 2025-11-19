"""Tests for Enhanced API Key Validator"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.api.errors import ValidationError
from services.security.api_key_validator import (
    APIKeyValidator,
    ValidationReport,
)


class TestAPIKeyValidator:
    """Test enhanced API key validation"""

    @pytest.fixture
    def validator(self):
        """APIKeyValidator instance for testing"""
        return APIKeyValidator()

    @pytest.fixture
    def mock_llm_config(self, validator):
        """Mock LLM config service"""
        validator.llm_config = AsyncMock()
        return validator

    @pytest.mark.asyncio
    async def test_validate_openai_key_valid_format(self, mock_llm_config):
        """Test OpenAI key with valid format"""
        mock_llm_config.llm_config.validate_api_key.return_value = True

        # Valid OpenAI key format
        valid_key = "sk-" + "a" * 48

        report = await mock_llm_config.validate_api_key("openai", valid_key)

        assert report.is_valid is True
        assert report.provider == "openai"
        assert len(report.errors) == 0
        assert "format_validation" in report.checks_performed
        assert "live_api_validation" in report.checks_performed

    @pytest.mark.asyncio
    async def test_validate_openai_key_invalid_format(self, mock_llm_config):
        """Test OpenAI key with invalid format"""
        # Invalid format - too short
        invalid_key = "sk-short"

        report = await mock_llm_config.validate_api_key("openai", invalid_key)

        assert report.is_valid is False
        assert len(report.errors) == 1
        assert report.errors[0].code == ValidationResult.INVALID_FORMAT
        assert "format_validation" in report.checks_performed

    @pytest.mark.asyncio
    async def test_validate_anthropic_key_valid_format(self, mock_llm_config):
        """Test Anthropic key with valid format"""
        mock_llm_config.llm_config.validate_api_key.return_value = True

        # Valid Anthropic key format
        valid_key = "sk-ant-" + "a" * 95

        report = await mock_llm_config.validate_api_key("anthropic", valid_key)

        assert report.is_valid is True
        assert report.provider == "anthropic"
        assert len(report.errors) == 0

    @pytest.mark.asyncio
    async def test_validate_unknown_provider(self, mock_llm_config):
        """Test validation with unknown provider"""
        report = await mock_llm_config.validate_api_key("unknown_provider", "test-key")

        assert report.is_valid is False
        assert len(report.errors) == 1
        assert report.errors[0].code == ValidationResult.UNKNOWN_PROVIDER
        assert "provider_support" in report.checks_performed

    @pytest.mark.asyncio
    async def test_security_validation_test_key(self, mock_llm_config):
        """Test security validation catches test keys"""
        # Test key pattern
        test_key = "sk-testkey123456789012345678901234567890123456"

        report = await mock_llm_config.validate_api_key("openai", test_key)

        assert report.is_valid is False
        assert any(error.code == ValidationResult.SECURITY_RISK for error in report.errors)
        assert "security_validation" in report.checks_performed

    @pytest.mark.asyncio
    async def test_security_validation_leaked_key(self, mock_llm_config):
        """Test security validation catches leaked keys"""
        # Leaked key prefix
        leaked_key = "sk-leaked123456789012345678901234567890123456"

        report = await mock_llm_config.validate_api_key("openai", leaked_key)

        assert report.is_valid is False
        assert any(error.code == ValidationResult.SECURITY_RISK for error in report.errors)

    @pytest.mark.asyncio
    async def test_rate_limiting(self, mock_llm_config):
        """Test rate limiting functionality"""
        valid_key = "sk-" + "a" * 48
        mock_llm_config.llm_config.validate_api_key.return_value = True

        # Make multiple requests quickly
        for i in range(mock_llm_config.max_attempts_per_hour):
            report = await mock_llm_config.validate_api_key("openai", valid_key)
            if i < mock_llm_config.max_attempts_per_hour - 1:
                assert report.is_valid is True

        # Next request should be rate limited
        report = await mock_llm_config.validate_api_key("openai", valid_key)
        assert report.is_valid is False
        assert any(error.code == ValidationResult.RATE_LIMITED for error in report.errors)

    @pytest.mark.asyncio
    async def test_skip_rate_limit(self, mock_llm_config):
        """Test skipping rate limit for admin use"""
        valid_key = "sk-" + "a" * 48
        mock_llm_config.llm_config.validate_api_key.return_value = True

        # Exhaust rate limit
        for _ in range(mock_llm_config.max_attempts_per_hour):
            await mock_llm_config.validate_api_key("openai", valid_key)

        # Should be rate limited normally
        report = await mock_llm_config.validate_api_key("openai", valid_key)
        assert any(error.code == ValidationResult.RATE_LIMITED for error in report.errors)

        # Should work with skip_rate_limit=True
        report = await mock_llm_config.validate_api_key("openai", valid_key, skip_rate_limit=True)
        assert report.is_valid is True

    @pytest.mark.asyncio
    async def test_skip_api_check(self, mock_llm_config):
        """Test skipping live API validation"""
        valid_key = "sk-" + "a" * 48

        # Don't mock the API call - it should be skipped
        report = await mock_llm_config.validate_api_key("openai", valid_key, skip_api_check=True)

        assert report.is_valid is True
        assert "live_api_validation" not in report.checks_performed
        assert "format_validation" in report.checks_performed

    @pytest.mark.asyncio
    async def test_api_validation_failure(self, mock_llm_config):
        """Test API validation failure"""
        valid_key = "sk-" + "a" * 48
        mock_llm_config.llm_config.validate_api_key.return_value = False

        report = await mock_llm_config.validate_api_key("openai", valid_key)

        assert report.is_valid is False
        assert any(error.code == ValidationResult.INVALID_API for error in report.errors)

    @pytest.mark.asyncio
    async def test_api_validation_network_error(self, mock_llm_config):
        """Test API validation network error"""
        valid_key = "sk-" + "a" * 48
        mock_llm_config.llm_config.validate_api_key.side_effect = Exception("Network error")

        report = await mock_llm_config.validate_api_key("openai", valid_key)

        assert report.is_valid is False
        assert any(error.code == ValidationResult.NETWORK_ERROR for error in report.errors)

    def test_format_patterns_loaded(self, validator):
        """Test that format patterns are properly loaded"""
        patterns = validator.format_patterns

        assert "openai" in patterns
        assert "anthropic" in patterns
        assert "gemini" in patterns
        assert "perplexity" in patterns

        # Check OpenAI pattern
        openai_pattern = patterns["openai"]
        assert openai_pattern["prefix"] == "sk-"
        assert openai_pattern["length"] == 51

    def test_security_patterns_loaded(self, validator):
        """Test that security patterns are properly loaded"""
        patterns = validator.security_patterns

        assert "common_test_keys" in patterns
        assert "suspicious_patterns" in patterns
        assert "leaked_key_prefixes" in patterns

        assert len(patterns["common_test_keys"]) > 0
        assert len(patterns["suspicious_patterns"]) > 0

    def test_key_hashing(self, validator):
        """Test API key hashing for tracking"""
        key1 = "sk-test123456789012345678901234567890123456"
        key2 = "sk-test123456789012345678901234567890123457"

        hash1 = validator._hash_key(key1)
        hash2 = validator._hash_key(key2)

        assert hash1 != hash2
        assert len(hash1) == 16  # Truncated SHA256
        assert isinstance(hash1, str)

    def test_prefix_checking(self, validator):
        """Test prefix checking functionality"""
        # Single prefix
        assert validator._check_prefix("sk-test", "sk-") is True
        assert validator._check_prefix("test", "sk-") is False

        # Multiple prefixes
        assert validator._check_prefix("xoxb-test", ["xoxb-", "xoxp-"]) is True
        assert validator._check_prefix("xoxp-test", ["xoxb-", "xoxp-"]) is True
        assert validator._check_prefix("invalid-test", ["xoxb-", "xoxp-"]) is False

        # No prefix required
        assert validator._check_prefix("anything", None) is True

    def test_validation_stats(self, validator):
        """Test validation statistics"""
        stats = validator.get_validation_stats()

        assert "active_keys_tracked" in stats
        assert "total_attempts_last_hour" in stats
        assert "rate_limit_threshold" in stats
        assert "supported_providers" in stats
        assert "security_patterns_loaded" in stats

        assert stats["rate_limit_threshold"] == validator.max_attempts_per_hour
        assert len(stats["supported_providers"]) > 0

    def test_clear_rate_limits(self, validator):
        """Test clearing rate limits"""
        # Add some fake attempts
        validator.validation_attempts["test_hash"] = [datetime.now()]
        validator.validation_attempts["test_hash2"] = [datetime.now()]

        # Clear specific key
        cleared = validator.clear_rate_limits("test_hash")
        assert cleared == 1
        assert "test_hash" not in validator.validation_attempts
        assert "test_hash2" in validator.validation_attempts

        # Clear all
        cleared = validator.clear_rate_limits()
        assert cleared == 1
        assert len(validator.validation_attempts) == 0

    @pytest.mark.asyncio
    async def test_validation_report_metadata(self, mock_llm_config):
        """Test validation report includes metadata"""
        valid_key = "sk-" + "a" * 48
        mock_llm_config.llm_config.validate_api_key.return_value = True

        report = await mock_llm_config.validate_api_key("openai", valid_key)

        assert "validation_duration_ms" in report.metadata
        assert report.metadata["validation_duration_ms"] >= 0
        assert isinstance(report.validation_time, datetime)
        assert len(report.key_hash) == 16

    @pytest.mark.asyncio
    async def test_github_token_validation(self, mock_llm_config):
        """Test GitHub token format validation"""
        # Valid GitHub personal access token
        valid_token = "ghp_" + "a" * 36

        # Mock API validation (GitHub not in LLM config)
        mock_llm_config.llm_config.validate_api_key.return_value = False

        report = await mock_llm_config.validate_api_key("github", valid_token, skip_api_check=True)

        assert report.is_valid is True  # Format is valid, API check skipped
        assert "format_validation" in report.checks_performed

    @pytest.mark.asyncio
    async def test_slack_token_validation(self, mock_llm_config):
        """Test Slack token format validation"""
        # Valid Slack bot token
        valid_token = "xoxb-" + "a" * 50

        report = await mock_llm_config.validate_api_key("slack", valid_token, skip_api_check=True)

        assert report.is_valid is True
        assert "format_validation" in report.checks_performed


class TestConvenienceFunctions:
    """Test convenience functions"""

    @pytest.mark.asyncio
    @patch("services.security.api_key_validator.api_key_validator")
    async def test_validate_api_key_convenience(self, mock_validator):
        """Test validate_api_key convenience function"""
        mock_report = ValidationReport(
            is_valid=True,
            provider="openai",
            key_hash="test_hash",
            validation_time=datetime.now(),
            checks_performed=["test"],
        )
        mock_validator.validate_api_key.return_value = mock_report

        result = await validate_api_key("openai", "test-key")

        assert result == mock_report
        mock_validator.validate_api_key.assert_called_once_with("openai", "test-key", False, False)

    def test_get_supported_providers(self):
        """Test get_supported_providers convenience function"""
        providers = get_supported_providers()

        assert isinstance(providers, list)
        assert len(providers) > 0
        assert "openai" in providers
        assert "anthropic" in providers

    def test_get_provider_format_info(self):
        """Test get_provider_format_info convenience function"""
        # Valid provider
        info = get_provider_format_info("openai")
        assert info is not None
        assert "pattern" in info
        assert "description" in info

        # Invalid provider
        info = get_provider_format_info("invalid")
        assert info is None


class TestValidationReport:
    """Test ValidationReport dataclass"""

    def test_validation_report_creation(self):
        """Test ValidationReport creation and defaults"""
        report = ValidationReport(
            is_valid=True,
            provider="openai",
            key_hash="test_hash",
            validation_time=datetime.now(),
            checks_performed=["format"],
        )

        assert report.is_valid is True
        assert report.provider == "openai"
        assert len(report.errors) == 0
        assert len(report.warnings) == 0
        assert len(report.metadata) == 0


class TestValidationError:
    """Test ValidationError dataclass"""

    def test_validation_error_creation(self):
        """Test ValidationError creation and defaults"""
        error = ValidationError(code=ValidationResult.INVALID_FORMAT, message="Test error")

        assert error.code == ValidationResult.INVALID_FORMAT
        assert error.message == "Test error"
        assert len(error.details) == 0
        assert len(error.suggestions) == 0
