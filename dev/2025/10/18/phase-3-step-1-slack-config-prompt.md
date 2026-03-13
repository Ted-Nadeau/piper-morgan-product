# Phase 3 Step 1: Add PIPER.user.md Configuration Loading to Slack

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase 3 Step 1
**Date**: October 18, 2025, 8:30 AM

---

## Mission

Add PIPER.user.md configuration loading to SlackConfigService, following the proven Calendar/Notion pattern while respecting Slack's direct spatial architecture (ADR-039).

## Critical Context

**ADR-039 Architectural Guidance**:
- Slack uses **direct spatial pattern** (NOT tool-based MCP)
- This is intentional design decision
- **DO NOT convert Slack to MCP adapter pattern**
- Focus: Configuration completion only

**Investigation Complete**: Slack is 95% complete!
- ✅ SlackSpatialAdapter + SlackClient (direct spatial)
- ✅ 22 operations implemented
- ✅ 194 comprehensive tests
- ❌ Missing: PIPER.user.md config loading

**This is the SAME task completed for Calendar and Notion!**

---

## Methodology Reminder: Use Serena MCP Efficiently! 🎯

**Before reading full files**, use Serena for token-efficient queries:

### Serena Best Practices

**1. Symbol Overview** (most efficient):
```python
# Get high-level structure without reading entire file
mcp__serena__get_symbols_overview("services/integrations/slack/config_service.py")
```

**2. Find Specific Symbols**:
```python
# Find class/method definitions
mcp__serena__find_symbol("SlackConfigService", scope="services", depth=1)
```

**3. Read Files** (when you need actual implementation):
```python
# Only after Serena queries to understand structure
mcp__serena__read_file("services/integrations/slack/config_service.py")
```

**Token Efficiency**:
- Serena symbolic queries: ~100-500 tokens
- Full file reads: ~2000-5000 tokens
- Always use Serena first!

---

## Step 1: Add Configuration Loading Method

### File to Modify
`services/integrations/slack/config_service.py`

### Reference Implementation
**Copy pattern from**:
- `services/integrations/calendar/config_service.py` (Calendar)
- `services/integrations/notion/config_service.py` (Notion)

### Method to Add

```python
def _load_from_user_config(self) -> Dict[str, Any]:
    """Load Slack configuration from PIPER.user.md

    Reads the slack: section from config/PIPER.user.md and parses
    authentication, workspace, and behavior settings.

    Returns:
        Dict with Slack configuration from user config file
    """
    try:
        # Read PIPER.user.md
        config_path = Path("config/PIPER.user.md")
        if not config_path.exists():
            logger.debug("PIPER.user.md not found")
            return {}

        content = config_path.read_text()

        # Extract YAML between ```yaml and ``` after slack:
        slack_match = re.search(
            r'slack:\s*```yaml\s*(.*?)\s*```',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if not slack_match:
            logger.debug("No slack: section found in PIPER.user.md")
            return {}

        yaml_content = slack_match.group(1)
        config = yaml.safe_load(yaml_content)

        logger.info(f"Loaded Slack config from PIPER.user.md: {list(config.keys())}")
        return config

    except Exception as e:
        logger.error(f"Error loading Slack config from PIPER.user.md: {e}")
        return {}
```

### Integration into _load_config Method

**Update `_load_config()` to use 3-layer priority**:

```python
def _load_config(self) -> SlackConfig:
    """Load configuration with priority: env vars > user config > defaults"""

    # Load from PIPER.user.md first
    user_config = self._load_from_user_config()

    # Get authentication section (with fallback to env vars and defaults)
    auth_config = user_config.get("authentication", {})
    workspace_config = user_config.get("workspace", {})
    behavior_config = user_config.get("behavior", {})

    return SlackConfig(
        # Authentication (3-layer priority for each field)
        bot_token=os.getenv("SLACK_BOT_TOKEN", auth_config.get("bot_token", "")),
        app_token=os.getenv("SLACK_APP_TOKEN", auth_config.get("app_token")),

        # Workspace
        workspace_id=os.getenv("SLACK_WORKSPACE_ID", workspace_config.get("workspace_id")),
        team_id=os.getenv("SLACK_TEAM_ID", workspace_config.get("team_id")),

        # Behavior (following same pattern)
        default_channel=os.getenv("SLACK_DEFAULT_CHANNEL", behavior_config.get("default_channel")),
        # ... other fields with same 3-layer pattern
    )
```

### Required Imports

**Add these imports if not present**:

```python
import re
import yaml
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)
```

---

## Step 2: Update PIPER.user.md

### File to Modify
`config/PIPER.user.md`

### Section to Add

**Add or update the `slack:` section**:

