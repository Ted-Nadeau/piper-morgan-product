# Cursor Agent Prompt: GREAT-3D Phase 2 - Contract Test Implementation

## Session Log Management
Continue session log: `dev/2025/10/04/2025-10-04-[timestamp]-cursor-log.md`

Update with timestamped entries for Phase 2 work.

## Mission
**Implement Contract Tests**: Fill in all 75 TODO test stubs with actual test implementation to verify ALL plugins comply with PiperPlugin interface contracts.

## Context

**Phase 1 Complete**: Code agent created contract test framework
- 6 files in tests/plugins/contract/
- 76 tests collected (19 methods × 4 plugins)
- 1 test implemented, 75 marked TODO
- Auto-parametrization working

**Phase 2 Goal**: Implement all contract tests to validate plugin compliance.

## CRITICAL: File Placement Rules

```
✅ Modify files in tests/plugins/contract/
✅ Working files → dev/2025/10/04/
❌ NEVER create files in root without PM permission
```

## Your Tasks

### Task 1: Implement Interface Contract Tests

**File**: `tests/plugins/contract/test_plugin_interface_contract.py`

Replace TODO markers with implementations:

```python
def test_get_metadata_returns_metadata(self, plugin_instance):
    """get_metadata() must return PluginMetadata instance"""
    metadata = plugin_instance.get_metadata()
    assert isinstance(metadata, PluginMetadata), \
        f"get_metadata() must return PluginMetadata, got {type(metadata)}"

def test_metadata_has_required_fields(self, plugin_instance):
    """Metadata must have all required fields populated"""
    metadata = plugin_instance.get_metadata()

    # Required fields must be non-empty strings
    assert metadata.name, "Metadata must have non-empty name"
    assert metadata.version, "Metadata must have non-empty version"
    assert metadata.description, "Metadata must have non-empty description"
    assert metadata.author, "Metadata must have non-empty author"

    # Capabilities must be a list (can be empty)
    assert isinstance(metadata.capabilities, list), \
        f"Capabilities must be list, got {type(metadata.capabilities)}"

def test_metadata_version_format(self, plugin_instance):
    """Version should follow semantic versioning (X.Y.Z)"""
    metadata = plugin_instance.get_metadata()
    version = metadata.version

    # Check semver format (simple check for X.Y.Z)
    parts = version.split('.')
    assert len(parts) == 3, \
        f"Version should be X.Y.Z format, got {version}"

    # Each part should be numeric
    for part in parts:
        assert part.isdigit(), \
            f"Version parts should be numeric, got {version}"

def test_get_router_returns_router(self, plugin_instance):
    """get_router() must return APIRouter instance"""
    router = plugin_instance.get_router()
    assert isinstance(router, APIRouter), \
        f"get_router() must return APIRouter, got {type(router)}"

def test_router_has_prefix(self, plugin_instance):
    """Router must have a prefix defined"""
    router = plugin_instance.get_router()
    assert router.prefix, \
        "Router must have non-empty prefix"
    assert router.prefix.startswith("/"), \
        f"Router prefix must start with '/', got {router.prefix}"

def test_router_has_routes(self, plugin_instance):
    """Router must define at least one route"""
    router = plugin_instance.get_router()
    assert len(router.routes) > 0, \
        "Router must have at least one route defined"

def test_is_configured_returns_bool(self, plugin_instance):
    """is_configured() must return boolean"""
    result = plugin_instance.is_configured()
    assert isinstance(result, bool), \
        f"is_configured() must return bool, got {type(result)}"

def test_get_status_returns_dict(self, plugin_instance):
    """get_status() must return dictionary"""
    status = plugin_instance.get_status()
    assert isinstance(status, dict), \
        f"get_status() must return dict, got {type(status)}"

def test_status_has_configured_field(self, plugin_instance):
    """Status dict should include 'configured' field"""
    status = plugin_instance.get_status()
    assert "configured" in status, \
        "Status dict must include 'configured' field"
    assert isinstance(status["configured"], bool), \
        "Status 'configured' field must be boolean"
```

### Task 2: Implement Lifecycle Contract Tests

**File**: `tests/plugins/contract/test_lifecycle_contract.py`

Implement all lifecycle tests:

```python
@pytest.mark.asyncio
async def test_initialize_is_async(self, plugin_instance):
    """initialize() must be async method"""
    import inspect
    assert inspect.iscoroutinefunction(plugin_instance.initialize), \
        "initialize() must be async method"

@pytest.mark.asyncio
async def test_initialize_is_idempotent(self, plugin_instance):
    """initialize() can be called multiple times safely"""
    # First call
    await plugin_instance.initialize()

    # Second call should not raise error
    try:
        await plugin_instance.initialize()
    except Exception as e:
        pytest.fail(f"initialize() should be idempotent, raised: {e}")

@pytest.mark.asyncio
async def test_shutdown_is_async(self, plugin_instance):
    """shutdown() must be async method"""
    import inspect
    assert inspect.iscoroutinefunction(plugin_instance.shutdown), \
        "shutdown() must be async method"

@pytest.mark.asyncio
async def test_shutdown_is_idempotent(self, plugin_instance):
    """shutdown() can be called multiple times safely"""
    # Initialize first
    await plugin_instance.initialize()

    # First shutdown
    await plugin_instance.shutdown()

    # Second shutdown should not raise error
    try:
        await plugin_instance.shutdown()
    except Exception as e:
        pytest.fail(f"shutdown() should be idempotent, raised: {e}")

@pytest.mark.asyncio
async def test_lifecycle_order(self, plugin_instance):
    """Plugins must support initialize -> use -> shutdown lifecycle"""
    # Initialize
    await plugin_instance.initialize()

    # Use plugin (get status)
    status = plugin_instance.get_status()
    assert status is not None

    # Shutdown
    await plugin_instance.shutdown()

    # Should still be able to get status after shutdown
    # (plugin object still valid, just resources cleaned up)
    status_after = plugin_instance.get_status()
    assert status_after is not None
```

