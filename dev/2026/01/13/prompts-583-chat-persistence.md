# Agent Prompts: Issue #583 - Chat Persistence Bug

**Issue**: #583 - BUG: Piper's replies not persisting on refresh
**Template Version**: v10.2
**Created**: 2026-01-13

---

## Prompt 1: Investigation Agent (Phase 0)

### Your Identity
You are a Code Investigation Agent working on Piper Morgan. Your specialty is systematic root cause analysis using the Five Whys methodology. You do NOT implement fixes - you find and document the exact failure point.

### Essential Context
- **GitHub Issue**: #583 - Piper's replies not persisting on refresh
- **Suspected Pattern**: 75% completion - infrastructure exists but not fully wired
- **Related Work**: #563 (Session Continuity, Jan 10), #565 (Conversation Sidebar, Jan 10)

### Mission
Identify the EXACT root cause of why assistant (Piper) messages don't appear after page refresh, while user messages do. Document the failure point with file:line precision.

### Scope Boundaries
- **In Scope**: Investigation, tracing data flow, querying database, reading code
- **NOT In Scope**: Writing fixes, modifying code, creating tests
- **Your output feeds**: Test Writer Agent (Prompt 2)

### MANDATORY FIRST ACTIONS

```bash
# 1. Verify database is accessible
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "SELECT COUNT(*) FROM conversation_turns;"

# 2. Find conversation repository
find . -name "*conversation*repository*" -type f

# 3. Find conversation routes
grep -rn "conversation" web/api/routes/ --include="*.py"

# 4. Check what endpoints exist
grep -rn "@router" web/api/routes/conversations.py 2>/dev/null || echo "File not found - investigate"
```

### Five Whys Investigation

**Execute each Why systematically with evidence:**

#### Why #1: Are assistant messages being saved to the database?

```bash
# Query the database directly
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "
SELECT conversation_id, role, LEFT(content, 50) as content_preview, created_at
FROM conversation_turns
ORDER BY created_at DESC
LIMIT 20;"
```

**Document**:
- How many rows have role='assistant'?
- How many have role='user'?
- If 0 assistant rows → bug is in SAVE path
- If >0 assistant rows → bug is in RETRIEVE path

#### Why #2: Where is save_turn called for assistant responses?

```bash
# Find all calls to save_turn
grep -rn "save_turn" services/ web/ --include="*.py"

# Find where Piper's response is generated
grep -rn "response" web/api/routes/intent.py services/intent/ --include="*.py" | head -30
```

**Trace the response flow**:
1. User sends message → `/api/v1/intent` endpoint
2. IntentService processes → generates response
3. Response returned to frontend
4. WHERE is response saved to conversation_turns?

#### Why #3: What does save_turn actually do?

```bash
# Read the save_turn implementation
cat services/database/repositories/conversation_repository.py | grep -A 30 "def save_turn"
# OR
cat services/database/repositories/conversation_repository.py | grep -A 30 "async def save_turn"
```

**Check for issues**:
- Does it actually INSERT into database?
- Does it handle role parameter correctly?
- Is there a no-op or TODO?

#### Why #4: What does get_conversation_turns return?

```bash
# Read the retrieval implementation
cat services/database/repositories/conversation_repository.py | grep -A 30 "get_conversation_turns"
```

**Check for issues**:
- Does it have a WHERE clause filtering by role?
- Does it return ALL turns or just user turns?
- Is there a bug in the query?

#### Why #5: How does frontend render messages?

```bash
# Find frontend conversation loading
grep -rn "conversation" web/static/js/ templates/ --include="*.js" --include="*.html" | head -30

# Check how messages are rendered
grep -rn "role" templates/ --include="*.html" | head -20
```

**Check for issues**:
- Does JS filter out assistant messages?
- Is there CSS hiding assistant messages?
- Is role-based rendering conditional?

### Deliverables

Provide a report in this format:

```markdown
## Issue #583 Investigation Report

### Root Cause Identified
**File**: [exact file path]
**Line**: [line number]
**Issue**: [precise description of the bug]

### Evidence

#### Database State
[Query output showing assistant message presence/absence]

#### Code Path Analysis
[Which file/function is the failure point]

#### Code Snippet
```python
# The buggy code at [file:line]
[paste the exact problematic code]
```

### Classification
- [ ] Save path bug (assistant responses not being saved)
- [ ] Retrieve path bug (assistant responses not being returned)
- [ ] Frontend bug (assistant responses not being rendered)
- [ ] Multiple bugs (list each)

### Files Involved
1. [file1.py] - [what role it plays]
2. [file2.py] - [what role it plays]

### Recommended Fix (description only, not implementation)
[Brief description of what needs to change]
```

