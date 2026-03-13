# Code Agent: Issues #284 + #285 - Mandatory Self-Validation

## Critical Context: You Made the Same Mistake as Cursor

**Your Claims**:
- ✅ Issue #284: ActionMapper complete (66 mappings)
- ✅ Issue #285: Todo system complete (16 endpoints + chat handlers)
- ✅ "All tests passing"
- ✅ "Both issues complete"

**Your Evidence**: Zero curl tests, zero manual validation, zero end-to-end proof

**This is the 80% pattern**: Unit tests pass ≠ Feature works for users

**What Cursor discovered**: Claimed "5/5 error types ✅" but HTTPException bypassed middleware. Only 67% actually working.

**You likely have the same problem**: Code works in isolation but routing/integration untested.

---

## Mission: Self-Audit + Validate to 100%

**You will**:
1. Create "Claimed vs Reality" matrices showing what you didn't verify
2. Run representative sample tests proving routing works end-to-end
3. Document EVERY curl/CLI output (not claims)
4. Fix any gaps discovered
5. Update matrices showing verified completion

**There is no other work until this is done** - PM cannot close issues without evidence.

---

## Matrix Standard: Multi-Column Breakdown (#290 Pattern)

Your matrices must follow the proven #290 pattern:

**Multi-Column Component Breakdown**:
- Separate columns for each layer (mapper vs handler vs route vs test)
- Explicit PASSING/FAILING/UNTESTED status
- Evidence column with actual file names or outputs
- TOTAL line showing N/M = X%

**Evolution Tracking**:
- CLAIMED: What you said was complete
- SAMPLED: What you actually tested
- VERIFIED: What's proven to work
- Makes gap between claims and reality visible

---

## Part 1: Issue #284 ActionMapper Validation

### Step 1: Create "CLAIMED" State Matrix (15 minutes)

**Document what you claimed without testing**:

```markdown
## Issue #284 ActionMapper - CLAIMED STATE (Before Validation)

| Category | Classifier Output | Mapped To | Handler Exists | Route Tested | Works End-to-End | Evidence |
|----------|------------------|-----------|---------------|--------------|------------------|----------|
| GitHub | create_github_issue | create_issue | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |
| GitHub | list_github_issues | list_issues | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |
| GitHub | update_github_issue | update_issue | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |
| Calendar | create_calendar_event | create_event | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |
| Calendar | list_calendar_events | list_events | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |
| Notion | create_notion_page | create_page | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |
| Notion | search_notion | search | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |
| Knowledge | query_knowledge | query | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |
| ... | (58 more mappings) | ... | ✅ YES | ❓ UNTESTED | ❓ UNKNOWN | None - claimed only |

**TOTAL CLAIMED: 66/66 mappings exist**
**TOTAL VERIFIED: 0/66 = 0% (no manual validation performed)**

**The Gap**: Mappings exist in code, but routing from user input → handler → response UNTESTED
```

**Commit this matrix** to your session log.

### Step 2: Define Representative Sample (15 minutes)

**You cannot test all 66 mappings** - define a representative sample:

```markdown
## Issue #284 - Sampling Strategy

**Sample Size**: 12 mappings (18% of 66)
**Selection Criteria**: At least 2 from each major category

### Selected Sample Mappings

| # | Category | Classifier Output | Why This One |
|---|----------|------------------|--------------|
| 1 | GitHub | create_github_issue | Most common operation |
| 2 | GitHub | list_github_issues | Second most common |
| 3 | Calendar | create_calendar_event | Core calendar operation |
| 4 | Calendar | list_calendar_events | Read operation test |
| 5 | Notion | create_notion_page | Write operation test |
| 6 | Notion | search_notion | Search operation test |
| 7 | Knowledge | query_knowledge | Complex query operation |
| 8 | Knowledge | summarize_knowledge | Processing operation |
| 9 | Task | create_task | Task management core |
| 10 | Task | list_tasks | Task retrieval |
| 11 | Error | unknown_intent | Error handling test |
| 12 | Help | get_help | System operation test |

**Coverage**: GitHub (2), Calendar (2), Notion (2), Knowledge (2), Task (2), System (2)
**Rationale**: Covers all major categories, tests both read/write operations
**Confidence**: If 12/12 work, high confidence in remaining 54
```