### Task 3: Implement Configuration Contract Tests

**File**: `tests/plugins/contract/test_configuration_contract.py`

Implement configuration tests:

```python
import time

def test_is_configured_is_fast(self, plugin_instance):
    """is_configured() should be fast (no I/O)"""
    # Measure time for 100 calls
    start = time.perf_counter()
    for _ in range(100):
        plugin_instance.is_configured()
    elapsed = time.perf_counter() - start

    # Should complete 100 calls in < 100ms (< 1ms per call)
    assert elapsed < 0.1, \
        f"is_configured() too slow: {elapsed*1000:.2f}ms for 100 calls"

def test_configuration_status_consistency(self, plugin_instance):
    """is_configured() and get_status() should be consistent"""
    is_configured = plugin_instance.is_configured()
    status = plugin_instance.get_status()

    assert "configured" in status, \
        "Status must include 'configured' field"
    assert status["configured"] == is_configured, \
        "is_configured() and status['configured'] must match"

def test_status_includes_router_info(self, plugin_instance):
    """get_status() should include router information"""
    status = plugin_instance.get_status()

    # Status should include some router information
    # (exact field names may vary, but should have something about router)
    router_fields = ["router_prefix", "router", "routes", "prefix"]
    has_router_info = any(field in status for field in router_fields)

    assert has_router_info, \
        f"Status should include router info, got fields: {list(status.keys())}"

def test_router_available_when_configured(self, plugin_instance):
    """Router should be available regardless of configuration status"""
    # Even if not configured, router should be available
    # (it just might return error responses)
    router = plugin_instance.get_router()
    assert router is not None, \
        "Router should always be available"
```

### Task 4: Implement Isolation Contract Tests

**File**: `tests/plugins/contract/test_isolation_contract.py`

Implement isolation tests:

```python
import sys
import importlib

def test_plugin_module_structure(self, plugin_instance):
    """Plugin should be in services/integrations/[name]/ structure"""
    metadata = plugin_instance.get_metadata()
    plugin_name = metadata.name

    # Plugin module should exist
    module_name = f"services.integrations.{plugin_name}"
    assert module_name in sys.modules, \
        f"Plugin module {module_name} should be loaded"

def test_plugin_has_no_circular_imports(self, plugin_instance):
    """Plugin should not create circular import issues"""
    metadata = plugin_instance.get_metadata()
    plugin_name = metadata.name

    # Try to reload plugin module (would fail with circular imports)
    try:
        module_name = f"services.integrations.{plugin_name}.{plugin_name}_plugin"
        if module_name in sys.modules:
            importlib.reload(sys.modules[module_name])
    except ImportError as e:
        pytest.fail(f"Plugin has import issues: {e}")

def test_plugin_auto_registration(self, plugin_instance):
    """Plugin should auto-register via registry pattern"""
    from services.plugins import get_plugin_registry

    metadata = plugin_instance.get_metadata()
    plugin_name = metadata.name

    # Plugin should be in registry
    registry = get_plugin_registry()
    assert plugin_name in registry.list_plugins(), \
        f"Plugin {plugin_name} should be auto-registered"

def test_plugin_independence(self, plugin_instance):
    """Each plugin should be independently importable"""
    metadata = plugin_instance.get_metadata()
    plugin_name = metadata.name

    # Should be able to get plugin without loading others
    from services.plugins import get_plugin_registry
    registry = get_plugin_registry()

    plugin = registry.get_plugin(plugin_name)
    assert plugin is not None, \
        f"Plugin {plugin_name} should be independently accessible"
```

### Task 5: Run Contract Tests

```bash
cd ~/Development/piper-morgan

# Run contract tests only
PYTHONPATH=. pytest tests/plugins/contract/ -v -m contract

# Expected: All tests passing (76 tests)
```

### Task 6: Verify Test Coverage

```bash
# Run with coverage
PYTHONPATH=. pytest tests/plugins/contract/ --cov=services.plugins --cov-report=term-missing

# Should show good coverage of plugin interface
```

### Task 7: Test Against All Plugins

Verify tests run against all 4 enabled plugins:

```bash
# Should see tests for each plugin
PYTHONPATH=. pytest tests/plugins/contract/ -v | grep "plugin="

# Expected output includes:
# test_...[plugin=github]
# test_...[plugin=slack]
# test_...[plugin=notion]
# test_...[plugin=calendar]
```

## Deliverable

Create: `dev/2025/10/04/phase-2-cursor-contract-implementation.md`

Include:
1. **Tests Implemented**: All 75 TODO markers replaced
2. **Test Results**: Full test run output
3. **Coverage Report**: Coverage percentages
4. **Plugin Verification**: Tests ran for all 4 plugins
5. **Any Failures**: Document and explain any test failures

## Success Criteria
- [ ] All 75 TODO markers implemented
- [ ] All contract tests passing (76/76)
- [ ] Tests run for all 4 plugins (github, slack, notion, calendar)
- [ ] Coverage report shows good interface coverage
- [ ] No test skips or xfails
- [ ] All assertions meaningful and specific

## Notes

**If any tests fail**:
1. Document the failure clearly
2. Determine if it's a test issue or plugin issue
3. If plugin issue, note for fixing but don't block
4. If test issue, fix the test

**Test Quality**:
- Clear assertion messages
- Specific error messages
- Test one thing per test
- Meaningful test names

---

**Deploy at 5:15 PM**
**Natural Stop Point 1 available after this phase**
