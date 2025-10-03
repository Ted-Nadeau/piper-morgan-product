# Claude Code Agent Prompt: GREAT-3A Phase Z - Validation & Completion

## Session Log Management
Continue using existing session log. Update with timestamped entries for your Phase Z work.

## Mission
**Phase Z Validation**: Execute comprehensive testing and validation to verify GREAT-3A completion.

## Context

**All Implementation Phases Complete**:
- Phase 1: Config compliance (100%)
- Phase 2A/B: web/app.py refactoring (56% reduction)
- Phase 3A: Plugin interface + tests
- Phase 3B: Plugin registry
- Phase 3C: 4 plugin wrappers

**Phase Z Goal**: Validate everything works together, run full test suite, verify success criteria.

## Your Tasks

### Task 1: Full Plugin System Integration Test

```bash
cd ~/Development/piper-morgan

# Test 1: All plugins import and register
python -c "
from services.plugins import get_plugin_registry, reset_plugin_registry
reset_plugin_registry()

# Import all plugins
from services.integrations.slack.slack_plugin import _slack_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.calendar.calendar_plugin import _calendar_plugin

registry = get_plugin_registry()
plugins = registry.list_plugins()

print('Registered plugins:', plugins)
assert len(plugins) == 4, f'Expected 4 plugins, got {len(plugins)}'
assert 'slack' in plugins, 'Slack plugin missing'
assert 'github' in plugins, 'GitHub plugin missing'
assert 'notion' in plugins, 'Notion plugin missing'
assert 'calendar' in plugins, 'Calendar plugin missing'
print('✅ All 4 plugins registered correctly')
"

# Test 2: All plugins validate interface
python -c "
from services.integrations.slack.slack_plugin import _slack_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.calendar.calendar_plugin import _calendar_plugin
from tests.plugins.test_plugin_interface import validate_plugin_interface

print('Validating Slack plugin...')
validate_plugin_interface(_slack_plugin)
print('✅ Slack: PASS')

print('Validating GitHub plugin...')
validate_plugin_interface(_github_plugin)
print('✅ GitHub: PASS')

print('Validating Notion plugin...')
validate_plugin_interface(_notion_plugin)
print('✅ Notion: PASS')

print('Validating Calendar plugin...')
validate_plugin_interface(_calendar_plugin)
print('✅ Calendar: PASS')

print('✅ All plugins validate interface')
"

# Test 3: Plugin metadata verification
python -c "
from services.plugins import get_plugin_registry, reset_plugin_registry
reset_plugin_registry()

from services.integrations.slack.slack_plugin import _slack_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.calendar.calendar_plugin import _calendar_plugin

registry = get_plugin_registry()

print('Plugin Metadata:')
for name in sorted(registry.list_plugins()):
    plugin = registry.get_plugin(name)
    metadata = plugin.get_metadata()
    print(f'  {name}:')
    print(f'    Version: {metadata.version}')
    print(f'    Capabilities: {metadata.capabilities}')
    print(f'    Configured: {plugin.is_configured()}')

print('✅ Plugin metadata validated')
"

# Test 4: Plugin lifecycle
python -c "
import asyncio
from services.plugins import get_plugin_registry, reset_plugin_registry
reset_plugin_registry()

from services.integrations.slack.slack_plugin import _slack_plugin
from services.integrations.github.github_plugin import _github_plugin
from services.integrations.notion.notion_plugin import _notion_plugin
from services.integrations.calendar.calendar_plugin import _calendar_plugin

registry = get_plugin_registry()

async def test_lifecycle():
    # Initialize all
    init_results = await registry.initialize_all()
    print('Initialize results:', init_results)
    assert all(init_results.values()), 'Some plugins failed to initialize'

    # Shutdown all
    shutdown_results = await registry.shutdown_all()
    print('Shutdown results:', shutdown_results)
    assert all(shutdown_results.values()), 'Some plugins failed to shutdown'

    print('✅ Plugin lifecycle tested')

asyncio.run(test_lifecycle())
"

# Test 5: App startup test
python -c "
import sys
sys.path.insert(0, '.')
from web.app import app
print('✅ App loads with plugin system')
"
```

### Task 2: Run Full Test Suite

```bash
# Plugin interface tests
echo "Running plugin interface tests..."
pytest tests/plugins/test_plugin_interface.py -v --tb=short

# Plugin registry tests
echo "Running plugin registry tests..."
pytest tests/plugins/test_plugin_registry.py -v --tb=short

# Config compliance tests
echo "Running config compliance tests..."
pytest tests/integration/config_pattern_compliance/ -v --tb=short

# Generate compliance report
echo "Generating compliance report..."
python tests/integration/config_pattern_compliance/generate_report.py
```

### Task 3: Verify No Regressions

```bash
# Check web/app.py syntax
python -m py_compile web/app.py && echo "✅ web/app.py syntax OK"

# Verify config services still work
python -c "
from services.integrations.slack.config_service import SlackConfigService
from services.integrations.github.config_service import GitHubConfigService
from services.integrations.notion.config_service import NotionConfigService
from services.integrations.calendar.config_service import CalendarConfigService

s = SlackConfigService()
g = GitHubConfigService()
n = NotionConfigService()
c = CalendarConfigService()

print('✅ All config services instantiate')
"

# Verify routers still work
python -c "
from services.integrations.slack.slack_integration_router import SlackIntegrationRouter
from services.integrations.github.github_integration_router import GitHubIntegrationRouter
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
from services.integrations.calendar.calendar_integration_router import CalendarIntegrationRouter

print('✅ All integration routers import correctly')
"
```

### Task 4: Calculate Final Metrics

```bash
# Count lines in web/app.py
echo "web/app.py line count:"
wc -l web/app.py

# Count plugin system lines
echo "Plugin system line count:"
find services/plugins -name "*.py" -exec wc -l {} + | tail -1

# Count plugin wrapper lines
echo "Plugin wrapper line count:"
wc -l services/integrations/*/\*_plugin.py

# Count test lines
echo "Plugin test line count:"
find tests/plugins -name "*.py" -exec wc -l {} + | tail -1
```

### Task 5: Create Completion Summary

**File**: `dev/2025/10/02/GREAT-3A-COMPLETION-SUMMARY.md`

Document:
1. What was accomplished (all phases)
2. Files created/modified
3. Test results (all passing)
4. Metrics (line counts, test coverage)
5. Success criteria verification
6. How to use plugin system
7. Known issues / future work

Use the template from phase-z-gameplan.md as guide.

## Deliverable

Create: `dev/2025/10/02/phase-z-code-validation.md`

Include:
1. **Integration Test Results**: All 4 plugins working together
2. **Test Suite Results**: Plugin tests + config compliance tests
3. **Regression Verification**: No existing functionality broken
4. **Metrics Summary**: Line counts, test coverage, improvements
5. **Completion Summary**: GREAT-3A-COMPLETION-SUMMARY.md created

## Success Criteria

- [ ] All 4 plugins register and load correctly
- [ ] All plugin interface tests passing (24/24)
- [ ] All plugin registry tests passing (10/10)
- [ ] Config compliance maintained at 100%
- [ ] No regressions detected
- [ ] App starts successfully
- [ ] Completion summary created

## Time Estimate
20 minutes

---

**Deploy at 9:10 PM**
**Final validation for GREAT-3A completion**
