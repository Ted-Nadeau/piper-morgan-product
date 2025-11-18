# TodoWrite vs Beads: When to Use Which

**Created:** 2025-11-15 (from Phase 4 testing feedback)
**Context:** Agent used TodoWrite for bugs instead of creating Beads issues

## The Core Distinction

- **TodoWrite** = Session-scoped planning and progress tracking
- **Beads** = Persistent issue tracking across sessions, creates GitHub issues

## Decision Matrix

### Use TodoWrite When:
✅ Breaking down work WITHIN current session  
✅ Planning implementation steps for current task  
✅ Tracking progress on already-tracked Beads issue  
✅ Session-scoped checklist (gone when session ends)  
✅ "What do I do next in the next 30 minutes?"

### Use Beads When:
✅ **ANY bug discovered** (even "small" ones)  
✅ **ANY feature/enhancement idea**  
✅ **ANY technical debt identified**  
✅ **ANY work that might outlive this session**  
✅ **ANY work that creates/modifies code files**  
✅ "This should be tracked across sessions"

## The Litmus Test

Ask yourself:
1. **"Will this still matter tomorrow?"** → Beads
2. **"Is this a bug/feature/debt?"** → Beads  
3. **"Just planning my steps for the next hour?"** → TodoWrite
4. **"Would PM want visibility into this?"** → Beads

## Examples

| Situation | Tool | Why |
|-----------|------|-----|
| Found bug during testing | **Beads** | Bugs always persist, need tracking |
| Breaking Phase 4.5 into 5 steps | **TodoWrite** | Session planning, ephemeral |
| "TODO: Refactor this later" | **Beads** | Technical debt, future work |
| "Next: write tests, then commit" | **TodoWrite** | Session checklist |
| UX improvement idea | **Beads** | Enhancement request |
| "First check X, then implement Y" | **TodoWrite** | Implementation steps |
| Context matching has None bug | **Beads** | Bug that needs fixing |
| "Now testing scenario 1, 2, 3" | **TodoWrite** | Test execution checklist |

## Real-World Case: Phase 4 Testing (2025-11-15)

**What happened:**
Agent discovered 3 bugs during Phase 4 testing:
1. Duplicate suggestions showing
2. Vague pattern descriptions
3. Wrong "workflow completed" message

Agent initially used TodoWrite to track these.

**What should have happened:**
```bash
bd create "Bug: Duplicate suggestions..." --type bug
bd create "Bug: Pattern description..." --type bug  
bd create "Bug: Workflow completed..." --type bug
bd dep add <each> piper-morgan-fk0 --type discovered-from
```

## Rule of Thumb

**If you're tempted to write `bd create`, just do it.**

TodoWrite is for planning your next steps.  
Beads is for tracking work that needs to get done.

## Anti-Patterns

❌ Using TodoWrite for bugs → Should be Beads  
❌ Using TodoWrite for "fix this later" → Should be Beads  
❌ Using Beads for "step 1, step 2, step 3" → Should be TodoWrite  
❌ Not using either because "it's small" → Use Beads anyway

## Integration

TodoWrite and Beads work together:

```bash
# Beads issue exists
bd show piper-morgan-86n  # Bug: Duplicate suggestions

# Use TodoWrite to plan implementation
TodoWrite: [
  "Read IntentService get_automation_patterns code"
  "Identify where deduplication should happen"  
  "Write deduplication logic"
  "Test with duplicate pattern"
  "Verify only one suggestion shows"
]

# When done
bd close piper-morgan-86n
```

## Summary

- **Bugs/Features/Debt** → Always Beads
- **Session planning** → TodoWrite
- **When in doubt** → Beads (lower cost to create than to lose track)
