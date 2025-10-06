# Cursor Agent Prompt: GREAT-3C Phase 4 - Documentation Integration

## Session Log Management
Continue session log: `dev/2025/10/04/2025-10-04-[timestamp]-cursor-log.md`

Update with timestamped entries for Phase 4 work.

## Mission
**Documentation Integration & Polish**: Link all documentation together, add demo plugin references, document versioning policy, and create final documentation polish.

## Context

**Phase 3 Complete**: Demo plugin implemented
- `services/integrations/demo/` exists with 5 files
- 9/9 tests passing
- Fully functional template

**Phase 0 Discovery**: All 4 existing plugins already have `version="1.0.0"`
- No code changes needed
- Just document the versioning policy

**Phase 4 Goal**: Complete documentation integration and add versioning policy.

## Your Tasks

### Task 1: Update Developer Guide with Demo Plugin Reference

**File**: `docs/guides/plugin-development-guide.md`

**Add new section before "Common Patterns"**:

```markdown
## Example: The Demo Plugin

We've created a complete example plugin you can reference or copy.

**Location**: `services/integrations/demo/`

**Files**:
- `config_service.py` - Configuration template
- `demo_integration_router.py` - Router with 3 endpoints
- `demo_plugin.py` - Plugin wrapper
- `tests/test_demo_plugin.py` - Test suite

**Try it**:
```bash
# Load the demo plugin
python3 main.py
# Visit http://localhost:8001/api/integrations/demo/health

# Run tests
PYTHONPATH=. pytest services/integrations/demo/tests/ -v
```

**What it demonstrates**:
- Health check endpoint pattern
- Echo endpoint (simple functionality)
- Status endpoint (integration details)
- Complete test coverage
- Heavily commented code

**How to use it**:
1. Copy `services/integrations/demo/` to your new integration name
2. Search and replace "demo" with your integration name
3. Modify endpoints and logic for your needs
4. Update tests
5. You're done!

See the demo plugin code for detailed comments explaining each part.
```

### Task 2: Create Versioning Policy Documentation

**File**: `docs/guides/plugin-versioning-policy.md`

```markdown
# Plugin Versioning Policy

**Status**: Active
**Last Updated**: October 4, 2025

## Overview

All Piper Morgan plugins use [Semantic Versioning (semver)](https://semver.org/) to communicate changes and compatibility.

## Version Format

Versions follow the format: `MAJOR.MINOR.PATCH`

Example: `1.2.3`
- **MAJOR**: 1
- **MINOR**: 2
- **PATCH**: 3

## When to Increment

### MAJOR Version (X.0.0)

Increment when making **breaking changes** that affect:
- Plugin interface compatibility
- Router API contracts
- Configuration schema (removing/renaming fields)
- Route paths or parameters

**Example**: Changing `/api/integrations/slack/webhook` to `/api/integrations/slack/v2/webhook`

### MINOR Version (1.X.0)

Increment when adding **new features** that are backwards compatible:
- New routes
- New configuration options (with defaults)
- New capabilities
- Performance improvements

**Example**: Adding a new `/forecast` endpoint to weather integration

### PATCH Version (1.2.X)

Increment when making **backwards compatible bug fixes**:
- Error handling improvements
- Documentation fixes
- Minor refactoring
- Security patches (non-breaking)

**Example**: Fixing error message formatting

## Current Plugin Versions

As of October 2025, all core plugins are at version `1.0.0`:
- Slack: `1.0.0`
- GitHub: `1.0.0`
- Notion: `1.0.0`
- Calendar: `1.0.0`
- Demo: `1.0.0`

## How to Update Versions

**1. Update plugin metadata**:

```python
def get_metadata(self) -> PluginMetadata:
    return PluginMetadata(
        name="slack",
        version="1.1.0",  # Updated version
        # ...
    )
```

**2. Document in CHANGELOG**:

```markdown
## [1.1.0] - 2025-10-15

### Added
- New `/reactions` endpoint for emoji reactions
- Support for threaded messages

### Fixed
- Webhook signature validation
```

**3. Update tests if needed**:

```python
def test_plugin_metadata():
    metadata = plugin.get_metadata()
    assert metadata.version == "1.1.0"  # Update expected version
```

## Version Display

Plugin versions are visible through:

1. **Metadata API**: `GET /api/plugins/{name}/metadata`
2. **Status endpoint**: Each plugin's status endpoint
3. **Startup logs**: Shown during plugin initialization

## Best Practices

### Do's
- ✅ Follow semver strictly
- ✅ Document all version changes
- ✅ Update CHANGELOG
- ✅ Test version upgrades
- ✅ Communicate breaking changes clearly

### Don'ts
- ❌ Skip version increments
- ❌ Use version `0.x.x` for production plugins
- ❌ Break compatibility in PATCH versions
- ❌ Forget to update metadata

## Related Documentation

- [Semantic Versioning](https://semver.org/)
- [Plugin Development Guide](plugin-development-guide.md)
- [CHANGELOG format](https://keepachangelog.com/)

---

*Established October 2025 as part of GREAT-3C*
```

### Task 3: Add Versioning Reference to Pattern Documentation

**File**: `docs/architecture/patterns/plugin-wrapper-pattern.md`

**In "Implementation Guidelines" section, add**:

```markdown
### Versioning Your Plugin

All plugins must specify a version using [Semantic Versioning](https://semver.org/):

```python
def get_metadata(self) -> PluginMetadata:
    return PluginMetadata(
        name="your_integration",
        version="1.0.0",  # MAJOR.MINOR.PATCH
        # ...
    )
```

See [Plugin Versioning Policy](../../guides/plugin-versioning-policy.md) for details on when to increment versions.
```

### Task 4: Update NAVIGATION.md

**File**: `docs/NAVIGATION.md`

**Add under "Developer Guides"**:

```markdown
## Developer Guides

- [Plugin Development Guide](guides/plugin-development-guide.md) - Step-by-step tutorial for adding integrations
- [Plugin Versioning Policy](guides/plugin-versioning-policy.md) - Semantic versioning guidelines for plugins

## Examples

- [Demo Plugin](../services/integrations/demo/) - Complete example integration to copy and adapt
```

### Task 5: Update Main README (services/plugins/README.md)

**Add section after "Configuration"**:

```markdown
## Example Plugin

A complete example plugin is available at `services/integrations/demo/`:

```bash
# View the demo plugin code
ls -la services/integrations/demo/

# Run demo plugin tests
PYTHONPATH=. pytest services/integrations/demo/tests/ -v

# Try the demo endpoints
python3 main.py
curl http://localhost:8001/api/integrations/demo/health
```

The demo plugin demonstrates:
- Standard file structure
- Config service pattern
- Router with multiple endpoints
- Plugin wrapper implementation
- Complete test coverage

See the [Plugin Development Guide](../../docs/guides/plugin-development-guide.md) for how to create your own integration based on this example.

## Versioning

All plugins use [Semantic Versioning](https://semver.org/). See [Plugin Versioning Policy](../../docs/guides/plugin-versioning-policy.md) for details.
```

### Task 6: Create Quick Reference Card

**File**: `docs/guides/plugin-quick-reference.md`

```markdown
# Plugin System Quick Reference

Quick reference for common plugin development tasks.

## File Structure

```
services/integrations/[name]/
├── __init__.py              # Package exports
├── config_service.py        # Configuration (~50 lines)
├── [name]_integration_router.py  # Routes (~100-300 lines)
├── [name]_plugin.py         # Plugin wrapper (~130 lines)
└── tests/
    └── test_[name]_plugin.py     # Tests (~100 lines)
```

## Checklist for New Plugin

- [ ] Create directory structure
- [ ] Implement config service
- [ ] Create router with routes
- [ ] Wrap router as plugin
- [ ] Add auto-registration
- [ ] Write tests (6+ tests)
- [ ] Add to PIPER.user.md
- [ ] Test locally
- [ ] Document in README

## Key Patterns

### Config Service
```python
class MyConfigService:
    def __init__(self):
        self.api_key = os.getenv("MY_API_KEY", "")

    def is_configured(self) -> bool:
        return bool(self.api_key)
```

### Router
```python
class MyIntegrationRouter:
    def __init__(self, config_service: MyConfigService):
        self.config = config_service
        self.router = APIRouter(prefix="/api/integrations/my")
        self._setup_routes()
```

### Plugin
```python
class MyPlugin(PiperPlugin):
    def __init__(self):
        self.config_service = MyConfigService()
        self.router_instance = MyIntegrationRouter(self.config_service)

    # Implement 6 interface methods...
```

### Auto-Registration
```python
from services.plugins import get_plugin_registry
_my_plugin = MyPlugin()
get_plugin_registry().register(_my_plugin)
```

## Common Commands

```bash
# Run plugin tests
PYTHONPATH=. pytest services/integrations/[name]/tests/ -v

# Run all plugin tests
PYTHONPATH=. pytest tests/plugins/ -v

# Start with your plugin
python3 main.py

# Test plugin endpoint
curl http://localhost:8001/api/integrations/[name]/health
```

## Resources

- [Plugin Development Guide](plugin-development-guide.md) - Full tutorial
- [Demo Plugin](../../services/integrations/demo/) - Complete example
- [Plugin Wrapper Pattern](../architecture/patterns/plugin-wrapper-pattern.md) - Architecture
- [Versioning Policy](plugin-versioning-policy.md) - Version management
```

### Task 7: Update NAVIGATION.md with Quick Reference

**Add**:

```markdown
- [Plugin Quick Reference](guides/plugin-quick-reference.md) - Cheat sheet for common tasks
```

## Deliverable

Create: `dev/2025/10/04/phase-4-cursor-documentation-integration.md`

Include:
1. **Files Created**:
   - `docs/guides/plugin-versioning-policy.md`
   - `docs/guides/plugin-quick-reference.md`
2. **Files Modified**:
   - `docs/guides/plugin-development-guide.md` (demo reference)
   - `docs/architecture/patterns/plugin-wrapper-pattern.md` (versioning)
   - `services/plugins/README.md` (demo + versioning)
   - `docs/NAVIGATION.md` (new entries)
3. **Documentation Network**: All docs cross-referenced
4. **Versioning Policy**: Complete semver guidelines

## Success Criteria
- [ ] Demo plugin referenced in developer guide
- [ ] Versioning policy documented
- [ ] Quick reference created
- [ ] All documentation cross-linked
- [ ] NAVIGATION.md complete
- [ ] No broken links

---

**Deploy at 2:00 PM**
**Final documentation polish before Phase Z validation**
