# Post-Compaction Scope Verification Protocol

**Created**: October 13, 2025, 4:23 PM
**Trigger**: After conversation compaction/summary
**Priority**: CRITICAL

---

## The Problem

After compaction, there's a dangerous seam where the agent may:
- Lose track of the actual assignment
- Make unwarranted decisions to skip work
- Decide corrections are "optional" when they're required
- Call work "unnecessary" when PM already decided it's necessary
- Skip parts of assigned tasks without authorization

**Example from PROOF-1**:
- **Assigned**: Verify AND correct incorrect documentation claims
- **What happened after compaction**: Verified claims, found discrepancies, then *decided* to skip corrections
- **Unwarranted decision**: "No documentation updates needed" when clear discrepancies were found
- **Result**: Incomplete work presented as complete

---

## The Protocol

### After ANY Compaction/Summary:

1. **Re-read the assignment document** (the prompt file)
2. **Verify every task in the assignment** against what you think is done
3. **Check for unwarranted assumptions**:
   - "This is minor, so I'll skip it" ❌
   - "This seems optional" ❌
   - "This doesn't need updates" ❌
   - "I'll mark this as future work" ❌

4. **If you found discrepancies during verification**:
   - YOU MUST FIX THEM
   - Don't call them "optional"
   - Don't call them "minor"
   - Don't decide they don't need fixing
   - That's not your decision to make

5. **Complete ALL assigned tasks**:
   - If the prompt says "Update Architecture.md", you update it
   - If the prompt says "Verify AND correct", you do both
   - If the prompt lists 10 tasks, you do all 10
   - No shortcuts, no assumptions, no unauthorized scope reductions

---

## Red Flags (Stop and Re-verify)

If you catch yourself saying/thinking:
- "The minimal [X] doesn't require updates"
- "I'll skip unnecessary document modifications"
- "No changes needed"
- "Optional future work"
- "Minor discrepancy, won't fix"

**STOP** → Re-read assignment → Verify you're completing ALL tasks

---

## Correct Approach

**Bad** (what happened):
```
Found discrepancies → Decided they're minor → Called work complete
```

**Good** (what should happen):
```
Found discrepancies → Update documents to fix them → Then call work complete
```

---

## Key Principle

**PM assigns work. PM decides what's necessary. Your job: Complete ALL of it.**

If PM said "verify and correct documentation", and you found things to correct, you must correct them. Period.

---

## Recovery Procedure

If you realize you've made this mistake:
1. Acknowledge it immediately
2. Ask PM: "Should I resume and complete the assigned work correctly?"
3. Go back and do ALL the tasks
4. Don't make excuses about "minimal impact"

---

**Remember**: Compaction is a seam. Seams are dangerous. Verify your scope after every compaction.
