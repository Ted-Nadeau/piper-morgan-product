# Agent Coordination Patterns - MANDATORY

## Strategic Agent Deployment

### Claude Code Deployment
Best for:
- Multi-file systematic changes
- Test creation and infrastructure
- Architecture and design work
- Pattern discovery across codebase

```bash
# Code deployment template:
Please implement [task] following our systematic methodology.

VERIFY FIRST:
1. [specific verification commands]
2. [pattern discovery commands]

OBJECTIVE: [clear single goal]

SUCCESS CRITERIA: [measurable outcome]
```

### Cursor Deployment
Best for:
- Targeted single-file fixes
- UI testing and debugging
- Quick iterations with verification
- Documentation updates

```bash
# Cursor deployment template:
Please fix [specific issue] with TDD approach.

MANDATORY VERIFICATION:
1. [exact test to write]
2. [exact file to modify]

NO ASSUMPTIONS - verify everything.
```

## Coordination Protocol
1. Create GitHub issue FIRST
2. Assign to appropriate agent
3. Monitor progress via commits
4. Verify completion with evidence
5. Update tracking documents
