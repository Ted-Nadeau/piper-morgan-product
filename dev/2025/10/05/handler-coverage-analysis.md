# Handler Coverage Analysis - GREAT-4C Phase -1 Investigation

**Date**: October 5, 2025, 8:20 PM
**Epic**: GREAT-4C - Canonical Handlers Enhancement
**GitHub Issue**: TBD

---

## Executive Summary

**CRITICAL FINDING**: The GREAT-4C gameplan assumed "219 handlers" exist, but investigation reveals only **5 canonical handlers** exist in `canonical_handlers.py`. However, this is **NOT a gap** - it's a misunderstanding of the architecture.

**Actual Architecture**: IntentService routes to different systems based on intent category, not all through canonical_handlers.py.

---

## Intent Classification → Handler Routing Flow

### Classification Results (Test Evidence)

From `test_unhandled_intent.py` execution:

| Query | Category | Action | Confidence | Source |
|-------|----------|--------|------------|--------|
| "what day is it" | TEMPORAL | get_current_time | 1.0 | PRE_CLASSIFIER |
| "what am i working on" | STATUS | get_project_status | 1.0 | PRE_CLASSIFIER |
| "what's my top priority" | PRIORITY | get_top_priority | 1.0 | PRE_CLASSIFIER |
| "create an issue about login bug" | EXECUTION | create_issue | 0.95 | LLM |
| "update the status of issue 123" | EXECUTION | update_issue_status | 0.95 | LLM |
| "search for architecture docs" | QUERY | search_documents | 0.95 | LLM |
| "analyze the codebase" | ANALYSIS | analyze_codebase | 0.85 | LLM |

### Routing Architecture

**IntentService.process_intent() flow**:

```python
# services/intent/intent_service.py

async def process_intent(message, session_id):
    # 1. Classify intent
    intent = await classifier.classify(message)

    # 2. Route by category
    if intent.category == "CONVERSATION":
        return await _handle_conversation_intent(intent, session_id)

    # 3. Create workflow
    workflow = await orchestration_engine.create_workflow_from_intent(intent)

    # 4. Route QUERY intents
    if intent.category == "QUERY":
        return await _handle_query_intent(intent, workflow, session_id)

    # 5. All other intents (EXECUTION, ANALYSIS, etc.)
    return await _handle_generic_intent(intent)
```

---

## Handler Coverage by Intent Category

### TEMPORAL (17 patterns) → ✅ canonical_handlers.py
**Handler**: `CanonicalHandlers._handle_temporal_query()`
**Location**: `services/intent_service/canonical_handlers.py:127`
**Status**: Operational (GREAT-4A validated)

**Actions**:
- `get_current_time`
- `get_date`
- `get_yesterday_summary`
- etc.

---

### STATUS (14 patterns) → ✅ canonical_handlers.py
**Handler**: `CanonicalHandlers._handle_status_query()`
**Location**: `services/intent_service/canonical_handlers.py:147`
**Status**: Operational (GREAT-4A validated)

**Actions**:
- `get_project_status`
- `list_projects`
- `show_project_overview`
- etc.

---

### PRIORITY (13 patterns) → ✅ canonical_handlers.py
**Handler**: `CanonicalHandlers._handle_priority_query()`
**Location**: `services/intent_service/canonical_handlers.py:167`
**Status**: Operational (GREAT-4A validated)

**Actions**:
- `get_top_priority`
- `get_focus_recommendations`
- etc.

---

### IDENTITY → ✅ canonical_handlers.py
**Handler**: `CanonicalHandlers._handle_identity_query()`
**Location**: `services/intent_service/canonical_handlers.py:107`
**Status**: Operational

**Actions**:
- `get_identity`
- `get_capabilities`

---

### GUIDANCE → ✅ canonical_handlers.py
**Handler**: `CanonicalHandlers._handle_guidance_query()`
**Location**: `services/intent_service/canonical_handlers.py:187`
**Status**: Operational

**Actions**:
- `get_guidance`
- `get_recommendations`

---

### QUERY (general) → ✅ QueryRouter (OrchestrationEngine)
**Handler**: `OrchestrationEngine.handle_query_intent()`
**Location**: `services/orchestration/engine.py:117`
**Status**: Operational (GREAT-1B)

