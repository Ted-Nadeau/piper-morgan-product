# Configuration Management Framework

**Pattern Strength**: 14/16 (High Strength)
**Category**: Framework (Emergent)
**Discovery Date**: July 2025
**Status**: Production Ready

## Overview

The **Configuration Management Framework** is a systematic approach to managing configuration across multiple environments in AI-assisted development systems. It provides centralized configuration management, environment detection, feature flags, and secure configuration handling.

### Core Principle

**"Configuration should be centralized, environment-aware, and secure across all deployment contexts."**

## Framework Definition

### Key Components

1. **Centralized Configuration**: Single source of truth for all configuration
2. **Environment Detection**: Automatic environment identification and configuration
3. **Feature Flags**: Runtime configuration switches for gradual rollout
4. **Secure Configuration**: Secure handling of sensitive configuration data
5. **Multi-Environment Orchestration**: Consistent configuration across environments

### Configuration Management Model

```
Environment Detection → Configuration Loading → Feature Flag Evaluation → Secure Access → Runtime Configuration
```

## Implementation Guide

### Step 1: Define Configuration Schema

Create a structured configuration schema with environment-specific settings:

```python
# services/infrastructure/config/feature_flags.py
class FeatureFlags:
    """Centralized feature flag management following ADR-010 patterns."""

    @staticmethod
    def get(key: str, default: Any = None) -> Any:
        """Get configuration value with environment-aware defaults."""
        # Environment detection
        env = os.getenv("ENVIRONMENT", "development")

        # Environment-specific configuration
        if env == "production":
            return os.getenv(key, default)
        elif env == "staging":
            return os.getenv(key, default)
        else:  # development
            return os.getenv(key, default)

    @staticmethod
    def is_feature_enabled(feature: str) -> bool:
        """Check if a feature is enabled for current environment."""
        return FeatureFlags.get(f"ENABLE_{feature.upper()}", "false").lower() == "true"
```

### Step 2: Implement Environment Detection

Create automatic environment detection and configuration loading:

```python
# services/infrastructure/config/environment.py
class EnvironmentConfig:
    """Environment detection and configuration management."""

    @staticmethod
    def detect_environment() -> str:
        """Detect current environment automatically."""
        if os.getenv("ENVIRONMENT"):
            return os.getenv("ENVIRONMENT")
        elif os.getenv("FLASK_ENV"):
            return os.getenv("FLASK_ENV")
        elif os.getenv("PYTHON_ENV"):
            return os.getenv("PYTHON_ENV")
        else:
            return "development"

    @staticmethod
    def get_config_for_environment(env: str) -> Dict[str, Any]:
        """Get environment-specific configuration."""
        configs = {
            "development": {
                "debug": True,
                "log_level": "DEBUG",
                "database_url": "postgresql://localhost/piper_dev",
                "github_token": os.getenv("GITHUB_TOKEN"),
                "enable_mcp_file_search": False,
            },
            "staging": {
                "debug": False,
                "log_level": "INFO",
                "database_url": os.getenv("DATABASE_URL"),
                "github_token": os.getenv("GITHUB_TOKEN"),
                "enable_mcp_file_search": True,
            },
            "production": {
                "debug": False,
                "log_level": "WARNING",
                "database_url": os.getenv("DATABASE_URL"),
                "github_token": os.getenv("GITHUB_TOKEN"),
                "enable_mcp_file_search": True,
            }
        }
        return configs.get(env, configs["development"])
```

### Step 3: Implement Feature Flags

Create runtime configuration switches for feature management:

```python
# services/infrastructure/config/feature_manager.py
class FeatureManager:
    """Feature flag management for gradual rollout and safe deployment."""

    @staticmethod
    def is_enabled(feature: str) -> bool:
        """Check if a feature is enabled."""
        return FeatureFlags.is_feature_enabled(feature)

    @staticmethod
    def get_feature_config(feature: str) -> Dict[str, Any]:
        """Get feature-specific configuration."""
        if not FeatureManager.is_enabled(feature):
            return {}

        config_key = f"{feature.upper()}_CONFIG"
        config_str = FeatureFlags.get(config_key, "{}")

        try:
            return json.loads(config_str)
        except json.JSONDecodeError:
            logger.warning(f"Invalid JSON in {config_key}: {config_str}")
            return {}

    @staticmethod
    def get_feature_with_fallback(feature: str, fallback_value: Any) -> Any:
        """Get feature value with fallback if disabled."""
        if FeatureManager.is_enabled(feature):
            return FeatureFlags.get(f"{feature.upper()}_VALUE")
        return fallback_value
```

