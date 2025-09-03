# Phase 2: Configuration Schema Design Framework

**GitHub Issue**: PM-131 (#138) - Design user configuration schema for Notion integration
**Mission**: Design YAML configuration structure based on audit findings and decision framework
**Duration**: 20 minutes schema design with ADR-027 documentation
**Context**: 5 decisions resolved, audit data provides concrete requirements

---

## DESIGN FOUNDATION

### Audit-Based Requirements

**Critical Configuration Needs**:
- ADR Database ID: `25e11704d8bf80deaac2f806390fe7da` (HIGH priority)
- Test Parent IDs: 3 different values for testing environments
- Default publishing locations for user content
- Development script workspace references

**Configuration Categories**:
- Database IDs (2 instances, same database)
- Parent IDs (3 instances, different pages)
- Workspace IDs (0 instances - environment-based)

### Decision Framework Applied

**Decision 1**: Extend PIPER.user.md with `notion:` section
**Decision 2**: Required (ADR database, default parent) vs Optional (workspace, testing)
**Decision 3**: Fail fast with actionable error messages
**Decision 4**: Manual migration with clear documentation
**Decision 5**: Tiered validation (MVP: format + connectivity)

---

## PROPOSED CONFIGURATION SCHEMA

### PIPER.user.md notion: Section Structure

```yaml
notion:
  # Core Publishing Configuration (REQUIRED)
  publishing:
    default_parent: "25d11704d8bf80c8a71ddbe7aba51f55"  # Default location for content
    enabled: true

  # ADR Database Configuration (REQUIRED)
  adrs:
    database_id: "25e11704d8bf80deaac2f806390fe7da"      # ADR publishing database
    enabled: true
    auto_publish: true                                    # Publish ADRs on creation

  # Optional Workspace Configuration
  workspace:
    id: null                                              # Optional - API can discover
    name: "Development Workspace"                         # Human-readable reference

  # Development & Testing Configuration (OPTIONAL)
  development:
    test_parent: "25d11704d8bf8135a3c9c732704c88a4"      # Test page creation location
    debug_parent: "25d11704d8bf80c8a71ddbe7aba51f55"     # Debug script location
    mock_mode: false                                      # Use real API vs mocks

  # Validation Settings (OPTIONAL)
  validation:
    level: "basic"                                        # basic|enhanced|full
    connectivity_check: true                              # Test API connection on load
    cache_results: true                                   # Cache validation for performance
```

### Field Documentation

**REQUIRED Fields**:
- `publishing.default_parent`: Core publishing functionality dependency
- `adrs.database_id`: Multi-user ADR publishing blocker if missing

**OPTIONAL Fields with Sensible Defaults**:
- `workspace.id`: API discovery fallback
- `development.*`: Environment variable fallbacks
- `validation.*`: Progressive enhancement

### Error Handling Design

**Missing Required Configuration**:
```python
if not config.get('notion', {}).get('adrs', {}).get('database_id'):
    raise ConfigurationError(
        "ADR database not configured.\n"
        "Add 'notion.adrs.database_id' to config/PIPER.user.md\n"
        "Run 'piper notion setup' to configure workspace"
    )
```

**Invalid Configuration**:
```python
if not validate_notion_id(database_id):
    raise ConfigurationError(
        f"Invalid ADR database ID format: {database_id}\n"
        "Expected: 32-character hex string\n"
        "Run 'piper notion list-databases' to find valid IDs"
    )
```

---

## VALIDATION TIER IMPLEMENTATION

### MVP Validation (Default)

```python
def validate_basic_config(config: dict) -> bool:
    """MVP validation: format + connectivity"""
    # Format validation
    for id_field in ['adrs.database_id', 'publishing.default_parent']:
        value = get_nested_config(config, id_field)
        if value and not is_valid_notion_id(value):
            raise ValueError(f"Invalid format for {id_field}: {value}")

    # Basic connectivity test (single API call)
    if config.get('validation', {}).get('connectivity_check', True):
        test_api_connection()

    return True
```

### Enhanced Validation (Opt-in)

```python
def validate_enhanced_config(config: dict) -> bool:
    """Enhanced validation: resource accessibility"""
    # Test actual resource access
    # Performance impact acceptable for opt-in usage
    pass
```

---

## MIGRATION STRATEGY SPECIFICATION

### User Setup Process

**Step 1**: Copy template to PIPER.user.md
**Step 2**: Extract hardcoded values using provided documentation
**Step 3**: Validate configuration with `piper notion test-config`
**Step 4**: Test functionality with actual operations

### Migration Documentation Template

```markdown
## Migration from Hardcoded Values

If you've been using development scripts, extract these values to configuration:

### ADR Database (REQUIRED)
- **Location**: `scripts/fields.py:12`, `scripts/adr.py:12`
- **Value**: `25e11704d8bf80deaac2f806390fe7da`
- **Add to**: `notion.adrs.database_id`

### Test Configuration (OPTIONAL)
- **Location**: `tests/publishing/test_publish_command.py:18`
- **Value**: `25d11704d8bf81dfb37acbdc143e6a80`
- **Add to**: `notion.development.test_parent`

[Additional mappings...]
```

---

## ADR-027 DOCUMENTATION REQUIREMENTS

### Architectural Decision Record Topics

**Title**: "Configuration Architecture: User vs System Separation"

**Decision Points**:
1. PIPER.user.md extension vs separate configuration files
2. Required vs optional field categorization
3. Fail-fast error handling approach
4. Manual migration strategy selection
5. Tiered validation implementation approach

**Consequences**:
- Multi-user support enabled through user configuration
- Clear error messages improve user experience
- Manual migration maintains user control
- Tiered validation balances performance with functionality

---

## SUCCESS CRITERIA

### Schema Design Complete
- [ ] YAML structure defined with required/optional categorization
- [ ] Error handling patterns specified
- [ ] Migration strategy documented
- [ ] ADR-027 created with architectural decisions

### Implementation Ready
- [ ] Configuration loader requirements specified
- [ ] Validation tier implementation approach defined
- [ ] User setup process documented
- [ ] Migration guidance prepared

**Time Target**: 20 minutes comprehensive schema design with ADR documentation
