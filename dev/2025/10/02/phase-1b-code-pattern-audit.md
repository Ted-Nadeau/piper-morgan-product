# GREAT-3A Phase 1B: Config Pattern Audit

**Date**: October 2, 2025 - 2:14 PM PT
**Agent**: Claude Code (Sonnet 4.5 - Programmer)
**Session**: Phase 1B Config Pattern Audit
**Duration**: ~20 minutes (2:14 PM - 2:34 PM)
**GitHub Issue**: GREAT-3A (Config Pattern Consistency)

---

## Executive Summary

**Mission**: Quick audit to verify config pattern consistency across all 4 integrations.

**Chief Architect Decision**: All 4 integrations MUST use consistent service injection pattern for plugin architecture.

**Findings**:

| Integration | Has config_service.py? | Router Accepts Config? | Pattern Type | Needs Alignment? |
|-------------|------------------------|------------------------|--------------|------------------|
| **Slack** | ✅ Yes | ✅ Yes (param) | Service injection | ❌ NO (reference) |
| **GitHub** | ✅ Yes | ❌ **NO** | Service exists but unused | ✅ **YES** |
| **Notion** | ❌ No (static) | ❌ NO | Static utility | ✅ **YES** |
| **Calendar** | ❌ No | ❌ NO | Direct env access | ✅ **YES** |

**Pattern Consistency**: ⚠️ **1 of 4 integrations follow service injection pattern** (25% compliance)

**Alignment Required**: ✅ **3 integrations need pattern alignment** (GitHub, Notion, Calendar)

---

## Task 1: GitHub Config Pattern Analysis

### Current State

**Config Service File**: ✅ **EXISTS**
- **Location**: `services/integrations/github/config_service.py`
- **Size**: 11,769 bytes
- **Class**: `GitHubConfigService` (ADR-010 compliant)
- **Status**: Complete and working

**GitHubConfigService Implementation**:
```python
class GitHubConfigService:
    """
    Centralized GitHub configuration service implementing ADR-010 patterns.

    Provides configuration access for GitHub integration components following
    the established patterns for Application/Domain layer services.
    """

    def __init__(self, environment: Optional[GitHubEnvironment] = None):
        self._environment = environment or self._detect_environment()
        self._config_cache: Dict[str, Any] = {}
        self._client_config: Optional[GitHubClientConfig] = None

    def get_authentication_token(self) -> Optional[str]:
        """Get GitHub authentication token with environment-specific handling."""
        token_env_vars = [
            "GITHUB_TOKEN",
            f"GITHUB_TOKEN_{self._environment.value.upper()}",
            "GITHUB_API_TOKEN",
            "GH_TOKEN",
        ]
        ...

    def get_client_configuration(self) -> GitHubClientConfig:
        """Get comprehensive GitHub client configuration."""
        return GitHubClientConfig(
            token=self.get_authentication_token(),
            user_agent=f"Piper-Morgan-PM/1.0 ({self._environment.value})",
            timeout_seconds=self._get_timeout_config(),
            retry_config=retry_config,
        )
```

**Where GitHubConfigService IS Used**:
- ✅ `services/integrations/github/production_client.py:ProductionGitHubClient`

```python
class ProductionGitHubClient:
    def __init__(
        self,
        config_service: Optional[GitHubConfigService] = None,
    ):
        # ADR-010: Use ConfigService for application layer configuration
        self.config_service = config_service or GitHubConfigService()
        self.config = config or self.config_service.get_client_configuration()
```

**Where GitHubConfigService IS NOT Used**:
- ❌ `services/integrations/github/github_integration_router.py:GitHubIntegrationRouter`

```python
class GitHubIntegrationRouter:
    def __init__(self):
        """Initialize GitHub integration router with feature flag detection"""
        self.spatial_github = None
        self.legacy_github = None

        # Feature flag state
        self.use_spatial = FeatureFlags.should_use_spatial_github()
        self.allow_legacy = FeatureFlags.is_legacy_github_allowed()

        # NO config_service parameter!
        # NO self.config_service attribute!
```