### Step 3: Manual Testing Protocol - Run Tests (1 hour)

**For EACH of the 12 sample mappings, run this protocol**:

#### Setup

```bash
# Start server
python main.py

# Get auth token
TOKEN=$(curl -s -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"xian","password":"test123456"}' \
  | jq -r '.token')
```

#### Test Template (Run for Each Mapping)

```bash
# Test: create_github_issue
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "create a github issue to test mapping"}' | jq .

# Save output to: test-284-create-github-issue.txt
# Check:
# 1. Does it route to correct handler?
# 2. Does handler execute?
# 3. Does user get meaningful response (not "No handler for action")?
# 4. Are there any errors in server logs?

# Expected: Success OR clear error (not routing failure)
# NOT Expected: "No handler for action: create_github_issue"
```

**Repeat for all 12 sample mappings**

**Document EVERY output** - save to files like:
- test-284-01-create-github-issue.txt
- test-284-02-list-github-issues.txt
- test-284-03-create-calendar-event.txt
- ... (12 total)

### Step 4: Create "VERIFIED" State Matrix (30 minutes)

**After running tests, document what actually works**:

```markdown
## Issue #284 ActionMapper - VERIFIED STATE (After Testing)

| # | Category | Classifier Output | Mapped To | Handler Exists | Route Tested | Works End-to-End | Test Status | Evidence |
|---|----------|------------------|-----------|---------------|--------------|------------------|-------------|----------|
| 1 | GitHub | create_github_issue | create_issue | ✅ YES | ✅ TESTED | ✅ WORKS | ✅ PASSING | test-284-01.txt |
| 2 | GitHub | list_github_issues | list_issues | ✅ YES | ✅ TESTED | ✅ WORKS | ✅ PASSING | test-284-02.txt |
| 3 | Calendar | create_calendar_event | create_event | ✅ YES | ✅ TESTED | ❌ FAILS | ❌ FAILING | "Handler not found" error |
| ... | (9 more tested) | ... | ... | ... | ... | ... | ... | ... |
| - | (54 untested) | ... | ✅ YES | ❓ UNTESTED | ❓ ASSUMED | ❓ UNKNOWN | Extrapolated from sample |

**SAMPLE TESTED: 12/12 mappings tested**
**SAMPLE PASSING: X/12 working (Y% pass rate)**
**ISSUES FOUND: Z mappings failed (document which ones and why)**
**TOTAL VERIFIED: X/66 = Z% (based on sample results)**
```

### Step 5: Fix Any Issues Found (30 minutes - 2 hours)

**If tests reveal problems**:
1. Document what failed and why
2. Fix the mapping/handler/route issues
3. Re-test the failed cases
4. Update matrix showing fixes

**Common issues to look for**:
- Mapping exists but handler method name wrong
- Handler exists but not wired into IntentService
- Route exists but authentication fails
- Integration with external service not configured

### Step 6: Update GitHub Issue #284 (15 minutes)

```bash
gh issue edit 284 --body "
## Issue #284 ActionMapper - VALIDATION COMPLETE

### Claimed State
- 66 mappings created
- Integrated into IntentService
- All tests passing (unit tests only)

### Validation Performed
- Representative sample: 12/66 mappings (18%)
- Coverage: All major categories (GitHub, Calendar, Notion, Knowledge, Task, System)
- Method: Manual curl tests for each mapping

### Results
- Sample tested: 12/12
- Sample passing: X/12 (Y%)
- Issues found: Z (list them)
- Issues fixed: Z (document fixes)
- Confidence: High (diverse sample across all categories)

### Evidence
[Link to test outputs]
[Link to matrices in session log]

**VERIFIED: X/12 sample = Y% working**
**EXTRAPOLATED: ~Y% of 66 total mappings expected to work**
"

gh issue comment 284 --body "
## Manual Validation Complete

### CLAIMED Matrix (Before)
- 66/66 mappings exist
- 0/66 manually tested
- Gap between code and reality unknown

### VERIFIED Matrix (After)
- 12/12 sample tested
- X/12 working (Y%)
- Z issues found and fixed

### All Test Outputs
[Paste outputs from 12 tests]

**Representative sample proves ActionMapper working at Y% confidence level**
"
```

