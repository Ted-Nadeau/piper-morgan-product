# Grammar Audit: Intent Classification (#619)

**Auditor**: Lead Developer (Claude Code)
**Date**: 2026-01-21
**File**: `services/intent_service/classifier.py`
**Lines**: 1047 (IntentClassifier class: 44-1047)

---

## Executive Summary

The IntentClassifier is a ~1000-line class responsible for understanding what users want. It works well mechanically but treats intent as **data extraction** rather than **understanding a person**. The core transformation opportunity: make Piper *notice* what someone wants rather than *process* their query.

---

## Grammar Element Analysis

### Entity: ✅ Present but Shallow

**Evidence**:
- User ID tracked: `user_id = context.get("user_id") if context else None` (line 150, 203, 307)
- Preference handler attached: `self.preference_handler = PreferenceDetectionHandler()` (line 73)

**Deficit**:
- Entity is an ID, not a person with history and personality
- No user preference memory applied during classification
- Intent belongs to a "message" not to a "person expressing themselves"

**Grammar Gap**: The Entity exists but isn't *known* — we don't ask "what does this person usually want?" or "how do they typically ask?"

---

### Moment: ⚠️ Events Without Experience

**Evidence**:
- Timestamp captured: `"timestamp": datetime.now().isoformat()` (line 219)
- Learning signals identified after classification (line 291)

**Deficit**:
- Intent is "classified" not "understood"
- The Moment of recognition isn't framed as Piper's experience
- Current language: "Classification failed" (line 346) — mechanical, not experiential
- Pre-classifier returns `pre_intent` — data, not insight

**Grammar Gap**: No PerceptionMode framing. Should be:
- NOTICING: "I'm noticing you want to..."
- REMEMBERING: "Last time you asked about X..."
- ANTICIPATING: "You might also want to..."

---

### Place: ❌ Context-Agnostic

**Evidence**:
- Spatial context passed but not used meaningfully:
  ```python
  spatial_context: Optional[Dict] = None
  ```
- Response target built from spatial_context (line 465-469) but only for routing, not personality

**Deficit**:
- Classification works identically whether from Slack, CLI, or web
- No awareness of "where this conversation is happening"
- Place could inform confidence thresholds, response verbosity, formality

**Grammar Gap**: Critical. The Place is ignored entirely:
- Slack DM → more casual
- Public channel → more formal
- CLI → more terse
- Web chat → more conversational

---

### Lenses: ⚠️ Single-Dimensional

**Currently Applied**:
- **Confidence lens** (implicit): Different paths for high/low confidence
- **Temporal lens** (partial): Timestamp captured but not applied

**Not Applied**:
- **Contextual lens**: Conversation history not used for classification
- **Collaborative lens**: Intent doesn't consider who else is involved
- **Priority lens**: Urgency not detected
- **Flow lens**: Position in workflow not considered
- **Causal lens**: Why are they asking this now?

**Grammar Gap**: Classification happens in a vacuum. A rich classification would know:
- "This is their third question about the same topic" (Contextual)
- "They seem frustrated" (Priority/urgency)
- "This follows up on yesterday's conversation" (Temporal)

---

### Situation: ✅ Functional but Mechanical

**Evidence**:
- Different handling for confidence levels (line 270-284)
- Vague intent detection triggers clarification (line 271)
- Error cases handled with structured errors (line 345-349)

**Deficit**:
- Situations are coded as conditionals, not as meaningful states
- Error message: `IntentClassificationFailedError` — technical, not human

---

## Key Methods Analysis

### `classify()` (lines 101-350)

**Current Flow**:
1. Check cache → return cached Intent
2. Try pre-classifier → return pre-classified Intent
3. Get graph context → for LLM hints
4. Call `_classify_with_reasoning()` → parse LLM response
5. Normalize action → map synonyms
6. Check confidence → request clarification if low
7. Run hooks → detect preferences
8. Return Intent object

**Grammar Issues**:
- Intent returned as data structure, not as "Piper's understanding"
- No warmth bridge before returning
- Cache hit doesn't acknowledge "I remember this pattern"

### `_classify_with_reasoning()` (lines 413-497)

**Current**: Builds prompt, calls LLM, parses JSON response.

