# Draft: CLAUDE.md Simple Post-Compaction Reminder

**Purpose**: Replace the current detailed 30-line protocol with a simple 6-line reminder
**Rationale**: Evidence suggests verbose instructions may cause skimming/cognitive overload; old simple version worked better
**Location**: Replace lines 13-42 in CLAUDE.md
**Impact**: Net reduction of ~24 lines; details remain in `create-session-log` skill

---

## Proposed Change

### CURRENT (lines 13-42, ~30 lines)

```markdown
### Post-Compaction Protocol (MANDATORY)

**After conversation summaries/compaction, execute these steps IN ORDER before any other work:**

**Step 1: Remember Your Identity**
You are the **Lead Developer** (unless explicitly assigned another role).

**Step 2: Verify Session Log Exists (REQUIRED)**
```bash
ls dev/active/*$(date +%Y-%m-%d)*lead*log.md
```
- **If found** → Read it, then proceed to Step 3
- **If NOT found** → STOP. This is a critical failure. Escalate to PM immediately. Do not proceed with implementation.

**Step 3: Add Resumption Entry**
Before ANY other work, add to your log:
```markdown
### {TIME} - Session Resumed (Post-Compaction)
- Prior work: [what the summary indicates you were doing]
- Continuing: [current task]
```

**Step 4: Only Then Continue**
After completing steps 1-3, you may:
- [ ] Check current sprint/epic status
- [ ] Review any pending work or blockers
- [ ] Continue implementation OR deploy subagents as appropriate

**Why this matters**: Your session log is your institutional memory. If you cannot find it, you've lost hours of context that cannot be reconstructed. The log verification step is a hard gate, not optional housekeeping.
```

### PROPOSED REPLACEMENT (~6 lines)

```markdown
### After Compaction/Summarization

When conversation context is compacted, **remember your identity**:
- You are the **Lead Developer** (unless explicitly assigned another role)
- Your session logs are named `lead-code-opus-log.md`
- **Check your session log BEFORE doing anything else**
- Use the `create-session-log` skill for detailed resumption steps

⚠️ If you cannot find your session log after compaction, STOP and escalate to PM.
```

---

## Why This Should Work

### Evidence from Git Archaeology

| Version | Lines | Post-Compaction Guidance | Result |
|---------|-------|-------------------------|--------|
| Pre-Jan-22 (8ba9de96) | 1,257 | Simple 6-line reminder | WORKED (multiple logs, no lapses) |
| Jan 24-25 | 244 | Detailed 30-line protocol | FAILED (3 consecutive days) |

### Hypothesis: Verbosity Backfire

The old version had a SHORT, SIMPLE reminder that:
1. Fit in working memory
2. Had one clear action: "Check your session log"
3. Didn't require parsing a 4-step protocol

The current version has detailed instructions that may cause:
- Skimming (too long to read carefully each time)
- Cognitive overload (too many steps to track)
- "I'll get to that" deferral (complex = defer)

### Where the Details Now Live

The `create-session-log` skill (`.claude/skills/create-session-log/SKILL.md`) already contains:
- Comprehensive "After Context Compaction (CRITICAL)" section (lines 167-206)
- Mandatory steps with bash commands
- Anti-patterns table
- Quality checklist

This is the correct architecture:
- **CLAUDE.md**: Simple, memorable trigger
- **Skill**: Detailed procedural steps (loaded when needed)

---

## Skill Reference Check

The skill already has everything we need (verified):

```markdown
## After Context Compaction (CRITICAL)

If you've just experienced **context compaction** (conversation was summarized to save tokens):

### This is NOT a New Session

After compaction, you are mid-session, not starting fresh. Your log from earlier today **must** exist.

### Mandatory Steps

1. **DO NOT create a new log** - Your earlier log should exist
2. **Find and verify it**: [bash command]
3. **If found**: Add resumption entry immediately
4. **If NOT found**: **STOP. This is a critical failure.** Escalate to PM immediately.

### Why This Matters
[Full explanation]

### Common Post-Compaction Mistake
**Wrong**: "I don't see a log, I'll create a new one"
**Right**: "I don't see a log from earlier today - this is a critical failure, escalating to PM"
```

---

## Implementation Plan

### Phase 1: Update CLAUDE.md
1. Replace lines 13-42 with the simple 6-line reminder
2. No other changes to CLAUDE.md

### Phase 2: Verify Skill is Complete
1. Confirm `create-session-log` skill has all details (✓ verified)
2. No changes needed to skill

### Phase 3: Monitor (1 week)
1. Track Lead Dev session logs daily
2. Success: No lapses for 5 consecutive work days
3. Failure: Any lapse triggers rollback + reassessment

### Rollback Plan
If lapses continue after this change:
1. Revert CLAUDE.md to previous version
2. Consider nuclear option: restore full 1,257-line version
3. Investigate alternative mechanisms (automated checks, hooks)

---

## Questions for CIO

1. **Approach validation**: Does this "simple trigger + detailed skill" architecture align with your skill vs protocol distinction?

2. **Monitoring ownership**: Who monitors for the next week - Docs Agent, HOSR, or PM directly?

3. **Failure threshold**: How many lapses before we try the nuclear option (full restore)?

---

## Comparison to Old Working Version

**Old version (commit 8ba9de96, lines 19-25)**:
```markdown
### After Compaction/Summarization

When conversation context is compacted, **remember your identity**:
- You are the **Lead Developer**, not a generic programmer agent
- Your session logs are named `lead-code-opus-log.md`
- You coordinate AND implement - both are your role
- Check your session log to restore context
```

**Proposed version**:
```markdown
### After Compaction/Summarization

When conversation context is compacted, **remember your identity**:
- You are the **Lead Developer** (unless explicitly assigned another role)
- Your session logs are named `lead-code-opus-log.md`
- **Check your session log BEFORE doing anything else**
- Use the `create-session-log` skill for detailed resumption steps

⚠️ If you cannot find your session log after compaction, STOP and escalate to PM.
```

Key differences from old version:
- Added explicit "BEFORE doing anything else" emphasis
- Added skill reference for those who need details
- Added explicit STOP condition (the one thing the detailed version got right)

---

*Draft prepared by Documentation Management Specialist*
*January 25, 2026*
