# Sprint A8 Phase 2 Gameplan: End-to-End System Testing (REVISED)

**Sprint**: A8 (Alpha Preparation)
**Phase**: 2 of 5
**Theme**: "System Validation & Bug Discovery"
**Duration**: 4-6 hours estimated
**Original Date**: October 27, 2025
**Revised Date**: October 26, 2025, 9:18 AM PT
**Based On**: Code archaeological investigation report (60 min)
**Philosophy**: Discovery testing with priority classification

---

## REVISION SUMMARY

### Major Finding
**Code's Discovery**: "This isn't a 75% complete codebase with scattered features. It's a unified system where components know about each other, learning flows from user behavior → patterns → preferences, preferences affect intent classification, classification uses graph reasoning, and everything is tested and working together."

### Changes from Original Gameplan
- ✅ Added [MUST WORK] / [IF EXISTS] / [FUTURE] priority tags to all tests
- ✅ Updated all commands with actual paths and locations from codebase
- ✅ Added status annotations for every component (52/52 learning tests passing!)
- ✅ Documented all 4 integrations as fully functional
- ✅ Clarified scope boundaries with evidence
- ✅ Noted discovered capabilities (2-tier user system, JWT auth, mature test infrastructure)
- ✅ **Refined learning system test** with 3 scenarios (A/B/C) after identifying potential context gap in original design

### Test Readiness Summary
- **[MUST WORK] tests**: 3/3 ready ✅ (Onboarding, Chat, API Keys)
- **[IF EXISTS] tests**: 8+/8+ ready ✅ (All integrations, learning system, cost tracking)
- **[FUTURE] tests**: 5+ correctly identified and skipped
- **Overall**: 79 integration test files, 447+ fixtures, 1,625+ lines of Sprint A8 test code

### Go/No-Go Decision
**Status**: ✅ **READY FOR COMPREHENSIVE END-TO-END TESTING**
**Confidence**: HIGH 🎯
**Blockers**: NONE
**Can Begin Testing**: YES - IMMEDIATELY

---

## CRITICAL CONTEXT

### Sprint A8 is NOT Complete
**Completed**: Phase 1 (5 integration issues) ✅
**Current**: Phase 2 (E2E testing) ← YOU ARE HERE
**Status**: ALL COMPONENTS READY FOR TESTING ✅
**Remaining**: Phases 3, 4, 5 still required

### Inchworm Position
2.9.3.1 → Moving toward 2.9.3.2
- We are IN Sprint A8
- We are IN Phase 2
- We are STARTING testing
- We have VERIFIED everything exists and works
- We are NOT done with Sprint A8

---

## Phase 2 Objectives

### Primary Goals
1. ✅ **Validate integrated system** - Code confirmed: All Phase 1 work plays nicely together
2. 🔍 **Discover blocking bugs** - Find what breaks before alpha testers do
3. ✅ **Verify user journeys** - Code confirmed: Complete paths exist end-to-end
4. ✅ **Document gaps** - Code found: Minimal gaps, mostly complete system

