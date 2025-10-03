"""
GitHub Configuration Service
Implements ADR-010 Configuration Access Patterns for GitHub integration components.

Provides centralized configuration management for GitHub operations including:
- Authentication and token management
- API rate limiting and retry configuration
- Feature flags for GitHub integrations
- Environment-specific settings
"""

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from services.infrastructure.config.feature_flags import FeatureFlags


class GitHubEnvironment(Enum):
    """GitHub environment types"""

    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TESTING = "testing"


@dataclass
class GitHubRetryConfig:
    """GitHub API retry configuration following ADR-010 patterns"""

    max_attempts: int = 3
    base_delay_seconds: float = 1.0
    max_delay_seconds: float = 60.0
    exponential_base: float = 2.0
    rate_limit_retry_enabled: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "max_attempts": self.max_attempts,
            "base_delay_seconds": self.base_delay_seconds,
            "max_delay_seconds": self.max_delay_seconds,
            "exponential_base": self.exponential_base,
            "rate_limit_retry_enabled": self.rate_limit_retry_enabled,
        }


@dataclass
class GitHubClientConfig:
    """GitHub client configuration following ADR-010 patterns"""

    token: Optional[str] = None
    user_agent: str = "Piper-Morgan-PM/1.0"
    timeout_seconds: int = 30
    per_page: int = 30
    enable_metrics: bool = True
    retry_config: GitHubRetryConfig = field(default_factory=GitHubRetryConfig)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "token": "***" if self.token else None,  # Mask token in serialization
            "user_agent": self.user_agent,
            "timeout_seconds": self.timeout_seconds,
            "per_page": self.per_page,
            "enable_metrics": self.enable_metrics,
            "retry_config": self.retry_config.to_dict(),
        }


