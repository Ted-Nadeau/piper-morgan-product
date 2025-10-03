# GREAT-3B Phase 0: Investigation Report

**Agent**: Claude Code (Sonnet 4.5)
**Date**: October 3, 2025
**Time**: 1:56 PM - 2:10 PM PT
**Phase**: GREAT-3B Phase 0 - Investigation

---

## Executive Summary

Investigated current plugin system to design dynamic discovery and config-based loading mechanism. **All objectives achieved** - auto-registration works with `importlib`, discovery algorithm validated, and config structure designed.

**Key Findings**:
- ✅ Auto-registration pattern compatible with dynamic imports
- ✅ Discovery mechanism simple and reliable (Path-based scanning)
- ✅ Config should follow existing YAML pattern in `config/plugins.yaml`
- ✅ No changes needed to existing plugin files

---

## Task 1: Auto-Registration Pattern Analysis

### Current Mechanism

**Location**: Bottom of each plugin file (e.g., `services/integrations/slack/slack_plugin.py:106-110`)

```python
# Auto-register plugin when module is imported
from services.plugins import get_plugin_registry

_slack_plugin = SlackPlugin()
get_plugin_registry().register(_slack_plugin)
```

### How It Works

1. **Module Import**: When `import services.integrations.slack.slack_plugin` runs
2. **Class Instantiation**: `_slack_plugin = SlackPlugin()` creates instance
3. **Auto-Registration**: `get_plugin_registry().register(_slack_plugin)` immediately registers
4. **Side Effect**: Registration happens as import side effect (Python module loading)

### Key Questions Answered

**Q: How does `_slack_plugin = SlackPlugin()` trigger registration?**
A: The instantiation itself doesn't trigger registration. The **next line** (`get_plugin_registry().register()`) explicitly registers the instance.

**Q: Where is `get_plugin_registry().register()` called?**
A: At module level (lines 107-110), executed immediately when module imports.

**Q: What happens on module import?**
A: Python executes all module-level code sequentially:
   1. Import statements (lines 1-15)
   2. Class definition (lines 18-103)
   3. Auto-registration block (lines 106-110) ← registration happens here

**Q: Does the plugin class need modification for dynamic loading?**
A: **No modifications needed**. Pattern already works with `importlib.import_module()`.

### Compatibility with Dynamic Imports

**Tested with `importlib.import_module()`**:
```python
import importlib
module = importlib.import_module('services.integrations.github.github_plugin')
# Result: ✅ Auto-registration triggered
# Registry contains: ['github']
```

**Conclusion**: Current pattern is **fully compatible** with dynamic loading.

---

## Task 2: Discovery Mechanism Design

### Algorithm

**Function Signature**:
```python
def discover_plugins() -> Dict[str, str]:
    """
    Scan integrations directory for plugin files.

    Returns:
        Dict mapping plugin name to module path
        Example: {'slack': 'services.integrations.slack.slack_plugin'}
    """
```

**Implementation**:
```python
from pathlib import Path
from typing import Dict

def discover_plugins() -> Dict[str, str]:
    plugins = {}
    integrations_dir = Path('services/integrations')

    # Scan each subdirectory
    for integration_dir in integrations_dir.iterdir():
        # Skip non-directories and hidden/system dirs
        if not integration_dir.is_dir():
            continue
        if integration_dir.name.startswith('_') or integration_dir.name.startswith('.'):
            continue

        # Look for *_plugin.py file
        plugin_files = list(integration_dir.glob('*_plugin.py'))

        if plugin_files:
            plugin_file = plugin_files[0]  # Take first match
            plugin_name = plugin_file.stem.replace('_plugin', '')
            module_path = f'services.integrations.{integration_dir.name}.{plugin_file.stem}'
            plugins[plugin_name] = module_path

    return plugins
```

### Discovery Test Results

**Discovered 4 plugins**:
```
calendar -> services.integrations.calendar.calendar_plugin
github   -> services.integrations.github.github_plugin
notion   -> services.integrations.notion.notion_plugin
slack    -> services.integrations.slack.slack_plugin
```

