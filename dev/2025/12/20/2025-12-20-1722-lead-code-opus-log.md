# Session Log: 2025-12-20-1722 - Lead Developer - Alpha Testing Resume

**Role**: Lead Developer
**Model**: Claude Opus 4.5
**Date**: Saturday, December 20, 2025
**Time**: 5:22 PM

---

## Session Context

Resuming after a day off (Dec 19). The #485 FK violation bugs have been fixed and are ready for manual testing verification.

**Previous Sessions Summary**:
- **Dec 17**: Investigated and fixed BUG-001 (user_api_keys FK violation) with `store=False` parameter
- **Dec 18**: Fixed BUG-001b (learned_patterns FK violation) with user existence check in IntentService

**Current State**: All automated tests pass. Manual testing needed to verify fixes work in real browser.

---

## To Resume Manual Alpha Testing

### 1. Start the Server

```bash
cd /Users/xian/Development/piper-morgan
python main.py --verbose
```

The server will start on http://localhost:8001

### 2. Clear Database for Fresh Install Test

To simulate a fresh install (no users), run:

```bash
docker exec -i piper-postgres psql -U piper -d piper_morgan << 'EOF'
DELETE FROM user_api_keys;
DELETE FROM learned_patterns;
DELETE FROM learning_settings;
DELETE FROM audit_logs;
DELETE FROM users;
SELECT 'Database cleared for fresh install test' as status;
EOF
```

### 3. Test Scenarios to Verify

| Test | Expected Result | Status |
|------|-----------------|--------|
| Open http://localhost:8001 | Should show setup wizard (fresh install detected) | ⬜ |
| Enter invalid API key → Validate | Should show "validation failed" error (NOT FK violation) | ⬜ |
| Enter valid OpenAI key → Validate | Should show "valid" confirmation (no red error) | ⬜ |
| Complete setup wizard | Should create user and store keys | ⬜ |
| Send chat message | Should work without JS errors or FK violations | ⬜ |

### 4. What to Look For

**Success indicators**:
- No red error boxes with SQL/FK violation text
- Clean validation messages ("API key validation failed" or "valid")
- Chat works after setup completes

**Failure indicators**:
- Red error with "foreign key constraint" or "violates"
- Pink JS error bubbles mentioning "undefined is not an object"
- Server crash or 500 errors

---

## Quick Commands Reference

```bash
# Start server
python main.py --verbose

# Check server logs
tail -f logs/backend.log

# Clear database
docker exec -i piper-postgres psql -U piper -d piper_morgan -c "DELETE FROM users CASCADE;"

# Run fresh install tests
python -m pytest tests/integration/test_fresh_install_flow.py -xvs
```

---

---

## Manual Testing Results

### 6:39 PM - API Key Validation Test ✅ PASSED

PM tested the GUI setup wizard and confirmed:
- OpenAI API key validation shows "✓ Valid"
- **No FK violation error** - the fix is working
- Clean validation flow with no red error boxes

**Screenshot evidence**: Setup wizard showing Step 2 (API Keys) with successful validation

### Current Status

PM is now pulling production branch to alpha testing laptop to continue end-to-end testing. Session may conclude for the day, or may have additional exchanges if new bugs are discovered during evening testing.

---

**Status**: ✅ BUG-001/BUG-001b VERIFIED FIXED - Awaiting full E2E test completion

---

### 6:46 PM - E2E Testing on Alpha Laptop

PM testing on alpha laptop after pulling production. Login works, but two scenarios failing:

1. **"Menu of services" request** → Gets generic answer (not the expected menu)
2. **"Setup projects" request** → Diverts to GitHub issue setup instead

**Console Errors Analysis**:
- All `background.js:70` and `DeviceTrust` errors are from **browser extension (1Password)** - NOT Piper Morgan
- No Piper-specific JavaScript errors visible in the console dump

**Server Status**:
- Server running on port 8001
- Health endpoint responding
- Configuration validation shows some integrations invalid (GitHub, Slack, Notion, Calendar) but these are optional

**Assessment**:
The FK violation bugs are fixed. The new issues appear to be **intent classification/routing issues** - the system is not correctly recognizing what the user is asking for. This is a different category of bug (feature behavior vs crash bug).

**Possible causes**:
1. Intent classifier not recognizing "menu of services" as a specific intent
2. "Setup projects" keyword being caught by GitHub integration pattern
3. Missing or disabled plugin functionality

**Next Steps Options**:
1. Continue E2E testing to fully characterize the behavior
2. File new issues for intent classification bugs
3. End session for today (FK fix validated) and address intent issues next session

---

**Status**: ⏸️ FK BUG FIXED - New intent classification issues discovered, awaiting PM decision

---

## Intent Classification Investigation (7:00 PM onwards)

### GitHub Issue Created

**Issue #487**: [BUG-ALPHA-INTENT: Intent classification failures for capability discovery and project setup](https://github.com/mediajunkie/piper-morgan-product/issues/487)

### Phase 1: Deep Investigation (3 Parallel Subagents)

