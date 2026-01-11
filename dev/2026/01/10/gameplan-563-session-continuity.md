# Gameplan: Issue #563 - CONV-PERSIST-1: Session Continuity & Auto-Save

**Date**: 2026-01-10
**Issue**: https://github.com/mediajunkie/piper-morgan-product/issues/563
**Parent**: #314 (CONV-UX-PERSIST)
**Priority**: P1 (Foundational)

---

## Phase -1: Infrastructure Verification Checkpoint

### Part A: Chief Architect's Current Understanding

**Infrastructure Status**:
- [x] Web framework: FastAPI (confirmed)
- [x] Database: PostgreSQL on port 5433 (confirmed)
- [x] Testing framework: pytest (confirmed)
- [x] Existing endpoints: `/api/v1/conversations/*` routes exist
- [x] Missing features: **Repository methods are stubbed - this is the root cause**

**My understanding of the task**:
- The `ConversationRepository` has three stubbed methods that return empty data
- The database tables (`conversations`, `conversation_turns`) already exist via migration
- We need to implement the actual repository methods to wire up persistence
- Auto-save is already being called (`conversation_manager.py:133`) but goes to the stub

### Part A.2: Work Characteristics Assessment

**Worktree Assessment:**
- [ ] Multiple agents will work in parallel - NO, single agent sequential
- [ ] Task duration >30 minutes - YES, likely
- [x] Tightly coupled files requiring atomic commits
- [x] Time-critical foundation work

**Assessment: SKIP WORKTREE** - Single agent, tightly coupled repository/manager changes, atomic commits needed.

### Part B: PM Verification Required

**What actually exists:**
```
services/database/repositories.py:829-855  # ConversationRepository (STUBBED)
services/database/models.py:679-700        # ConversationTurnDB (full schema)
services/database/models.py:~650           # ConversationDB (full schema)
alembic/versions/a9ee08bbdf8c_*            # Migration exists, tables created
services/conversation/conversation_manager.py # Calls save_turn() already
```

**Recent work in this area:**
- Migration created August 2025 (PM-034 Phase 1)
- Repository stubbed with comments "we don't have DB table yet" - but we DO have tables
- Clear 75% pattern - infrastructure built but not wired

**Actual task needed:**
- [x] Fix incomplete functionality (complete the 75% pattern)
- [x] Bug fix (missing assistant responses)

### Part C: Proceed/Revise Decision

- [x] **PROCEED** - Understanding is correct, gameplan appropriate

---

## Phase 0: Initial Bookending - GitHub Investigation

### Required Actions

```bash
# 1. Verify issue exists and is assigned
gh issue view 563

# 2. Update issue status
gh issue edit 563 --body "## Status: Implementation Started
- [x] Root cause identified: ConversationRepository methods are stubs
- [x] Database tables exist (migration a9ee08bbdf8c)
- [ ] Repository methods implemented
- [ ] Auto-save verified
- [ ] Continue prompt added
- [ ] Save indicator added"
```

### Root Cause Confirmed

The `ConversationRepository` methods are **stubs that return empty data**:

```python
# services/database/repositories.py lines 837-855

async def get_conversation_turns(...) -> List[domain.ConversationTurn]:
    # For now, return empty list since we don't have DB table yet
    return []  # <-- THIS IS THE BUG

async def save_turn(self, turn: domain.ConversationTurn, ...) -> None:
    # For now, this is a no-op since we don't have DB table yet
    logger.info(f"ConversationTurn saved (cache-only): {turn.id}")  # <-- NO-OP

async def get_next_turn_number(...) -> int:
    # For now, return 1 as fallback
    return 1  # <-- ALWAYS RETURNS 1
```

**Why this explains the bug:**
1. User sends message → `conversation_manager.py:133` calls `_save_turn_to_database()`
2. `_save_turn_to_database()` calls `repo.save_turn(turn)` → **NO-OP**
3. On page refresh, frontend requests conversation turns
4. Repository returns `[]` → Only user messages (from localStorage?) display, no responses

---

## Phase 0.6: Data Flow & Integration Verification

### Data Flow Requirements

| Layer | Purpose | Status |
|-------|---------|--------|
| `ConversationDB` | Store conversation metadata | Table exists, model exists |
| `ConversationTurnDB` | Store turn data (user + assistant) | Table exists, model exists |
| `ConversationRepository` | CRUD operations | **STUBBED - needs implementation** |
| `ConversationManager` | Business logic | Calls repository methods correctly |

### Integration Points Verified

