# One-Shot Prompt: Piper Mobile PoC

## Prompt

You are building a rapid proof-of-concept mobile app to explore gestural interaction patterns for **Piper Morgan**, an AI-powered PM assistant. This is a skunkworks exploration — speed and feel matter more than polish.

### The Core Insight

The key design concept is **entity-based gesture mapping**: gestures mean different things depending on what type of entity you're touching. Swiping right on a *task* means "complete." Swiping right on a *decision* means "approve." Swiping right on a *person* might mean "send message." The gesture vocabulary is semantic, tied to the entity model, not arbitrary UI conventions.

This is inspired by CloudOn's patent (US 9886189) on object-based touch interaction — "anything you can touch, you do stuff to, spatially."

### What to Build

Create an Expo (React Native + TypeScript) project with:

1. **GestureLabScreen** (the main playground)
   - Display 4-6 entity cards of different types (task, decision, person, project, blocker)
   - Each card responds to gestures: swipe left/right/up/down, long-press
   - Gestures trigger entity-type-specific intents (see scaffold doc for mapping)
   - Visual feedback: cards animate with the gesture (translate, opacity, color shift)
   - Haptic feedback: light tap on threshold approach, medium impact on commit
   - Toast or overlay showing "Intent: [action]" so I can see what fired

2. **Entity Cards**
   - Show entity type (icon or color-coded)
   - Title and subtitle
   - "Heat" indicator (cold/warm/hot = urgency)
   - Clear visual threshold feedback as gesture approaches commit point

3. **Mock Data**
   - Hardcoded entities that feel real:
     - "Review Q1 roadmap draft" (task, warm)
     - "Approve vendor contract" (decision, hot)
     - "Sarah Chen — waiting for response" (person, warm)
     - "Mobile 2.0 initiative" (project, cold)
     - "API rate limiting unresolved" (blocker, hot)

4. **Gesture Configuration**
   - Implement the gesture→intent mapping from the scaffold
   - Make it easy to tweak thresholds and mappings (config object, not hardcoded)

### Technical Stack

- Expo with TypeScript (`npx create-expo-app ... --template blank-typescript`)
- `react-native-gesture-handler` + `react-native-reanimated` for gestures
- `expo-haptics` for tactile feedback
- Keep dependencies minimal — this is a PoC

### What I Care About

- **Feel**: Does swiping feel satisfying? Do the gestures have weight?
- **Clarity**: Can I tell what gesture I'm about to commit?
- **Entity semantics**: Does the intent make sense for the entity type?

### What I Don't Care About (Yet)

- Navigation between screens (just the lab screen is fine)
- Actual backend or data persistence
- Perfect visual design (functional > pretty)
- Tests (we're exploring, not shipping)

### Success Criteria

When you're done, I should be able to:
1. Run `npx expo start` and scan the QR with Expo Go on my phone
2. See a screen with several entity cards
3. Swipe cards in different directions and feel haptic feedback
4. See which intent each gesture triggered
5. Notice that the same gesture does different things for different entity types

### How to Work

- Use subagents freely if helpful
- Make reasonable decisions without asking — this is autonomous
- If something isn't specified, use good judgment
- Commit working increments (the project should always be runnable)
- Stop when you have something I can play with

### Reference

The attached scaffold document (`piper-mobile-poc-expo-scaffold.md`) has:
- Full project structure
- Type definitions for entities, gestures, moments
- Sample component code for EntityCard
- Gesture→intent mapping table

Use it as a guide, not a rigid spec. Deviate if you find a better approach.

---

*Now go build something I can feel in my hands.*