**Grammar Issue**: The reasoning is extracted but never expressed. Piper has an understanding but doesn't share *why* she understood it that way.

### `_fallback_classify()` (lines 543-751)

**Current**: 200+ lines of keyword matching and pattern detection.

**Grammar Issue**: Fallback is purely mechanical. When Piper has to guess, she doesn't acknowledge uncertainty or ask gently. She just returns a lower confidence score.

---

## Experience Test

**Current Experience** (from user perspective):
> "I type something, get a response. Sometimes it asks for clarification."

**Target Experience** (grammar-conscious):
> "I type something, Piper acknowledges she understood, explains why she understood it that way if it's ambiguous, and adjusts her approach based on where we're talking."

---

## Transformation Opportunities

### High Impact

1. **Add Place-Aware Classification**
   - Detect channel type (Slack DM vs channel vs web vs CLI)
   - Adjust confidence thresholds by Place
   - Adjust response verbosity by Place

2. **Frame Understanding as Moment**
   - When returning Intent, add "understanding_narrative"
   - Apply PerceptionMode to classification result
   - Make fallback express appropriate uncertainty

3. **Apply Contextual Lens**
   - Check if user has asked similar questions recently
   - Reference previous conversation context
   - Build on existing understanding

### Medium Impact

4. **Warm the Fallback Path**
   - Instead of silent low-confidence, acknowledge uncertainty
   - "I'm not quite sure what you mean" instead of just low confidence

5. **Cache with Memory**
   - When returning cached result, note pattern recognition
   - "I remember you often ask about X"

---

## Recommended Transformation Approach

Based on the transformation guide, use this sequence:

1. **Pattern-050 (Context/Result Dataclass Pair)**
   - Create `IntentClassificationContext` capturing rich input
   - Create `IntentUnderstanding` as grammar-conscious result
   - Context includes Place awareness, user history hints

2. **Pattern-051 (Parallel Place Gathering)**
   - Detect Place type before classification
   - Fetch Place-appropriate settings (formality, verbosity)

3. **Pattern-052 (Personality Bridge)**
   - Transform `Intent` to `IntentUnderstanding`
   - Add understanding_narrative with PerceptionMode
   - Bridge method: `_make_understanding_personal()`

4. **Pattern-053 (Warmth Calibration)**
   - Calibrate response warmth by confidence level
   - Higher confidence → more decisive language
   - Lower confidence → gentler, more questioning

5. **Pattern-054 (Honest Failure)**
   - Replace `IntentClassificationFailedError` with graceful admission
   - "I'm having trouble understanding" not "Classification failed"

---

## Files to Modify

| File | Change Type | Scope |
|------|-------------|-------|
| `services/intent_service/classifier.py` | Major refactor | Add Context/Result pair, Place awareness, warmth |
| `services/intent_service/intent_types.py` | New dataclasses | IntentClassificationContext, IntentUnderstanding |
| `services/intent_service/place_detector.py` | New file | Detect Place from spatial_context |
| `services/shared_types.py` | Enum additions | PlaceType enum if not present |

---

## Risks and Mitigations

| Risk | Mitigation |
|------|-----------|
| Performance impact of Place detection | Cache Place determination per session |
| Breaking existing callers | IntentUnderstanding wraps Intent for compatibility |
| Over-personalization feeling forced | Keep warmth subtle, use Contractor Test |
| Scope creep | Stick to classification layer; don't change handlers |

---

## Estimated Effort

| Phase | Estimate | Notes |
|-------|----------|-------|
| Context/Result dataclasses | 1-2h | New types, bridge method |
| Place detection | 2h | Detect from spatial_context |
| Personality bridge | 2h | Transform output |
| Warmth calibration | 1h | Adjust by confidence |
| Honest failure | 1h | Improve error UX |
| Testing | 2h | Unit + experience tests |
| **Total** | **9-11h** | Spread across multiple sessions |

---

## Next Steps

1. **PM Review**: Get approval on this audit
2. **Gameplan**: Create detailed implementation gameplan
3. **Prompts**: Create agent prompts for parallel work

---

*Audit completed: 2026-01-21 7:15 PM PT*
*Following #625 cascade methodology*
