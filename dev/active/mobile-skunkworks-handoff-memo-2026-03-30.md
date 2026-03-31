# Mobile 2.0 Skunkworks — Handoff Memo

**From**: Mobile App Consultant
**To**: Future Mobile App Consultant (successor conversation)
**Date**: March 30, 2026
**Re**: Complete Context for Continuing Mobile Exploration

---

## Executive Summary

This memo documents everything you need to continue the Piper Morgan Mobile 2.0 skunkworks project. The project explored whether **entity-based gesture mapping** could create an intuitive mobile interaction model for an AI-powered PM assistant.

**Current state**: A functional proof-of-concept exists. It was ready for tactile validation as of January 24, 2026, but the validation period was interrupted by other priorities. The core hypothesis — does entity-based gesture mapping feel intuitive? — remains unvalidated.

**Your mission**: Pick up where we left off. The code works. The concepts are solid. We just need hands on the device to learn what the theory feels like in practice.

---

## The Core Idea

### Entity-Based Gesture Mapping

Most mobile apps treat gestures positionally: swipe-left means "delete" regardless of what you're swiping. We proposed that gestures should be **semantic**, tied to entity type:

| Entity Type | Swipe Right | Swipe Left | Swipe Up | Swipe Down |
|-------------|-------------|------------|----------|------------|
| Task | Complete | Defer | Escalate | Delegate |
| Decision | Approve | Decline | Need Info | — |
| Person | Message | Snooze | — | — |
| Project | Dashboard | Archive | Add Milestone | — |
| Blocker | Resolved | Escalate | — | — |

The same gesture means different things depending on what you're touching. This maps gestures to the **entity model**, not to arbitrary UI conventions.

### Theoretical Foundation

This concept builds on several principles established in the December 1, 2025 exploration session:

1. **"The user is mobile"** — There is no separate mobile UX. There's a holistic UX with mobile touchpoints for specific jobs-to-be-done. (Insight from xian's CloudOn experience)

2. **Moment-optimized, not feature-portable** — Mobile Piper shouldn't shrink the desktop; it should specialize in bounded-time interactions:
   - Transitional moments (walking to meeting, commute)
   - Interstitial moments (between meetings, waiting)
   - Capture moments (post-meeting, ideas while walking)
   - Decompression moments (end of day, processing)

3. **Front-end / back-end split** — Phone for quick decisions, approvals, triage. Laptop for context synthesis and complex work. Piper bridges the handoff.

4. **Lazy object instantiation** — Entities crystallize through attention. Touch creates ontology. (Pattern from CloudOn patent US 9886189)

5. **Grammar alignment** — The Piper Morgan object model grammar "Entities experience Moments in Places" has natural gestural expression. Mobile is uniquely suited to *moments* while desktop handles *situations*.

### Trust Gradient on Mobile

Trust is earned differently on mobile:
- **Desktop**: Trust through competence (did you do the thing right?)
- **Mobile**: Trust through respect (did you interrupt me appropriately?)

Notifications should be actionable and self-resolving, not nagging. The "floor inversion" principle (ADR-060) applies: the AI should be helpful by default, not gatekeeping.

---

## What Was Built

### Technical Stack

- **Framework**: Expo SDK 54 with React Native + TypeScript
- **Gestures**: react-native-gesture-handler + react-native-reanimated
- **Haptics**: expo-haptics
- **Build**: Native iOS via Xcode (Expo Go is incompatible due to Worklets version mismatch)

### Project Location

```
skunkworks/mobile/piper-mobile-poc/
├── src/
│   ├── components/
│   │   ├── EntityCard.tsx      # Main interactive card with gestures
│   │   └── IntentToast.tsx     # Shows fired intents
│   ├── entities/
│   │   ├── types.ts            # Entity, HeatLevel, LifecycleState types
│   │   └── mockData.ts         # 6 realistic mock entities
│   ├── gestures/
│   │   └── gestureConfig.ts    # Entity-specific gesture→intent mappings
│   ├── screens/
│   │   └── GestureLabScreen.tsx # Main playground
│   └── theme/
│       └── index.ts            # Dark theme colors, typography
└── ios/                        # Native Xcode project
```

### Features Implemented

| Feature | Status | Notes |
|---------|--------|-------|
| Entity cards (6 types) | ✅ Working | Task, Decision, Person, Project, Blocker, + one more |
| Pan gestures (4 directions) | ✅ Working | Swipe right/left/up/down |
| Long-press gesture | ✅ Working | For contextual actions |
| Gesture thresholds | ✅ Working | 100px commit, 60px warning, 500px/s velocity |
| Visual feedback | ✅ Working | Card animation, color shift toward intent |
| Haptic feedback | ✅ Working | Light at warning, medium at commit |
| Intent toast | ✅ Working | Shows entity + gesture + intent (no fade animation) |
| Spring-back animation | ✅ Working | Cards return to position after gesture |

### Known Technical Debt

| Issue | Status | Notes |
|-------|--------|-------|
| Toast fade animation | Disabled | Reanimated compatibility issue; functional but no smooth fade |
| Expo Go compatibility | Won't fix | Must use native Xcode build; Worklets version mismatch |
| Mock data | Generic | Could be updated with realistic PM scenarios |

---

## How to Run the PoC

### Prerequisites

- Mac with Xcode installed
- iPhone with Developer Mode enabled
- Apple Developer account (free tier works)

### Build Process

```bash
# Start Metro bundler
cd skunkworks/mobile/piper-mobile-poc
npx expo start --dev-client --port 8081

# In separate terminal, open Xcode project
open ios/PiperMobile.xcworkspace

# In Xcode:
# 1. Select your iPhone from device dropdown
# 2. Press Cmd+R to build and run
```

