# Multi-Agent Coordination Methodology Summary

**To:** Head of Sapient Resources
**From:** Lead Developer Session (2026-01-05)
**Re:** Multi-agent coordination patterns and subagent use in Piper Morgan

---

## Executive Summary

Piper Morgan employs multiple levels of AI agent coordination:

1. **Inter-session coordination** (Claude Code ↔ Cursor) - Different tools working on same codebase
2. **Intra-session subagents** (Task tool deployments) - Spawning specialist agents within Claude Code
3. **Async prompt queue** (coordination/) - Self-service prompts for agents
4. **Git worktrees** (Issue #463) - Isolated directories for parallel work

---

## 1. Inter-Session Agent Coordination (Claude Code ↔ Cursor)

### Documented Methodology
**Source**: `docs/internal/development/methodology-core/methodology-02-AGENT-COORDINATION.md`

### Agent Strengths (Canonical Reference)

| Agent | Strengths |
|-------|-----------|
| **Claude Code** | Multi-file implementations, GitHub Actions, domain architecture, database schema, **subagent coordination**, integration planning, pattern discovery |
| **Cursor** | API endpoints, testing infrastructure, documentation, UI/UX, performance validation, focused file editing, backward compatibility |

### Coordination Modes

1. **Cross-Validation Mode**: Both agents tackle same task, compare approaches, merge best elements
   - Use for: High-risk, critical features, security
   - Cost: Higher time investment

2. **Parallel Separation Mode**: Each agent works their domain, coordinate at integration points
   - Use for: Clear domain boundaries, time-critical work
   - Cost: Requires excellent handoff discipline

### Proven Pattern (August 5, 2025)
PM-081 Universal List Architecture:
- Claude Code: Domain models (1,500+ lines)
- Cursor: API layer
- Result: 6-minute architectural revolution, zero breaking changes

---

## 2. Intra-Session Subagent Deployment (Task Tool)

### How It Works
Within a Claude Code session, the Lead Developer can spawn **Haiku subagents** via the Task tool for parallel investigation or implementation.

### Today's Example (2026-01-05)
```
Deployed 3 Haiku agents in parallel:
| Agent ID | Task | Result |
|----------|------|--------|
| aa60990 | Fix test_api_degradation_integration.py | 10 tests fixed |
| acccefb | Fix test_create_endpoints_contract.py | Mock method fixed |
| ae0117d | Fix test_todo_service.py | UUID owner_id fixed |

Total wall-clock time: ~15 minutes for work that would take 45+ minutes sequentially
```

### Subagent Types Available
- `general-purpose` - Complex multi-step tasks
- `Explore` - Fast codebase exploration (quick/medium/very thorough)
- `Plan` - Architecture and implementation planning
- `claude-code-guide` - Documentation lookups

### Best Practices
1. **Parallel deployment**: Launch multiple Task calls in single message
2. **Clear prompts**: Include issue number, acceptance criteria, evidence requirements
3. **Independence**: Only parallelize truly independent tasks
4. **Monitoring**: Use TaskOutput to check progress

---

## 3. Async Prompt Queue (coordination/)

### Purpose
Self-service prompt queue for when PM isn't available for real-time coordination.

### Structure
```
coordination/
├── manifest.json       # Source of truth for queue state
├── QUEUE-README.md     # Agent instructions
├── available/          # Prompts ready to claim
├── claimed/            # Work in progress
├── complete/           # Finished work
└── blocked/            # Waiting on dependencies
```

### Workflow
1. Agent checks `manifest.json` for available prompts
2. Claims prompt, updates status
3. Executes work (optionally with worktree)
4. Marks complete, awaits PM review

### Manifest Schema
```json
{
  "id": "001",
  "status": "available|claimed|complete|blocked",
  "priority": "P0|P1|P2|P3",
  "estimated_minutes": 60,
  "max_claim_duration": 180,
  "dependencies": ["002"],
  "worktree_path": ".trees/001-abc123"
}
```

---

## 4. Git Worktrees (Issue #463)

### Problem Solved
Multiple agents sharing one git working directory caused:
- 15-20 minute context-switching costs per handoff
- Risk of accidental work on wrong branches
- Merge conflicts from parallel development

### Solution
Isolated worktrees in `.trees/<prompt-id>-<session>/`

### Commands
```bash
./scripts/worktree-setup.sh <prompt-id> <session-id>   # Create
./scripts/worktree-status.sh                           # Check all
./scripts/worktree-teardown.sh <prompt-id>             # Cleanup (requires PM approval)
```

### Implementation Status (Issue #463)
- **Phase 0-2 (MVP)**: ✅ Complete
  - Scripts created
  - Documentation added
  - Manifest schema extended
- **Phase 3-5 (Python Integration)**: Pending
  - Python `WorktreeManager` class
  - Integration with `MandatoryHandoffProtocol`

---

## 5. Coordination Anti-Patterns

### From `methodology-03-COMMON-FAILURES.md`

1. **The 75% Pattern**: Agent implements feature but doesn't close the loop (tests, docs, verification)
2. **Evidence-Free Closure**: Closing issues without proof of completion
3. **Role Drift**: Lead Dev implementing instead of coordinating
4. **Completion Bias**: Claiming "done" without meeting all criteria

### Countermeasures
- Pattern-045: Green Tests, Red User (tests passing ≠ users succeeding)
- Pattern-046: Beads Completion Discipline (no expedience rationalization)
- Pattern-047: Time Lord Alert (escape hatch for uncertainty)

---

## 6. Documentation References

### Core Methodology Docs
- `methodology-02-AGENT-COORDINATION.md` - Coordination framework
- `HOW_TO_USE_MULTI_AGENT.md` - Practical guide
- `MULTI_AGENT_INTEGRATION_GUIDE.md` - Technical integration
- `MULTI_AGENT_QUICK_START.md` - 5-minute deployment

### Infrastructure
- `coordination/QUEUE-README.md` - Prompt queue system
- `.trees/README.md` - Worktree documentation
- `scripts/worktree-*.sh` - Worktree management

### Patterns
- Pattern-045: Anti-completion-bias
- Pattern-046: Beads Completion Discipline
- Pattern-047: Time Lord Alert

---

## 7. Metrics & Observations

### What Works Well
- **Subagent parallelization**: 3x speedup for independent tasks
- **Role clarity**: CODE vs CURSOR assignments reduce conflicts
- **Beads tracking**: Issue-level accountability prevents drift

### Areas for Improvement
- **Worktree adoption**: Phase 3-5 Python integration still pending
- **Cross-session handoffs**: Still relies on session logs rather than structured protocol
- **Subagent cost**: Haiku agents are cheap but Opus coordination is expensive

---

## 8. Recommendations for Codification

For the Head of Sapient Resources to formalize:

1. **Subagent Deployment Protocol**
   - When to use (independent tasks, investigation, parallel fixes)
   - Evidence requirements (what to report back)
   - Cost considerations (Haiku for implementation, Opus for coordination)

2. **Coordination Mode Selection**
   - Decision tree for Cross-Validation vs Parallel Separation
   - Risk assessment criteria

3. **Handoff Discipline**
   - Structured handoff format (not just session logs)
   - Required fields: context, work done, blockers, next steps

4. **Completion Criteria Enforcement**
   - The Completion Discipline Triad (045, 046, 047)
   - "Done" definition checklist

---

*Prepared from live session experience and methodology documentation review.*
