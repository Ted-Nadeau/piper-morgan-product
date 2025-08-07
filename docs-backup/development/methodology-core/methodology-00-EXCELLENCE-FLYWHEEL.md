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

### 4. GitHub-First Tracking
- Create issue BEFORE starting
- Update backlog.md and roadmap.md
- Track progress in issue comments
- Close with evidence of completion

## Daily Practice

1. Start with verification commands
2. Write failing test
3. Implement minimal fix
4. Verify with evidence
5. Document patterns discovered

**Break this cycle = Break the flywheel**
