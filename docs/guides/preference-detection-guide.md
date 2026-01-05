# Preference Detection - Integration Guide

**For Developers**: How to integrate preference detection into your application

---

## Quick Start

### 1. Enable Preference Detection in Your Intent Handler

In your intent service, the preference detection is automatically integrated via hooks:

```python
from services.intent_service.classifier import IntentClassifier
from services.intent_service.preference_handler import PreferenceDetectionHandler

# Preference detection is automatically enabled
classifier = IntentClassifier()
handler = PreferenceDetectionHandler()

# When classifying an intent, preferences are detected automatically
result = await classifier.classify(user_id, message)

# result.intent now includes:
# result.intent.preferences = {
#   "hints": [...],
#   "has_suggestions": True,
#   "has_auto_applies": False,
#   "analysis_summary": "..."
# }
```

### 2. Include Preferences in Your Response

When returning the response to the user:

```python
from services.intent.intent_service import IntentService

intent_service = IntentService()
result = await intent_service.process_intent(user_id, message, session_id)

# Include preferences in JSON response
response = {
    "response": result.response,
    "preferences": result.preferences  # Automatically set by hooks
}

return response
```

### 3. Handle Preference Acceptance on Frontend

When user clicks "Accept" on a preference suggestion:

```javascript
// In your JavaScript code
async function acceptPreference(hintId) {
    const response = await fetch(
        `/api/v1/preferences/hints/${hintId}/accept`,
        {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({session_id: getCurrentSessionId()})
        }
    );

    const result = await response.json();
    if (result.success) {
        showToast(`Preference updated! ${result.message}`, 'success');
        // Optionally refresh profile
        updatePersonalityProfile();
    }
}
```

---

## Architecture Overview

```
User Message (with intent + context)
    ↓
IntentClassifier.classify()
    ├─ Classify intent
    ├─ Call hooks.on_intent_classified()
    │   ├─ Load PersonalityProfile
    │   ├─ Run ConversationAnalyzer.analyze_message()
    │   ├─ Filter by confidence thresholds
    │   ├─ Store hints in session
    │   └─ Auto-apply high-confidence hints
    ↓
IntentProcessingResult with:
    ├─ intent (with preferences attached)
    ├─ response
    └─ preferences: {hints, has_suggestions, has_auto_applies}
    ↓
Frontend receives response
    ├─ Display main response
    └─ Display preference suggestions
    ↓
User confirms/rejects
    ↓
POST /api/v1/preferences/hints/{id}/accept
    ↓
PreferenceDetectionHandler.confirm_preference()
    ├─ Retrieve hint from session
    ├─ Create confirmation record
    ├─ Store in UserPreferenceManager
    ├─ Log to learning system
    └─ Apply to personality profile
    ↓
All future responses reflect updated preferences
```

---

## Integration Points

### 1. Intent Classification System

**File**: `services/intent_service/classifier.py`

Preferences are automatically detected after intent classification:

```python
class IntentClassifier:
    async def classify(self, user_id: str, message: str):
        # ... existing classification logic ...

        # Preferences are automatically detected via hooks
        # See IntentProcessingHooks.on_intent_classified()

        # Return intent with preferences attached
        return intent
```

**What it does**:
- Runs ConversationAnalyzer on the message
- Filters hints by confidence thresholds
- Stores suggested hints in session (30-min TTL)
- Auto-applies high-confidence hints

### 2. Intent Service

**File**: `services/intent_service/intent_service.py`

Preferences are extracted and propagated to response:

```python
class IntentService:
    async def process_intent(self, user_id, message, session_id):
        # ... intent processing ...

        # Extract preferences from intent
        result.preferences = intent.preferences

        return result  # Includes preferences
```

### 3. HTTP Response Layer

**File**: `web/app.py`

Preferences are included in API response:

```python
@app.post("/api/v1/intent")
async def intent_endpoint(request):
    result = await intent_service.process_intent(...)

    return {
        "response": result.response,
        "preferences": result.preferences  # ← Included here
    }
```

### 4. Preference Handler

**File**: `services/intent_service/preference_handler.py`

Manages the full preference lifecycle:

```python
handler = PreferenceDetectionHandler()

# Store hints in session (called by hooks)
await handler._store_hints_in_session(session_id, hints)

# Retrieve hint when user confirms
hint = await handler._retrieve_hint_from_session(session_id, hint_id)

# Process confirmation (accept/reject)
result = await handler.confirm_preference(
    user_id=user_id,
    session_id=session_id,
    hint_id=hint_id,
    accepted=True
)

# Apply auto-preferences (high confidence)
await handler.apply_auto_preferences(
    user_id=user_id,
    session_id=session_id,
    hints=auto_apply_hints
)
```

