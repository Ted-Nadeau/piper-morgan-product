# Cursor Agent Prompt: GREAT-3B Phase 2 - Dynamic Loading

## Session Log Management
Continue session log: `dev/2025/10/03/2025-10-03-[timestamp]-cursor-log.md`

Update with timestamped entries for Phase 2 work.

## Mission
**Implement Dynamic Loading**: Add `load_plugin()` method to PluginRegistry that dynamically imports and registers plugins using importlib.

## Context

**Phase 1 Complete**: Discovery system working
- `discover_plugins()` returns dict: `{name: module_path}`
- Finds all 4 existing plugins correctly
- 39 tests passing

**Phase 2 Goal**: Build dynamic loading that imports plugins on-demand without static imports.

## Your Tasks

### Task 1: Implement load_plugin() Method

**File**: `services/plugins/plugin_registry.py`

**Add method to PluginRegistry class**:

```python
def load_plugin(self, name: str, module_path: str) -> bool:
    """
    Dynamically load and register a plugin.

    Uses importlib to import the plugin module, which triggers
    auto-registration via the module's _plugin instance.

    Args:
        name: Plugin name (e.g., "slack")
        module_path: Full module path (e.g., "services.integrations.slack.slack_plugin")

    Returns:
        bool: True if loaded successfully, False otherwise

    Note:
        - Import triggers auto-registration (plugin registers itself)
        - Plugin must already be registered after import
        - Handles import errors gracefully
    """
    import importlib

    try:
        self.logger.info(
            f"Loading plugin: {name}",
            extra={"plugin_name": name, "module_path": module_path}
        )

        # Import the module - this triggers auto-registration
        module = importlib.import_module(module_path)

        # Verify plugin was registered
        if name not in self._plugins:
            self.logger.error(
                f"Plugin {name} failed to register after import",
                extra={"plugin_name": name, "module_path": module_path}
            )
            return False

        self.logger.info(
            f"Successfully loaded plugin: {name}",
            extra={"plugin_name": name}
        )
        return True

    except ImportError as e:
        self.logger.error(
            f"Failed to import plugin {name}: {e}",
            extra={"plugin_name": name, "module_path": module_path, "error": str(e)}
        )
        return False
    except Exception as e:
        self.logger.error(
            f"Unexpected error loading plugin {name}: {e}",
            extra={"plugin_name": name, "module_path": module_path, "error": str(e)}
        )
        return False
```

### Task 2: Test Dynamic Loading

**Create test script**: `test_dynamic_loading.py` (temporary)

```python
"""Test dynamic plugin loading"""

from services.plugins import get_plugin_registry, reset_plugin_registry

# Reset to clean state
reset_plugin_registry()
registry = get_plugin_registry()

# Discover available plugins
available = registry.discover_plugins()
print(f"Discovered {len(available)} plugin(s): {list(available.keys())}")

# Test loading each plugin dynamically
print("\nTesting dynamic loading:")
for name, module_path in available.items():
    success = registry.load_plugin(name, module_path)
    status = "✅" if success else "❌"
    print(f"  {status} {name}: {'Loaded' if success else 'Failed'}")

# Verify all plugins registered
registered = registry.list_plugins()
print(f"\nRegistered plugins: {registered}")
assert len(registered) == 4, f"Expected 4 plugins registered, got {len(registered)}"

# Verify plugins are functional
print("\nVerifying plugin functionality:")
for name in registered:
    plugin = registry.get_plugin(name)
    metadata = plugin.get_metadata()
    print(f"  - {name}: v{metadata.version} - {metadata.capabilities}")

print("\n✅ Dynamic loading test passed!")
```

**Run test**:
```bash
cd ~/Development/piper-morgan
PYTHONPATH=. python3 test_dynamic_loading.py
```

### Task 3: Add Unit Tests

**File**: `tests/plugins/test_plugin_registry.py`

**Add test class**:

```python
class TestPluginLoading:
    """Tests for dynamic plugin loading"""

    def test_load_plugin_success(self, fresh_registry):
        """Test loading a valid plugin"""
        # Discover plugins first
        available = fresh_registry.discover_plugins()

        # Load slack plugin
        success = fresh_registry.load_plugin("slack", available["slack"])

        assert success is True
        assert "slack" in fresh_registry.list_plugins()

    def test_load_plugin_registers_automatically(self, fresh_registry):
        """Test that loading triggers auto-registration"""
        available = fresh_registry.discover_plugins()

        # Registry should be empty before loading
        assert fresh_registry.get_plugin_count() == 0

        # Load plugin
        fresh_registry.load_plugin("github", available["github"])

        # Plugin should now be registered
        assert fresh_registry.get_plugin_count() == 1
        assert fresh_registry.get_plugin("github") is not None

    def test_load_multiple_plugins(self, fresh_registry):
        """Test loading multiple plugins"""
        available = fresh_registry.discover_plugins()

        # Load all plugins
        results = {}
        for name, module_path in available.items():
            results[name] = fresh_registry.load_plugin(name, module_path)

        # All should succeed
        assert all(results.values())
        assert fresh_registry.get_plugin_count() == 4

    def test_load_plugin_invalid_module(self, fresh_registry):
        """Test loading with invalid module path"""
        success = fresh_registry.load_plugin("fake", "services.integrations.fake.fake_plugin")

        assert success is False
        assert "fake" not in fresh_registry.list_plugins()

    def test_load_plugin_already_loaded(self, fresh_registry):
        """Test loading same plugin twice"""
        available = fresh_registry.discover_plugins()

        # Load once
        success1 = fresh_registry.load_plugin("notion", available["notion"])
        count1 = fresh_registry.get_plugin_count()

        # Load again
        success2 = fresh_registry.load_plugin("notion", available["notion"])
        count2 = fresh_registry.get_plugin_count()

        # Both should succeed, count shouldn't increase
        assert success1 is True
        assert success2 is True
        assert count1 == count2  # No duplicate registration

    def test_load_plugin_logs_errors(self, fresh_registry, caplog):
        """Test that load failures are logged"""
        import logging
        caplog.set_level(logging.ERROR)

        fresh_registry.load_plugin("invalid", "invalid.module.path")

        assert "Failed to import plugin" in caplog.text
```

**Run new tests**:
```bash
cd ~/Development/piper-morgan
PYTHONPATH=. python3 -m pytest tests/plugins/test_plugin_registry.py::TestPluginLoading -v
```

### Task 4: Verify No Breaking Changes

**Check all tests still pass**:
```bash
PYTHONPATH=. python3 -m pytest tests/plugins/ -v
```

**Expected**: All 39 original tests + 6 new tests = 45 tests passing

### Task 5: Update Documentation

**File**: `services/plugins/README.md`

**Add section after Plugin Discovery**:

```markdown
## Dynamic Plugin Loading

Plugins can be loaded dynamically without static imports:

```python
from services.plugins import get_plugin_registry

registry = get_plugin_registry()

# Discover available plugins
available = registry.discover_plugins()

# Load specific plugin
success = registry.load_plugin("slack", available["slack"])
if success:
    print("Slack plugin loaded!")

# Load all discovered plugins
for name, module_path in available.items():
    registry.load_plugin(name, module_path)
```

**Loading Process**:
1. Plugin module is imported using `importlib`
2. Import triggers auto-registration (plugin's `_plugin` instance registers itself)
3. Plugin is immediately available via `get_plugin(name)`

**Error Handling**:
- Import errors are caught and logged
- Failed loads return `False`
- Existing plugins are not affected by failed loads
- Safe to attempt loading invalid plugins
```

## Deliverable

Create: `dev/2025/10/03/phase-2-cursor-dynamic-loading.md`

Include:
1. **Implementation**: Complete `load_plugin()` method
2. **Test Results**: Output from test_dynamic_loading.py
3. **Unit Tests**: 6 new tests added
4. **Verification**: All 45 tests passing
5. **Documentation**: README updated

## Success Criteria
- [ ] `load_plugin()` method implemented
- [ ] Loads all 4 existing plugins successfully
- [ ] Auto-registration triggered by import
- [ ] 6 new unit tests created
- [ ] All tests passing (45 total)
- [ ] Error handling for invalid modules
- [ ] Documentation updated
- [ ] No breaking changes

## Time Estimate
45 minutes

---

**Deploy at 2:45 PM**
**Foundation for Phase 3 config integration**
