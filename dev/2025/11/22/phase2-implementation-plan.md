# Phase 2: Implementation - CONV-LEARN-PREF #248

**Date**: November 22, 2025
**Time**: 3:44 PM - Start
**Duration Target**: 4-5 hours
**Status**: 🔨 IN PROGRESS

---

## Overview

Phase 2 implements the preference detection system designed in Phase 1. This phase focuses on:

1. **Phase 2.1**: Detection pattern integration (1.5 hours)
2. **Phase 2.2**: Confirmation flow and UI (1.5 hours)
3. **Phase 2.3**: Application logic and storage (1 hour)
4. **Phase 2.4**: Intent handler hook integration (1 hour)

---

## Phase 2.1: Detection Pattern Integration (1.5 hours)

### Objective
Hook preference detection into the intent service pipeline so every user message is analyzed.

### Tasks

#### 2.1.1: Create Intent Service Integration Hook
**File**: `services/intent_service/intent_hooks.py` (NEW)

Purpose: Central hook dispatcher for post-intent processing

```python
class IntentProcessingHooks:
    """Hooks called after intent classification"""

    async def on_intent_classified(
        self,
        user_id: str,
        message: str,
        intent: Intent,
        session_id: Optional[str]
    ) -> Dict[str, Any]:
        """Called after intent is classified, before response generation"""
        # Run preference detection
        # Store hints in context
        # Return metadata
```

**Acceptance Criteria**:
- ✅ Hook receives: user_id, message, intent, session_id
- ✅ Calls PreferenceDetectionHandler.handle_message_analysis()
- ✅ Stores hints in session context (for later retrieval)
- ✅ Returns detection metadata
- ✅ No errors if handler fails (graceful degradation)

#### 2.1.2: Integrate Hook into Intent Classification Flow
**File**: `services/intent_service/classifier.py` (MODIFY)

Purpose: Call the hook after classifying intent

Current flow:
```python
def classify(user_id, message, context):
    intent = self._run_classification(message)  # Existing
    return intent
```

New flow:
```python
def classify(user_id, message, context):
    intent = self._run_classification(message)  # Existing

    # NEW: Run preference detection hook
    _ = await self._hooks.on_intent_classified(
        user_id, message, intent, context.get("session_id")
    )

    return intent
```

**Acceptance Criteria**:
- ✅ Hook called after classification
- ✅ Hook doesn't block response generation (async)
- ✅ No exceptions propagate (try/except)
- ✅ Hook failure doesn't affect intent results
- ✅ All existing tests still pass

#### 2.1.3: Add Preference Context to Intent Result
**File**: `services/intent_service/classifier.py` (MODIFY)

Purpose: Return preference hints with intent result

```python
# Existing Intent result
{
    "intent": "ask_question",
    "confidence": 0.92,
    "parameters": {...}
}

# Enhanced with preferences
{
    "intent": "ask_question",
    "confidence": 0.92,
    "parameters": {...},
    "preferences": {  # NEW
        "hints": [PreferenceHint.to_dict(), ...],
        "has_suggestions": bool,
        "analysis_summary": str
    }
}
```

**Acceptance Criteria**:
- ✅ Intent dict includes "preferences" key
- ✅ Preferences contains: hints, has_suggestions, analysis_summary
- ✅ Can be null/empty if no hints detected
- ✅ Serializable to JSON
- ✅ Doesn't break existing code expecting old format

---

## Phase 2.2: Confirmation Flow and UI (1.5 hours)

### Objective
Enable users to see and accept/reject preference suggestions.

### Tasks

#### 2.2.1: Create Preference Suggestion Component
**File**: `templates/components/preference_suggestion.html` (NEW)

Purpose: UI component to display detected preferences

```html
<div class="preference-suggestion" id="pref-hint-{{ hint_id }}">
  <div class="suggestion-header">
    <span class="icon">💡</span>
    <strong>We noticed something</strong>
  </div>

  <p class="suggestion-text">{{ explanation }}</p>

  <div class="suggestion-meta">
    <span class="confidence">{{ confidence_level }}</span>
    <span class="confidence-score">{{ confidence_score }}% confident</span>
  </div>

  <div class="suggestion-actions">
    <button class="btn-accept" onclick="acceptPreference('{{ hint_id }}')">
      ✓ Apply
    </button>
    <button class="btn-dismiss" onclick="dismissPreference('{{ hint_id }}')">
      ✗ Not now
    </button>
  </div>
</div>

<style>
.preference-suggestion {
  border-left: 4px solid #667eea;
  background: #f8f9ff;
  padding: 12px 16px;
  margin: 16px 0;
  border-radius: 4px;
  font-size: 14px;
}

.suggestion-header {
  margin-bottom: 8px;
  font-weight: 600;
}

.confidence-score {
  display: inline-block;
  background: #e0e5ff;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  margin-left: 8px;
}

.suggestion-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.btn-accept, .btn-dismiss {
  padding: 6px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
}

.btn-accept {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.btn-accept:hover {
  background: #5568d3;
}

.btn-dismiss {
  background: white;
  color: #666;
}

.btn-dismiss:hover {
  background: #f5f5f5;
}
</style>
```

