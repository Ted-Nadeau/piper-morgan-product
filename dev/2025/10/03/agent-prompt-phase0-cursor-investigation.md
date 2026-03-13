# Cursor Agent Prompt: GREAT-3B Phase 0 - Investigation

## Session Log Management
Create new session log: `dev/2025/10/03/2025-10-03-phase0-cursor-investigation.md`

Update with timestamped entries for your work.

## Mission
**Investigate web/app.py Integration**: Understand current plugin loading in lifespan, analyze what needs to change, and design new loading pattern.

## Context

**GREAT-3A Complete** (yesterday):
- 4 plugins with static imports in `web/app.py`
- Plugins auto-register on import
- Registry initializes and mounts routers

**GREAT-3B Goal** (today):
Replace static imports with discovery-based dynamic loading controlled by config.

## Your Tasks

### Task 1: Analyze Current Loading Pattern

**Examine web/app.py lifespan function**:
```bash
# Find the lifespan function
grep -B 5 -A 50 "@asynccontextmanager" web/app.py | grep -A 50 "async def lifespan"

# Focus on plugin section
grep -B 2 -A 30 "Phase 3C: Import plugins" web/app.py
```

**Document Current Flow**:
1. What happens at startup?
2. When are plugins imported?
3. When are plugins initialized?
4. When are routers mounted?
5. What happens at shutdown?

**Current Code Analysis**:
```python
# Phase 3C: Import plugins (triggers auto-registration)
print("  📦 Loading plugins...")
from services.integrations.calendar.calendar_plugin import _calendar_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.slack.slack_plugin import _slack_plugin

# Initialize all registered plugins
init_results = await registry.initialize_all()
# ...
# Mount plugin routers
routers = registry.get_routers()
for router in routers:
    app.include_router(router)
```

**Questions to Answer**:
1. Can we replace imports with function calls?
2. Where should discovery happen in this flow?
3. How to handle plugins that fail to load?
4. What order: discover → load → initialize → mount?

### Task 2: Design New Loading Pattern

**Requirements**:
- Replace 4 static imports with discovery
- Only load plugins enabled in config
- Handle missing/broken plugins gracefully
- Maintain same initialization and mounting
- Keep shutdown working

**Proposed New Flow**:
```python
# Phase 3B: Plugin System (Dynamic Loading)
print("\n🔌 Initializing Plugin System...")

try:
    from services.plugins import get_plugin_registry

    registry = get_plugin_registry()

    # Step 1: Discover available plugins
    available = registry.discover_plugins()  # New method
    print(f"  📦 Discovered {len(available)} plugin(s)")

    # Step 2: Load enabled plugins from config
    enabled = registry.load_enabled_plugins()  # New method
    print(f"  ✅ Loaded {len(enabled)} plugin(s)")

    # Step 3: Initialize loaded plugins
    init_results = await registry.initialize_all()
    success_count = sum(1 for success in init_results.values() if success)
    print(f"  ✅ Initialized {success_count}/{len(init_results)} plugin(s)")

    # Step 4: Mount plugin routers
    routers = registry.get_routers()
    for router in routers:
        app.include_router(router)
    print(f"  ✅ Mounted {len(routers)} router(s)")

except Exception as e:
    print(f"  ⚠️ Plugin system error: {e}")
    # Don't fail startup if plugins have issues
```

**Evaluate**:
- Is this flow clear?
- Error handling adequate?
- Backwards compatible?
- Testable?

### Task 3: Analyze Error Handling Needs

**Current Behavior**:
- What happens if plugin import fails?
- Does app crash or continue?
- Are errors logged?

**Scenarios to Handle**:
1. Plugin file missing
2. Plugin has syntax error
3. Plugin config invalid
4. Plugin initialization fails
5. No plugins available
6. All plugins disabled

**Design Error Handling**:
- Which failures are fatal?
- Which can be logged and skipped?
- What's the user experience?

### Task 4: Examine Shutdown Flow

**Current Shutdown**:
```bash
# Find shutdown section
grep -A 20 "# Shutdown" web/app.py | grep -A 20 "plugin"
```

**Questions**:
1. How are plugins shut down now?
2. Will dynamic loading affect shutdown?
3. Need any changes to shutdown flow?

### Task 5: Consider Backwards Compatibility

**Transition Plan**:
- Can we support both patterns temporarily?
- How to test new pattern without breaking current?
- Migration strategy?

**Fallback Behavior**:
- If discovery fails, fall back to static imports?
- If config missing, load all plugins?
- If config malformed, what's default?

### Task 6: Integration Testing Strategy

**Test Scenarios Needed**:
1. All plugins enabled (current behavior)
2. Some plugins disabled
3. Plugin missing but enabled in config
4. Config file missing entirely
5. Empty config file
6. Invalid config format

**Testing Approach**:
- Unit tests for discovery?
- Integration tests for loading?
- How to test without breaking current system?

## Deliverable

Create: `dev/2025/10/03/phase-0-cursor-investigation.md`

Include:
1. **Current Flow Analysis**: How loading works now
2. **New Flow Design**: Proposed replacement pattern
3. **Error Handling Strategy**: What to handle, how
4. **Shutdown Analysis**: Any changes needed
5. **Backwards Compatibility Plan**: Transition approach
6. **Testing Strategy**: How to validate new pattern

## Success Criteria
- [ ] Current pattern understood
- [ ] New pattern designed
- [ ] Error scenarios identified
- [ ] Shutdown flow analyzed
- [ ] Migration plan clear
- [ ] Testing approach defined

## Time Estimate
30 minutes

---

**Deploy at 1:50 PM**
**Coordinate with Code on discovery mechanism design**