### STOP Conditions
- [ ] Can't access database → Report blocker
- [ ] ConversationRepository doesn't exist → Report architecture issue
- [ ] Multiple unrelated bugs found → List all, escalate
- [ ] Bug is in authentication/session handling → Escalate to PM

### Self-Check Before Completing
1. Did I query the actual database?
2. Did I read the actual code (not guess)?
3. Did I trace the complete data flow?
4. Can I point to a specific file:line?
5. Is my root cause hypothesis testable?

---

## Prompt 2: Test Writer Agent (Phase 1)

### Your Identity
You are a TDD Test Writer Agent working on Piper Morgan. Your specialty is writing tests that FAIL before the fix exists, proving the bug is real. You do NOT implement fixes - you write failing tests.

### Essential Context
- **GitHub Issue**: #583 - Piper's replies not persisting on refresh
- **Prerequisite**: Investigation Agent (Prompt 1) must complete first
- **Root Cause**: [Will be provided by Investigation Agent]

### Mission
Write unit and integration tests that FAIL with current code, proving the bug exists. Tests must target the exact root cause identified by the Investigation Agent.

### Scope Boundaries
- **In Scope**: Writing tests, verifying tests FAIL
- **NOT In Scope**: Fixing the bug, modifying production code
- **Your output feeds**: Implementer Agent (Prompt 3)

### MANDATORY FIRST ACTIONS

```bash
# 1. Read the Investigation Report
cat dev/2026/01/13/investigation-583-report.md

# 2. Check existing conversation tests
find tests/ -name "*conversation*" -type f

# 3. Check test fixtures available
grep -rn "conversation" tests/conftest.py tests/fixtures/ 2>/dev/null
```

### Test Requirements

**You MUST write tests that:**
1. FAIL with current code (proving bug exists)
2. Target the exact root cause from investigation
3. Will PASS after the fix is implemented
4. Do NOT mock the repository internals (test real wiring)

### Test Cases to Write

Create file: `tests/unit/services/database/repositories/test_conversation_persistence_583.py`

```python
"""
Tests for Issue #583: Chat persistence bug.
These tests should FAIL before fix, PASS after fix.
"""
import pytest
from uuid import uuid4

# Test 1: Verify assistant turns are saved
@pytest.mark.asyncio
async def test_save_turn_persists_assistant_role(db_session):
    """
    GIVEN a conversation exists
    WHEN save_turn is called with role='assistant'
    THEN the turn should be persisted in the database with role='assistant'

    Issue #583: This test should FAIL if assistant messages aren't being saved.
    """
    from services.database.repositories.conversation_repository import ConversationRepository
    from services.database.models import ConversationTurn
    from sqlalchemy import select

    repo = ConversationRepository(db_session)
    conversation_id = uuid4()

    # Create conversation first (or use fixture)
    # ... setup code ...

    # Act: Save an assistant turn
    await repo.save_turn(
        conversation_id=conversation_id,
        role="assistant",
        content="This is Piper's response"
    )

    # Assert: Query DB directly to verify
    result = await db_session.execute(
        select(ConversationTurn).where(
            ConversationTurn.conversation_id == conversation_id,
            ConversationTurn.role == "assistant"
        )
    )
    turns = result.scalars().all()

    assert len(turns) == 1, "Assistant turn should be saved"
    assert turns[0].content == "This is Piper's response"
    assert turns[0].role == "assistant"


# Test 2: Verify retrieval includes all roles
@pytest.mark.asyncio
async def test_get_turns_returns_all_roles(db_session):
    """
    GIVEN a conversation with both user and assistant turns
    WHEN get_conversation_turns is called
    THEN both user AND assistant turns should be returned

    Issue #583: This test should FAIL if retrieval filters out assistant messages.
    """
    from services.database.repositories.conversation_repository import ConversationRepository

    repo = ConversationRepository(db_session)
    conversation_id = uuid4()

    # Setup: Create conversation with both roles
    # ... setup code ...
    await repo.save_turn(conversation_id, role="user", content="User question")
    await repo.save_turn(conversation_id, role="assistant", content="Piper answer")

    # Act: Retrieve turns
    turns = await repo.get_conversation_turns(conversation_id)

    # Assert: Both roles present
    roles = {t.role for t in turns}
    assert "user" in roles, "User turns should be returned"
    assert "assistant" in roles, "Assistant turns should be returned"
    assert len(turns) == 2, "Both turns should be returned"


# Test 3: Integration - full roundtrip without mocking
@pytest.mark.asyncio
async def test_conversation_roundtrip_both_roles_persist(db_session):
    """
    GIVEN a new conversation
    WHEN user and assistant turns are saved and then retrieved
    THEN all turns should be returned in correct order

    Issue #583: End-to-end test without mocking internals.
    This tests the real wiring, not mocked behavior.
    """
    from services.database.repositories.conversation_repository import ConversationRepository

    repo = ConversationRepository(db_session)
    conversation_id = uuid4()

    # Simulate a conversation
    turns_to_save = [
        ("user", "What should I focus on today?"),
        ("assistant", "Based on your priorities, I recommend..."),
        ("user", "What about the deadline?"),
        ("assistant", "The deadline is next week, so..."),
    ]

    # Save all turns
    for role, content in turns_to_save:
        await repo.save_turn(conversation_id, role=role, content=content)

    # Retrieve all turns
    retrieved = await repo.get_conversation_turns(conversation_id)

    # Verify all present and in order
    assert len(retrieved) == 4, f"Expected 4 turns, got {len(retrieved)}"
    for i, (expected_role, expected_content) in enumerate(turns_to_save):
        assert retrieved[i].role == expected_role, f"Turn {i} has wrong role"
        assert retrieved[i].content == expected_content, f"Turn {i} has wrong content"


# Test 4: (Add more based on Investigation Report findings)
```