Deployed 3 subagents to investigate:
1. **Classification Tracer** - Traced exact classification for failing messages
2. **ActionMapper Auditor** - Audited action mapping coverage
3. **Capability Path Mapper** - Mapped all discovery paths

---

### Synthesized Findings

#### Classification Trace for Failing Messages

| Message | Pre-classifier Match | LLM Category | Handler | Root Cause |
|---------|---------------------|--------------|---------|------------|
| "What services do you offer?" | None (NO MATCH) | QUERY/CONVERSATION (ambiguous) | Generic | IDENTITY patterns lack "services" keyword; LLM prompt doesn't clarify |
| "Help me setup my projects" | STATUS (FALSE POSITIVE) | STATUS (inherited) | `_handle_status_query` | "my projects" pattern matches without checking "setup" verb |

#### Root Cause Chain

```
Message 1 ("What services do you offer?"):
Pre-classifier: No pattern for "services" → Falls to LLM
LLM: "services" sounds like product info → Classifies as QUERY
Handler: QUERY handler returns generic response → NOT capability menu

Message 2 ("Help me setup my projects"):
Pre-classifier: "my projects" matches STATUS_PATTERNS → Immediate return
Handler: STATUS handler returns current work → NOT setup guidance
WRONG: Should have triggered GUIDANCE or EXECUTION
```

#### ActionMapper Coverage Summary

- **Total mapped actions**: 26 (todos + GitHub issues + special cases)
- **Design pattern**: ActionMapper only handles EXECUTION category
- **Other categories** (QUERY, ANALYSIS, etc.) route around ActionMapper
- **Gap**: `setup_projects`, `show_capabilities`, `configure_integration` not mapped → 404 NotImplementedError

#### Capability Discovery Paths

| Path | Exists? | User-Facing? | Quality |
|------|---------|--------------|---------|
| IDENTITY handler ("Who are you?") | ✅ | ✅ | GOOD - lists 3-7 capabilities |
| Plugin Registry (get_metadata) | ✅ | ❌ | Rich metadata but HIDDEN |
| REST API for capabilities | ❌ | N/A | **CRITICAL GAP** |
| Help system endpoint | ❌ | N/A | **GAP** |
| Test coverage for discovery | ❌ | N/A | **GAP** |

---

### Systemic Issues Identified

#### Issue A: Command-Oriented Design Gap
- System assumes users know commands ("create a todo")
- No support for discovery-oriented users ("what can you do?")
- IDENTITY handler exists but patterns are incomplete

#### Issue B: Pre-classifier Over-Greedy Matching
- "my projects" matches STATUS without considering verb context
- "setup" verb ignored, message wrongly routed

#### Issue C: Plugin Capabilities Not Exposed
- PluginRegistry has rich metadata (`get_metadata()`, `capabilities`)
- No API endpoint exposes this to users or intent system

#### Issue D: Missing Test Coverage
- No E2E tests for discovery scenarios
- Same pattern as #485 (FK violation) - happy path only

---

### Files Requiring Changes

| File | Change Needed |
|------|---------------|
| `services/intent_service/pre_classifier.py` | Add "services", "offerings", "features" to IDENTITY_PATTERNS |
| `services/intent_service/prompts.py` | Add "services" to IDENTITY vs QUERY disambiguation examples |
| `services/intent_service/pre_classifier.py` | Make STATUS pattern context-aware (check for "setup" verb) |
| `services/intent_service/canonical_handlers.py` | Dynamic capability enumeration from PluginRegistry |
| `web/api/routes/` | Consider `/api/v1/capabilities` endpoint |
| `tests/` | Add discovery scenario tests |

---

### Recommended Fix Approach

**Option B (Lower Risk)**: Extend IDENTITY handler
1. Add "services", "what can you do", "capabilities" to pre-classifier IDENTITY_PATTERNS
2. Update IDENTITY handler to return dynamic capabilities from PluginRegistry
3. Fix STATUS pattern false positive (context-aware matching)
4. Add tests for discovery scenarios

**Estimated Effort**: ~2-3 hours implementation + testing

---

### Discovered Issues for Beads

1. **Pre-classifier over-greedy matching** - "my projects" matches without verb context
2. **Plugin capabilities not bridged to intent** - Architectural gap
3. **No capability discovery tests** - Testing gap
4. **ActionMapper only covers EXECUTION** - Design documentation needed

---

**Status**: 🔍 INVESTIGATION COMPLETE - Ready for implementation planning

---

## Implementation Gameplan (#487)

### Beads Created

| Bead ID | Issue | Priority |
|---------|-------|----------|
| piper-morgan-ti9 | Pre-classifier over-greedy matching | P2 |
| piper-morgan-3t7 | Plugin capabilities not bridged to intent | P2 |
| piper-morgan-d8f | No capability discovery tests | P2 |

---

### Phase 0: Fix Message 1 ("What services do you offer?")

**Goal**: Make "What services do you offer?" return capability menu

**Changes**:

