# Claude Code Agent Prompt: GREAT-3A Phase 1D - Calendar Config Service Creation

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 1D work.

## Mission
**Create Calendar Config Service**: Implement standard config service pattern for Calendar integration to achieve 100% compliance.

## Context

**Current Compliance**: 75% (3 of 4)
- ✅ Slack: Standard interface
- ✅ Notion: Standard interface
- ✅ GitHub: Standard interface + extensions
- ❌ Calendar: No config service (current task)

**Target**: 100% compliance - all 4 integrations using standard config interface

## Standard Interface Required

```python
class CalendarConfigService:
    def get_config(self) -> dict:
        """Returns complete configuration dictionary"""

    def is_configured(self) -> bool:
        """Returns True if all required config present"""

    def _load_config(self) -> dict:
        """Private method to load from environment/files"""
```

## Your Tasks

### Task 1: Analyze Current Calendar Config Pattern

```bash
cd ~/Development/piper-morgan

# Check what Calendar currently does
grep -A 30 "def __init__" services/integrations/calendar/calendar_integration_router.py

# Check adapter config pattern
grep -A 40 "def __init__" services/mcp/consumer/google_calendar_adapter.py | head -45

# Find direct environment access
grep "os.getenv\|os.environ" services/integrations/calendar/calendar_integration_router.py
grep "os.getenv\|os.environ" services/mcp/consumer/google_calendar_adapter.py
```

**Document**:
- Where does Calendar get config now? (direct env access in adapter)
- What config does Calendar need? (client_secrets_file, token_file, scopes)
- What pattern does it currently use?

### Task 2: Create CalendarConfigService

**File**: `services/integrations/calendar/config_service.py`

**Implementation Pattern** (follow Slack/Notion):

```python
"""
Calendar Configuration Service

Implements ADR-010 Configuration Access Patterns for Calendar integration.
Provides centralized configuration management for Google Calendar operations.
"""

import os
from dataclasses import dataclass
from typing import Optional, List

from services.infrastructure.config.feature_flags import FeatureFlags


@dataclass
class CalendarConfig:
    """Calendar configuration settings"""

    # OAuth 2.0 Configuration
    client_secrets_file: str = "credentials.json"
    token_file: str = "token.json"

    # API Configuration
    calendar_id: str = "primary"
    scopes: List[str] = None

    # Timeouts
    timeout_seconds: int = 30

    # Feature Flags
    enable_spatial_mapping: bool = True

    def __post_init__(self):
        if self.scopes is None:
            self.scopes = ["https://www.googleapis.com/auth/calendar.readonly"]

    def validate(self) -> bool:
        """Validate configuration settings"""
        # Check if credential files exist
        return os.path.exists(self.client_secrets_file)


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
            calendar_id=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
            timeout_seconds=int(os.getenv("CALENDAR_TIMEOUT_SECONDS", "30")),
            enable_spatial_mapping=self.feature_flags.is_enabled("calendar_spatial_mapping"),
        )

    def is_configured(self) -> bool:
        """Check if Calendar is properly configured"""
        config = self.get_config()
        return config.validate()
```

### Task 3: Update GoogleCalendarMCPAdapter

**File**: `services/mcp/consumer/google_calendar_adapter.py`

**Current Pattern** (direct env access):
```python
def __init__(self):
    self._client_secrets_file = os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json")
    self._token_file = os.getenv("GOOGLE_TOKEN_FILE", "token.json")
```

**New Pattern** (service injection):
```python
from typing import Optional
from services.integrations.calendar.config_service import CalendarConfigService

def __init__(self, config_service: Optional[CalendarConfigService] = None):
    super().__init__("google_calendar_mcp")

    # Store config service
    self.config_service = config_service or CalendarConfigService()

    # Load config from service
    config = self.config_service.get_config()
    self._client_secrets_file = config.client_secrets_file
    self._token_file = config.token_file
    self._calendar_id = config.calendar_id
    self._scopes = config.scopes

    # ... rest of initialization
```

**Changes**:
1. Add config_service parameter
2. Replace direct os.getenv() with config.attribute
3. Maintain backward compatibility (create default config if none provided)

### Task 4: Test Config Service

```bash
# Test 1: Import and instantiate
python -c "from services.integrations.calendar.config_service import CalendarConfigService; c = CalendarConfigService(); print('Config service created')"

# Test 2: get_config() works
python -c "from services.integrations.calendar.config_service import CalendarConfigService; c = CalendarConfigService(); config = c.get_config(); print('Config:', config); assert config.client_secrets_file"

# Test 3: is_configured() works
python -c "from services.integrations.calendar.config_service import CalendarConfigService; c = CalendarConfigService(); configured = c.is_configured(); print('Configured:', configured); assert isinstance(configured, bool)"

# Test 4: Adapter uses config service
python -c "from services.integrations.calendar.config_service import CalendarConfigService; from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter; c = CalendarConfigService(); a = GoogleCalendarMCPAdapter(c); print('Adapter initialized with config service')"
```

### Task 5: Remove Direct Environment Access

**Verify no direct env access remains**:
```bash
# Should return nothing from adapter after changes
grep "os.getenv\|os.environ" services/mcp/consumer/google_calendar_adapter.py

# If any remain, replace with config service usage
# OLD: os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json")
# NEW: config.client_secrets_file
```

### Task 6: Run Compliance Tests

```bash
# Run Cursor's test suite on Calendar
pytest tests/integration/config_pattern_compliance/ -k calendar -v

# Should now pass all 6 checks
# Generate updated report
python tests/integration/config_pattern_compliance/generate_report.py
```

## Deliverable

Create: `dev/2025/10/02/phase-1d-code-calendar-service.md`

Include:
1. **Current Pattern Analysis**: How Calendar gets config now
2. **Config Service Implementation**: Complete CalendarConfigService code
3. **Adapter Updates**: Changes to GoogleCalendarMCPAdapter with diffs
4. **Test Results**: All 4 test commands passing
5. **Compliance Tests**: Test suite results showing 6/6 checks pass
6. **Environment Access Removed**: Verification no direct env access remains

## Critical Requirements

- **DO follow** Slack/Notion pattern exactly
- **DO implement** standard interface (get_config, is_configured, _load_config)
- **DO update** adapter to use config service
- **DO maintain** backward compatibility
- **DO remove** all direct os.getenv() calls from adapter

## Time Estimate
1-1.5 hours

## Success Criteria
- [ ] CalendarConfigService created with standard interface
- [ ] Adapter accepts config_service parameter
- [ ] Adapter uses config service (not direct env access)
- [ ] All test commands pass
- [ ] Compliance tests pass (6/6 checks)
- [ ] 100% compliance achieved (4 of 4 integrations)

---

**Deploy at 4:37 PM**
**Final alignment task - achieves 100% pattern compliance**