### Pattern Analysis

**Pattern Type**: ⚠️ **Partial Service Injection**

**What Exists**:
- ✅ GitHubConfigService (complete, ADR-010 compliant)
- ✅ ProductionGitHubClient uses it
- ✅ Service injection pattern working in client layer

**What's Missing**:
- ❌ GitHubIntegrationRouter doesn't accept config_service parameter
- ❌ Router doesn't use config_service internally
- ❌ Router doesn't pass config_service to clients
- ❌ No dependency injection at router level

### Gap Analysis

**Is There a Gap?** ✅ **YES - Router bypass pattern**

**Evidence**:
1. ✅ GitHubConfigService exists and is complete
2. ✅ ProductionGitHubClient uses service injection
3. ❌ GitHubIntegrationRouter does NOT use service injection
4. ❌ Router creates clients without config_service

**The Problem**:
```python
# Router creates spatial GitHub without config
self.spatial_github = GitHubSpatialIntelligence()

# ProductionGitHubClient can accept config, but router doesn't pass it
# So client creates its own: self.config_service = config_service or GitHubConfigService()
```

**Impact**:
- Router can't inject config for testing
- Router can't control client configuration
- Plugin architecture needs router-level injection
- Breaks dependency injection chain

### Alignment Needed

✅ **YES - GitHub router needs service injection pattern**

**Required Changes**:

1. **Router signature**:
```python
# Current
def __init__(self):
    ...

# Should be
def __init__(self, config_service: Optional[GitHubConfigService] = None):
    self.config_service = config_service or GitHubConfigService()
```

2. **Client initialization**:
```python
# Current
self.spatial_github = GitHubSpatialIntelligence()

# Should be
self.spatial_github = GitHubSpatialIntelligence(config_service=self.config_service)
```

3. **Factory function**:
```python
# Add factory that accepts config_service
def create_github_router(config_service: Optional[GitHubConfigService] = None) -> GitHubIntegrationRouter:
    return GitHubIntegrationRouter(config_service)
```

---

## Task 2: Calendar Config Pattern Analysis

### Current State

**Config Service File**: ❌ **DOES NOT EXIST**
- No `services/integrations/calendar/config_service.py`
- No `CalendarConfigService` class
- No service injection infrastructure

**Current Pattern**: Direct environment variable access in adapter

**GoogleCalendarMCPAdapter** (lines 62-64):
```python
def __init__(self):
    super().__init__("google_calendar_mcp")
    ...

    # OAuth 2.0 configuration - DIRECT env access
    self._client_secrets_file = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json")
    self._token_file = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
    self._scopes = ["https://www.googleapis.com/auth/calendar.readonly"]
```

**CalendarIntegrationRouter** (no config parameter):
```python
def __init__(self):
    """Initialize router with feature flag checking"""
    self.use_spatial = FeatureFlags.should_use_spatial_calendar()
    self.allow_legacy = FeatureFlags.is_legacy_calendar_allowed()

    # Initialize spatial integration
    self.spatial_calendar = None
    if self.use_spatial:
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            self.spatial_calendar = GoogleCalendarMCPAdapter()
            # NO config passed!
```

### Pattern Analysis

**Pattern Type**: ❌ **Direct Environment Access** (anti-pattern for DDD)

**What Exists**:
- ✅ Environment variables work (GOOGLE_CLIENT_SECRETS_FILE, GOOGLE_TOKEN_FILE)
- ✅ Graceful defaults (credentials.json, token.json)
- ✅ System operational

