# Phase 2 Step 3: Update Documentation for Notion Configuration

**Agent**: Claude Code (Programmer)
**Task**: CORE-MCP-MIGRATION #198 - Phase 2 Step 3
**Date**: October 18, 2025, 8:05 AM

---

## Mission

Update ADR-010 and related documentation to include Notion's PIPER.user.md configuration pattern, establishing it as part of our canonical configuration approach.

## Context

**Steps 1-2 Complete**:
- ✅ Configuration loading implemented (3-layer priority)
- ✅ Test suite created (19 comprehensive tests)
- ✅ Pattern matches Calendar exactly

**Your Job**: Document this configuration pattern so others can follow it

**Why This Matters**:
- ADRs are our architectural decisions of record
- Future integrations will reference this pattern
- Documents the evolution: Calendar → GitHub → Notion
- Establishes consistency across all MCP integrations

---

## Documentation Updates Required

### 1. Update ADR-010: Configuration Patterns

**File**: `docs/internal/architecture/current/adrs/adr-010-configuration-patterns.md`

**Find the section on Configuration Service Pattern** and add Notion to the examples.

**Locate**:
Look for sections mentioning Calendar or GitHub configuration examples.

**Add Notion Example**:
After the existing Calendar/GitHub examples, add:

```markdown
#### Notion Configuration Service

**Location**: `services/integrations/notion/config_service.py`

**Pattern**: Service injection with PIPER.user.md YAML parsing

**Configuration Priority**:
1. Environment variables (highest priority)
   - `NOTION_API_KEY`
   - `NOTION_WORKSPACE_ID`
   - `NOTION_TIMEOUT_SECONDS`
   - `NOTION_MAX_RETRIES`
   - `NOTION_REQUESTS_PER_MINUTE`

2. PIPER.user.md configuration (middle priority)
   ```yaml
   notion:
     authentication:
       api_key: "secret_..."
       workspace_id: "workspace_id"
     api_base_url: "https://api.notion.com/v1"
     timeout_seconds: 30
     max_retries: 3
     requests_per_minute: 30
   ```

3. Hardcoded defaults (lowest priority)
   - Empty api_key
   - Default API base URL
   - 30s timeout
   - 3 retries
   - 30 requests/minute

**Implementation**:
```python
class NotionConfigService:
    def _load_from_user_config(self) -> Dict[str, Any]:
        """Load Notion configuration from PIPER.user.md"""
        # Parse YAML from markdown
        # Return notion: section configuration

    def _load_config(self) -> NotionConfig:
        """Load with 3-layer priority"""
        user_config = self._load_from_user_config()
        auth = user_config.get("authentication", {})
        return NotionConfig(
            api_key=os.getenv("NOTION_API_KEY", auth.get("api_key", "")),
            # ... other fields with same pattern
        )
```

**Test Coverage**: 19 comprehensive tests in `tests/integration/test_notion_config_loading.py`

**Status**: ✅ Implemented (October 2025, Phase 2)
```

---

### 2. Update Configuration Pattern Summary

**In ADR-010**, find or create a **Summary of Integrations** section:

```markdown
## Configuration Pattern Summary

| Integration | Config Service | PIPER.user.md | Env Vars | Tests | Status |
|-------------|----------------|---------------|----------|-------|--------|
| Calendar    | ✅ Yes         | ✅ Yes        | ✅ Yes   | 8     | 100%   |
| GitHub      | ✅ Yes         | ✅ Yes        | ✅ Yes   | 16    | 100%   |
| Notion      | ✅ Yes         | ✅ Yes        | ✅ Yes   | 19    | 100%   |
| Slack       | 🔄 Pending     | 🔄 Pending    | ✅ Yes   | TBD   | Phase 3|

**Pattern Consistency**: All MCP integrations follow the same configuration approach:
- Service injection with dedicated ConfigService
- PIPER.user.md YAML parsing for user configuration
- Environment variable overrides for sensitive data
- Three-layer priority (env > user > defaults)
- Comprehensive test coverage for all scenarios
```

