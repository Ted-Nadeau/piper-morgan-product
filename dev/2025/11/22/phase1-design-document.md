# Phase 1: Design & Models - CONV-LEARN-PREF #248

**Date**: November 22, 2025
**Status**: 🔨 IN PROGRESS
**Completion Target**: 1.5-2 hours

---

## Overview

Phase 1 establishes the data models, service architecture, and integration points for conversational preference gathering. This phase designs how preferences are detected, stored, and applied without implementing the full logic.

**Deliverables**:
1. ✅ Preference detection models (`preference_detection.py`)
2. ✅ Conversation analyzer service (`conversation_analyzer.py`)
3. ⏳ Integration points documentation
4. ⏳ Intent handler hook design

---

## 1. Models Created ✅

### preference_detection.py

**Enums**:
- `PreferenceDimension`: The 4 dimensions we detect (WARMTH, CONFIDENCE, ACTION, TECHNICAL)
- `DetectionMethod`: How preference was found (LANGUAGE_PATTERNS, EXPLICIT_FEEDBACK, BEHAVIORAL_SIGNALS, COMMAND_FREQUENCY, RESPONSE_PATTERNS)
- `ConfidenceLevel`: Signal strength classification (LOW, MEDIUM, HIGH, VERY_HIGH)

**PreferenceHint** (40 lines):
- Detected signal that user may have a preference
- NOT yet stored in PersonalityProfile (awaiting confirmation or high confidence)
- Fields:
  - `id`: Unique hint ID
  - `user_id`: User who preferences were detected for
  - `dimension`: Which dimension (WARMTH, CONFIDENCE, ACTION, TECHNICAL)
  - `detected_value`: The value we think they prefer
  - `current_value`: Their current profile value
  - `detection_method`: How we detected it
  - `confidence_score`: 0.0-1.0
  - `source_text`: Conversation excerpt that triggered detection
  - `evidence`: Supporting data (word counts, patterns)
  - `created_at`: When detected
  - `expires_at`: Optional staleness timeout
- Key methods:
  - `confidence_level()`: Classify confidence into categories
  - `is_ready_for_suggestion()`: Should we suggest to user? (confidence ≥ 0.4)
  - `is_ready_for_auto_apply()`: Can we auto-apply? (confidence ≥ 0.9 + strong evidence)
  - `to_dict()`: Serialize for storage

**PreferenceConfirmation** (30 lines):
- User has confirmed a preference change
- Result of: suggesting hint → user accepts → convert to confirmation
- Stored in UserPreferenceManager with key: `f"personality_{dimension}"`
- Fields:
  - `id`: Unique confirmation ID
  - `user_id`: User confirming
  - `dimension`: Which dimension
  - `new_value`: Value to apply
  - `previous_value`: Their prior preference
  - `hint_id`: Reference to the PreferenceHint
  - `confirmation_source`: "user_explicit", "auto_apply", or "learning_system"
  - `confirmed_at`: When confirmed
  - `applied_at`: When actually applied to profile

**PreferenceDetectionResult** (45 lines):
- Result of analyzing conversation for preference hints
- Returned by ConversationAnalyzer.analyze_*() methods
- Fields:
  - `hints`: Newly detected hints
  - `analysis_summary`: Human-readable summary
  - `confidence_summary`: Per-dimension confidence scores
  - `suggested_hints`: Hints ready for user suggestion
  - `auto_apply_hints`: Hints confident enough to auto-apply
  - `detected_at`: Timestamp
- Key methods:
  - `has_suggestions()`: Should we show suggestion UI?
  - `has_auto_applies()`: Should we silently apply changes?
  - `to_dict()`: Serialize for API responses

---

## 2. ConversationAnalyzer Service ✅

**Location**: `services/personality/conversation_analyzer.py` (~440 lines)

**Core Methods**:

