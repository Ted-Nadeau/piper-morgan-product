# The Excellence Flywheel - MANDATORY READING

**If you're a new lead developer, THIS is why we achieve exceptional velocity.**

## The Flywheel Effect

Quality → Velocity → Quality → Velocity (compounds infinitely)

## Four Pillars (Non-Negotiable)

### 1. Systematic Verification First

```bash
# ALWAYS run these before ANY work:
find . -name "*.py" | grep [feature]  # Find existing patterns
grep -r "pattern" services/            # Check implementations
cat services/domain/models.py          # Verify domain models
```

### 2. Test-Driven Development

- Write test FIRST, watch it fail
- Implement MINIMAL solution
- Verify success before moving on
- NO EXCEPTIONS

### 3. Multi-Agent Coordination

- Claude Code: Multi-file systematic work
- Cursor: Targeted fixes and UI testing
- NEVER work alone, always coordinate
- **Task Decomposition**: Break complex tasks into agent-specific subtasks
- **Agent Assignment**: Match tasks to agent strengths (Code vs Cursor)
- **Synchronization Points**: Plan handoffs and coordination protocols
- **Performance Monitoring**: Track coordination latency and success rates

### 4. GitHub-First Tracking & Test Activation

- Create issue BEFORE starting
- Update backlog.md and ../planning/roadmap.md
- Track progress in issue comments
- Close with evidence of completion
- **Test Infrastructure**: Activate our 599+ test suite before implementation
- **Smoke Tests**: Run quick validation (<5 seconds) for immediate feedback
- **Integration Tests**: Validate complete workflows before deployment
- **Performance Monitoring**: Track test execution time and success rates

### 5. Agent-Driven Development

- Use `/agent` command for complex multi-agent tasks
- Specialized agents for focused execution
- Systematic handoffs between agents
- Compound expertise across interactions

## Daily Practice

1. Start with verification commands
2. Write failing test
3. Implement minimal fix
4. Verify with evidence
5. Document patterns discovered

**Break this cycle = Break the flywheel**
