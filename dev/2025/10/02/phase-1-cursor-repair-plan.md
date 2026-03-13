# GREAT-3A Phase 1: Config Artifact Repair Plan

**Date**: October 2, 2025
**Agent**: Cursor (Sonnet 4.5)
**Mission**: Design fixes for config dependency gaps from DDD refactoring
**Context**: ConfigValidator reveals code-level dependency gaps, not env var issues

## Executive Summary

**Root Cause Identified**: Notion integration is missing `config_service.py` entirely, explaining ConfigValidator gaps. Slack has proper config service implementation that should be replicated for Notion.

**Repair Strategy**: Hybrid Option A + B approach - Create missing Notion config service and update router to use it, following the working Slack pattern.

---

## 1. Config Service Pattern Analysis

### Working Pattern: Slack Integration

**File**: `services/integrations/slack/config_service.py`

**Key Components**:

- **Environment Enum**: `SlackEnvironment` (development, staging, production)
- **Config Dataclass**: `SlackConfig` with all settings and validation
- **Service Class**: `SlackConfigService` with environment variable loading
- **Validation**: `is_configured()` method for health checks
- **Feature Flag Integration**: Uses `FeatureFlags` service

**Router Integration Pattern**:

```python
# services/integrations/slack/slack_integration_router.py
def __init__(self, config_service=None):
    self.config_service = config_service
    if config_service:
        self.spatial_client = SlackClient(config_service)
```

**Key Methods**:

- `get_config()` - Returns config with env var loading
- `is_configured()` - Validates required settings
- `get_environment()` - Environment detection
- `_load_config()` - Environment variable mapping

### Non-Pattern: GitHub Integration

**File**: `services/integrations/github/config_service.py` (exists but unused)

**Issue**: GitHub has sophisticated config service but router doesn't use it directly. Router uses `FeatureFlags` only. This suggests GitHub config service is for direct GitHubAgent usage, not router pattern.

**Conclusion**: Slack pattern is the correct model for router-based integrations.

---

## 2. Slack Integration Assessment

### Current State: ✅ WORKING

**Structure**:

```
services/integrations/slack/
├── config_service.py          ✅ EXISTS - Complete implementation
├── slack_integration_router.py ✅ USES CONFIG - Proper pattern
└── slack_client.py            ✅ ACCEPTS CONFIG - From router
```

**Config Usage Flow**:

1. Router accepts `config_service` parameter in `__init__`
2. Router passes config to `SlackClient(config_service)`
3. Client uses config for authentication and settings

**Assessment**: No changes needed. This is the working pattern to replicate.

---

## 3. Notion Integration Assessment

### Current State: ❌ BROKEN

**Structure**:

```
services/integrations/notion/
├── config_service.py          ❌ MISSING - Root cause of gaps
└── notion_integration_router.py ❌ NO CONFIG - No config parameter
```

**Current Router Pattern**:

```python
def __init__(self):  # No config_service parameter
    self.spatial_notion = NotionMCPAdapter()  # No config passed
```

**Missing Components**:

1. **config_service.py** - Entire file missing
2. **Router config integration** - No config_service parameter
3. **Adapter config flow** - NotionMCPAdapter gets no config

**Assessment**: Complete config layer missing. Explains ConfigValidator gaps.

---

## 4. Repair Strategy: Hybrid Option A + B

### Phase 1: Create Notion Config Service (Option A)

**Target**: `services/integrations/notion/config_service.py`

**Implementation**: Follow Slack pattern exactly, adapted for Notion

**Required Environment Variables**:

- `NOTION_API_KEY` - Primary authentication
- `NOTION_ENVIRONMENT` - Environment detection
- `NOTION_TIMEOUT_SECONDS` - API timeout
- `NOTION_MAX_RETRIES` - Retry configuration

### Phase 2: Update Notion Router (Option B)

**Target**: `services/integrations/notion/notion_integration_router.py`

**Changes Required**:

1. Add `config_service` parameter to `__init__`
2. Store config service for adapter initialization
3. Pass config to `NotionMCPAdapter` if supported
4. Add graceful degradation when config missing