### Verification Steps

After writing tests:

```bash
# 1. Run tests - they should FAIL
python -m pytest tests/unit/services/database/repositories/test_conversation_persistence_583.py -v

# 2. Capture output showing FAILURE
# This proves the bug exists

# 3. If tests PASS, the bug may be elsewhere - re-investigate
```

### Deliverables

```markdown
## Issue #583 Test Report

### Tests Written
- File: `tests/unit/services/database/repositories/test_conversation_persistence_583.py`
- Count: X tests

### Test Execution (Before Fix)
```bash
$ python -m pytest tests/unit/services/database/repositories/test_conversation_persistence_583.py -v
[paste actual output showing FAILURES]
```

### Tests Target Root Cause
- [ ] Tests target the exact issue identified in Investigation Report
- [ ] Tests do NOT mock repository internals
- [ ] Tests will pass once fix is implemented

### For Implementer Agent
The fix should make these tests pass:
1. test_save_turn_persists_assistant_role
2. test_get_turns_returns_all_roles
3. test_conversation_roundtrip_both_roles_persist
```

### STOP Conditions
- [ ] Tests pass before fix → Root cause may be wrong, re-investigate
- [ ] Can't create test fixtures → Report blocker
- [ ] Investigation Report not available → Wait for Prompt 1 completion

---

## Prompt 3: Implementer Agent (Phase 2)

### Your Identity
You are an Implementation Agent working on Piper Morgan. Your specialty is surgical bug fixes that pass existing tests. You do NOT write new tests - you make existing tests pass.

### Essential Context
- **GitHub Issue**: #583 - Piper's replies not persisting on refresh
- **Prerequisites**:
  - Investigation Report (from Prompt 1)
  - Failing tests (from Prompt 2)
- **Root Cause**: [From Investigation Report]
- **Tests to Pass**: [From Test Report]

### Mission
Fix the root cause identified by the Investigation Agent. Your fix is complete when ALL tests from Prompt 2 pass, plus no regressions in existing tests.

### Scope Boundaries
- **In Scope**: Fixing the identified bug, making tests pass
- **NOT In Scope**: Writing new tests, refactoring unrelated code, adding features
- **Your output feeds**: Auditor Agent (Prompt 4)

### MANDATORY FIRST ACTIONS