---

## Part 2: Issue #285 Todo System Validation

### Step 1: Create "CLAIMED" State Matrix (15 minutes)

```markdown
## Issue #285 Todo System - CLAIMED STATE (Before Validation)

| Operation | API Endpoint | Handler Exists | Wired to IntentService | Chat Works | API Works | Test Status | Evidence |
|-----------|-------------|----------------|----------------------|-----------|-----------|-------------|----------|
| Create todo | POST /api/v1/todos | ✅ YES | ✅ YES | ❓ UNTESTED | ❓ UNTESTED | ❓ | None - claimed only |
| List todos | GET /api/v1/todos | ✅ YES | ✅ YES | ❓ UNTESTED | ❓ UNTESTED | ❓ | None - claimed only |
| Get todo | GET /api/v1/todos/{id} | ✅ YES | ✅ YES | ❓ UNTESTED | ❓ UNTESTED | ❓ | None - claimed only |
| Update todo | PATCH /api/v1/todos/{id} | ✅ YES | ✅ YES | ❓ UNTESTED | ❓ UNTESTED | ❓ | None - claimed only |
| Delete todo | DELETE /api/v1/todos/{id} | ✅ YES | ✅ YES | ❓ UNTESTED | ❓ UNTESTED | ❓ | None - claimed only |
| Mark complete | PATCH /api/v1/todos/{id} | ✅ YES | ✅ YES | ❓ UNTESTED | ❓ UNTESTED | ❓ | None - claimed only |
| Create list | POST /api/v1/todos/lists | ✅ YES | ✅ YES | ❓ UNTESTED | ❓ UNTESTED | ❓ | None - claimed only |
| List lists | GET /api/v1/todos/lists | ✅ YES | ✅ YES | ❓ UNTESTED | ❓ UNTESTED | ❓ | None - claimed only |

**TOTAL CLAIMED: 16/16 endpoints exist + 14 mappings + chat handlers**
**TOTAL VERIFIED: 0/16 = 0% (no manual validation performed)**

**The Gap**: API exists, handlers exist, but NEITHER chat NOR API tested end-to-end
```

### Step 2: Manual Testing Protocol - API Tests (30 minutes)

**Test core CRUD operations via API**:

#### Setup

```bash
# Start server
python main.py

# Get auth token
TOKEN=$(curl -s -X POST http://localhost:8001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"xian","password":"test123456"}' \
  | jq -r '.token')
```

#### Test 1: Create Todo

```bash
curl -X POST http://localhost:8001/api/v1/todos \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test validation todo",
    "description": "Testing Issue #285",
    "status": "todo"
  }' | jq .

# Save output to: test-285-api-create.txt
# Expected: 201 Created with todo object (with id)
# Extract todo_id for next tests
```

#### Test 2: List Todos

```bash
curl -X GET http://localhost:8001/api/v1/todos \
  -H "Authorization: Bearer $TOKEN" | jq .

# Save output to: test-285-api-list.txt
# Expected: 200 OK with array of todos (including the one just created)
```

#### Test 3: Update Todo

```bash
curl -X PATCH http://localhost:8001/api/v1/todos/{todo_id} \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}' | jq .

# Save output to: test-285-api-update.txt
# Expected: 200 OK with updated todo
```

#### Test 4: Mark Complete

```bash
curl -X PATCH http://localhost:8001/api/v1/todos/{todo_id} \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}' | jq .

# Save output to: test-285-api-complete.txt
# Expected: 200 OK with completed todo
```

#### Test 5: Delete Todo

```bash
curl -X DELETE http://localhost:8001/api/v1/todos/{todo_id} \
  -H "Authorization: Bearer $TOKEN" | jq .

# Save output to: test-285-api-delete.txt
# Expected: 204 No Content or 200 OK
```

### Step 3: Manual Testing Protocol - Chat Tests (30 minutes)

**Test natural language todo operations**:

#### Test 6: Create via Chat

