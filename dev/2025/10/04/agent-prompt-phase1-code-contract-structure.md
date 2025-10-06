# Claude Code Agent Prompt: GREAT-3D Phase 1 - Contract Test Structure

## Session Log Management
Continue session log: `dev/2025/10/04/2025-10-04-[timestamp]-code-log.md`

Update with timestamped entries for Phase 1 work.

## Mission
**Create Contract Test Framework**: Build directory structure, fixtures, and test file stubs for comprehensive contract testing of all plugins.

## Context

**Phase 0 Complete**: Investigation identified critical gaps
- No contract tests verifying ALL plugins implement interface
- Need parametrized approach for better debugging
- Target: 4 contract test files covering all aspects

**Phase 1 Goal**: Create infrastructure for contract testing.

## CRITICAL: File Placement Rules

```
✅ Contract tests → tests/plugins/contract/
✅ Working files → dev/2025/10/04/
❌ NEVER create files in root without PM permission
```

## Your Tasks

### Task 1: Create Contract Test Directory Structure

```bash
cd ~/Development/piper-morgan

# Create contract test directory
mkdir -p tests/plugins/contract

# Create __init__.py
touch tests/plugins/contract/__init__.py
```

### Task 2: Create Contract Fixtures

**File**: `tests/plugins/contract/conftest.py`

```python
"""Fixtures for contract testing all plugins

These fixtures provide automatic plugin discovery and parametrization
for testing that ALL plugins comply with the PiperPlugin interface.
"""

import pytest
from services.plugins import get_plugin_registry, reset_plugin_registry


@pytest.fixture(scope="session")
def contract_registry():
    """Session-scoped plugin registry for contract tests

    Loads all enabled plugins once per test session for efficiency.
    """
    reset_plugin_registry()
    registry = get_plugin_registry()
    registry.load_enabled_plugins()
    return registry


@pytest.fixture(scope="session")
def all_plugin_names(contract_registry):
    """List of all registered plugin names

    Returns:
        List[str]: Names of all plugins in the registry
    """
    return contract_registry.list_plugins()


@pytest.fixture
def plugin_instance(request, contract_registry):
    """Get a specific plugin instance by name

    Used with parametrize to test each plugin individually.

    Args:
        request: pytest request with plugin name as param
        contract_registry: The session-scoped registry

    Returns:
        PiperPlugin: The requested plugin instance
    """
    plugin_name = request.param
    return contract_registry.get_plugin(plugin_name)


def pytest_generate_tests(metafunc):
    """Auto-parametrize tests that use plugin_instance fixture

    This hook automatically parametrizes any test using the plugin_instance
    fixture to run against all registered plugins.

    Example:
        def test_something(plugin_instance):
            # This will run once for each plugin automatically
            assert plugin_instance is not None
    """
    if "plugin_instance" in metafunc.fixturenames:
        # Get all plugin names for parametrization
        registry = get_plugin_registry()
        reset_plugin_registry()
        registry = get_plugin_registry()
        registry.load_enabled_plugins()
        plugin_names = registry.list_plugins()

        # Parametrize the test with all plugin names
        metafunc.parametrize(
            "plugin_instance",
            plugin_names,
            indirect=True,
            ids=lambda name: f"plugin={name}"
        )
```

### Task 3: Create Interface Contract Test Stub

**File**: `tests/plugins/contract/test_plugin_interface_contract.py`

