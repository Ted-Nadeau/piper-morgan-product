# Gameplan: GREAT-3B - Plugin Infrastructure

**Date**: October 3, 2025
**Epic**: GREAT-3B (GitHub Issue #198)
**Chief Architect**: Claude Opus 4.1
**Context**: Building on GREAT-3A's plugin foundation (interface, registry, 4 operational plugins)

## Mission

Enhance the plugin system created in GREAT-3A with dynamic loading, automatic discovery, lifecycle management, and configuration integration.

## Current State (from GREAT-3A)

### What We Have
- ✅ PiperPlugin interface defined (6 methods)
- ✅ PluginRegistry operational (singleton pattern)
- ✅ 4 plugin wrappers working (Slack, GitHub, Notion, Calendar)
- ✅ 72 tests passing
- ✅ Config services standardized

### What We Need
- Dynamic plugin loading (replace static imports)
- Automatic discovery mechanism
- Lifecycle hooks (enable/disable at runtime)
- Plugin metadata system
- Per-plugin configuration

## Phase Structure

### Phase -1: Infrastructure Verification
**Lead Developer - Before Agent Deployment**

```bash
# Verify plugin foundation from 3A
ls -la services/plugins/
python -c "from services.plugins import PluginRegistry; print(PluginRegistry().list_plugins())"

# Check current import pattern
grep -r "from services.plugins.wrappers" . --include="*.py"

# Verify tests still passing
pytest services/plugins/tests/ -v
```

**Expected**: 4 plugins registered, 72 tests passing

### Phase 0: Investigation
**Both Agents - 30 minutes**

**Questions to Answer**:
1. How are plugins currently loaded? (static imports?)
2. What prevents dynamic loading now?
3. How should discovery work? (directory scan? config file?)
4. What metadata do plugins need?
5. How to handle plugin dependencies?

**Investigate**:
```bash
# Current loading mechanism
grep -A5 "class PluginRegistry" services/plugins/registry.py

# Plugin wrapper structure
ls -la services/plugins/wrappers/

# Config integration points
grep -r "config_service" services/plugins/ --include="*.py"
```

### Phase 1: Dynamic Plugin Loading
**Claude Code - Implementation**

**Replace Static Imports**:
```python
# Current (static)
from services.plugins.wrappers.slack_plugin import SlackPlugin
registry.register(SlackPlugin())

# Target (dynamic)
plugin_module = importlib.import_module(f"services.plugins.wrappers.{name}")
plugin_class = getattr(plugin_module, f"{name.title()}Plugin")
registry.register(plugin_class())
```

**Cursor Agent - Testing**
- Create test plugins
- Verify dynamic loading
- Test error handling

### Phase 2: Plugin Discovery System
**Cursor Agent - Directory Scanner**

```python
class PluginDiscovery:
    def discover_plugins(self, path="services/plugins/wrappers"):
        """Scan directory for plugin modules"""

    def validate_plugin(self, module):
        """Ensure module has valid plugin class"""

    def get_plugin_metadata(self, plugin_class):
        """Extract name, version, dependencies"""
```

**Claude Code - Auto-Registration**
- Integrate discovery with registry
- Handle registration errors
- Support plugin priorities

### Phase 3: Lifecycle Management
**Both Agents Collaborate**

**Required Lifecycle Hooks**:
```python
class PiperPlugin:
    def enable(self) -> bool:
        """Enable plugin at runtime"""

    def disable(self) -> bool:
        """Disable plugin at runtime"""

    def reload(self) -> bool:
        """Reload configuration"""

    def health_check(self) -> dict:
        """Report plugin status"""
```

**Implementation**:
- Add to base interface
- Update all 4 plugin wrappers
- Test runtime enable/disable

### Phase 4: Plugin Metadata System
**Claude Code - Metadata Structure**

```python
class PluginMetadata:
    name: str
    version: str
    author: str
    description: str
    dependencies: List[str]
    config_schema: dict
    capabilities: List[str]
```

**Cursor Agent - Metadata Integration**
- Add metadata to each plugin
- Create metadata validation
- Build plugin info endpoint

### Phase 5: Configuration Integration
**Both Agents - Config per Plugin**

**Requirements**:
- Each plugin has config namespace
- Validation at plugin load time
- Runtime config updates
- Integration with ConfigValidator

```yaml
# config/plugins.yaml
plugins:
  slack:
    enabled: true
    config:
      workspace: "dev"
  github:
    enabled: true
    config:
      org: "default"
```

### Phase Z: Validation & Documentation
**Both Agents - Final Verification**

```bash
# Dynamic loading works
python -c "from services.plugins import PluginRegistry; registry = PluginRegistry(); registry.discover_and_load()"

# Lifecycle management works
python test_plugin_lifecycle.py

# All tests passing
pytest services/plugins/ -v

# Documentation complete
ls -la services/plugins/docs/
```

## Anti-80% Checklist

```
Component        | Built | Tested | Documented | Integrated
---------------- | ----- | ------ | ---------- | ----------
Dynamic Loading  | [ ]   | [ ]    | [ ]        | [ ]
Discovery System | [ ]   | [ ]    | [ ]        | [ ]
Lifecycle Mgmt   | [ ]   | [ ]    | [ ]        | [ ]
Metadata System  | [ ]   | [ ]    | [ ]        | [ ]
Config per Plugin| [ ]   | [ ]    | [ ]        | [ ]
TOTAL: 0/20 = 0% (Must reach 100%)
```

## STOP Conditions

Stop immediately if:
1. Breaking existing plugin functionality
2. Tests drop below 72 passing
3. Circular dependency in loading
4. Performance degradation >100ms
5. Security concern with dynamic loading

## Time Estimate

- Phase -1: 5 minutes (verification)
- Phase 0: Half a mango (investigation)
- Phase 1: One mango (dynamic loading)
- Phase 2: One mango (discovery system)
- Phase 3: One mango (lifecycle management)
- Phase 4: Half a mango (metadata)
- Phase 5: Half a mango (config integration)
- Phase Z: Half a mango (validation)

**Total**: ~5 mangos (1-2 hurons)

## Success Criteria

### Must Achieve
- [ ] Dynamic plugin loading operational
- [ ] Automatic discovery working
- [ ] Lifecycle management implemented
- [ ] Plugin metadata system complete
- [ ] Per-plugin configuration working
- [ ] All existing tests still passing
- [ ] Documentation updated

### Nice to Have
- [ ] Plugin dependency resolution
- [ ] Hot reload without restart
- [ ] Plugin marketplace metadata

## Key Decisions for PM/Architect

1. **Discovery Method**: Directory scan vs config file vs both?
2. **Metadata Format**: JSON, YAML, or Python attributes?
3. **Config Location**: Unified plugins.yaml vs per-plugin files?
4. **Dependency Handling**: Error vs auto-install vs warn?

---

*Gameplan prepared for GREAT-3B execution*
*Building on solid foundation from GREAT-3A*