```bash
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "add todo: Review PR #284"}' | jq .

# Save output to: test-285-chat-create.txt
# Expected: Friendly response confirming todo created
# NOT Expected: "No handler for action" or routing error
```

#### Test 7: List via Chat

```bash
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "show my todos"}' | jq .

# Save output to: test-285-chat-list.txt
# Expected: Friendly response listing todos
```

#### Test 8: Complete via Chat

```bash
curl -X POST http://localhost:8001/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "mark todo 1 as complete"}' | jq .

# Save output to: test-285-chat-complete.txt
# Expected: Friendly confirmation of completion
```

### Step 4: Create "VERIFIED" State Matrix (20 minutes)

```markdown
## Issue #285 Todo System - VERIFIED STATE (After Testing)

| Operation | API Endpoint | Handler Exists | Wired | Chat Works | API Works | Test Status | Evidence |
|-----------|-------------|----------------|-------|-----------|-----------|-------------|----------|
| Create todo | POST /api/v1/todos | ✅ YES | ✅ YES | ✅ WORKS | ✅ WORKS | ✅ PASSING | test-285-chat-create.txt, test-285-api-create.txt |
| List todos | GET /api/v1/todos | ✅ YES | ✅ YES | ✅ WORKS | ✅ WORKS | ✅ PASSING | test-285-chat-list.txt, test-285-api-list.txt |
| Get todo | GET /api/v1/todos/{id} | ✅ YES | ✅ YES | ❓ | ✅ WORKS | ✅ PASSING | (included in list test) |
| Update todo | PATCH /api/v1/todos/{id} | ✅ YES | ✅ YES | ❓ | ✅ WORKS | ✅ PASSING | test-285-api-update.txt |
| Delete todo | DELETE /api/v1/todos/{id} | ✅ YES | ✅ YES | ❓ | ✅ WORKS | ✅ PASSING | test-285-api-delete.txt |
| Mark complete | PATCH /api/v1/todos/{id} | ✅ YES | ✅ YES | ✅ WORKS | ✅ WORKS | ✅ PASSING | test-285-chat-complete.txt |
| ... | (10 more operations) | ... | ... | ... | ... | ... | ... |

**CORE TESTED: 8/16 operations tested (50%)**
**CORE PASSING: X/8 working (Y%)**
**ISSUES FOUND: Z (document)**
**CONFIDENCE: High for core CRUD, untested operations assumed working**
```

### Step 5: Fix Any Issues (30 minutes - 1 hour)

**If tests fail**:
1. Document failure mode
2. Fix handler/mapping/integration
3. Re-test
4. Update matrix

### Step 6: Update GitHub Issue #285 (15 minutes)

```bash
gh issue edit 285 --body "
## Issue #285 Todo System - VALIDATION COMPLETE

### Claimed State
- 16 API endpoints mounted
- Chat handlers created (162 lines)
- 14 todo action mappings
- All tests passing (unit tests only)

### Validation Performed
- API tests: 5/5 core CRUD operations
- Chat tests: 3/3 core natural language operations
- Total: 8/16 operations tested (core operations)

### Results
- API CRUD: X/5 working (Y%)
- Chat operations: X/3 working (Y%)
- Issues found: Z (list them)
- Issues fixed: Z (document fixes)

### Evidence
[Link to 8 test outputs]
[Link to matrices]

**VERIFIED: Core CRUD operations working via both API and chat**
"

gh issue comment 285 --body "
## Manual Validation Complete

### CLAIMED Matrix
- 16 endpoints + chat handlers
- 0/16 manually tested
- Gap unknown

### VERIFIED Matrix
- 8/16 tested (core operations)
- X/8 working (Y%)
- Z issues found and fixed

### Test Outputs
[Paste all 8 test results]

**Core todo functionality verified working via both API and natural language**
"
```

---

## Evolution Summary: Claimed → Verified

Create this summary showing the validation journey:

