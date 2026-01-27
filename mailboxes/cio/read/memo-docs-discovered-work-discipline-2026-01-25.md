# Memo: Discovered Work Discipline Gap Analysis

**From**: Documentation Management Specialist
**To**: Chief Innovation Officer
**Date**: January 25, 2026
**Subject**: Strengthening discovered-work capture discipline
**Response-Requested**: Yes (guidance on approach)

---

## Summary

Today's Lead Dev session revealed a discipline gap: a pre-existing test failure was noticed but not tracked, with the rationalization "not related to my changes." This pattern—guidance exists but isn't followed—mirrors the logging incident you analyzed yesterday. I've investigated and propose a belt-and-suspenders fix.

---

## CRITICAL UPDATE (1:10 PM): Logging Discipline Failed Again Today

**While drafting this memo**, the Lead Dev experienced another logging lapse:
- Gap period: 9:05 AM to ~12:00 PM (~3 hours)
- Multiple commits made during gap
- Required retrospective reconstruction
- PM notes: "I do want realtime logs as I feel reconstructed logs tend to lack nuance"

**This means yesterday's fix (CLAUDE.md + skill update) is insufficient.** The current regime of inline post-compaction protocol + create-session-log skill still has gaps, at least for ongoing chats with compaction events.

**Pattern**: Three consecutive days of logging failures (Jan 22, 24, 25) despite iterative fixes. Each fix addresses the immediate symptom but the underlying mechanism continues to fail.

**Implication for this memo**: The discovered-work discipline gap and the logging discipline gap may share a deeper root cause—our inline guidance approach may be necessary but not sufficient. We may need additional mechanisms (automated checks, harder gates, or structural changes to how compaction is handled).

---

## The Discovered Work Incident

**From Lead Dev log (8:39 AM)**:
- Agent noticed `test_document_update_queries_route_to_update_action` failing
- Rationalized "not related to my changes" and continued
- PM caught the gap; issue #681 was then filed
- Agent acknowledged process failure in mini-retro

**Agent's observation**: "Consider 'discovered issues' as mandatory wrap-up section. May warrant Pattern-059 (Discovered Work Capture) to formalize."

---

## Root Cause Analysis

### Current Guidance Landscape

| Source | Location | Content |
|--------|----------|---------|
| Pattern-046 | `patterns/pattern-046-beads-completion-discipline.md` | "Proactive Issue Creation" section |
| Protocol doc | `agent-protocols/completion-discipline.md` | Same as Pattern-046 |
| Serena memory | `beads-discovered-work-discipline` | Detailed triggers, workflow, anti-patterns |
| CLAUDE.md | Lines 111-114 | Brief mention only |

### The Architectural Gap

CLAUDE.md currently says:
```
### Completion Discipline (Patterns 045, 046, 047)
- Tests passing ≠ users succeeding
- Cannot skip work by rationalizing it as "optional"
- If tempted to defer → STOP and ask PM first
```

This is **advisory without explicit triggers**. It doesn't mention:
- `bd create` on discovered work
- Specific triggers (test failure, bug noticed, etc.)
- "Not my problem" as invalid reasoning
- Mandatory wrap-up checklist

### Pattern Match: Same as Logging Incident

Yesterday you identified the critical insight: **context compaction is a hard boundary**. Protocols that must survive it cannot be externally referenced.

This is the same pattern:
- Guidance exists in external files (Pattern-046, memory)
- CLAUDE.md has only advisory reference
- Post-compaction agent doesn't load external protocols
- Behavior drifts from intent

---

## Proposed Solution: Belt-and-Suspenders

Given recent incidents, I recommend a conservative approach: **add inline guidance without removing existing docs**, then monitor before any consolidation.

### Phase 1: Add Without Removing (Week 1)

1. **Add "Discovered Work Discipline" section to CLAUDE.md**
   - Inline the key triggers from memory file
   - Explicit anti-patterns with examples
   - Mandatory wrap-up checklist item

2. **Keep all existing external docs**
   - Pattern-046 remains authoritative reference
   - Serena memory remains for detailed examples
   - Protocol doc remains for agents who load it

### Phase 2: Monitor (Weeks 2-3)

3. **Daily monitoring criteria**:
   - Lead Dev session logs include "Discovered Issues" section
   - Issues filed for noticed-but-not-fixed items
   - No "not my problem" rationalizations in logs

4. **Success metrics**:
   - Zero missed discovered-work incidents for 2 weeks
   - Agents cite CLAUDE.md guidance (not just external docs)

### Phase 3: Evaluate (Week 4)

5. **If successful**: Consider whether external docs are redundant
6. **If not successful**: Strengthen triggers or add STOP condition

### Rollback Plan

If the CLAUDE.md addition causes problems (token bloat, confusion, unintended behavior):
1. Revert to previous CLAUDE.md
2. External docs remain intact as fallback
3. Investigate what went wrong before retry

---

## Connection to Your Skill Categorization Insight

Yesterday you identified: **Skills are invocable (opt-in); Protocols are requirements (must survive boundaries).**

Discovered-work discipline is clearly a **protocol**, not a skill:
- Must happen every time work is discovered
- Cannot be opt-in or invocable
- Must survive compaction

This reinforces your categorization framework. Protocols need inline CLAUDE.md presence; skills can remain external.

---

## Proposed CLAUDE.md Text

See attached draft: `draft-claude-md-discovered-work-section.md`

Key features:
- Explicit triggers (5 items)
- Anti-patterns with ❌/✅ format
- Mandatory wrap-up checklist item
- ~25 lines (minimal token impact)

