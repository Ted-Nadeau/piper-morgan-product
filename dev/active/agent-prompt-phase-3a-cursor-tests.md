# Cursor Agent Prompt: GREAT-3A Phase 3A - Plugin Interface Test Suite

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase 3A work.

## Mission
**Create Plugin Test Suite**: Build comprehensive tests to validate plugin interface compliance for all current and future plugins.

## Context

**Phase 3A In Progress**: Code agent defining PiperPlugin interface
**Your Task**: Create test infrastructure to validate plugins implement interface correctly

**Why This Matters**:
- Phase 3C will create 4 plugin wrappers (Slack, Notion, GitHub, Calendar)
- Need automated way to verify each plugin implements interface correctly
- Tests catch missing methods, wrong signatures, invalid metadata
- Reusable for future plugin development

## Your Tasks

### Task 1: Create Test Directory Structure

```bash
cd ~/Development/piper-morgan

# Create directory
mkdir -p tests/plugins

# Create files
touch tests/plugins/__init__.py
touch tests/plugins/test_plugin_interface.py
touch tests/plugins/conftest.py

# Verify
ls -la tests/plugins/
```

### Task 2: Create Test Fixtures

**File**: `tests/plugins/conftest.py`

**Purpose**: Pytest fixtures for plugin testing

```python
"""
Pytest fixtures for plugin interface testing
"""

import pytest
from typing import Optional, Dict, Any
from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata


@pytest.fixture
def sample_metadata():
    """Sample plugin metadata for testing"""
    return PluginMetadata(
        name="test_plugin",
        version="1.0.0",
        description="Test plugin for validation",
        author="Test Author",
        capabilities=["routes", "webhooks"],
        dependencies=["other_plugin"]
    )


@pytest.fixture
def minimal_plugin():
    """Minimal valid plugin implementation"""
    class MinimalPlugin(PiperPlugin):
        def get_metadata(self) -> PluginMetadata:
            return PluginMetadata(
                name="minimal",
                version="1.0.0",
                description="Minimal test plugin",
                author="Test",
                capabilities=[],
                dependencies=[]
            )

        def get_router(self) -> Optional[APIRouter]:
            return None

        def is_configured(self) -> bool:
            return True

        async def initialize(self) -> None:
            pass

        async def shutdown(self) -> None:
            pass

        def get_status(self) -> Dict[str, Any]:
            return {"status": "ok"}

    return MinimalPlugin()


@pytest.fixture
def plugin_with_router():
    """Plugin with router implementation"""
    class RouterPlugin(PiperPlugin):
        def __init__(self):
            self._router = APIRouter(prefix="/api/v1/test")

            @self._router.get("/health")
            async def health():
                return {"status": "healthy"}

        def get_metadata(self) -> PluginMetadata:
            return PluginMetadata(
                name="router_plugin",
                version="1.0.0",
                description="Plugin with routes",
                author="Test",
                capabilities=["routes"],
                dependencies=[]
            )

        def get_router(self) -> Optional[APIRouter]:
            return self._router

        def is_configured(self) -> bool:
            return True

        async def initialize(self) -> None:
            pass

        async def shutdown(self) -> None:
            pass

        def get_status(self) -> Dict[str, Any]:
            return {"router": "active"}

    return RouterPlugin()
```

### Task 3: Create Interface Compliance Tests

**File**: `tests/plugins/test_plugin_interface.py`

