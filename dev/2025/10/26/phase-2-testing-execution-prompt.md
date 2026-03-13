# Phase 2 End-to-End Testing - Execution Prompt

**Date**: Sunday, October 26, 2025, 1:38 PM PT
**Sprint**: A8 Phase 2 (E2E System Testing)
**Duration**: 4-6 hours estimated
**Philosophy**: Discovery testing - document reality, not validate assumptions
**Confidence**: HIGH - All components verified ready by Code's archaeological investigation

---

## MISSION

Execute comprehensive end-to-end testing of Piper Morgan Alpha to:
1. **Validate** [MUST WORK] features (alpha blockers)
2. **Discover** [IF EXISTS] feature behavior (document reality)
3. **Document** bugs and surprises (P0/P1 blockers vs minor issues)
4. **Verify** Code's archaeological predictions match reality

**Key Principle**: "Try each feature optimistically, document what happens, compare to expectations. This is a unified system - components should work together."

---

## CRITICAL CONTEXT

### What Code's Investigation Found

**Quote**: "This isn't a 75% complete codebase with scattered features. It's a unified system where components know about each other, learning flows from user behavior → patterns → preferences, preferences affect intent classification, classification uses graph reasoning, and everything is tested and working together."

**Numbers**:
- ✅ 4/4 CLI commands working
- ✅ 4/4 integrations fully implemented (GitHub, Slack, Calendar, Notion)
- ✅ 4/4 Sprint A8 Phase 1 features complete
- ✅ 3/3 learning components wired (52/52 tests passing)
- ✅ 79 integration test files, 447+ fixtures
- ✅ 1,625+ lines of Sprint A8 test code

**Expectation**: Minimal surprises, system should work as designed.

---

## ESSENTIAL MATERIALS

