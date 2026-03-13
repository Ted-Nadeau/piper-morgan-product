# Medium Priority Bypass Analysis

**Epic**: GREAT-4B - Intent Classification Universal Enforcement
**Phase**: Phase 1 - Medium Priority Analysis
**Date**: October 5, 2025
**Analyst**: Cursor Agent

---

## CLI Command: personality

**File**: `cli/commands/personality.py`
**Current State**: Direct service call
**Reason for Medium Priority**: Personality commands are user-facing but may have structured inputs

**Conversion Complexity**: Medium
**Estimated Effort**: 30 minutes
**Dependencies**: None
**Slack Pattern Applicability**: Yes

**Conversion Approach**:

1. Wrap command execution with intent classification
2. Map personality operations to intent categories (likely EXECUTION)
3. Route through canonical handlers or direct intent processing
4. Maintain existing CLI argument structure

**Test Strategy**:

- [ ] Verify personality commands classify correctly
- [ ] Test argument parsing still works
- [ ] Validate output format unchanged

---

## CLI Command: publish

**File**: `cli/commands/publish.py`
**Current State**: Direct service call
**Reason for Medium Priority**: Publishing commands are user-facing but may be simple operations

**Conversion Complexity**: Small
**Estimated Effort**: 15 minutes
**Dependencies**: None
**Slack Pattern Applicability**: Yes

**Conversion Approach**:

1. Add intent classification wrapper
2. Classify publish operations as EXECUTION intents
3. Route to appropriate handlers
4. Preserve existing publish workflow

**Test Strategy**:

- [ ] Test publish commands classify as EXECUTION
- [ ] Verify publishing workflow intact
- [ ] Check error handling preserved

---

## CLI Command: test_issues_integration

**File**: `cli/commands/test_issues_integration.py`
**Current State**: Direct service call
**Reason for Medium Priority**: Test command - may be excluded from enforcement

**Conversion Complexity**: Small (or Skip)
**Estimated Effort**: 15 minutes (or 0 if excluded)
**Dependencies**: None
**Slack Pattern Applicability**: Questionable (test command)

**Conversion Approach**:

1. **Option A**: Convert like other CLI commands
2. **Option B**: Add to bypass exemption list (recommended)
3. If converting: Classify test operations as EXECUTION

**Test Strategy**:

- [ ] Decide: Convert or exempt?
- [ ] If converting: Test classification works
- [ ] If exempting: Update scanner exemption list

---

## Web Route: GET /standup

**File**: `web/app.py`
**Current State**: Direct HTML serving
**Reason for Medium Priority**: UI page that may process query parameters

**Conversion Complexity**: Small
**Estimated Effort**: 15 minutes
**Dependencies**: None
**Slack Pattern Applicability**: No (HTML serving)

**Conversion Approach**:

1. Check if route processes any user input (query params)
2. If yes: Classify query parameters through intent
3. If no: Consider exempting as static content
4. Likely needs intent classification for any dynamic content

**Test Strategy**:

- [ ] Identify if route processes user input
- [ ] Test query parameter classification
- [ ] Verify HTML serving unchanged

---

## Web Route: GET /api/personality/profile/{user_id}

**File**: `web/app.py`
**Current State**: Direct API call
**Reason for Medium Priority**: CRUD operation, may not have free text input

**Conversion Complexity**: Small
**Estimated Effort**: 15 minutes
**Dependencies**: None
**Slack Pattern Applicability**: Partial (API pattern)

**Conversion Approach**:

1. Classify profile retrieval as QUERY intent
2. Route through intent system to personality service
3. Maintain existing API response format
4. Handle user_id parameter validation

**Test Strategy**:

- [ ] Test profile retrieval classifies as QUERY
- [ ] Verify API response format unchanged
- [ ] Check user_id validation preserved

---

## Web Route: PUT /api/personality/profile/{user_id}

**File**: `web/app.py`
**Current State**: Direct API call
**Reason for Medium Priority**: CRUD operation with potential free text in request body

**Conversion Complexity**: Medium
**Estimated Effort**: 30 minutes
**Dependencies**: None
**Slack Pattern Applicability**: Yes (API with body content)

**Conversion Approach**:

1. Classify profile updates as EXECUTION intent
2. Parse request body for intent classification
3. Route through intent system to personality service
4. Handle validation and error responses

