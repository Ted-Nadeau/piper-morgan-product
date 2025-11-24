# Prompt for Cursor Agent: Conversational Error Messages (#283)

## Your Identity
You are Cursor Agent, a specialized development agent working on the Piper Morgan project. You focus on precise file modifications and testing. You follow systematic methodology and provide evidence for all claims.

## Essential Context (Read First)
Read these briefing documents in project knowledge:
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-CURRENT-STATE.md - Sprint A8 Phase 3 focus
- piper-style-guide.md - **CRITICAL** - Piper's voice/tone for all error messages

---

## 🚨 INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Check Gameplan Assumptions FIRST
**Before doing ANYTHING else, verify infrastructure matches gameplan**:

```bash
# Gameplan assumes:
# - Error handling exists but is technical
# - Some humanization work may already exist
# - Error messages returned to users
# - Need conversational fallbacks

# Verify reality:
ls -la web/api/routes/
ls -la services/errors/
ls -la services/conversation/

# CRITICAL: Find existing humanization work (75% pattern)
find . -name "*humanize*" -o -name "*error*message*" -o -name "*friendly*" -type f
grep -r "humanize\|friendly.error\|conversational.error" services/ --include="*.py"
grep -r "ActionHumanizer\|ErrorTranslator" . --include="*.py"
```

**PM SAID**: "We made a whole effort to humanize error messages in the past. Doesn't seem to be fully engaged."

**This means**:
1. **Something already exists** - find it first
2. **It's not working** - figure out why
3. **Extend it, don't rebuild it** - this is the 75% pattern

**If you find existing humanization work**:
1. **STOP implementation**
2. **Report what exists and why not working**
3. **Get PM approval** before proceeding

---

## 🛡️ ANTI-80% COMPLETION SAFEGUARDS

### MANDATORY Error Type Enumeration
**Create comparison table FIRST**:
```
Error Type          | Has Fallback | Status
------------------- | ------------ | ------
Empty Input         | ✓            | Complete
Unknown Action      | ✓            | Complete
Timeout             | ✗            | MISSING
Unknown Intent      | ✗            | MISSING
System Error        | ✗            | MISSING
TOTAL: 2/5 = 40% INCOMPLETE - CANNOT PROCEED
```

**100% = ALL 5 error types, not "most common errors"**

### Reference Piper's Voice
**Every error message must**:
- Follow piper-style-guide.md tone
- Be helpful, not cute
- Suggest next actions
- Avoid technical jargon
- Maintain Piper's personality

---

## Mission

**Objective**: Transform technical error messages into conversational, helpful responses

**Single Issue**:
- **#283** (4h): Add conversational error fallbacks for 5 error types

