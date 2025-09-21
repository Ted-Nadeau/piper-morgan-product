# The Great Refactor: Inchworm Roadmap
**Created**: September 19, 2025
**Purpose**: Sequential execution plan for architectural restoration
**Philosophy**: Complete each epic 100% before moving to next

---

## 🐛 The Inchworm Protocol

**RULE**: Cannot start next epic until current is 100% complete, tested, and documented. NO EXCEPTIONS.

Each epic follows this pattern:
1. **Fix** the broken system
2. **Test** comprehensively
3. **Lock** with tests that prevent regression
4. **Document** what was done and why
5. **Verify** with core user story

---

## 📍 Current Location: ALL STOP - Architectural Review

### What We Know
- QueryRouter disabled but 75% complete (PM-034)
- OrchestrationEngine never initialized
- Multiple unfinished refactors creating confusion
- Core user story (GitHub issue creation) must work

---

## 🗺️ The Great Refactor Sequence

### REFACTOR-1: Orchestration Core (2 weeks)
**Why First**: Unlocks everything else - this is the heart

**Scope**:
- [ ] Review PM-034 QueryRouter implementation
- [ ] Fix initialization in main.py/web/app.py
- [ ] Initialize OrchestrationEngine properly
- [ ] Remove workarounds and TODO comments
- [ ] Test GitHub issue creation end-to-end

**Success Criteria**:
- "Create GitHub issue about X" works from chat
- No "None" objects or undefined errors
- Performance <500ms for issue creation
- All tests pass

**Lock Strategy**:
- Integration test for GitHub issue flow
- Unit tests for QueryRouter
- Unit tests for OrchestrationEngine
- No TODO comments remain

---

### REFACTOR-2: Integration Cleanup (1 week)
**Why Second**: Cleans up dual patterns before extraction

**Scope**:
- [ ] Remove old GitHub service patterns
- [ ] Single flow through OrchestrationEngine
- [ ] Fix configuration validation
- [ ] Fix 28 broken documentation links
- [ ] Update Excellence Flywheel docs

**Success Criteria**:
- Only one way to call GitHub
- Config validated automatically
- Zero broken links
- All agents follow methodology

**Lock Strategy**:
- Remove old import paths
- Config validation in CI
- Link checker in CI
- Methodology in agent configs

---

### REFACTOR-3: Plugin Architecture (2 weeks)
**Why Third**: Now that integrations are clean, extract them

**Scope**:
- [ ] Define plugin interface (simple)
- [ ] Extract GitHub to plugin
- [ ] Extract Slack to plugin
- [ ] Extract Notion to plugin
- [ ] Test all integrations still work

**Success Criteria**:
- Each integration is a separate module
- Core doesn't import integration code
- Plugins can be disabled/enabled
- All existing features still work

**Lock Strategy**:
- Plugin interface tests
- Integration tests per plugin
- Core isolation tests
- Dynamic loading works

---

### REFACTOR-4: Intent Universalization (1 week)
**Why Fourth**: With plugins done, ensure consistent entry

**Scope**:
- [ ] All endpoints route through intent
- [ ] Remove any direct endpoint calls
- [ ] Test every user flow
- [ ] Document intent patterns

**Success Criteria**:
- No way to bypass intent layer
- Every user input classified
- Consistent behavior across entry points
- Intent docs complete

**Lock Strategy**:
- Remove direct endpoints
- Intent required in API
- Test coverage 100%
- No bypass possible

---

### REFACTOR-5: Validation & Quality (1 week)
**Why Last**: Can't meaningfully test until system works

**Scope**:
- [ ] Full integration test suite
- [ ] Performance benchmarks
- [ ] Staging deployment
- [ ] Monitoring setup

**Success Criteria**:
- All user flows have tests
- Performance meets targets
- Staging environment works
- Monitoring dashboards live

**Lock Strategy**:
- CI runs all tests
- Performance gates in CI
- Staging required for merge
- Alerts configured

---

## 📊 Progress Tracking

### Current Status
```
[🔴] REFACTOR-1: Not Started (0%)
[⚫] REFACTOR-2: Blocked
[⚫] REFACTOR-3: Blocked
[⚫] REFACTOR-4: Blocked
[⚫] REFACTOR-5: Blocked
```

### Success Metrics
- Epic Completion Rate: 0/5
- Test Coverage: TBD
- Performance: TBD
- User Story Success: 0/5

---

## 🎯 North Star

**The GitHub Issue Creation Flow Must Work**

This is our "Hello World". If this doesn't work, nothing else matters. Every refactor is validated against this core user story.

---

## 🚫 What We're NOT Doing

1. **No new features** until refactors complete
2. **No partial implementations** - finish what you start
3. **No workarounds** - fix the real problem
4. **No skipping tests** - they lock in the fix
5. **No parallel work** - strict sequential execution

---

## 📅 Realistic Timeline

- **REFACTOR-1**: 2 weeks (Oct 3)
- **REFACTOR-2**: 1 week (Oct 10)
- **REFACTOR-3**: 2 weeks (Oct 24)
- **REFACTOR-4**: 1 week (Oct 31)
- **REFACTOR-5**: 1 week (Nov 7)

**Total: 7 weeks** to architectural stability

Then we can build features on solid foundation.

---

## 🔗 Key Documents

- PM-034-queryrouter-integration.md - The interrupted work
- PM-034-integration-strategy.md - The original plan
- architecture.md - Current system design
- INCOMPLETE_WORK_ANALYSIS.md - What's unfinished

---

## ✅ Daily Checklist

Before starting work each day:
1. Which REFACTOR epic am I on?
2. What's the next unchecked box?
3. Will this help GitHub issue creation work?
4. Am I finishing or starting?

If starting when not finished: STOP.

---

*Remember: We're not building new things. We're finishing what we started.*