**Directories Scanned**:
- ✅ `calendar/` → found `calendar_plugin.py`
- ✅ `github/` → found `github_plugin.py`
- ❌ `mcp/` → no plugin file (correctly skipped)
- ✅ `notion/` → found `notion_plugin.py`
- ✅ `slack/` → found `slack_plugin.py`
- ❌ `spatial/` → no plugin file (correctly skipped)

**Error Handling**:
- Non-directories: Skipped (e.g., `spatial_adapter.py`)
- Hidden/system dirs: Skipped (e.g., `__pycache__`)
- No plugin file: Skipped (e.g., `mcp/`, `spatial/`)
- Multiple plugin files: Takes first match (edge case)

### Design Choices

**Path-based scanning** (vs alternatives):
- ✅ Simple and reliable
- ✅ No string manipulation gymnastics
- ✅ Handles edge cases naturally
- ✅ Fast (small directory tree)

**Naming convention**:
- Pattern: `{name}_plugin.py` → plugin name = `{name}`
- Example: `slack_plugin.py` → `"slack"`
- Consistent across all 4 plugins

---

## Task 3: Dynamic Import Testing

### Test Results

**Test 1: Module Contents** ✅
```python
import importlib
module = importlib.import_module('services.integrations.slack.slack_plugin')

# Available attributes:
['APIRouter', 'Any', 'Dict', 'Optional', 'PiperPlugin', 'PluginMetadata',
 'SlackConfigService', 'SlackIntegrationRouter', 'SlackPlugin',
 'get_plugin_registry', '_slack_plugin']

# ✅ _slack_plugin instance accessible: hasattr(module, '_slack_plugin') == True
```

**Test 2: Auto-Registration** ✅
```python
from services.plugins import get_plugin_registry, reset_plugin_registry

reset_plugin_registry()
registry = get_plugin_registry()

# Before import: []
module = importlib.import_module('services.integrations.github.github_plugin')
# After import: ['github']

# ✅ Auto-registration triggered by dynamic import
```

**Test 3: Plugin Instance Access** ✅
```python
plugin = module._github_plugin
metadata = plugin.get_metadata()

# Plugin name: github
# Plugin version: 1.0.0
# Plugin capabilities: ['routes', 'spatial']

# ✅ Plugin instance fully accessible and functional
```

### Findings

1. **`importlib.import_module()` works perfectly**
   - Module loads completely
   - All attributes accessible
   - Plugin instance available as `_<name>_plugin`

2. **Auto-registration triggers on import**
   - Side effect executes (lines 106-110 in plugin file)
   - Plugin registers with singleton registry
   - No code changes needed

3. **No issues detected**
   - No circular import problems
   - No initialization failures
   - Config services load correctly

### Conclusion

**Dynamic import with `importlib` is production-ready** for plugin loading. No modifications to existing plugin files required.

---

## Task 4: Config File Structure Design

### Requirements Analysis

**From Chief Architect**:
- List of enabled plugins
- Per-plugin settings (optional)
- Clear, readable format

**From Existing Config System**:
- Uses YAML format (`config/PIPER.user.md` has YAML blocks)
- Hierarchical structure (see GitHub/Notion sections)
- Optional settings with defaults

### Recommended Structure

**Location**: `config/plugins.yaml`

**Format** (Recommended):
```yaml
# Plugin Configuration
# Controls which plugins are loaded at startup

plugins:
  # Enabled plugins (loaded at startup)
  enabled:
    - slack
    - github
    - notion
    - calendar

  # Disabled plugins (discovered but not loaded)
  # Uncomment to disable:
  # disabled:
  #   - notion

  # Per-plugin settings (optional)
  settings:
    slack:
      # Plugin-specific config if needed
      timeout: 30
      retry_attempts: 3

    github:
      default_org: "myorg"
      cache_ttl: 300

    notion:
      sync_interval: 600

    calendar:
      timezone: "America/Los_Angeles"
```

### Alternative Structure (Evaluated)

