# GREAT-3B: Plugin Infrastructure

## Context
Second sub-epic of GREAT-3. Creates core plugin system building on refactored foundation from 3A.

## Scope
1. **Plugin Interface Definition**
   - Build on existing router pattern
   - Define standard plugin contract
   - Support for three spatial patterns
   - Lifecycle hooks (init, enable, disable, cleanup)

2. **Plugin Loader System**
   - Dynamic plugin discovery
   - Plugin registration mechanism
   - Dependency resolution
   - Error handling for missing plugins

3. **Configuration System**
   - Per-plugin configuration
   - Enable/disable flags
   - Configuration validation
   - Integration with ConfigValidator

4. **Plugin Manager**
   - Orchestrate plugin lifecycle
   - Handle plugin communication
   - Manage plugin state
   - Provide plugin API to core

## Acceptance Criteria
- [ ] Plugin interface defined
- [ ] Plugin loader operational
- [ ] Configuration system working
- [ ] Sample plugin demonstrates interface
- [ ] Plugin can be enabled/disabled
- [ ] Core has no direct plugin imports

## Success Validation
```bash
# Plugin interface exists
ls -la services/plugin_base.py

# Loader can discover plugins
python -c "from services.plugin_manager import PluginManager; pm = PluginManager(); print(pm.discover_plugins())"

# Configuration working
DISABLED_PLUGINS=sample python main.py  # Starts without sample plugin

# Tests passing
pytest tests/plugin_infrastructure/ -v
```

## Time Estimate
One huron
