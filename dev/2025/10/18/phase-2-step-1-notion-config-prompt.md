# Phase 2 Step 1: Add PIPER.user.md Configuration Loading to Notion

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase 2 Step 1
**Duration**: 30 minutes estimated
**Date**: October 18, 2025, 7:35 AM

---

## Mission

Add PIPER.user.md configuration loading to NotionConfigService, following the exact pattern from Calendar's successful Phase 1 implementation.

## Context

**Investigation Complete**: Notion is already tool-based MCP (like Calendar)!
- ✅ NotionMCPAdapter exists (29KB, 22 methods)
- ✅ Router wired (NotionIntegrationRouter)
- ✅ Service injection working
- ❌ Missing: PIPER.user.md config loading

**This is the SAME task you completed for Calendar in Phase 1!**

**Calendar Success Pattern**:
- Added `_load_from_user_config()` to CalendarConfigService
- Implemented 3-layer priority (env > user config > defaults)
- Parsed YAML from PIPER.user.md
- Time: 30 minutes
- Result: 100% success

**Your Job**: Do the exact same thing for Notion!

---

## Step 1: Add Configuration Loading Method

### File to Modify
`services/integrations/notion/config_service.py`

### Reference Implementation
**Copy from**: `services/integrations/calendar/config_service.py` lines 80-129

### Method to Add

```python
def _load_from_user_config(self) -> Dict[str, Any]:
    """Load Notion configuration from PIPER.user.md

    Reads the notion: section from config/PIPER.user.md and parses
    authentication, publishing, and ADR settings.

    Returns:
        Dict with Notion configuration from user config file
    """
    try:
        # Read PIPER.user.md
        config_path = Path("config/PIPER.user.md")
        if not config_path.exists():
            logger.debug("PIPER.user.md not found")
            return {}

        content = config_path.read_text()

        # Extract YAML between ```yaml and ``` after notion:
        # Pattern: Look for "notion:" followed by ```yaml block
        notion_match = re.search(
            r'notion:\s*```yaml\s*(.*?)\s*```',
            content,
            re.DOTALL | re.IGNORECASE
        )

        if not notion_match:
            logger.debug("No notion: section found in PIPER.user.md")
            return {}

        yaml_content = notion_match.group(1)
        config = yaml.safe_load(yaml_content)

        logger.info(f"Loaded Notion config from PIPER.user.md: {list(config.keys())}")
        return config

    except Exception as e:
        logger.error(f"Error loading Notion config from PIPER.user.md: {e}")
        return {}
```

### Integration into _load_config Method

**Find the existing `_load_config()` method** and update it to use 3-layer priority:

```python
def _load_config(self) -> NotionConfig:
    """Load configuration with priority: env vars > user config > defaults"""

    # Load from PIPER.user.md first
    user_config = self._load_from_user_config()

    # Get authentication section (with fallback to env vars and defaults)
    auth_config = user_config.get("authentication", {})

    return NotionConfig(
        api_key=os.getenv("NOTION_API_KEY", auth_config.get("api_key", "")),
        workspace_id=os.getenv("NOTION_WORKSPACE_ID", auth_config.get("workspace_id")),
        # ... other config fields with same pattern
    )