**Acceptance Criteria**:
- ✅ Displays hint explanation (from PreferenceDetectionHandler)
- ✅ Shows confidence score
- ✅ Has "Apply" and "Not now" buttons
- ✅ Styled consistently with app design
- ✅ Accessible (semantic HTML, ARIA labels)

#### 2.2.2: Create Preference API Endpoint
**File**: `web/api/routes/preferences.py` (NEW)

Purpose: Handle user's acceptance/rejection of preferences

```python
@router.post("/preferences/hints/{hint_id}/accept")
async def accept_preference(
    hint_id: str,
    session_id: str,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """User accepted a preference suggestion"""

    # Call handler to confirm and apply
    result = await handler.confirm_preference(
        user_id=current_user.id,
        session_id=session_id,
        hint_id=hint_id,
        accepted=True
    )

    return result

@router.post("/preferences/hints/{hint_id}/dismiss")
async def dismiss_preference(
    hint_id: str,
    session_id: str,
    current_user: User = Depends(get_current_user),
) -> Dict[str, Any]:
    """User dismissed a preference suggestion"""

    # Log dismissal for learning system
    result = await handler.confirm_preference(
        user_id=current_user.id,
        session_id=session_id,
        hint_id=hint_id,
        accepted=False
    )

    return result
```

**Acceptance Criteria**:
- ✅ POST `/api/v1/preferences/hints/{hint_id}/accept`
- ✅ POST `/api/v1/preferences/hints/{hint_id}/dismiss`
- ✅ Requires authentication
- ✅ Updates user profile on accept
- ✅ Logs dismissal on dismiss (for learning)
- ✅ Returns success/error status

#### 2.2.3: Add Suggestion Rendering to Chat Component
**File**: `templates/conversation.html` (MODIFY)

Purpose: Display preference suggestions after each response

Current flow:
```html
<div class="message system">
  {{ response_text }}
</div>
```

New flow:
```html
<div class="message system">
  {{ response_text }}

  {% if preferences.has_suggestions %}
    <!-- Include preference suggestion component -->
    {% for hint in preferences.hints %}
      {% include "components/preference_suggestion.html" with hint=hint %}
    {% endfor %}
  {% endif %}
</div>
```

**Acceptance Criteria**:
- ✅ Suggestions shown after response text
- ✅ Only shown if confidence ≥ 0.4
- ✅ JavaScript handlers for accept/dismiss
- ✅ No layout disruption if no suggestions
- ✅ Works with existing chat styling

#### 2.2.4: Create Client-side Handler
**File**: `static/js/preferences.js` (NEW)

Purpose: Handle suggestion button clicks

```javascript
async function acceptPreference(hintId) {
    const sessionId = getCurrentSessionId();

    try {
        const response = await fetch(
            `/api/v1/preferences/hints/${hintId}/accept`,
            {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({session_id: sessionId})
            }
        );

        const result = await response.json();

        if (result.success) {
            // Hide suggestion element
            document.getElementById(`pref-hint-${hintId}`).remove();
            // Show toast: "Preference updated!"
            showToast('Preference updated!', 'success');
        }
    } catch (error) {
        console.error('Error accepting preference:', error);
        showToast('Error updating preference', 'error');
    }
}

async function dismissPreference(hintId) {
    // Similar to accept, but calls /dismiss endpoint
    // Hide without persisting
}
```

**Acceptance Criteria**:
- ✅ Accept button calls API
- ✅ Dismiss button calls API
- ✅ Shows success/error toast
- ✅ Removes suggestion from UI
- ✅ No page reload needed

---

## Phase 2.3: Application Logic and Storage (1 hour)

### Objective
Implement the full preference confirmation → storage → profile update flow.

### Tasks