```python
"""
Plugin Interface Compliance Tests

Tests to verify plugins correctly implement PiperPlugin interface.
"""

import pytest
from typing import get_type_hints
from inspect import signature
from fastapi import APIRouter

from services.plugins import PiperPlugin, PluginMetadata


class TestPluginMetadata:
    """Tests for PluginMetadata dataclass"""

    def test_metadata_creation(self, sample_metadata):
        """Test PluginMetadata can be created"""
        assert sample_metadata.name == "test_plugin"
        assert sample_metadata.version == "1.0.0"
        assert sample_metadata.description == "Test plugin for validation"
        assert sample_metadata.author == "Test Author"

    def test_metadata_capabilities(self, sample_metadata):
        """Test capabilities list"""
        assert "routes" in sample_metadata.capabilities
        assert "webhooks" in sample_metadata.capabilities

    def test_metadata_dependencies(self, sample_metadata):
        """Test dependencies list"""
        assert "other_plugin" in sample_metadata.dependencies

    def test_metadata_defaults(self):
        """Test PluginMetadata with default values"""
        metadata = PluginMetadata(
            name="simple",
            version="1.0.0",
            description="Simple plugin",
            author="Author"
        )
        assert metadata.capabilities == []
        assert metadata.dependencies == []


class TestPiperPluginInterface:
    """Tests for PiperPlugin ABC"""

    def test_cannot_instantiate_abstract_class(self):
        """Test PiperPlugin cannot be instantiated directly"""
        with pytest.raises(TypeError):
            PiperPlugin()

    def test_minimal_plugin_implements_interface(self, minimal_plugin):
        """Test minimal plugin implements all required methods"""
        assert isinstance(minimal_plugin, PiperPlugin)
        assert hasattr(minimal_plugin, 'get_metadata')
        assert hasattr(minimal_plugin, 'get_router')
        assert hasattr(minimal_plugin, 'is_configured')
        assert hasattr(minimal_plugin, 'initialize')
        assert hasattr(minimal_plugin, 'shutdown')
        assert hasattr(minimal_plugin, 'get_status')

    def test_get_metadata_returns_metadata(self, minimal_plugin):
        """Test get_metadata() returns PluginMetadata"""
        metadata = minimal_plugin.get_metadata()
        assert isinstance(metadata, PluginMetadata)
        assert metadata.name == "minimal"

    def test_get_router_returns_optional_router(self, minimal_plugin):
        """Test get_router() returns Optional[APIRouter]"""
        router = minimal_plugin.get_router()
        assert router is None or isinstance(router, APIRouter)

    def test_is_configured_returns_bool(self, minimal_plugin):
        """Test is_configured() returns bool"""
        result = minimal_plugin.is_configured()
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_initialize_is_async(self, minimal_plugin):
        """Test initialize() is async"""
        result = await minimal_plugin.initialize()
        assert result is None

    @pytest.mark.asyncio
    async def test_shutdown_is_async(self, minimal_plugin):
        """Test shutdown() is async"""
        result = await minimal_plugin.shutdown()
        assert result is None

    def test_get_status_returns_dict(self, minimal_plugin):
        """Test get_status() returns dict"""
        status = minimal_plugin.get_status()
        assert isinstance(status, dict)


class TestPluginWithRouter:
    """Tests for plugins with router implementation"""

    def test_router_is_api_router(self, plugin_with_router):
        """Test router is FastAPI APIRouter"""
        router = plugin_with_router.get_router()
        assert isinstance(router, APIRouter)

    def test_router_has_prefix(self, plugin_with_router):
        """Test router has prefix configured"""
        router = plugin_with_router.get_router()
        assert router.prefix == "/api/v1/test"

    def test_router_has_routes(self, plugin_with_router):
        """Test router has routes defined"""
        router = plugin_with_router.get_router()
        assert len(router.routes) > 0

    def test_metadata_has_routes_capability(self, plugin_with_router):
        """Test plugin with router declares routes capability"""
        metadata = plugin_with_router.get_metadata()
        assert "routes" in metadata.capabilities


class TestPluginLifecycle:
    """Tests for plugin lifecycle management"""

    @pytest.mark.asyncio
    async def test_initialize_before_use(self, minimal_plugin):
        """Test plugin can be initialized"""
        await minimal_plugin.initialize()
        assert minimal_plugin.is_configured()

    @pytest.mark.asyncio
    async def test_shutdown_after_use(self, minimal_plugin):
        """Test plugin can be shut down"""
        await minimal_plugin.initialize()
        await minimal_plugin.shutdown()
        # Plugin should still report status after shutdown
        status = minimal_plugin.get_status()
        assert isinstance(status, dict)

    @pytest.mark.asyncio
    async def test_full_lifecycle(self, minimal_plugin):
        """Test complete plugin lifecycle"""
        # Initialize
        await minimal_plugin.initialize()

        # Use plugin
        metadata = minimal_plugin.get_metadata()
        assert metadata.name == "minimal"

        router = minimal_plugin.get_router()
        assert router is None

        status = minimal_plugin.get_status()
        assert isinstance(status, dict)

        # Shutdown
        await minimal_plugin.shutdown()


class TestPluginStatus:
    """Tests for plugin status reporting"""

    def test_status_is_dict(self, minimal_plugin):
        """Test status is dictionary"""
        status = minimal_plugin.get_status()
        assert isinstance(status, dict)

    def test_status_not_empty(self, minimal_plugin):
        """Test status contains information"""
        status = minimal_plugin.get_status()
        assert len(status) > 0

    def test_status_includes_configured(self, plugin_with_router):
        """Test status includes configuration status"""
        status = plugin_with_router.get_status()
        # Status should have some meaningful information
        assert isinstance(status, dict)


class TestPluginValidation:
    """Tests for plugin validation helpers"""

    def test_validate_plugin_has_all_methods(self, minimal_plugin):
        """Test helper to validate plugin implements all methods"""
        required_methods = [
            'get_metadata',
            'get_router',
            'is_configured',
            'initialize',
            'shutdown',
            'get_status'
        ]

        for method in required_methods:
            assert hasattr(minimal_plugin, method), f"Missing method: {method}"

    def test_validate_method_signatures(self, minimal_plugin):
        """Test method signatures match interface"""
        # get_metadata() -> PluginMetadata
        metadata = minimal_plugin.get_metadata()
        assert isinstance(metadata, PluginMetadata)

        # get_router() -> Optional[APIRouter]
        router = minimal_plugin.get_router()
        assert router is None or isinstance(router, APIRouter)

        # is_configured() -> bool
        configured = minimal_plugin.is_configured()
        assert isinstance(configured, bool)

        # get_status() -> Dict[str, Any]
        status = minimal_plugin.get_status()
        assert isinstance(status, dict)
```

