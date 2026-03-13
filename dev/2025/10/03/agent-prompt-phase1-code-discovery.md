# Claude Code Agent Prompt: GREAT-3B Phase 1 - Discovery System

## Session Log Management
Continue session log: `dev/2025/10/03/2025-10-03-[timestamp]-code-log.md`

Update with timestamped entries for Phase 1 work.

## Mission
**Implement Discovery System**: Add `discover_plugins()` method to PluginRegistry that scans `services/integrations/*/` for plugin files.

## Context

**Phase 0 Complete**: Investigation confirmed
- Auto-registration works with `importlib.import_module()`
- No plugin file modifications needed
- Config will be embedded in `config/PIPER.user.md`
- Discovery via filesystem scanning

**Phase 1 Goal**: Build discovery mechanism that finds available plugins.

## Your Tasks

### Task 1: Implement discover_plugins() Method

**File**: `services/plugins/plugin_registry.py`

**Add method to PluginRegistry class**:

```python
def discover_plugins(self) -> Dict[str, str]:
    """
    Discover available plugins by scanning integrations directory.

    Scans services/integrations/*/ for *_plugin.py files and returns
    a mapping of plugin names to their module paths.

    Returns:
        Dict[str, str]: Map of plugin name to module path
        Example: {
            "slack": "services.integrations.slack.slack_plugin",
            "github": "services.integrations.github.github_plugin"
        }

    Note:
        - Only discovers plugins, does not load them
        - Ignores files that don't match *_plugin.py pattern
        - Returns empty dict if integrations directory not found
    """
    import os
    from pathlib import Path

    plugins = {}
    base_path = Path("services/integrations")

    if not base_path.exists():
        self.logger.warning(f"Integrations directory not found: {base_path}")
        return plugins

    # Scan each subdirectory in integrations
    for integration_dir in base_path.iterdir():
        if not integration_dir.is_dir():
            continue

        # Look for *_plugin.py files
        for plugin_file in integration_dir.glob("*_plugin.py"):
            # Extract plugin name from filename
            # Example: slack_plugin.py -> slack
            plugin_name = plugin_file.stem.replace("_plugin", "")

            # Build module path
            # Example: services.integrations.slack.slack_plugin
            module_path = f"services.integrations.{integration_dir.name}.{plugin_file.stem}"

            plugins[plugin_name] = module_path
            self.logger.debug(
                f"Discovered plugin: {plugin_name} at {module_path}",
                extra={"plugin_name": plugin_name, "module_path": module_path}
            )

    self.logger.info(
        f"Discovery complete: found {len(plugins)} plugin(s)",
        extra={"plugin_count": len(plugins), "plugins": list(plugins.keys())}
    )

    return plugins
```

### Task 2: Test Discovery Method

**Create test script**: `test_discovery.py` (temporary)

```python
"""Test plugin discovery mechanism"""

from services.plugins import get_plugin_registry, reset_plugin_registry

# Reset to clean state
reset_plugin_registry()

# Get registry
registry = get_plugin_registry()

# Test discovery
available = registry.discover_plugins()

print(f"Discovered {len(available)} plugin(s):")
for name, module_path in available.items():
    print(f"  - {name}: {module_path}")

# Expected output:
# Discovered 4 plugin(s):
#   - calendar: services.integrations.calendar.calendar_plugin
#   - github: services.integrations.github.github_plugin
#   - notion: services.integrations.notion.notion_plugin
#   - slack: services.integrations.slack.slack_plugin

assert len(available) == 4, f"Expected 4 plugins, found {len(available)}"
assert "slack" in available, "Slack plugin not found"
assert "github" in available, "GitHub plugin not found"
assert "notion" in available, "Notion plugin not found"
assert "calendar" in available, "Calendar plugin not found"

print("\n✅ Discovery test passed!")
```

**Run test**:
```bash
cd ~/Development/piper-morgan
PYTHONPATH=. python3 test_discovery.py
```

### Task 3: Add Unit Tests

