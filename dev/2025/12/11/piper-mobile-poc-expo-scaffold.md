# Piper Morgan Mobile PoC — Expo Scaffold

## Purpose

Rapid proof-of-concept for exploring mobile/gestural interaction patterns for Piper Morgan, an AI-powered PM assistant. This is a skunkworks exploration, not production code.

**Goals:**
- Get something touchable on a real phone quickly
- Explore gesture vocabulary mapped to entity types
- Experiment with moment-oriented flows
- All data mocked — no backend required

---

## Project Setup

```bash
# Create new Expo project
npx create-expo-app piper-mobile-poc --template blank-typescript

cd piper-mobile-poc

# Install gesture and animation libraries
npx expo install react-native-gesture-handler react-native-reanimated

# Install haptics for feedback
npx expo install expo-haptics

# Install safe area handling
npx expo install react-native-safe-area-context

# Navigation (lightweight)
npx expo install @react-navigation/native @react-navigation/native-stack
npx expo install react-native-screens
```

**babel.config.js** — Add reanimated plugin:
```javascript
module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: ['react-native-reanimated/plugin'],
  };
};
```

---

## Project Structure

```
piper-mobile-poc/
├── App.tsx                    # Entry point, navigation setup
├── src/
│   ├── components/
│   │   ├── EntityCard.tsx     # Touchable entity representation
│   │   ├── GesturePlayground.tsx  # Sandbox for testing gestures
│   │   ├── MomentView.tsx     # Context-aware moment display
│   │   └── ActionNotification.tsx # Self-resolving notification mock
│   │
│   ├── entities/
│   │   ├── types.ts           # Entity type definitions
│   │   └── mockData.ts        # Fake entities for exploration
│   │
│   ├── gestures/
│   │   ├── useEntityGestures.ts   # Hook: gesture handlers per entity type
│   │   └── gestureConfig.ts       # Gesture → intent mappings
│   │
│   ├── moments/
│   │   ├── types.ts           # Moment type definitions
│   │   └── MomentContext.tsx  # Current moment state
│   │
│   ├── screens/
│   │   ├── HomeScreen.tsx     # Entry point / moment detection
│   │   ├── EntityListScreen.tsx   # List of entities to interact with
│   │   ├── EntityDetailScreen.tsx # Single entity deep view
│   │   └── GestureLabScreen.tsx   # Pure gesture experimentation
│   │
│   └── theme/
│       └── index.ts           # Colors, spacing, typography
│
└── assets/                    # Icons, images if needed
```

---

## Core Concepts to Implement

### 1. Entity Types

```typescript
// src/entities/types.ts

type EntityType = 'task' | 'person' | 'project' | 'decision' | 'blocker';

interface Entity {
  id: string;
  type: EntityType;
  title: string;
  subtitle?: string;
  heat: 'cold' | 'warm' | 'hot';  // urgency signal
  lifecycle: 'nascent' | 'active' | 'blocked' | 'resolved';
  relatedEntityIds?: string[];
}

// Example entities in mockData.ts
const mockEntities: Entity[] = [
  {
    id: '1',
    type: 'task',
    title: 'Review Q1 roadmap draft',
    subtitle: 'From: Sarah Chen',
    heat: 'warm',
    lifecycle: 'active',
  },
  {
    id: '2',
    type: 'decision',
    title: 'Approve vendor contract',
    subtitle: 'Legal cleared, awaiting PM sign-off',
    heat: 'hot',
    lifecycle: 'blocked',
  },
  // ... more
];
```

### 2. Gesture → Intent Mapping

```typescript
// src/gestures/gestureConfig.ts

// The key insight: gestures mean different things for different entities

type GestureType = 'swipeRight' | 'swipeLeft' | 'swipeUp' | 'swipeDown' | 'longPress' | 'doubleTap';

type IntentByEntityType = {
  [K in EntityType]: {
    [G in GestureType]?: string;  // intent name
  };
};

const gestureIntents: IntentByEntityType = {
  task: {
    swipeRight: 'complete',
    swipeLeft: 'defer',
    swipeUp: 'escalate',
    swipeDown: 'delegate',
    longPress: 'showActions',
    doubleTap: 'quickView',
  },
  decision: {
    swipeRight: 'approve',
    swipeLeft: 'decline',
    swipeUp: 'needsMoreInfo',
    longPress: 'showContext',
  },
  person: {
    swipeRight: 'sendMessage',
    swipeLeft: 'snooze',
    longPress: 'showRelationships',
    doubleTap: 'quickCall',
  },
  project: {
    swipeRight: 'openDashboard',
    swipeLeft: 'archive',
    swipeUp: 'addMilestone',
    longPress: 'showTimeline',
  },
  blocker: {
    swipeRight: 'markResolved',
    swipeLeft: 'escalate',
    longPress: 'showBlockedItems',
  },
};
```

### 3. Moment Context