class GitHubConfigService:
    """
    Centralized GitHub configuration service implementing ADR-010 patterns.

    Provides configuration access for GitHub integration components following
    the established patterns for Application/Domain layer services.

    Implements standard config service interface for plugin architecture:
    - get_config() -> dict: Returns complete configuration
    - is_configured() -> bool: Validates required config present
    - _load_config() -> dict: Loads config from environment

    GitHub-specific extensions:
    - get_client_configuration(): Returns GitHubClientConfig object
    - get_authentication_token(): Returns GitHub auth token
    - get_default_repository(): Returns default repository
    - get_configuration_summary(): Returns masked config for debugging
    """

    def __init__(self, environment: Optional[GitHubEnvironment] = None):
        self._environment = environment or self._detect_environment()
        self._config_cache: Dict[str, Any] = {}
        self._client_config: Optional[GitHubClientConfig] = None

    def _detect_environment(self) -> GitHubEnvironment:
        """Detect current environment from infrastructure layer"""
        env_name = os.getenv("PIPER_ENVIRONMENT", "development").lower()

        environment_mapping = {
            "prod": GitHubEnvironment.PRODUCTION,
            "production": GitHubEnvironment.PRODUCTION,
            "staging": GitHubEnvironment.STAGING,
            "stage": GitHubEnvironment.STAGING,
            "dev": GitHubEnvironment.DEVELOPMENT,
            "development": GitHubEnvironment.DEVELOPMENT,
            "test": GitHubEnvironment.TESTING,
            "testing": GitHubEnvironment.TESTING,
        }

        return environment_mapping.get(env_name, GitHubEnvironment.DEVELOPMENT)

    def get_authentication_token(self) -> Optional[str]:
        """
        Get GitHub authentication token with environment-specific handling.

        Follows ADR-010: ConfigService for application layer configuration access.
        """
        # Check cache first
        if "auth_token" in self._config_cache:
            return self._config_cache["auth_token"]

        # Environment-specific token resolution
        token_env_vars = [
            "GITHUB_TOKEN",
            f"GITHUB_TOKEN_{self._environment.value.upper()}",
            "GITHUB_API_TOKEN",
            "GH_TOKEN",
        ]

        token = None
        for env_var in token_env_vars:
            token = os.getenv(env_var)
            if token:
                break

        # Cache the result
        self._config_cache["auth_token"] = token
        return token

    def get_default_repository(self) -> Optional[str]:
        """Get default GitHub repository for issue creation"""
        if "default_repo" in self._config_cache:
            return self._config_cache["default_repo"]

        # Environment-specific repository configuration
        repo_env_vars = [
            "GITHUB_DEFAULT_REPO",
            f"GITHUB_REPO_{self._environment.value.upper()}",
            "PIPER_GITHUB_REPO",
        ]

        repo = None
        for env_var in repo_env_vars:
            repo = os.getenv(env_var)
            if repo:
                break

        self._config_cache["default_repo"] = repo
        return repo

    def get_client_configuration(self) -> GitHubClientConfig:
        """
        Get comprehensive GitHub client configuration.

        Returns environment-specific configuration for GitHub API client
        following ADR-010 configuration access patterns.
        """
        if self._client_config:
            return self._client_config

        # Build retry configuration based on environment
        retry_config = GitHubRetryConfig()

        if self._environment == GitHubEnvironment.PRODUCTION:
            retry_config.max_attempts = 5
            retry_config.max_delay_seconds = 120.0
            retry_config.rate_limit_retry_enabled = True
        elif self._environment == GitHubEnvironment.TESTING:
            retry_config.max_attempts = 1
            retry_config.base_delay_seconds = 0.1
            retry_config.rate_limit_retry_enabled = False

        # Build client configuration
        self._client_config = GitHubClientConfig(
            token=self.get_authentication_token(),
            user_agent=f"Piper-Morgan-PM/1.0 ({self._environment.value})",
            timeout_seconds=self._get_timeout_config(),
            per_page=self._get_pagination_config(),
            enable_metrics=self._should_enable_metrics(),
            retry_config=retry_config,
        )

        return self._client_config

    def _get_timeout_config(self) -> int:
        """Get API timeout configuration"""
        timeout_str = os.getenv("GITHUB_API_TIMEOUT", "30")
        try:
            return int(timeout_str)
        except ValueError:
            return 30

    def _get_pagination_config(self) -> int:
        """Get API pagination configuration"""
        per_page_str = os.getenv("GITHUB_API_PER_PAGE", "30")
        try:
            return min(100, max(1, int(per_page_str)))  # GitHub limits: 1-100
        except ValueError:
            return 30

    def _should_enable_metrics(self) -> bool:
        """Determine if metrics collection should be enabled"""
        if self._environment == GitHubEnvironment.TESTING:
            return False

        metrics_env = os.getenv("GITHUB_ENABLE_METRICS", "true").lower()
        return metrics_env in ("true", "1", "yes", "on")

    def is_feature_enabled(self, feature_name: str) -> bool:
        """
        Check if a GitHub-specific feature is enabled.

        Integrates with FeatureFlags utility following ADR-010 patterns.
        """
        feature_flag_methods = {
            "production_client": self._is_production_client_enabled,
            "enhanced_error_handling": self._is_enhanced_error_handling_enabled,
            "content_generation": self._is_content_generation_enabled,
            "rate_limit_monitoring": self._is_rate_limit_monitoring_enabled,
            "issue_template_validation": self._is_issue_template_validation_enabled,
        }

        if feature_name in feature_flag_methods:
            return feature_flag_methods[feature_name]()

        # Fallback to general feature flags
        return FeatureFlags.is_debug_mode_enabled() if feature_name == "debug" else False

    def _is_production_client_enabled(self) -> bool:
        """Check if production GitHub client should be used"""
        if self._environment == GitHubEnvironment.TESTING:
            return False

        return os.getenv("GITHUB_USE_PRODUCTION_CLIENT", "true").lower() in (
            "true",
            "1",
            "yes",
            "on",
        )

    def _is_enhanced_error_handling_enabled(self) -> bool:
        """Check if enhanced error handling is enabled"""
        return self._environment != GitHubEnvironment.TESTING

    def _is_content_generation_enabled(self) -> bool:
        """Check if LLM-powered content generation is enabled"""
        if self._environment == GitHubEnvironment.TESTING:
            return False

        return os.getenv("GITHUB_ENABLE_CONTENT_GENERATION", "true").lower() in (
            "true",
            "1",
            "yes",
            "on",
        )

    def _is_rate_limit_monitoring_enabled(self) -> bool:
        """Check if rate limit monitoring is enabled"""
        return self._environment == GitHubEnvironment.PRODUCTION

    def _is_issue_template_validation_enabled(self) -> bool:
        """Check if issue template validation is enabled"""
        return self._environment in (GitHubEnvironment.PRODUCTION, GitHubEnvironment.STAGING)

    def get_allowed_repositories(self) -> List[str]:
        """
        Get list of repositories allowed for operations.

        Returns environment-specific repository allowlist for security.
        """
        if "allowed_repos" in self._config_cache:
            return self._config_cache["allowed_repos"]

        repos_env = os.getenv("GITHUB_ALLOWED_REPOS", "")
        if repos_env:
            repos = [repo.strip() for repo in repos_env.split(",") if repo.strip()]
        else:
            # Default based on environment
            default_repo = self.get_default_repository()
            repos = [default_repo] if default_repo else []

        self._config_cache["allowed_repos"] = repos
        return repos

    def is_repository_allowed(self, repo_name: str) -> bool:
        """Check if operations are allowed on the specified repository"""
        allowed_repos = self.get_allowed_repositories()

        # If no allowlist is configured, allow all repositories
        if not allowed_repos:
            return True

        return repo_name in allowed_repos

    def get_environment(self) -> GitHubEnvironment:
        """Get current environment"""
        return self._environment

    def get_configuration_summary(self) -> Dict[str, Any]:
        """
        Get summary of current configuration for debugging/monitoring.

        Returns masked configuration data suitable for logging/debugging.
        """
        client_config = self.get_client_configuration()

        return {
            "environment": self._environment.value,
            "has_authentication_token": self.get_authentication_token() is not None,
            "default_repository": self.get_default_repository(),
            "allowed_repositories_count": len(self.get_allowed_repositories()),
            "client_configuration": client_config.to_dict(),
            "feature_flags": {
                "production_client": self.is_feature_enabled("production_client"),
                "enhanced_error_handling": self.is_feature_enabled("enhanced_error_handling"),
                "content_generation": self.is_feature_enabled("content_generation"),
                "rate_limit_monitoring": self.is_feature_enabled("rate_limit_monitoring"),
                "issue_template_validation": self.is_feature_enabled("issue_template_validation"),
            },
        }

    # ===== Standard Config Service Interface (for plugin architecture) =====

    def get_config(self) -> Dict[str, Any]:
        """
        Returns complete configuration dictionary (standard interface).

        Implements standard config service interface for plugin architecture.
        Returns dictionary with all GitHub configuration including authentication,
        repository settings, and feature flags.

        Returns:
            Dict[str, Any]: Complete GitHub configuration
        """
        return self.get_configuration_summary()

    def is_configured(self) -> bool:
        """
        Returns True if all required config present (standard interface).

        Implements standard config service interface for plugin architecture.
        Checks if GitHub authentication token is available, which is the
        minimum requirement for GitHub operations.

        Returns:
            bool: True if GitHub is properly configured
        """
        try:
            token = self.get_authentication_token()
            return bool(token)
        except Exception:
            return False

    def _load_config(self) -> Dict[str, Any]:
        """
        Private method to load config from environment (standard interface).

        Implements standard config service interface for plugin architecture.
        GitHub's config loading is handled dynamically in __init__ and getter methods.
        This method provides the standard interface by returning current config.

        Returns:
            Dict[str, Any]: Current configuration state
        """
        return self.get_config()

    # ===== Utility Methods =====

    def clear_cache(self):
        """Clear configuration cache (useful for testing)"""
        self._config_cache.clear()
        self._client_config = None