### Phase 3: Validate Integration

**Verification**: ConfigValidator should show Notion as configured when env vars present

---

## 5. Implementation Templates

### Template 1: Notion Config Service

**File**: `services/integrations/notion/config_service.py`

```python
"""
Notion Configuration Service
Implements ADR-010 Configuration Access Patterns for Notion integration components.

Provides centralized configuration management for Notion operations including:
- Authentication and API key management
- API rate limiting and retry configuration
- Feature flags for Notion integrations
- Environment-specific settings
"""

import os
from dataclasses import dataclass
from enum import Enum
from typing import Optional

from services.infrastructure.config.feature_flags import FeatureFlags


class NotionEnvironment(Enum):
    """Notion environment types"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class NotionConfig:
    """Notion configuration settings"""

    # Authentication
    api_key: str = ""

    # API Configuration
    api_base_url: str = "https://api.notion.com/v1"
    timeout_seconds: int = 30
    max_retries: int = 3

    # Rate Limiting
    requests_per_minute: int = 30  # Notion's rate limit

    # Feature Flags
    enable_spatial_mapping: bool = True

    # Environment
    environment: NotionEnvironment = NotionEnvironment.DEVELOPMENT

    def validate(self) -> bool:
        """Validate configuration settings"""
        return bool(self.api_key)


class NotionConfigService:
    """Notion configuration service following ADR-010 patterns"""

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        self._config: Optional[NotionConfig] = None

    def get_config(self) -> NotionConfig:
        """Get Notion configuration with environment variable loading"""
        if self._config is None:
            self._config = self._load_config()
        return self._config

    def _load_config(self) -> NotionConfig:
        """Load configuration from environment variables"""
        return NotionConfig(
            api_key=os.getenv("NOTION_API_KEY", ""),
            api_base_url=os.getenv("NOTION_API_BASE_URL", "https://api.notion.com/v1"),
            timeout_seconds=int(os.getenv("NOTION_TIMEOUT_SECONDS", "30")),
            max_retries=int(os.getenv("NOTION_MAX_RETRIES", "3")),
            requests_per_minute=int(os.getenv("NOTION_RATE_LIMIT_RPM", "30")),
            enable_spatial_mapping=self.feature_flags.is_enabled("notion_spatial_mapping"),
            environment=NotionEnvironment(os.getenv("NOTION_ENVIRONMENT", "development")),
        )

    def is_configured(self) -> bool:
        """Check if Notion is properly configured"""
        config = self.get_config()
        return config.validate()

    def get_environment(self) -> NotionEnvironment:
        """Get current Notion environment"""
        return self.get_config().environment

    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.get_environment() == NotionEnvironment.PRODUCTION
```

### Template 2: Notion Router Update

**File**: `services/integrations/notion/notion_integration_router.py`

**Changes to `__init__` method**:

```python
# BEFORE (current broken pattern):
def __init__(self):
    """Initialize router with feature flag checking"""
    # ... existing code ...
    self.spatial_notion = NotionMCPAdapter()

# AFTER (fixed pattern following Slack):
def __init__(self, config_service=None):
    """Initialize router with feature flag checking and config service"""
    # ... existing feature flag code ...

    # Store config service for adapter initialization
    self.config_service = config_service

    # Initialize spatial integration with config
    self.spatial_notion = None
    if self.use_spatial:
        try:
            from services.integrations.mcp.notion_adapter import NotionMCPAdapter

            # Pass config to adapter if available
            if config_service:
                self.spatial_notion = NotionMCPAdapter(config_service)
            else:
                # Graceful degradation - adapter handles missing config
                self.spatial_notion = NotionMCPAdapter()

        except ImportError as e:
            warnings.warn(f"Spatial Notion unavailable: {e}")
```

### Template 3: Service Usage Pattern

**For services that use NotionIntegrationRouter**:

```python
# BEFORE (current broken usage):
router = NotionIntegrationRouter()

# AFTER (fixed usage with config):
from services.integrations.notion.config_service import NotionConfigService

config_service = NotionConfigService()
router = NotionIntegrationRouter(config_service)
```

---

## 6. Validation Strategy