1. **Add patterns to pre_classifier.py** (IDENTITY_PATTERNS)
   ```python
   # Lines 44-52, add to IDENTITY_PATTERNS:
   r"\bwhat services\b",
   r"\bwhat do you offer\b",
   r"\bwhat features\b",
   r"\bwhat can you help with\b",
   r"\bshow me your capabilities\b",
   ```

2. **Update prompts.py** (IDENTITY vs QUERY disambiguation)
   ```python
   # Lines 88-111, add example:
   "What services do you offer?" → IDENTITY (not QUERY)
   ```

**Files**:
- `services/intent_service/pre_classifier.py`
- `services/intent_service/prompts.py`

---

### Phase 1: Fix Message 2 ("Help me setup my projects")

**Goal**: Make "Help me setup my projects" trigger GUIDANCE not STATUS

**Changes**:

1. **Make STATUS pattern context-aware** (pre_classifier.py)
   - Check for action verbs like "setup", "configure", "help with" before matching
   - If action verb present, skip STATUS and route to GUIDANCE/EXECUTION

**Approach A (Simple)**: Add negative lookahead
```python
# Change from:
r"\bmy projects\b"
# To:
r"(?<!setup\s)(?<!configure\s)\bmy projects\b"
```

**Approach B (Robust)**: Add explicit GUIDANCE patterns
```python
# Add to GUIDANCE_PATTERNS:
r"\bhelp.*setup\b",
r"\bhelp.*configure\b",
r"\bsetup.*project\b",
```

**Recommendation**: Approach B (explicit is better than implicit)

**Files**:
- `services/intent_service/pre_classifier.py`

---

### Phase 2: Enhance IDENTITY Handler (Optional)

**Goal**: Return dynamic capabilities from PluginRegistry

**Changes**:

1. **Update canonical_handlers.py** (lines 142-162)
   - Import PluginRegistry
   - Query active plugins
   - Build dynamic capability list

**Note**: This is a P2 enhancement. The immediate fixes (Phase 0-1) address the failing messages.

---

### Phase 3: Add Tests

**Goal**: Prevent regression

**Tests to Add**:

```python
# tests/integration/test_capability_discovery.py

def test_services_query_returns_capabilities():
    """'What services do you offer?' → IDENTITY with capability list"""
    response = client.post("/api/v1/intent", json={"message": "What services do you offer?"})
    assert response.status_code == 200
    data = response.json()
    assert "capabilities" in data["response"].lower() or "piper" in data["response"].lower()

def test_setup_projects_returns_guidance():
    """'Help me setup my projects' → GUIDANCE not STATUS"""
    response = client.post("/api/v1/intent", json={"message": "Help me setup my projects"})
    assert response.status_code == 200
    data = response.json()
    # Should NOT be about current work status
    assert "setup" in data["response"].lower() or "configure" in data["response"].lower()
```

---

### Completion Criteria

| Criteria | Metric |
|----------|--------|
| Message 1 correctly classified | "What services..." → IDENTITY |
| Message 2 correctly classified | "Help me setup..." → GUIDANCE |
| Tests added and passing | 2+ new tests |
| No regressions | Existing tests pass |

---

### Estimated Time

| Phase | Time |
|-------|------|
| Phase 0 (patterns) | 30 min |
| Phase 1 (context-aware) | 30 min |
| Phase 2 (optional) | 1 hour |
| Phase 3 (tests) | 30 min |
| **Total (P0-P1)** | ~1.5 hours |

---

**Status**: 📋 GAMEPLAN READY - Awaiting PM approval to implement

---

## Implementation (Overnight Dec 20-21)

PM approved implementation at end of Dec 20 session. Work completed overnight:

### Phase 0: IDENTITY Patterns ✅
Added 9 new patterns to `services/intent_service/pre_classifier.py`:
- `what services`, `what do you offer`, `what features`
- `what can you help`, `show me your capabilities`, `what can you do`
- `menu of services`, `list.*capabilities`, `your capabilities`

### Phase 1: GUIDANCE Patterns + Order Fix ✅
Added 8 new patterns:
- `help.*setup`, `help.*configure`
- `setup.*projects?`, `configure.*projects?`
- `how do i.*setup`, `how do i.*configure`
- `get started`, `getting started`

**Critical fix**: Moved GUIDANCE check BEFORE STATUS check to catch "help setup my projects" before "my projects" triggers STATUS.

### Phase 3: Tests ✅
Created `tests/integration/test_capability_discovery.py` with 31 tests:
- 12 IDENTITY tests (capability discovery queries)
- 9 GUIDANCE tests (setup/configure queries)
- 6 STATUS regression tests
- 4 IDENTITY regression tests

All 31 tests passing.

### Beads Created
| ID | Issue |
|----|-------|
| piper-morgan-e4k | Pre-existing test_bypass_prevention.py 401 error |

---

**Session End**: 6:55 AM, December 21, 2025 (overnight completion)
**Files Modified**:
- `services/intent_service/pre_classifier.py` - Added patterns, reordered checks
- `tests/integration/test_capability_discovery.py` - New test file (31 tests)

**Status**: ✅ #487 FIX IMPLEMENTED - Ready for manual verification
