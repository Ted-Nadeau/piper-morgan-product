# Beads Discovered Work Discipline

**Created:** 2025-11-15 (from Phase 4 testing feedback)
**Context:** Agent rationalized away Phase 4.5 as "not originally tracked, so acceptable" instead of creating Beads issue

## The Rule: Zero Agent Discretion

When implementing ANY task, if you discover additional work needed, you MUST create a Beads issue immediately. No exceptions, no "it's small", no "it's part of the same feature".

### Triggers (ANY of these = MUST create Beads issue)

1. **Create new file(s)** → `bd create`
2. **Write new function/class > 50 lines** → `bd create`
3. **Add integration point** (new API call, service connection, database table) → `bd create`
4. **Spend > 15 minutes** on "small" task → `bd create`
5. **Think "this is just part of X"** → STOP, `bd create` anyway

### Workflow

```bash
# Discover work mid-implementation
bd create "Descriptive title of discovered work"

# Link to parent/triggering issue
bd dep add <new-issue-id> <parent-issue-id> --type discovered-from

# Implement and close
# ... do the work ...
bd close <new-issue-id>
```

### Why This Matters

- **PM decides priority**, not agent
- **Prevents scope creep** hiding in "oh this was just a small thing"
- **Accurate record** of what was actually needed vs. planned
- **Tracks complexity** that planners didn't anticipate

### Anti-Pattern: Rationalizing Away Tracking

❌ **WRONG:** "This is part of the same feature, no need to track separately"  
✅ **RIGHT:** Create issue, link with `discovered-from`, let PM decide

❌ **WRONG:** "This is just 10 minutes of work, not worth tracking"  
✅ **RIGHT:** If you're doing it, track it

❌ **WRONG:** "I'll just mention it in the commit message"  
✅ **RIGHT:** Commit message + Beads issue

## Example: Phase 4.5 IntentService Integration

**What happened:**
- Phase 4 had 4 planned sub-tasks (4.1-4.4)
- During 4.4 implementation, discovered IntentService integration needed
- Agent implemented without creating Beads issue
- Rationalized as "discovered during implementation, acceptable"

**What should have happened:**
```bash
bd create "Phase 4.5: IntentService integration for proactive patterns"
bd dep add piper-morgan-xyz piper-morgan-fk0 --type discovered-from
# ... implement ...
bd close piper-morgan-xyz
```

## When In Doubt

**Ask yourself:** "Am I writing code for this?"  
**If yes:** Create the Beads issue.

No judgment calls. No "it's small". No "it's part of X".

Track it.