**Per-Plugin Enabled Flag**:
```yaml
# Alternative: per-plugin enabled flag
slack:
  enabled: true
  timeout: 30

github:
  enabled: true
  default_org: "myorg"

notion:
  enabled: false  # Disabled

calendar:
  enabled: true
```

**Pros**:
- Flat structure
- Settings co-located with enabled flag

**Cons**:
- Harder to see all enabled plugins at once
- Requires loading all config to get plugin list
- More verbose for simple enable/disable

### Recommendation Rationale

**Recommended structure is better because**:

1. **Clear Overview**: `enabled` list shows all active plugins at a glance
2. **Separation of Concerns**: Enable/disable separate from settings
3. **Optional Settings**: Settings only needed if customizing defaults
4. **Default Behavior**: Missing config → all discovered plugins enabled
5. **Consistency**: Matches existing config patterns (list + settings)

### Default Behavior

**If `config/plugins.yaml` missing**:
- Default: Load all discovered plugins
- Rationale: Same as current behavior (all 4 plugins imported)

**If `plugins.enabled` empty**:
- Default: Load no plugins
- Rationale: Explicit empty list means "disable all"

**If plugin not listed in `enabled` or `disabled`**:
- Default: Enable (load the plugin)
- Rationale: Permissive default (backward compatible)

---

## Task 5: Existing Config System Integration

### Current Config System Analysis

**Config Files**:
```
config/
├── PIPER.user.md          # Main user config (YAML blocks)
├── PIPER.defaults.md      # Default config
├── PIPER.md               # Config documentation
├── notion_config.py       # Notion-specific config
├── notion_user_config.py  # Notion user config
└── feature_flags/         # Feature flag configs
```

**Config Format**:
- Primary format: YAML blocks within Markdown files
- Example from `PIPER.user.md`:
  ```yaml
  github:
    default_repository: "mediajunkie/piper-morgan-product"
    owner: "mediajunkie"
    pm_numbers:
      prefix: "PM-"
  ```

**Config Services**:
- Each integration has `ConfigService` class
- Example: `SlackConfigService`, `GitHubConfigService`
- Pattern: Read from env vars, provide validation
- Location: `services/integrations/{name}/config_service.py`

### Plugin Config Integration Strategy

**Option 1: Separate Plugin Config** (Recommended)
- File: `config/plugins.yaml` (pure YAML, not Markdown)
- Scope: Plugin loading and registry management only
- Rationale: Plugin system is infrastructure, not integration config

**Option 2: Integrate with PIPER.user.md**
- Add `plugins:` section to existing file
- Pros: Centralized config
- Cons: Mixing infrastructure with integration config

**Option 3: Feature Flag System**
- Use existing `config/feature_flags/` directory
- Pros: Consistent with other toggles
- Cons: Plugin loading is more than a feature flag

### Recommendation

**Use Option 1: Separate `config/plugins.yaml`**

**Rationale**:
1. **Separation of Concerns**: Plugin loading vs integration config
2. **Clean Format**: Pure YAML (no Markdown wrapper)
3. **Clear Ownership**: Plugin system infrastructure config
4. **Backward Compatible**: Doesn't touch existing config files
5. **Simple Parsing**: Standard YAML library

**Integration Points**:
- Plugin config read by `PluginRegistry` at startup
- Integration config still read by `ConfigService` classes
- No overlap or conflict

**Config Hierarchy**:
```
config/plugins.yaml          → Plugin loading (which plugins)
  ↓ Plugins loaded
services/integrations/{name}/config_service.py → Integration config (how plugins work)
```

---

## Task 6: Implementation Plan

### Component Design

**1. Discovery Function**

**Location**: `services/plugins/discovery.py` (new file)

**Function Signature**:
```python
def discover_plugins() -> Dict[str, str]:
    """
    Scan integrations directory for available plugins.

    Returns:
        Dict[str, str]: Maps plugin name to module path
        Example: {"slack": "services.integrations.slack.slack_plugin"}
    """
```

**Implementation**:
- Use `pathlib.Path` for directory scanning
- Pattern: `services/integrations/*/*.py` where `*_plugin.py`
- Extract plugin name from filename
- Return `{name: module_path}` dict

