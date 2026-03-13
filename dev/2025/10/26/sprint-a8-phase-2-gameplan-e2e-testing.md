# Sprint A8 Phase 2 Gameplan: End-to-End System Testing

**Sprint**: A8 (Alpha Preparation)
**Phase**: 2 of 5
**Theme**: "System Validation & Bug Discovery"
**Duration**: 4-6 hours estimated
**Date**: October 27, 2025

---

## CRITICAL CONTEXT

### Sprint A8 is NOT Complete
**Completed**: Phase 1 (5 integration issues) ✅
**Current**: Phase 2 (E2E testing) ← YOU ARE HERE
**Remaining**: Phases 3, 4, 5 still required

### Inchworm Position
2.9.3.1 → Moving toward 2.9.3.2
- We are IN Sprint A8
- We are IN Phase 2
- We are STARTING testing
- We are NOT done with Sprint A8

---

## Phase 2 Objectives

### Primary Goals
1. **Validate integrated system** - All Phase 1 work plays nicely together
2. **Discover blocking bugs** - Find what breaks before alpha testers do
3. **Verify user journeys** - Complete paths work end-to-end
4. **Document gaps** - What's missing for alpha readiness

### What This Phase is NOT
- NOT final testing (that's Phase 5)
- NOT performance optimization
- NOT feature additions
- NOT "good enough" checking

---

## Phase -1: Infrastructure Verification (MANDATORY)

### Before ANY Testing

**Verify Test Environment**:
```bash
# Check system is running
curl http://localhost:8001/health

# Verify database state
python -c "from services.database import db; print(db.status())"

# Check all integrations
python cli/status.py --verbose

# Verify test data
python scripts/verify_test_data.py
```

**Expected State**:
- Web server running on 8001
- Database connected and migrated
- All Phase 1 integrations active
- Test user accounts exist

**If ANY mismatch**: STOP and fix before proceeding

---

## Phase 0: Test Planning

### Test User Personas

**Alpha User Day 1** (Primary):
- Name: alex-alpha
- Profile: New PM, never used Piper
- Goal: Get value in first session
- Success: Completes onboarding and one real task

**Power User** (Secondary):
- Name: pat-power
- Profile: Expert PM, high expectations
- Goal: Complex workflow automation
- Success: Multi-tool orchestration works

**Edge Case User** (Tertiary):
- Name: eve-edge
- Profile: Breaks everything
- Goal: Find failure modes
- Success: System handles gracefully

---

## Phase 1: User Journey Testing

### Journey 1: Alpha Onboarding (CRITICAL PATH)

**Test Sequence**:
```bash
# Start fresh
rm -rf ~/.piper/alex-alpha/
export PIPER_USER=alex-alpha

# 1. First run
python main.py
# EXPECT: Welcome message, setup wizard launches

# 2. Setup wizard
python main.py setup
# COMPLETE: Each step, note any confusion points

# 3. API key configuration
python main.py keys add --provider openai
# TEST: Invalid key rejection (from #268)
# TEST: Valid key storage

# 4. Preference questionnaire
python main.py preferences
# TEST: All 5 questions work (from #267)
# TEST: Preferences saved to database

# 5. First conversation
python main.py chat "Hello, what can you help me with?"
# TEST: Response reflects preferences (from #269)
# TEST: No errors, smooth interaction

# 6. Document test
echo "Test document content" > test.md
python main.py analyze test.md
# TEST: Upload works
# TEST: Analysis completes
# TEST: Knowledge graph updated (from #278)
```

**Evidence Collection**:
- Screenshot each step
- Note exact error messages
- Time each operation
- Record confusion points

**Acceptance Criteria**:
- [ ] Complete onboarding < 10 minutes
- [ ] No crashes or hangs
- [ ] Clear next steps at each point
- [ ] Preferences affect behavior
- [ ] Document handling works

### Journey 2: Power Workflows

**Test Sequence**:
```bash
export PIPER_USER=pat-power

# 1. Complex query with context
python main.py chat "Review my GitHub issues and create a prioritized list"
# TEST: GitHub integration works
# TEST: Prioritization logic sound

# 2. Multi-tool orchestration
python main.py chat "Schedule standup based on team availability and create agenda from open issues"
# TEST: Calendar integration
# TEST: GitHub integration
# TEST: Orchestration works

# 3. Learning system test
# Repeat similar query 3 times
python main.py chat "Summarize project status"
python main.py chat "What's our project status?"
python main.py chat "Give me a status update"
# TEST: Responses improve/adapt
# TEST: Pattern learning active

# 4. Cost tracking verification
python main.py costs --today
# TEST: Shows actual API usage (from #271)
# TEST: Costs match reality
```

**Acceptance Criteria**:
- [ ] Complex queries handled
- [ ] Multi-tool orchestration works
- [ ] Learning visible
- [ ] Costs tracked accurately

### Journey 3: Edge Cases & Failure Modes

**Test Sequence**:
```bash
export PIPER_USER=eve-edge

# 1. Bad inputs
python main.py chat ""  # Empty
python main.py chat "$(python -c 'print("x"*10000)')"  # Huge
python main.py chat "'; DROP TABLE users; --"  # Injection attempt

# 2. Resource exhaustion
for i in {1..100}; do
  python main.py chat "Test $i" &
done
# TEST: Rate limiting works
# TEST: Graceful degradation

# 3. Integration failures
# Temporarily break each integration
export GITHUB_TOKEN=invalid
python main.py chat "Check my GitHub"
# TEST: Clear error message
# TEST: Fallback behavior

# 4. Preference edge cases
python main.py preferences --set communication_style=invalid
# TEST: Validation works
# TEST: No corruption
```

**Acceptance Criteria**:
- [ ] No crashes on bad input
- [ ] Security boundaries hold
- [ ] Clear error messages
- [ ] Graceful degradation

---

## Phase 2: Integration Testing

### Test Matrix

| Feature | Integration Points | Test Focus | Priority |
|---------|-------------------|------------|----------|
| Preferences | Database, PersonalityProfile, LLM | Bridge works (#269) | HIGH |
| Cost Tracking | LLMClient, Database, Analytics | Accurate capture (#271) | HIGH |
| Knowledge Graph | Graph DB, Intent, Retrieval | Reasoning chains (#278) | HIGH |
| Key Validation | Storage, Providers, Security | Invalid rejection (#268) | MEDIUM |
| Smoke Tests | Pre-commit, Git hooks | Developer flow | LOW |

### Integration Test Commands

```bash
# Preferences → Behavior
python test_integration.py test_preferences_affect_output

# Cost → Database
python test_integration.py test_cost_tracking_persistence

# Graph → Retrieval
python test_integration.py test_graph_first_retrieval

# All together
python test_integration.py test_full_stack
```

---

## Phase 3: Bug Documentation

### Bug Severity Classification

**P0 - BLOCKER**: Cannot proceed to alpha
- Crashes on startup
- Data corruption
- Security vulnerabilities
- Core features broken

**P1 - CRITICAL**: Must fix before alpha
- Major features broken
- Confusing UX blocks progress
- Performance < 5 second response

**P2 - MAJOR**: Should fix if time
- Minor features broken
- Workaround exists
- Polish issues

**P3 - MINOR**: Document for later
- Edge cases
- Nice-to-have improvements
- Future enhancements

### Bug Report Template

```markdown
## Bug #[NUMBER]: [TITLE]

**Severity**: P0/P1/P2/P3
**Component**: [Where it occurs]
**User Impact**: [Who this affects and how]

### Reproduction
1. Step one
2. Step two
3. ERROR: [What happens]

### Expected
[What should happen]

### Evidence
[Terminal output, screenshots]

### Proposed Fix
[If obvious]
```

---

## Phase Z: Testing Complete

### Deliverables Required

1. **Test Results Summary**
```markdown
# Phase 2 Test Results

## Journeys Tested
- [ ] Alpha onboarding: PASS/FAIL
- [ ] Power workflows: PASS/FAIL
- [ ] Edge cases: PASS/FAIL

## Bugs Found
- P0: [count]
- P1: [count]
- P2: [count]
- P3: [count]

## Go/No-Go Recommendation
[Ready for alpha? Or blockers to fix?]
```

2. **Bug Tracker Update**
- Create GitHub issues for all P0/P1 bugs
- Tag appropriately
- Link to test evidence

3. **Documentation Updates**
- Known issues list
- Workarounds documented
- Alpha tester warnings

---

## STOP Conditions

### Stop Testing Immediately If

**Infrastructure Issues**:
- Database corrupted
- Security vulnerability found
- Core services won't start
→ Fix before continuing

**Systematic Failures**:
- Same error in multiple journeys
- Integration completely broken
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
- [ ] Alpha onboarding tested completely
- [ ] Power workflows validated
- [ ] Edge cases explored
- [ ] Evidence collected for each

**All Integrations**:
- [ ] Preferences → behavior verified
- [ ] Costs → tracking verified
- [ ] Graph → retrieval verified
- [ ] Keys → validation verified

**All Bugs**:
- [ ] Documented with reproduction steps
- [ ] Classified by severity
- [ ] P0/P1 issues created in GitHub
- [ ] Fix/defer decision made

**Documentation**:
- [ ] Test results summarized
- [ ] Known issues updated
- [ ] Go/no-go recommendation clear

---

## Handoff to Phase 3

### What Phase 3 Needs From Us
- List of P0/P1 bugs to fix
- Testing gaps identified
- User journey pain points
- Performance baselines

### What We're NOT Handing Off
- Feature requests (→ MVP backlog)
- P2/P3 bugs (→ documented only)
- Performance optimization (→ post-alpha)
- UI polish (→ later)

---

## Session Management

### During Testing
- Keep terminal output
- Screenshot everything
- Note timing for each operation
- Document confusion points

### Evidence Format
```bash
# Terminal evidence
$ command_executed
[FULL OUTPUT INCLUDED]
# Time: X seconds
# Result: PASS/FAIL
# Notes: [observations]
```

### Session Log Updates
Every 30 minutes:
- Update progress
- Note findings
- Check time box

---

## Remember

**This is Phase 2 of 5**. After this:
- Phase 3: Baseline Piper Education
- Phase 4: Documentation (polish drafts)
- Phase 5: Alpha deployment preparation

**We are NOT done** when testing completes. Sprint A8 continues.

**Inchworm Protocol**: Complete Phase 2 100% before moving to Phase 3.

---

*Lead Developer: This is your testing charter. Execute systematically, document thoroughly, and remember - finding bugs now saves alpha tester frustration later.*