### Test Scenarios

#### Scenario 1: No Environment Variables (Graceful Degradation)

```bash
# Should not crash, should show "not configured" in ConfigValidator
python -m services.infrastructure.config.config_validator
```

**Expected**: Notion shows as "not configured" but system doesn't crash

#### Scenario 2: Partial Configuration (Warning)

```bash
# Should warn about missing config but not crash
NOTION_API_KEY=test_key python -m services.infrastructure.config.config_validator
```

**Expected**: Notion shows as "configured" with warnings about test key

#### Scenario 3: Full Configuration (Success)

```bash
# Should validate successfully
NOTION_API_KEY=secret_real_key python -m services.infrastructure.config.config_validator
```

**Expected**: Notion shows as "✅ configured" in ConfigValidator

### Integration Tests

1. **Router Initialization**: Verify router accepts config_service parameter
2. **Config Service Creation**: Verify NotionConfigService loads env vars correctly
3. **Adapter Integration**: Verify NotionMCPAdapter receives config (if supported)
4. **Feature Flag Integration**: Verify config service respects feature flags
5. **Error Handling**: Verify graceful degradation when config missing

### Success Metrics

- [ ] ConfigValidator shows Notion as configurable service
- [ ] Router accepts config_service parameter without errors
- [ ] Config service loads environment variables correctly
- [ ] System degrades gracefully when config missing
- [ ] No breaking changes to existing functionality

---

## 7. Execution Plan

### Order of Operations (Safest to Riskiest)

#### Step 1: Create Config Service (Low Risk)

- Create `services/integrations/notion/config_service.py`
- Test in isolation with ConfigValidator
- Verify environment variable loading

#### Step 2: Update Router Signature (Medium Risk)

- Add `config_service=None` parameter to router `__init__`
- Store config service but don't use it yet
- Test that existing usage still works

#### Step 3: Integrate Config Flow (Higher Risk)

- Pass config to NotionMCPAdapter (if supported)
- Add config validation to router initialization
- Test end-to-end config flow

#### Step 4: Update Service Usage (Highest Risk)

- Update services that create NotionIntegrationRouter
- Pass config_service to router constructor
- Test full integration with real services

### Rollback Plan

Each step maintains backward compatibility:

- Step 1: New file, no existing code changes
- Step 2: Optional parameter, existing calls still work
- Step 3: Graceful degradation when config missing
- Step 4: Can revert to old usage pattern if needed

---

## 8. Coordination with Code Agent

### Code Agent's Role

- **Identify specific gaps**: What exactly is ConfigValidator reporting?
- **Validate assumptions**: Confirm Notion is the primary issue
- **Test implementation**: Execute the repair templates
- **Verify fixes**: Confirm ConfigValidator gaps resolved

### Cursor Agent's Role (This Plan)

- **Design repair strategy**: How to fix identified gaps
- **Provide implementation templates**: Ready-to-use code
- **Plan validation approach**: How to prove fixes work
- **Ensure architectural consistency**: Follow established patterns

### Handoff Points

1. **After Code identifies gaps**: Adjust plan based on specific findings
2. **During implementation**: Provide additional templates if needed
3. **After fixes applied**: Validate repair strategy worked

---

## 9. Risk Assessment

### Low Risk

- Creating new config_service.py file (no existing dependencies)
- Following established Slack pattern (proven approach)
- Maintaining backward compatibility (optional parameters)

### Medium Risk

- Router signature changes (affects service instantiation)
- Config flow integration (new dependency paths)

### High Risk

- NotionMCPAdapter config integration (unknown if supported)
- Service usage updates (multiple files to change)

### Mitigation

- **Incremental approach**: Each step maintains existing functionality
- **Graceful degradation**: System works without config
- **Pattern replication**: Following proven Slack implementation
- **Comprehensive testing**: Multiple validation scenarios

---

**Plan Status**: ✅ READY FOR CODE AGENT COORDINATION
**Implementation Readiness**: HIGH - Templates prepared
**Risk Level**: MEDIUM - Incremental approach with rollback plan
**Expected Outcome**: ConfigValidator gaps resolved, Notion properly configured