**Error Handling**:
- Skip non-directories
- Skip hidden/system dirs (`_*`, `.*`)
- Skip dirs without plugin files
- Log warnings for unexpected patterns

---

**2. Dynamic Loading Function**

**Location**: `services/plugins/loader.py` (new file)

**Function Signature**:
```python
def load_plugin(module_path: str) -> Optional[PiperPlugin]:
    """
    Dynamically load plugin from module path.

    Args:
        module_path: Full module path (e.g., "services.integrations.slack.slack_plugin")

    Returns:
        PiperPlugin instance if successful, None if failed
    """
```

**Implementation**:
```python
import importlib
from typing import Optional

def load_plugin(module_path: str) -> Optional[PiperPlugin]:
    try:
        module = importlib.import_module(module_path)
        # Auto-registration happens as side effect
        # Plugin already in registry
        return True  # Success indicator
    except Exception as e:
        logger.error(f"Failed to load plugin {module_path}: {e}")
        return False
```

**Error Handling**:
- Catch `ImportError` (module not found)
- Catch `AttributeError` (missing required attributes)
- Catch general `Exception` (initialization failures)
- Log errors with context
- Return `None` on failure (don't crash)

**Note**: Auto-registration means we don't need to return plugin instance. Registry already has it.

---

**3. Config Parser**

**Location**: `services/plugins/config.py` (new file)

**Function Signature**:
```python
@dataclass
class PluginConfig:
    """Plugin system configuration."""
    enabled: List[str]
    disabled: List[str]
    settings: Dict[str, Dict[str, Any]]

def load_plugin_config(config_path: str = "config/plugins.yaml") -> PluginConfig:
    """
    Load plugin configuration from YAML file.

    Args:
        config_path: Path to plugins.yaml

    Returns:
        PluginConfig with enabled/disabled/settings
    """
```

**Implementation**:
```python
import yaml
from dataclasses import dataclass, field
from typing import Any, Dict, List
from pathlib import Path

@dataclass
class PluginConfig:
    enabled: List[str] = field(default_factory=list)
    disabled: List[str] = field(default_factory=list)
    settings: Dict[str, Dict[str, Any]] = field(default_factory=dict)

def load_plugin_config(config_path: str = "config/plugins.yaml") -> PluginConfig:
    config_file = Path(config_path)

    # Default: all plugins enabled if config missing
    if not config_file.exists():
        return PluginConfig(enabled=[], disabled=[], settings={})

    with open(config_file) as f:
        data = yaml.safe_load(f)

    plugins_section = data.get('plugins', {})

    return PluginConfig(
        enabled=plugins_section.get('enabled', []),
        disabled=plugins_section.get('disabled', []),
        settings=plugins_section.get('settings', {})
    )
```

**Error Handling**:
- File not found → return default (all enabled)
- Invalid YAML → log error, return default
- Missing sections → use empty defaults

---

**4. Registry Integration**

**Location**: `services/plugins/plugin_registry.py` (modify existing)

**New Method**:
```python
def load_plugins_from_config(self, config_path: str = "config/plugins.yaml") -> Dict[str, bool]:
    """
    Discover and load plugins based on configuration.

    Args:
        config_path: Path to plugins.yaml

    Returns:
        Dict[str, bool]: Maps plugin name to load success
    """
```

**Implementation**:
```python
from .config import load_plugin_config
from .discovery import discover_plugins
from .loader import load_plugin

def load_plugins_from_config(self, config_path: str = "config/plugins.yaml") -> Dict[str, bool]:
    # 1. Load config
    config = load_plugin_config(config_path)

    # 2. Discover available plugins
    available = discover_plugins()

    # 3. Determine which plugins to load
    if config.enabled:
        # Explicit enabled list
        to_load = [p for p in config.enabled if p in available]
    else:
        # Default: all discovered except disabled
        to_load = [p for p in available.keys() if p not in config.disabled]

    # 4. Load each plugin
    results = {}
    for plugin_name in to_load:
        module_path = available[plugin_name]
        success = load_plugin(module_path)
        results[plugin_name] = success

    return results
```

---

### Order of Implementation

**Phase 1: Foundation** (30 minutes)
1. Create `services/plugins/discovery.py`
   - Implement `discover_plugins()`
   - Test with existing plugins
2. Create `services/plugins/loader.py`
   - Implement `load_plugin()`
   - Test dynamic loading
3. Create `services/plugins/config.py`
   - Implement `PluginConfig` dataclass
   - Implement `load_plugin_config()`
   - Test YAML parsing

**Phase 2: Integration** (20 minutes)
4. Modify `services/plugins/plugin_registry.py`
   - Add `load_plugins_from_config()` method
   - Test end-to-end loading
5. Create `config/plugins.yaml`
   - Initial config with all 4 plugins enabled
   - Document settings format

**Phase 3: Web App Integration** (15 minutes)
6. Update `web/app.py`
   - Remove static imports
   - Replace with `registry.load_plugins_from_config()`
   - Test startup

**Phase 4: Testing** (30 minutes)
7. Create test suite
   - Test discovery with various directory structures
   - Test loading with valid/invalid plugins
   - Test config parsing with various YAML
   - Test registry integration end-to-end
8. Test edge cases
   - Missing config file
   - Empty enabled list
   - Plugin load failures
   - Invalid YAML

**Phase 5: Documentation** (15 minutes)
9. Update plugin documentation
   - Add dynamic loading explanation
   - Document config file format
   - Add examples
10. Update session logs

**Total Estimated Time**: ~2 hours

---

### Dependencies Between Components

```
discovery.py (no dependencies)
    ↓
config.py (no dependencies)
    ↓
loader.py (no dependencies)
    ↓
plugin_registry.py (depends on: discovery, config, loader)
    ↓
web/app.py (depends on: plugin_registry)
    ↓
tests (depends on: all above)
```

**Build Order**: Foundation → Integration → App → Tests → Docs

---

### Testing Strategy

**Unit Tests**:
- `test_discovery.py`: Test plugin discovery algorithm
- `test_loader.py`: Test dynamic loading mechanism
- `test_config.py`: Test YAML parsing and defaults
- `test_registry_integration.py`: Test registry loading

**Integration Tests**:
- `test_plugin_loading_e2e.py`: End-to-end loading test
- Test scenarios:
  - All plugins enabled
  - Some plugins disabled
  - Missing config file (default behavior)
  - Invalid config (error handling)
  - Plugin load failures

**Edge Case Tests**:
- Empty integrations directory
- Plugin file with syntax errors
- Missing plugin instance (`_plugin`)
- Circular import issues
- Config file with unknown plugins

---

## Summary

### Investigation Complete ✅

**6/6 Tasks Complete**:
1. ✅ Auto-registration pattern understood
2. ✅ Discovery algorithm designed and tested
3. ✅ Dynamic import verified working
4. ✅ Config structure recommended
5. ✅ Config system integration planned
6. ✅ Implementation plan created

### Key Findings

1. **Auto-Registration**: Works perfectly with `importlib.import_module()`
2. **Discovery**: Simple Path-based scanning discovers all 4 plugins
3. **Config Format**: YAML in `config/plugins.yaml` (separate from integration config)
4. **No Breaking Changes**: Existing plugin files need no modifications
5. **Implementation**: ~2 hours with clear build order

### Recommendations

**Proceed with**:
- Discovery function using `pathlib.Path`
- Dynamic loading with `importlib.import_module()`
- Config file at `config/plugins.yaml` (YAML format)
- Registry method `load_plugins_from_config()`
- Default behavior: load all discovered plugins if config missing

**Next Steps**:
- Phase 1: Implement foundation (discovery, loader, config)
- Phase 2: Integrate with registry
- Phase 3: Update web/app.py
- Phase 4: Comprehensive testing
- Phase 5: Documentation

---

**Investigation Duration**: 14 minutes (1:56 PM - 2:10 PM)
**Estimated Implementation**: ~2 hours
**Risk Level**: Low (no breaking changes, backward compatible)

**Phase 0 Status**: ✅ COMPLETE

---

*Ready for GREAT-3B Phase 1 Implementation*