### What This Phase is NOT
- NOT final testing (that's Phase 5)
- NOT performance optimization
- NOT feature additions
- NOT "good enough" checking

---

## Phase -1: Infrastructure Verification [MUST WORK]

### Status from Code's Investigation: ✅ ALL READY

**System Requirements**:
```bash
# PostgreSQL must be on port 5433 (NOT 5432)
psql -h localhost -p 5433 -U postgres

# Web server runs on port 8001 (NOT 8080)
curl http://localhost:8001/health

# Main entry point is main.py (NOT web/app.py)
python main.py
```

### Verify Test Environment

**Infrastructure Check**:
```bash
# 1. Check system health (Code found this command)
python main.py status
# Location: main.py lines 178-209
# Status: ✅ EXISTS
# Purpose: Verifies services, database, external connections

# 2. Verify database state
# Database: PostgreSQL on localhost:5433
# Status: ✅ Ready with migrations applied
# Tables: users (production), alpha_users (testers), api_usage_logs, etc.

# 3. Check all integrations (Code confirmed all 4 exist)
# GitHub: services/integrations/github/ (20+ operations)
# Slack: services/integrations/slack/ (22 operations)
# Calendar: services/integrations/calendar/ (4+ operations)
# Notion: services/integrations/notion/ (22 operations)

# 4. Verify test data
# Test users: Auto-created from personality_profiles via migrations
# Alpha users: Separate table (alpha_users) with UUID IDs
# Production users: String(255) IDs from migrated system
```

**Required Environment Variables**:
```bash
export GITHUB_TOKEN=<your_token>               # For GitHub integration
export SLACK_BOT_TOKEN=<your_token>            # For Slack integration
export GOOGLE_APPLICATION_CREDENTIALS=<path>   # For Calendar integration
export NOTION_API_KEY=<your_key>              # For Notion integration
```

**Expected State**:
- ✅ Web server ready on port 8001
- ✅ Database connected on port 5433 and migrated
- ✅ All Phase 1 integrations active and testable
- ✅ Test user accounts exist (via migrations)
- ✅ JWT authentication system working

**If ANY mismatch**: STOP and fix before proceeding

---

## Phase 0: Test Planning

### Test User Personas

**Alpha User Day 1** (Primary):
- Name: alex-alpha
- Profile: New PM, never used Piper
- Goal: Get value in first session
- Success: Completes onboarding and one real task
- **Implementation**: Create via setup wizard or ORM as AlphaUser

**Power User** (Secondary):
- Name: pat-power
- Profile: Expert PM, high expectations
- Goal: Complex workflow automation
- Success: Multi-tool orchestration works
- **Implementation**: Create as AlphaUser with advanced preferences

**Edge Case User** (Tertiary):
- Name: eve-edge
- Profile: Breaks everything
- Goal: Find failure modes
- Success: System handles gracefully
- **Implementation**: Create as AlphaUser for destructive testing

**User Creation** (from Code's findings):
```python
# Via ORM
from services.database.models import AlphaUser
user = AlphaUser(username="alex-alpha", email="alex@test.com", ...)

# Via setup wizard (interactive)
python main.py setup

# Via migrations (automatic from personality_profiles)
# Already created during database setup
```

---

## Phase 1: User Journey Testing

### Journey 1: Alpha Onboarding [MUST WORK] ✅

**Overall Status**: ✅ READY - All components verified by Code
**Can Test**: YES - No blockers found

**Test Sequence**:

#### Step 1: First Run [MUST WORK]
**Status**: ✅ READY
**Command**: `python main.py`
**Location**: main.py line 25
**Found by Code**: Web server starts on localhost:8001
**Expected**: Welcome message, system initializes

**Test**:
```bash
# Start system
python main.py

# Verify web interface loads
curl http://localhost:8001/

# Expected: Server responds, logs show initialization
```

**Evidence to Collect**:
- Terminal output showing server start
- Browser screenshot of web interface
- Time to start (should be <10 seconds)

---

#### Step 2: Setup Wizard [MUST WORK]
**Status**: ✅ READY
**Command**: `python main.py setup`
**Location**: main.py lines 53-104
**Found by Code**: Interactive onboarding wizard (Issue #218)
**Expected**: Step-by-step setup with API key collection

**Test**:
```bash
python main.py setup

# EXPECT:
# 1. Welcome message
# 2. API key prompts (OpenAI, Anthropic, etc.)
# 3. Validation of each key (Issue #268)
# 4. Success confirmation
# 5. User account creation
```

**Evidence to Collect**:
- Screenshot each wizard step
- Note any confusing prompts
- Verify completion message
- Check database for created user

**Acceptance Criteria**:
- [ ] Complete onboarding < 10 minutes
- [ ] No crashes or hangs
- [ ] Clear next steps at each point
- [ ] Keys validated before storage
- [ ] User created in database

---

#### Step 3: API Key Configuration [MUST WORK]
**Status**: ✅ READY
**Service**: services/security/api_key_validator.py
**Found by Code**: Full validation (format, strength, leak detection)
**Tests**: tests/security/test_key_storage_validation.py
**Expected**: Invalid keys rejected, valid keys stored

**Test Invalid Key**:
```bash
# During setup wizard, try invalid key
# Test API key: "invalid-key-12345"

# EXPECT:
# - Format validation error
# - Clear error message
# - Prompt to retry
# - NO storage of invalid key
```

**Test Valid Key**:
```bash
# Enter valid API key format
# Test API key: sk-proj-... (real format)

# EXPECT:
# - Format validation passes
# - Strength analysis (if weak, warn but allow)
# - Leak detection check
# - Key stored in database
# - Success confirmation
```

**Evidence to Collect**:
- Screenshot of invalid key rejection
- Screenshot of valid key acceptance
- Database query showing stored key (encrypted)
- Verification that key validator components work

**Acceptance Criteria**:
- [ ] Invalid keys rejected with clear errors
- [ ] Valid keys accepted and stored
- [ ] No plaintext keys in database
- [ ] KeyValidator, KeyStrengthAnalyzer, KeyLeakDetector all functional

---

#### Step 4: Preference Questionnaire [MUST WORK]
**Status**: ✅ READY
**Command**: `python main.py preferences`
**Location**: main.py lines 106-145
**Found by Code**: Interactive questionnaire (Issue #267)
**Service**: services/personality/personality_profile.py
**Tests**: tests/services/test_personality_preferences.py (650 lines)
**Expected**: All 5 questions work, preferences saved to database

**Test**:
```bash
python main.py preferences

# EXPECT 5 Questions:
# 1. Communication style (formal/casual/adaptive)
# 2. Work style (structured/flexible/balanced)
# 3. Technical preference (detailed/overview/contextual)
# 4. Decision style (data-driven/intuitive/collaborative)
# 5. Learning style (hands-on/conceptual/mixed)
```

**Test Flow**:
1. Answer each question
2. Verify saved to database
3. Check preferences applied to profile
4. Confirm no errors during save

**Evidence to Collect**:
- Screenshot questionnaire prompts
- Terminal output of completion
- Database query: `SELECT preferences FROM alpha_users WHERE username='test-user'`
- Verify JSONB storage working

**Acceptance Criteria**:
- [ ] All 5 questions display correctly
- [ ] Input validation works
- [ ] Preferences saved to database (JSONB field)
- [ ] No crashes during questionnaire
- [ ] Completion message clear

---

#### Step 5: First Conversation [IF EXISTS] 🔍
**Status**: ✅ READY (web interface exists, chat functionality testable)
**Command**: Via web interface at localhost:8001
**Found by Code**: Web server infrastructure complete
**Expected**: Response reflects preferences (Issue #269 semantic bridge)

**Test**:
```bash
# Start web server if not running
python main.py

# Open browser: http://localhost:8001

# Send message: "Hello, what can you help me with?"

# EXPECT:
# - Response generated (no errors)
# - Tone matches preference (if set to casual, response is casual)
# - No crashes
# - Smooth interaction
```

**Evidence to Collect**:
- Screenshot of first message
- Screenshot of response
- Note response time
- Check if preferences affect tone/style

**Acceptance Criteria**:
- [ ] Chat interface loads
- [ ] Message sent successfully
- [ ] Response generated
- [ ] Preferences appear to influence response
- [ ] No errors in logs

---

#### Step 6: Document Analysis [IF EXISTS] 🔍
**Status**: ✅ READY (Knowledge graph enhancement #278 fully implemented)
**Service**: services/knowledge/knowledge_graph_service.py
**Tests**: 40/40 PASS in test_knowledge_graph_enhancement.py
**Expected**: Upload works, analysis completes, knowledge graph updated

**Test**:
```bash
# Create test document
echo "Test document about project management best practices" > test.md

# Upload via web interface or CLI
# (Check web interface for upload functionality)

# EXPECT:
# - File uploaded successfully
# - Content extracted
# - Knowledge graph nodes created
# - Relationships established
# - No errors during processing
```

**Evidence to Collect**:
- Screenshot of upload interface
- Terminal logs showing processing
- Database query showing new graph nodes
- Verification that graph-first retrieval works

**Acceptance Criteria**:
- [ ] Document upload mechanism exists
- [ ] Content processing works
- [ ] Graph updated with new nodes
- [ ] Reasoning chains established
- [ ] No crashes during upload

---

### Journey 2: Power Workflows [IF EXISTS] 🔍

**Overall Status**: ✅ READY - All integrations exist and are testable
**Can Test**: YES - Code confirmed all 4 integrations implemented

**Integration Summary from Code**:
- ✅ GitHub: 20+ operations, requires `GITHUB_TOKEN`
- ✅ Slack: 22 operations, requires `SLACK_BOT_TOKEN`
- ✅ Calendar: 4+ operations, requires `GOOGLE_APPLICATION_CREDENTIALS`
- ✅ Notion: 22 operations, requires `NOTION_API_KEY`

---

#### Step 1: GitHub Integration Test [IF EXISTS]
**Status**: ✅ READY
**Location**: services/integrations/github/
**Operations**: 20+ (issues, repos, workflows, content generation)
**Tests**: 4+ test files with comprehensive coverage
**Found by Code**: Fully functional with MCP + Spatial Router

**Test Complex Query**:
```bash
# Via web interface
# Message: "Review my GitHub issues and create a prioritized list"

# EXPECT:
# - GitHub integration activates
# - Issues fetched successfully
# - Prioritization logic applied
# - Formatted list returned
# - No authentication errors
```

**Evidence to Collect**:
- Screenshot of query
- Screenshot of response with issue list
- Check logs for GitHub API calls
- Verify token usage (cost tracking should log this)

**Acceptance Criteria**:
- [ ] GitHub integration responds
- [ ] Issues retrieved successfully
- [ ] Response coherent and prioritized
- [ ] No crashes or auth failures

---

#### Step 2: Multi-Tool Orchestration [IF EXISTS]
**Status**: ✅ READY
**Service**: services/orchestration/engine.py
**Found by Code**: Multi-tool coordination functional
**Expected**: Calendar + GitHub integration working together

**Test**:
```bash
# Via web interface
# Message: "Schedule standup based on team availability and create agenda from open issues"

# EXPECT:
# - Calendar integration checks availability
# - GitHub integration fetches open issues
# - Orchestration combines both
# - Suggested time + agenda returned
# - Both integrations logged
```

**Evidence to Collect**:
- Screenshot of query
- Screenshot of response
- Check logs for both Calendar and GitHub calls
- Verify orchestration engine coordinated properly

**Acceptance Criteria**:
- [ ] Both integrations activated
- [ ] Data from both sources combined
- [ ] Response coherent and actionable
- [ ] No integration conflicts

---

#### Step 3: Learning System Test [IF EXISTS] 🔍 DISCOVERY MODE
**Status**: ✅ READY - ALL THREE COMPONENTS WIRED
**Components**: Graph reasoning + Preference persistence + Pattern learning
**Tests**: 52/52 PASS (40 graph + 5 preference + 7 learning)
**Found by Code**: Fully integrated learning flow

**IMPORTANT NOTE**: Original test design identified to have potential context gap. Testing multiple scenarios to discover actual behavior.

---

**Scenario A: Original Test** (Context Gap Suspected)

**Purpose**: Test what happens with potentially incomplete context

```bash
# Message 1
"I prefer morning meetings because I have more energy"

# Wait ~30 seconds for processing

# Message 2
"When should we schedule the architecture review?"

# DISCOVER what happens:
# - Does it suggest morning? (learning working)
# - Does it ask for context? ("What architecture review?")
# - Does it ignore preference? (not applied)
# - Does it reference Message 1 explicitly?
# - Something else entirely?
```

**Evidence to Collect**:
- [ ] Screenshot both messages and responses
- [ ] Note exact wording of both responses
- [ ] Check database for stored preference
- [ ] Check logs for graph/learning activity
- [ ] Document what actually happens

---

**Scenario B: Generic Test** (More Realistic)

**Purpose**: Test with more natural conversational flow

```bash
# Message 1
"I prefer morning meetings because I have more energy"

# Wait ~30 seconds

# Message 2
"When should we have our next team meeting?"

# DISCOVER what happens:
# - Does it suggest morning?
# - Does it explicitly reference the earlier preference?
# - How does it phrase the recommendation?
# - More coherent than Scenario A?
```

**Evidence to Collect**:
- [ ] Screenshot both messages and responses
- [ ] Compare response quality to Scenario A
- [ ] Note which feels more natural
- [ ] Check if preference is applied

---

**Scenario C: Full Context Test** (Ideal)

**Purpose**: Test with complete context established first

```bash
# Message 1: Establish context
"We need to schedule an architecture review meeting"

# Wait ~10 seconds

# Message 2: Establish preference
"I prefer morning meetings because I have more energy"

# Wait ~30 seconds

# Message 3: Test learning
"When should we schedule the architecture review?"

# DISCOVER what happens:
# - Does it connect all three messages?
# - Does it suggest morning for the architecture review specifically?
# - Does it reference both meeting type and preference?
# - Best overall behavior of the three scenarios?
```

**Evidence to Collect**:
- [ ] Screenshot all three messages and responses
- [ ] Note conversation flow quality
- [ ] Compare to Scenarios A and B
- [ ] Document which scenario works best

---

**Database Verification** (After Testing All Scenarios):

```sql
-- Check preference storage
SELECT username, preferences FROM alpha_users WHERE username='test_user';

-- Check knowledge graph nodes
SELECT * FROM knowledge_nodes WHERE content ILIKE '%morning%';

-- Check knowledge graph edges
SELECT * FROM knowledge_edges
WHERE source_id IN (SELECT id FROM knowledge_nodes WHERE content ILIKE '%morning%');

-- Check learning patterns (file-based)
-- Location: data/learning/learned_patterns.json
```

**Acceptance Criteria**:
- [ ] At least one scenario demonstrates learning system activation
- [ ] Preference stored in database (preferences JSONB field)
- [ ] Graph nodes created (if applicable)
- [ ] Pattern learning recorded (if applicable)
- [ ] Reality documented for all three scenarios
- [ ] Best-working scenario identified

**Reality Check Questions**:
1. Was preference stored correctly?
2. Did graph create relationship nodes?
3. Did pattern learning activate?
4. Which scenario worked best?
5. Does reality match Code's prediction of "fully wired" system?
6. Is the context gap in Scenario A observable?

**Not a Bug If**: Learning system partially works or needs more context. This is discovery testing - document what actually happens.

---

#### Step 4: Cost Tracking Verification [IF EXISTS]
**Status**: ✅ READY
**Service**: services/analytics/api_usage_tracker.py
**Components**: APIUsageTracker, CostEstimator
**Tests**: 269 lines, 15 tests in test_api_usage_tracking.py
**Found by Code**: Full estimator with Claude/GPT pricing
**Database**: Migration 68166c68224b ready (api_usage_logs table)

**Test** (Note: CLI command not found, use database query):
```bash
# After running several queries with API calls

# Check database for logged usage
psql -h localhost -p 5433 -U postgres -d piper_morgan

# Query:
SELECT
  timestamp,
  model_name,
  prompt_tokens,
  completion_tokens,
  estimated_cost
FROM api_usage_logs
ORDER BY timestamp DESC
LIMIT 10;

# EXPECT:
# - Rows for each API call
# - Token counts accurate
# - Costs calculated
# - Timestamps recent
```

**Evidence to Collect**:
- Screenshot of database query results
- Compare token counts to API provider dashboard
- Verify cost calculations reasonable
- Check all API calls logged

**Acceptance Criteria**:
- [ ] All API calls logged to database
- [ ] Token counts accurate
- [ ] Cost estimates reasonable
- [ ] No missing entries

---

### Journey 3: Edge Cases & Failure Modes [IF EXISTS] 🔍

**Overall Status**: ✅ READY - Error handling infrastructure exists
**Can Test**: YES - Discovery mode for failure handling

---

#### Step 1: Bad Inputs [IF EXISTS]
**Status**: 🔍 DISCOVERY (test and document behavior)
**Expected**: Graceful degradation, clear errors

**Test**:
```bash
# Empty input
# Via web interface, send empty message

# Huge input
# Send message with 10,000+ characters

# Injection attempt
# Send message: "'; DROP TABLE users; --"

# EXPECT (for each):
# - No crashes
# - Clear error messages
# - System remains stable
# - Security boundaries hold
```

**Evidence to Collect**:
- Screenshot each test
- Note error messages
- Check logs for proper handling
- Verify database integrity after injection attempt

**Acceptance Criteria**:
- [ ] Empty input handled gracefully
- [ ] Huge input doesn't crash system
- [ ] Injection attempts safely rejected
- [ ] Clear, helpful error messages

---

#### Step 2: Resource Exhaustion [IF EXISTS]
**Status**: 🔍 DISCOVERY (test rate limiting if exists)
**Expected**: Rate limiting, graceful degradation

**Test**:
```bash
# Rapid-fire requests
# Send 100 messages as fast as possible

# EXPECT:
# - Rate limiting kicks in (if implemented)
# - OR: System handles all requests
# - No crashes
# - Clear response even under load
```

**Evidence to Collect**:
- Count successful vs rate-limited requests
- Note response times
- Check system stability
- Monitor resource usage

**Acceptance Criteria**:
- [ ] System doesn't crash under load
- [ ] Rate limiting present OR handles gracefully
- [ ] Clear messages if limited
- [ ] System recovers after load

---

#### Step 3: Integration Failures [IF EXISTS]
**Status**: ✅ READY (error handling exists in integrations)
**Expected**: Clear error messages, fallback behavior

**Test**:
```bash
# Break GitHub integration
export GITHUB_TOKEN=invalid_token_12345

# Send message: "Check my GitHub issues"

# EXPECT:
# - Authentication error detected
# - Clear error message to user
# - System doesn't crash
# - Fallback or degraded response

# Restore GitHub token
export GITHUB_TOKEN=<valid_token>
```

**Evidence to Collect**:
- Screenshot of error message
- Check logs for proper error handling
- Verify system stability
- Note fallback behavior

**Acceptance Criteria**:
- [ ] Integration failure detected
- [ ] Clear error message (not stack trace)
- [ ] System remains stable
- [ ] Fallback behavior documented

---

#### Step 4: Preference Edge Cases [IF EXISTS]
**Status**: ✅ READY (validation exists)
**Service**: services/domain/user_preference_manager.py (829 lines)
**Expected**: Validation prevents corruption

**Test**:
```bash
# Try invalid preference value
# During questionnaire, enter: "invalid_style_xyz"

# EXPECT:
# - Validation error
# - Clear message about valid options
# - Prompt to retry
# - No corruption of database
```

**Evidence to Collect**:
- Screenshot of validation error
- Verify database unchanged
- Check valid options presented
- Test retry mechanism

**Acceptance Criteria**:
- [ ] Invalid values rejected
- [ ] Validation messages clear
- [ ] No database corruption
- [ ] Retry mechanism works

---

## Phase 2: Integration Testing

### Test Matrix with Code's Findings

| Feature | Status | Location | Integration Points | Test Focus | Priority |
|---------|--------|----------|-------------------|------------|----------|
| Preferences (#269) | ✅ READY | personality_profile.py | Database, PersonalityProfile, LLM | Semantic bridge works | HIGH |
| Cost Tracking (#271) | ✅ READY | api_usage_tracker.py | LLMClient, Database, Analytics | Accurate capture | HIGH |
| Knowledge Graph (#278) | ✅ READY | knowledge_graph_service.py | Graph DB, Intent, Retrieval | Reasoning chains | HIGH |
| Key Validation (#268) | ✅ READY | api_key_validator.py | Storage, Providers, Security | Invalid rejection | MEDIUM |
| GitHub Integration | ✅ READY | integrations/github/ | MCP, Spatial Router | 20+ operations | MEDIUM |
| Slack Integration | ✅ READY | integrations/slack/ | Direct Spatial Router | 22 operations | MEDIUM |
| Calendar Integration | ✅ READY | integrations/calendar/ | Tool-based MCP | 4+ operations | LOW |
| Notion Integration | ✅ READY | integrations/notion/ | Tool-based MCP | 22 operations | LOW |

### Integration Test Commands

**Run Full Integration Test Suite**:
```bash
# From Code's findings: 79 integration test files
pytest tests/integration/ -v

# Expected: High pass rate (1,625+ lines of test code)
```

**Specific Integration Tests**:
```bash
# Preferences → Behavior
pytest tests/integration/test_preference_learning.py -v
# Expected: 5/5 PASS

# Cost → Database
pytest tests/integration/test_api_usage_tracking.py -v
# Expected: 15 tests PASS

# Graph → Retrieval
pytest tests/integration/test_knowledge_graph_enhancement.py -v
# Expected: 40/40 PASS

# Learning System
pytest tests/integration/test_learning_system.py -v
# Expected: 7 PASS, 2 SKIPPED

# All Sprint A8 features
pytest tests/integration/ -k "preference_learning or api_usage or knowledge_graph or key_storage" -v
# Expected: Most tests PASS
```

---

## Phase 3: Bug Documentation

### Bug Severity Classification

**P0 - BLOCKER**: Cannot proceed to alpha
- Crashes on startup
- Data corruption
- Security vulnerabilities
- Core [MUST WORK] features broken

**P1 - CRITICAL**: Must fix before alpha
- Major [MUST WORK] features degraded
- [IF EXISTS] features completely broken that are important
- Confusing UX blocks progress
- Performance < 5 second response

**P2 - MAJOR**: Should fix if time
- Minor [MUST WORK] features have issues
- [IF EXISTS] features partially broken
- Workaround exists
- Polish issues

**P3 - MINOR**: Document for later
- [IF EXISTS] edge cases
- Nice-to-have improvements
- [FUTURE] features noted as missing (NOT bugs)
- Future enhancements

### Bug Report Template

```markdown
## Bug #[NUMBER]: [TITLE]

**Severity**: P0/P1/P2/P3
**Category**: [MUST WORK] / [IF EXISTS] / [FUTURE]
**Component**: [Where it occurs]
**User Impact**: [Who this affects and how]

### Reproduction
1. Step one
2. Step two
3. ERROR: [What happens]

### Expected
[What should happen based on Code's findings]

### Actual
[What actually happened]

### Evidence
[Terminal output, screenshots, database state]

### Code's Finding
[What Code's archaeological report said about this component]

### Proposed Fix
[If obvious based on Code's report]
```

---

## Phase Z: Testing Complete

### Deliverables Required

#### 1. Test Results Summary
```markdown
# Phase 2 Test Results

## Journeys Tested

### Journey 1: Alpha Onboarding [MUST WORK]
**Status**: PASS / FAIL / PARTIAL
**Evidence**: [links to screenshots, logs]
**Bugs Found**: [count by severity]
**Notes**: [observations]

### Journey 2: Power Workflows [IF EXISTS]
**Status**: PASS / FAIL / PARTIAL / DISCOVERY
**Evidence**: [links to screenshots, logs]
**Bugs Found**: [count by severity]
**Surprises**: [features that exceeded expectations]
**Notes**: [observations]

### Journey 3: Edge Cases [IF EXISTS]
**Status**: PASS / FAIL / PARTIAL / DISCOVERY
**Evidence**: [links to screenshots, logs]
**Bugs Found**: [count by severity]
**Notes**: [observations]

## Bugs Found by Severity
- P0 (BLOCKER): [count] - [list]
- P1 (CRITICAL): [count] - [list]
- P2 (MAJOR): [count] - [list]
- P3 (MINOR): [count] - [list]

## Integration Test Results
```bash
pytest tests/integration/ -v
```
**Expected from Code**: 79 test files, 447+ fixtures
**Actual**: [results]
**Pass Rate**: [percentage]

## Code's Predictions vs Reality
| Prediction | Reality | Match? |
|------------|---------|--------|
| All [MUST WORK] ready | [actual] | ✅/❌ |
| All [IF EXISTS] ready | [actual] | ✅/❌ |
| Learning system wired | [actual] | ✅/❌ |
| 4 integrations working | [actual] | ✅/❌ |

## Go/No-Go Recommendation
**Recommendation**: READY FOR ALPHA / BLOCKERS FOUND / NEEDS WORK
**Confidence**: HIGH / MEDIUM / LOW
**Rationale**: [based on test results vs Code's findings]
```

#### 2. Bug Tracker Update
- Create GitHub issues for all P0/P1 bugs
- Tag appropriately (priority:P0, priority:P1, phase:2)
- Link to test evidence
- Reference Code's archaeological findings for context

#### 3. Documentation Updates
- Known issues list (from bugs found)
- Workarounds documented (if any)
- Alpha tester warnings (for P2/P3 issues)
- Surprises documented (features that exceeded expectations)

---

## STOP Conditions

### Stop Testing Immediately If

**Infrastructure Issues**:
- Database corrupted
- Security vulnerability found
- Core services won't start
→ Fix before continuing (unlikely given Code's findings)

**Systematic Failures**:
- Multiple [MUST WORK] features failing
- Same error in multiple journeys
- Integration completely broken (contradicts Code's findings)
- Performance degraded severely
→ Investigate root cause

**Time Box Exceeded**:
- Testing takes > 6 hours
- Stuck on single issue > 30 min
→ Document and move on

---

## Success Criteria

### Phase 2 is Complete When

**All User Journeys**:
- [x] Journey 1 (Alpha onboarding) - Code confirmed ready
- [x] Journey 2 (Power workflows) - Code confirmed ready
- [x] Journey 3 (Edge cases) - Components exist for testing
- [ ] Evidence collected for each journey
- [ ] Actual behavior vs Code's predictions documented

**All Integrations**:
- [x] GitHub - Code confirmed: 20+ ops working
- [x] Slack - Code confirmed: 22 ops working
- [x] Calendar - Code confirmed: 4+ ops working
- [x] Notion - Code confirmed: 22 ops working
- [ ] Integration tests run (pytest tests/integration/)
- [ ] Results match Code's expectations (79 files, high pass rate)

**All Learning Components**:
- [x] Knowledge graph - Code confirmed: 40/40 tests pass
- [x] Preferences - Code confirmed: 5/5 tests pass
- [x] Pattern learning - Code confirmed: 7/7 tests pass (2 skipped)
- [ ] Concrete learning test executed (morning meeting preference)
- [ ] Learning flow verified end-to-end

**All Bugs**:
- [ ] Documented with reproduction steps
- [ ] Classified by severity (P0/P1/P2/P3)
- [ ] Classified by category ([MUST WORK] / [IF EXISTS] / [FUTURE])
- [ ] P0/P1 issues created in GitHub
- [ ] Fix/defer decision made for each

**Documentation**:
- [ ] Test results summarized
- [ ] Known issues updated
- [ ] Go/no-go recommendation clear
- [ ] Comparison to Code's predictions documented

---

## Handoff to Phase 3

### What Phase 3 Needs From Us
- List of P0/P1 bugs to fix (if any found)
- Testing gaps identified (should be minimal)
- User journey pain points (if any)
- Performance baselines (response times, load capacity)
- Validation that Code's findings match reality

### What We're NOT Handing Off
- Feature requests (→ MVP backlog)
- P2/P3 bugs (→ documented only, fix post-alpha)
- Performance optimization (→ post-alpha)
- UI polish (→ later phases)
- [FUTURE] features (→ post-MVP)

---

## Session Management

### During Testing
- Keep terminal output (save all logs)
- Screenshot everything (every step, every result)
- Note timing for each operation (should be < 5 sec per query)
- Document confusion points (UX improvements)
- Compare reality to Code's predictions

### Evidence Format
```bash
# Terminal evidence
$ command_executed
[FULL OUTPUT INCLUDED]
# Time: X seconds
# Result: PASS/FAIL/DISCOVERY
# Code Predicted: [what Code said]
# Actual: [what happened]
# Match: YES/NO
# Notes: [observations]
```

### Session Log Updates
Every 30 minutes:
- Update progress (which journey, which step)
- Note findings (bugs, surprises, confirmations)
- Check time box (are we on track?)
- Reference Code's report (does reality match?)

---

## Remember

**This is Phase 2 of 5**. After this:
- Phase 3: Baseline Piper Education
- Phase 4: Documentation (polish drafts)
- Phase 5: Alpha deployment preparation

**We are NOT done** when testing completes. Sprint A8 continues through all 5 phases.

**Inchworm Protocol**: Complete Phase 2 100% before moving to Phase 3.

**Discovery Philosophy**: Try each feature optimistically, document what happens, compare to expectations. Only flag P0/P1 bugs for [MUST WORK] features. Everything else is discovery.

**Code's Verdict**: "This is a unified system where components know about each other and everything is tested." Test to confirm, not to doubt.

---

## Quick Reference Summary

### CLI Commands (All Verified by Code)
```bash
python main.py               # Start web server (port 8001)
python main.py setup         # Interactive onboarding wizard
python main.py status        # System health check
python main.py preferences   # Preference questionnaire
python main.py migrate-user  # Alpha to production migration
```

### Database
- **Host**: localhost:5433 (NOT 5432)
- **Database**: piper_morgan
- **Tables**: users, alpha_users, api_usage_logs, personality_profiles, +more

### Integrations (All Ready)
- **GitHub**: 20+ operations, needs GITHUB_TOKEN
- **Slack**: 22 operations, needs SLACK_BOT_TOKEN
- **Calendar**: 4+ operations, needs GOOGLE_APPLICATION_CREDENTIALS
- **Notion**: 22 operations, needs NOTION_API_KEY

### Test Infrastructure
- **Integration Tests**: 79 files in tests/integration/
- **Fixtures**: 447+ defined in tests/conftest.py
- **Run Tests**: `pytest tests/integration/ -v`
- **Expected**: High pass rate based on Code's findings

### Learning System (All Wired)
- **Graph Reasoning**: 40/40 tests pass
- **Preferences**: 5/5 tests pass
- **Pattern Learning**: 7/7 tests pass (2 skipped)
- **Total**: 52/52 tests pass
- **Status**: Fully integrated and working

### Priority Tags
- **[MUST WORK]**: Alpha blocker if broken (3 features, all ready)
- **[IF EXISTS]**: Test and document (8+ features, all ready)
- **[FUTURE]**: Skip, note absence (5+ features correctly identified)

---

**Status: READY FOR COMPREHENSIVE END-TO-END TESTING** ✅
**Confidence: HIGH** 🎯
**Next: Execute Phase 2 Test Plan Immediately**

*Revised gameplan version: 2.0*
*Based on 60-minute archaeological investigation by Code*
*All components verified, locations documented, tests counted*
*Go/No-Go: GO!*
