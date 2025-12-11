# Special Assignments Session Log
**Date**: 2025-12-04
**Agent**: spec-code-opus (Special Assignments Agent)
**PM**: xian

---

## Session Objective

Research and recommend approaches for making beads usage more routine for Code agents.

## Status

- **Started**: 2025-12-04 ~05:32 PST
- **Current Phase**: Research complete, drafting recommendations

---

## Session Timeline

### 05:32 - Session Start

- Initialized session log
- Awaiting reference material on beads integration options from PM

### 05:35 - Reference Material Received

PM shared two approaches from Medium thread:
1. **Havriil Pietukhin**: Use Claude Code hooks + `bd onboard` prompt injection via `settings.local.json`
2. **Nicholas Hirsch**: Modular `.agents/*.md` approach with dedicated beads.md guide

### 05:40 - Research Phase

**Current State Analysis:**
- `.claude/settings.json` - has permissions, no hooks
- `.claude/settings.local.json` - has `"*"` permissions, no hooks, no bd onboard prompt
- `CLAUDE.md` - has extensive bd instructions (~80 lines in "BEADS COMPLETION DISCIPLINE" section)
- `.cursor/rules/` - 5 rule files, no beads-specific content
- `dev/2025/09/21/AGENTS.md` - old file, not in active use
- No `.agents/` directory exists
- Serena memory `beads-discovered-work-discipline` exists with detailed rules

**Hook Research (Claude Code Guide):**
- 10 hook events available
- `UserPromptSubmit` - fires before Claude processes user input (best for prompt injection)
- `SessionStart` - fires at session initialization (good for context loading)
- Hooks configured in `.claude/settings.json` under `"hooks"` key
- Can use `type: "command"` to run scripts or `type: "prompt"` for LLM-based decisions

**`bd onboard` Command Output:**
- Outputs comprehensive AGENTS.md content for beads workflow
- Includes issue types, priorities, workflow steps, MCP server setup
- Designed as one-time bootstrap instruction

---

## Research Findings

### Approach A: Hook-Based Prompt Injection (Havriil's approach)

**Mechanism:**
```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo 'Before starting any work, run bd onboard to understand the current project state and available issues.'"
      }]
    }]
  }
}
```

**Pros:**
- Automatic - no agent memory required
- Works every session
- Lightweight (just a reminder)

**Cons:**
- `bd onboard` outputs ~150 lines of AGENTS.md template - not what we want
- We already HAVE beads instructions in CLAUDE.md
- Would create confusion between existing instructions and `bd onboard` output
- `bd onboard` is designed for projects WITHOUT existing beads setup

### Approach B: Modular `.agents/*.md` (Nicholas's approach)

**Mechanism:**
- Break CLAUDE.md into focused guides in `.agents/`
- Create `.agents/beads.md` by having agent study beads repo
- Point AGENTS.md → `.agents/*`
- Point CLAUDE.md → AGENTS.md

**Pros:**
- Modular, maintainable
- Agent-generated from source (accurate)
- Cleaner separation of concerns

**Cons:**
- Significant refactoring of our current setup
- We already have working beads instructions in CLAUDE.md
- Token cost of loading multiple files vs. single CLAUDE.md
- Cursor/AGENTS.md adds another layer of indirection

### Approach C: What We Actually Have (Current State)

**Current beads integration:**
1. `CLAUDE.md` lines 640-725: Complete beads workflow documentation
2. Serena memory `beads-discovered-work-discipline`: Detailed discovered-work rules
3. `.claude/settings.local.json`: bd commands pre-approved (`bd status`, `bd list`, `bd create`, `bd sync`, `bd show`, `bd close`)

**Problem identified:**
- Instructions are there but agents don't consistently use them
- No automatic reminder at session start
- Relies on agent reading and remembering CLAUDE.md

---

## Recommendations

### Recommended: Hybrid Approach (Minimal Change)