### What You Should See

1. "Gesture Lab" screen with 5-6 entity cards
2. Each card shows entity type, title, subtitle, and heat indicator
3. Drag cards in any direction — they animate with your finger
4. At ~60px: warning haptic fires
5. At ~100px: commit haptic fires, card snaps back, toast appears showing intent
6. Toast shows: entity type icon, title, gesture direction, and intent label

### Troubleshooting

- **Expo Go crashes**: Expected. Must use native build.
- **USB connection issues**: Try different cable, direct port (no hub), or wireless debugging
- **Build fails in Xcode**: Try `npx expo prebuild --clean` to regenerate iOS folder

---

## Project History

| Date | Milestone |
|------|-----------|
| Dec 1, 2025 | Conceptual exploration session — established dual-track approach, core concepts |
| Dec 5, 2025 | One-shot prompt created; vibe coding completed in 12 minutes |
| Dec 5-7 | Expo Go blocked by Worklets version mismatch |
| Dec 7 | Decision: use Xcode native build instead |
| Dec 23 | Native build working, app runs in Simulator |
| Dec 25-27 | Device deployment attempted, certificate/USB issues |
| Jan 3, 2026 | App running on device; toast bug identified |
| Jan 24 | Toast bug fixed; tactile validation begun |
| Jan 24 - Mar 30 | Hiatus — PM focused on MUX, alpha testing |
| Mar 30 | Handoff documentation created |

**Total coding time**: ~1.5 hours (12 min initial build + ~1 hour debugging)
**Total platform friction**: ~50 days

---

## What's Been Validated

1. **Technical feasibility**: Entity-based gesture mapping is implementable with standard React Native tooling

2. **Gesture vocabulary is expressible**: Swipe directions + long-press provide enough semantic space for PM entity types

3. **Haptic feedback adds information**: Warning and commit thresholds can be distinguished by feel

4. **The code works**: All gesture types fire intents correctly (verified via Metro logs)

---

## What Remains Unvalidated

The core UX hypothesis:

> "Gestures should be semantic, tied to entity type, not positional. The same gesture means different things depending on what you're touching. This will feel intuitive, not confusing."

This can only be validated through actual use. A 2-3 day "carry and note" validation protocol was defined but not completed.

### Validation Questions

| Question | What We're Learning |
|----------|---------------------|
| Semantic coherence | Does swipe-right meaning different things for different entities feel natural or confusing? |
| Learnability | After a few uses, do gesture meanings become predictable? |
| Haptic value | Does warning-then-commit feedback help or distract? |
| Missing gestures | Any moments where you want a gesture that doesn't exist? |
| Moment fit | How does it feel in actual mobile contexts (coffee line, pre-meeting, quick triage)? |

---

## Key Documents in Project Knowledge

1. **piper-mobile-poc-expo-scaffold.md** — Original project structure and component sketches
2. **claude-code-one-shot-prompt.md** — The prompt that built the PoC in 12 minutes
3. **Session logs** (various dates) — Detailed progress and decisions
4. **Memos** — Communication trail with CXO and Vibe Coding Agent

### External References

- **CloudOn Patent**: US 9886189 — "Systems and Methods for Object-based Interaction with Cloud-Based Applications" (now Dropbox-owned)
- **ADR-042**: Mobile Strategy Progressive Enhancement — Desktop-first, responsive web → PWA → native based on usage signals
- **ADR-060**: Floor-First Routing — LLM is the floor, not the ceiling

---

## Recommendations for Resumption

### Immediate Next Steps

1. **Verify the app still builds** — Dependencies may have drifted; may need `npm install` and pod updates

2. **Complete tactile validation** — Carry the device for 2-3 days, collect informal feedback on the validation questions above

3. **Assess concept validity** — Does entity-based gesture mapping feel right? If yes, continue design discovery. If no, identify what's wrong.

### If Concept Validates

- Continue Track A (Design Discovery): Formalize the entity-gesture grammar, moment taxonomy, notification philosophy
- Consider updating mock data with realistic PM scenarios
- Explore how this connects to the broader Piper Morgan experience (handoff to desktop, notification patterns)

### If Concept Doesn't Validate

- Identify what feels wrong (gesture mappings confusing? thresholds off? wrong entity types?)
- Iterate on the specific issues
- Consider whether the concept needs refinement vs. abandonment

### Technical Improvements (If Proceeding)

- Fix toast animation (use RN Animated API instead of Reanimated)
- Consider threshold tuning based on feedback
- Update to newer Expo SDK if Worklets compatibility improves

---

## Relationship to Broader Piper Morgan

This mobile exploration is a **skunkworks side project**, commissioned by the CXO but operating on a "simmer" basis without interfering with the critical path.

**Strategic alignment**:
- ADR-042 establishes progressive enhancement: responsive web → PWA → native
- This PoC is exploratory — validating concepts for a potential future native phase
- The entity model and moment concepts align with MUX (Modeled User Experience) work

**If the concept validates strongly**, it could inform:
- Mobile web interactions (gesture-like tap patterns)
- PWA capabilities when that phase arrives
- Native app design if usage signals justify the investment

---

## Closing Note

This project demonstrates something interesting: the actual coding took 12 minutes. The platform friction took 50 days. The concept validation... hasn't happened yet.

The ideas are good. The code works. What's missing is someone with the device in their hand, using it in real mobile moments, developing intuitions about whether semantic gestures feel natural.

When you pick this up, that's your job: feel it. Note what works and what doesn't. The theory is ready to meet reality.

Good luck.

---

*Mobile App Consultant*
*March 30, 2026*
