# Phase 1 Step 1.1: Complete Calendar MCP Implementation

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Calendar Completion (95%→100%)
**Duration**: 2-3 hours estimated
**Date**: October 17, 2025, 2:00 PM

---

## Mission

Complete the Calendar MCP implementation by adding PIPER.user.md configuration loading to CalendarConfigService. This will establish the pattern for GitHub and other integrations to follow.

## Context

**Your Investigation Found**:
- Calendar is 95% complete and architecturally excellent
- Missing: CalendarConfigService doesn't read from PIPER.user.md
- Current: Only reads from environment variables
- GitHub/Notion/Standup already have PIPER.user.md loading

**Why This Matters**:
- Configuration consistency across all services
- Calendar becomes canonical reference implementation
- Pattern established for GitHub, Slack, and future integrations

---

## Your Deliverables

### 1. Add Calendar Section to PIPER.user.md (5 minutes)

**Location**: `config/PIPER.user.md`

**Add this YAML block** (find appropriate location in file):

```yaml
calendar:
  # OAuth 2.0 Configuration
  client_secrets_file: "credentials.json"
  token_file: "token.json"

  # API Configuration
  calendar_id: "primary"
  scopes:
    - "https://www.googleapis.com/auth/calendar.readonly"

  # Timeouts & Circuit Breaker
  timeout_seconds: 30
  circuit_timeout: 300
  error_threshold: 5

  # Feature Flags
  enable_spatial_mapping: true
```

**Verification**:
```bash
# Verify YAML is valid
python -c "import yaml; yaml.safe_load(open('config/PIPER.user.md').read())"

# Confirm calendar section exists
grep -A 10 "^calendar:" config/PIPER.user.md
```

---

### 2. Implement YAML Parsing in CalendarConfigService (1-2 hours)

**File**: `services/integrations/calendar/config_service.py`

**Current Implementation** (Lines 77-102):
```python
def _load_config(self) -> CalendarConfig:
    """Load calendar configuration from environment variables."""
    return CalendarConfig(
        client_secrets_file=os.getenv("GOOGLE_CLIENT_SECRETS_FILE", "credentials.json"),
        token_file=os.getenv("GOOGLE_TOKEN_FILE", "token.json"),
        calendar_id=os.getenv("GOOGLE_CALENDAR_ID", "primary"),
        # ... all from environment variables
    )
```

**Required Changes**:

#### Step 2.1: Check for Existing YAML Utility

**First, search for existing YAML parsing utilities**:
```bash
# Find YAML parsing in GitHub/Notion config services
grep -r "yaml.safe_load\|_load_from_user_config" services/integrations/github/
grep -r "yaml.safe_load\|_load_from_user_config" services/integrations/notion/

# Find PIPER.user.md parsing utilities
find services -name "*config*" -type f -exec grep -l "PIPER.user.md" {} \;
```

**If utility exists**: Use it! Import and call it.
**If utility doesn't exist**: Implement the pattern below.

#### Step 2.2: Add YAML Import

```python
import yaml
from pathlib import Path
```

#### Step 2.3: Add _load_from_user_config() Method

```python
def _load_from_user_config(self) -> Dict[str, Any]:
    """Load calendar configuration from PIPER.user.md.

    Returns:
        Dict with calendar configuration, or empty dict if not found/invalid
    """
    try:
        user_config_path = Path("config/PIPER.user.md")
        if not user_config_path.exists():
            return {}

        # Read the markdown file
        content = user_config_path.read_text()

        # Extract YAML blocks (content between ```yaml and ```)
        yaml_blocks = []
        in_yaml_block = False
        current_block = []

        for line in content.split('\n'):
            if line.strip() == '```yaml':
                in_yaml_block = True
                current_block = []
            elif line.strip() == '```' and in_yaml_block:
                yaml_blocks.append('\n'.join(current_block))
                in_yaml_block = False
            elif in_yaml_block:
                current_block.append(line)

        # Parse YAML blocks and find calendar section
        for block in yaml_blocks:
            try:
                data = yaml.safe_load(block)
                if data and 'calendar' in data:
                    return data['calendar']
            except yaml.YAMLError:
                continue

        return {}
    except Exception as e:
        # Log error but don't crash - graceful fallback
        print(f"Warning: Could not load calendar config from PIPER.user.md: {e}")
        return {}
