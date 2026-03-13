# GREAT-3B Phase 0: Plugin Loading Investigation

**Agent**: Cursor (Programmer)
**Date**: Friday, October 3, 2025
**Time**: 1:57 PM - 2:25 PM
**Duration**: 28 minutes

## Executive Summary

**Mission**: Investigate current plugin loading in web/app.py, analyze what needs to change, and design new discovery-based dynamic loading pattern.

**Status**: ✅ **INVESTIGATION COMPLETE**

**Key Finding**: Current static import pattern can be replaced with discovery-based loading while maintaining full backwards compatibility and robust error handling.

## Current State Analysis

### Plugin Loading Flow (web/app.py)

**Current Pattern**:

```python
# Phase 3C: Import plugins (triggers auto-registration)
print("  📦 Loading plugins...")
from services.integrations.calendar.calendar_plugin import _calendar_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.slack.slack_plugin import _slack_plugin

# Initialize all registered plugins
init_results = await registry.initialize_all()

# Mount plugin routers
routers = registry.get_routers()
for router in routers:
    app.include_router(router)
```

**Current Limitations**:

- ❌ **Static imports**: All plugins loaded regardless of config
- ❌ **No discovery**: Hardcoded list of 4 specific plugins
- ❌ **No filtering**: Can't disable individual plugins
- ❌ **Import failures**: Would crash startup entirely

**Current Strengths**:

- ✅ **Error handling**: Plugin init/shutdown failures don't crash app
- ✅ **Registry pattern**: Clean separation of concerns
- ✅ **Auto-registration**: Plugins register themselves on import
- ✅ **Lifecycle management**: Proper init/shutdown flow

## New Loading Pattern Design

### Proposed Flow

```python
# Phase 3B: Plugin System (Dynamic Loading)
print("\n🔌 Initializing Plugin System...")

try:
    from services.plugins import get_plugin_registry

    registry = get_plugin_registry()

    # Step 1: Discover available plugins
    available = registry.discover_plugins()  # NEW METHOD
    print(f"  📦 Discovered {len(available)} plugin(s)")

    # Step 2: Load enabled plugins from config
    enabled = registry.load_enabled_plugins()  # NEW METHOD
    print(f"  ✅ Loaded {len(enabled)} plugin(s)")

    # Step 3: Initialize loaded plugins (EXISTING)
    init_results = await registry.initialize_all()
    success_count = sum(1 for success in init_results.values() if success)
    print(f"  ✅ Initialized {success_count}/{len(init_results)} plugin(s)")

    # Step 4: Mount plugin routers (EXISTING)
    routers = registry.get_routers()
    for router in routers:
        app.include_router(router)
    print(f"  ✅ Mounted {len(routers)} router(s)")

except Exception as e:
    print(f"  ⚠️ Plugin system error: {e}")
    # Don't fail startup if plugins have issues
```

### New Registry Methods Required

**1. `discover_plugins()` Method**:

- Scan `services/integrations/*/plugin.py` files
- Return list of available plugin names
- Handle missing directories gracefully

**2. `load_enabled_plugins()` Method**:

- Read plugin configuration
- Import only enabled plugins using `importlib`
- Handle import failures gracefully (log and continue)

### Configuration Design

**New Config Section** (in `config/PIPER.user.md`):

```yaml
plugins:
  enabled:
    - slack
    - notion
    - github
    - calendar
  disabled: []

  # Plugin-specific settings
  slack:
    auto_initialize: true
  notion:
    auto_initialize: true
  github:
    auto_initialize: true
  calendar:
    auto_initialize: true
```

**Default Behavior** (backwards compatible):

- If config missing → load all discovered plugins
- If config malformed → load all discovered plugins
- If no plugins discovered → continue without plugins

## Error Handling Strategy

### Fatal vs Non-Fatal Classification

**NON-FATAL** (log and continue - all plugin failures):

