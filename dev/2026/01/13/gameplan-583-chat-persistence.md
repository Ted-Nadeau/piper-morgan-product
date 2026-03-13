# Gameplan: Issue #583 - Chat Persistence Bug

**Issue**: #583 - BUG: Piper's replies not persisting on refresh
**Priority**: P1
**Sprint**: A20 (Alpha Testing)
**Created**: 2026-01-13
**Template Version**: v9.3

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Lead Developer's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Database: PostgreSQL on port 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] Existing endpoints: `/api/v1/conversations/latest`, `/api/v1/conversations/{id}/turns` (from #563)
- [x] Repository: ConversationRepository in `services/database/repositories/`

**My understanding of the task**:
- I believe: Assistant (Piper) responses are not being saved or retrieved correctly
- This involves: ConversationRepository.save_turn() or get_conversation_turns()
- Current state: User messages appear after refresh, assistant messages don't

**Suspected 75% Pattern**: #563 implemented conversation persistence on Jan 10. Tables exist, endpoints exist, but something in the save/retrieve path is incomplete.

### Part A.2: Work Characteristics Assessment

Worktrees ADD value when:
- [x] Multiple agents will work in parallel (TDD cross-check approach)
- [x] Task duration >30 minutes (investigation + fix + tests)
- [x] Multi-component work (backend + frontend verification)

**Assessment**: **USE WORKTREE** - Multiple agents, cross-validation required

### Part B: PM Verification Required

**PM, please confirm/correct**:

1. **Recent work in this area?**
   - #563 (Session Continuity) - Jan 10 - implemented save_turn, get_conversation_turns
   - #565 (Conversation History Sidebar) - Jan 10 - implemented conversation list UI
   - Any known issues from #563/#565 implementation?

2. **Actual task needed?**
   - [x] Fix broken functionality (most likely)
   - [ ] Create new feature from scratch
   - [ ] Refactor existing code

3. **Critical context I'm missing?**
   - Was there any testing of assistant message persistence specifically?
   - Are there existing tests for ConversationRepository?

### Part C: Proceed/Revise Decision

- [ ] **PROCEED** - After PM confirms
- [ ] **REVISE** - If assumptions wrong
- [ ] **CLARIFY** - If more context needed

---

## Phase 0: Five-Whys Investigation

### Objective
Systematically trace the data flow to identify exact failure point.

### Five Whys Framework

**Problem**: Piper's replies don't appear after page refresh.

**Why #1**: Are assistant messages being saved to the database?
```sql
-- Check conversation_turns table
SELECT role, content, created_at
FROM conversation_turns
WHERE conversation_id = '[recent_conversation_id]'
ORDER BY created_at;
```

**Why #2**: If not saved - is `save_turn()` being called for assistant responses?
```bash
# Add logging or grep for save_turn calls
grep -rn "save_turn" services/ web/
```

**Why #3**: If save_turn is called - is the role set correctly?
```python
# Check what role value is passed
# Expected: "assistant" or similar
# Bug possibility: "user" for all, or role not passed
```

**Why #4**: If saved correctly - is retrieval filtering by role incorrectly?
```python
# Check get_conversation_turns implementation
# Bug possibility: WHERE role = 'user' hardcoded
```

**Why #5**: If retrieval correct - is frontend filtering or not rendering assistant messages?
```javascript
// Check how messages are rendered
// Bug possibility: CSS hiding, conditional render failing
```

### Investigation Tasks

- [ ] Query database directly for conversation_turns
- [ ] Read ConversationRepository.save_turn() implementation
- [ ] Read ConversationRepository.get_conversation_turns() implementation
- [ ] Read API endpoint that returns turns
- [ ] Read frontend JS that renders messages
- [ ] Identify exact failure point

### Deliverables
- Root cause statement with file:line reference
- Evidence (query output, code snippet showing bug)

---

## Phase 0.6: Data Flow & Integration Verification

### Data Flow Map