```markdown
## Issues #284 + #285 - Validation Journey

### Starting Point (Your Claims)
- #284: 66/66 mappings complete
- #285: 16/16 endpoints + chat complete
- Evidence: Unit tests passing
- **Gap: 0% manual validation**

### Validation Performed
- #284: 12/66 mappings tested (18% representative sample)
- #285: 8/16 operations tested (50% core operations)
- Method: Manual curl/chat tests
- **Evidence: X test output files**

### Results Discovered
- #284: X/12 sample working (Y% pass rate)
- #285: X/8 core working (Y% pass rate)
- Issues found: Z total
- Issues fixed: Z total

### Final State
- #284: Y% verified working (high confidence via sampling)
- #285: Core CRUD verified working (API + chat)
- Evidence: Complete test outputs + matrices
- **Gap closed: Manual validation complete**

### Lesson Learned
**"Tests pass" ≠ "Feature works"**

Unit tests passing proved code compiles and isolated logic works.
Manual curl tests proved routing, integration, and user experience work.

Both are required. We had the first, not the second.
```

---

## Acceptance Criteria - ALL REQUIRED

**Issue #284**:
- [ ] CLAIMED state matrix created (66/66 claimed, 0/66 verified)
- [ ] Sampling strategy documented (12 mappings, rationale provided)
- [ ] 12/12 sample mappings tested with curl
- [ ] All 12 curl outputs saved and documented
- [ ] VERIFIED state matrix created (X/12 working)
- [ ] Any issues found documented and fixed
- [ ] GitHub issue #284 updated with validation evidence
- [ ] Session log updated with complete validation

**Issue #285**:
- [ ] CLAIMED state matrix created (16/16 claimed, 0/16 verified)
- [ ] 5 API operations tested (Create, List, Get, Update, Delete)
- [ ] 3 Chat operations tested (create, list, complete via natural language)
- [ ] All 8 test outputs saved and documented
- [ ] VERIFIED state matrix created (X/8 working)
- [ ] Any issues found documented and fixed
- [ ] GitHub issue #285 updated with validation evidence
- [ ] Session log updated with complete validation

**Cross-Issue**:
- [ ] Evolution summary created (Claimed → Verified)
- [ ] Lesson learned documented
- [ ] Total time spent on validation tracked

**DO NOT CLAIM VALIDATION COMPLETE WITHOUT ALL 17 CHECKBOXES**

---

## Critical Reminders

**You made the same mistake as Cursor**:
- Cursor: Claimed 5/5 error types, only 67% actually worked
- You: Claimed 66 mappings + 16 endpoints, 0% manually verified
- Both: "Tests pass" was insufficient evidence

**Complete means VERIFIED**:
- Not "code exists"
- Not "unit tests pass"
- Manual end-to-end tests proving routing works
- Multi-column matrices showing what's actually tested

**Evidence means ACTUAL OUTPUTS**:
- Curl commands and their actual JSON responses
- Not "it should work"
- Not "I implemented it"
- Saved test output files

**Sampling is acceptable**:
- Cannot test all 66 mappings (too many)
- 12-mapping sample is sufficient IF:
  - Diverse across categories
  - Tests both read and write
  - Representative of whole system
- Document sampling rationale

**No bounty in skipping**:
- PM cannot close issues without this validation
- This is the work that proves your claims
- Do it right now, not later

---

## Session Log Format

Continue your existing log: `dev/2025/11/03/2025-11-03-0615-prog-code-log.md`

Add self-validation section with:
- CLAIMED state matrices (both issues)
- Sampling strategy (#284)
- All test outputs (20 total: 12 for #284, 8 for #285)
- VERIFIED state matrices (both issues)
- Issues found and fixes applied
- Evolution summary
- GitHub updates

---

## You Said Earlier Today

> "Session Complete! 🎉 Both Issues Delivered"

**But they weren't delivered** - they were claimed without verification.

**This self-validation is your delivery**:
1. Admit what wasn't tested (CLAIMED matrices)
2. Define testing strategy (sampling)
3. Run the actual tests (curl outputs)
4. Document what works (VERIFIED matrices)
5. Fix what's broken
6. Prove completion with evidence

**Then and only then: "Issues #284 + #285 VALIDATED & COMPLETE"**

---

**Start with Part 1, Step 1: Create CLAIMED matrix for #284 showing 66/66 exist but 0/66 verified. Report back with matrix in session log.**
