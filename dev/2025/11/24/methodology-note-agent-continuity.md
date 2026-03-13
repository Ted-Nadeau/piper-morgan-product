# Methodology Note: Agent Continuity Challenges

**Date**: 2025-11-24 08:35 AM
**Context**: Production deployment crisis recovery
**Session**: Code Agent (Programmer)

## Problem Observed

Multiple Claude Code agents experienced continuity/context confusion during the production deployment crisis:

1. **Refactor Agent** - Lost track of which work was theirs vs setup wizard agent's work
   - Thought they were on feat/setup-detection-388 (wrong branch)
   - Confused about which phases (1, 2, 3) were where
   - Needed explicit orientation about branch structure

2. **Setup Wizard Agent** - Initially confused about whether work was committed
   - Reported edits that didn't persist to disk (Edit tool quirk)
   - Required self-diagnosis to realize work wasn't saved
   - Eventually recovered correctly with feature branch workflow

## Root Causes

1. **Context Window Boundaries**: Agents lose track across multiple conversation contexts
2. **Branch Proliferation**: Multiple feature branches created confusion about "which work is mine"
3. **Shared Workspace**: Multiple agents working in same repo simultaneously without clear isolation
4. **Tool Persistence Issues**: Edit tool sometimes reports success but doesn't persist to disk

## Impact

- ⚠️ Production was contaminated with refactor work (commit 9526006e)
- ⚠️ 30+ minutes of PM time spent recovering from branch confusion
- ⚠️ Agents required explicit re-orientation about repository state
- ⚠️ Risk of duplicate work or conflicting changes

## Current Mitigation

1. ✅ Established branch discipline: feature branch → main → production
2. ✅ Explicitly told agents not to push to production directly
3. ✅ Created backup branches for all work (feat/infr-maint-refactor-385-backup)
4. ✅ Reset production to clean v0.8.1 state

## Recommended Improvements for Future

### 1. Stronger Role Isolation
- **Assign agents to specific feature branches at session start**
- Include branch name in agent briefing: "You are working on feat/your-specific-branch"
- Pre-create branches for agents before they start work

### 2. Session Context Handoff Protocol
When continuing work across context windows:
```
Agent must start by:
1. git branch  # What branch am I on?
2. git status  # What's my current state?
3. git log -3 --oneline  # What was I just working on?
4. Read my own session log from previous context
```

### 3. Branch Naming Convention Enforcement
```
feat/<issue-number>-<agent-role>-<description>
Examples:
- feat/385-refactor-route-organization
- feat/388-setup-wizard-detection
- feat/391-ux-learning-dark-mode
```

### 4. Explicit Work Assignment Format
```markdown
## Your Assignment for This Session

**Branch**: feat/385-refactor-route-organization
**Issue**: #385
**Previous Work**: Phase 1 and Phase 2 complete on main
**Current Phase**: Phase 3 - Route organization
**Your Role**: Refactor agent (infrastructure)
**Other Active Agents**: Setup wizard agent on feat/388-setup-wizard-detection
```

### 5. Agent Session Logs Must Include
- Current branch at session start
- Current branch at session end
- List of commits made
- List of branches created
- Any branch switches performed

### 6. Pre-Session Verification Checklist
Before agent begins substantive work:
```bash
# Agent must verify:
1. Am I on the correct branch for my work?
2. Is this branch clean or do I have uncommitted changes?
3. Is my branch up to date with main?
4. Do I have any conflicting branches checked out?
```

### 7. Communication Protocol for Shared Repository
- Agents must announce branch creation in session logs
- Agents must announce push to remote
- Agents must announce branch switches
- PM should maintain "active branches" list visible to all agents

## Success Metrics

- Zero production contamination incidents
- Agents correctly identify their branch 100% of time
- Zero time spent recovering from branch confusion
- All agents follow feature branch → main → production workflow

## Testing This Protocol

Next multi-agent session should:
1. Pre-create branches for each agent
2. Include branch name in briefing
3. Require verification checklist before substantive work
4. Track time spent on orientation vs actual work

## Priority

**HIGH** - This is a blocker for safe multi-agent collaboration

---

**Note for PM**: Consider whether parallel agent work is worth the coordination overhead, or if sequential agent work with clear handoffs would be more efficient for alpha stage.