```python
"""Contract tests for PiperPlugin interface compliance

These tests verify that ALL plugins correctly implement the PiperPlugin
interface. Each test is automatically run against every registered plugin.
"""

import pytest
from services.plugins.plugin_interface import PiperPlugin, PluginMetadata
from fastapi import APIRouter
from typing import Dict, Any


@pytest.mark.contract
class TestPluginInterfaceContract:
    """Verify all plugins implement PiperPlugin interface correctly"""

    def test_plugin_implements_interface(self, plugin_instance):
        """Every plugin must be instance of PiperPlugin"""
        assert isinstance(plugin_instance, PiperPlugin), \
            f"Plugin {plugin_instance} does not implement PiperPlugin"

    def test_get_metadata_returns_metadata(self, plugin_instance):
        """get_metadata() must return PluginMetadata instance"""
        # TODO: Implement in Phase 2
        pass

    def test_metadata_has_required_fields(self, plugin_instance):
        """Metadata must have all required fields populated"""
        # TODO: Implement in Phase 2
        pass

    def test_get_router_returns_router(self, plugin_instance):
        """get_router() must return APIRouter instance"""
        # TODO: Implement in Phase 2
        pass

    def test_router_has_prefix(self, plugin_instance):
        """Router must have a prefix defined"""
        # TODO: Implement in Phase 2
        pass

    def test_is_configured_returns_bool(self, plugin_instance):
        """is_configured() must return boolean"""
        # TODO: Implement in Phase 2
        pass

    def test_get_status_returns_dict(self, plugin_instance):
        """get_status() must return dictionary"""
        # TODO: Implement in Phase 2
        pass
```

### Task 4: Create Lifecycle Contract Test Stub

**File**: `tests/plugins/contract/test_lifecycle_contract.py`

```python
"""Contract tests for plugin lifecycle methods

Verifies that initialize() and shutdown() work correctly and can be
called multiple times safely (idempotency).
"""

import pytest


@pytest.mark.contract
class TestLifecycleContract:
    """Verify plugin lifecycle methods work correctly"""

    @pytest.mark.asyncio
    async def test_initialize_is_async(self, plugin_instance):
        """initialize() must be async method"""
        # TODO: Implement in Phase 2
        pass

    @pytest.mark.asyncio
    async def test_initialize_is_idempotent(self, plugin_instance):
        """initialize() can be called multiple times safely"""
        # TODO: Implement in Phase 2
        pass

    @pytest.mark.asyncio
    async def test_shutdown_is_async(self, plugin_instance):
        """shutdown() must be async method"""
        # TODO: Implement in Phase 2
        pass

    @pytest.mark.asyncio
    async def test_shutdown_is_idempotent(self, plugin_instance):
        """shutdown() can be called multiple times safely"""
        # TODO: Implement in Phase 2
        pass

    @pytest.mark.asyncio
    async def test_lifecycle_order(self, plugin_instance):
        """Plugins must support initialize -> use -> shutdown lifecycle"""
        # TODO: Implement in Phase 2
        pass
```

### Task 5: Create Configuration Contract Test Stub

**File**: `tests/plugins/contract/test_configuration_contract.py`

```python
"""Contract tests for plugin configuration

Verifies that plugins handle configuration correctly and provide
appropriate status information.
"""

import pytest


@pytest.mark.contract
class TestConfigurationContract:
    """Verify plugin configuration contracts"""

    def test_is_configured_is_fast(self, plugin_instance):
        """is_configured() should be fast (no I/O)"""
        # TODO: Implement in Phase 2
        pass

    def test_unconfigured_plugin_behavior(self, plugin_instance):
        """Unconfigured plugins should indicate status clearly"""
        # TODO: Implement in Phase 2
        pass

    def test_status_includes_configuration(self, plugin_instance):
        """get_status() should include configuration status"""
        # TODO: Implement in Phase 2
        pass

    def test_router_availability(self, plugin_instance):
        """Router should be available when plugin is configured"""
        # TODO: Implement in Phase 2
        pass
```

### Task 6: Create Isolation Contract Test Stub

**File**: `tests/plugins/contract/test_isolation_contract.py`

