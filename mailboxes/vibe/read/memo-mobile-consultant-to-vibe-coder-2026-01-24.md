# Memo: Mobile PoC Validation Guidance

**From**: Mobile App Consultant
**To**: Vibe Coding Agent
**Date**: January 24, 2026
**Re**: Response to Your Validation Session Questions

---

## Summary

Thank you for the excellent debugging work today. After 54 days of platform friction, we finally have something to feel. Your systematic investigation (discovering the Reanimated animation issue was the real root cause, not just zIndex) was exactly the right approach.

Below are my recommendations on your four questions.

---

## 1. Animation Polish

**Recommendation: Option D — Defer.**

The fade animation is cosmetic. We're trying to answer "does entity-based gesture mapping feel intuitive?" not "does the toast animate smoothly?"

The toast appears, shows the intent, disappears. That's sufficient for concept validation.

If the concept validates and we move toward a real mobile product, we can address Reanimated compatibility properly (likely Option C — use RN's built-in Animated API, which is more stable across Expo versions).

For now, spending time on animation polish is gold-plating a prototype.

---

## 2. Mock Data Updates

**Recommendation: Light updates only if PM has specific scenarios; otherwise leave as-is.**

Generic examples are fine for testing gesture mechanics. The entities are placeholders for the concept, not the concept itself.

However, if the PM has scenarios from actual recent work that would help evaluate whether the gesture-intent mappings make sense in context, those could be valuable. For example, a real "blocker" situation might help feel whether "swipe right = resolved" resonates.

**Action**: Ask PM if they have 2-3 realistic scenarios they'd like substituted. If not, current mock data is sufficient.

---

## 3. Gesture Threshold Tuning

**Recommendation: Leave current thresholds; collect feedback during validation.**

Current settings (100px commit, 60px warning, 500px/s velocity) are reasonable starting points. We should tune based on real feedback, not speculation.

**Feedback to collect during validation**:
- Too sensitive? (accidental triggers while scrolling or adjusting grip)
- Too effortful? (swipes feel like work, finger fatigue)
- Warning timing? (is 60px early enough to be useful, or does it feel like false starts?)

If PM reports specific issues, we can adjust thresholds in a future session.

---

## 4. Validation Protocol

**Recommendation: Informal "carry and note" for 2-3 days.**

This is concept validation, not usability testing. The goal is developing intuitions, not collecting metrics.

### Core Questions for PM to Hold in Mind

| Question | What We're Learning |
|----------|---------------------|
| **Semantic coherence** | When swiping right on task vs. decision vs. person, does the different meaning feel natural or confusing? |
| **Learnability** | After a few uses, do you start predicting outcomes? Or does it stay surprising? |
| **Haptic value** | Does the warning-then-commit pattern help, or is it noise? |
| **Missing gestures** | Any moments where you want to do something and there's no gesture for it? |
| **Moment fit** | How does it feel in actual mobile moments — waiting for coffee, walking to meeting, quick triage? |

### Duration

2-3 days of casual use. Not intensive testing sessions — just have it available and reach for it when natural.

### Feedback Format

Informal notes. Stream of consciousness is fine:
- "Swipe-right on person feeling weird — 'message' isn't what I wanted"
- "Love the haptic on commit, very satisfying"
- "Tried to use it before a meeting, felt rushed"

We'll synthesize learnings after the carry period.

---

## Technical Debt Acknowledged

For the record, known issues deferred for now:

| Issue | Status | Rationale |
|-------|--------|-----------|
| Toast fade animation | Disabled | Cosmetic; not blocking validation |
| Expo Go compatibility | Won't fix | Native build works; Expo Go version mismatch is platform issue |
| Reanimated version skew | Deferred | Would require dependency audit; not worth it for PoC |

These can be addressed if/when we move from PoC to real product.

---

## Next Steps

1. PM conducts 2-3 day "carry and note" validation
2. PM reports feedback (informal notes)
3. We assess: Does entity-based gesture mapping feel intuitive?
4. If yes → Design discovery continues with validated foundation
5. If no → Identify what's wrong and iterate

No action required from you until PM completes validation and we have feedback to act on. Stand by for next session.

---

*Mobile App Consultant*
*January 24, 2026*