```

#### Step 2.4: Update _load_config() Method

**Replace current implementation with**:

```python
def _load_config(self) -> CalendarConfig:
    """Load calendar configuration with priority: env vars > PIPER.user.md > defaults.

    Configuration Priority Order:
    1. Environment variables (highest priority - overrides everything)
    2. PIPER.user.md calendar section (middle priority)
    3. Hardcoded defaults (lowest priority - fallback)

    Returns:
        CalendarConfig with loaded configuration
    """
    # Load from PIPER.user.md first (base layer)
    user_config = self._load_from_user_config()

    # Environment variables override user config
    # (os.getenv returns env var if set, otherwise uses second argument as default)
    return CalendarConfig(
        client_secrets_file=os.getenv(
            "GOOGLE_CLIENT_SECRETS_FILE",
            user_config.get("client_secrets_file", "credentials.json")
        ),
        token_file=os.getenv(
            "GOOGLE_TOKEN_FILE",
            user_config.get("token_file", "token.json")
        ),
        calendar_id=os.getenv(
            "GOOGLE_CALENDAR_ID",
            user_config.get("calendar_id", "primary")
        ),
        scopes=os.getenv(
            "GOOGLE_CALENDAR_SCOPES",
            ",".join(user_config.get("scopes", [
                "https://www.googleapis.com/auth/calendar.readonly"
            ]))
        ).split(","),
        timeout_seconds=int(os.getenv(
            "GOOGLE_CALENDAR_TIMEOUT",
            str(user_config.get("timeout_seconds", 30))
        )),
        circuit_timeout=int(os.getenv(
            "GOOGLE_CALENDAR_CIRCUIT_TIMEOUT",
            str(user_config.get("circuit_timeout", 300))
        )),
        error_threshold=int(os.getenv(
            "GOOGLE_CALENDAR_ERROR_THRESHOLD",
            str(user_config.get("error_threshold", 5))
        )),
    )
```

**Verification**:
```bash
# Syntax check
python -m py_compile services/integrations/calendar/config_service.py

# Import check
python -c "from services.integrations.calendar.config_service import CalendarConfigService"
```

---

### 3. Add Test for PIPER.user.md Loading (30 minutes)

**Location**: Create new test file `tests/integration/test_calendar_config_loading.py`

**Test Implementation**:

```python
"""Tests for Calendar configuration loading from PIPER.user.md."""

import os
import pytest
import tempfile
import yaml
from pathlib import Path
from unittest.mock import patch

from services.integrations.calendar.config_service import CalendarConfigService


class TestCalendarConfigLoading:
    """Test CalendarConfigService configuration loading from PIPER.user.md."""

    def test_loads_from_piper_user_md(self, tmp_path):
        """Test that config loads from PIPER.user.md when present."""
        # Create temporary PIPER.user.md
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("""
# Test Configuration

```yaml
calendar:
  client_secrets_file: "test_credentials.json"
  token_file: "test_token.json"
  calendar_id: "test@calendar.com"
  timeout_seconds: 60
```
        """)

        # Patch config path to use temp file
        with patch('services.integrations.calendar.config_service.Path') as mock_path:
            mock_path.return_value = piper_config

            # Load config
            service = CalendarConfigService()
            config = service.get_config()

            # Verify values from PIPER.user.md
            assert config.client_secrets_file == "test_credentials.json"
            assert config.token_file == "test_token.json"
            assert config.calendar_id == "test@calendar.com"
            assert config.timeout_seconds == 60

    def test_env_vars_override_user_config(self, tmp_path):
        """Test that environment variables override PIPER.user.md."""
        # Create PIPER.user.md with one value
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("""
```yaml
calendar:
  calendar_id: "user_config@calendar.com"
  timeout_seconds: 30
```
        """)

        # Set environment variable to override
        os.environ["GOOGLE_CALENDAR_ID"] = "env_override@calendar.com"

        try:
            with patch('services.integrations.calendar.config_service.Path') as mock_path:
                mock_path.return_value = piper_config

                service = CalendarConfigService()
                config = service.get_config()

                # Verify env var overrides user config
                assert config.calendar_id == "env_override@calendar.com"
                # Verify non-overridden value still from user config
                assert config.timeout_seconds == 30
        finally:
            # Clean up environment
            del os.environ["GOOGLE_CALENDAR_ID"]

    def test_defaults_when_no_config(self, tmp_path):
        """Test that defaults are used when neither PIPER.user.md nor env vars present."""
        # Create empty PIPER.user.md
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("# Empty config")

        with patch('services.integrations.calendar.config_service.Path') as mock_path:
            mock_path.return_value = piper_config

            service = CalendarConfigService()
            config = service.get_config()

            # Verify defaults
            assert config.client_secrets_file == "credentials.json"
            assert config.token_file == "token.json"
            assert config.calendar_id == "primary"
            assert config.timeout_seconds == 30

    def test_graceful_fallback_when_piper_missing(self, tmp_path):
        """Test graceful fallback when PIPER.user.md doesn't exist."""
        # Point to non-existent file
        missing_path = tmp_path / "nonexistent.md"

        with patch('services.integrations.calendar.config_service.Path') as mock_path:
            mock_path.return_value = missing_path

            # Should not raise exception
            service = CalendarConfigService()
            config = service.get_config()

            # Should use defaults
            assert config.calendar_id == "primary"

    def test_graceful_fallback_when_yaml_malformed(self, tmp_path):
        """Test graceful fallback when PIPER.user.md has malformed YAML."""
        piper_config = tmp_path / "PIPER.user.md"
        piper_config.write_text("""
```yaml
calendar:
  bad: yaml: syntax: here:
  - invalid
```
        """)

        with patch('services.integrations.calendar.config_service.Path') as mock_path:
            mock_path.return_value = piper_config

            # Should not raise exception
            service = CalendarConfigService()
            config = service.get_config()

            # Should use defaults
            assert config.calendar_id == "primary"
