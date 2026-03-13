# Claude Code Agent Prompt: GREAT-3B Phase 3 - Config Integration

## Session Log Management
Continue session log: `dev/2025/10/03/2025-10-03-[timestamp]-code-log.md`

Update with timestamped entries for Phase 3 work.

## Mission
**Implement Config Integration**: Add config parsing and selective plugin loading based on enabled list in `config/PIPER.user.md`.

## Context

**Phase 1 Complete**: Discovery system working
- `discover_plugins()` finds all available plugins

**Phase 2 Complete**: Dynamic loading working
- `load_plugin()` imports and registers plugins dynamically

**Phase 3 Goal**: Read config from PIPER.user.md and load only enabled plugins.

## Your Tasks

### Task 1: Examine Current Config Pattern

**Check how other services read PIPER.user.md**:
```bash
# See what's in the config
cat config/PIPER.user.md | head -50

# Find how config is currently parsed
grep -r "PIPER.user.md" services/ --include="*.py" -B 2 -A 5

# Look for YAML extraction pattern
grep -r "yaml.load" services/ --include="*.py" -B 2 -A 5

# Check config service implementations
ls -la services/integrations/*/config_service.py
cat services/integrations/slack/config_service.py | head -30
```

**Questions to Answer**:
1. How do integration config services currently read PIPER.user.md?
2. Is there a common YAML extraction pattern?
3. Where should plugin config reader live?
4. Should we follow existing pattern or create new?

### Task 2: Add Plugin Config to PIPER.user.md

**File**: `config/PIPER.user.md`

**Add section** (if not already present):

```markdown
## Plugin Configuration

Configure which plugins are enabled and their settings.

```yaml
plugins:
  enabled:
    - github
    - slack
    - notion
    - calendar

  settings:
    github:
      # Plugin-specific settings (optional)
      timeout: 30
    slack:
      # Plugin-specific settings (optional)
      workspace: "engineering"
```

**Note**: All plugins enabled by default matches current behavior (backwards compatible).

### Task 3: Implement Config Reader Method

**File**: `services/plugins/plugin_registry.py`

**Add method to PluginRegistry class**:

```python
def _read_plugin_config(self) -> Dict[str, Any]:
    """
    Read plugin configuration from PIPER.user.md.

    Extracts YAML block from Plugin Configuration section.

    Returns:
        Dict containing plugin config, or empty dict if not found

    Default Behavior:
        - If config file missing: return empty dict
        - If plugin section missing: return empty dict
        - If YAML invalid: log error, return empty dict
    """
    import yaml
    from pathlib import Path

    config_path = Path("config/PIPER.user.md")

    if not config_path.exists():
        self.logger.warning("Config file not found: config/PIPER.user.md")
        return {}

    try:
        content = config_path.read_text()

        # Find Plugin Configuration section
        # Look for ## Plugin Configuration header
        if "## Plugin Configuration" not in content:
            self.logger.debug("No Plugin Configuration section found")
            return {}

        # Extract YAML block after Plugin Configuration header
        # YAML block is between ```yaml and ```
        lines = content.split("\n")
        in_plugin_section = False
        in_yaml_block = False
        yaml_lines = []

        for line in lines:
            if "## Plugin Configuration" in line:
                in_plugin_section = True
                continue

            if in_plugin_section:
                # End of section if we hit another ## header
                if line.startswith("## ") and "Plugin Configuration" not in line:
                    break

                # Start of YAML block
                if "```yaml" in line:
                    in_yaml_block = True
                    continue

                # End of YAML block
                if in_yaml_block and "```" in line:
                    break

                # Collect YAML lines
                if in_yaml_block:
                    yaml_lines.append(line)

        if not yaml_lines:
            self.logger.debug("No YAML block found in Plugin Configuration")
            return {}

        # Parse YAML
        yaml_content = "\n".join(yaml_lines)
        config = yaml.safe_load(yaml_content)

        self.logger.info(
            "Loaded plugin configuration",
            extra={"config": config}
        )
        return config or {}

    except yaml.YAMLError as e:
        self.logger.error(
            f"Invalid YAML in plugin configuration: {e}",
            extra={"error": str(e)}
        )
        return {}
    except Exception as e:
        self.logger.error(
            f"Error reading plugin configuration: {e}",
            extra={"error": str(e)}
        )
        return {}


def get_enabled_plugins(self) -> List[str]:
    """
    Get list of enabled plugins from configuration.

    Returns:
        List of enabled plugin names

    Default Behavior:
        - If no config: return all discovered plugins (backwards compatible)
        - If config exists but no enabled list: return all discovered plugins
        - If empty enabled list: return empty list (all plugins disabled)
    """
    config = self._read_plugin_config()

    # Get enabled list from config
    if "plugins" in config and "enabled" in config["plugins"]:
        enabled = config["plugins"]["enabled"]
        self.logger.info(
            f"Enabled plugins from config: {enabled}",
            extra={"enabled_plugins": enabled}
        )
        return enabled if enabled is not None else []

    # Default: all discovered plugins enabled
    available = self.discover_plugins()
    all_plugins = list(available.keys())

    self.logger.info(
        f"No config found, enabling all discovered plugins: {all_plugins}",
        extra={"enabled_plugins": all_plugins}
    )
    return all_plugins
