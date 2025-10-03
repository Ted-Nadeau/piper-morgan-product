# Cursor Agent Prompt: GREAT-3B Phase 4 - web/app.py Integration

## Session Log Management
Continue session log: `dev/2025/10/03/2025-10-03-[timestamp]-cursor-log.md`

Update with timestamped entries for Phase 4 work.

## Mission
**Update web/app.py**: Replace static plugin imports with dynamic discovery-based loading using new PluginRegistry methods.

## Context

**Phase 1-3 Complete**: Full dynamic loading system operational
- `discover_plugins()` - finds available plugins
- `load_plugin()` - loads individual plugin
- `load_enabled_plugins()` - discovers + filters + loads
- Config in PIPER.user.md controls what loads
- 48 tests passing

**Phase 4 Goal**: Integrate dynamic loading into app startup, removing static imports.

## Your Tasks

### Task 1: Locate Current Plugin Loading

**File**: `web/app.py`

**Find the lifespan function and plugin section**:
```bash
grep -B 5 -A 30 "Phase 3C: Import plugins" web/app.py
```

**Current code** (from GREAT-3A):
```python
# Phase 3C: Import plugins (triggers auto-registration)
print("  📦 Loading plugins...")
from services.integrations.calendar.calendar_plugin import _calendar_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.slack.slack_plugin import _slack_plugin

# Initialize all registered plugins
init_results = await registry.initialize_all()
# ... rest of initialization
```

### Task 2: Replace with Dynamic Loading

**File**: `web/app.py`

**Replace the static imports section with**:

```python
# Phase 3B: Plugin System (Dynamic Loading - GREAT-3B)
print("\n🔌 Initializing Plugin System...")

try:
    from services.plugins import get_plugin_registry

    registry = get_plugin_registry()

    # Discover and load enabled plugins from config
    load_results = registry.load_enabled_plugins()

    success_count = sum(1 for success in load_results.values() if success)
    total_count = len(load_results)

    if total_count == 0:
        print("  ⚠️  No plugins enabled in configuration")
    else:
        print(f"  📦 Loaded {success_count}/{total_count} plugin(s)")
        for name, success in load_results.items():
            status = "✅" if success else "❌"
            print(f"    {status} {name}")

    # Initialize all registered plugins
    init_results = await registry.initialize_all()

    success_count = sum(1 for success in init_results.values() if success)
    total_count = len(init_results)

    print(f"  ✅ Initialized {success_count}/{total_count} plugin(s)")

    # Mount plugin routers
    routers = registry.get_routers()
    for router in routers:
        app.include_router(router)

    print(f"  ✅ Mounted {len(routers)} router(s)")

    # Store registry in app state for access
    app.state.plugin_registry = registry

    print(f"✅ Plugin system initialized\n")

except Exception as e:
    print(f"⚠️ Plugin system initialization failed: {e}")
    print("   Continuing without plugin system\n")
    # Don't fail startup if plugin system has issues
    app.state.plugin_registry = None
```