**File**: `tests/plugins/test_plugin_registry.py`

**Add test class**:

```python
class TestPluginDiscovery:
    """Tests for plugin discovery mechanism"""

    def test_discover_plugins_finds_all(self, fresh_registry):
        """Test discovery finds all 4 existing plugins"""
        available = fresh_registry.discover_plugins()

        assert len(available) == 4
        assert "slack" in available
        assert "github" in available
        assert "notion" in available
        assert "calendar" in available

    def test_discover_plugins_returns_dict(self, fresh_registry):
        """Test discovery returns dict of name to module path"""
        available = fresh_registry.discover_plugins()

        assert isinstance(available, dict)
        for name, module_path in available.items():
            assert isinstance(name, str)
            assert isinstance(module_path, str)
            assert "services.integrations" in module_path

    def test_discover_plugins_correct_module_paths(self, fresh_registry):
        """Test discovery returns correct module paths"""
        available = fresh_registry.discover_plugins()

        # Check expected format
        assert available["slack"] == "services.integrations.slack.slack_plugin"
        assert available["github"] == "services.integrations.github.github_plugin"

    def test_discover_plugins_empty_when_no_integrations(self, fresh_registry, tmp_path, monkeypatch):
        """Test discovery returns empty dict when integrations dir missing"""
        # Temporarily change base path to non-existent directory
        monkeypatch.setattr("pathlib.Path", lambda x: tmp_path / "nonexistent" if x == "services/integrations" else tmp_path)

        available = fresh_registry.discover_plugins()

        assert available == {}

    def test_discover_plugins_logs_results(self, fresh_registry, caplog):
        """Test discovery logs what it finds"""
        import logging
        caplog.set_level(logging.INFO)

        available = fresh_registry.discover_plugins()

        assert "Discovery complete" in caplog.text
        assert f"found {len(available)} plugin(s)" in caplog.text
```

**Run new tests**:
```bash
cd ~/Development/piper-morgan
PYTHONPATH=. python3 -m pytest tests/plugins/test_plugin_registry.py::TestPluginDiscovery -v
```

### Task 4: Verify No Breaking Changes

**Check existing tests still pass**:
```bash
PYTHONPATH=. python3 -m pytest tests/plugins/ -v
```

**Expected**: All 34 original tests + 5 new tests = 39 tests passing

### Task 5: Update PluginRegistry __init__.py

**File**: `services/plugins/__init__.py`

Make sure `discover_plugins` is accessible if needed (registry methods are accessed via instance, so no changes needed here - just verify).

### Task 6: Document Discovery Method

**File**: `services/plugins/README.md`

**Add section**:

```markdown
## Plugin Discovery

The plugin system automatically discovers available plugins by scanning the integrations directory:

```python
from services.plugins import get_plugin_registry

registry = get_plugin_registry()

# Discover what's available
available = registry.discover_plugins()
print(f"Found {len(available)} plugins: {list(available.keys())}")
```

Discovery scans `services/integrations/*/` for `*_plugin.py` files and returns a mapping of plugin names to module paths.

**Discovery does not load plugins** - it only identifies what's available. Use `load_plugin()` or `load_enabled_plugins()` to actually import and register plugins.
```

## Deliverable

Create: `dev/2025/10/03/phase-1-code-discovery.md`

Include:
1. **Implementation**: Complete `discover_plugins()` method
2. **Test Results**: Output from test_discovery.py
3. **Unit Tests**: 5 new tests added
4. **Verification**: All 39 tests passing
5. **Documentation**: README updated

## Success Criteria
- [ ] `discover_plugins()` method implemented
- [ ] Finds all 4 existing plugins correctly
- [ ] Returns dict of name → module path
- [ ] 5 new unit tests created
- [ ] All tests passing (39 total)
- [ ] Documentation updated
- [ ] No breaking changes

## Time Estimate
45 minutes

---

**Deploy at 2:20 PM**
**Foundation for Phase 2 dynamic loading**