**Actions**:
- `search_documents` → QueryRouter.file_queries
- `search_projects` → QueryRouter.project_queries
- `list_files` → QueryRouter.file_queries

**Evidence**: Test showed "search for architecture docs" → `query/search_documents`

**Routing**:
```python
# services/orchestration/engine.py:117
async def handle_query_intent(intent: Intent):
    if intent.action in ["search_projects", "list_projects", "find_projects"]:
        return await query_router.project_queries.list_active_projects()

    elif intent.action in ["search_files", "find_files", "list_files"]:
        return await query_router.file_queries.list_recent_files()

    # etc.
```

---

### EXECUTION → ⚠️ Placeholder (Phase 3C)
**Handler**: `IntentService._handle_generic_intent()`
**Location**: `services/intent/intent_service.py:338`
**Status**: **Placeholder message only**

**Actions**:
- `create_issue` (Test confirmed: EXECUTION/create_issue)
- `update_issue_status` (Test confirmed: EXECUTION/update_issue_status)
- etc.

**Current Behavior**:
```python
# services/intent/intent_service.py:338
async def _handle_generic_intent(intent: Intent):
    return IntentProcessingResult(
        success=True,
        message=f"Intent '{intent.action}' (category: {intent.category.value}) requires full orchestration workflow. This is being restored in Phase 3.",
        # ...
    )
```

**Status**: Returns placeholder message saying "requires full orchestration workflow"

---

### ANALYSIS → ⚠️ Placeholder (Phase 3C)
**Handler**: `IntentService._handle_generic_intent()`
**Location**: `services/intent/intent_service.py:338`
**Status**: **Placeholder message only**

**Actions**:
- `analyze_codebase` (Test confirmed: ANALYSIS/analyze_codebase)
- etc.

**Current Behavior**: Same placeholder as EXECUTION

---

### CONVERSATION → ✅ ConversationHandler
**Handler**: `ConversationHandler.respond()`
**Location**: `services/conversation/conversation_handler.py`
**Status**: Operational (Tier 1 bypass - Phase 3D)

**Actions**:
- `greeting`
- `farewell`
- `thanks`

---

## Key Findings

### Finding 1: Canonical Handlers are ONLY for Standup Queries

**Evidence from canonical_handlers.py docstring**:
```python
class CanonicalHandlers:
    """Handlers for canonical standup queries using PIPER.md context"""
```

**Purpose**: Handle the 5 canonical query categories (TEMPORAL, STATUS, PRIORITY, IDENTITY, GUIDANCE) that provide standup-style information from PIPER.md.

**Scope**: Does NOT handle EXECUTION/ANALYSIS/general QUERY intents.

---

### Finding 2: Different Intent Categories → Different Handler Systems

| Category | Handler System | Location |
|----------|---------------|----------|
| TEMPORAL | CanonicalHandlers | canonical_handlers.py |
| STATUS | CanonicalHandlers | canonical_handlers.py |
| PRIORITY | CanonicalHandlers | canonical_handlers.py |
| IDENTITY | CanonicalHandlers | canonical_handlers.py |
| GUIDANCE | CanonicalHandlers | canonical_handlers.py |
| QUERY (general) | QueryRouter | orchestration/engine.py |
| CONVERSATION | ConversationHandler | conversation/conversation_handler.py |
| EXECUTION | **Placeholder** | intent/intent_service.py |
| ANALYSIS | **Placeholder** | intent/intent_service.py |

---

### Finding 3: EXECUTION/ANALYSIS are Placeholders

**From IntentService**:
```python
# Phase 3C: For EXECUTION/ANALYSIS intents, indicate orchestration needed
return await self._handle_generic_intent(intent)
```

**Message returned**:
```
"Intent 'create_issue' (category: execution) requires full orchestration
workflow. This is being restored in Phase 3."
```

**Status**: Not a bug - intentional placeholder for Phase 3C restoration work.

---

### Finding 4: The "219 Handlers" Misunderstanding

**Gameplan Assumption**: "219 handlers exist"

**Reality**:
- 5 canonical handlers in canonical_handlers.py ✅
- QueryRouter handles QUERY intents ✅
- ConversationHandler handles CONVERSATION ✅
- EXECUTION/ANALYSIS are placeholders (Phase 3C) ⚠️