```python
"""Contract tests for plugin isolation

Verifies that plugins maintain proper isolation from core system
and don't create unwanted dependencies.
"""

import pytest
import importlib
import sys


@pytest.mark.contract
class TestIsolationContract:
    """Verify plugins maintain proper isolation"""

    def test_plugin_no_direct_core_imports(self, plugin_instance):
        """Plugins should not directly import core modules"""
        # TODO: Implement in Phase 2
        pass

    def test_plugin_uses_registry_pattern(self, plugin_instance):
        """Plugins should auto-register via registry pattern"""
        # TODO: Implement in Phase 2
        pass

    def test_plugin_module_isolation(self, plugin_instance):
        """Plugin modules should be properly isolated"""
        # TODO: Implement in Phase 2
        pass
```

### Task 7: Update pytest Configuration

**File**: `pytest.ini`

Add contract marker to existing markers:

```ini
markers =
    smoke: Critical path tests that should run in <5 seconds total
    unit: Unit tests that should run in <30 seconds total
    integration: Integration tests that may take up to 2 minutes
    performance: Performance tests (slow, run separately)
    benchmark: Benchmark tests
    contract: Contract tests verifying plugin interface compliance
```

### Task 8: Create Test Validation Script

**File**: `dev/2025/10/04/validate_contract_tests.py`

```python
"""Validate contract test structure is correct"""

import os
import sys

def check_contract_structure():
    """Verify all contract test files exist"""

    base = "tests/plugins/contract"
    required_files = [
        "__init__.py",
        "conftest.py",
        "test_plugin_interface_contract.py",
        "test_lifecycle_contract.py",
        "test_configuration_contract.py",
        "test_isolation_contract.py"
    ]

    missing = []
    for file in required_files:
        path = os.path.join(base, file)
        if not os.path.exists(path):
            missing.append(path)

    if missing:
        print(f"❌ Missing files: {missing}")
        return False

    print("✅ All contract test files exist")
    return True

def check_pytest_markers():
    """Verify pytest.ini has contract marker"""

    with open("pytest.ini", "r") as f:
        content = f.read()

    if "contract:" in content:
        print("✅ Contract marker added to pytest.ini")
        return True
    else:
        print("❌ Contract marker missing from pytest.ini")
        return False

if __name__ == "__main__":
    os.chdir("/Users/xian/Development/piper-morgan")

    structure_ok = check_contract_structure()
    markers_ok = check_pytest_markers()

    if structure_ok and markers_ok:
        print("\n✅ Contract test structure validated!")
        sys.exit(0)
    else:
        print("\n❌ Validation failed")
        sys.exit(1)
```

Run validation:
```bash
cd ~/Development/piper-morgan
python3 dev/2025/10/04/validate_contract_tests.py
```

### Task 9: Test Contract Test Discovery

```bash
# Discover contract tests (should find stub tests)
pytest tests/plugins/contract/ --collect-only

# Should show something like:
# <Module test_plugin_interface_contract.py>
#   <Class TestPluginInterfaceContract>
#     <Function test_plugin_implements_interface[plugin=slack]>
#     <Function test_plugin_implements_interface[plugin=github]>
#     ...
```

## Deliverable

Create: `dev/2025/10/04/phase-1-code-contract-structure.md`

Include:
1. **Directory Structure**: Files created and organized
2. **Fixtures Created**: conftest.py with auto-parametrization
3. **Test Stubs**: 4 contract test files with TODO markers
4. **pytest Configuration**: Contract marker added
5. **Validation Results**: Structure verified
6. **Discovery Test**: pytest can discover contract tests
7. **Ready for Phase 2**: Cursor can implement test bodies

## Success Criteria
- [ ] tests/plugins/contract/ directory created
- [ ] conftest.py with fixtures and parametrization hook
- [ ] 4 contract test stub files created
- [ ] pytest.ini updated with contract marker
- [ ] Validation script confirms structure
- [ ] pytest can discover contract tests
- [ ] All files in correct locations (not root)

---

**Deploy at 5:20 PM**
**Phase 1 creates infrastructure for Phase 2 implementation**