**Test Strategy**:

- [ ] Test profile updates classify as EXECUTION
- [ ] Verify request body parsing works
- [ ] Check validation and error handling preserved

---

## Summary

**Total medium priority items**: 6

- **CLI commands**: 3 (personality, publish, test_issues_integration)
- **Web routes**: 3 (GET /standup, GET/PUT /api/personality/profile/{user_id})

**Total estimated effort**: 2.25 hours

- Small tasks (4): 1 hour (15 min each)
- Medium tasks (2): 1 hour (30 min each)
- Optional (1): 15 min or exempt

**Recommended approach**: Sequential (dependencies are minimal)

**Dependencies**: None identified - all items can be converted independently

---

## Conversion Priority Order

1. **publish.py** - Effort: Small (15 min), No dependencies, Clear EXECUTION pattern
2. **GET /standup** - Effort: Small (15 min), No dependencies, Simple HTML route
3. **GET /api/personality/profile/{user_id}** - Effort: Small (15 min), No dependencies, Simple QUERY
4. **personality.py** - Effort: Medium (30 min), No dependencies, Multiple operations
5. **PUT /api/personality/profile/{user_id}** - Effort: Medium (30 min), No dependencies, Complex body parsing
6. **test_issues_integration.py** - Effort: Small (15 min) OR Exempt, Test command consideration

**Recommended Phase 2 sequence**: 1 → 2 → 3 → 4 → 5 → (6 - decide exempt vs convert)

---

## Slack Pattern Applicability

### Pattern Analysis

Slack integration shows the gold standard with 375 intent references across 219 handlers. Key patterns:

**Intent Classification Wrapper**:

```python
# Slack pattern: Wrap all user input with intent classification
async def handle_message(message):
    intent = await classifier.classify(message.text)
    return await route_intent(intent)
```

**Applicable to**:

- ✅ **CLI commands**: All user commands should classify intent
- ✅ **API routes with body content**: Parse and classify request content
- ❌ **Static HTML routes**: No user input to classify
- ⚠️ **CRUD operations**: May need intent for operation type

**Canonical Handler Routing**:

```python
# Route classified intents to appropriate handlers
if intent.category == IntentCategory.EXECUTION:
    return await execution_handler.handle(intent)
```

**Applicable to**:

- ✅ **All conversions**: Route through canonical handlers
- ✅ **Maintain existing logic**: Handlers call existing services

**Direct Intent Endpoint Redirect**:

```python
# For API routes: Redirect to /api/v1/intent endpoint
return await intent_endpoint.process(request_data)
```

**Applicable to**:

- ✅ **Web API routes**: Can redirect to intent endpoint
- ❌ **CLI commands**: Direct classification more appropriate

---

## Phase 2 Conversion Recommendation

### Approach

**Sequential** - Items have minimal dependencies and can be converted one by one for easier testing and validation.

### Grouping Strategy

- **Group 1**: Quick wins (1 hour total)

  - `publish.py` (15 min)
  - `GET /standup` (15 min)
  - `GET /api/personality/profile/{user_id}` (15 min)
  - `test_issues_integration.py` - **RECOMMEND EXEMPT** (0 min)

- **Group 2**: Standard conversions (1 hour total)
  - `personality.py` (30 min)
  - `PUT /api/personality/profile/{user_id}` (30 min)

**Total Phase 2 estimate**: 2 hours (excluding test command exemption)

### Risk Factors

- **API Response Format Changes**: Ensure intent routing preserves existing API contracts
  - _Mitigation_: Test API responses match exactly before/after conversion
- **CLI Argument Parsing**: Intent classification might interfere with argument parsing
  - _Mitigation_: Classify the full command + args, not individual arguments
- **Performance Impact**: Adding intent classification to every request
  - _Mitigation_: Use fast pre-classifier patterns where possible

### Success Metrics

- All 5 medium priority bypasses converted (excluding test command)
- Bypass count reduced from 20 to 15 (or 14 if test exempt)
- All bypass detection tests pass for converted items
- No regression in existing functionality
- API contracts preserved
- CLI commands maintain existing behavior

---

**Status**: ✅ Medium priority analysis complete - Ready for Phase 2 implementation