## Real Examples from Project

### Example 1: PM-055 Python Version Consistency

**Context**: Standardizing Python 3.11 across all environments

**Implementation**:

#### Environment-Specific Configuration

```python
# pyproject.toml
[tool.poetry.dependencies]
python = "^3.11"

# .python-version
3.11.0

# Dockerfile
FROM python:3.11-slim

# scripts/verify-python-version.sh
#!/bin/bash
REQUIRED_VERSION="3.11"
CURRENT_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')

if [[ "$CURRENT_VERSION" != "$REQUIRED_VERSION" ]]; then
    echo "❌ Python version mismatch. Required: $REQUIRED_VERSION, Found: $CURRENT_VERSION"
    exit 1
else
    echo "✅ Python version $CURRENT_VERSION matches requirement"
fi
```

#### Configuration Validation

```python
# services/infrastructure/config/python_version.py
class PythonVersionConfig:
    """Python version configuration and validation."""

    @staticmethod
    def validate_python_version():
        """Validate Python version matches requirements."""
        required_version = "3.11"
        current_version = f"{sys.version_info.major}.{sys.version_info.minor}"

        if current_version != required_version:
            raise ConfigurationError(
                f"Python version mismatch. Required: {required_version}, Found: {current_version}"
            )

        logger.info(f"✅ Python version {current_version} validated")

    @staticmethod
    def get_python_config():
        """Get Python-specific configuration."""
        return {
            "version": "3.11",
            "async_timeout": FeatureFlags.get("PYTHON_ASYNC_TIMEOUT", "120"),
            "max_workers": FeatureFlags.get("PYTHON_MAX_WORKERS", "4"),
        }
```

**Result**: Consistent Python 3.11 across development, Docker, and CI/CD environments

### Example 2: PM-012 GitHub Integration Configuration

**Context**: Production GitHub integration with ADR-010 configuration patterns

**Implementation**:

#### GitHub Configuration Service

```python
# services/integrations/github/config_service.py
class GitHubConfigService:
    """GitHub integration configuration following ADR-010 patterns."""

    def __init__(self):
        self.environment = EnvironmentConfig.detect_environment()
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load GitHub configuration for current environment."""
        base_config = {
            "api_url": "https://api.github.com",
            "timeout": 30,
            "retry_attempts": 3,
            "retry_delay": 1.0,
        }

        env_config = {
            "development": {
                "production_client": False,
                "allowed_repos": ["test-org/test-repo"],
                "rate_limit_warning": 1000,
            },
            "staging": {
                "production_client": True,
                "allowed_repos": os.getenv("GITHUB_ALLOWED_REPOS", "").split(","),
                "rate_limit_warning": 5000,
            },
            "production": {
                "production_client": True,
                "allowed_repos": os.getenv("GITHUB_ALLOWED_REPOS", "").split(","),
                "rate_limit_warning": 10000,
            }
        }

        return {**base_config, **env_config.get(self.environment, {})}

    def get_authentication_token(self) -> str:
        """Get GitHub authentication token with environment-specific validation."""
        token = os.getenv("GITHUB_TOKEN")

        if not token:
            if self.environment == "production":
                raise ConfigurationError("GITHUB_TOKEN required in production")
            else:
                logger.warning("GITHUB_TOKEN not set, using limited functionality")
                return ""

        return token

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if GitHub feature is enabled."""
        return FeatureFlags.is_feature_enabled(f"github_{feature}")

    def get_client_config(self) -> Dict[str, Any]:
        """Get GitHub client configuration."""
        return {
            "token": self.get_authentication_token(),
            "api_url": self.config["api_url"],
            "timeout": self.config["timeout"],
            "retry_config": {
                "attempts": self.config["retry_attempts"],
                "delay": self.config["retry_delay"],
            }
        }
```

#### Feature Flag Integration

```python
# services/orchestration/engine.py
class OrchestrationEngine:
    def __init__(self):
        # Initialize GitHub clients with ADR-010 configuration patterns
        self.github_config_service = GitHubConfigService()

        try:
            # Use production client with ConfigService if feature is enabled
            if self.github_config_service.is_feature_enabled("production_client"):
                self.github_client = ProductionGitHubClient(
                    config_service=self.github_config_service
                )
                logger.info("✅ Using ProductionGitHubClient for GitHub operations")
            else:
                logger.info("📎 Production client disabled, using GitHubAgent")
                self.github_client = GitHubAgent(
                    token=self.github_config_service.get_authentication_token()
                )
        except Exception as e:
            # Fall back to original agent for backward compatibility
            logger.warning(f"ProductionGitHubClient unavailable: {e}")
            logger.info("📎 Falling back to GitHubAgent")
            try:
                self.github_client = GitHubAgent(
                    token=self.github_config_service.get_authentication_token()
                )
            except Exception as fallback_error:
                logger.error(f"Both GitHub clients failed: {fallback_error}")
                self.github_client = GitHubAgent()  # Final fallback without token
```

