# Claude Code Agent Prompt: GREAT-3B Phase 0 - Investigation

## Session Log Management
Create new session log: `dev/2025/10/03/2025-10-03-phase0-code-investigation.md`

Update with timestamped entries for your work.

## Mission
**Investigate Current Plugin System**: Understand auto-registration pattern, design discovery mechanism, and plan config structure.

## Context

**GREAT-3A Complete** (yesterday):
- PiperPlugin interface with 6 methods
- PluginRegistry operational (singleton)
- 4 plugins at `services/integrations/{calendar,github,notion,slack}/[name]_plugin.py`
- 34 tests passing

**GREAT-3B Goal** (today):
Replace static imports with dynamic discovery and config-based loading.

**Current Loading** (from verification):
```python
# web/app.py - Phase 3C section
from services.integrations.calendar.calendar_plugin import _calendar_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.slack.slack_plugin import _slack_plugin
```

## Your Tasks

### Task 1: Understand Auto-Registration Pattern

**Examine one plugin file in detail**:
```bash
cat services/integrations/slack/slack_plugin.py
```

**Questions to answer**:
1. How does `_slack_plugin = SlackPlugin()` trigger registration?
2. Where is `get_plugin_registry().register()` called?
3. What happens on module import?
4. Does the plugin class need modification for dynamic loading?

**Document**:
- Current auto-registration mechanism
- Whether it works with dynamic imports
- Any changes needed for importlib

### Task 2: Design Discovery Mechanism

**Analyze target directory structure**:
```bash
# See what's in integrations
ls -la services/integrations/

# Find all plugin files
find services/integrations -name "*_plugin.py" -type f

# Check naming patterns
ls -la services/integrations/*/[a-z]*_plugin.py
```

**Design Requirements**:
- Scan `services/integrations/*/` for `*_plugin.py` files
- Extract plugin name from filename (e.g., `slack_plugin.py` → "slack")
- Return dict of available plugins: `{"slack": "services.integrations.slack.slack_plugin", ...}`
- Handle missing/malformed files gracefully

**Create pseudocode**:
```python
def discover_plugins() -> Dict[str, str]:
    """
    Scan integrations directory for plugin files.

    Returns:
        Dict mapping plugin name to module path
        Example: {"slack": "services.integrations.slack.slack_plugin"}
    """
    # Your design here
```

### Task 3: Analyze Dynamic Import Requirements

**Test dynamic import with existing plugin**:
```python
# Try importing slack plugin dynamically
import importlib

module_path = "services.integrations.slack.slack_plugin"
module = importlib.import_module(module_path)

# What's in the module?
print(dir(module))

# Is _slack_plugin accessible?
print(hasattr(module, '_slack_plugin'))

# Does import trigger auto-registration?
from services.plugins import get_plugin_registry, reset_plugin_registry
reset_plugin_registry()

# Import should register plugin
module = importlib.import_module("services.integrations.slack.slack_plugin")
registry = get_plugin_registry()
print("Plugins after import:", registry.list_plugins())
```

**Document**:
- Does importlib work with current pattern?
- Do we get the `_plugin` instance?
- Does auto-registration still trigger?
- Any issues to address?

### Task 4: Design Config File Structure

**Requirements** (from Chief Architect):
- List of enabled plugins
- Per-plugin settings (optional)
- Clear, readable format

**Proposed Structure**:
```yaml
# config/plugins.yaml
plugins:
  enabled:
    - slack
    - github
    - notion
    - calendar

  settings:
    slack:
      # Plugin-specific config if needed
      timeout: 30
    github:
      default_org: "myorg"
```

**Alternative Structure**:
```yaml
# config/plugins.yaml
slack:
  enabled: true
  timeout: 30

github:
  enabled: true
  default_org: "myorg"

notion:
  enabled: false  # Disabled plugin

calendar:
  enabled: true
```

**Evaluate**:
- Which structure is clearer?
- How to handle missing config (default to enabled/disabled)?
- Where does this fit with existing config pattern?

### Task 5: Check Existing Config System

**Analyze current config setup**:
```bash
# What config files exist?
ls -la config/

# How do services read config?
grep -r "ConfigService" services/integrations/slack/ --include="*.py" -A 5 | head -30

# Is there a config loader pattern?
ls -la config/*.py 2>/dev/null
```

**Questions**:
- How do integration config services work?
- Should plugin config use same pattern?
- Where should plugin config live?

### Task 6: Implementation Planning

**Create implementation plan**:

1. **Discovery Function Design**:
   - Function signature
   - Algorithm for scanning
   - Error handling approach
   - Return format

2. **Dynamic Loading Design**:
   - Function signature
   - Import mechanism
   - Registration approach
   - Error handling

3. **Config Integration Design**:
   - Config file location and format
   - Parser implementation
   - Default behavior (all enabled? all disabled?)
   - Integration with PluginRegistry

4. **Order of Implementation**:
   - What to build first?
   - Dependencies between components?
   - Testing strategy?

## Deliverable

Create: `dev/2025/10/03/phase-0-code-investigation.md`

Include:
1. **Auto-Registration Analysis**: How current pattern works
2. **Discovery Design**: Pseudocode and algorithm
3. **Dynamic Import Test**: Results from importlib testing
4. **Config Structure Recommendation**: Preferred format with rationale
5. **Integration Analysis**: How plugin config fits with existing patterns
6. **Implementation Plan**: Step-by-step build order

## Success Criteria
- [ ] Auto-registration pattern understood
- [ ] Discovery algorithm designed
- [ ] Dynamic import verified working
- [ ] Config structure recommended
- [ ] Implementation plan clear
- [ ] All questions answered

## Time Estimate
30 minutes

---

**Deploy at 1:50 PM**
**Coordinate with Cursor on complementary investigation**