#### 2.3.1: Implement Preference Application in Handler
**File**: `services/intent_service/preference_handler.py` (MODIFY)

Purpose: Complete the `confirm_preference` method with full logic

Current state: Skeleton exists, needs implementation

```python
async def confirm_preference(
    self,
    user_id: str,
    session_id: Optional[str],
    hint_id: str,
    accepted: bool,
) -> Dict[str, Any]:
    """Handle user's preference confirmation"""

    if not accepted:
        logger.info(f"User {user_id} dismissed hint {hint_id}")
        return {"success": True, "action": "dismissed"}

    # Get hint from session storage
    hint = self._get_hint_from_session(session_id, hint_id)
    if not hint:
        return {"success": False, "error": "Hint not found"}

    # Create confirmation
    confirmation = PreferenceConfirmation(
        id=f"confirm_{uuid4().hex[:8]}",
        user_id=user_id,
        dimension=hint.dimension,
        new_value=hint.detected_value,
        previous_value=hint.current_value,
        hint_id=hint.id,
        confirmation_source="user_explicit",
    )

    # Apply to UserPreferenceManager
    await self.preference_manager.apply_preference_pattern(
        pattern={
            "dimension": confirmation.dimension.value,
            "new_value": str(confirmation.new_value),
            "hint_id": confirmation.hint_id,
            "source": "user_confirmation",
        },
        user_id=user_id,
        session_id=session_id,
        scope="user",
    )

    # Log to learning system
    await self._log_preference_to_learning(confirmation)

    return {
        "success": True,
        "action": "accepted",
        "dimension": confirmation.dimension.value,
        "message": "Preference updated!"
    }
```

**Acceptance Criteria**:
- ✅ Retrieves hint from session storage
- ✅ Creates PreferenceConfirmation
- ✅ Applies to UserPreferenceManager
- ✅ Logs to learning system
- ✅ Returns success/error with details
- ✅ Handles missing hints gracefully

#### 2.3.2: Add Session-based Hint Storage
**File**: `services/intent_service/preference_handler.py` (MODIFY)

Purpose: Store and retrieve hints during conversation session

```python
class PreferenceDetectionHandler:
    def __init__(self):
        # ... existing init ...
        self.session_hints = {}  # session_id -> {hint_id -> hint}

    async def store_hint(self, session_id: str, hint: PreferenceHint):
        """Store hint for later retrieval"""
        if session_id not in self.session_hints:
            self.session_hints[session_id] = {}
        self.session_hints[session_id][hint.id] = hint

        # Set TTL: hints expire after 30 minutes
        asyncio.create_task(self._expire_hint(session_id, hint.id))

    def _get_hint_from_session(self, session_id: str, hint_id: str) -> Optional[PreferenceHint]:
        """Retrieve hint from session"""
        if session_id in self.session_hints:
            return self.session_hints[session_id].get(hint_id)
        return None

    async def _expire_hint(self, session_id: str, hint_id: str):
        """Expire hint after TTL"""
        await asyncio.sleep(30 * 60)  # 30 minutes
        if session_id in self.session_hints:
            self.session_hints[session_id].pop(hint_id, None)
```

**Acceptance Criteria**:
- ✅ Hints stored in-memory per session
- ✅ Hints expire after 30 minutes
- ✅ Can retrieve by hint_id
- ✅ Clean up on session end
- ✅ No memory leaks

#### 2.3.3: Implement Learning System Integration
**File**: `services/intent_service/preference_handler.py` (MODIFY - already has skeleton)

Purpose: Log confirmed preferences to learning system

The skeleton already exists in `_log_preference_to_learning`. Needs:
- Proper LearnedPattern creation
- Integration with QueryLearningLoop
- Error handling and logging

**Acceptance Criteria**:
- ✅ Creates LearnedPattern with PatternType.PREFERENCE
- ✅ Calls QueryLearningLoop._apply_user_preference_pattern()
- ✅ Returns success/failure
- ✅ Logs errors without blocking confirmation
- ✅ Includes proper metadata

---

## Phase 2.4: Intent Handler Hook Integration (1 hour)

### Objective
Wire everything together so preferences are detected and applied in the full conversation flow.

### Tasks

#### 2.4.1: Update Intent Classification to Async
**File**: `services/intent_service/classifier.py` (MODIFY)

Purpose: Make classify() async so it can call async preference detection

**Change**:
```python
# Before
def classify(self, message: str, context: Dict) -> Intent:
    ...

# After
async def classify(self, message: str, context: Dict) -> Intent:
    ...
```