| Caller | Callee | Import Works? | Method Exists? | Parameters OK? |
|--------|--------|---------------|----------------|----------------|
| conversation_manager | ConversationRepository | ✓ | ✓ | ✓ |
| ConversationRepository | domain.ConversationTurn | ✓ | ✓ | ✓ |
| ConversationRepository | ConversationTurnDB | ✓ | ✓ | Need to add mapping |

---

## Phase 0.5: Frontend-Backend Contract Verification

### When to Apply
Phases 3-4 involve frontend work calling backend endpoints. Verify contracts BEFORE writing frontend.

### Backend Endpoints Needed

| Endpoint | Route Path | Mount Prefix | Full Path |
|----------|------------|--------------|-----------|
| get_latest | /latest | /api/v1/conversations | /api/v1/conversations/latest |
| get_turns | /{id}/turns | /api/v1/conversations | /api/v1/conversations/{id}/turns |

### Verification (Before Phase 3)
```bash
# Verify conversations router is mounted
grep -n "conversations" web/app.py web/router_initializer.py

# After creating endpoints, verify they work
curl -s http://localhost:8001/api/v1/conversations/latest -H "Authorization: Bearer $TOKEN"
# Must NOT return {"detail":"Not Found"}
```

### Static Files
```bash
# Verify static file serving for any new JS
grep -n "StaticFiles" web/app.py
# Confirm: web/static/ → /static/
```

---

## Phase 0.8: Post-Completion Integration

### Completion Side-Effects

When this feature completes successfully:

| Side Effect | Table/Field | Value | Verified? |
|-------------|-------------|-------|-----------|
| Turns persisted | conversation_turns | N rows | [ ] |
| Conversation updated | conversations.updated_at | now() | [ ] |
| Last activity tracked | conversations.last_activity_at | now() | [ ] |

### Downstream Behavior Changes

| Feature | Before Completion | After Completion |
|---------|-------------------|------------------|
| Page refresh | Loses assistant responses | Full conversation restores |
| Returning user | No prompt | "Continue where you left off?" |
| Message send | No feedback | Subtle save indicator |

---

## Phase 1: Implement ConversationRepository Methods

### 1.1 Implement `save_turn()`

**File**: `services/database/repositories.py`

Replace stub with actual database write:

```python
async def save_turn(self, turn: domain.ConversationTurn, is_admin: bool = False) -> None:
    """Save conversation turn to database."""
    from services.database.models import ConversationTurnDB

    db_turn = ConversationTurnDB(
        id=turn.id,
        conversation_id=turn.conversation_id,
        turn_number=turn.turn_number,
        user_message=turn.user_message,
        assistant_response=turn.assistant_response,
        intent=turn.intent,
        entities=turn.entities,
        references=turn.references,
        context_used=turn.context_used,
        turn_metadata=turn.metadata,
        processing_time=turn.processing_time,
        created_at=turn.created_at,
        completed_at=turn.completed_at,
    )

    self.session.add(db_turn)
    await self.session.commit()
    logger.info(f"ConversationTurn saved to database: {turn.id}")
```

### 1.2 Implement `get_conversation_turns()`

```python
async def get_conversation_turns(
    self, conversation_id: str, limit: int = 10, is_admin: bool = False
) -> List[domain.ConversationTurn]:
    """Get conversation turns for a conversation ID."""
    from services.database.models import ConversationTurnDB
    from sqlalchemy import select

    stmt = (
        select(ConversationTurnDB)
        .where(ConversationTurnDB.conversation_id == conversation_id)
        .order_by(ConversationTurnDB.turn_number)
        .limit(limit)
    )

    result = await self.session.execute(stmt)
    db_turns = result.scalars().all()

    return [
        domain.ConversationTurn(
            id=t.id,
            conversation_id=t.conversation_id,
            turn_number=t.turn_number,
            user_message=t.user_message,
            assistant_response=t.assistant_response,
            intent=t.intent,
            entities=t.entities,
            references=t.references,
            context_used=t.context_used,
            metadata=t.turn_metadata,
            processing_time=t.processing_time,
            created_at=t.created_at,
            completed_at=t.completed_at,
        )
        for t in db_turns
    ]
```

### 1.3 Implement `get_next_turn_number()`

```python
async def get_next_turn_number(self, conversation_id: str, is_admin: bool = False) -> int:
    """Get next turn number for conversation."""
    from services.database.models import ConversationTurnDB
    from sqlalchemy import select, func

    stmt = select(func.max(ConversationTurnDB.turn_number)).where(
        ConversationTurnDB.conversation_id == conversation_id
    )

    result = await self.session.execute(stmt)
    max_turn = result.scalar()

    return (max_turn or 0) + 1
```