Add a **SessionStart hook** that outputs a brief reminder, NOT the full `bd onboard`:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo '📋 BEADS REMINDER: Run \"bd ready --json\" to check available work before starting. See CLAUDE.md \"BEADS COMPLETION DISCIPLINE\" section for workflow.'"
      }]
    }]
  }
}
```

**Why this works:**
1. Zero refactoring of existing CLAUDE.md
2. Automatic reminder every session
3. Points to existing documentation (not duplicate)
4. bd commands already permitted in settings.local.json
5. Works for both Claude Code and Cursor (via .cursor/rules/ equivalent)

### Optional Enhancement: Cursor Rule

Create `.cursor/rules/beads-workflow.mdc`:
```markdown
---
description: Beads issue tracking workflow
globs: ["**/*"]
alwaysApply: true
---
# BEADS WORKFLOW REMINDER
Run `bd ready --json` at session start to check available work.
See CLAUDE.md "BEADS COMPLETION DISCIPLINE" section for complete workflow.
```

### NOT Recommended

1. **`bd onboard` prompt injection** - Wrong tool; it's for bootstrapping, not ongoing use
2. **Full `.agents/*.md` refactor** - Too much change for unclear benefit
3. **Duplicate beads.md guide** - We already have comprehensive instructions

---

### 05:47 - Brainstorming Session: Other Useful Hooks

PM asked: What other recurring issues might benefit from session-start reminders?

**Candidate Hooks (based on CLAUDE.md pain points and Serena memories):**

| Hook | Purpose | Evidence of Need |
|------|---------|------------------|
| **Beads reminder** | Check `bd ready` before starting | Agents forget to use beads workflow |
| **Context7 for syntax** | Use Context7 MCP before guessing library APIs | Agents hallucinate API syntax |
| **Serena for codebase** | Use Serena before reading full files | Agents wastefully read entire files |
| **Feature branch check** | Verify not on `main` | Lines 759-767: Critical rule, easy to forget |
| **TodoWrite vs Beads** | Remind of distinction | Serena memory shows recurring confusion |
| **Pre-commit script** | Remind about `./scripts/fix-newlines.sh` | Line 26: ALWAYS before committing |

**Proposed SessionStart Hook Bundle:**

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "echo '🚀 SESSION CHECKLIST:\n• Run \"bd ready --json\" for available work\n• Use Context7 MCP for library syntax (not guessing)\n• Use Serena for codebase exploration (not reading full files)\n• Verify you are NOT on main branch\n• Run ./scripts/fix-newlines.sh before commits'"
      }]
    }]
  }
}
```

**Alternative: Minimal vs Comprehensive**

Option A - **Minimal (just beads)**:
```
📋 Run "bd ready --json" before starting.
```

Option B - **Focused (top 3 issues)**:
```
🚀 SESSION START:
• bd ready --json (check available work)
• Context7 for library APIs (don't guess)
• Verify NOT on main branch
```

Option C - **Comprehensive (5 reminders)**:
Full checklist above.

**Trade-off**: More reminders = more noise. May want to start minimal and add only if specific issues recur.

---

### 06:32 - Implementation & Coordination Research

**SessionStart Hook Implemented:**

Added to `.claude/settings.json`:
```json
"hooks": {
  "SessionStart": [
    {
      "hooks": [
        {
          "type": "command",
          "command": "echo '🚀 SESSION START REMINDERS:\n• Run \"bd ready --json\" to check available work\n• Use Context7 MCP for library APIs (don't guess syntax)'"
        }
      ]
    }
  ]
}
```

**Coordination System Research:**

Two separate systems exist:

1. **`coordination/` directory** - Async Prompt Queue (file-based)
   - `manifest.json` tracks prompts with status: available → claimed → complete
   - Agents claim work by updating manifest + moving files
   - 3 prompts completed so far, 0 currently available
   - No branch management - works on current branch
   - Simple file locking via claim/complete workflow

2. **`methodology/coordination/`** - MandatoryHandoffProtocol (code-based)
   - Python enforcement system for agent-to-agent handoffs
   - Tracks `github_branch` in HandoffContext (line 79)
   - AgentType enum: CODE, CURSOR, ARCHITECT
   - Verification pyramid with evidence requirements
   - More sophisticated but not actively integrated with queue

**Key Finding: Branch Management Gap**

Neither system currently enforces branch coordination:

- `coordination/manifest.json` has no branch field
- `methodology/coordination/handoff.py` has `github_branch` field but it's optional
- CLAUDE.md assumes "one agent = one feature branch" model
- Reality: multiple agents share one working directory on your laptop

**The Multi-Agent-Single-Machine Problem:**

| Distributed Model (CLAUDE.md assumes) | Your Reality |
|---------------------------------------|--------------|
| Agent A on branch-A, Agent B on branch-B | All agents share one git state |
| Each agent pushes to own branch | Push conflicts if agents diverge |
| Git isolates work naturally | File queue + discipline required |

**Options for Discussion:**

1. **Accept single-branch model**: All agents work on `main` or a shared dev branch, queue serializes work
2. **Stash-based switching**: Agents stash before switching, restore after (fragile)
3. **Worktree per agent**: `git worktree add` creates separate directories per branch (more complex setup)
4. **Current approach works**: If queue serializes effectively, branch isolation may be unnecessary overhead

---

### 07:09 - Plan Mode: Git Worktrees Integration

PM requested thorough planning for:
1. Adopting git worktrees for agent isolation
2. Reviewing both coordination systems
3. Recommending how they should work together
4. Tactical first step to connect existing elements

**Three parallel explore agents deployed:**
- Coordination queue system exploration
- MandatoryHandoffProtocol exploration
- Git worktrees research (web + codebase)

**Plan agent synthesized findings into implementation plan.**

**PM Decisions (via AskUserQuestion):**
- Naming: Hybrid `.trees/<prompt-id>-<short-session>/`
- Cleanup: After PM review
- Enforcement: Start advisory
- Scope: Phase 0-2 only (scripts + schema)

Plan file: `/Users/xian/.claude/plans/recursive-sauteeing-rose.md`

---

### 08:00 - Implementation: Phase 0-2 Complete

**Phase 0: Infrastructure**
- [x] `.gitignore` - Added `.trees/` entry
- [x] `.trees/README.md` - Documentation

**Phase 1: Shell Scripts**
- [x] `scripts/worktree-setup.sh` - Creates isolated worktree + updates manifest
- [x] `scripts/worktree-teardown.sh` - PM-controlled cleanup
- [x] `scripts/worktree-status.sh` - Shows all active worktrees
- [x] `coordination/QUEUE-README.md` - Updated with worktree workflow

**Phase 2: Schema Extension**
- [x] `coordination/manifest.json` v1.1.0
  - Added: `branch_name`, `worktree_path`, `worktree_created_at`, `cleanup_approved`
  - Backfilled existing prompts with null values

**GitHub Tracking:**
- Epic: #463 (FLY-COORD-TREES: Git Worktrees for Multi-Agent Coordination)
- Phase 0-2: #464 (MVP - Complete)
- Phase 3-5: #465 (Future Python Integration - Deferred to MVP milestone)

**Memo Written:**
- `docs/internal/architecture/current/memos/2025-12-04-worktree-coordination-memo.md`
- For Chief Architect and Lead Developer

---

## Session Summary

### Morning (05:32 - 06:32): Beads Integration Research
- Researched Claude Code hooks mechanism
- Evaluated `bd onboard` and `.agents/*.md` approaches
- Implemented SessionStart hook with beads + Context7 reminders
- Discovered branch management gap in coordination systems

### Late Morning (07:09 - 12:15): Git Worktrees Implementation
- Comprehensive research via explore agents
- Plan mode planning with PM decisions
- Implemented Phase 0-2 (scripts + schema)
- Created GitHub epic and child issues
- Wrote architecture memo

### Deliverables

| Deliverable | Location |
|-------------|----------|
| SessionStart hook | `.claude/settings.json` |
| Worktree scripts | `scripts/worktree-*.sh` |
| Schema extension | `coordination/manifest.json` v1.1.0 |
| Documentation | `.trees/README.md`, `coordination/QUEUE-README.md` |
| Architecture memo | `docs/internal/architecture/current/memos/2025-12-04-worktree-coordination-memo.md` |
| GitHub tracking | #463, #464, #465 |

---

### Afternoon: Pilot Observation & Template Iteration

### 12:21 - Pilot Planning

PM identified #462 (UI dialog fixes) and #466 as pilot candidates for worktree workflow.

### 13:23 - Pilot Observation Mode

PM: "we are piloting it now... you are welcome to read (without intervening, of course)"

Observed Lead Dev session working on #462 and #455/#456 auth fixes.

### 13:41 - Pilot Evidence Check

**Findings:**
- Worktree status: 0 agent worktrees in `.trees/`
- #462 commits: 4 commits directly to main/production (no worktree isolation)
- Manifest: No worktree_path entries

**Conclusion:** Worktree workflow was not used for this pilot.

### 13:51 - Lead Dev Feedback Received

Lead Dev provided honest reflection:
- Task was small (5 files, 15 min) - worktrees would add overhead
- No parallel agents deployed
- Time pressure (PM testing blocked)

**Key Insight:** Worktrees designed for parallel work, not sequential single-agent tasks.

**Recommendation from Lead Dev:**
1. Identify next suitable task for true pilot, OR
2. Defer until naturally larger task emerges

**My Recommendation:** Option 2 - let it emerge naturally. Add guidance to gameplan template so architects can assess "worktree candidate?" during planning.

### 13:51 - Gameplan Template Iteration

PM approved proposing template iteration with worktree guidance.

**Proposed Addition:** New section in Phase -1 for worktree assessment criteria.

### 14:00 - Template v9.2 Applied

- Updated `knowledge/gameplan-template.md` to v9.2
- Added Part A.2: Work Characteristics Assessment
- Archived to `knowledge/versions/gameplan-template-v9.2.md`
- PM to upload to project knowledge for cloud agents

---

## Notes

*12:15 - Morning session objectives complete. Phase 0-2 implemented, documented, and tracked.*

*13:51 - Afternoon: Pilot did not use worktrees (appropriate for small task). Proposing gameplan template iteration with worktree guidance.*