**What's Missing**:
- ❌ No CalendarConfigService
- ❌ No service injection pattern
- ❌ Direct os.getenv() calls in adapter (infrastructure leak)
- ❌ No testability (can't inject test config)
- ❌ No centralized config management

### Gap Analysis

**Is There a Gap?** ✅ **YES - No service layer**

**Evidence**:
1. ❌ No CalendarConfigService exists
2. ❌ Adapter reads environment directly (os.getenv)
3. ❌ Router doesn't accept config parameter
4. ❌ No config abstraction layer

**The Problem**:
```python
# Adapter directly accesses infrastructure layer (os.getenv)
# This violates DDD layering:
# - Adapter is in domain/application layer
# - os.getenv is infrastructure layer
# - Should go through config service abstraction
```

**Impact**:
- Violates ADR-010 (config access patterns)
- Can't inject test configuration
- Can't swap environment configs
- Tight coupling to environment variables
- Plugin architecture needs abstraction

### Alignment Needed

✅ **YES - Calendar needs complete service injection pattern**

**Required Changes**:

1. **Create CalendarConfigService**:
```python
# NEW FILE: services/integrations/calendar/config_service.py

class CalendarConfigService:
    """Calendar configuration service following ADR-010 patterns"""

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        self._config: Optional[CalendarConfig] = None

    def get_config(self) -> CalendarConfig:
        """Get Calendar configuration with environment variable loading"""
        if self._config is None:
            self._config = self._load_config()
        return self._config

    def _load_config(self) -> CalendarConfig:
        """Load configuration from environment variables"""
        return CalendarConfig(
            client_secrets_file=os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json"),
            token_file=os.getenv("GOOGLE_TOKEN_FILE", "token.json"),
            scopes=["https://www.googleapis.com/auth/calendar.readonly"],
        )

@dataclass
class CalendarConfig:
    """Calendar configuration settings"""
    client_secrets_file: str = "credentials.json"
    token_file: str = "token.json"
    scopes: List[str] = field(default_factory=lambda: ["https://www.googleapis.com/auth/calendar.readonly"])
```

2. **Update Router**:
```python
# MODIFY: services/integrations/calendar/calendar_integration_router.py

def __init__(self, config_service: Optional[CalendarConfigService] = None):
    self.config_service = config_service or CalendarConfigService()

    self.use_spatial = FeatureFlags.should_use_spatial_calendar()

    if self.use_spatial:
        self.spatial_calendar = GoogleCalendarMCPAdapter(self.config_service)
```

3. **Update Adapter**:
```python
# MODIFY: services/mcp/consumer/google_calendar_adapter.py

def __init__(self, config_service: CalendarConfigService):
    super().__init__("google_calendar_mcp")
    self.config_service = config_service

    # Get config through service (not direct env access)
    config = self.config_service.get_config()
    self._client_secrets_file = config.client_secrets_file
    self._token_file = config.token_file
    self._scopes = config.scopes
```

---

## Task 3: Pattern Comparison Table

### Complete Pattern Analysis

| Integration | Has config_service.py? | Location | Router Accepts Config? | Client/Adapter Uses Config? | Pattern Type | Compliance | Needs Alignment? |
|-------------|------------------------|----------|------------------------|----------------------------|--------------|------------|------------------|
| **Slack** | ✅ Yes | `services/integrations/slack/` | ✅ Yes (optional param) | ✅ Yes (SlackClient) | **Service Injection** | ✅ COMPLIANT | ❌ NO (reference) |
| **GitHub** | ✅ Yes | `services/integrations/github/` | ❌ **NO** | ✅ Yes (ProductionGitHubClient) | **Partial Injection** | ⚠️ PARTIAL | ✅ **YES** |
| **Notion** | ❌ No | `config/` (static) | ❌ NO | ❌ No (static util) | **Static Utility** | ❌ NON-COMPLIANT | ✅ **YES** |
| **Calendar** | ❌ No | N/A | ❌ NO | ❌ No (direct env) | **Direct Env Access** | ❌ NON-COMPLIANT | ✅ **YES** |

### Pattern Details

#### Slack (✅ Reference Pattern)

**Service**: `services/integrations/slack/config_service.py`
- `SlackConfigService` class
- `SlackConfig` dataclass
- ADR-010 compliant

**Router**: Accepts config_service parameter
```python
def __init__(self, config_service=None):
    self.config_service = config_service
    if config_service:
        self.spatial_client = SlackClient(config_service)
```

**Client**: Uses config_service
```python
class SlackClient:
    def __init__(self, config_service: SlackConfigService):
        self.config_service = config_service
        config = self.config_service.get_config()
```

**Status**: ✅ **COMPLIANT** - This is the reference pattern

---

#### GitHub (⚠️ Partial)

**Service**: `services/integrations/github/config_service.py`
- `GitHubConfigService` class (complete)
- `GitHubClientConfig` dataclass
- ADR-010 compliant

**Router**: ❌ Does NOT accept config_service parameter
```python
def __init__(self):
    # NO config_service parameter!
    self.spatial_github = GitHubSpatialIntelligence()
```

**Client**: Uses config_service (but router doesn't inject it)
```python
class ProductionGitHubClient:
    def __init__(self, config_service: Optional[GitHubConfigService] = None):
        self.config_service = config_service or GitHubConfigService()
```

**Status**: ⚠️ **PARTIAL** - Service exists but router doesn't use injection pattern

**Gap**: Router-level injection missing

---

#### Notion (❌ Non-Compliant)

**Service**: `config/notion_config.py`
- `NotionConfig` static utility class
- NOT a service (just static methods)
- NOT ADR-010 compliant

**Router**: Does NOT accept config_service parameter
```python
def __init__(self):
    # NO config_service parameter!
    self.spatial_notion = NotionMCPAdapter()
```

**Adapter**: Creates own config internally
```python
class NotionMCPAdapter:
    def __init__(self):
        self.config = NotionConfig()  # Static utility, not injected
        api_key = self.config.get_api_key()  # Calls os.environ.get internally
```

**Status**: ❌ **NON-COMPLIANT** - Static utility pattern, no service injection

**Gap**: Need to create NotionConfigService and refactor to service injection

---

#### Calendar (❌ Non-Compliant)

**Service**: ❌ Does NOT exist
- No CalendarConfigService
- No config service infrastructure

**Router**: Does NOT accept config_service parameter
```python
def __init__(self):
    # NO config_service parameter!
    self.spatial_calendar = GoogleCalendarMCPAdapter()
```

**Adapter**: Direct environment access (anti-pattern)
```python
class GoogleCalendarMCPAdapter:
    def __init__(self):
        # Direct os.getenv calls (infrastructure leak)
        self._client_secrets_file = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json")
        self._token_file = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
```

**Status**: ❌ **NON-COMPLIANT** - Direct environment access, no abstraction

**Gap**: Need to create CalendarConfigService and implement full injection pattern

---

### Compliance Summary

**Pattern Compliance**: ⚠️ **25% (1 of 4)**

| Status | Count | Integrations |
|--------|-------|--------------|
| ✅ Compliant | 1 | Slack |
| ⚠️ Partial | 1 | GitHub |
| ❌ Non-Compliant | 2 | Notion, Calendar |

**Alignment Required**: 3 of 4 integrations (75%)

---

## Task 4: Specific Alignment Recommendations

### Alignment Priority

**P0 (Critical)**: Create missing config services
- Calendar: No service exists
- Notion: Static utility needs conversion

**P1 (High)**: Router pattern alignment
- GitHub: Add router-level injection
- Notion: Refactor to service pattern
- Calendar: Add router-level injection

**P2 (Medium)**: Adapter/client updates
- Notion: Remove static pattern
- Calendar: Remove direct env access

### GitHub Alignment Plan

**Status**: ⚠️ Service exists, router doesn't use it

**Changes Required**:

1. **Update Router Signature** (`github_integration_router.py`):
```python
# BEFORE
def __init__(self):
    self.spatial_github = None
    self.legacy_github = None
    self._initialize_integrations()

# AFTER
def __init__(self, config_service: Optional[GitHubConfigService] = None):
    self.config_service = config_service or GitHubConfigService()
    self.spatial_github = None
    self.legacy_github = None
    self._initialize_integrations()
```

2. **Pass Config to Clients** (`github_integration_router.py`):
```python
# BEFORE
def _initialize_integrations(self):
    if self.use_spatial:
        self.spatial_github = GitHubSpatialIntelligence()

# AFTER
def _initialize_integrations(self):
    if self.use_spatial:
        self.spatial_github = GitHubSpatialIntelligence(config_service=self.config_service)
```

3. **Update Factory** (`github_integration_router.py:create_github_router`):
```python
# BEFORE
def create_github_router() -> GitHubIntegrationRouter:
    return GitHubIntegrationRouter()

# AFTER
def create_github_router(config_service: Optional[GitHubConfigService] = None) -> GitHubIntegrationRouter:
    return GitHubIntegrationRouter(config_service)
```

**Effort**: LOW (service already exists, just wire it up)
**Time**: 30 minutes

---

### Notion Alignment Plan

**Status**: ❌ Static utility, needs service conversion

**Changes Required**:

1. **Create NotionConfigService** (NEW FILE: `services/integrations/notion/config_service.py`):
```python
"""
Notion Configuration Service
Implements ADR-010 Configuration Access Patterns for Notion integration components.
"""

import os
from dataclasses import dataclass
from typing import Optional

from services.infrastructure.config.feature_flags import FeatureFlags


@dataclass
class NotionConfig:
    """Notion configuration settings"""

    # Authentication
    api_key: str = ""
    workspace_id: str = ""

    # API Configuration
    api_base_url: str = "https://api.notion.com/v1"
    timeout_seconds: int = 30
    max_retries: int = 3

    # Notion API version
    notion_version: str = "2022-06-28"

    def validate(self) -> bool:
        """Validate configuration settings"""
        if not self.api_key:
            return False
        if not (self.api_key.startswith("secret_") or self.api_key.startswith("ntn_")):
            return False
        return True


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
            workspace_id=os.getenv("NOTION_WORKSPACE_ID", ""),
            api_base_url=os.getenv("NOTION_API_BASE_URL", "https://api.notion.com/v1"),
            timeout_seconds=int(os.getenv("NOTION_TIMEOUT_SECONDS", "30")),
            max_retries=int(os.getenv("NOTION_MAX_RETRIES", "3")),
            notion_version=os.getenv("NOTION_VERSION", "2022-06-28"),
        )

    def is_configured(self) -> bool:
        """Check if Notion is properly configured"""
        config = self.get_config()
        return config.validate()

    def get_config_status(self) -> dict:
        """Get detailed configuration status"""
        config = self.get_config()
        return {
            "api_key_set": bool(config.api_key),
            "api_key_format_valid": bool(
                config.api_key and (config.api_key.startswith("secret_") or config.api_key.startswith("ntn_"))
            ),
            "workspace_id_set": bool(config.workspace_id),
            "fully_configured": self.is_configured(),
        }
```

2. **Update Router** (`notion_integration_router.py`):
```python
# BEFORE
def __init__(self):
    self.use_spatial = FeatureFlags.should_use_spatial_notion()
    if self.use_spatial:
        from services.integrations.mcp.notion_adapter import NotionMCPAdapter
        self.spatial_notion = NotionMCPAdapter()

# AFTER
from .config_service import NotionConfigService

def __init__(self, config_service: Optional[NotionConfigService] = None):
    self.config_service = config_service or NotionConfigService()
    self.use_spatial = FeatureFlags.should_use_spatial_notion()
    if self.use_spatial:
        from services.integrations.mcp.notion_adapter import NotionMCPAdapter
        self.spatial_notion = NotionMCPAdapter(self.config_service)
```

3. **Update Adapter** (`services/integrations/mcp/notion_adapter.py`):
```python
# BEFORE
from config.notion_config import NotionConfig

class NotionMCPAdapter(BaseSpatialAdapter):
    def __init__(self):
        super().__init__("notion_mcp")
        self.config = NotionConfig()
        self._initialize_client()

    def _initialize_client(self):
        api_key = self.config.get_api_key()  # Static method call
        if api_key:
            self._notion_client = Client(auth=api_key)

# AFTER
from services.integrations.notion.config_service import NotionConfigService

class NotionMCPAdapter(BaseSpatialAdapter):
    def __init__(self, config_service: NotionConfigService):
        super().__init__("notion_mcp")
        self.config_service = config_service
        self._initialize_client()

    def _initialize_client(self):
        config = self.config_service.get_config()  # Service method call
        if config.api_key:
            self._notion_client = Client(auth=config.api_key)
```

4. **Remove Old Config** (optional cleanup):
```bash
# DEPRECATED: config/notion_config.py
# Can be removed after migration complete
```

**Effort**: MEDIUM (create new service, refactor adapter)
**Time**: 1-2 hours

---

### Calendar Alignment Plan

**Status**: ❌ No service, direct env access

**Changes Required**:

1. **Create CalendarConfigService** (NEW FILE: `services/integrations/calendar/config_service.py`):
```python
"""
Calendar Configuration Service
Implements ADR-010 Configuration Access Patterns for Calendar integration components.
"""

import os
from dataclasses import dataclass, field
from typing import List, Optional

from services.infrastructure.config.feature_flags import FeatureFlags


@dataclass
class CalendarConfig:
    """Calendar configuration settings"""

    # OAuth Configuration
    client_secrets_file: str = "credentials.json"
    token_file: str = "token.json"
    scopes: List[str] = field(default_factory=lambda: [
        "https://www.googleapis.com/auth/calendar.readonly"
    ])

    # API Configuration
    calendar_id: str = "primary"
    timeout_seconds: int = 30
    max_retries: int = 3

    # Circuit Breaker
    circuit_timeout: int = 300  # 5 minutes
    error_threshold: int = 5

    def validate(self) -> bool:
        """Validate configuration settings"""
        # Check if files exist
        import os.path
        if not os.path.exists(self.client_secrets_file):
            return False
        if not os.path.exists(self.token_file):
            # Token file created during OAuth flow, so this is optional
            pass
        return True


class CalendarConfigService:
    """Calendar configuration service following ADR-010 patterns"""

    def __init__(self, feature_flags: Optional[FeatureFlags] = None):
        self.feature_flags = feature_flags or FeatureFlags()
        self._config: Optional[CalendarConfig] = None

    def get_config(self) -> CalendarConfig:
        """Get Calendar configuration with environment variable loading"""
        if self._config is None:
            self._config = self._load_config()
        return self._config

    def _load_config(self) -> CalendarConfig:
        """Load configuration from environment variables"""
        return CalendarConfig(
            client_secrets_file=os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json"),
            token_file=os.getenv("GOOGLE_TOKEN_FILE", "token.json"),
            scopes=[
                s.strip() for s in os.getenv(
                    "GOOGLE_CALENDAR_SCOPES",
                    "https://www.googleapis.com/auth/calendar.readonly"
                ).split(",")
            ],
            calendar_id=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
            timeout_seconds=int(os.getenv("GOOGLE_CALENDAR_TIMEOUT", "30")),
            max_retries=int(os.getenv("GOOGLE_CALENDAR_MAX_RETRIES", "3")),
            circuit_timeout=int(os.getenv("GOOGLE_CALENDAR_CIRCUIT_TIMEOUT", "300")),
            error_threshold=int(os.getenv("GOOGLE_CALENDAR_ERROR_THRESHOLD", "5")),
        )

    def is_configured(self) -> bool:
        """Check if Calendar is properly configured"""
        config = self.get_config()
        return config.validate()
```

2. **Update Router** (`calendar_integration_router.py`):
```python
# BEFORE
def __init__(self):
    self.use_spatial = FeatureFlags.should_use_spatial_calendar()
    if self.use_spatial:
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
        self.spatial_calendar = GoogleCalendarMCPAdapter()

# AFTER
from .config_service import CalendarConfigService

def __init__(self, config_service: Optional[CalendarConfigService] = None):
    self.config_service = config_service or CalendarConfigService()
    self.use_spatial = FeatureFlags.should_use_spatial_calendar()
    if self.use_spatial:
        from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter
        self.spatial_calendar = GoogleCalendarMCPAdapter(self.config_service)
```

3. **Update Adapter** (`services/mcp/consumer/google_calendar_adapter.py`):
```python
# BEFORE
def __init__(self):
    super().__init__("google_calendar_mcp")
    # Direct env access (anti-pattern)
    self._client_secrets_file = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json")
    self._token_file = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
    self._scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

# AFTER
from services.integrations.calendar.config_service import CalendarConfigService

def __init__(self, config_service: CalendarConfigService):
    super().__init__("google_calendar_mcp")
    self.config_service = config_service

    # Get config through service (proper abstraction)
    config = self.config_service.get_config()
    self._client_secrets_file = config.client_secrets_file
    self._token_file = config.token_file
    self._scopes = config.scopes
    self._calendar_id = config.calendar_id
```

**Effort**: MEDIUM (create new service, refactor adapter)
**Time**: 1-2 hours

---

## Overall Alignment Summary

### Implementation Order

**Phase 1: Quick Wins** (30 minutes)
1. ✅ GitHub: Wire up existing service to router

**Phase 2: Service Creation** (2-3 hours)
1. ✅ Notion: Create NotionConfigService
2. ✅ Calendar: Create CalendarConfigService

**Phase 3: Adapter Refactoring** (1-2 hours)
1. ✅ Notion: Update NotionMCPAdapter to use service
2. ✅ Calendar: Update GoogleCalendarMCPAdapter to use service

**Phase 4: Cleanup** (30 minutes)
1. ✅ Remove deprecated config/notion_config.py
2. ✅ Update factory functions
3. ✅ Update tests

**Total Estimated Time**: 4-6 hours

### Benefits of Alignment

**Consistency**:
- All 4 integrations follow same pattern
- Easier to understand and maintain
- Plugin architecture ready

**Testability**:
- Can inject test configurations
- Can mock config services
- Integration tests easier

**Flexibility**:
- Can swap configurations at runtime
- Environment-specific configs easier
- Plugin registry can manage lifecycle

**DDD Compliance**:
- Proper layer separation
- No infrastructure leaks
- ADR-010 compliant across all integrations

---

## Phase 1B Complete

**Time**: 2:14 PM - 2:34 PM (~20 minutes)

**Mission Accomplished**: ✅ **Config pattern audit complete with specific alignment recommendations**

**Key Findings**:
- Only 1 of 4 integrations (25%) follow service injection pattern
- 3 integrations need alignment (GitHub, Notion, Calendar)
- GitHub is quickest fix (service exists, just wire it up)
- Notion and Calendar need new config services created

**Next Steps**: Implement alignment plan (estimated 4-6 hours total)

**Success Criteria Met**:
- ✅ GitHub config pattern verified (partial service injection)
- ✅ Calendar config pattern verified (direct env access)
- ✅ Comparison table created (all 4 integrations analyzed)
- ✅ Specific alignment recommendations provided (detailed implementation plans)
- ✅ Clear list of what needs fixing (3 integrations, prioritized)

---

**Report Complete**

**Session Log**: `dev/2025/10/02/2025-10-02-1222-prog-code-log.md`

**Generated**: October 2, 2025 at 2:34 PM PT by Claude Code (Sonnet 4.5)