### Acceptance Criteria - Phase 1

- [ ] `save_turn()` writes to database (verify with SQL query)
- [ ] `get_conversation_turns()` returns actual turns
- [ ] `get_next_turn_number()` returns correct sequence
- [ ] Unit tests for all three methods
- [ ] Integration test: save → retrieve roundtrip

### Progressive Bookending - Phase 1
```bash
gh issue comment 563 -b "✓ Phase 1 Complete: Repository Methods Implemented

Evidence:
- save_turn(): [SQL verification output]
- get_conversation_turns(): [test output]
- get_next_turn_number(): [test output]

Tests: X unit tests, Y integration tests passing"
```

### Verification Gate
- [ ] All Phase 1 acceptance criteria met before starting Phase 2
- [ ] Tests passing: `python -m pytest tests/unit/services/database/test_conversation_repository.py -v`

---

## Phase 2: Verify Auto-Save Already Works

The auto-save trigger already exists in `conversation_manager.py:133`:
```python
await self._save_turn_to_database(turn)
```

Once Phase 1 is complete, auto-save will work automatically because:
1. `_save_turn_to_database()` calls `repo.save_turn(turn)`
2. `save_turn()` will now actually persist to database

### Verification Steps
- [ ] Send message in UI
- [ ] Check database: `SELECT * FROM conversation_turns ORDER BY created_at DESC LIMIT 1;`
- [ ] Verify both `user_message` AND `assistant_response` are populated

### Progressive Bookending - Phase 2
```bash
gh issue comment 563 -b "✓ Phase 2 Complete: Auto-Save Verified

Evidence:
- SQL query showing both user_message and assistant_response populated
- Screenshot or terminal output

No code changes needed - existing wiring now works with Phase 1 fix."
```

### Verification Gate
- [ ] Database shows complete turns before starting Phase 3

---

## Phase 3: Implement "Continue Where You Left Off" Prompt

### 3.1 Frontend Detection

When user loads app, check for existing conversation:

**File**: `templates/components/chat.html` (or relevant JS)

```javascript
async function checkForExistingConversation() {
    const response = await fetch('/api/v1/conversations/latest');
    const data = await response.json();

    if (data.conversation && data.has_turns) {
        showContinuePrompt(data.conversation);
    }
}
```

### 3.2 Backend Endpoint

**File**: `web/api/routes/conversations.py`

```python
@router.get("/latest")
async def get_latest_conversation(current_user: JWTClaims = Depends(get_current_user)):
    """Get user's most recent conversation for restore prompt."""
    repo = ConversationRepository(session)
    conversation = await repo.get_latest_for_user(current_user.sub)

    if not conversation:
        return {"conversation": None, "has_turns": False}

    turns = await repo.get_conversation_turns(conversation.id, limit=1)
    return {
        "conversation": conversation,
        "has_turns": len(turns) > 0
    }
```

### 3.3 UI Component

Subtle toast or inline prompt:
```
"Continue your conversation from earlier? [Yes] [Start Fresh]"
```

### Acceptance Criteria - Phase 3

- [ ] `/api/v1/conversations/latest` endpoint exists
- [ ] Returns null if no previous conversation
- [ ] Returns conversation + has_turns if exists
- [ ] UI shows prompt when conversation exists
- [ ] "Yes" restores conversation
- [ ] "Start Fresh" creates new conversation

### Progressive Bookending - Phase 3
```bash
gh issue comment 563 -b "✓ Phase 3 Complete: Continue Prompt Implemented

Evidence:
- curl output showing /latest endpoint works
- Screenshot of continue prompt UI
- Test of Yes/Start Fresh buttons

Files modified:
- web/api/routes/conversations.py
- templates/components/chat.html (or relevant)"
```

### Verification Gate
- [ ] Endpoint returns correct data
- [ ] UI prompt appears for returning users
- [ ] Both buttons work correctly

---

## Phase 4: Add Save Indicator

### 4.1 Visual Feedback

After each message exchange, show subtle indicator:
- Checkmark icon that fades in/out
- Or status text "Saved" that appears briefly

### 4.2 Implementation

