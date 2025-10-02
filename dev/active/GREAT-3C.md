# GREAT-3C: Integration Migration

## Context
Third sub-epic of GREAT-3. Migrates all 4 integrations to plugin architecture while preserving spatial patterns.

## Scope
1. **GitHub Plugin Migration**
   - Move from integration to plugins/github/
   - Implement plugin interface
   - Preserve existing spatial pattern
   - Maintain all current features

2. **Slack Plugin Migration**
   - Move from integration to plugins/slack/
   - Implement plugin interface
   - Preserve Granular spatial pattern (11 files)
   - Maintain all current features

3. **Notion Plugin Migration**
   - Move from integration to plugins/notion/
   - Implement plugin interface
   - Preserve Embedded spatial pattern (1 file)
   - Maintain all current features

4. **Calendar Plugin Migration**
   - Move from integration to plugins/calendar/
   - Implement plugin interface
   - Preserve Delegated MCP pattern
   - Maintain all current features

## Acceptance Criteria
- [ ] All 4 integrations migrated to plugins/
- [ ] Each plugin implements standard interface
- [ ] Spatial patterns preserved and working
- [ ] All existing features still work
- [ ] No direct imports from core to plugins
- [ ] Each plugin can be disabled

## Success Validation
```bash
# Plugins in place
ls -la plugins/
# Expected: github/ slack/ notion/ calendar/

# Each plugin can be disabled
DISABLED_PLUGINS=github python main.py  # Works without GitHub
DISABLED_PLUGINS=slack python main.py   # Works without Slack
DISABLED_PLUGINS=notion python main.py  # Works without Notion
DISABLED_PLUGINS=calendar python main.py # Works without Calendar

# All tests passing
pytest tests/integrations/ -v  # Existing tests still work
pytest tests/plugins/ -v  # New plugin tests pass
```

## Anti-80% Check
```
Integration | Migrated | Interface | Spatial | Features | Tests
----------- | -------- | --------- | ------- | -------- | -----
GitHub      | [ ]      | [ ]       | [ ]     | [ ]      | [ ]
Slack       | [ ]      | [ ]       | [ ]     | [ ]      | [ ]
Notion      | [ ]      | [ ]       | [ ]     | [ ]      | [ ]
Calendar    | [ ]      | [ ]       | [ ]     | [ ]      | [ ]
TOTAL: 0/20 checkmarks = 0% (Must reach 100%)
```

## Time Estimate
One to two hurons