```yaml
slack:
```yaml
  # Authentication (REQUIRED for Slack API access)
  authentication:
    bot_token: ""      # Your Slack bot token (xoxb-...)
    app_token: ""      # Your Slack app token (xapp-...) - optional for Socket Mode

  # Workspace Configuration
  workspace:
    workspace_id: ""   # Slack workspace ID (optional)
    team_id: ""        # Slack team ID (optional)

  # Behavior Settings
  behavior:
    default_channel: "general"     # Default channel for posting
    rate_limit_per_minute: 60      # API rate limit (Slack allows 60/min)
    retry_attempts: 3              # Number of retry attempts
    timeout_seconds: 30            # Request timeout

  # Features (optional toggles)
  features:
    enable_socket_mode: false      # Enable Socket Mode for events
    enable_markdown: true          # Parse markdown in messages
    thread_replies: true           # Enable threading
```
```

**Key Points**:
- Add `authentication:`, `workspace:`, `behavior:`, and `features:` subsections
- Include placeholder comments
- Maintain YAML formatting consistency with Calendar/Notion

---

## Step 3: Verify Configuration Priority

**Test the 3-layer priority system**:

### Priority Order (same as Calendar/Notion):
1. **Environment variables** (highest priority)
   - `SLACK_BOT_TOKEN`
   - `SLACK_APP_TOKEN`
   - `SLACK_WORKSPACE_ID`
   - `SLACK_DEFAULT_CHANNEL`
   - etc.

2. **PIPER.user.md** (middle priority)
   - `slack.authentication.bot_token`
   - `slack.workspace.workspace_id`
   - etc.

3. **Defaults** (lowest priority)
   - Empty strings for tokens
   - Sensible defaults for behavior settings

### Verification Commands

```python
# Test that config service initializes
from services.integrations.slack.config_service import SlackConfigService
config_service = SlackConfigService()
config = config_service._load_config()
print(f"Bot token loaded: {bool(config.bot_token)}")
print(f"Workspace ID: {config.workspace_id}")
print(f"Default channel: {config.default_channel}")
```

---

## Serena Usage Strategy for This Task

### Phase 1: Understand Current Structure (Use Serena!)

```python
# 1. Get overview of SlackConfigService
mcp__serena__get_symbols_overview("services/integrations/slack/config_service.py")

# 2. Find existing _load_config method
mcp__serena__find_symbol("_load_config", scope="services/integrations/slack", depth=1)

# 3. Check what imports exist
mcp__serena__get_symbols_overview("services/integrations/slack/config_service.py")
# Look at imports section
```

### Phase 2: Reference Calendar/Notion (Use Serena!)

```python
# Compare Calendar's implementation (don't read full file unless needed)
mcp__serena__find_symbol("_load_from_user_config", scope="services/integrations/calendar")
```

### Phase 3: Implement (Read full files only if needed)

Only after Serena queries, if you need full implementation details:
```python
mcp__serena__read_file("services/integrations/calendar/config_service.py", start=80, end=140)
```

**Remember**: Serena first, full reads only when necessary!

---

## Success Criteria

Your Step 1 is complete when:

- [ ] `_load_from_user_config()` method added to SlackConfigService
- [ ] Method parses YAML from PIPER.user.md correctly
- [ ] `_load_config()` uses 3-layer priority (env > user > defaults)
- [ ] Required imports added (re, yaml, Path)
- [ ] PIPER.user.md has proper `slack:` section with all subsections
- [ ] Configuration priority verified manually
- [ ] Code follows Calendar/Notion pattern exactly
- [ ] Logging added for debugging
- [ ] Error handling for missing files/malformed YAML
- [ ] **Used Serena efficiently** (symbolic queries before file reads)

---

## Reference Files

**Calendar Implementation** (your template):
- Use Serena first: `mcp__serena__find_symbol("_load_from_user_config", scope="services/integrations/calendar")`
- Then read if needed: `services/integrations/calendar/config_service.py` lines 80-129

**Notion Implementation** (also proven):
- Use Serena first: `mcp__serena__find_symbol("_load_from_user_config", scope="services/integrations/notion")`
- Then read if needed: `services/integrations/notion/config_service.py`

**Slack Files** (to modify):
- Use Serena: `mcp__serena__get_symbols_overview("services/integrations/slack/config_service.py")`
- Modify: `services/integrations/slack/config_service.py`
- Update: `config/PIPER.user.md`

---

## Pattern Checklist

- [ ] Same YAML parsing regex pattern (from Calendar/Notion)
- [ ] Same 3-layer priority logic
- [ ] Same error handling approach
- [ ] Same logging statements
- [ ] Same method signatures
- [ ] **Used Serena for token efficiency**

---

## Remember

- **Slack is direct spatial** (ADR-039) - don't convert to MCP
- **Copy Calendar/Notion pattern** for config loading only
- **Use Serena first** - symbolic queries are token-efficient
- **Test manually** - verify config loads correctly
- **Follow 3-layer priority** - env > user > defaults
- **Add logging** - helps with debugging
- **Handle errors gracefully** - return empty dict on failure

---

**This is the same proven task from Calendar and Notion - just applied to Slack's direct spatial architecture!**

**Use Serena MCP queries to understand structure before reading full files!**

**Ready to add PIPER.user.md configuration loading to Slack!** 🎯