### Required Documents
1. **[Revised Phase 2 Gameplan](sprint-a8-phase-2-gameplan-e2e-testing-REVISED.md)** - Complete test plan with all details
2. **[Quick Reference Card](phase2-testing-quick-reference.md)** - Commands and locations
3. **[Code's Executive Briefing](PHASE-2-EXECUTIVE-BRIEFING.md)** - Summary of findings

### Testing Setup
- **System**: localhost:8001 (web interface)
- **Database**: PostgreSQL on localhost:5433
- **Entry**: `python main.py` starts web server
- **CLI**: `python main.py setup|status|preferences|migrate-user`

### Environment Variables Required (for integration testing)
```bash
export GITHUB_TOKEN=<your_token>
export SLACK_BOT_TOKEN=<your_token>
export GOOGLE_APPLICATION_CREDENTIALS=<path>
export NOTION_API_KEY=<your_key>
```

---

## TESTING APPROACH

### Human + Assistant Collaboration

**Human Role**:
- Web UI interaction (required - no Chrome MCP currently working)
- Visual verification (screenshots, UI behavior)
- Real-time observations (confusion points, timing)
- Decision-making (go/no-go, bug severity)

**Assistant Role**:
- Command execution (CLI, database queries)
- Log analysis (terminal output, error messages)
- Documentation (evidence collection, bug reports)
- Pattern recognition (comparing to Code's predictions)

**Together**:
- Execute test scenarios systematically
- Document everything
- Make go/no-go decisions
- Create bug reports as needed

---

## PHASE -1: INFRASTRUCTURE VERIFICATION [5-10 MIN]

### Goal: Confirm system is ready for testing

**Step 1: Start System**
```bash
# Terminal 1: Start web server
python main.py

# Expected: Server starts on localhost:8001
# Time: < 10 seconds
# Evidence: Screenshot terminal output
```

**Step 2: Verify Web Interface**
```bash
# Browser: http://localhost:8001

# Expected: Interface loads
# Evidence: Screenshot landing page
```

**Step 3: Check Database**
```bash
# Terminal 2: Database connection
psql -h localhost -p 5433 -U postgres -d piper_morgan

# Query:
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM alpha_users;

# Expected: Both tables exist, may have rows
# Evidence: Screenshot query results
```

**Step 4: Run Status Check**
```bash
# Terminal 2: System status
python main.py status

# Expected: Services OK, database connected
# Evidence: Screenshot output
```

**Go/No-Go Decision**:
- ✅ **GO**: All 4 steps pass → Proceed to Journey 1
- ❌ **NO-GO**: Any step fails → Stop, document, fix

---

## JOURNEY 1: ALPHA ONBOARDING [MUST WORK] [30-45 MIN]

### Goal: Verify complete onboarding flow works

**Priority**: P0 - Alpha blocker if broken
**Status from Code**: ✅ All components ready
**Expected**: Smooth flow, no crashes, clear prompts

---

### Step 1.1: Setup Wizard [MUST WORK]

**Command**:
```bash
python main.py setup
```

**Expected Flow**:
1. Welcome message
2. API key prompts (OpenAI, Anthropic, etc.)
3. Key validation (format, strength, leak detection)
4. Success confirmation
5. User account creation

**Test Actions**:
1. Run setup command
2. Try invalid key first: "invalid-key-12345"
3. Observe validation error (should reject clearly)
4. Try valid key format: sk-proj-... or sk-ant-...
5. Complete setup

**Evidence to Collect**:
- [ ] Screenshot each wizard step
- [ ] Screenshot invalid key rejection
- [ ] Screenshot valid key acceptance
- [ ] Terminal output (full)
- [ ] Time to complete (target: < 10 minutes)

**Acceptance Criteria**:
- [ ] Setup completes without crashes
- [ ] Invalid keys rejected with clear errors
- [ ] Valid keys accepted and stored
- [ ] Prompts clear and helpful
- [ ] User created in database

**Reality Check**:
```sql
-- Verify user created
SELECT username, email, created_at FROM alpha_users ORDER BY created_at DESC LIMIT 1;

-- Verify API key stored (encrypted)
SELECT provider, created_at FROM user_api_keys WHERE user_id = (SELECT id FROM alpha_users ORDER BY created_at DESC LIMIT 1);
```

**If Fails**: Document as P0 bug, stop testing Journey 1

---

### Step 1.2: Preferences Questionnaire [MUST WORK]

**Command**:
```bash
python main.py preferences
```

**Expected Flow**:
1. 5 questions presented:
   - Communication style (formal/casual/adaptive)
   - Work style (structured/flexible/balanced)
   - Technical preference (detailed/overview/contextual)
   - Decision style (data-driven/intuitive/collaborative)
   - Learning style (hands-on/conceptual/mixed)
2. Answers validated
3. Preferences saved to database
4. Success confirmation

**Test Actions**:
1. Run preferences command
2. Answer all 5 questions
3. Try invalid input (should validate)
4. Complete questionnaire

**Evidence to Collect**:
- [ ] Screenshot questionnaire
- [ ] Screenshot each question
- [ ] Terminal output
- [ ] Time to complete

**Acceptance Criteria**:
- [ ] All 5 questions work
- [ ] Input validation works
- [ ] Preferences saved to database
- [ ] No crashes

**Reality Check**:
```sql
-- Verify preferences saved
SELECT username, preferences FROM alpha_users ORDER BY created_at DESC LIMIT 1;
```

**If Fails**: Document as P0/P1 bug depending on severity

---

### Step 1.3: First Conversation [MUST WORK]

**Action**: Via web interface at http://localhost:8001

**Test Message**:
```
"Hello, what can you help me with?"
```

**Expected**:
- Response generates successfully
- No crashes or errors
- Response reflects preferences (if set to casual, tone is casual)
- Response time < 10 seconds

**Test Actions**:
1. Open web interface
2. Send test message
3. Wait for response
4. Observe tone/style

**Evidence to Collect**:
- [ ] Screenshot message sent
- [ ] Screenshot response received
- [ ] Note response time
- [ ] Check if preferences affect tone

**Acceptance Criteria**:
- [ ] Chat interface works
- [ ] Message sends successfully
- [ ] Response generated
- [ ] No errors in terminal logs
- [ ] Preferences appear to influence style

**If Fails**: Document as P0 bug, major blocker

---

## JOURNEY 2: LEARNING SYSTEM [IF EXISTS] [45-60 MIN]

### Goal: Discover how learning system actually behaves

**Priority**: P1 - Should work, but discovery mode
**Status from Code**: ✅ All 3 components wired, 52/52 tests pass
**Expected**: Learning flow works, but behavior may differ from predictions

---

### Step 2.1: Learning System Discovery Tests [IF EXISTS] 🔍

**IMPORTANT NOTE**: Original test design had context gap. We're testing 3 scenarios to discover actual behavior.

---

#### Scenario A: Original Test (Context Gap Suspected)

**Purpose**: Test what Code's system does with potentially incomplete context

**Messages** (via web interface):
```
Message 1: "I prefer morning meetings because I have more energy"
[Wait ~30 seconds for processing]

Message 2: "When should we schedule the architecture review?"
```

**Discover**:
- What does Piper respond to Message 1?
- Does it acknowledge the preference?
- What does Piper respond to Message 2?
- Does it suggest morning?
- Does it ask for context ("What architecture review?")?
- Does it reference the preference from Message 1?
- Something else entirely?

**Evidence**:
- [ ] Screenshot both messages
- [ ] Screenshot both responses (full text)
- [ ] Note exact wording
- [ ] Check database for stored preference
- [ ] Check logs for graph/learning activity

**Analysis Questions**:
- Did learning system activate?
- Was preference stored?
- Was preference applied?
- Does response make sense given context gap?

---

#### Scenario B: Generic Test (More Realistic)

**Purpose**: Test with more natural conversational flow

**Messages**:
```
Message 1: "I prefer morning meetings because I have more energy"
[Wait ~30 seconds]

Message 2: "When should we have our next team meeting?"
```

**Discover**:
- Does it suggest morning?
- Does it explicitly reference the earlier preference?
- How does it phrase the recommendation?
- More coherent than Scenario A?

**Evidence**:
- [ ] Screenshot both messages
- [ ] Screenshot both responses
- [ ] Compare to Scenario A
- [ ] Note which feels more natural

---

#### Scenario C: Full Context Test (Ideal)

**Purpose**: Test with complete context established

**Messages**:
```
Message 1: "We need to schedule an architecture review meeting"
[Wait ~10 seconds]

Message 2: "I prefer morning meetings because I have more energy"
[Wait ~30 seconds]

Message 3: "When should we schedule the architecture review?"
```

**Discover**:
- Does it connect all three messages?
- Does it suggest morning for the architecture review specifically?
- Does it reference both the meeting type and preference?
- Best overall behavior?

**Evidence**:
- [ ] Screenshot all messages and responses
- [ ] Note conversation flow
- [ ] Check if this is the "ideal" pattern

---

#### Learning System Verification (Database)

**After all scenarios**, check what was stored:

```sql
-- Check preference storage
SELECT username, preferences FROM alpha_users WHERE username = 'your_test_user';

-- Check knowledge graph (if accessible)
SELECT * FROM knowledge_nodes WHERE content ILIKE '%morning%';
SELECT * FROM knowledge_edges WHERE source_id IN (SELECT id FROM knowledge_nodes WHERE content ILIKE '%morning%');

-- Check learning patterns (file-based, may need to check filesystem)
-- Location from Code: data/learning/learned_patterns.json
```

**Reality Check Questions**:
1. Was preference stored correctly? (preferences JSONB field)
2. Did graph create relationship nodes? (knowledge_nodes/edges)
3. Did pattern learning record the preference? (JSON files)
4. Which scenario worked best?
5. Does reality match Code's prediction of "fully wired" system?

---

### Step 2.2: Preference Persistence Test [IF EXISTS]

**Purpose**: Verify preferences persist across sessions/messages

**Test**:
```
Message 1: Set preference in Scenario B or C above
[Close browser or restart session]

Message 2: "What time works best for meetings?"
```

**Discover**:
- Does it remember the morning preference?
- Does it apply it without re-stating?
- Persistence actually working?

**Evidence**:
- [ ] Screenshot response
- [ ] Check database confirms preference still stored
- [ ] Note if system "remembers"

---

## JOURNEY 3: INTEGRATIONS [IF EXISTS] [60-90 MIN]

### Goal: Test all 4 integrations work as Code predicted

**Priority**: P1-P2 depending on integration
**Status from Code**: ✅ All 4 fully implemented
**Expected**: Operations work with proper credentials

**SETUP REQUIRED**:
```bash
# Ensure environment variables set
echo $GITHUB_TOKEN
echo $SLACK_BOT_TOKEN
echo $GOOGLE_APPLICATION_CREDENTIALS
echo $NOTION_API_KEY

# If any missing, testing that integration will fail
```

---

### Step 3.1: GitHub Integration [IF EXISTS]

**Status from Code**: ✅ 20+ operations, MCP + Spatial Router

**Test Query** (via web interface):
```
"Show me my GitHub issues"
```

**Expected**:
- GitHub integration activates
- Issues fetched (or clear error if token invalid)
- Formatted list returned
- No crashes

**Evidence**:
- [ ] Screenshot query and response
- [ ] Check terminal logs for GitHub API calls
- [ ] Note response quality
- [ ] Verify integration activated

**If Works**: Mark as ✅ WORKING
**If Fails**: Check token, document behavior

---

### Step 3.2: Slack Integration [IF EXISTS]

**Status from Code**: ✅ 22 operations, Direct Spatial Router

**Test Query**:
```
"Post to Slack: This is a test message from Piper Morgan"
```

**Expected**:
- Slack integration activates
- Message posted (or clear error)
- Confirmation returned
- No crashes

**Evidence**:
- [ ] Screenshot query and response
- [ ] Check Slack for actual message
- [ ] Note if message appeared

**If Works**: Mark as ✅ WORKING
**If Fails**: Check token, document behavior

---

### Step 3.3: Calendar Integration [IF EXISTS]

**Status from Code**: ✅ 4+ operations, Tool-based MCP

**Test Query**:
```
"Check my calendar for tomorrow"
```

**Expected**:
- Calendar integration activates
- Events listed (or "no events")
- No crashes

**Evidence**:
- [ ] Screenshot response
- [ ] Verify accuracy if events exist

**If Works**: Mark as ✅ WORKING
**If Fails**: Check credentials, document

---

### Step 3.4: Notion Integration [IF EXISTS]

**Status from Code**: ✅ 22 operations, Tool-based MCP

**Test Query**:
```
"List my Notion databases"
```

**Expected**:
- Notion integration activates
- Databases listed
- No crashes

**Evidence**:
- [ ] Screenshot response
- [ ] Verify databases match reality

**If Works**: Mark as ✅ WORKING
**If Fails**: Check API key, document

---

### Step 3.5: Multi-Tool Orchestration [IF EXISTS]

**Status from Code**: ✅ Orchestration engine functional

**Test Query**:
```
"Check my GitHub issues and my calendar for tomorrow, then suggest when I can work on the highest priority issue"
```

**Expected**:
- Both GitHub and Calendar activate
- Data combined intelligently
- Suggestion makes sense
- Orchestration coordinates properly

**Evidence**:
- [ ] Screenshot query and response
- [ ] Check logs for both integrations called
- [ ] Note response quality
- [ ] Verify orchestration worked

**This is the "unified system" test** - do components really work together?

---

## JOURNEY 4: EDGE CASES [IF EXISTS] [30-45 MIN]

### Goal: Test error handling and boundaries

**Priority**: P2-P3 (nice to have working)
**Expected**: Graceful degradation, clear errors

---

### Step 4.1: Bad Inputs [IF EXISTS]

**Tests**:

1. **Empty Input**:
   - Send empty message
   - Expected: Clear error or "I need input"

2. **Huge Input**:
   - Send 10,000+ character message
   - Expected: Handled gracefully (truncation or error)

3. **Injection Attempt**:
   - Send: `'; DROP TABLE users; --`
   - Expected: Safely rejected, no SQL injection

**Evidence**:
- [ ] Screenshot each test
- [ ] Note error messages
- [ ] Verify system stability
- [ ] Check database integrity after injection

---

### Step 4.2: Integration Failures [IF EXISTS]

**Test**: Break an integration temporarily

```bash
# Break GitHub token
export GITHUB_TOKEN=invalid_token_xyz

# Try GitHub query
"Show me my GitHub issues"

# Expected: Clear error message, no crash

# Restore token
export GITHUB_TOKEN=<valid_token>
```

**Evidence**:
- [ ] Screenshot error message
- [ ] Check if error is user-friendly
- [ ] Verify system remains stable

---

### Step 4.3: Cost Tracking Verification [IF EXISTS]

**Status from Code**: ✅ Full cost tracker with database logging

**Test**: After running several queries, check costs

```sql
-- Query cost tracking
SELECT
  timestamp,
  model_name,
  prompt_tokens,
  completion_tokens,
  estimated_cost
FROM api_usage_logs
ORDER BY timestamp DESC
LIMIT 20;
```

**Evidence**:
- [ ] Screenshot query results
- [ ] Verify token counts seem reasonable
- [ ] Check estimated costs calculated
- [ ] Compare to API provider dashboard if possible

**This verifies Issue #271 (CORE-KEYS-COST-TRACKING) working**

---

## PHASE 3: RUN INTEGRATION TEST SUITE [15-30 MIN]

### Goal: Verify Code's predictions about test infrastructure

**Status from Code**: ✅ 79 files, 447+ fixtures, expect high pass rate

**Command**:
```bash
# Run full integration test suite
pytest tests/integration/ -v --tb=short

# Expected: Most tests pass
# Code predicted: 52/52 learning tests pass
```

**Evidence**:
- [ ] Screenshot test results summary
- [ ] Note pass/fail counts
- [ ] Compare to Code's predictions
- [ ] Document any surprising failures

**Specific tests to verify**:
```bash
# Learning system (should be 52 pass)
pytest tests/integration/test_knowledge_graph_enhancement.py -v  # 40 tests
pytest tests/integration/test_preference_learning.py -v          # 5 tests
pytest tests/integration/test_learning_system.py -v              # 7 tests, 2 skip

# Sprint A8 features
pytest tests/integration/test_api_usage_tracking.py -v           # 15 tests
```

**Reality Check**:
- Do test results match Code's report?
- Any surprising failures?
- Are the 52/52 learning tests still passing?

---

## EVIDENCE COLLECTION REQUIREMENTS

### For Each Test

**Required**:
1. ✅ Screenshot (before and after)
2. ✅ Terminal output (if CLI command)
3. ✅ Timing (how long did it take?)
4. ✅ Result (PASS/FAIL/PARTIAL/DISCOVERY)
5. ✅ Comparison to Code's prediction (MATCH/DIFFER)
6. ✅ Notes (observations, confusion points)

**Save Location**:
```
~/Desktop/piper-phase2-evidence/
├── journey-1-onboarding/
├── journey-2-learning/
├── journey-3-integrations/
├── journey-4-edge-cases/
└── test-suite-results/
```

---

## BUG REPORTING

### When to Create Bug Report

**P0 - BLOCKER** (Stop testing immediately):
- System crashes on startup
- [MUST WORK] feature completely broken
- Data corruption
- Security vulnerability

**P1 - CRITICAL** (Document, continue testing):
- [MUST WORK] feature degraded
- [IF EXISTS] feature completely broken if important
- Major UX confusion

**P2 - MAJOR** (Document, not urgent):
- [MUST WORK] minor issues
- [IF EXISTS] partially broken
- Workarounds exist

**P3 - MINOR** (Note for later):
- [IF EXISTS] edge cases
- Polish issues
- Nice-to-have improvements

### Bug Report Template

```markdown
## Bug #XXX: [TITLE]

**Severity**: P0/P1/P2/P3
**Category**: [MUST WORK] / [IF EXISTS] / [FUTURE]
**Journey**: Journey X, Step Y
**Component**: [What broke]

### Code's Prediction
[What Code said should exist/work]

### Expected Behavior
[What should happen]

### Actual Behavior
[What actually happened]

### Reproduction Steps
1. Step one
2. Step two
3. ERROR: [What happens]

### Evidence
- Screenshot: [link]
- Terminal output: [paste]
- Database state: [query results]

### Impact
[Who this affects and how]

### Proposed Fix
[If obvious]
```

---

## SESSION MANAGEMENT

### Every 30 Minutes

**Update Progress**:
- Which journey? Which step?
- Findings so far?
- Any blockers?
- On track for 4-6 hour completion?

**Reality vs Predictions**:
- What matched Code's report?
- What surprised us?
- What needs deeper investigation?

### Evidence Format

```markdown
## Test: [Name]
**Time**: [timestamp]
**Duration**: X seconds
**Result**: PASS / FAIL / PARTIAL / DISCOVERY

### Code Predicted
[What Code said]

### Reality
[What actually happened]

### Match
✅ YES - Matched prediction
❌ NO - Differed from prediction
🔍 DISCOVERY - No specific prediction, documenting reality

### Evidence
- Screenshot: [link]
- Terminal: [paste]
- Database: [query results]

### Notes
[Observations, surprises, next steps]
```

---

## SUCCESS CRITERIA

### Phase 2 Complete When

**Journeys**:
- [ ] Journey 1 (Onboarding) - All [MUST WORK] tests executed
- [ ] Journey 2 (Learning) - All 3 scenarios tested, reality documented
- [ ] Journey 3 (Integrations) - All 4 integrations tested
- [ ] Journey 4 (Edge cases) - Error handling verified

**Tests**:
- [ ] Integration test suite run
- [ ] Results compared to Code's predictions

**Documentation**:
- [ ] All evidence collected
- [ ] Test results summary created
- [ ] Bugs documented (if any)
- [ ] Reality vs predictions analysis complete
- [ ] Go/no-go recommendation made

**Deliverables**:
- [ ] Test results summary document
- [ ] Bug reports (if needed)
- [ ] Evidence folder with all screenshots
- [ ] Updated session log

---

## FINAL DELIVERABLE

### Test Results Summary

```markdown
# Phase 2 Testing Results

**Date**: Sunday, October 26, 2025
**Duration**: [actual time]
**Tester**: [name]

## Executive Summary

**Overall Assessment**: READY / BLOCKERS / NEEDS WORK
**Confidence**: HIGH / MEDIUM / LOW

**Key Findings**:
- [3-5 bullet points]

## Journey Results

### Journey 1: Alpha Onboarding [MUST WORK]
- Status: PASS / FAIL / PARTIAL
- All steps: [list results]
- Bugs: P0: X, P1: Y, P2: Z

### Journey 2: Learning System [IF EXISTS]
- Scenario A: [result + findings]
- Scenario B: [result + findings]
- Scenario C: [result + findings]
- Best scenario: [A/B/C]
- Learning system working: YES / NO / PARTIALLY

### Journey 3: Integrations [IF EXISTS]
- GitHub: WORKING / NOT WORKING
- Slack: WORKING / NOT WORKING
- Calendar: WORKING / NOT WORKING
- Notion: WORKING / NOT WORKING
- Orchestration: WORKING / NOT WORKING

### Journey 4: Edge Cases [IF EXISTS]
- Error handling: GOOD / NEEDS WORK
- Security boundaries: HELD / ISSUES

## Code's Predictions vs Reality

| Prediction | Reality | Match? |
|------------|---------|--------|
| All [MUST WORK] ready | [actual] | ✅/❌ |
| All integrations working | [actual] | ✅/❌ |
| Learning system wired | [actual] | ✅/❌ |
| 52/52 learning tests pass | [actual] | ✅/❌ |

## Bugs Found

**P0 (Blockers)**: [count]
- [list with links]

**P1 (Critical)**: [count]
- [list with links]

**P2 (Major)**: [count]
- [list with links]

**P3 (Minor)**: [count]
- [list with links]

## Go/No-Go Recommendation

**Recommendation**: READY FOR ALPHA / BLOCKERS / NEEDS WORK

**Rationale**: [based on test results]

**Next Steps**: [what needs to happen before Phase 3]
```

---

## REMEMBER

1. **Discovery Philosophy**: Try optimistically, document reality
2. **Code's Confidence**: System is unified and well-tested
3. **Compare Reality**: Does it match Code's predictions?
4. **Focus on Blockers**: P0/P1 bugs stop alpha, not P2/P3
5. **Evidence Everything**: Screenshots, logs, database queries
6. **Time Box**: Stop after 6 hours, document what's left

---

## CURRENT TIME: 1:38 PM

**Estimated Completion**: 5:38 PM - 7:38 PM (4-6 hours)

**Ready to begin?** 🚀

Start with Phase -1 (Infrastructure Verification), then proceed systematically through each journey!

---

*Testing Prompt Version: 1.0*
*Created: Sunday, October 26, 2025, 1:38 PM PT*
*Based on Code's archaeological investigation + refined learning test*
*Ready for execution!*
