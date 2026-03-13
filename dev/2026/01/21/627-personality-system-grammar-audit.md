# Issue #627: Personality System Grammar Audit

## Audit Date: 2026-01-21

## 1. System Overview

The Personality System is **largely grammar-compliant** due to previous work:
- Issue #619: Created WarmthCalibration and PersonalityBridge
- Issue #632: Integrated consciousness patterns into StandupToChatBridge

### Components Analyzed
- `services/personality/personality_profile.py` - PersonalityProfile, ResponseContext
- `services/personality/standup_bridge.py` - StandupToChatBridge (uses consciousness)
- `services/intent_service/warmth_calibration.py` - WarmthCalibrator (Pattern-053)
- `services/intent_service/personality_bridge.py` - PersonalityBridge (Pattern-052)
- `services/consciousness/standup_consciousness.py` - Standup consciousness patterns

### Architecture
```
User Message → Intent Classification → PersonalityBridge → IntentUnderstanding
                                          ↓
                      WarmthCalibrator → WarmthCalibration
                                          ↓
                                    Conscious Response
```

## 2. Compliance Assessment

### 2.1 Already Compliant Components

| Component | Status | Notes |
|-----------|--------|-------|
| WarmthCalibration | ✅ | Pattern-053, place-aware warmth calibration |
| PersonalityBridge | ✅ | Pattern-052, perception modes, confidence expression |
| StandupToChatBridge | ✅ | Uses consciousness patterns (#632) |
| PersonalityProfile | ⚠️ | Has context adjustment but no explicit lens support |

### 2.2 Grammar Element Coverage

| Element | Status | Implementation |
|---------|--------|----------------|
| Entity | ✅ | Piper identity expressed via "I" statements |
| Moment | ✅ | Standup as conscious narrative |
| Place | ✅ | WarmthCalibrator considers PlaceType |
| Lenses | ⚠️ | Limited - only confidence-based |
| Situation | ⚠️ | Context adjustment exists but could be richer |

## 3. Gap Analysis

### 3.1 Missing: PersonalityResponseContext

The system lacks a unified context dataclass that captures:
- User's personality preferences (from PersonalityProfile)
- Current situation (error, success, clarification)
- Relationship state (first interaction, repeat user)
- Lens application (Collaborative, Temporal, Spatial)

This context would enable richer, more consistent personality expression.

### 3.2 Missing: Explicit Lens Application

Current PersonalityProfile adjusts for intent confidence but doesn't explicitly
apply grammar lenses:
- **Collaborative Lens**: User-Piper relationship awareness
- **Temporal Lens**: Time pressure, deadlines, pace
- **Spatial Lens**: Context proximity, scope awareness

### 3.3 Missing: Narrative Helpers for Personality

No helper functions exist to:
- Apply personality to arbitrary response content
- Get warmth-appropriate phrases for common situations
- Bridge personality profile to grammar-conscious output

## 4. Transformation Plan

### Phase 1: PersonalityResponseContext
Create `services/personality/response_context.py`:
- Captures personality profile summary
- Current situation type
- Applicable lenses
- Relationship indicators

### Phase 2: PersonalityNarrativeBridge
Create `services/personality/narrative_bridge.py`:
- Situation-aware tone phrases
- Lens-informed adjustments
- Formality calibration narratives

### Phase 3: Narrative Helpers
Create `services/personality/narrative_helpers.py`:
- apply_personality_to_message()
- get_situation_tone()
- narrate_relationship_context()

### Phase 4: Integration
Update `services/personality/__init__.py` with exports

## 5. Estimated Scope

- Response Context: ~6 tests (simpler than calendar/feedback)
- Narrative Bridge: ~15 tests
- Narrative Helpers: ~8 tests
- Total: ~29 tests

## 6. Acceptance Criteria Mapping

| Criteria | Implementation |
|----------|----------------|
| Consistent Piper personality | PersonalityNarrativeBridge tone phrases |
| Situation-aware tone | PersonalityResponseContext situation types |
| Multiple lenses inform personality | Explicit lens application in context |
| Passes experience test | Contractor Test verification in tests |
