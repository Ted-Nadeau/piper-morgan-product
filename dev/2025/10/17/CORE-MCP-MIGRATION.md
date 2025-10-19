# CORE-MCP-MIGRATION: Systematic Model Context Protocol Adoption

## Context
During GREAT-2 investigation, we discovered inconsistent MCP (Model Context Protocol) adoption across integrations. Some services have MCP adapters (Notion, Calendar), others may not (GitHub, Slack). This creates architectural inconsistency and limits our ability to leverage advanced AI context management.

## Background
- MCP provides standardized context management for AI interactions
- Enables better tool integration and context passing
- Some integrations already have MCP adapters (discovered in GREAT-2A)
- Inconsistent adoption creates maintenance complexity
- Future AI capabilities will assume MCP patterns

## Current State (from GREAT-2A findings)
- **Notion**: Has MCP adapter + spatial intelligence ✓
- **Calendar**: Has MCP adapter (basic) ✓
- **GitHub**: MCP status unknown
- **Slack**: Has spatial, MCP status unknown
- **Other integrations**: Not yet assessed

## Acceptance Criteria
- [ ] All integration services have MCP adapters
- [ ] Consistent MCP pattern across all services
- [ ] MCP adapters work with spatial intelligence layer
- [ ] Context passing standardized across integrations
- [ ] Tool definitions follow MCP specification
- [ ] Documentation of MCP patterns complete
- [ ] Migration guide for future services

## Tasks

### Discovery Phase
- [ ] Audit all integration services for MCP status
- [ ] Document which services have MCP adapters
- [ ] Identify MCP pattern variations
- [ ] Assess effort for each migration

### Implementation Phase
- [ ] Create MCP adapter for GitHub (if missing)
- [ ] Create MCP adapter for Slack (if missing)
- [ ] Standardize existing MCP adapters (Notion, Calendar)
- [ ] Create MCP adapter template for future services
- [ ] Ensure MCP works with spatial intelligence layer
- [ ] Update OrchestrationEngine to leverage MCP

### Validation Phase
- [ ] Test context passing between services
- [ ] Verify tool definitions work correctly
- [ ] Performance testing with MCP layer
- [ ] Integration testing across all services

### Documentation Phase
- [ ] Document MCP architecture pattern
- [ ] Create MCP implementation guide
- [ ] Update service documentation
- [ ] Create troubleshooting guide

## Lock Strategy
- All new integrations must use MCP pattern
- Tests verify MCP adapter presence
- Context passing tests required
- Pattern compliance in CI/CD

## Success Validation
```bash
# All services have MCP adapters
ls -la services/integrations/*/mcp_adapter.py

# MCP tests pass
pytest tests/integrations/test_mcp_*.py -v

# Context passing works
python test_mcp_context_flow.py

# Tool definitions valid
python validate_mcp_tools.py
```

## Dependencies
- Complete GREAT-2 (spatial intelligence migration)
- Before GREAT-3 (plugin architecture)
- Before 1.0 release

## Estimated Duration
1-2 weeks, depending on discovery findings

## Risk Assessment

### Medium Risk
- MCP pattern may conflict with existing patterns
- Performance impact of additional layer
- Learning curve for MCP specification

### Mitigation
- Gradual service-by-service migration
- Performance benchmarking at each step
- Clear documentation and examples

## Strategic Value
- **Standardization**: Consistent pattern across all integrations
- **Future-proofing**: Ready for advanced AI capabilities
- **Maintainability**: Single pattern to understand and maintain
- **Interoperability**: Better tool integration with AI models
- **Context Management**: Improved context passing between services

## Priority
HIGH - Required for architectural consistency before 1.0

## Related
- After: CORE-GREAT-2 (Integration Cleanup/Completion)
- Before: CORE-GREAT-3 (Plugin Architecture)
- Related: CORE-ETHICS-ACTIVATE (may use MCP for context)

## Notes
MCP adoption follows the same "75% pattern" we've seen elsewhere - partially implemented but not systematically deployed. This epic ensures consistent adoption across all services.

---

**Labels**: core, architecture, mcp, standardization, integration
