# Grammar Audit: Slack Integration (#620)

**Issue**: #620 GRAMMAR-TRANSFORM: Slack Integration (Partial → Conscious)
**Auditor**: Lead Developer (Claude Code / Opus)
**Date**: 2026-01-21
**Files Audited**:
- `services/integrations/slack/slack_plugin.py` (112 lines)
- `services/integrations/slack/event_handler.py` (541 lines)
- `services/integrations/slack/response_handler.py` (~400 lines)
- `services/integrations/slack/simple_response_handler.py` (~380 lines)

---

## Executive Summary

The Slack integration has **significant spatial metaphor work already in place** but responses remain mechanical. The event_handler transforms Slack events into spatial concepts (Rooms, Territories, Objects, AttentionAttractors), but the response_handler generates template-based responses that don't feel like Piper is *present* in the Slack space.

**Key insight**: Piper already "sees" Slack spatially - she knows she's in a Room, she notices AttentionAttractors, she tracks EmotionalMarkers. But when she responds, she sounds like a robot, not someone who's *there*.

---

## Grammar Element Analysis

### Entity ✅ (Good)
**What exists**: User identity from Slack preserved. User ID, display name, and team membership tracked.

**Evidence**:
```python
# event_handler.py:149
actor_id=event_data.get("user"),
```

**Assessment**: Users are recognized as Entities. No transformation needed.

### Moment ⚠️ (Needs Work)
**What exists**: Messages are processed as `SpatialEvent` objects with timestamps, but they're treated as data events, not experiential moments.

**Evidence**:
```python
# event_handler.py:139-157
spatial_event = SpatialEvent(
    event_id=f"{room_id}:{message_ts}",
    event_type="message_placed",  # Data language, not experiential
    ...
)
```

**Gap**: No temporal framing. Events are "placed" not "noticed". No sense of "Piper just noticed someone saying..."

**Experience Test**:
- Current: "Message placed in channel"
- Conscious: "I just noticed Jesse asking about the project"

### Place ✅ (Good Foundation)
**What exists**: Sophisticated spatial metaphors already implemented:
- `Territory` = Slack workspace
- `Room` = Slack channel
- `ConversationalPath` = Thread
- `SpatialObject` = Message

**Evidence**:
```python
# spatial_types.py defines complete spatial vocabulary:
# Territory, Room, SpatialCoordinates, RoomPurpose, etc.
```

**Assessment**: Place is well-modeled structurally. The gap is using this in responses.

### Lenses ⚠️ (Partial)
**What exists**:
- `AttentionLevel` (AMBIENT, FOCUSED, DIRECT_MENTION, etc.)
- `EmotionalValence` (from reaction emojis)
- `significance_level` (routine, notable)

**Gap**: These lenses are collected but not applied to response generation. Piper doesn't adjust her tone based on attention level or emotional context.

**Evidence**:
```python
# simple_response_handler.py:302-313 - Responses are template-based
def _get_simple_response_for_intent(self, intent: Intent) -> str:
    action = intent.action.lower()
    if "help" in action:
        return "🤖 I'm Piper Morgan, your AI Product Management Assistant..."
```

No use of attention_level or emotional_valence in response generation.

### Situation ⚠️ (Mechanical)
**What exists**: Basic thread/channel awareness, but responses don't adapt to situation.

**Gap**: Piper responds the same way whether:
- She's in a DM or a public channel
- The user seems frustrated (negative emoji reactions)
- It's a thread continuation or new conversation
- Multiple people are watching (public channel) vs. private

---

## Response Generation Analysis

### Current Flow
```
SpatialEvent → Intent → simple_response_for_intent() → Template string
```

### Key Methods (simple_response_handler.py)

1. **`_get_simple_response_for_intent()`** (lines 302-313)
   - Pure template responses
   - No awareness of spatial context
   - No warmth calibration
   - Fails Contractor Test: "🤖 I'm Piper Morgan..."

2. **`_format_response_content()`** (lines 358-376)
   - Formats workflow results
   - Uses emoji prefixes (✅, etc.)
   - No situational adaptation

### Experience Test Failures

