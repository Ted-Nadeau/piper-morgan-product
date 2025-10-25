"""
Provider-Specific Key Validation Service

Validates API key formats against provider-specific rules and patterns.
Ensures keys match expected formats before attempting validation or storage.

Issue #252 CORE-KEYS-STRENGTH-VALIDATION
"""

import logging
import re
from dataclasses import dataclass
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    """Result of key format validation"""

    valid: bool
    message: str
    provider: str
    warnings: List[str] = None

    def __post_init__(self):
        if self.warnings is None:
            self.warnings = []


class ProviderKeyValidator:
    """Validates API keys against provider-specific format rules"""

    def __init__(self):
        """Initialize provider key validator with format rules"""
        self.rules = {
            "openai": {
                "prefixes": ["sk-"],
                "min_length": 50,
                "max_length": 60,
                "pattern": r"^sk-[A-Za-z0-9]{48,}$",
                "description": "OpenAI API key (starts with 'sk-')",
            },
            "anthropic": {
                "prefixes": ["sk-ant-"],
                "min_length": 100,
                "max_length": 120,
                "pattern": r"^sk-ant-[A-Za-z0-9\-_]{100,}$",
                "description": "Anthropic API key (starts with 'sk-ant-')",
            },
            "github": {
                "prefixes": ["ghp_", "gho_", "ghu_", "ghs_"],
                "min_length": 40,
                "max_length": 50,
                "pattern": r"^gh[pous]_[A-Za-z0-9]{36,}$",
                "description": "GitHub token (starts with 'ghp_', 'gho_', 'ghu_', or 'ghs_')",
            },
            "perplexity": {
                "prefixes": ["pplx-"],
                "min_length": 40,
                "max_length": 80,
                "pattern": r"^pplx-[A-Za-z0-9\-_]{35,}$",
                "description": "Perplexity API key (starts with 'pplx-')",
            },
            "gemini": {
                "prefixes": ["AIza"],
                "min_length": 35,
                "max_length": 45,
                "pattern": r"^AIza[A-Za-z0-9\-_]{35,}$",
                "description": "Google Gemini API key (starts with 'AIza')",
            },
        }

    def validate_format(self, provider: str, api_key: str) -> ValidationResult:
        """
        Validate key format for specific provider

        Args:
            provider: Provider name (openai, anthropic, github, etc.)
            api_key: API key to validate

        Returns:
            ValidationResult with validation details
        """
        try:
            # Normalize provider name
            provider = provider.lower().strip()

            # Check if provider is supported
            if provider not in self.rules:
                return ValidationResult(
                    valid=True,  # Allow unknown providers
                    message=f"Provider '{provider}' not configured for format validation",
                    provider=provider,
                    warnings=[f"No format rules defined for {provider}"],
                )

            rules = self.rules[provider]
            warnings = []

            # Check basic requirements
            if not api_key or not isinstance(api_key, str):
                return ValidationResult(
                    valid=False, message="API key must be a non-empty string", provider=provider
                )

            # Trim whitespace
            api_key = api_key.strip()

            # Check prefix
            valid_prefix = any(api_key.startswith(prefix) for prefix in rules["prefixes"])
            if not valid_prefix:
                expected_prefixes = "', '".join(rules["prefixes"])
                return ValidationResult(
                    valid=False,
                    message=f"Key must start with '{expected_prefixes}' for {provider}",
                    provider=provider,
                )

            # Check length
            key_length = len(api_key)
            if key_length < rules["min_length"]:
                return ValidationResult(
                    valid=False,
                    message=f"Key too short (minimum {rules['min_length']} characters for {provider})",
                    provider=provider,
                )

            if key_length > rules["max_length"]:
                warnings.append(
                    f"Key longer than typical {provider} keys ({rules['max_length']} chars)"
                )

            # Check pattern
            if not re.match(rules["pattern"], api_key):
                return ValidationResult(
                    valid=False,
                    message=f"Key format invalid for {provider}. Expected: {rules['description']}",
                    provider=provider,
                )

            # Additional provider-specific checks
            provider_warnings = self._provider_specific_checks(provider, api_key)
            warnings.extend(provider_warnings)

            return ValidationResult(
                valid=True,
                message=f"Format valid for {provider}",
                provider=provider,
                warnings=warnings,
            )

        except Exception as e:
            logger.error(f"Error validating {provider} key format: {e}")
            return ValidationResult(
                valid=False, message=f"Validation error: {str(e)}", provider=provider
            )

    def _provider_specific_checks(self, provider: str, api_key: str) -> List[str]:
        """Perform additional provider-specific validation checks"""
        warnings = []

        if provider == "openai":
            # Check for old format keys
            if api_key.startswith("sk-") and len(api_key) < 51:
                warnings.append("This appears to be an older OpenAI key format")

            # Check for project keys vs user keys
            if "proj" in api_key:
                warnings.append("This appears to be a project-scoped key")

        elif provider == "github":
            # Check token type
            if api_key.startswith("ghp_"):
                warnings.append("Personal access token detected")
            elif api_key.startswith("gho_"):
                warnings.append("OAuth token detected")
            elif api_key.startswith("ghu_"):
                warnings.append("User-to-server token detected")
            elif api_key.startswith("ghs_"):
                warnings.append("Server-to-server token detected")

        elif provider == "anthropic":
            # Check for workspace keys
            if "ws" in api_key:
                warnings.append("This appears to be a workspace-scoped key")

        return warnings

    def detect_provider(self, api_key: str) -> Optional[str]:
        """
        Attempt to detect provider from key format

        Args:
            api_key: API key to analyze

        Returns:
            Detected provider name or None
        """
        if not api_key:
            return None

        api_key = api_key.strip()

        # Check each provider's prefixes
        for provider, rules in self.rules.items():
            for prefix in rules["prefixes"]:
                if api_key.startswith(prefix):
                    # Verify it matches the full pattern
                    if re.match(rules["pattern"], api_key):
                        return provider

        return None

    def get_provider_info(self, provider: str) -> Optional[Dict]:
        """Get format information for a provider"""
        provider = provider.lower().strip()
        if provider in self.rules:
            return self.rules[provider].copy()
        return None

    def list_supported_providers(self) -> List[str]:
        """Get list of supported providers"""
        return list(self.rules.keys())

    def validate_multiple_formats(self, api_key: str) -> List[ValidationResult]:
        """
        Validate key against all known provider formats

        Args:
            api_key: API key to validate

        Returns:
            List of validation results for each provider
        """
        results = []

        for provider in self.rules.keys():
            result = self.validate_format(provider, api_key)
            results.append(result)

        return results

    def get_format_help(self, provider: str) -> str:
        """Get help text for provider key format"""
        provider = provider.lower().strip()

        if provider not in self.rules:
            return f"No format information available for '{provider}'"

        rules = self.rules[provider]
        prefixes = "', '".join(rules["prefixes"])

        help_text = f"""
{rules['description']}

Format Requirements:
• Must start with: '{prefixes}'
• Length: {rules['min_length']}-{rules['max_length']} characters
• Pattern: {rules['pattern']}

Example: {rules['prefixes'][0]}{'x' * (rules['min_length'] - len(rules['prefixes'][0]))}
        """.strip()

        return help_text