```

### Required Imports

**Add these imports at the top of the file if not present**:

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

### Section to Add/Update

**Find the existing `notion:` section** (it may already have publishing/ADR config) and ensure it has this structure:

```yaml
notion:
```yaml
  authentication:
    api_key: "secret_..."  # Your Notion API key
    workspace_id: null     # Optional workspace ID

  publishing:
    # ... existing publishing config ...

  adrs:
    # ... existing ADR config ...
```
```

**If notion: section doesn't exist**, add it following the pattern of other integrations in PIPER.user.md.

**Key Points**:
- Add `authentication:` subsection if missing
- Keep existing `publishing:` and `adrs:` sections intact
- Add placeholder comment for API key
- Maintain YAML formatting consistency

---

## Step 3: Verify Configuration Priority

**Test the 3-layer priority system works**:

### Priority Order (same as Calendar):
1. **Environment variables** (highest priority)
   - `NOTION_API_KEY`
   - `NOTION_WORKSPACE_ID`

2. **PIPER.user.md** (middle priority)
   - `notion.authentication.api_key`
   - `notion.authentication.workspace_id`

3. **Defaults** (lowest priority)
   - Empty string for api_key
   - None for workspace_id

### Verification Commands

```python
# Test that config service initializes
from services.integrations.notion.config_service import NotionConfigService
config_service = NotionConfigService()
config = config_service._load_config()
print(f"API Key loaded: {bool(config.api_key)}")
print(f"Workspace ID: {config.workspace_id}")
```

---

## Step 4: Document the Changes

### Update Comments in Code

**Add docstring to `_load_from_user_config()`**:
- Explain YAML parsing pattern
- Note the notion: section structure
- Reference Calendar implementation

**Update `_load_config()` docstring**:
- Document 3-layer priority
- Show example of priority override
- Reference PIPER.user.md format

---

## Success Criteria

Your Step 1 is complete when:

- [ ] `_load_from_user_config()` method added to NotionConfigService
- [ ] Method parses YAML from PIPER.user.md correctly
- [ ] `_load_config()` uses 3-layer priority (env > user > defaults)
- [ ] Required imports added (re, yaml, Path)
- [ ] PIPER.user.md has proper `notion.authentication` section
- [ ] Configuration priority verified manually
- [ ] Code follows Calendar pattern exactly
- [ ] Logging added for debugging
- [ ] Error handling for missing files/malformed YAML

---

## Reference Files

**Calendar Implementation** (your template):
- `services/integrations/calendar/config_service.py` lines 80-129
- PIPER.user.md `google_calendar:` section format

**Notion Files** (to modify):
- `services/integrations/notion/config_service.py`
- `config/PIPER.user.md`

**Pattern Checklist**:
- [ ] Same YAML parsing regex pattern
- [ ] Same 3-layer priority logic
- [ ] Same error handling approach
- [ ] Same logging statements
- [ ] Same method signatures

---

## Time Budget

- **Total**: 30 minutes
- **Add method**: 10 min (copy and adapt from Calendar)
- **Update _load_config**: 10 min (3-layer priority)
- **Update PIPER.user.md**: 5 min (add authentication section)
- **Verify**: 5 min (manual test)

---

## Common Patterns to Reuse

### YAML Extraction Pattern (from Calendar)
```python
# Look for section_name: followed by ```yaml block
pattern = r'notion:\s*```yaml\s*(.*?)\s*```'
match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
```

### 3-Layer Priority Pattern (from Calendar)
```python
user_config = self._load_from_user_config()
auth_config = user_config.get("authentication", {})
api_key = os.getenv("NOTION_API_KEY", auth_config.get("api_key", ""))
```

### Error Handling Pattern (from Calendar)
```python
try:
    config_path = Path("config/PIPER.user.md")
    if not config_path.exists():
        logger.debug("PIPER.user.md not found")
        return {}
    # ... parsing logic
except Exception as e:
    logger.error(f"Error loading config: {e}")
    return {}
```

---

## Implementation Notes

### What to Copy Exactly
- YAML regex pattern
- Error handling structure
- Logging statements
- Method signature

### What to Adapt
- Section name: `notion:` instead of `google_calendar:`
- Config fields: `api_key`, `workspace_id` instead of calendar fields
- Logger name: `notion.config_service`
- Variable names: `notion_match` instead of `calendar_match`

### What to Keep from Existing Code
- NotionConfig dataclass
- Any existing configuration logic
- Validation logic (if present)

---

## Verification Steps

After implementation:

1. **Import test**:
   ```python
   from services.integrations.notion.config_service import NotionConfigService
   ```

2. **Initialization test**:
   ```python
   service = NotionConfigService()
   ```

3. **Config loading test**:
   ```python
   config = service._load_config()
   print(config.api_key)  # Should load from env or PIPER.user.md
   ```

4. **YAML parsing test**:
   ```python
   user_config = service._load_from_user_config()
   print(user_config.get("authentication", {}))  # Should show parsed config
   ```

---

## Expected Output

When complete, you should be able to:

```python
# Load Notion config from PIPER.user.md
from services.integrations.notion.config_service import NotionConfigService

service = NotionConfigService()
config = service._load_config()

# Config should have values from PIPER.user.md (if set)
# Or from environment variables (if set)
# Or defaults (empty/None)
print(f"Notion configured: {bool(config.api_key)}")
```

---

## Remember

- **Copy Calendar's pattern EXACTLY** - it worked perfectly
- **Don't overthink** - this is a proven implementation
- **Test manually** - verify config loads correctly
- **Follow 3-layer priority** - env > user > defaults
- **Add logging** - helps with debugging
- **Handle errors gracefully** - return empty dict on failure

---

**This is the same task you already completed successfully for Calendar!**

**Just adapt the Calendar implementation for Notion and you're done.** 🎯

**Ready to add PIPER.user.md configuration loading to Notion!**

**Estimated Time**: 30 minutes
**Difficulty**: LOW (copying proven pattern)
**Success Rate**: 100% (if following Calendar exactly)