### Task 4: Create Plugin Validation Utility

**File**: `tests/plugins/test_plugin_interface.py` (add at end)

```python
# Plugin validation helper function
def validate_plugin_interface(plugin: PiperPlugin) -> bool:
    """
    Validate that a plugin correctly implements PiperPlugin interface.

    Args:
        plugin: Plugin instance to validate

    Returns:
        bool: True if valid, raises AssertionError if invalid
    """
    # Check it's a PiperPlugin
    assert isinstance(plugin, PiperPlugin), "Plugin must inherit from PiperPlugin"

    # Check all methods exist
    required_methods = [
        'get_metadata', 'get_router', 'is_configured',
        'initialize', 'shutdown', 'get_status'
    ]
    for method in required_methods:
        assert hasattr(plugin, method), f"Missing required method: {method}"

    # Check method return types
    metadata = plugin.get_metadata()
    assert isinstance(metadata, PluginMetadata), "get_metadata() must return PluginMetadata"

    router = plugin.get_router()
    assert router is None or isinstance(router, APIRouter), "get_router() must return Optional[APIRouter]"

    configured = plugin.is_configured()
    assert isinstance(configured, bool), "is_configured() must return bool"

    status = plugin.get_status()
    assert isinstance(status, dict), "get_status() must return dict"

    return True
```

### Task 5: Create Test README

**File**: `tests/plugins/README.md`