```typescript
// src/moments/types.ts

type MomentType =
  | 'transitional'   // walking to meeting, commute
  | 'interstitial'   // between meetings, waiting
  | 'capture'        // post-meeting, need to record
  | 'decompression'  // end of day, processing
  | 'focused';       // deliberate engagement (rare on mobile)

interface MomentContext {
  type: MomentType;
  timeAvailable: 'glance' | 'minute' | 'extended';  // <10s, <2min, >2min
  nextEvent?: {
    title: string;
    minutesUntil: number;
  };
}

// For PoC: manually switchable, later could use signals
```

### 4. Entity Card with Gestures

```typescript
// src/components/EntityCard.tsx — sketch

import { Gesture, GestureDetector } from 'react-native-gesture-handler';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
  runOnJS
} from 'react-native-reanimated';
import * as Haptics from 'expo-haptics';

interface EntityCardProps {
  entity: Entity;
  onIntent: (intent: string) => void;
}

export function EntityCard({ entity, onIntent }: EntityCardProps) {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);

  const panGesture = Gesture.Pan()
    .onUpdate((event) => {
      translateX.value = event.translationX;
      translateY.value = event.translationY;
    })
    .onEnd((event) => {
      const { translationX, translationY } = event;

      // Determine swipe direction
      if (Math.abs(translationX) > Math.abs(translationY)) {
        // Horizontal swipe
        if (translationX > 100) {
          runOnJS(handleIntent)('swipeRight');
        } else if (translationX < -100) {
          runOnJS(handleIntent)('swipeLeft');
        }
      } else {
        // Vertical swipe
        if (translationY < -100) {
          runOnJS(handleIntent)('swipeUp');
        } else if (translationY > 100) {
          runOnJS(handleIntent)('swipeDown');
        }
      }

      // Spring back
      translateX.value = withSpring(0);
      translateY.value = withSpring(0);
    });

  const longPressGesture = Gesture.LongPress()
    .minDuration(500)
    .onStart(() => {
      runOnJS(Haptics.impactAsync)(Haptics.ImpactFeedbackStyle.Medium);
      runOnJS(handleIntent)('longPress');
    });

  const handleIntent = (gestureType: GestureType) => {
    const intent = gestureIntents[entity.type][gestureType];
    if (intent) {
      Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
      onIntent(intent);
    }
  };

  const composed = Gesture.Race(panGesture, longPressGesture);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
    ],
  }));

  return (
    <GestureDetector gesture={composed}>
      <Animated.View style={[styles.card, animatedStyle]}>
        {/* Entity display */}
      </Animated.View>
    </GestureDetector>
  );
}
```

---

## Screens to Build (Priority Order)

### 1. GestureLabScreen (Start Here)
Pure sandbox. Show a few entity cards. Swipe them. See what intent fires. No navigation, no complexity. Just feel the gestures.

### 2. EntityListScreen
List of mock entities. Swipe to act. Visual feedback on intent. Maybe a toast showing "You chose: [intent]".

### 3. MomentView
Simulate different moments. "You're in a transitional moment. Here's one thing." vs "You have 2 minutes. Here are your hot items."

### 4. ActionNotification (mock)
Simulate a notification that includes inline actions. "Sarah replied. [Approve draft] [Edit] [Later]"

---

## Visual Design Notes

For PoC, keep it minimal:
- Dark background, light cards (or inverse)
- Clear visual feedback on gesture thresholds (color shift as you approach commit point)
- Haptic feedback at key moments (threshold reached, action committed)
- Entity type indicated by subtle icon or color accent
- Heat shown as border glow or color intensity

Don't over-design. The goal is feeling the gestures, not pixel perfection.

---

## Running the PoC

```bash
# Start Expo
npx expo start

# Scan QR with Expo Go app on your phone
# Or press 'i' for iOS simulator, 'a' for Android emulator
```

---

## What We're Learning

As you use the PoC, note:
- Which gestures feel natural vs. forced?
- Which entity-intent mappings make sense vs. confuse?
- What's missing from the gesture vocabulary?
- How does moment context change what you want to see/do?
- Where does the mock fall short of real?

Feed learnings back to Track A (design discovery).

---

## Claude Code Prompt

When handing this to Claude Code, you might say:

> "I'm building a mobile PoC to explore gestural interactions for a PM assistant called Piper Morgan. The key concept is that gestures map to entity types — swiping a task means something different than swiping a person.
>
> Please scaffold an Expo TypeScript project following the structure in this document. Start with the GestureLabScreen — I want to see 3-4 entity cards I can swipe and get haptic feedback. The gesture → intent mapping should follow the gestureConfig pattern shown.
>
> Use react-native-gesture-handler and react-native-reanimated for gestures. Keep the UI minimal — I care about feel, not polish."

---

*Document created: December 1, 2025*
*For: Piper Morgan Mobile 2.0 Skunkworks*
