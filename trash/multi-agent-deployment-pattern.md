# Multi-Agent Deployment Pattern

## Where This Goes
1. **Add to**: Project knowledge as `multi-agent-deployment-pattern.md`
2. **Reference from**: Lead Developer instructions (00-START-HERE-LEAD-DEV.md)
3. **Link in**: Gameplan template Phase instructions

---

# Multi-Agent Deployment Pattern - Default Approach

## Core Principle: Multi-Agent by Default
**Single-agent deployment requires explicit justification**

---

## Standard Deployment Patterns

### Pattern 1: Parallel Investigation
```markdown
## Phase X: Investigation - Multi-Agent Parallel

### Code Agent Tasks
- Broad codebase search using /agent
- Pattern discovery across all services
- Architecture mapping and documentation
- GitHub bookending (primary responsibility)

### Cursor Agent Tasks
- Test infrastructure investigation
- Specific file deep-dives
- UI/frontend investigation
- Cross-validation preparation

### Coordination
- Both start simultaneously
- Share findings via GitHub issue
- Reconvene after 30 minutes
```

### Pattern 2: Discovery → Implementation
```markdown
## Phase X: Feature Development - Sequential Multi-Agent

### Step 1: Code Discovery (20 min)
- Investigate existing patterns
- Map architecture
- Identify integration points
- Document in GitHub

### Step 2: Parallel Implementation (40 min)
Code Agent:
- Core service implementation
- Domain logic
- Orchestration

Cursor Agent:
- Tests for Code's implementation
- UI/API layer
- Documentation

### Step 3: Cross-Validation (20 min)
- Code validates Cursor's tests
- Cursor validates Code's implementation
- Both update GitHub with verification
```

### Pattern 3: Test-Driven Multi-Agent
```markdown
## Phase X: TDD Implementation - Coordinated Multi-Agent

### Round 1: Test Creation
Code Agent:
- Write failing integration tests
- Define system behavior tests

Cursor Agent:
- Write failing unit tests
- Define component tests

### Round 2: Implementation Race
Both agents implement to make tests pass
- Code: Backend/services
- Cursor: Frontend/UI
- First to green tests wins!

### Round 3: Polish
- Code: Refactor and optimize
- Cursor: UI polish and docs
- Both: Update GitHub with evidence
```

### Pattern 4: Complex Investigation
```markdown
## Phase X: System Analysis - Code with Subagents

### Code Agent - Orchestrator
Deploy /agent subagents for parallel investigation:

```bash
/agent search-patterns "Look for all error handling patterns"
/agent analyze-tests "Analyze test coverage gaps"
/agent map-dependencies "Map service dependencies"
```

### Cursor Agent - Verification
- Validate subagent findings
- Test specific discoveries
- Document patterns found

### Synthesis
- Code: Compile all subagent reports
- Cursor: Verify and test findings
- Both: Create unified recommendations
```

---

## When Single-Agent is Acceptable

### Justified Single-Agent Scenarios
1. **Trivial fixes** (<10 lines, <15 minutes)
2. **Documentation only** (no code changes)
3. **Emergency hotfix** (production down)
4. **Pure investigation** (no implementation)

### Required Justification Format
```markdown
## Single-Agent Justification
**Agent**: [Code/Cursor]
**Reason**: [Why multi-agent not beneficial]
**Risk**: [What could go wrong]
**Mitigation**: [How to prevent issues]
```

---

## Agent Strengths Reference

### Claude Code Strengths
- Multi-file systematic changes
- Broad codebase exploration
- Pattern discovery with /agent
- Architecture design
- Complex refactoring
- Service orchestration

### Cursor Strengths
- Focused file editing
- UI/UX implementation
- Test creation
- Documentation
- Debugging specific issues
- Visual/frontend work

---

## Coordination Mechanisms

### GitHub Issue Coordination
```bash
# Both agents update same issue
# Code updates main checkboxes
# Cursor adds verification comments

gh issue edit [ISSUE#] --body "
## Multi-Agent Status
Code: [Current work]
Cursor: [Current work]
Last Sync: [Time]
"
```

### Session Log Coordination
```markdown
## Multi-Agent Coordination Log

### 10:00 - Deployment
Code: Starting investigation
Cursor: Starting test infrastructure

### 10:30 - Sync Point
Code: Found 3 patterns
Cursor: Tests ready for patterns

### 11:00 - Completion
Code: Implementation complete
Cursor: Verification complete
```

---

## Anti-Patterns to Avoid

### ❌ Default Single-Agent
Starting with one agent without justification

### ❌ Duplicate Work
Both agents doing the same task

### ❌ No Coordination Points
Agents working in isolation without sync

### ❌ Sequential When Parallel Possible
Making Cursor wait for Code unnecessarily

### ❌ Ignoring /agent Capability
Code not using subagents for broad work

---

## Success Metrics

### Good Multi-Agent Deployment
- Parallel work increasing velocity
- Clear task separation
- Regular coordination (30-min intervals)
- Cross-validation catching issues
- GitHub tracking by both agents

### Warning Signs
- One agent idle while other works
- Duplicate implementations
- Conflicting changes
- No cross-validation
- GitHub updates from only one agent

---

## Lead Developer Checklist

Before deploying agents:
- [ ] Multi-agent strategy defined
- [ ] Tasks clearly separated
- [ ] Coordination points scheduled
- [ ] GitHub responsibilities assigned
- [ ] Cross-validation planned
- [ ] /agent usage considered for Code

---

*Pattern Version: 1.0*
*Purpose: Ensure multi-agent deployment is the default*
*Key Principle: Two agents are better than one*