```markdown
# Plugin Interface Tests

## Purpose

Validates that plugins correctly implement the PiperPlugin interface.

## Running Tests

```bash
# Run all plugin tests
pytest tests/plugins/ -v

# Run specific test class
pytest tests/plugins/test_plugin_interface.py::TestPiperPluginInterface -v

# Run with coverage
pytest tests/plugins/ --cov=services.plugins --cov-report=html
```

## Test Coverage

- **PluginMetadata**: Dataclass creation and fields
- **PiperPlugin Interface**: All required methods
- **Plugin Lifecycle**: Initialize and shutdown
- **Router Integration**: FastAPI router handling
- **Status Reporting**: Status dict validation

## Using Tests for New Plugins

When creating a new plugin, use `validate_plugin_interface()`:

```python
from tests.plugins.test_plugin_interface import validate_plugin_interface

# Validate your plugin
plugin = MyNewPlugin()
validate_plugin_interface(plugin)  # Raises AssertionError if invalid
```

## Phase 3C Usage

These tests will be used to validate all 4 integration plugin wrappers:
- SlackPlugin
- NotionPlugin
- GitHubPlugin
- CalendarPlugin
```

### Task 6: Test the Test Suite

```bash
# Install pytest if needed
pip install pytest pytest-asyncio --break-system-packages

# Run tests (may fail until Code finishes interface)
pytest tests/plugins/ -v

# Expected: Tests should run (may have import errors until Code finishes)
```

### Task 7: Create Integration Test Plan

**File**: `tests/plugins/INTEGRATION_TEST_PLAN.md`

```markdown
# Plugin Integration Test Plan

## Phase 3C Testing Strategy

When each plugin wrapper is created, run:

### 1. Interface Compliance
```bash
pytest tests/plugins/test_plugin_interface.py -v
```

### 2. Plugin-Specific Tests

**SlackPlugin**:
- Router provides Slack routes
- Config service integration
- Spatial adapter present
- Webhook handling capability

**NotionPlugin**:
- Router provides Notion routes
- MCP adapter integration
- Config service present

**GitHubPlugin**:
- Router provides GitHub routes
- Config service integration
- Standard interface methods

**CalendarPlugin**:
- Router provides Calendar routes
- MCP adapter integration
- OAuth handling

### 3. Full System Integration

After all 4 plugins created:
```bash
# Start app and verify plugins loaded
uvicorn web.app:app --port 8001

# Check plugin registry endpoint (if created)
curl http://localhost:8001/api/v1/plugins

# Verify all routes mounted correctly
curl http://localhost:8001/docs
```

## Success Criteria

- [ ] All interface compliance tests pass
- [ ] All 4 plugins validate successfully
- [ ] Plugin registry shows 4 plugins
- [ ] All plugin routes accessible
- [ ] No runtime errors on startup
```

## Deliverable

Create: `dev/2025/10/02/phase-3a-cursor-test-suite.md`

Include:
1. **Test Suite Structure**: All test files created
2. **Test Coverage**: What each test validates
3. **Fixtures Created**: Reusable test fixtures
4. **Validation Helper**: Plugin validation utility
5. **Documentation**: README and test plan
6. **Usage Guide**: How to use tests in Phase 3C

## Critical Requirements

- **DO create** comprehensive interface tests
- **DO use** pytest and pytest-asyncio
- **DO provide** fixtures for reuse
- **DO create** validation helper function
- **DON'T test** specific plugins yet (Phase 3C)
- **DON'T assume** interface details (wait for Code's implementation)

## Time Estimate
30-45 minutes (parallel with Code's interface work)

## Success Criteria
- [ ] tests/plugins/ directory created
- [ ] Interface compliance tests written
- [ ] Lifecycle tests written
- [ ] Router integration tests written
- [ ] Fixtures provided
- [ ] Validation helper created
- [ ] Documentation complete
- [ ] Tests ready for Phase 3C use

---

**Deploy at 5:32 PM**
**Parallel with Code's interface definition**