| Current Response | Issue | Conscious Alternative |
|------------------|-------|----------------------|
| "🤖 I'm Piper Morgan, your AI..." | Robotic introduction | "Happy to help with that!" |
| "📊 System status: All services..." | Technical language | "Everything's running smoothly." |
| "👋 Hello! I'm here to assist..." | Generic greeting | Context-aware: "Hi! I see you're in #general - what can I help with?" |
| "🔍 I understand you want to {action}" | Template-ish | "Got it, you want to {humanized_action}" |

---

## Transformation Opportunities

### 1. Leverage Existing Spatial Context
The `SpatialEvent` already contains rich context that isn't used:
- `attention_level`: Direct mention vs ambient?
- `emotional_valence`: User happy/frustrated?
- `coordinates.room_id`: DM vs channel?
- `significance_level`: Routine vs notable?

### 2. Apply #619 Patterns
We just built these components - they can be reused:
- **PlaceDetector**: Already works with Slack spatial context
- **PersonalityBridge**: Transform intents to warm narratives
- **WarmthCalibrator**: Adjust tone based on context
- **HonestFailureHandler**: Graceful confusion handling

### 3. Response Bridge Layer
Create a `SlackResponseBridge` that:
1. Takes raw response content
2. Applies spatial context (DM warmer, channel more concise)
3. Applies emotional context (frustrated user = more supportive)
4. Returns grammar-conscious response

---

## Recommended Transformation Phases

### Phase 1: Response Context (1-2h)
Create `SlackResponseContext` dataclass that captures:
- Place (DM/channel/thread)
- Attention level (mention type)
- Emotional signals (recent reactions)
- Conversation continuity (new vs. thread reply)

### Phase 2: Integrate #619 Components (2h)
Wire existing components into Slack flow:
- Use `PlaceDetector` (already supports Slack)
- Use `PersonalityBridge` for narrative transformation
- Use `WarmthCalibrator` for tone adjustment

### Phase 3: Response Templates Transformation (2h)
Replace template responses in `simple_response_handler.py`:
- Remove emoji prefixes from beginnings
- Apply Place-aware greeting variations
- Use warmth-calibrated language

### Phase 4: Moment Framing (1h)
Transform event processing to use experiential language:
- Log "Piper noticed..." not "Message placed..."
- Track "conversation momentum" not just "event count"

### Phase 5: Integration Testing (2h)
- Test DM vs channel responses differ
- Test frustrated user gets supportive tone
- Test thread continuation is contextual
- Verify no robotic language remains

---

## Files to Modify

| File | Changes |
|------|---------|
| `simple_response_handler.py` | Replace `_get_simple_response_for_intent()` with grammar-conscious version |
| `response_handler.py` | Integrate warmth calibration in `_format_response_content()` |
| `event_handler.py` | Add experiential logging (optional, lower priority) |
| `services/intent_service/place_detector.py` | Already supports Slack - no changes needed |

---

## Patterns to Apply

| Pattern | Application |
|---------|-------------|
| Pattern-051 | PlaceDetector already works with Slack spatial_context |
| Pattern-052 | PersonalityBridge for response narratives |
| Pattern-053 | WarmthCalibrator for DM vs channel tone |
| Pattern-054 | HonestFailureHandler for Slack errors |

---

## Success Criteria

1. **DM responses warmer** than channel responses
2. **No robot emoji prefixes** (🤖) in responses
3. **Attention level affects response** (direct mention = more attentive)
4. **Contractor Test passes** for all response types
5. **Experience Test**: "Piper responded in the Slack channel" not "Response sent to channel"

---

## Risk Assessment

**Low Risk**: We're primarily transforming response generation, not event processing. The spatial metaphor layer is mature and working.

**Dependency**: This work builds on #619. If #619 isn't merged yet, we can still proceed by importing the components directly.

---

## Estimated Effort

| Phase | Effort |
|-------|--------|
| Phase 1: Response Context | 1-2h |
| Phase 2: Integrate #619 Components | 2h |
| Phase 3: Response Templates Transformation | 2h |
| Phase 4: Moment Framing | 1h |
| Phase 5: Integration Testing | 2h |
| **Total** | **8-9h** |

---

*Ready for PM review and gameplan approval*