### `analyze_message(user_id, message, current_profile) → PreferenceDetectionResult`
- Called with each user message
- Detects preferences from:
  - Language patterns (word choice, phrasing)
  - Emotional language (warmth signals)
  - Action orientation (urgency indicators)
  - Technical terminology (depth preference)
  - Confidence-related language (data vs reasoning preferences)

**Implementation Strategy**:
- Uses word frequency analysis against curated word lists
- Confidence scoring based on word ratios
- Only creates hints if detected value differs from current profile
- Examples:
  ```python
  WARM_WORDS = {"love", "awesome", "appreciate", "friendly", ...}
  PROFESSIONAL_WORDS = {"efficient", "concise", "professional", ...}

  # Detects: More warm words → suggests higher warmth_level
  # Detects: More professional words → suggests lower warmth_level
  ```

### `analyze_response(user_id, user_message, system_response, current_profile) → PreferenceDetectionResult`
- Called after system provides response to user
- Detects preferences from user's reaction:
  - "too long" / "tldr" → technical_depth = SIMPLIFIED
  - "more detail" → technical_depth = DETAILED
  - Response length analysis

### `analyze_feedback(user_id, feedback_text, current_profile) → PreferenceDetectionResult`
- Called when user provides explicit feedback
- Parses explicit statements like:
  - "more warm" / "friendlier" → warmth_level up
  - "always tell me what to do" → action_orientation = HIGH

**Detection Methods** (per dimension):

| Dimension | Detection | Confidence |
|-----------|-----------|------------|
| WARMTH | Warm vs Professional word ratio | 0.3-0.7 |
| ACTION | Action vs Exploratory word ratio | 0.3-0.6 |
| CONFIDENCE | Numeric vs Contextual word ratio | 0.3-0.55 |
| TECHNICAL | Technical vs Simplified word ratio | 0.3-0.65 |