---

### 3. Add Implementation Timeline

**In ADR-010**, add or update the **Implementation History** section:

```markdown
## Implementation History

### Phase 1: Calendar (October 17, 2025)
- Added PIPER.user.md configuration loading
- Established 3-layer priority pattern
- Created 8 comprehensive tests
- **Status**: ✅ Complete

### Phase 1: GitHub (October 17, 2025)
- Verified existing PIPER.user.md support
- Wired MCP adapter following Delegated MCP Pattern (ADR-038)
- Added 16 comprehensive tests
- **Status**: ✅ Complete

### Phase 2: Notion (October 18, 2025)
- Added PIPER.user.md configuration loading
- Followed Calendar pattern exactly
- Created 19 comprehensive tests (most thorough coverage)
- **Status**: ✅ Complete

### Phase 3: Slack (Planned)
- Will follow same configuration pattern
- Estimated completion: [TBD]
- **Status**: 🔄 Pending
```

---

### 4. Update PIPER.user.md Documentation

**File**: `config/PIPER.user.md`

**Find the Configuration Documentation Section** (likely near the top or in a configuration guide section).

**Add or Update**:

```markdown
## Configuration Priority

All integrations follow a consistent 3-layer priority system:

1. **Environment Variables** (Highest Priority)
   - Override all other configuration
   - Used for sensitive data (API keys, tokens)
   - Example: `NOTION_API_KEY="secret_..."`

2. **PIPER.user.md** (Middle Priority)
   - Personal configuration in this file
   - Overrides hardcoded defaults
   - Version-controlled with your preferences

3. **Hardcoded Defaults** (Lowest Priority)
   - Built into the application
   - Used when nothing else is specified
   - Sensible fallback values

### Example: Notion Configuration

```yaml
notion:
  # Authentication credentials
  authentication:
    api_key: ""  # Or set NOTION_API_KEY environment variable
    workspace_id: ""  # Optional

  # API settings (optional - uses defaults if not specified)
  api_base_url: "https://api.notion.com/v1"
  timeout_seconds: 30
  max_retries: 3
  requests_per_minute: 30
```

**How it works**:
- Set `NOTION_API_KEY` environment variable → API key comes from environment
- Configure `api_key` in this file → API key comes from PIPER.user.md
- Neither set → API key defaults to empty string

This pattern applies to all integrations (Calendar, GitHub, Notion, Slack).
```

---

### 5. Update Integration README