### 5. Conversation Analyzer

**File**: `services/personality/conversation_analyzer.py`

Detects preferences from message text:

```python
analyzer = ConversationAnalyzer()

profile = await PersonalityProfile.load_with_preferences(user_id)

result = analyzer.analyze_message(
    user_id=user_id,
    message=message,
    current_profile=profile
)

# result contains:
# - hints: All detected preferences
# - suggested_hints: Those ready for user confirmation (≥0.4)
# - auto_apply_hints: Those ready for silent application (≥0.9 + explicit)
# - analysis_summary: Human-readable explanation
```

---

## Adding Custom Detection

### Extend ConversationAnalyzer

To add your own detection logic:

```python
from services.personality.conversation_analyzer import ConversationAnalyzer
from services.personality.preference_detection import PreferenceHint, DetectionMethod

class CustomAnalyzer(ConversationAnalyzer):
    def _detect_custom_preference(self, user_id, message, current_profile):
        """Detect custom preference from message"""

        # Your custom detection logic
        if your_condition:
            return PreferenceHint(
                id=self._next_hint_id(),
                user_id=user_id,
                dimension=PreferenceDimension.YOUR_DIMENSION,
                detected_value=your_value,
                current_value=current_profile.your_field,
                detection_method=DetectionMethod.CUSTOM_METHOD,
                confidence_score=your_score,
                source_text=message,
                evidence={...}
            )
        return None

    async def analyze_message(self, user_id, message, current_profile):
        """Override to include custom detection"""
        result = await super().analyze_message(user_id, message, current_profile)

        # Add custom detection
        custom_hint = self._detect_custom_preference(user_id, message, current_profile)
        if custom_hint:
            result.hints.append(custom_hint)
            if custom_hint.is_ready_for_suggestion():
                result.suggested_hints.append(custom_hint)

        return result
```

### Add Custom Detection Method

Add to `services/personality/preference_detection.py`:

```python
class DetectionMethod(Enum):
    """Methods for detecting preferences"""
    LANGUAGE_PATTERNS = "language_patterns"
    BEHAVIORAL_SIGNALS = "behavioral_signals"
    EXPLICIT_FEEDBACK = "explicit_feedback"
    RESPONSE_ANALYSIS = "response_analysis"
    YOUR_METHOD = "your_method"  # ← Add here
```

---

## Customizing Thresholds

### Suggestion Threshold

Change when preferences appear as suggestions:

```python
# In services/personality/conversation_analyzer.py

# Increase to only show high-confidence suggestions
SUGGESTION_THRESHOLD = 0.5  # Default: 0.4

# Then in PreferenceHint
def is_ready_for_suggestion(self) -> bool:
    return self.confidence_score >= SUGGESTION_THRESHOLD
```

### Auto-Apply Threshold

Change when preferences are applied silently:

```python
# In services/personality/preference_detection.py

# Increase to require very high confidence for auto-apply
AUTO_APPLY_THRESHOLD = 0.95  # Default: 0.9

# Then in PreferenceHint
def is_ready_for_auto_apply(self) -> bool:
    # Also requires explicit source (not just high confidence)
    return (
        self.confidence_score >= AUTO_APPLY_THRESHOLD and
        self.detection_method == DetectionMethod.EXPLICIT_FEEDBACK
    )
```

### Session TTL

Change how long preference suggestions stay available:

```python
# In services/intent_service/preference_handler.py

SESSION_HINT_TTL_MINUTES = 60  # Default: 30

# Hints older than this are automatically expired
```

---

## Disabling Features

### Disable Preference Detection Entirely

```python
# In web/app.py or your initialization

from services.intent_service.intent_hooks import IntentProcessingHooks

# Create hooks without preference handler
hooks = IntentProcessingHooks(preference_handler=None)
# Preference detection will be skipped
```

### Disable Auto-Apply (Require User Confirmation)

```python
# In services/personality/preference_detection.py

# Set auto-apply threshold impossibly high
AUTO_APPLY_THRESHOLD = 1.1  # Never auto-apply

# Now users must confirm all preferences
```

### Disable Specific Detection Methods

```python
# In services/personality/conversation_analyzer.py

async def analyze_message(self, user_id, message, current_profile):
    result = PreferenceDetectionResult()

    # Only run language patterns, skip others
    warmth = self._detect_warmth_preference(...)
    if warmth:
        result.hints.append(warmth)

    # Skip other detection methods
    # (comment out _detect_confidence_preference, etc.)

    return result
```