**Scope Boundaries**:
- This prompt covers: User-facing error messages only
- NOT in scope: Technical logging (keep that intact)
- Code handles: Action mapping (#284), todo system (#285)

---

## Context

**GitHub Issue**: #283: CORE-ALPHA-ERROR-MESSAGES

**Current State**:
- ❌ "An API error occurred" (technical)
- ❌ "No handler for action: X" (exposes internals)
- ❌ "Operation timed out after 30 seconds" (technical)
- ❌ Empty input causes 30-second timeout (bad UX)
- ❌ Generic fallthrough for unknown intents

**Target State**:
- ✅ "I didn't quite catch that. Could you share more?" (empty input)
- ✅ "I'm still learning how to help with that." (unknown actions)
- ✅ "That's complex - let me reconsider." (timeouts)
- ✅ "I'm not sure I understood correctly." (unknown intents)
- ✅ "Something went wrong on my end." (system errors)

**Dependencies**:
- Parallel to Code's work (#284, #285)
- No conflicts expected (different files)
- May complement Code's ActionMapper

**User Data Risk**: None (only error messages)

**Infrastructure Verified**: After Phase -1 investigation above

---

## 🔍 PHASE -1 CRITICAL DISCOVERY (MUST INVESTIGATE)

### Find Existing Humanization Work
**PM's Statement**: "We made a whole effort to humanize error messages in the past."

**Your Investigation Tasks**:
```bash
# Search for existing humanization classes/modules
find . -name "*humanize*" -o -name "*friendly*" -o -name "*conversational*" -type f | grep -v node_modules

# Search for error message patterns
grep -r "I didn't\|I'm still\|Something went\|not sure I understood" . --include="*.py"

# Search for error translation/mapping
grep -r "class.*Error.*Service\|class.*Message.*Service" services/ --include="*.py"

# Check ActionHumanizer specifically (PM mentioned this concept)
grep -r "ActionHumanizer\|action_humanizer" . --include="*.py"

# Look in likely locations
cat services/errors/action_humanizer.py 2>/dev/null
cat services/conversation/response_builder.py 2>/dev/null
cat services/shared/error_messages.py 2>/dev/null
```

**What to Document**:
1. **If humanization exists**: What is it? Where is it? Why not working?
2. **If partially working**: What % works? What's missing?
3. **If completely broken**: What broke it? Can we fix it?

**Report Template**:
```markdown
## Phase -1 Discovery Results

**Existing Humanization Found**: [YES/NO]

[If YES]
- **Location**: [file path]
- **Functionality**: [what it does]
- **Coverage**: [X/5 error types covered]
- **Why Not Working**: [diagnosis]
- **Recommendation**: [extend vs rebuild]

[If NO]
- **Searched**: [list all search locations]
- **Evidence**: [show grep/find outputs]
- **Recommendation**: Create new ConversationalErrorService
```

**Wait for PM Approval** before implementing if you find existing work.

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:
- **"Created error service"** → Show `cat services/errors/conversational_errors.py`
- **"All 5 errors handled"** → Show comparison table with 5/5 = 100%
- **"Empty input caught"** → Show `curl` test with empty message
- **"Technical logs preserved"** → Show log output still has details
- **"Piper's tone maintained"** → Reference piper-style-guide.md sections
- **"Tests pass"** → Show `pytest` output
- **"Committed changes"** → Show `git log --oneline -1` output

### Before/After Evidence Required:
```bash
# Before: Show current error message
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'

# After: Show conversational error message
# Should return friendly message, not timeout/exception
```

### Git Workflow Discipline:
After changes:
```bash
git status
git add [files]
git commit -m "feat: Add conversational error messages (#283)"
git log --oneline -1  # SHOW THIS OUTPUT
```

---

## Implementation Plan (4 hours)

### Step 1: Phase -1 Investigation (30 min) - MANDATORY
**See Phase -1 section above**
- Find existing humanization work
- Document what exists
- Report to PM
- Get approval to proceed

**STOP if you find existing work** - report first!

### Step 2: Create or Extend Error Service (1h)

**Option A: If Nothing Exists**
```python
# services/errors/conversational_errors.py (NEW FILE)
import structlog
from typing import Optional

logger = structlog.get_logger()

class ConversationalErrorService:
    """
    Provides user-friendly error messages while preserving technical logging.

    Based on Piper's voice/tone from piper-style-guide.md:
    - Helpful and encouraging
    - Professional but approachable
    - Suggests next actions
    - Never sarcastic or dismissive
    """

    @staticmethod
    def empty_input() -> str:
        """User sent empty or whitespace-only message."""
        return (
            "I didn't quite catch that. Could you share more about "
            "what you'd like to work on?"
        )

    @staticmethod
    def unknown_action(action: str) -> str:
        """Classifier identified action but no handler exists."""
        # Log technical details
        logger.warning(f"Unknown action: {action}")

        # Return friendly message
        return (
            "I'm still learning how to help with that. "
            "What else can I assist you with?"
        )

    @staticmethod
    def timeout() -> str:
        """Operation took too long."""
        return (
            "That's a complex request - let me reconsider. "
            "Could you break it down into smaller parts?"
        )

    @staticmethod
    def unknown_intent() -> str:
        """Couldn't classify user's intent."""
        return (
            "I'm not sure I understood correctly. "
            "Could you rephrase that?"
        )

    @staticmethod
    def system_error(error: Optional[Exception] = None) -> str:
        """Internal system error occurred."""
        # Log technical details
        if error:
            logger.error(f"System error: {str(error)}", exc_info=True)

        # Return friendly message
        return (
            "Something went wrong on my end. Let me try again, "
            "or would you like to try something else?"
        )
```

**Option B: If Existing Work Found**
- Extend existing ActionHumanizer or similar
- Add missing error types
- Fix whatever is preventing it from working
- Follow existing patterns

**Evidence Required**:
- File created or modified: Show full file or diff
- All 5 methods present: Show method enumeration
- Follows style guide: Reference specific sections

### Step 3: Add Input Validation (45 min)
```python
# web/api/routes/chat.py
from services.errors.conversational_errors import ConversationalErrorService

@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Handle chat message with input validation."""

    # NEW: Catch empty input immediately
    if not request.message or request.message.strip() == "":
        return ChatResponse(
            response=ConversationalErrorService.empty_input(),
            session_id=request.session_id
        )

    # ... rest of handler
```

**Evidence Required**:
- Show exact location of change
- Test empty input: `curl` command with `"message": ""`
- Show friendly response, not timeout

### Step 4: Update Error Handlers (1h)
```python
# services/intent_service/intent_service.py
from services.errors.conversational_errors import ConversationalErrorService

async def route_action(self, intent, session_id, user_id):
    """Route intent with conversational error handling."""

    handler_name = f"_handle_{intent.action}"
    handler = getattr(self, handler_name, None)

    if not handler:
        # NEW: Conversational fallback instead of technical error
        return ConversationalErrorService.unknown_action(intent.action)

    try:
        return await handler(intent, session_id, user_id)
    except TimeoutError:
        # NEW: Friendly timeout message
        return ConversationalErrorService.timeout()
    except Exception as e:
        # NEW: Friendly system error (but log details)
        return ConversationalErrorService.system_error(e)

# services/conversation/conversation_handler.py (or wherever fallback lives)
async def handle_unknown_intent(self, message):
    """Handle when classifier can't determine intent."""
    # NEW: Use conversational error instead of generic response
    return ConversationalErrorService.unknown_intent()
```

**Evidence Required**:
- Show all integration points
- Test each error type:
  - Empty: `curl` with `"message": ""`
  - Unknown action: `curl` with request that has no handler
  - Timeout: (if testable)
  - Unknown intent: `curl` with gibberish message
  - System error: (if testable)

### Step 5: Verify Technical Logging Intact (30 min)
```bash
# Start server with visible logging
python main.py --log-level=DEBUG

# Trigger various errors
# Check that logs still have technical details

# Example: Unknown action should log:
# [WARNING] Unknown action: non_existent_action
# But user sees: "I'm still learning how to help with that."
```

**Evidence Required**:
- Log output showing technical details preserved
- User response showing friendly message
- Both happen simultaneously

### Step 6: End-to-End Testing (1h)
```bash
# Test all 5 error types
TOKEN=$(curl -s -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"xian","password":"test123456"}' \
  | jq -r '.token')

# 1. Empty input
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": ""}'
# Expected: "I didn't quite catch that..."

# 2. Unknown action (trigger via impossible request)
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "xyzabc123impossible"}'
# Expected: "I'm still learning..." or "I'm not sure I understood..."

# 3. Test via CLI
python main.py chat ""
# Expected: Friendly error, not crash

# 4. Run any existing error-related tests
pytest tests/ -k "error" -v

# 5. Manual review: Read all error messages for tone consistency
grep -r "return.*Error\|return.*error" services/ --include="*.py" | less
```

**Evidence Required**:
- All 5 curl test outputs
- pytest results (if error tests exist)
- Manual review notes on tone consistency

---

## Acceptance Criteria Checklist

**Issue #283**:
- [ ] Phase -1 investigation complete (found/didn't find existing work)
- [ ] All 5 error types have conversational fallbacks
- [ ] Empty input caught immediately (no 30s timeout)
- [ ] No technical jargon in user-facing messages
- [ ] Error messages suggest next actions
- [ ] Piper's tone maintained (checked against style guide)
- [ ] Technical logging preserved (not removed)
- [ ] All tests pass (show pytest output)
- [ ] Manual testing complete (show all 5 error types working)
- [ ] Changes committed with evidence (show git log)

**Completion Matrix**: 5/5 error types = 100%

---

## Multi-Agent Coordination

**You are working in parallel with Code Agent**:
- **Code**: #284 + #285 (action mapping, todo system)
- **You**: #283 (error messages)

**Coordination Points**:
- After Phase -1: Share discovery if it affects Code's work
- After implementation: Check if Code's ActionMapper complements your work
- No direct dependencies, can work simultaneously

**Share via GitHub**:
- Update #283 description with checkboxes as you progress
- Commit frequently with issue reference
- Comment if discoveries affect approach

---

## STOP Conditions (17 Total)
Stop immediately and escalate if:
1. Existing humanization found (report before proceeding)
2. Style guide conflicts with error messages (PM decides)
3. Can't achieve Piper's tone (need guidance)
4. Error handling architecture different than expected
5. Tests fail (report, don't decide if critical)
6. Can't preserve technical logging
7. Performance impact (measure before/after)
8. Auth system affected (dependency from Nov 1)
9. Breaking existing error reporting
10. Git operations failing
11. Can't provide evidence for claims
12. Completion bias detected (claiming without proof)
13. Rationalizing gaps (e.g., "most errors covered")
14. GitHub tracking not working
15. Server state unexpected
16. Discovery proves gameplan wrong
17. User experience degrades (test manually)

---

## When Tests Fail (CRITICAL)

**If ANY test fails**:
1. **STOP immediately**
2. **Do NOT decide** if it's "just" a test issue
3. **Report**:

```
⚠️ STOP - Tests Failing

Test: [name]
Error: [exact output]
Root cause: [if known]

Options:
1. [fix approach]
2. [alternative]

Awaiting PM decision.
```

---

## Success Metrics

**Issue #283** (Error Messages):
- 5/5 error types handled = 100%
- All messages follow Piper's voice/tone
- Technical logging preserved
- User testing shows improvement
- Zero technical jargon in user messages
- All error types tested and working

**Quality Indicators**:
- PM approves tone/personality
- Messages suggest helpful next actions
- Users understand what went wrong
- Logs still useful for debugging

---

## Final Reminders

1. **Phase -1 FIRST** - Find existing humanization work
2. **Report discoveries** - Especially if existing work found
3. **Reference style guide** - Every error message must follow it
4. **100% completion** - All 5 error types, not "most"
5. **Before/After evidence** - Show current vs improved messages
6. **Technical logging** - Preserve for debugging
7. **Manual testing** - Actually trigger each error type
8. **Coordinate with Code** - Share relevant discoveries
9. **No time pressure** - Quality over speed
10. **PM approval** - Before claiming complete

---

**Ready to begin Phase -1 investigation. Report findings before implementing anything.**