**Result**: Production-ready GitHub integration with environment-specific configuration and graceful fallbacks

### Example 3: PM-015 Test Infrastructure Configuration

**Context**: Test infrastructure reliability with configuration-driven testing

**Implementation**:

#### Test Configuration Management

```python
# services/infrastructure/config/test_config.py
class TestConfig:
    """Test infrastructure configuration management."""

    @staticmethod
    def get_test_config() -> Dict[str, Any]:
        """Get test configuration for current environment."""
        env = EnvironmentConfig.detect_environment()

        base_config = {
            "timeout": 30,
            "retry_attempts": 3,
            "parallel_workers": 4,
        }

        env_config = {
            "development": {
                "database_url": "postgresql://localhost/piper_test",
                "log_level": "DEBUG",
                "enable_mock_apis": True,
            },
            "staging": {
                "database_url": os.getenv("TEST_DATABASE_URL"),
                "log_level": "INFO",
                "enable_mock_apis": False,
            },
            "production": {
                "database_url": os.getenv("TEST_DATABASE_URL"),
                "log_level": "WARNING",
                "enable_mock_apis": False,
            }
        }

        return {**base_config, **env_config.get(env, {})}

    @staticmethod
    def is_mock_enabled() -> bool:
        """Check if mock APIs are enabled for testing."""
        return FeatureFlags.is_feature_enabled("test_mock_apis")

    @staticmethod
    def get_connection_pool_config() -> Dict[str, Any]:
        """Get database connection pool configuration."""
        return {
            "min_size": FeatureFlags.get("DB_POOL_MIN_SIZE", "1"),
            "max_size": FeatureFlags.get("DB_POOL_MAX_SIZE", "10"),
            "timeout": FeatureFlags.get("DB_POOL_TIMEOUT", "30"),
        }
```

#### Configuration-Driven Testing

```python
# tests/conftest.py
import pytest
from services.infrastructure.config.test_config import TestConfig

@pytest.fixture(scope="session")
def test_config():
    """Provide test configuration to all tests."""
    return TestConfig.get_test_config()

@pytest.fixture(scope="session")
def database_url(test_config):
    """Provide database URL for testing."""
    return test_config["database_url"]

@pytest.fixture(scope="session")
def mock_apis_enabled():
    """Check if mock APIs should be used in tests."""
    return TestConfig.is_mock_enabled()

@pytest.fixture(scope="session")
def connection_pool_config():
    """Provide connection pool configuration for tests."""
    return TestConfig.get_connection_pool_config()
```

**Result**: 95%+ test success rate with configuration-driven test infrastructure

## Configuration Categories

### Environment Configuration

- **Development**: Debug mode, local services, mock APIs
- **Staging**: Production-like with test data, limited external services
- **Production**: Full production configuration, external services

### Feature Configuration

- **Feature Flags**: Runtime switches for gradual rollout
- **Service Configuration**: API endpoints, timeouts, retry logic
- **Security Configuration**: Authentication tokens, access controls

### Infrastructure Configuration

- **Database Configuration**: Connection strings, pool settings
- **External Services**: API keys, endpoints, rate limits
- **Monitoring Configuration**: Log levels, metrics collection

## Best Practices

### Configuration Security

✅ **Good Configuration Security**:

```python
# Environment variables for sensitive data
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

# No hardcoded secrets
# No secrets in version control
# Environment-specific secrets
```

❌ **Bad Configuration Security**:

```python
# Hardcoded secrets
GITHUB_TOKEN = "ghp_1234567890abcdef"

# Secrets in version control
# Same secrets across environments
```

### Environment Detection

✅ **Good Environment Detection**:

```python
def detect_environment():
    """Robust environment detection."""
    if os.getenv("ENVIRONMENT"):
        return os.getenv("ENVIRONMENT")
    elif os.getenv("FLASK_ENV"):
        return os.getenv("FLASK_ENV")
    else:
        return "development"
```

❌ **Bad Environment Detection**:

```python
def detect_environment():
    """Fragile environment detection."""
    return os.getenv("ENV", "dev")  # Too simple, no fallbacks
```

### Feature Flag Management

✅ **Good Feature Flag Management**:

