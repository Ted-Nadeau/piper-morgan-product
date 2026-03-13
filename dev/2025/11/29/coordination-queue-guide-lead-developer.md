# Coordination Queue Guide for Lead Developer

**Date**: November 29, 2025
**Author**: Chief Architect
**Purpose**: Enable async work distribution through self-service prompt queue

---

## Overview

We've implemented and tested a lightweight coordination queue that allows AI agents to claim and execute work autonomously. Three successful pilots completed today with parallel execution and zero conflicts.

---

## System Architecture

```
/coordination/
├── manifest.json          # Single source of truth for queue state
├── README.md             # Agent instructions
├── available/            # Prompts ready to claim
│   └── XXX-task-name.md
├── claimed/              # Work in progress
│   └── XXX-task-name.md
├── complete/             # Finished work
│   └── XXX-task-name.md
└── blocked/              # Waiting on dependencies
    └── XXX-task-name.md
```

---

## How It Works

### 1. Creating Work
PM or Lead Dev writes prompt files with:
- Context (why this matters)
- Scope (in/out boundaries)
- Acceptance Criteria (checklist)
- Resources (files, ADRs, issues)
- Deliverables (what gets created)

### 2. Agent Claims Work
```bash
# Agent checks available work
cat /coordination/manifest.json

# Claims by updating manifest + moving file
# Updates: status, claimed_by, claimed_at
```

### 3. Agent Executes
- Follows prompt specifications
- Creates deliverables
- Meets acceptance criteria

### 4. Agent Completes
- Moves prompt to complete/
- Updates manifest with completed_at
- Notes deliverable locations

---

## GitHub Issue Integration

### Breaking Down Large Issues

**GitHub Issue #433** (16 hours) becomes:
```yaml
coordination/available/
  ├── 001-implement-moment-model.md      # 4h, refs #433
  ├── 002-implement-situation-model.md   # 4h, refs #433
  ├── 003-implement-lifecycle-enum.md    # 4h, refs #433
  └── 004-integrate-with-existing.md     # 4h, refs #433
```

Each prompt must reference the parent GitHub issue.

### Documentation Requirements
Add to each GitHub issue:
```markdown
## Documentation Updates Required
- [ ] Update domain-models.md with new models
- [ ] Update architecture.md if structure changes
- [ ] Update dependency diagrams if relationships change
```

---

## Pilot Results (Nov 29)

| Prompt | Agent | Time | Result |
|--------|-------|------|---------|
| 001-Audit | Claude Code | 37 min | Complete audit report |
| 002-Mailbox | Claude Code | 6 min | Structure + bonus CLI |
| 003-Composting | Claude Code | 9 min | Full architecture doc |

**Key Success**: Two agents worked in parallel with no conflicts.

---

## Agent Feedback & Iterations

### What's Working
- Clear claim/complete lifecycle
- Self-documenting via file movement
- Parallel execution without conflicts
- Comprehensive prompt specifications

### Friction Points (from pilots)
1. **Path confusion**: Sandbox paths needed correction
2. **Manual manifest updates**: Error-prone
3. **Deliverable locations**: Not always clear

### Recommended Improvements
```bash
# 1. Add claim/complete scripts
coordination/scripts/claim.sh 001     # Claims prompt, updates manifest
coordination/scripts/complete.sh 001  # Marks complete, moves file

# 2. Explicit paths in prompts
Deliverable: /docs/internal/architecture/current/new-doc.md

# 3. Add blocked workflow
coordination/scripts/block.sh 001 "Waiting on ADR-045 approval"
```

---

## Creating Effective Prompts

### Template Structure
```markdown
# [TITLE]: Brief description

## Context
[Why this matters, what triggered it]

## GitHub Issue
#[NUMBER] - [Link if needed]

## Scope
**In Scope:**
- Specific deliverables
- Clear boundaries

**Out of Scope:**
- What NOT to do

## Acceptance Criteria
- [ ] Specific, verifiable item
- [ ] Another checkable item
- [ ] Documentation updated

## Resources
- /path/to/relevant/file.md
- ADR-XXX for context
- GitHub issue #XXX

## Deliverables
1. Create: /specific/path/to/output.md
2. Update: /path/to/existing.md

## Verification
[How to confirm it works]
```

### Size Guidelines
- **2-4 hours**: Single focused deliverable
- **4-8 hours**: Multiple related deliverables
- **8+ hours**: Consider breaking into multiple prompts

---

## Sprint Planning with Queue

### Week Planning
1. Break GitHub issues into 2-8 hour prompts
2. Place in available/ with priority prefixes (P0-, P1-, P2-)
3. Agents work queue throughout week
4. Review complete/ at sprint end

### Daily Flow
```
Morning: Write 2-3 prompts based on priorities
Midday: Check progress (manifest.json)
Evening: Review completed work
Next day: Address any blocked items
```

---

## Sub-agent Deployment

When a Sonnet agent needs to deploy Haiku sub-agents:

```markdown
# In the Sonnet agent's prompt:
"You may create micro-prompts in /coordination/available/
for simpler subtasks. Prefix them with 'SUB-' and reference
this parent prompt."
```

Example:
```
001-implement-feature.md (parent, Sonnet)
├── SUB-001a-write-tests.md (Haiku)
├── SUB-001b-update-docs.md (Haiku)
└── SUB-001c-create-examples.md (Haiku)
```

---

## Monitoring & Metrics

### Check Queue Status
```python
# Simple status script (could add to utils/)
import json
with open('coordination/manifest.json') as f:
    data = json.load(f)
    print(f"Available: {data['queue_stats']['available']}")
    print(f"Claimed: {data['queue_stats']['claimed']}")
    print(f"Complete: {data['queue_stats']['complete']}")
```

### Cycle Time Tracking
Manifest includes timestamps for:
- created_at (when added)
- claimed_at (when started)
- completed_at (when done)

---

## Common Patterns

### Pattern 1: Investigation → Implementation
```
001-investigate-approach.md (2h, research)
002-implement-solution.md (4h, build)
003-test-and-document.md (2h, validate)
```

### Pattern 2: Parallel Independent Tasks
```
001-update-frontend.md (can run parallel)
002-update-backend.md (can run parallel)
003-integrate-both.md (depends on 001, 002)
```

### Pattern 3: Documentation Sprint
```
001-audit-current-docs.md
002-update-architecture.md
003-create-missing-adrs.md
```

---

## Best Practices

1. **Write prompts when planning**, not when executing
2. **Include verification criteria** - be specific
3. **Reference GitHub issues** for traceability
4. **Specify deliverable paths** explicitly
5. **Keep prompts focused** - one concern per prompt
6. **Document dependencies** if order matters

---

## Next Steps

### Immediate (This Sprint)
- Add claim/complete scripts to reduce friction
- Create prompt template file
- Document blocked workflow

### Future Iterations
- Dashboard for queue visualization
- Automatic cycle time metrics
- Dependency graph generation
- Priority-based auto-assignment

---

## Questions?

The system is lightweight but effective. Agents report it "gets out of the way" while providing enough structure for coordination.

Key insight: **This enables true async development** - you can write prompts during planning time, agents execute when available, you review when convenient.

---

*The coordination queue is tested and operational. Use it to reduce synchronous coordination overhead.*