**Key Changes**:
- ❌ Remove 4 static imports
- ✅ Add `registry.load_enabled_plugins()` call
- ✅ Better status reporting (shows which plugins loaded)
- ✅ Maintain same initialization and mounting flow
- ✅ Keep error handling (don't fail startup)

### Task 3: Verify Shutdown Still Works

**Find shutdown section**:
```bash
grep -B 5 -A 20 "Shutting down Plugin System" web/app.py
```

**Verify shutdown logic** is still correct:
```python
# Shutdown: cleanup plugins
print("\n🔌 Shutting down Plugin System...")

if hasattr(app.state, 'plugin_registry') and app.state.plugin_registry:
    try:
        shutdown_results = await app.state.plugin_registry.shutdown_all()
        success_count = sum(1 for success in shutdown_results.values() if success)
        print(f"✅ Plugin shutdown: {success_count}/{len(shutdown_results)} successful")
    except Exception as e:
        print(f"⚠️ Plugin shutdown error: {e}")

print("🛑 Plugin system shutdown complete\n")
```

**No changes needed** - shutdown already uses registry, not imports.

### Task 4: Test App Startup

**Start the app**:
```bash
cd ~/Development/piper-morgan
python3 main.py
```

**Verify output shows**:
- "Initializing Plugin System"
- "Loaded 4/4 plugin(s)" (all enabled by default)
- Each plugin status (✅)
- "Initialized 4/4 plugin(s)"
- "Mounted X router(s)"
- "Plugin system initialized"

**Check app is functional**:
```bash
# In another terminal
curl http://localhost:8001/
# Should get home page

curl http://localhost:8001/api/health
# Should return 200 OK
```

**Shutdown cleanly** (Ctrl+C) and verify:
- "Shutting down Plugin System"
- "Plugin shutdown: 4/4 successful"

### Task 5: Test with Disabled Plugin

**Edit config/PIPER.user.md**:
```yaml
plugins:
  enabled:
    - github
    - slack
    # - notion    # Disabled for testing
    - calendar
```

**Start app again**:
```bash
python3 main.py
```

**Verify output shows**:
- "Loaded 3/3 plugin(s)" (not 4)
- Notion not in the list
- App still functions correctly

**Restore config** (enable all plugins):
```yaml
plugins:
  enabled:
    - github
    - slack
    - notion
    - calendar
```

### Task 6: Run Integration Tests

**Full test suite**:
```bash
PYTHONPATH=. python3 -m pytest tests/ -v -k "not slow"
```

**Plugin-specific tests**:
```bash
PYTHONPATH=. python3 -m pytest tests/plugins/ -v
```

**Verify**: All tests still passing

### Task 7: Update Comments

**File**: `web/app.py`

Update section comment from:
```python
# Phase 3C: Import plugins (triggers auto-registration)
```

To:
```python
# Phase 3B: Plugin System (Dynamic Loading - GREAT-3B)
```

Add comment explaining the change:
```python
# GREAT-3B Update: Replaced static imports with dynamic loading
# - Plugins discovered from services/integrations/*/
# - Config in PIPER.user.md controls what loads
# - Backwards compatible: all plugins enabled by default
```

### Task 8: Create Migration Test Script

**Create**: `test_plugin_migration.py` (temporary)

```python
"""
Test that plugin system migration maintains functionality
"""

import subprocess
import time
import requests

def test_app_starts():
    """Test app starts successfully"""
    print("Starting app...")
    proc = subprocess.Popen(
        ["python3", "main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Wait for startup
    time.sleep(3)

    try:
        # Check if app is running
        response = requests.get("http://localhost:8001/api/health")
        assert response.status_code == 200
        print("✅ App started successfully")

        # Check plugin routes work
        # (Would need to test specific plugin endpoints)

        return True
    finally:
        # Cleanup
        proc.terminate()
        proc.wait(timeout=5)
        print("✅ App shutdown successfully")

if __name__ == "__main__":
    test_app_starts()
    print("\n✅ Migration test passed!")
```

## Deliverable

Create: `dev/2025/10/03/phase-4-cursor-app-integration.md`

Include:
1. **Code Changes**: Before/after comparison of web/app.py
2. **Startup Test**: Output showing dynamic loading works
3. **Config Test**: Output with plugin disabled
4. **Test Results**: All tests still passing
5. **Migration Verification**: App functionality maintained

## Success Criteria
- [ ] Static imports removed from web/app.py
- [ ] Dynamic loading integrated
- [ ] App starts successfully
- [ ] All 4 plugins load by default
- [ ] Can disable plugins via config
- [ ] All tests still passing
- [ ] Shutdown working correctly
- [ ] No breaking changes

## Critical Requirement
**Must maintain backwards compatibility**: Users who don't add plugin config should see no change in behavior (all plugins load).

---

**Deploy at 3:20 PM**
**Final integration before Phase Z validation**