Add state tracking in frontend:
```javascript
async function sendMessage(message) {
    const response = await fetch('/api/v1/intent', {...});
    // ... handle response ...

    showSaveIndicator();  // Brief visual feedback
}

function showSaveIndicator() {
    const indicator = document.getElementById('save-indicator');
    indicator.classList.add('visible');
    setTimeout(() => indicator.classList.remove('visible'), 1500);
}
```

### Acceptance Criteria - Phase 4

- [ ] Save indicator element exists
- [ ] Shows after successful message exchange
- [ ] Fades after 1.5 seconds
- [ ] Does not interfere with conversation flow

### Progressive Bookending - Phase 4
```bash
gh issue comment 563 -b "✓ Phase 4 Complete: Save Indicator Added

Evidence:
- Screenshot/GIF of indicator appearing and fading
- CSS/JS changes documented

Files modified:
- templates/components/chat.html
- web/static/css/[relevant].css (if needed)"
```

---

## Phase Z: Final Verification

### Complete Acceptance Criteria

From Issue #563:
- [ ] Conversations persist across page refresh (100%)
- [ ] Both user messages AND assistant responses restore
- [ ] Auto-save triggers after each exchange
- [ ] "Continue where you left off" prompt appears appropriately
- [ ] Save indicator provides feedback
- [ ] Restore performance <500ms
- [ ] Unit tests for repository methods
- [ ] Integration tests for save/restore flow
- [ ] Zero regressions

### Evidence Required

```bash
# 1. Database verification
docker exec -it piper-postgres psql -U piper -d piper_morgan \
  -c "SELECT id, user_message, assistant_response FROM conversation_turns ORDER BY created_at DESC LIMIT 3;"

# 2. Test results
python -m pytest tests/unit/services/conversation/ -v
python -m pytest tests/integration/services/conversation/ -v

# 3. Manual verification
# - Send message, refresh page, verify both sides restore
# - Clear localStorage, refresh, verify database-only restore works
```

---

## Test Scope Requirements

| Test Type | What It Tests | Location |
|-----------|---------------|----------|
| **Unit** | Repository methods in isolation | `tests/unit/services/database/test_conversation_repository.py` |
| **Integration** | Save → retrieve roundtrip with real DB | `tests/integration/services/conversation/test_persistence.py` |
| **Wiring** | ConversationManager → Repository → DB chain | `tests/integration/services/conversation/test_wiring.py` |
| **Regression** | Existing conversation features still work | `tests/unit/services/conversation/` (existing) |

---

## Multi-Agent Deployment Map

| Phase | Agent Type | Evidence Required | Handoff |
|-------|------------|------------------|---------|
| 1 | Code Agent | Unit tests, SQL verification | Test locations, commit hash |
| 2 | Code Agent (same) | SQL query showing complete turns | Verification output |
| 3 | Code Agent | curl output, UI screenshot | Endpoint paths |
| 4 | Code Agent | Screenshot/GIF | CSS/JS file locations |
| Z | Lead Dev | Full test suite, PM review request | Issue ready for closure |

**Single Agent Justification**: Sequential phases with dependencies. Phase 2 depends on Phase 1, etc.

---

## Documentation Updates

- [ ] Update `docs/internal/architecture/current/patterns/` if new pattern emerges
- [ ] No ADR needed (completing existing infrastructure)
- [ ] Remove "we don't have DB table yet" comments from repository
- [ ] Update BRIEFING-CURRENT-STATE if significant

---

## Completion Matrix

| Phase | Deliverable | Verified By |
|-------|-------------|-------------|
| Phase 1 | 3 repository methods implemented | Unit tests + SQL query |
| Phase 2 | Auto-save working | Database shows complete turns |
| Phase 3 | Continue prompt | Endpoint + UI verification |
| Phase 4 | Save indicator | Visual confirmation |
| Phase Z | Issue closed | PM approval |

---

## STOP Conditions

- [ ] If database schema doesn't match domain model → STOP
- [ ] If save_turn() fails silently → STOP, add error handling
- [ ] If existing frontend expects different data format → STOP, verify contract
- [ ] If tests fail → STOP, fix before proceeding
- [ ] If endpoint path mismatch with frontend → STOP, verify Phase 0.5

---

## Summary

**Root Cause**: `ConversationRepository` methods are stubs returning empty data despite database tables existing.

**Fix**: Implement the three stubbed methods to actually read/write from PostgreSQL.

**Why This Was Missed**: Comments say "we don't have DB table yet" but migration was created August 2025. Classic 75% pattern - infrastructure built but wiring incomplete.

**Effort Estimate**: Phase 1 (repository) is the core fix. Phases 2-4 build on the foundation.