```
User sends message
    ↓
POST /api/v1/intent (or similar)
    ↓
IntentService.process_intent()
    ↓
[Handler generates response]
    ↓
??? Where is assistant response saved ???
    ↓
ConversationRepository.save_turn(role="assistant", content=response)
    ↓
Database: conversation_turns table

Page refresh
    ↓
GET /api/v1/conversations/{id}/turns
    ↓
ConversationRepository.get_conversation_turns()
    ↓
??? Does this return assistant turns ???
    ↓
Frontend JS renders messages
```

### Key Questions

| Layer | Question | Verification Method |
|-------|----------|---------------------|
| API Response | Does /intent return response AND save it? | Read route handler |
| Repository Save | Is save_turn called for assistant responses? | Grep + read code |
| Repository Get | Does get_turns return ALL roles? | Read code + test query |
| Frontend | Does JS render role="assistant" messages? | Read JS + browser inspect |

### Integration Points Checklist

| Caller | Callee | Verified? |
|--------|--------|-----------|
| intent route | ConversationRepository.save_turn() | [ ] |
| conversation route | ConversationRepository.get_conversation_turns() | [ ] |
| Frontend JS | /conversations/{id}/turns endpoint | [ ] |

---

## Phase 1: TDD - Write Failing Tests First

### Objective
Create tests that FAIL with current code, proving the bug exists.

### Test Agent Instructions (Agent A - Test Writer)

Write the following tests in `tests/unit/services/database/repositories/test_conversation_repository_persistence.py`:

```python
# Test 1: save_turn correctly saves assistant role
async def test_save_turn_with_assistant_role():
    """Verify assistant messages are saved with correct role."""
    # Arrange
    repo = ConversationRepository(session)
    conversation = await create_test_conversation()

    # Act
    await repo.save_turn(
        conversation_id=conversation.id,
        role="assistant",
        content="This is Piper's response"
    )

    # Assert - query DB directly
    turns = await session.execute(
        select(ConversationTurn).where(
            ConversationTurn.conversation_id == conversation.id,
            ConversationTurn.role == "assistant"
        )
    )
    assert len(turns.all()) == 1
    assert turns[0].content == "This is Piper's response"

# Test 2: get_turns returns ALL roles (not filtered)
async def test_get_turns_returns_all_roles():
    """Verify both user and assistant turns are returned."""
    # Arrange
    repo = ConversationRepository(session)
    conversation = await create_test_conversation()

    # Save both user and assistant turns
    await repo.save_turn(conversation.id, role="user", content="User message")
    await repo.save_turn(conversation.id, role="assistant", content="Assistant reply")

    # Act
    turns = await repo.get_conversation_turns(conversation.id)

    # Assert
    assert len(turns) == 2
    roles = {t.role for t in turns}
    assert "user" in roles
    assert "assistant" in roles

# Test 3: Integration - full roundtrip
async def test_conversation_roundtrip_both_roles():
    """End-to-end: save user+assistant, retrieve both."""
    # Full integration test with real DB
    pass
```

### Test Requirements
- [ ] Tests must FAIL before fix (proving bug exists)
- [ ] Tests must target exact suspected failure points
- [ ] Tests must not mock the repository internals

---

## Phase 2: Implementation

### Objective
Fix the root cause identified in Phase 0.

### Implementation Agent Instructions (Agent B - Implementer)

**After Phase 0 identifies root cause**, fix the specific issue. Possible fixes:

**If save_turn not called for assistant**:
- Find where response is generated
- Add save_turn call after response generation

**If role incorrectly set**:
- Fix the role parameter being passed

**If get_turns filtering**:
- Remove incorrect WHERE clause or fix query

**If frontend filtering**:
- Fix JS rendering logic

### Implementation Requirements
- [ ] Fix ONLY the identified root cause
- [ ] Do not refactor unrelated code
- [ ] Ensure Phase 1 tests pass after fix
- [ ] Run full test suite - no regressions

---

## Phase 3: Cross-Validation

### Objective
Independent verification by separate agent.

### Audit Agent Instructions (Agent C - Auditor)

