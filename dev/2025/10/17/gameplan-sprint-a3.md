# Gameplan: Sprint A3 - Core Activation

**Sprint**: A3
**Duration**: 2-3 days
**Start**: October 17, 2025
**Context**: Foundation solid from A2, ready for core system activation
**Mission**: MCP migration, Ethics activation, Knowledge graph, complete Notion

## Sprint Scope

### Issues to Complete
1. **CORE-MCP-MIGRATION #198** (2d) - Model Context Protocol standardization
2. **CORE-ETHICS-ACTIVATE #197** (1d) - Ethics middleware activation
3. **CORE-KNOW #99** (1d) - Connect knowledge graph
4. **CORE-KNOW-BOUNDARY #226** (4h) - Knowledge boundary management
5. **CORE-NOTN-UP #165** (Phase 2) - Complete Notion API upgrade from A2

## Issue #198: MCP Migration Strategy

### Overall Approach: Sequential → Parallel → Sequential

**Phase 0: Discovery** (Sequential - Lead Dev - 3 hours)
```python
# Audit all integrations
integrations = ['github', 'slack', 'notion', 'calendar', 'others']
for service in integrations:
    - Check for MCP adapter existence
    - Document current implementation
    - Assess migration effort
    - Note pattern variations
```

**Phase 1: Pattern Definition** (Sequential - Lead Dev - 2 hours)
```python
# Define canonical MCP adapter interface
class MCPAdapter:
    def get_tools() -> List[Tool]
    def execute_tool(name: str, params: dict) -> Result
    def get_context() -> Context
    def update_context(context: Context) -> None
```
- Create adapter template
- Document requirements
- Define test patterns

**Phase 2: Parallel Implementation** (Multiple Agents - 4-6 hours)

**Agent Assignments**:
```
Agent 1 (Code): GitHub MCP Adapter
- Create/update adapter
- Implement tool definitions
- Write tests
- Document

Agent 2 (Code): Slack MCP Adapter
- Create/update adapter
- Integrate with spatial
- Write tests
- Document

Agent 3 (Cursor): Notion MCP Standardization
- Update existing adapter
- Ensure pattern compliance
- Enhance tests
- Document changes

Agent 4 (Cursor): Calendar MCP Standardization
- Update existing adapter
- Ensure pattern compliance
- Enhance tests
- Document changes
```

**Phase 3: Integration** (Sequential - Lead Dev - 3 hours)
- Wire adapters to OrchestrationEngine
- Test context passing between services
- Performance validation
- CI/CD updates

## Day 1 Plan (October 17)

### Morning: MCP Discovery & Pattern
1. **Phase 0**: MCP service audit (3 hours)
2. **Phase 1**: Define MCP pattern (2 hours)

### Afternoon: Start Parallel MCP Work
1. **Brief all agents** with pattern
2. **Launch Phase 2** parallel work
3. **Monitor progress** via quick syncs

### End of Day
- Collect Phase 2 progress
- Plan Day 2 integration

## Day 2 Plan (October 18)

### Morning: Complete MCP
1. **Finish Phase 2** if needed (1 hour)
2. **Phase 3**: Integration & testing (3 hours)
3. **Validate** MCP migration complete

### Afternoon: Ethics & Knowledge Graph
1. **CORE-ETHICS-ACTIVATE #197** (4 hours)
   - Locate ethics middleware
   - Activate and configure
   - Test ethical boundaries
   - Document activation

2. **CORE-KNOW #99** start (2 hours)
   - Investigate knowledge graph state
   - Plan connection approach

## Day 3 Plan (October 19) - If Needed

### Morning: Complete Knowledge Graph
1. **CORE-KNOW #99** complete (2 hours)
2. **CORE-KNOW-BOUNDARY #226** (4 hours)

### Afternoon: Notion Completion
1. **CORE-NOTN-UP #165 Phase 2** (3 hours)
   - Complete API upgrade
   - Test database operations
   - Validate with MCP adapter

## Coordination Protocol

### For Parallel Work (Phase 2)

**Agent Launch Message**:
```
You are Agent [1/2/3/4] working on [Service] MCP adapter.
Pattern template: [link to Phase 1 output]
Your deliverables:
1. MCP adapter following pattern
2. Tests with >90% coverage
3. Documentation
4. No merge conflicts

Work in: services/integrations/[service]/mcp_adapter.py
Tests in: tests/integrations/test_[service]_mcp.py

Time budget: 4-6 hours
Check in every 2 hours
```

**Sync Points**:
- T+2 hours: Progress check
- T+4 hours: Near completion check
- T+6 hours: Completion confirmation

### Conflict Avoidance
- Each agent works on separate service directories
- No shared file modifications
- Pattern template is read-only reference
- Tests isolated per service

## Success Criteria

### MCP Migration Complete
- [ ] All services have MCP adapters
- [ ] Pattern consistency verified
- [ ] Context passing works
- [ ] Tests pass (>90% coverage)
- [ ] Performance acceptable
- [ ] Documentation complete

### Ethics Activation Complete
- [ ] Middleware located and understood
- [ ] Activation configuration complete
- [ ] Ethical boundaries tested
- [ ] No regression in functionality
- [ ] Documentation updated

### Knowledge Graph Connected
- [ ] Connection established
- [ ] Basic operations work
- [ ] Boundaries configured
- [ ] Tests passing
- [ ] Documentation complete

### Notion Upgrade Complete
- [ ] API upgrade finished
- [ ] Database operations work
- [ ] MCP adapter integrated
- [ ] Tests passing
- [ ] No regressions

## Risk Management

### Parallel Work Risks
- **Pattern deviation**: Mitigated by clear template
- **Merge conflicts**: Mitigated by separate directories
- **Communication overhead**: Mitigated by clear assignments
- **Quality variance**: Mitigated by test requirements

### Technical Risks
- **MCP performance impact**: Monitor and benchmark
- **Ethics activation side effects**: Careful testing
- **Knowledge graph complexity**: Time-boxed investigation

## A2 Lessons Applied

1. **Foundation First**: MCP pattern before parallel work
2. **Investigation Prevents Waste**: Phase 0 discovery critical
3. **Batching**: Test after each component
4. **Documentation**: Update as we go

## Notes

- Start with fresh Lead Dev chat (A2 used 100K+ tokens)
- Brief agents clearly for parallel work
- Keep session logs for coordination
- Apply DDD patterns from A2

## Fallback Plan

If parallel work encounters issues:
1. Revert to sequential (adds 1 day)
2. Lead Dev takes primary role
3. Cursor assists with documentation
4. Focus on pattern consistency

---

*Ready for Sprint A3 - combining systematic execution with efficient parallelization*