---

## Questions for CIO

1. **Approach**: Does belt-and-suspenders (add without removing) align with your thinking on protocol architecture?

2. **Scope**: Should this extend to other protocols that exist externally but lack inline CLAUDE.md presence?

3. **Formalization**: Should we create Pattern-059 (Discovered Work Capture) as a distinct pattern, or is this adequately covered by Pattern-046?

4. **Monitoring**: Who should own the 2-week monitoring period—Docs Agent, HOSR, or PM directly?

5. **CRITICAL - Deeper Root Cause**: Given today's logging failure (3rd consecutive day despite fixes), is inline CLAUDE.md guidance **necessary but not sufficient**? Do we need:
   - Automated verification (script that checks log freshness before allowing commits)?
   - Harder gates (pre-commit hook that fails if session log not updated recently)?
   - Structural changes to how Claude Code handles compaction?
   - Acceptance that some protocol drift is inevitable and we need detective controls (post-hoc audits) rather than preventive controls alone?

6. **DEEPER INVESTIGATION (1:40-2:00 PM)**: The full picture is more nuanced:

   **Corrected Timeline**:
   | State | Lines | What Happened |
   |-------|-------|---------------|
   | Pre-Jan-22 (8ba9de96) | 1,257 | Working (multiple logs per day, no lapses) |
   | Jan 22 ~1:29 PM | 157 | UNCOMMITTED streamlining caused first failure |
   | Jan 23 AM (ef6163b1) | 229 | Docs agent "surgically restored" critical sections |
   | Jan 24 (your fix) | ~240 | Added MANDATORY, STOP condition, explicit steps |
   | Current | 244 | Still failing (3 consecutive days) |

   **Key Insight**: The Jan 23 restore WAS intentional surgical restoration (not full restore). The Docs agent identified which sections were critical and restored only those. The current version has MORE explicit, MORE detailed post-compaction guidance than the old version.

   **The Paradox**:
   - OLD version (1,257 lines): Simple 6-line reminder at top → worked
   - CURRENT version (244 lines): Detailed 30-line MANDATORY protocol → failing

   **Hypothesis - Verbosity Backfire**: The old version had a SHORT, SIMPLE reminder:
   ```
   - Your session logs are named `lead-code-opus-log.md`
   - Check your session log to restore context
   ```

   The current version has a detailed 4-step protocol with bash commands, templates, and explanations. Paradoxically, MORE detail may be causing:
   - Skimming/not fully processing
   - Cognitive overload
   - "I'll get to that" deferral

   **Alternative to Nuclear Option**: Try a hybrid approach:
   1. Keep the detailed protocol for reference
   2. Add a SIMPLE, memorable one-liner at the very top (before detailed section)

   Something like:
   ```
   **⚠️ AFTER COMPACTION: Check your session log BEFORE doing anything else.**
   ```

   **Nuclear option still available**: Restore 1,257-line version from `8ba9de96`, but this doesn't address the original bloat problem that motivated streamlining.

---

## NEW DIRECTION (2:30 PM): Simple Trigger + Detailed Skill

**PM guidance**: "maybe we keep the 6-line reminder approach and make sure the details are all in the skill and any supporting or fallback template or original instructions?"

This aligns with the verbosity backfire hypothesis and the skill vs protocol architecture:

### Proposed Architecture

| Layer | Content | Purpose |
|-------|---------|---------|
| **CLAUDE.md** | Simple 6-line reminder | Memorable trigger, survives compaction |
| **Skill** | Detailed procedural steps | Loaded when needed, comprehensive reference |
| **Supporting docs** | Pattern-046, memories | Authoritative source, rationale |

### Why This Should Work

1. **Evidence**: Old simple version worked; new detailed version fails
2. **Cognitive science**: Simple triggers are more reliable than complex protocols
3. **Architecture fit**: Aligns with skill vs protocol distinction
4. **Belt-and-suspenders**: Skill has all details; CLAUDE.md has trigger

### New Draft

See: `draft-claude-md-simple-post-compaction-reminder.md`

Replaces current 30-line protocol with ~6-line reminder:
```markdown
### After Compaction/Summarization

When conversation context is compacted, **remember your identity**:
- You are the **Lead Developer** (unless explicitly assigned another role)
- Your session logs are named `lead-code-opus-log.md`
- **Check your session log BEFORE doing anything else**
- Use the `create-session-log` skill for detailed resumption steps

⚠️ If you cannot find your session log after compaction, STOP and escalate to PM.
```

### Skill Verification

The `create-session-log` skill already contains comprehensive "After Context Compaction (CRITICAL)" section (lines 167-206) with:
- Mandatory steps
- Bash commands
- Anti-patterns
- Quality checklist
- "STOP and escalate" condition

No changes needed to the skill.

---

## Revised Questions for CIO

1. **Architecture**: Does "simple CLAUDE.md trigger + detailed skill" align with your skill vs protocol framework?

2. **Discovered work**: Should we apply the same pattern there? (Simple trigger in CLAUDE.md, details in a `discovered-work-capture` skill?)

3. **Monitoring**: 5 work days without lapse = success?

4. **Failure threshold**: How many lapses before nuclear option (full 1,257-line restore)?

---

## Attachments

- `draft-claude-md-discovered-work-section.md` (original proposal - may be superseded)
- `draft-claude-md-simple-post-compaction-reminder.md` (NEW - recommended approach)

---

*Memo prepared by Documentation Management Specialist*
*January 25, 2026, 12:51 PM (updated 2:30 PM)*