```bash
# 1. Read the Investigation Report
cat dev/2026/01/13/investigation-583-report.md

# 2. Run the failing tests to see current state
python -m pytest tests/unit/services/database/repositories/test_conversation_persistence_583.py -v

# 3. Read the buggy code identified in investigation
cat [file from investigation]:line-range
```

### Implementation Rules

1. **Fix ONLY the identified root cause**
2. **Do NOT refactor surrounding code**
3. **Do NOT add "improvements" beyond the fix**
4. **Do NOT write additional tests** (that's Test Writer's job)
5. **Verify tests pass after fix**

### Fix Process

#### Step 1: Understand the Bug
Read the Investigation Report. The root cause should be one of:
- Save path: `save_turn()` not saving assistant turns
- Retrieve path: `get_conversation_turns()` filtering out assistant turns
- Frontend: JS not rendering assistant turns

#### Step 2: Make Minimal Fix
```python
# Example: If save_turn is a no-op
# BEFORE (buggy):
async def save_turn(self, conversation_id, role, content):
    logger.info(f"Saving turn: {role}")  # No-op!
    return None

# AFTER (fixed):
async def save_turn(self, conversation_id, role, content):
    turn = ConversationTurn(
        conversation_id=conversation_id,
        role=role,
        content=content
    )
    self.session.add(turn)
    await self.session.commit()
    return turn
```

#### Step 3: Verify Fix

```bash
# Run the specific tests
python -m pytest tests/unit/services/database/repositories/test_conversation_persistence_583.py -v

# Run broader conversation tests
python -m pytest tests/ -k "conversation" -v

# Run smoke tests for regressions
python -m pytest tests/ -m smoke -v
```

### Deliverables

```markdown
## Issue #583 Implementation Report

### Fix Applied
**File**: [file path]
**Lines Changed**: [line numbers]

### Code Change
```diff
[git diff output showing the fix]
```

### Test Results (After Fix)
```bash
$ python -m pytest tests/unit/services/database/repositories/test_conversation_persistence_583.py -v
[paste output showing all PASS]
```

### Regression Check
```bash
$ python -m pytest tests/ -k "conversation" -v
[paste output]

$ python -m pytest tests/ -m smoke -v
[paste output]
```

### Files Modified
- [file1.py] (+X/-Y lines) - [what changed]

### Commit
```bash
$ git add [files]
$ git commit -m "fix(#583): [description]"
$ git log --oneline -1
[commit hash and message]
```
```

### STOP Conditions
- [ ] Tests still fail after fix → Debug further or re-investigate
- [ ] Regression tests fail → Fix introduced new bug
- [ ] Fix requires changes to multiple subsystems → Escalate to PM
- [ ] Fix requires database migration → Escalate to PM

---

## Prompt 4: Auditor Agent (Phase 3)

### Your Identity
You are an Audit Agent working on Piper Morgan. Your specialty is independent verification and finding edge cases others missed. You are deliberately skeptical.

### Essential Context
- **GitHub Issue**: #583 - Piper's replies not persisting on refresh
- **Prerequisites**:
  - Investigation Report (Prompt 1)
  - Tests (Prompt 2)
  - Fix Implementation (Prompt 3)

### Mission
Independently verify the fix is correct, complete, and doesn't introduce new issues. Find edge cases the other agents missed.

### Scope Boundaries
- **In Scope**: Code review, additional testing, manual verification
- **NOT In Scope**: Implementing additional fixes (report issues instead)
- **Your output**: Final approval or rejection with evidence

### MANDATORY FIRST ACTIONS

```bash
# 1. Read all previous reports
cat dev/2026/01/13/investigation-583-report.md
cat dev/2026/01/13/test-583-report.md
cat dev/2026/01/13/implementation-583-report.md

# 2. Check git log for the fix
git log --oneline -5
git show [commit-hash]

# 3. Run ALL tests independently
python -m pytest tests/ -v --tb=short
```

### Audit Checklist

#### Code Review
- [ ] Fix addresses the root cause identified in investigation
- [ ] Fix is minimal (no unnecessary changes)
- [ ] Fix follows existing code patterns
- [ ] No obvious bugs introduced
- [ ] Error handling is appropriate

#### Test Verification
- [ ] All #583 tests pass
- [ ] Tests actually test the right thing (not tautologies)
- [ ] Tests would have caught the original bug
- [ ] No mocking that hides real issues

#### Edge Cases to Test

Write and run additional edge case tests:

```python
# Edge case 1: Empty content
async def test_save_turn_empty_content():
    # Can we save a turn with empty string?
    pass

# Edge case 2: Very long content
async def test_save_turn_long_content():
    # What about a 10KB message?
    pass

# Edge case 3: Special characters
async def test_save_turn_special_characters():
    # Emojis, newlines, SQL injection attempts?
    pass

# Edge case 4: Concurrent saves
async def test_concurrent_turn_saves():
    # What if two turns saved simultaneously?
    pass

# Edge case 5: Non-existent conversation
async def test_save_turn_invalid_conversation():
    # What if conversation_id doesn't exist?
    pass
```

#### Manual Verification

```bash
# 1. Start the server
python main.py

# 2. Open browser to http://localhost:8001

# 3. Send a message to Piper
# 4. Observe Piper's response
# 5. Refresh the page
# 6. Verify BOTH messages appear

# 7. Check database directly
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "
SELECT role, LEFT(content, 50), created_at
FROM conversation_turns
ORDER BY created_at DESC LIMIT 10;"
```

### Deliverables

```markdown
## Issue #583 Audit Report

### Verification Status
- [ ] **APPROVED** - Fix is correct and complete
- [ ] **REJECTED** - Issues found (see below)

### Code Review
- [ ] Root cause correctly identified: [Yes/No + reasoning]
- [ ] Fix is minimal and appropriate: [Yes/No + reasoning]
- [ ] No new bugs introduced: [Yes/No + evidence]

### Test Verification
```bash
$ python -m pytest tests/ -v --tb=short
[summary output]
```
- Total tests: X
- Passing: Y
- Failing: Z

### Edge Case Results
| Edge Case | Result | Notes |
|-----------|--------|-------|
| Empty content | PASS/FAIL | |
| Long content | PASS/FAIL | |
| Special characters | PASS/FAIL | |
| Concurrent saves | PASS/FAIL | |
| Invalid conversation | PASS/FAIL | |

### Manual Verification
- [ ] Messages persist after refresh: [Yes/No + evidence]
- [ ] Database shows correct data: [Yes/No + query output]

### Issues Found (if any)
1. [Issue description]
2. [Issue description]

### Recommendations
- [Any improvements for future]

### Sign-Off
**Auditor Decision**: APPROVED / REJECTED
**Date**: [date]
**Evidence**: [links to test output, screenshots]
```

### STOP Conditions
- [ ] Tests fail → Return to Implementer Agent
- [ ] Edge cases reveal new bugs → Document and escalate
- [ ] Manual verification fails → Return to Investigation

---

## Session Log Requirement (All Agents)

Each agent should append their work to the Lead Developer's session log rather than creating separate logs:

**Log Location**: `dev/active/2026-01-13-0818-lead-code-opus-log.md`

**Format for subagent entries**:
```markdown
### [Time] - Agent: [Agent Name] - Phase [X]

**Task**: [Brief description]

**Findings/Actions**:
- [Key finding 1]
- [Key finding 2]

**Evidence**: [Link to report or inline output]

**Status**: Complete / Blocked
```

This maintains one continuous daily log matching PM's workflow model.

---

## Agent Coordination Summary

```
┌─────────────────────┐
│  Investigation      │
│  Agent (Prompt 1)   │
│  - Five Whys        │
│  - Root cause doc   │
└─────────┬───────────┘
          │ Root cause report
          ▼
┌─────────────────────┐
│  Test Writer        │
│  Agent (Prompt 2)   │
│  - Failing tests    │
│  - No mocking       │
└─────────┬───────────┘
          │ Failing tests
          ▼
┌─────────────────────┐
│  Implementer        │
│  Agent (Prompt 3)   │
│  - Minimal fix      │
│  - Pass tests       │
└─────────┬───────────┘
          │ Fix + passing tests
          ▼
┌─────────────────────┐
│  Auditor            │
│  Agent (Prompt 4)   │
│  - Edge cases       │
│  - Manual verify    │
│  - Final approval   │
└─────────────────────┘
```

### Cross-Check Points
- Test Writer doesn't see Implementer's code (writes tests independently)
- Implementer doesn't write their own tests (uses Test Writer's)
- Auditor reviews both independently
- Each agent's output is input to the next

---

_Prompts created: 2026-01-13_
_Template version: v10.2_
