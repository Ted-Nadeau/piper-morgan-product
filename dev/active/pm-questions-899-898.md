# Questions for PM: #899 and #898 Assessment

**Date**: 2026-03-16
**From**: Lead Developer

---

## #899 — Off-Topic Detection for Guided Processes (Layer C)

### Summary
Architecturally sound and feasible. The ProcessRegistry already has the interception point (ADR-049), and the GuidedProcess protocol is extensible (proven by #888). Estimated ~4-5 days.

### What I Can Do Without PM Input
- Protocol extension: add `claim_message()` to GuidedProcess
- Registry integration: check claim before routing to handler
- Pattern-based detection for onboarding (project/repo format matching)

### Questions That Need Your Input

1. **Aggressiveness**: How strict should off-topic detection be?
   - Conservative: Only clear non-sequiturs ("What's the weather?" during onboarding)
   - Moderate: Also catches tangential messages ("Tell me about your features" during standup)
   - Aggressive: Anything that doesn't look like a direct answer to the current prompt

   *My recommendation*: Start conservative. Under-detection is annoying but safe; over-detection breaks flow.

2. **UX when off-topic detected**: Pause the process, or just warn?
   - Option A: Auto-pause + "That doesn't seem related to [process]. I've paused it — you can say 'resume' to continue. Meanwhile: [answer their actual question]"
   - Option B: Warn + continue: "Hmm, that doesn't seem related to [process]. Did you want to pause, or should I try to work with it?"

   *My recommendation*: Option A — auto-pause and answer their question. Less friction.

3. **Scope for M1**: All three process types, or just onboarding + standup?
   - SlotFilling is short-lived and already cancelable

   *My recommendation*: Just onboarding + standup for M1.

4. **Pattern-based vs LLM-based**: Start with regex patterns (fast, free) or use LLM (accurate, costly)?

   *My recommendation*: Patterns first. LLM fallback in Phase 2 if needed.

### Verdict
**Shovel-ready for implementation** once you answer the 4 questions above. I'm comfortable proceeding with my recommendations if you want to approve them as a batch.

---

## #898 — 9 Classifier Misroutes

### Summary
Mixed bag. Investigation found:
- **1 false positive**: Q2 ("What can you help me with?" → DISCOVERY) is actually correct. Test expectation is wrong.
- **3 LLM classifier issues**: Q23, Q24, Q25 need prompt tuning (few-shot examples for ANALYSIS/SYNTHESIS/PLANNING)
- **5 pre-classifier pattern issues**: Q27, Q33, Q40, Q43, Q62 — patterns exist and regex-verify as correct, but matching isn't working. Likely a bug in `_matches_patterns()` or message preprocessing.

### Relationship to #911 (Floor Inversion)
Floor inversion does NOT fix these. Even with floor-first routing, messages that need specific handlers (calendar booking, document management, blocker analysis) still need correct classification to reach the right handler.

### What I Can Do Without PM Input
- **Fix Q2**: Update test expectation (DISCOVERY is correct, not IDENTITY)
- **Debug the pattern matching bug**: The 5 pre-classifier failures (Q27/33/40/43/62) have correct patterns that aren't matching. This looks like a single bug in the matching utility. Finding and fixing it would resolve 5 of 9 in one shot.
- **Add few-shot examples**: Q23/24/25 need better LLM prompt examples for ANALYSIS vs GUIDANCE, SYNTHESIS vs PRIORITY, PLANNING vs PRIORITY.

### Questions That Need Your Input

1. **Priority relative to #911**: Should classifier fixes happen before, after, or in parallel with floor inversion? Floor inversion may shift which misclassifications matter (if GUIDANCE goes through the floor, Q23 being classified as GUIDANCE instead of ANALYSIS matters less).

2. **Q2 — change test or code?**: "What can you help me with?" → DISCOVERY seems correct to me. IDENTITY is "who are you?", DISCOVERY is "what can you do?". Agree to update the test expectation?

3. **Scope**: Fix the pattern matching bug (5 queries) and update Q2 now, leave Q23/24/25 prompt tuning for after floor inversion? Or do all at once?

### Verdict
**Partially shovel-ready**. The pattern matching bug hunt is independent work I can start now. The LLM prompt tuning is intertwined with floor inversion. Recommend splitting: fix patterns now, prompt tune later.

---

## Recommended Priority Order

1. **#898 pattern matching bug** — likely a single fix that resolves 5 misroutes (S-M effort, high value)
2. **#899 off-topic detection** — solid M effort, architecturally clean, but needs your UX decisions
3. **#898 prompt tuning** — defer until after #911 floor inversion clarifies which categories matter
