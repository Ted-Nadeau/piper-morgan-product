# CORE-GREAT-3: Plugin Architecture Epic

## Title
CORE-GREAT-3: Plugin Architecture - Extract Integrations

## Labels
epic, refactor, architecture, plugin, great-refactor

## Description

## Overview
Define plugin interface and extract all integrations (GitHub, Slack, Notion) into plugins with spatial intelligence pattern.

## Background
- Integrations currently embedded in core code
- Different patterns for each integration
- No consistent interface for adding new integrations
- Spatial intelligence pattern not uniformly applied
- ADR-034 (Plugin Architecture) already exists but not implemented

## Pre-Work: ADR Review
- [ ] Review ADR-034 (Plugin Architecture) for implementation approach
- [ ] Review ADR-013 (MCP + Spatial Intelligence Integration) for patterns
- [ ] Review ADR-017 (Spatial MCP) for spatial requirements
- [ ] Review ADR-001 (MCP Integration) for protocol alignment
- [ ] Run verification commands to map current integration code
- [ ] Document all integration touchpoints in core
- [ ] Identify any additional integrations beyond GitHub/Slack/Notion
- [ ] Update ADRs based on actual plugin implementation

## Acceptance Criteria
- [ ] Each integration is a separate plugin module
- [ ] Core doesn't import integration-specific code
- [ ] Plugins can be disabled/enabled via config
- [ ] All existing features still work
- [ ] Spatial intelligence pattern uniformly applied
- [ ] Plugin interface follows ADR-034 design
- [ ] MCP readiness per ADR-001

## Tasks
- [ ] Complete ADR pre-work review
- [ ] Map all current integration touchpoints
- [ ] Design plugin interface based on ADR-034
- [ ] Create plugin base class
- [ ] Create plugin loader mechanism
- [ ] **Extract GitHub to plugin**:
  - [ ] Move GitHub code to plugins/github/
  - [ ] Implement plugin interface
  - [ ] Add spatial intelligence (ADR-013)
  - [ ] Test GitHub plugin isolation
  - [ ] Verify all GitHub features work
- [ ] **Extract Slack to plugin**:
  - [ ] Move Slack code to plugins/slack/
  - [ ] Implement plugin interface
  - [ ] Add spatial intelligence
  - [ ] Test Slack plugin isolation
  - [ ] Verify all Slack features work
- [ ] **Extract Notion to plugin**:
  - [ ] Move Notion code to plugins/notion/
  - [ ] Implement plugin interface
  - [ ] Add spatial intelligence
  - [ ] Test Notion plugin isolation
  - [ ] Verify all Notion features work
- [ ] Implement plugin configuration system
- [ ] Add plugin enable/disable mechanism
- [ ] Create plugin discovery system
- [ ] Test multi-plugin orchestration
- [ ] Update ADR-034 with actual implementation details
- [ ] Document plugin development guide

## Lock Strategy
- Plugin interface has contract tests
- Each plugin has comprehensive integration tests
- Core isolation tests (verify no integration imports)
- Dynamic loading verification tests
- Plugin disable/enable tests
- Spatial intelligence validation tests
- All related ADRs updated with implementation

## Dependencies
- CORE-GREAT-2 must be 100% complete

## Estimated Duration
2 weeks

## Success Validation
```bash
# Core should have no direct integration imports
grep -r "from integrations.github" core/ # Should return nothing
grep -r "from integrations.slack" core/  # Should return nothing
grep -r "from integrations.notion" core/ # Should return nothing

# Plugins should be in their own directories
ls -la plugins/
# Expected: github/ slack/ notion/ __init__.py base.py

# Can disable a plugin and system still starts
DISABLED_PLUGINS=github python web/app.py # Should start without GitHub

# All existing integration tests still pass
pytest tests/integrations/ -v
```

## Plugin Checklist
- [ ] Plugin interface defined (base class)
- [ ] Plugin loader implemented
- [ ] Plugin configuration system
- [ ] Plugin discovery mechanism
- [ ] GitHub plugin extracted and working
- [ ] Slack plugin extracted and working
- [ ] Notion plugin extracted and working
- [ ] Spatial intelligence uniformly applied
- [ ] MCP readiness verified
- [ ] All tests passing

## Architecture Validation
- [ ] ADR-034 implementation complete
- [ ] ADR-013 spatial patterns applied
- [ ] ADR-001 MCP alignment verified
- [ ] No core → plugin dependencies
- [ ] Plugin → core interface minimal
- [ ] New plugin addition documented

---

**Note**: This epic follows the Inchworm Protocol - must be 100% complete before moving to CORE-GREAT-4
