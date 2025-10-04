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

_Established October 2025 as part of GREAT-3C_