- ✅ Plugin file missing
- ✅ Plugin syntax error
- ✅ Plugin import failure
- ✅ Plugin config invalid
- ✅ Plugin initialization failure
- ✅ No plugins found
- ✅ All plugins disabled

**FATAL** (crash startup):

- None - all plugin failures should be non-fatal

### Error Handling Implementation

```python
# Import failure handling
try:
    module = importlib.import_module(f"services.integrations.{plugin_name}.{plugin_name}_plugin")
except ImportError as e:
    self.logger.warning(f"Plugin '{plugin_name}' not found: {e}")
    continue
except SyntaxError as e:
    self.logger.error(f"Plugin '{plugin_name}' has syntax error: {e}")
    continue
except Exception as e:
    self.logger.error(f"Plugin '{plugin_name}' failed to load: {e}")
    continue
```

## Backwards Compatibility Plan

### Migration Strategy

**Phase 1: Add Discovery (Non-Breaking)**

- Add new registry methods
- Keep static imports as fallback
- No config required initially

**Phase 2: Config Support (Optional)**

- Add plugin config section
- If config missing → load all (current behavior)
- If config present → respect enabled/disabled

**Phase 3: Remove Static Imports (Breaking)**

- Remove hardcoded imports from web/app.py
- Rely entirely on discovery + config
- Provide migration guide

### Fallback Behavior

**Discovery Fails**: Fall back to static imports
**Config Missing**: Load all discovered plugins
**No Plugins Found**: Continue without plugin system

## Shutdown Flow Analysis

**Impact**: ✅ **NO CHANGES NEEDED**

- Shutdown operates on registered plugins only
- Registry tracks what was actually loaded/initialized
- Failed imports don't register, so won't be in shutdown
- Current error handling already robust

## Testing Strategy

### Test Scenarios

1. **All plugins enabled** (current behavior)
2. **Some plugins disabled**
3. **Plugin missing but enabled in config**
4. **Config file missing entirely**
5. **Empty/invalid config format**
6. **No plugins discovered**

### Testing Approach

**Unit Tests**: Discovery and loading methods in isolation
**Integration Tests**: Various config scenarios end-to-end
**Feature Flag**: Safe parallel testing alongside static imports
**Validation**: Compare old vs new loading results

### Safe Testing Pattern

```python
USE_DYNAMIC_LOADING = os.getenv("PIPER_USE_DYNAMIC_PLUGIN_LOADING", "false").lower() == "true"

if USE_DYNAMIC_LOADING:
    # New dynamic loading path
    available = registry.discover_plugins()
    enabled = registry.load_enabled_plugins()
else:
    # Current static import path (fallback)
    from services.integrations.slack.slack_plugin import _slack_plugin
    # ... etc
```

## Implementation Roadmap

### Next Steps

1. **Code Agent**: Implement `discover_plugins()` and `load_enabled_plugins()` methods
2. **Config**: Add plugin configuration section to PIPER.user.md
3. **Web App**: Update lifespan function to use new loading pattern
4. **Tests**: Implement comprehensive test suite
5. **Documentation**: Update plugin development guide

### Success Criteria

- [ ] Discovery method finds all 4 current plugins
- [ ] Loading method respects config enable/disable
- [ ] Error handling prevents startup crashes
- [ ] Backwards compatibility maintained
- [ ] Comprehensive test coverage
- [ ] Documentation updated

## Risk Assessment

**LOW RISK**:

- Non-breaking changes initially
- Comprehensive fallback behavior
- Extensive error handling
- Gradual migration path

**MITIGATION**:

- Feature flag for safe testing
- Parallel validation against current behavior
- Comprehensive test suite before deployment

---

**Investigation Status**: ✅ **COMPLETE**
**Confidence Level**: HIGH
**Ready for Implementation**: YES

**Key Insight**: The plugin system can be made fully dynamic while maintaining 100% backwards compatibility through intelligent defaults and robust fallback behavior.