**Acceptance Criteria**:
- ✅ Classify method is async
- ✅ Can await preference detection hook
- ✅ All callers updated to await classify()
- ✅ No blocking calls in chain
- ✅ All tests updated

#### 2.4.2: Add Hook Instantiation to Classifier
**File**: `services/intent_service/classifier.py` (MODIFY)

```python
class IntentClassifier:
    def __init__(self):
        # ... existing init ...
        self.preference_handler = PreferenceDetectionHandler()
        self.hooks = IntentProcessingHooks(self.preference_handler)
```

**Acceptance Criteria**:
- ✅ PreferenceDetectionHandler instantiated
- ✅ Available in classify() method
- ✅ Properly initialized with dependencies
- ✅ No circular imports

#### 2.4.3: Call Hook in Classification Flow
**File**: `services/intent_service/classifier.py` (MODIFY)

```python
async def classify(self, user_id: str, message: str, context: Dict) -> Intent:
    # Classify intent (existing logic)
    intent = self._run_classification(message)

    # NEW: Run preference detection hook
    session_id = context.get("session_id")
    pref_result = await self.hooks.on_intent_classified(
        user_id=user_id,
        message=message,
        intent=intent,
        session_id=session_id
    )

    # Attach to intent result
    intent.preferences = pref_result

    return intent
```

**Acceptance Criteria**:
- ✅ Hook called with proper parameters
- ✅ Preference result attached to intent
- ✅ Hook failure doesn't break classification
- ✅ Graceful degradation on errors
- ✅ Logging for debugging

#### 2.4.4: Update Chat Response Handler
**File**: `web/api/routes/conversation.py` (MODIFY - or similar route)

Purpose: Include preferences in response to frontend

```python
@router.post("/chat/message")
async def send_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
):
    # Get user profile
    profile = await PersonalityProfile.load_with_preferences(current_user.id)

    # Classify intent and detect preferences
    intent = await intent_classifier.classify(
        user_id=current_user.id,
        message=request.message,
        context={"session_id": request.session_id}
    )

    # Generate response
    response_text = await response_generator.generate(
        intent=intent,
        profile=profile,
        context=request.context
    )

    # Return with preferences
    return {
        "response": response_text,
        "intent": intent.intent_type,
        "preferences": intent.preferences,  # NEW
        "session_id": request.session_id,
    }
```

**Acceptance Criteria**:
- ✅ Preferences included in chat response
- ✅ Frontend receives preference hints
- ✅ No performance degradation
- ✅ Graceful if preferences missing
- ✅ Works with existing response generation

---

## Stop Conditions Check 🚦

**Before proceeding to each sub-phase, verify**:

### 2.1 Stop Conditions
- [ ] No import errors in intent_hooks.py
- [ ] Classifier.classify() still returns valid Intent
- [ ] Hook doesn't block response generation
- [ ] All existing tests pass

### 2.2 Stop Conditions
- [ ] Preference component renders without errors
- [ ] API endpoints respond with 200 status
- [ ] JavaScript functions defined and callable
- [ ] No XSS vulnerabilities in hint rendering

### 2.3 Stop Conditions
- [ ] Preference application completes without errors
- [ ] UserPreferenceManager receives updates
- [ ] Learning system logs are created
- [ ] Session storage working (hints persist during conversation)

### 2.4 Stop Conditions
- [ ] classify() is properly async
- [ ] Preferences attached to intent results
- [ ] Chat endpoint returns preferences in response
- [ ] E2E flow works: detect → suggest → accept → store → apply

---

## Phase 2 Timeline

**Estimated schedule**:
- 2.1 Detection Integration: 1.5 hours (3:44 PM - 5:15 PM)
- 2.2 Confirmation Flow: 1.5 hours (5:15 PM - 6:45 PM)
- 2.3 Application Logic: 1 hour (6:45 PM - 7:45 PM)
- 2.4 Hook Integration: 1 hour (7:45 PM - 8:45 PM)

**Total**: 5 hours (with buffer built in)

---

## Next Steps After Phase 2

Once Phase 2 completes:
- All code committed and tests passing
- Full e2e flow implemented but untested
- Ready for Phase 3: Comprehensive Testing

Phase 3 will include:
- Unit tests for all new methods
- Integration tests for full flow
- Manual testing and refinement
- Bug fixes and edge cases

---

**Phase 2 Status**: 🚀 READY TO BEGIN
**Starting sub-phase**: 2.1 Detection Pattern Integration