```

**Run Tests**:
```bash
# Run new tests
pytest tests/integration/test_calendar_config_loading.py -v

# Run all calendar tests to ensure no regression
pytest tests/integration/test_calendar_integration.py -v

# Check test coverage
pytest tests/integration/test_calendar_config_loading.py --cov=services.integrations.calendar.config_service
```

---

### 4. Documentation Update (30 minutes)

#### Update 1: Add Configuration Example to PIPER.user.md

**Add comment/documentation section** explaining Calendar configuration:

```markdown
## Calendar Integration

Configure Google Calendar integration with OAuth 2.0 credentials:

```yaml
calendar:
  # OAuth 2.0 files (obtain from Google Cloud Console)
  client_secrets_file: "credentials.json"
  token_file: "token.json"

  # Calendar to monitor
  calendar_id: "primary"  # or specific calendar ID

  # API scopes
  scopes:
    - "https://www.googleapis.com/auth/calendar.readonly"

  # Timeouts and error handling
  timeout_seconds: 30
  circuit_timeout: 300  # seconds before circuit breaker resets
  error_threshold: 5    # errors before circuit opens
```

Configuration Priority:
1. Environment variables (highest - overrides everything)
2. PIPER.user.md (middle - overrides defaults)
3. Hardcoded defaults (lowest - fallback)
```

#### Update 2: Document Pattern in ADR-037

**Add section to ADR-037** documenting configuration pattern:

```markdown
## Configuration Pattern

Tool-based MCP implementations follow this configuration loading pattern:

1. **Load from PIPER.user.md** (base layer)
   - Parse YAML blocks from markdown
   - Extract service-specific section
   - Graceful fallback if file missing or invalid

2. **Environment variables override** (priority layer)
   - `os.getenv(ENV_VAR, user_config_value or default)`
   - Env vars always win when set

3. **Hardcoded defaults** (fallback layer)
   - Sensible defaults for all configuration
   - System works out-of-box with no config

Example: CalendarConfigService (services/integrations/calendar/config_service.py)
```

#### Update 3: Create Configuration Guide

**Create** `docs/integrations/calendar-configuration.md`:

```markdown
# Calendar Integration Configuration

## Overview

Calendar integration supports three configuration methods with priority order:

1. **Environment Variables** (highest priority)
2. **PIPER.user.md** (middle priority)
3. **Hardcoded Defaults** (lowest priority)

## Quick Start

### Method 1: PIPER.user.md (Recommended)

Add to `config/PIPER.user.md`:

```yaml
calendar:
  client_secrets_file: "credentials.json"
  token_file: "token.json"
  calendar_id: "primary"
```

### Method 2: Environment Variables

```bash
export GOOGLE_CLIENT_SECRETS_FILE="credentials.json"
export GOOGLE_TOKEN_FILE="token.json"
export GOOGLE_CALENDAR_ID="primary"
```

### Method 3: Defaults Only

System works with defaults if no configuration provided.

## OAuth 2.0 Setup

1. Create project in Google Cloud Console
2. Enable Google Calendar API
3. Create OAuth 2.0 credentials
4. Download as `credentials.json`
5. Run authentication flow (generates `token.json`)

## Configuration Reference

[Full configuration options with explanations]
```

---

## Success Criteria

Calendar completion is **100%** when:

- [ ] PIPER.user.md has calendar section with example config
- [ ] CalendarConfigService has `_load_from_user_config()` method
- [ ] CalendarConfigService `_load_config()` uses priority order (env > user > defaults)
- [ ] All 5 test cases pass for configuration loading
- [ ] All existing calendar tests still pass (no regression)
- [ ] Documentation updated with configuration instructions
- [ ] Configuration pattern documented in ADR-037
- [ ] Can verify config loading manually:
  ```bash
  # With PIPER.user.md only (no env vars)
  python -c "from services.integrations.calendar.config_service import CalendarConfigService; c = CalendarConfigService(); print(c.get_config())"

  # With env var override
  GOOGLE_CALENDAR_ID="test@calendar.com" python -c "..."
  ```

---

## Evidence Required

For completion, provide:

1. **PIPER.user.md** - Show calendar section added
2. **config_service.py** - Show `_load_from_user_config()` and updated `_load_config()`
3. **Test results** - All tests passing
4. **Documentation** - Configuration guide created
5. **Manual verification** - Config loads from PIPER.user.md and env vars override

---

## Time Budget

- **Total**: 2-3 hours
- **PIPER.user.md**: 5 min ✅
- **YAML parsing**: 1-2 hours (depends on utility reuse)
- **Tests**: 30 min
- **Documentation**: 30 min

---

## Remember

- Graceful fallback for missing/malformed config
- Environment variables always override user config
- Existing tests must still pass (no regression)
- Calendar becomes reference implementation for GitHub
- Document pattern clearly for future integrations

---

**Ready to complete Calendar MCP to 100%!** 🎯