---

## Monitoring & Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('services.personality.conversation_analyzer')
logger.setLevel(logging.DEBUG)
```

This will log:
- Each detected preference
- Confidence scores
- Filtering decisions
- Session storage operations

### Health Check

```bash
curl http://localhost:8001/api/v1/preferences/health
```

Returns status of all components:
- analyzer: Preference detection engine
- storage: Session hint storage
- learning_integration: Learning system integration
- preference_manager: Persistent storage

### Get Stats

```bash
curl http://localhost:8001/api/v1/preferences/stats
```

Shows:
- Total preferences detected
- Total preferences applied
- Breakdown by dimension
- Detection methods used

---

## Error Handling

### Handle Preference Detection Errors

Preference detection failures don't block intent processing:

```python
# If preference detection fails, the system continues
# Check if preferences are present in result

if result.preferences and result.preferences.get('has_suggestions'):
    # Show suggestions to user
    pass
else:
    # No suggestions (might be error or no signals)
    # Continue without preference UI
    pass
```

### Retry Failed Confirmations

```python
async def confirm_preference_with_retry(hint_id, session_id):
    for attempt in range(3):
        try:
            result = await handler.confirm_preference(
                user_id=user_id,
                session_id=session_id,
                hint_id=hint_id,
                accepted=True
            )
            if result['success']:
                return result
        except Exception as e:
            logger.error(f"Attempt {attempt+1} failed: {e}")
            await asyncio.sleep(1)  # Back off

    raise Exception("Failed to confirm preference after retries")
```

---

## Performance Optimization

### Cache Analyzer Instance

```python
# Good: Create once, reuse
analyzer = ConversationAnalyzer()

# Don't do this (creates new instance per call)
async def process(message):
    analyzer = ConversationAnalyzer()  # ← Avoid
    return analyzer.analyze_message(...)
```

### Batch Preference Confirmations

```python
# If multiple preferences from one message
confirmations = []
for hint in result.preferences['hints']:
    confirmation = await handler.confirm_preference(
        user_id=user_id,
        session_id=session_id,
        hint_id=hint.id,
        accepted=True
    )
    confirmations.append(confirmation)

# All confirmations processed
return {"confirmations": confirmations}
```

### Use Connection Pooling

```python
# Ensure database connections are pooled
# (Handled automatically by SQLAlchemy, but verify in production)
```

---

## Testing Integration

### Unit Test Your Integration

```python
@pytest.mark.asyncio
async def test_preference_integration():
    # Setup
    analyzer = ConversationAnalyzer()
    handler = PreferenceDetectionHandler()
    profile = create_mock_profile()

    # Test detection
    message = "I'd like more technical detail"
    result = analyzer.analyze_message(user_id, message, profile)

    assert result.has_suggestions()
    assert len(result.suggested_hints) > 0

    # Test confirmation
    hint = result.suggested_hints[0]
    confirmation = await handler.confirm_preference(
        user_id=user_id,
        session_id=session_id,
        hint_id=hint.id,
        accepted=True
    )

    assert confirmation['success']
```

---

## Common Issues & Solutions

### Preferences Not Detected

**Issue**: ConversationAnalyzer returns empty hints

**Solution**:
1. Check message contains preference signal words
2. Verify confidence score calculation
3. Check current_profile is loaded correctly
4. Enable debug logging to see word matching

### Preferences Not Persisting

**Issue**: Preference accepted but doesn't affect future responses

**Solution**:
1. Verify UserPreferenceManager.set_preference() succeeded
2. Check PersonalityProfile.load_with_preferences() returns updated values
3. Verify learning system integration logs the preference
4. Check database connection and permissions

### Slow Preference Detection

**Issue**: analyze_message() takes >100ms

**Solution**:
1. Reduce word set sizes (fewer words = faster matching)
2. Cache analyzer instance (don't recreate per request)
3. Profile with Python cProfile to find bottleneck
4. Consider running in background job for large messages

---

## Next Steps

1. **Integrate** into your intent service (see Quick Start above)
2. **Add UI** to display preference suggestions (see preference-detection.md)
3. **Configure** thresholds for your use case
4. **Test** with real users (see #375 for manual testing)
5. **Monitor** via health endpoint and stats

---

**Last Updated**: November 22, 2025
**Status**: Production Ready ✅
**Related**: #248 (CONV-LEARN-PREF)