**Confidence Scoring**:
- Language patterns: 0.3-0.7 (moderate confidence, can be wrong)
- Behavioral signals: 0.5-0.8 (user's actions)
- Explicit feedback: 0.85-0.95 (user told us)
- Only create hints if confidence > 0.3

---

## 3. Integration Points

### Integration Point 1: Intent Handler Hook ✅ (Designed)

**Where**: `services/intent_service/` - After intent classification
**When**: After every user message is classified
**What**: Run preference detection on classified intent

**Flow**:
```
User Message
    ↓
IntentClassifier (existing)
    ↓
[NEW] Preference Detection Hook
    - Load PersonalityProfile
    - Run ConversationAnalyzer.analyze_message()
    - Store hints in session context
    ↓
Response Generation (existing)
    ↓
[NEW] Response Analysis Hook
    - Analyze system's response
    - Detect if user reacts
    ↓
Return Response to User
    ↓
[NEW] Preference Suggestion Hook
    - If suggestions exist → show to user
    - If auto-applies exist → apply silently
    - Store confirmations in learning system
```

**Implementation File**: `services/intent_service/preference_handler.py` (Phase 2)

### Integration Point 2: Chat Response Decorator ✅ (Designed)

**Where**: Response generation middleware
**When**: Before returning response to user
**What**: Optionally suggest detected preferences

**UI Pattern**:
```
[System Response]

─── 📊 We noticed something ───
Based on how you ask questions, you might prefer:
○ More concise responses (Confidence: 67%)
[Learn more] [Apply]
─────────────────────────
```

**Files**:
- Suggestion template: `templates/components/preference_suggestion.html` (Phase 2)
- API endpoint: `POST /api/v1/preferences/suggest/{hint_id}` (Phase 2)

### Integration Point 3: Learning System Hook ✅ (Designed)

**Where**: Learning system's `_apply_user_preference_pattern()` method
**When**: When preference is confirmed
**What**: Convert PreferenceConfirmation to LearnedPattern and store

**Data Flow**:
```
PreferenceConfirmation (from user accepting suggestion)
    ↓
Convert to LearnedPattern:
{
    pattern_type: PatternType.PREFERENCE,
    pattern_data: {
        dimension: PreferenceDimension.WARMTH,
        new_value: 0.8,
        previous_value: 0.6,
        hint_id: "hint_123"
    },
    confidence: 0.95,  # User explicitly confirmed
    metadata: {
        source: "conversation_learning",
        applied_by: "preference_confirmation_hook"
    }
}
    ↓
QueryLearningLoop._apply_user_preference_pattern()
    ↓
UserPreferenceManager.apply_preference_pattern()
    ↓
Stored in user preferences with TTL
```

**File**: Hook logic in `services/intent_service/preference_handler.py` (Phase 2)

### Integration Point 4: UserPreferenceManager Integration ✅ (Designed)

**Where**: UserPreferenceManager (existing)
**Method**: `apply_preference_pattern()`
**What**: Store confirmed preferences persistently

**Storage Key Pattern**:
```
Key: f"personality_{dimension}"
Example: "personality_warmth_level"

Value: {
    "new_value": 0.8,
    "previous_value": 0.6,
    "hint_id": "hint_123",
    "confirmed_at": "2025-11-22T14:30:00Z",
    "applied_at": "2025-11-22T14:30:01Z",
    "source": "conversation_learning"
}
```

---

## 4. Service Architecture

```
ConversationAnalyzer (services/personality/conversation_analyzer.py)
├─ analyze_message() → PreferenceDetectionResult
├─ analyze_response() → PreferenceDetectionResult
├─ analyze_feedback() → PreferenceDetectionResult
└─ Private detection methods:
   ├─ _detect_warmth_preference()
   ├─ _detect_action_preference()
   ├─ _detect_confidence_preference()
   └─ _detect_technical_preference()

Intent Service Integration Point (Phase 2)
├─ services/intent_service/preference_handler.py (NEW)
└─ PostIntentProcessing Hook
   ├─ Message Analysis
   ├─ Response Analysis
   └─ Preference Application

Personality Profile Integration (existing)
├─ PersonalityProfile (existing)
├─ PersonalityProfile.adjust_for_context() (existing)
└─ PersonalityProfile.get_response_style_guidance() (existing)

Learning System Integration (Phase 2)
├─ QueryLearningLoop._apply_user_preference_pattern() (existing)
└─ LearnedPattern (existing)

UserPreferenceManager Integration (existing)
└─ UserPreferenceManager.apply_preference_pattern() (existing)
```

---

## 5. Data Flow Diagrams

### Full User Journey

```
┌─────────────────────────────────────────────────────────────────┐
│ User sends message: "Can you explain this algorithm in detail?" │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                  [IntentService classifies]
                              ↓
         ┌─────────────────────────────────────────┐
         │ PreferenceDetectionHook (NEW)           │
         │ ├─ Load PersonalityProfile              │
         │ ├─ ConversationAnalyzer.analyze_message │
         │ │  └─ Detects: TECHNICAL + DETAILED     │
         │ │     confidence: 0.7                   │
         │ └─ Create PreferenceHint                │
         └─────────────────────────────────────────┘
                              ↓
                 [System generates response]
                              ↓
         ┌─────────────────────────────────────────┐
         │ ResponseAnalysisHook (NEW)              │
         │ ├─ Run analyze_response()               │
         │ ├─ Check user's reaction to response    │
         │ └─ Refine confidence if needed          │
         └─────────────────────────────────────────┘
                              ↓
          ┌──────────────────────────────────────────────┐
          │ System returns response to user              │
          │                                              │
          │ [Response content...]                        │
          │                                              │
          │ ── 📊 We noticed something ───               │
          │ Based on your questions, you might prefer:  │
          │ ○ More technical depth (Confidence: 70%)    │
          │ [Learn more] [Apply]                        │
          └──────────────────────────────────────────────┘
                              ↓
                 [User clicks "Apply"]
                              ↓
         ┌─────────────────────────────────────────┐
         │ PreferenceConfirmationHook (NEW)        │
         │ ├─ Create PreferenceConfirmation        │
         │ ├─ Apply to PersonalityProfile         │
         │ ├─ Store in UserPreferenceManager      │
         │ └─ Log to QueryLearningLoop            │
         └─────────────────────────────────────────┘
                              ↓
    ┌──────────────────────────────────────────────────┐
    │ LearnedPattern stored in database                │
    │ ├─ pattern_type: PREFERENCE                      │
    │ ├─ pattern_data: {dimension, new_value, hint_id}│
    │ ├─ confidence: 0.95 (user confirmed)            │
    │ └─ Persisted for future profile loading         │
    └──────────────────────────────────────────────────┘
                              ↓
              All future responses will use
          new technical_depth=DETAILED preference
```

---

## 6. Phase 1 Design Decisions

### Decision 1: Confidence-Based Suggestion vs Auto-Apply
✅ **DECIDED**:
- `confidence ≥ 0.4` → Suggest to user (wait for confirmation)
- `confidence ≥ 0.9` + explicit evidence → Auto-apply silently
- Rationale: User autonomy + signal strength = safety

### Decision 2: Word List vs ML Classification
✅ **DECIDED**:
- Use curated word lists for Phase 1 (simple, interpretable)
- ML classification can be added in Phase 2 enhancement
- Rationale: MVP needs interpretability for user trust

### Decision 3: Where to Integrate
✅ **DECIDED**:
- Hook into IntentService (after classification)
- Before response generation (in-flight detection)
- After response sent (reaction analysis)
- Rationale: Central point, minimum disruption

### Decision 4: Storage Strategy
✅ **DECIDED**:
- PreferenceHint → Session-scoped (temporary signal)
- PreferenceConfirmation → User-scoped (persistent)
- LearnedPattern → Learning system (historical + analytics)
- Rationale: Right durability level for each type

---

## 7. Test Strategy (Preview for Phase 3)

**Unit Tests** (30+ tests):
- `test_preference_hint_creation.py` - Hint validation
- `test_conversation_analyzer.py` - Detection logic
  - Language pattern detection (20 test cases)
  - Confidence scoring (10 test cases)
  - Hint ready-for-suggestion checks (5 test cases)
  - Auto-apply eligibility (5 test cases)
- `test_preference_confirmation.py` - Confirmation flow

**Integration Tests** (15+ tests):
- Intent handler hook integration
- Learning system integration
- UserPreferenceManager storage
- End-to-end message → hint → confirmation → storage

**Manual Tests**:
- Type messages with warm/professional language
- Verify hints are created with correct dimension
- Accept hint and verify PersonalityProfile updates
- Verify learning system has record

---

## 8. Remaining Phase 1 Tasks

- [x] Create preference detection models
- [x] Create ConversationAnalyzer service
- [x] Design integration points
- [ ] Create intent handler hook skeleton
- [ ] Document integration architecture
- [ ] Create Phase 1 completion summary

**Estimated Time**: 30-45 minutes remaining
**Total Phase 1**: ~1.5-2 hours (on track)

---

## 9. Stop Condition Check 🚦

**Question**: Are all designs validated?

**Check**:
- ✅ Models are concrete and testable
- ✅ Service logic is clear
- ✅ Integration points are identified
- ✅ No architectural conflicts found
- ✅ Existing infrastructure supports design

**Result**: ✅ NO STOP CONDITIONS - Ready for Phase 2

---

## 10. Transition to Phase 2

When Phase 1 complete:

1. **File the intent handler hook skeleton** (Phase 2.1)
2. **Implement detection patterns** (Phase 2.2)
3. **Implement confirmation flow** (Phase 2.3)
4. **Implement application logic** (Phase 2.4)
5. **Add intent handler hook** (Phase 2.5)

Each phase validates we're on track before continuing.

---

**Phase 1 Status**: 🔨 IN PROGRESS (est. 30-45 min remaining)
**All deliverables tracking to completion within time estimates** ✅
