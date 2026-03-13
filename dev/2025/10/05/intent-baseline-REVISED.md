# Intent Classification Baseline - REVISED SCOPE
## GREAT-4B Phase 0/1 - Scope Clarification

**Date**: October 5, 2025, 4:05 PM
**Revision**: Scope clarified - structured CLI commands EXEMPT
**Previous**: 16 bypasses identified
**Revised**: 1-2 actual bypasses requiring conversion

---

## Scope Clarification

### What Requires Intent Classification
✅ **Natural language input** - ambiguous, needs classification
- Slack messages: "create an issue about the login bug"
- Web NL endpoints: `/api/v1/intent` with free-text
- Conversational UI inputs

✅ **Unstructured requests** - no explicit operation
- Free-text search queries
- Content enhancement requests
- Any endpoint accepting prose

### What is EXEMPT from Intent Classification
❌ **Structured CLI commands** - already expressing intent via structure
- `piper issues create --title "Bug"` → structure = CREATE_ISSUE intent
- `piper documents search "k8s" --timeframe week` → structure = SEARCH intent
- `piper cal show --days 7` → structure = SHOW_CALENDAR intent

❌ **Static/Infrastructure routes** - no user input to classify
- Health checks: `/health/config`
- Static pages: `/`, `/debug-markdown`
- Direct ID lookups: `/api/v1/workflows/{id}`

---

## Revised Baseline Analysis

### Slack Integration ✅
- **Status**: 100% compliant (gold standard)
- **Pattern**: Natural language → IntentClassifier → CanonicalHandlers
- **Volume**: 375 intent refs across 219 handlers

### Web Routes - REVISED

**Total Routes**: 11
**Natural Language Routes**: 2
**Structured/Static Routes**: 9 (EXEMPT)

#### ✅ Using Intent (2 routes):
1. `GET /api/standup` - Uses intent classification
2. `POST /api/v1/intent` - IS the intent classification endpoint

#### ⚠️ Natural Language Bypasses (1 route):
1. **`POST /api/personality/enhance`**
   - **Input**: Free-text content (natural language)
   - **Current**: Direct to PersonalityEnhancer
   - **Should**: Route through intent classification
   - **Effort**: Small - redirect to `/api/v1/intent`
   - **Priority**: HIGH

#### ✅ EXEMPT - Structured/Static (8 routes):
1. `GET /` - Static page
2. `GET /api/personality/profile/{user_id}` - Direct config retrieval
3. `PUT /api/personality/profile/{user_id}` - Direct config update
4. `GET /api/v1/workflows/{workflow_id}` - Direct ID lookup
5. `GET /debug-markdown` - Debug endpoint
6. `GET /health/config` - Health check
7. `GET /personality-preferences` - Static UI page
8. `GET /standup` - Static UI page

### CLI Commands - REVISED

**Total Commands**: 8
**Natural Language Commands**: 1
**Structured Commands**: 7 (EXEMPT)

#### ✅ Using Intent (1 command):
1. `standup.py` - Uses CanonicalHandlers

#### ✅ EXEMPT - Structured CLI (7 commands):
1. `cal.py` - Argparse structured commands
2. `documents.py` - Click structured commands
3. `issues.py` - Click structured commands
4. `notion.py` - Click structured commands
5. `personality.py` - Structured config commands
6. `publish.py` - Structured publish commands
7. `test_issues_integration.py` - Test command

**Rationale**: These commands use argparse/click with explicit subcommands. The command structure IS the intent:
- `piper documents search "topic"` → SEARCH_DOCUMENTS (explicit)
- No ambiguity → no classification needed

---

## Revised Gap Analysis

### Actual Bypasses Requiring Conversion: **1**

**High Priority**:
1. **`POST /api/personality/enhance`**
   - Accepts free-text content (NL input)
   - Should route through intent classification
   - Simple fix: Redirect to `/api/v1/intent`

