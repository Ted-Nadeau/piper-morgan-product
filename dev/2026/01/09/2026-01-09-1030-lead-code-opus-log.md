# Session Log: Issue #490 Five Whys Analysis

**Date**: January 9, 2026 10:06 - 10:30 AM
**Role**: Lead Developer (Code)
**Model**: Claude Code (Opus)
**Issue**: #490 FTUX-PORTFOLIO Portfolio Onboarding

---

## Session Context

PM completed initial implementation and manual testing of portfolio onboarding. Despite all 39 unit/integration tests passing, manual testing showed "nothing is really working as expected."

PM requested:
1. Full test suite run (unit, integration, e2e, regression)
2. Gap analysis
3. Five Whys subagent analysis for categorical issues and antipatterns

---

## Key Discoveries

### Root Cause: user_id Never Reaches ConversationHandler

The portfolio onboarding trigger check in `ConversationHandler._check_portfolio_onboarding()` expects `user_id` from `intent.context.get("user_id")`, but this is **NEVER populated** in the real request flow.

**Request Flow Analysis**:

```
Frontend (chat.js)
  POST /api/v1/intent {message, session_id}  <- NO user_id
       |
       v
web/api/routes/intent.py::process_intent(request)
  - Does NOT use get_current_user dependency
  - Does NOT extract user_id
       |
       v
services/intent/intent_service.py::process_intent()
  - Calls intent_classifier.classify(message)  <- NO context passed
  - Hardcoded user_id "xian" UUID only for learning patterns (line 222-223)
       |
       v
services/intent_service/canonical_handlers.py::_handle_conversation_query()
  - Creates new ConversationHandler()
  - intent.context has NO user_id
       |
       v
services/conversation/conversation_handler.py::respond()
  user_id = intent.context.get("user_id")   <- Returns None
  if user_id and session_id:                <- FALSE, never executes
      await self._check_portfolio_onboarding(user_id, session_id)
```

### Why Tests Pass But Feature Fails

Tests create `Intent` objects directly with fake `user_id` in context:

```python
# Test code (passes)
Intent(context={"user_id": "test-user-123", ...})

# Real system (fails)
intent = await intent_classifier.classify(message)  # No user_id
```

### Hardcoded "xian" Problem

Found 40+ occurrences of hardcoded `user_id = "xian"` across codebase:
- `services/intent/intent_service.py:222-223` - TODO comment but hardcoded UUID
- `services/features/issue_intelligence.py:64`
- `cli/commands/standup.py:126`
- Many test files

PM note: "we need to eradicate anything expecting test user = 'xian' - obsolete mocking strategy"

---

## Beads Created

| Bead ID | Priority | Title |
|---------|----------|-------|
| piper-morgan-9mc | P0 | user_id never passed to ConversationHandler - breaks portfolio onboarding trigger |
| piper-morgan-3pv | P0 | E2E tests mock _check_portfolio_onboarding instead of testing real integration |
| piper-morgan-ejj | P1 | /intent route doesn't use get_current_user dependency - no user context available |
| piper-morgan-a0h | P1 | IntentClassifier.classify() not passed user_id/context - intent has no user context |
| piper-morgan-7mr | P2 | TEST-ANTIPATTERN: Unit tests create Intent objects directly with fake context |
| piper-morgan-3cq | P2 | TEST-GAP: No integration test exercises full HTTP request path |
| piper-morgan-6ee | P2 | RETRO: Gameplan #490 did not anticipate user_id propagation requirements |

---

## Five Whys Summary

1. **Why manual testing fails?** → `_check_portfolio_onboarding()` never called
2. **Why never called?** → `user_id` is None in ConversationHandler.respond()
3. **Why is user_id None?** → `intent.context.get("user_id")` returns None
4. **Why no user_id in context?** → IntentClassifier.classify() called with only message
5. **Why no context passed?** → /intent route doesn't integrate with authentication

**Root Cause**: The `/intent` route doesn't use `get_current_user` dependency, so user_id is never available anywhere in the intent processing pipeline.

---

## Antipatterns Identified

1. **"Mock the Integration Point"**: Tests mock the method they're testing
2. **"Construct Test Objects with Fake Data"**: Tests create Intent with properties real code never populates
3. **"Integration Tests That Don't Integrate"**: Files named `*_e2e.py` use heavy mocking
4. **"Missing the HTTP Boundary"**: Tests call service methods directly, skipping route layer

---

## Recommended Fixes

### P0 Fixes (Required)

1. **Update `/intent` route** to use `get_current_user` dependency
2. **Update IntentService** to accept and propagate user_id
3. **Ensure Intent context** includes user_id for downstream handlers

### P1/P2 Fixes (Test Strategy)

4. Create true integration test for /intent with authenticated user
5. Remove mocks from E2E tests or rename them
6. Add "contract" marker for integration boundary tests

---

## Retrospective Action Item

**PM Request**: "please also make a note that we should retro our gameplan and issue description to see where they could have been more robust and anticipated some of these real issues"

Created bead `piper-morgan-6ee` to track this methodology improvement:
- Gameplan #490 didn't specify user_id flow requirements
- Issue description focused on UI/UX, not the auth integration
- Phase -1 verification should include "data flow requirements" checkpoint
- Future gameplans should explicitly trace authenticated user context through system

---

## Test Results

- 39 unit/integration tests: ALL PASS
- 11 conversation handler tests: ALL PASS
- Manual testing: FAILS (onboarding never triggers)

**Classic Pattern-045 (Green Tests, Red User)**

---

## Next Steps

1. PM decision on fix priority/approach
2. Implement P0 fixes to wire user_id through /intent route
3. Eradicate hardcoded "xian" user_id across codebase
4. Update gameplan template with data flow verification step

---

*Session log by Claude Code (Opus) - January 9, 2026*