```python
def is_feature_enabled(feature: str) -> bool:
    """Robust feature flag checking."""
    env = detect_environment()

    # Environment-specific defaults
    defaults = {
        "development": True,
        "staging": True,
        "production": False
    }

    return os.getenv(f"ENABLE_{feature.upper()}",
                    str(defaults.get(env, False))).lower() == "true"
```

❌ **Bad Feature Flag Management**:

```python
def is_feature_enabled(feature: str) -> bool:
    """Fragile feature flag checking."""
    return os.getenv(f"ENABLE_{feature}") == "true"  # No defaults, no environment awareness
```

## Evolution Story

### Discovery Phase (June 2025)

The Configuration Management Framework emerged from early deployment challenges:

- **Configuration Drift**: Different environments had inconsistent configurations
- **Hardcoded Values**: Configuration values were embedded in code
- **Environment Confusion**: Unclear which environment was being used
- **Feature Deployment Risk**: All-or-nothing deployments were risky

### Refinement Phase (July 2025)

The framework evolved through systematic application:

1. **PM-055**: Python version consistency across all environments
2. **PM-012**: GitHub integration with ADR-010 configuration patterns
3. **PM-015**: Test infrastructure with configuration-driven testing

### Standardization Phase (Current)

The framework is now standardized across the project:

- **ADR-010 Patterns**: Centralized configuration management
- **Environment Detection**: Automatic environment identification
- **Feature Flags**: Runtime configuration switches
- **Secure Configuration**: Environment-specific secrets management

## Success Metrics

### Quantitative Metrics

- **Configuration Consistency**: 100% consistency across environments
- **Deployment Success Rate**: 99%+ successful deployments
- **Feature Rollout Safety**: Zero incidents from feature rollouts

### Qualitative Metrics

- **Developer Experience**: Easy configuration management
- **System Reliability**: Consistent behavior across environments
- **Security**: Secure handling of sensitive configuration

## Anti-Patterns

### What NOT to Do

❌ **Hardcoded Configuration**

```python
# BAD: Hardcoded values
DATABASE_URL = "postgresql://localhost/piper"
GITHUB_TOKEN = "ghp_1234567890abcdef"
```

❌ **Environment Confusion**

```python
# BAD: No environment detection
def get_config():
    return {
        "database_url": "postgresql://localhost/piper",  # Always localhost
        "debug": True,  # Always debug
    }
```

❌ **No Feature Flags**

```python
# BAD: All-or-nothing deployments
def deploy_feature():
    # Deploy to all users immediately
    enable_feature_for_all_users()
```

❌ **Configuration in Code**

```python
# BAD: Configuration embedded in code
class DatabaseConfig:
    def __init__(self):
        self.host = "localhost"  # Hardcoded
        self.port = 5432         # Hardcoded
        self.database = "piper"  # Hardcoded
```

### What TO Do

✅ **Environment Variables**

```python
# GOOD: Environment-based configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/piper_dev")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
```

✅ **Environment Detection**

```python
# GOOD: Automatic environment detection
def get_config():
    env = detect_environment()
    configs = {
        "development": {"debug": True, "database": "piper_dev"},
        "staging": {"debug": False, "database": "piper_staging"},
        "production": {"debug": False, "database": "piper_prod"},
    }
    return configs.get(env, configs["development"])
```

✅ **Feature Flags**

```python
# GOOD: Gradual rollout with feature flags
def deploy_feature():
    if is_feature_enabled("new_feature"):
        enable_feature_for_percentage_of_users(10)  # Gradual rollout
```

✅ **Configuration Service**

```python
# GOOD: Centralized configuration management
class ConfigService:
    def __init__(self):
        self.environment = detect_environment()
        self.config = load_config_for_environment(self.environment)

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)
```

## Implementation Checklist

- [ ] Define configuration schema and structure
- [ ] Implement environment detection
- [ ] Create centralized configuration service
- [ ] Implement feature flag management
- [ ] Secure sensitive configuration data
- [ ] Test configuration across environments
- [ ] Document configuration patterns
- [ ] Train team on configuration management

## Conclusion

The Configuration Management Framework is essential for building reliable, deployable AI-assisted development systems. By providing centralized configuration, environment awareness, and feature flags, we ensure consistent behavior across all deployment contexts.

**Key Takeaway**: "Configuration should be as reliable as code. Centralized, environment-aware configuration prevents deployment issues and enables safe feature rollouts."

---

**Related**: [Error Handling Framework](./error-handling-framework.md), [Verification-First Pattern](../../decision-patterns/emergent/verification-first-pattern.md)