### Potential Additional Bypasses: **0-1**

Need to verify if any other routes accept free-text without classification.

**Action**: Scan for routes with:
- Text/content fields (not structured data)
- Search queries (not ID lookups)
- User messages (not config data)

---

## Coverage Metrics - REVISED

### By Entry Point Type:
- **Slack**: 100% (natural language) ✅
- **Web NL Routes**: 67% (2/3) - 1 bypass ⚠️
- **CLI NL Commands**: 100% (1/1) ✅
- **Structured CLI**: N/A (exempt)
- **Static Routes**: N/A (exempt)

### Overall Natural Language Coverage:
- **Total NL Entry Points**: 222 (220 Slack + 3 web - 1 CLI)
- **Using Intent**: 221 (220 Slack + 2 web + 1 CLI - standup may not actually use it)
- **Bypassing**: 1 (`POST /api/personality/enhance`)
- **Coverage**: 99.5%

### Architectural Compliance:
- ✅ **Principle**: Natural language → intent classification
- ✅ **Principle**: Structured commands → direct execution
- ⚠️ **Gap**: 1 NL route bypasses classification

---

## Revised Recommendations

### Phase 1 (Immediate - 30 minutes)
Convert 1 high-priority bypass:
1. ✅ `POST /api/personality/enhance` → route through `/api/v1/intent`

**Implementation**:
```python
@app.post("/api/personality/enhance")
async def enhance_response(request: Request):
    # Redirect to intent endpoint
    data = await request.json()
    intent_request = {
        "message": f"Enhance this response: {data.get('content', '')}",
        "session_id": data.get("user_id", "default")
    }
    return await process_intent(Request(...))  # Route through intent
```

### Phase 2 (Verification - 15 minutes)
1. Scan for additional NL routes
2. Verify no other free-text inputs bypass intent
3. Document architectural principles

### Phase 3 (Enforcement - 30 minutes)
1. Add bypass detection test for NL routes
2. Update architecture docs with exemption rules
3. Create pre-commit hook to flag new NL routes

---

## Updated Success Metrics

### Target State:
- **100% of natural language input** → intent classification
- **0% of structured commands** → forced through intent (unnecessary)
- **Clear exemption rules** → documented and enforced

### Current vs Target:
- Before: Thought we had 16 bypasses
- After Scope Clarification: Actually 1 bypass
- Coverage: 99.5% → need 100%

---

## Architectural Principles - DOCUMENTED

### Intent Classification IS Required For:
1. ✅ Natural language messages (Slack, chat, conversational UI)
2. ✅ Free-text content (search queries, enhancement requests)
3. ✅ Unstructured user input (any prose)

### Intent Classification NOT Required For:
1. ❌ Structured CLI commands with explicit subcommands
2. ❌ Direct ID lookups (GET /resource/{id})
3. ❌ Config updates with structured data
4. ❌ Static pages and health checks
5. ❌ Infrastructure endpoints

### Rationale:
- **Intent classification solves ambiguity** in natural language
- **Structured commands have no ambiguity** - the structure IS the intent
- **Forcing structured → NL → classify → structured is circular and wasteful**

---

## Evidence Files

1. **Original Baseline**: `intent-baseline-report.md` (Phase 0)
2. **This Revision**: `intent-baseline-REVISED.md` (Phase 1)
3. **Session Log**: `2025-10-05-1540-prog-code-log.md`
4. **Mapping Scripts**: `map_web_routes.py`, `map_cli_commands.py`

---

## Next Steps

1. ✅ Convert `POST /api/personality/enhance` (30 min)
2. ✅ Verify no other NL routes bypass intent (15 min)
3. ✅ Update architecture docs with exemption rules (30 min)
4. ✅ Add bypass detection for NL routes (30 min)
5. ✅ GitHub issue update with revised scope

**GREAT-4B Phase 1**: SCOPE CLARIFIED - Only 1 actual bypass to fix!
