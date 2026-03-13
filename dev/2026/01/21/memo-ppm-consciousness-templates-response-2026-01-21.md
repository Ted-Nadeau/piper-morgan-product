# Memo: PPM Input on Consciousness Template Transformation Issues

**From**: Principal Product Manager (PPM)
**To**: Lead Developer
**CC**: CXO, PM (xian)
**Date**: January 21, 2026
**Re**: RE: Draft Issues for Consciousness Template Transformation

---

## Overall Principle

Consciousness isn't about adding personality everywhere. It's about **removing coldness where it creates distance**. The goal is Piper feeling like a colleague, not Piper being chatty.

A useful test: Would a competent, friendly coworker phrase it this way? If yes, it's probably right. If it sounds like marketing copy or a children's app, pull back.

---

## Issue-by-Issue Guidance

### Issue 1: Onboarding Flow (MEDIUM, 2-3h)

**Q1: How much personality vs professionalism?**

Lean toward **warm professionalism**. First impressions matter, but users in onboarding are often task-focused—they want to get set up, not be entertained. Warmth should reduce friction, not add steps.

**Q2: First person introduction?**

Yes, **first person is appropriate**. "Hi, I'm Piper Morgan" establishes the colleague framing from the start. This is one of the few places where explicit self-introduction makes sense.

**Q3: Phrases/tones to avoid?**

| Avoid | Why | Better |
|-------|-----|--------|
| "Let's get started!" (overly enthusiastic) | Feels like marketing | "Let's get you set up" |
| "Don't worry, this is easy!" | Patronizing | Just make it easy, don't announce it |
| "Yay! You're all set!" | Infantilizing | "You're all set. I'm ready when you are." |

**Scope adjustment**: None needed. Proceed as scoped.

---

### Issue 2: Confirmation Dialogs (MEDIUM, 1-2h)

**Q1: Revisit helper tone or just integrate?**

Review the helper briefly, but this is mostly integration work. The pattern exists; apply it consistently.

**Q2: Different levels for destructive actions?**

Yes, but **clarity trumps warmth for destructive actions**. Delete should feel appropriately serious—not scary, but not casual either.

| Action | Tone Level | Example |
|--------|------------|---------|
| Delete | Clear, respectful | "This will permanently remove [X]. Are you sure?" |
| Reset | Clear, informative | "This will reset [X] to defaults. Your current settings will be lost." |
| Disconnect | Neutral, helpful | "Disconnecting will stop syncing with [service]. You can reconnect anytime." |

Don't make destructive actions feel trivial. Warmth ≠ casualness.

**Scope adjustment**: None needed.

---

### Issue 3: Session Timeout (MEDIUM, 1h)

**Q1: Security messaging + warmth balance?**

The "why" can BE the warmth. Instead of hiding the reason, frame it helpfully:

| Current | Conscious Alternative |
|---------|----------------------|
| "Your Session is About to Expire" | "I'm going to sign you out soon to keep things secure" |
| "For your security, inactive sessions automatically end after 30 minutes" | "It's been a while since you've been active—I'll sign you out in a few minutes to keep your account safe." |

**Q2: Avoiding bureaucratic feel?**

Use "I" and explain the benefit to *them*. "To keep your account safe" is warmer than "for security reasons."

**Scope adjustment**: None needed.

---

### Issue 4: Toast System (HARD, 6-8h)

**Q1: Backend-driven vs JS-side map?**

**JS-side message map is sufficient.** Backend-driven is over-engineering for this use case. Toast messages don't need server round-trips; they need consistency. A simple JS object with message templates is the right level of abstraction.

```javascript
const TOAST_MESSAGES = {
  todo_created: { title: "Got it", body: "Todo added" },
  todo_deleted: { title: "Done", body: "Todo removed" },
  // ...
};
```

**Q2: Identity in toasts?**

Keep it **brief and neutral-warm**. Toasts are glanceable—users don't read them carefully. "Saved" is fine. "Got it—saved" adds a touch of acknowledgment without bloat. Avoid "I have successfully saved your item."

| Too Cold | Too Chatty | Right |
|----------|------------|-------|
| "Success" | "I've saved that for you!" | "Saved" or "Got it" |
| "Error" | "Oops, something went wrong!" | "Couldn't save—try again?" |

**Q3: Worth the investment?**

Yes, but **scope down to JS-side map**. The architectural investment of a backend MessageService is not justified. A find-and-replace pass with a centralized JS constants file is the right level.

**Scope adjustment**: Reduce from backend architecture to JS-side centralization. Estimate drops to 3-4 hours.

---

### Issue 5: Validation Messages (HARD, 2-3h)

**Q1: Personality in validation?**

**Minimal.** Error states are frustrating. Adding personality can feel dismissive or condescending. The goal is clarity + respect, not charm.

**Q2: Risk of being too casual?**

Yes. "Oops, you forgot your password" is patronizing. "We need your email" is warm without being cutesy.

| Current | Conscious | Too Far |
|---------|-----------|---------|
| "Email is required" | "We need your email to continue" | "Oops! Don't forget your email!" |
| "Minimum 8 characters required" | "8 characters minimum" | "Just a bit more! 🎉" |

**Principle**: For errors, remove coldness but don't add personality. The user is already frustrated; don't make them feel talked down to.

**Scope adjustment**: Reclassify as MEDIUM (2h). This doesn't require architectural changes—it's copy updates in one file.

---

## Summary Table (Revised)

| Issue | Category | Est. Time | Key Guidance |
|-------|----------|-----------|--------------|
| Onboarding flow | MEDIUM | 2-3h | Warm professionalism; first person OK |
| Confirmation dialogs | MEDIUM | 1-2h | Clarity > warmth for destructive actions |
| Session timeout | MEDIUM | 1h | "Why" can be the warmth |
| Toast system | **MEDIUM** (revised) | **3-4h** | JS-side map, not backend; keep brief |
| Validation messages | **MEDIUM** (revised) | **2h** | Remove coldness, don't add personality |

**Total revised estimate**: 9-12 hours (down from 12-17h)

---

## Prioritization Recommendation

| Priority | Issues | Rationale |
|----------|--------|-----------|
| **P1** | Onboarding, Session timeout | First impressions + trust |
| **P2** | Confirmation dialogs, Validation | Consistency |
| **P3** | Toast system | Polish; existing toasts work |

---

## Missing Items?

One thing not mentioned: **Empty states**. We have `empty-state-voice-guide-v1.md` from B1. Are empty states already covered, or do they need a separate issue?

---

*Filed: 2026-01-21 6:35 PM PT*
*In response to: 2026-01-21-consciousness-template-issues-draft.md*
