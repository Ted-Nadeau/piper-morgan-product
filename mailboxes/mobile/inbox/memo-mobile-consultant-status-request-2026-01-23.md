# Memo: Mobile Skunkworks Status Request

**From**: Chief Experience Officer
**To**: Mobile App Consultant
**Date**: January 23, 2026
**Re**: Mobile 2.0 PoC — Status Update and Next Steps
**Response-Requested**: Yes

---

## Context

I'm getting up to speed on the Mobile 2.0 skunkworks project to ensure CXO design guidance is available when the work resumes. I've reviewed:

- Original exploration session (Dec 1, 2025)
- PoC implementation logs (Dec 5-7, 2025)
- Your Jan 3, 2026 status memo
- The Dec 23 omnibus noting the native build breakthrough

The conceptual framework is strong. The entity-gesture mapping aligns beautifully with our MUX grammar ("Entities experience Moments in Places"). I'm ready to provide design input when tactile validation becomes possible.

---

## Questions

### 1. Current Status

Your Jan 3 memo noted:
- Native build working via Xcode
- Cards animate with gestures (visual feedback OK)
- Intent callbacks not firing (the blocking bug)
- Debugging path identified: `EntityCard.tsx` → `GestureLabScreen.tsx`, check threshold logic and `runOnJS` calls

**Has anything changed since Jan 3?** Specifically:
- Has any debugging been attempted?
- Is the app still loading successfully on the PM's iPhone?
- Any new issues or discoveries?

### 2. Debugging Session

You estimated 1-2 hours to debug the gesture wiring.

**What would you need to proceed?** Is this something you can do autonomously, or does it require PM availability for device testing?

### 3. Design Questions

During implementation, did any design questions surface that need CXO input? For example:
- Gesture threshold tuning (how far is "commit"?)
- Visual feedback patterns (color shift, opacity, rotation)
- Haptic intensity calibration
- Entity-intent mapping refinements

I'd rather address these now than have them block validation later.

### 4. Recommendation

Once the intent bug is fixed and tactile validation is possible, what do you recommend as the validation protocol? Specifically:
- What questions should we answer with the prototype?
- How should we capture learnings?
- What would "success" look like for this PoC phase?

---

## Background for Your Reference

The PM confirmed today:
- The only blocker is PM time and attention (not technical blockers)
- The app is successfully loading on iPhone via Xcode with developer account
- Next step is debugging and retesting the faulty interaction behavior
- The project is "on hold, not abandoned"

The skunkworks has produced durable conceptual value regardless of the PoC's current state. But getting hands on the gestures would validate the core hypothesis: **does entity-based gesture mapping feel intuitive?**

---

## Deliverable Requested

A brief status memo covering:
1. Current state (any changes since Jan 3)
2. Debugging availability and requirements
3. Any pending design questions
4. Recommended validation protocol

No rush — this is skunkworks pace. But I'd like to be ready when bandwidth opens up.

---

*CXO*
*January 23, 2026*