```

### Task 4: Implement Selective Loading Method

**File**: `services/plugins/plugin_registry.py`

**Add method to PluginRegistry class**:

```python
def load_enabled_plugins(self) -> Dict[str, bool]:
    """
    Discover and load only enabled plugins.

    Combines discovery, config reading, and selective loading.

    Returns:
        Dict mapping plugin name to load success status

    Process:
        1. Discover available plugins
        2. Read enabled list from config
        3. Load only enabled plugins
        4. Log results
    """
    # Discover what's available
    available = self.discover_plugins()

    if not available:
        self.logger.warning("No plugins discovered")
        return {}

    # Get enabled list
    enabled = self.get_enabled_plugins()

    # Load enabled plugins
    results = {}
    for plugin_name in enabled:
        if plugin_name not in available:
            self.logger.warning(
                f"Enabled plugin not found: {plugin_name}",
                extra={"plugin_name": plugin_name, "available": list(available.keys())}
            )
            results[plugin_name] = False
            continue

        module_path = available[plugin_name]
        success = self.load_plugin(plugin_name, module_path)
        results[plugin_name] = success

    # Log summary
    success_count = sum(1 for success in results.values() if success)
    self.logger.info(
        f"Plugin loading complete: {success_count}/{len(results)} successful",
        extra={"results": results}
    )

    return results
```

### Task 5: Test Config Integration

**Create test script**: `test_config_loading.py` (temporary)

```python
"""Test config-based plugin loading"""

from services.plugins import get_plugin_registry, reset_plugin_registry

# Test 1: Default behavior (no config changes)
print("Test 1: Default loading (all plugins)")
reset_plugin_registry()
registry = get_plugin_registry()

results = registry.load_enabled_plugins()
print(f"Loaded {len(results)} plugin(s): {list(results.keys())}")
print(f"Success: {sum(1 for s in results.values() if s)}/{len(results)}")

assert len(results) == 4, "Should load all 4 plugins by default"
print("✅ Test 1 passed\n")

# Test 2: Check config reading
print("Test 2: Config reading")
reset_plugin_registry()
registry = get_plugin_registry()

enabled = registry.get_enabled_plugins()
print(f"Enabled plugins: {enabled}")
print("✅ Test 2 passed\n")

# Test 3: Verify loaded plugins are functional
print("Test 3: Plugin functionality")
reset_plugin_registry()
registry = get_plugin_registry()
registry.load_enabled_plugins()

for name in registry.list_plugins():
    plugin = registry.get_plugin(name)
    metadata = plugin.get_metadata()
    print(f"  - {name}: v{metadata.version}")

print("✅ Test 3 passed\n")

print("✅ All config integration tests passed!")
```

**Run test**:
```bash
cd ~/Development/piper-morgan
PYTHONPATH=. python3 test_config_loading.py
```

### Task 6: Add Unit Tests

**File**: `tests/plugins/test_plugin_registry.py`

**Add test class**:

```python
class TestPluginConfig:
    """Tests for plugin configuration"""

    def test_get_enabled_plugins_default(self, fresh_registry):
        """Test default enables all discovered plugins"""
        enabled = fresh_registry.get_enabled_plugins()

        # Should return all 4 plugins
        assert len(enabled) == 4
        assert "slack" in enabled
        assert "github" in enabled
        assert "notion" in enabled
        assert "calendar" in enabled

    def test_load_enabled_plugins_loads_all_by_default(self, fresh_registry):
        """Test load_enabled_plugins loads all by default"""
        results = fresh_registry.load_enabled_plugins()

        assert len(results) == 4
        assert all(results.values())  # All should succeed
        assert fresh_registry.get_plugin_count() == 4

    def test_load_enabled_plugins_returns_results(self, fresh_registry):
        """Test load_enabled_plugins returns success status"""
        results = fresh_registry.load_enabled_plugins()

        assert isinstance(results, dict)
        for name, success in results.items():
            assert isinstance(name, str)
            assert isinstance(success, bool)
```

**Run new tests**:
```bash
PYTHONPATH=. python3 -m pytest tests/plugins/test_plugin_registry.py::TestPluginConfig -v
```

### Task 7: Verify All Tests Pass

```bash
PYTHONPATH=. python3 -m pytest tests/plugins/ -v
```

**Expected**: 48 tests passing (45 from before + 3 new)

### Task 8: Update Documentation

**File**: `services/plugins/README.md`

**Add section**:

```markdown
## Plugin Configuration

Configure which plugins are enabled in `config/PIPER.user.md`:

```yaml
## Plugin Configuration

```yaml
plugins:
  enabled:
    - github
    - slack
    # - notion  # Disabled
    # - calendar  # Disabled
```

**Loading Enabled Plugins**:

```python
from services.plugins import get_plugin_registry

registry = get_plugin_registry()

# Load only enabled plugins from config
results = registry.load_enabled_plugins()

print(f"Loaded {len(results)} plugins")
for name, success in results.items():
    status = "✅" if success else "❌"
    print(f"{status} {name}")
```

**Default Behavior**:
- If no config section exists: all discovered plugins are loaded
- If config exists with empty enabled list: no plugins are loaded
- Maintains backwards compatibility (everything enabled by default)
```

## Deliverable

Create: `dev/2025/10/03/phase-3-code-config-integration.md`

Include:
1. **Config Section**: Added to PIPER.user.md
2. **Implementation**: Three new methods (read config, get enabled, load enabled)
3. **Test Results**: Output from test_config_loading.py
4. **Unit Tests**: 3 new tests added
5. **Verification**: All 48 tests passing
6. **Documentation**: README updated with config examples

## Success Criteria
- [ ] Plugin config section in PIPER.user.md
- [ ] Config reading implemented
- [ ] `get_enabled_plugins()` working
- [ ] `load_enabled_plugins()` working
- [ ] Default behavior maintains backwards compatibility
- [ ] 3 new unit tests created
- [ ] All tests passing (48 total)
- [ ] Documentation updated

---

**Deploy at 2:58 PM**
**Enables config-controlled plugin loading**