**Where "219" came from**: Likely confused with:
- 219 Slack handler references (grep count)
- Or 219 intent patterns (not handlers)

---

## Recommendations for GREAT-4C

### Recommendation 1: Clarify Scope

**GREAT-4C should focus on**:
- ✅ Canonical handlers (TEMPORAL, STATUS, PRIORITY, IDENTITY, GUIDANCE)
- ✅ Enhancing existing 5 handlers
- ❌ NOT creating EXECUTION/ANALYSIS handlers (that's Phase 3C)

### Recommendation 2: Enhancement Areas

**Potential enhancements for canonical_handlers.py**:

1. **Integration with Spatial Intelligence**
   - TEMPORAL queries could check Calendar spatial context
   - STATUS queries could check Slack/Notion spatial context
   - PRIORITY queries could use spatial ranking

2. **Better PIPER.md Parsing**
   - More sophisticated section extraction
   - Handle nested sections
   - Parse TODO lists

3. **Confidence Scoring**
   - Add confidence scores to handler responses
   - Return multiple options when ambiguous

4. **Caching Integration**
   - Cache PIPER.md reads (currently reads every time)
   - Cache parsed results

5. **Error Handling**
   - Graceful degradation when PIPER.md unavailable
   - Better error messages

### Recommendation 3: Don't Build What Exists

**DO NOT**:
- Create 219 new handlers
- Build EXECUTION/ANALYSIS handlers (Phase 3C owns this)
- Duplicate QueryRouter functionality

**DO**:
- Enhance existing 5 canonical handlers
- Improve integration with spatial intelligence
- Add missing query patterns to pre_classifier

---

## Architecture Diagram

```
User Message
     ↓
IntentClassifier.classify()
     ↓
Intent { category, action, confidence }
     ↓
IntentService.process_intent()
     ↓
     ├─ CONVERSATION → ConversationHandler
     ├─ TEMPORAL → CanonicalHandlers._handle_temporal_query()
     ├─ STATUS → CanonicalHandlers._handle_status_query()
     ├─ PRIORITY → CanonicalHandlers._handle_priority_query()
     ├─ IDENTITY → CanonicalHandlers._handle_identity_query()
     ├─ GUIDANCE → CanonicalHandlers._handle_guidance_query()
     ├─ QUERY → OrchestrationEngine.handle_query_intent() → QueryRouter
     ├─ EXECUTION → Placeholder (Phase 3C)
     └─ ANALYSIS → Placeholder (Phase 3C)
```

---

## Test Evidence

**Test Script**: `dev/2025/10/05/test_unhandled_intent.py`

**Execution Time**: 10 seconds (6 queries with LLM fallback)

**Results**:
- ✅ TEMPORAL/STATUS/PRIORITY classified correctly (pre-classifier)
- ✅ EXECUTION/QUERY/ANALYSIS classified correctly (LLM)
- ✅ All queries classified successfully
- ⚠️ EXECUTION/ANALYSIS return placeholder messages

**Confidence Scores**:
- Pre-classifier patterns: 1.0 (perfect)
- LLM classifications: 0.85-0.95 (excellent)

---

## Conclusion

**GREAT-4C Gameplan Revision Needed**:

1. ❌ "219 handlers exist" - FALSE (only 5 canonical handlers)
2. ✅ Canonical handlers are for STANDUP queries only
3. ✅ Other intent categories route to different systems
4. ⚠️ EXECUTION/ANALYSIS are placeholders (not gaps - intentional)

**Recommended GREAT-4C Focus**:
- Enhance the 5 existing canonical handlers
- Integrate with spatial intelligence
- Improve PIPER.md parsing
- Add caching for performance
- Better error handling

**What NOT to do**:
- Don't create 214 new handlers
- Don't build EXECUTION/ANALYSIS handlers (Phase 3C)
- Don't duplicate QueryRouter

---

**Next Step**: Report findings to Lead Developer for Chief Architect consultation and gameplan revision.

---

*Investigation completed: October 5, 2025, 8:20 PM*
*Duration: 15 minutes*
*Test evidence: dev/2025/10/05/test_unhandled_intent.py (7 test cases)*
