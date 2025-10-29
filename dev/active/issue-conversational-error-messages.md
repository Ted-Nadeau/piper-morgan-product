# Issue: Implement Conversational Error Message Fallbacks

**Priority**: HIGH
**Milestone**: Sprint A8 (MVP Blocker)
**Labels**: `ux`, `error-handling`, `mvp-blocker`, `user-experience`
**Estimated Effort**: 4 hours

---

## Problem

Current error messages are technical and non-actionable, violating Piper Morgan's conversational UX principles. Users encounter cryptic errors that don't guide them toward resolution.

**Examples from Testing**:
- "An API error occurred" ← User doesn't know what to do
- "No handler for action: create_github_issue" ← Technical jargon
- "Operation timed out after 30 seconds" ← On empty input, should catch immediately
- Falls through to generic error for unknown intents

**Impact**: Breaks conversational experience, creates user frustration, blocks MVP quality standard.

---

## Current Behavior vs. Required Behavior

### 1. Empty/Invalid Input

**Current**: 30-second timeout, then "Operation timed out"

**Required**: Immediate validation with friendly prompt
```
"I didn't quite catch that. Could you share a bit more about what you'd like to work on?"
```

**Implementation**:
- Add input validation before processing
- Check for empty, whitespace-only, or too-short input
- Return friendly prompt immediately (no LLM call needed)

---

### 2. Missing/Unknown Actions

**Current**: "No handler for action: create_github_issue"

**Required**: Conversational acknowledgment
```
"I'm still learning how to help with that. What else can I assist you with?"
```

**Implementation**:
- Catch action not found errors
- Return conversational fallback
- Log action name for future implementation tracking

---

### 3. Operation Timeouts

**Current**: "Operation timed out after 30 seconds"

**Required**: Helpful explanation with suggestion
```
"That's a complex request - let me reconsider the approach. Could you break it down into smaller steps?"
```

**Implementation**:
- Catch timeout exceptions
- Provide context-aware suggestions
- Offer to help with simpler version

---

### 4. Unknown Intents

**Current**: Falls through to generic error

**Required**: ConversationHandler fallback
```
"I'm not sure I understood that correctly. Could you rephrase or give me more context?"
```

**Implementation**:
- Route UNKNOWN intents to ConversationHandler
- Use clarification flow
- Learn from user's rephrasing

---

### 5. API/System Errors

**Current**: "An API error occurred"

**Required**: Friendly acknowledgment with action
```
"Something went wrong on my end. Let me try that again, or would you like to try something else?"
```

**Implementation**:
- Catch system exceptions
- Provide retry option
- Log technical details server-side only

---

## Technical Implementation

### File Locations

**Primary**:
- `services/intent/intent_service.py` - Add error handling middleware
- `services/conversation/conversation_handler.py` - Fallback responses
- `services/ux/error_messages.py` - NEW: Conversational error templates

**Secondary**:
- `web/app.py` - Web UI error responses
- `services/api/serializers.py` - Error response formatting

---

### Implementation Pattern

```python
# services/ux/error_messages.py (NEW FILE)
class ConversationalErrorMessages:
    """Conversational error message templates"""

    @staticmethod
    def empty_input() -> str:
        return "I didn't quite catch that. Could you share a bit more about what you'd like to work on?"

    @staticmethod
    def unknown_action(action: str) -> str:
        # Log action for tracking, don't show technical details to user
        return "I'm still learning how to help with that. What else can I assist you with?"

    @staticmethod
    def timeout() -> str:
        return "That's a complex request - let me reconsider the approach. Could you break it down into smaller steps?"

    @staticmethod
    def unknown_intent() -> str:
        return "I'm not sure I understood that correctly. Could you rephrase or give me more context?"

    @staticmethod
    def system_error() -> str:
        return "Something went wrong on my end. Let me try that again, or would you like to try something else?"
```

```python
# services/intent/intent_service.py - Add validation
async def process_intent(self, message: str, session_id: str = "default_session"):
    # Validate input BEFORE processing
    if not message or message.strip() == "":
        return IntentProcessingResult(
            message=ConversationalErrorMessages.empty_input(),
            success=False,
            intent_category="validation_error"
        )

    if len(message.strip()) < 3:
        return IntentProcessingResult(
            message=ConversationalErrorMessages.empty_input(),
            success=False,
            intent_category="validation_error"
        )

    try:
        # Existing processing...
    except ActionNotFoundError as e:
        logger.warning(f"Action not found: {e.action}")  # Log for tracking
        return IntentProcessingResult(
            message=ConversationalErrorMessages.unknown_action(e.action),
            success=False,
            intent_category="unknown_action"
        )
    except TimeoutError:
        return IntentProcessingResult(
            message=ConversationalErrorMessages.timeout(),
            success=False,
            intent_category="timeout"
        )
    except Exception as e:
        logger.error(f"System error: {e}", exc_info=True)  # Log technical details
        return IntentProcessingResult(
            message=ConversationalErrorMessages.system_error(),
            success=False,
            intent_category="system_error"
        )
```

---

## Testing Requirements

### Unit Tests
- [ ] Test empty input validation
- [ ] Test whitespace-only input
- [ ] Test action not found error
- [ ] Test timeout error
- [ ] Test unknown intent routing
- [ ] Test system error handling
- [ ] Verify no technical jargon in user messages

### Integration Tests
- [ ] Test empty message via web UI → friendly response
- [ ] Test unknown action via API → conversational fallback
- [ ] Test timeout scenario → helpful suggestion
- [ ] Verify error logging preserves technical details

### User Acceptance Tests
- [ ] User sees friendly messages for all error types
- [ ] No technical jargon or stack traces in UI
- [ ] Error messages suggest next actions
- [ ] Conversational tone maintained throughout

---

## Acceptance Criteria

- [ ] All error types have conversational fallbacks
- [ ] Empty input caught immediately (no 30s timeout)
- [ ] Technical details logged server-side only
- [ ] User messages maintain Piper's conversational tone
- [ ] Error messages provide actionable suggestions
- [ ] All tests pass (unit, integration, UAT)
- [ ] Manual testing confirms improved UX

---

## Related Issues

- #XXX: CONVERSATION handler architectural placement
- #XXX: Learning system activation investigation
- #XXX: Action name coordination (create_github_issue)

---

## References

- **Gap Analysis**: `dev/2025/10/27/CRITICAL-GAPS-ANALYSIS.md` (Gap 4)
- **Style Guide**: `piper-style-guide.md` (conversational tone)
- **User Testing**: Phase 2 manual testing (Oct 27, 2025)

---

## Notes

**MVP Blocker**: This is essential for MVP quality. Users must have a conversational experience even when things go wrong.

**Priority Order**:
1. Empty input validation (immediate win)
2. Unknown action fallback (unblocks testing)
3. Timeout handling (improves UX)
4. Unknown intent routing (learning opportunity)
5. System error messages (safety net)

**Estimated Time**: 4 hours total
- 1 hour: Create error message templates
- 1 hour: Add validation and error handling
- 1 hour: Write tests
- 1 hour: Manual testing and polish

---

**Created**: October 27, 2025, 12:30 PM
**Reporter**: Lead Developer (Sonnet 4.5)
**Discovered During**: Phase 2 Manual Testing