**File**: `services/integrations/notion/README.md` (create if doesn't exist)

```markdown
# Notion Integration

Tool-based MCP integration for Notion API following the Calendar pattern.

## Architecture

**Pattern**: Tool-based MCP (ADR-037)
**Configuration**: PIPER.user.md with 3-layer priority (ADR-010)
**Status**: ✅ Complete (Phase 2, October 2025)

## Configuration

### Quick Start

1. **Set Environment Variable** (recommended for sensitive data):
   ```bash
   export NOTION_API_KEY="secret_your_integration_token"
   ```

2. **Or Configure in PIPER.user.md**:
   ```yaml
   notion:
     authentication:
       api_key: "secret_your_integration_token"
       workspace_id: "optional_workspace_id"
   ```

3. **Or Use Defaults** (no authentication):
   - Integration will initialize with empty credentials
   - Operations requiring authentication will fail gracefully

### Configuration Priority

```
Environment Variables > PIPER.user.md > Defaults
```

**Environment Variables** (highest priority):
- `NOTION_API_KEY` - Notion integration token
- `NOTION_WORKSPACE_ID` - Workspace ID (optional)
- `NOTION_TIMEOUT_SECONDS` - API timeout (default: 30)
- `NOTION_MAX_RETRIES` - Retry attempts (default: 3)
- `NOTION_REQUESTS_PER_MINUTE` - Rate limit (default: 30)

**PIPER.user.md** (middle priority):
See `config/PIPER.user.md` for full configuration example.

**Defaults** (lowest priority):
Built-in fallback values for all settings.

## Usage

```python
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

# Initialize with automatic configuration loading
router = NotionIntegrationRouter()

# Use Notion operations
database = await router.get_database("database_id")
pages = await router.query_database("database_id", filter={...})
```

## Testing

Run Notion configuration tests:
```bash
pytest tests/integration/test_notion_config_loading.py -v
```

**Test Coverage**: 19 comprehensive tests covering:
- PIPER.user.md loading (5 tests)
- Priority system (3 tests)
- Authentication (2 tests)
- API configuration (4 tests)
- Service basics (3 tests)
- Edge cases (2 tests)

## Implementation Details

**Config Service**: `services/integrations/notion/config_service.py`
**MCP Adapter**: `services/integrations/mcp/notion_adapter.py`
**Router**: `services/integrations/notion/notion_integration_router.py`

**Pattern Consistency**: Follows Calendar and GitHub configuration patterns exactly.

## Related ADRs

- ADR-010: Configuration Patterns (PIPER.user.md loading)
- ADR-037: Tool-based MCP Standardization
- ADR-038: Spatial Intelligence Patterns

## Phase 2 Completion

- ✅ Configuration loading from PIPER.user.md
- ✅ 3-layer priority system
- ✅ 19 comprehensive tests
- ✅ Documentation complete
- **Status**: Ready for production use
```

---

## Success Criteria

Your Step 3 is complete when:

- [ ] ADR-010 updated with Notion configuration example
- [ ] Configuration pattern summary updated (includes Notion)
- [ ] Implementation timeline added/updated
- [ ] PIPER.user.md configuration guide updated
- [ ] Notion README created with comprehensive documentation
- [ ] All files reviewed for consistency
- [ ] Documentation follows same style as Calendar/GitHub

---

## Documentation Quality Standards

### Consistency
- Follow same format as Calendar/GitHub documentation
- Use same terminology across all docs
- Maintain same level of detail

### Completeness
- Explain all configuration options
- Document all priority layers
- Include examples for common scenarios
- Reference related ADRs

### Clarity
- Clear, concise explanations
- Code examples where helpful
- Step-by-step instructions
- Troubleshooting guidance

### Maintainability
- Date all implementation notes
- Reference issue numbers
- Link related documentation
- Update summaries/tables

---

## Files to Modify

1. **ADR-010**: `docs/internal/architecture/current/adrs/adr-010-configuration-patterns.md`
   - Add Notion configuration example
   - Update integration summary table
   - Add implementation timeline

2. **PIPER.user.md**: `config/PIPER.user.md`
   - Update configuration priority documentation
   - Add Notion example to guide section
   - Ensure consistency with Calendar/GitHub

3. **Notion README**: `services/integrations/notion/README.md`
   - Create comprehensive integration documentation
   - Include configuration guide
   - Document test coverage
   - Link to ADRs

---

## Verification Steps

After documentation updates:

1. **Review all changes**:
   - Read through each file
   - Check for consistency
   - Verify examples are accurate

2. **Cross-reference**:
   - Ensure ADR-010 matches implementation
   - Verify PIPER.user.md examples match code
   - Check README matches actual behavior

3. **Test examples**:
   - Verify configuration examples work
   - Check environment variable examples
   - Test priority system as documented

4. **Pattern consistency check**:
   - Compare Notion docs to Calendar docs
   - Ensure same style and format
   - Verify all integrations documented similarly

---

## Remember

- **Document what we built** - configuration loading with 3-layer priority
- **Follow established patterns** - match Calendar/GitHub documentation style
- **Be thorough but concise** - explain clearly without excess verbosity
- **Think about future readers** - make it easy for others to follow this pattern
- **Update all relevant files** - ADRs, PIPER.user.md, README

---

**Focus on creating documentation that makes the pattern clear and repeatable.**

**Future integrations should be able to follow Notion's example exactly.**

**Ready to document the Notion configuration pattern!** 📝