1. **Code Review**:
   - Read the fix implementation
   - Verify it addresses root cause
   - Check for edge cases missed

2. **Additional Test Cases**:
   - Empty conversation
   - Very long messages
   - Special characters in content
   - Concurrent saves

3. **Manual Verification**:
   - Start server
   - Send message, get response
   - Refresh page
   - Verify both messages appear

### Cross-Validation Requirements
- [ ] Auditor confirms fix addresses root cause
- [ ] Auditor confirms no obvious regressions
- [ ] Manual test passes

---

## Phase Z: Completion & Handoff

### Completion Checklist

- [ ] Root cause documented with evidence
- [ ] Unit tests written and passing
- [ ] Integration tests written and passing
- [ ] Fix implemented
- [ ] Cross-validation complete
- [ ] Manual testing verified
- [ ] No regressions (full test suite passes)
- [ ] Session log updated
- [ ] GitHub issue updated with evidence

### Evidence Required

| Item | Evidence |
|------|----------|
| Root cause | File:line + explanation |
| Tests | pytest output showing pass |
| Fix | Commit hash + diff |
| Cross-validation | Auditor sign-off |
| Manual test | Screenshot or terminal output |

---

## Multi-Agent Coordination Plan

### Agent Deployment Map

| Phase | Agent | Role | Evidence Required |
|-------|-------|------|-------------------|
| 0 | Explore Agent | Investigation | Root cause doc |
| 1 | Agent A | TDD Test Writer | Failing test file |
| 2 | Agent B | Implementer | Fix + passing tests |
| 3 | Agent C | Auditor | Review report |

### Cross-Check Design

```
Agent A (Tests) ←→ Agent B (Implementation)
       ↓                    ↓
       └──→ Agent C (Audit) ←──┘
```

- Agent A writes tests without seeing implementation
- Agent B implements fix without writing their own tests
- Agent C reviews both independently
- Agent D (optional): Additional edge case testing

### Handoff Protocol

1. Phase 0 complete → Document root cause → All agents read
2. Agent A complete → Tests committed → Agent B sees test locations
3. Agent B complete → Fix committed → Agent C reviews both
4. Agent C complete → Report submitted → Lead Dev compiles evidence

### Verification Gates

- [ ] **Gate 0→1**: Root cause identified with file:line evidence
- [ ] **Gate 1→2**: Failing tests exist and are committed
- [ ] **Gate 2→3**: All tests pass, no regressions
- [ ] **Gate 3→Z**: Audit report approves fix

**NO phase proceeds without gate verification.**

### Evidence Collection Points

| Point | When | What to Collect |
|-------|------|-----------------|
| Post-Phase 0 | After root cause | SQL query output, code snippet |
| Post-Phase 1 | After tests written | pytest output showing FAIL |
| Post-Phase 2 | After fix | pytest output showing PASS |
| Post-Phase 3 | After audit | Auditor sign-off statement |
| Post-Phase Z | Before closure | All evidence compiled |

---

## STOP Conditions

Stop immediately and escalate if:
- [ ] ConversationRepository fundamentally broken (not just incomplete)
- [ ] Database schema needs migration
- [ ] Bug affects data integrity beyond this feature
- [ ] Fix requires changes to authentication/session handling
- [ ] Multiple unrelated bugs discovered

---

## Success Metrics

### Quantitative
- 100% of conversation turns (user + assistant) persist
- 0 regressions in existing test suite
- Page load with conversation < 2 seconds

### Qualitative
- Alpha testers can trust conversation history
- Clean audit report from Agent C

---

## Appendix: Related Code Locations (To Be Verified)

```
services/database/repositories/conversation_repository.py
  - save_turn()
  - get_conversation_turns()

web/api/routes/conversations.py (or similar)
  - GET /{id}/turns endpoint

web/api/routes/intent.py
  - Where response is generated and (maybe) saved

templates/index.html or web/static/js/
  - Frontend conversation rendering
```

---

_Gameplan created: 2026-01-13 08:55_
_Status: Awaiting PM verification of Phase -1_
