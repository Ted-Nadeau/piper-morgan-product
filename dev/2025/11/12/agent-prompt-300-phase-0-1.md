# Claude Code Agent Prompt: Implement Basic Auto-Learning (#300)

## Your Identity
You are Claude Code, a specialized development agent working on the Piper Morgan project. You follow systematic methodology and provide evidence for all claims.

## Essential Context
Read these briefing documents first in docs/briefing/:
- BRIEFING-ESSENTIAL-AGENT.md - Your role requirements
- BRIEFING-CURRENT-STATE.md - Current epic and focus (Sprint A8)
- BRIEFING-METHODOLOGY.md - Inchworm Protocol and verification requirements

---

## 🏛️ STRATEGIC CONTEXT: The Cathedral Foundation

### This Is Foundation Stone #1
- **Level 1: Basic Auto-Learning** ← **THIS PROMPT**
- Real-time pattern detection from individual users
- Confidence-based suggestions (>0.7)
- User-controlled learning
- **All future learning depends on getting this right**

### Philosophy
- **Time Lord**: Quality over speed - build it right
- **Building in Public**: Transparent, user-controlled learning
- **Methodology-Driven**: Learns PM best practices
- **Human-AI Collaboration**: Suggestions, not black-box automation

**This is not just "make it auto"** - it's **"lay the foundation for the cathedral"**

---

## 🛠️ INFRASTRUCTURE VERIFICATION (MANDATORY FIRST ACTION)

### Phase -1: Verify Sprint A5 Deliverables FIRST

**Before doing ANYTHING else, verify these exist**:

```bash
# Check Learning Handler exists
ls -la services/learning/
# Expected: Directory with learning_handler.py or similar

# Check database models
grep -r "LearnedPattern" services/ --include="*.py"
# Expected: Model definition with fields: pattern_id, user_id, confidence, etc.

# Check Pattern-026 documentation
ls -la patterns/ | grep -i learning
cat patterns/pattern-026-cross-feature-learning.md
# Expected: Architecture documentation exists

# Check orchestration integration points
grep -r "orchestration" services/ --include="*.py"
ls -la services/orchestration/
# Expected: orchestration_engine.py or similar

# Check what's currently running
ps aux | grep python
ps aux | grep piper
```

**Expected Sprint A5 Infrastructure**:
- ✅ `services/learning/` directory exists
- ✅ `LearnedPattern` model defined with confidence tracking
- ✅ `patterns/pattern-026-cross-feature-learning.md` documented
- ✅ Orchestration engine accessible
- ✅ Pattern types defined (6 types)
- ✅ Database schema matches gameplan

**STOP Conditions**:
- ❌ Sprint A5 deliverables missing
- ❌ Database schema doesn't match expected structure
- ❌ Orchestration engine doesn't support hooks
- ❌ Learning Handler missing or incomplete

**If reality doesn't match expectations**:
1. **STOP immediately**
2. **Report the mismatch** with evidence (show `ls`, `grep` outputs)
3. **Wait for revised gameplan**

**Evidence Required**: Provide terminal outputs showing all components present

---

## Session Log Management

**IMPORTANT**: Check for existing log before creating new one!

```bash
# Check if you already have a log today
ls -la dev/$(date +%Y/%m/%d)/$(date +%Y-%m-%d)-*-code-*-log.md
```

**If NO log exists**: Create new log:
- Format: `dev/YYYY/MM/DD/YYYY-MM-DD-HHMM-code-agent-log.md`

**If log EXISTS**: DO NOT create new log!
- Append new section to existing log
- Format: `## Session [N]: Issue #300 ([Time])`
- Include `---` between sessions

---

## Mission

**Implement Basic Auto-Learning (#300)**: Real-time pattern detection and application with user-controlled personalization for Alpha testing.

**Scope for This Prompt**:
- Phase -1: Infrastructure Verification
- Phase 0: Wire Learning Handler to Orchestration
- Phase 1: Implement Core Learning Cycle
- **NOT in this prompt**: Phases 2-6 (separate prompts after Phase 1 verified)

**Success Target**: User actions automatically captured, patterns detected in real-time, confidence calculated based on outcomes.

---

## Context

### GitHub Issue
- **Issue**: #300 - CORE-ALPHA-LEARNING-BASIC
- **Priority**: P2 (Alpha Feature)
- **Milestone**: Sprint A8 or A9
- **Labels**: `learning`, `alpha`, `foundation`, `intelligence`
- **Related**: Sprint A5 (Learning Infrastructure), Pattern-026

### Current State
- Sprint A5 completed learning infrastructure
- Database models exist
- Learning Handler service layer operational
- Pattern-026 architecture documented
- **Gap**: Handler not wired to orchestration, no real-time learning

### Target State
- Learning Handler integrated into orchestration pipeline
- Real-time pattern capture working
- Confidence updates based on outcomes
- Pattern similarity detection (no duplicates)
- Foundation ready for user controls (Phase 2)

### Dependencies
- Sprint A5 deliverables (must verify exist)
- Orchestration pipeline (must support hooks)
- Database schema (must match LearnedPattern model)
- Intent classification system (provides action types)

### User Data Risk
- **LOW** - This phase doesn't touch user configuration
- Patterns stored per-user in database
- No changes to existing user data

### Infrastructure Verified
- **NO - Must verify in Phase -1**
- This is your FIRST action

---

## 📋 GAMEPLAN ATTACHMENT

**Full Gameplan**: `/mnt/user-data/uploads/gameplan-300-learning-basic-revised.md`

**You are implementing**: Phase -1, Phase 0, Phase 1 only

**Key Architectural Decisions**:

1. **Confidence Thresholds**:
   - Suggestion: 0.7 (show to user)
   - Automation: 0.9 (apply automatically)
   - Disable: <0.3 (turn off)

2. **Integration Point**: Orchestration Pipeline
   ```
   Intent → Orchestration → [LEARNING CAPTURE] → Execute → [OUTCOME RECORD] → Response
   ```

3. **Confidence Formula**:
   ```python
   confidence = (success_rate * 0.8 + previous_confidence * 0.2) * volume_factor
   # volume_factor = min(usage_count / 10, 1.0)
   ```

4. **Performance Targets**:
   - Pattern capture: <10ms
   - Confidence update: <5ms
   - Total overhead: <20ms per request

---

## Evidence Requirements (CRITICAL)

### For EVERY Claim You Make:

**"Infrastructure verified"** → Show terminal outputs:
```bash
$ ls -la services/learning/
$ grep -r "LearnedPattern" services/
$ cat patterns/pattern-026-cross-feature-learning.md | head -20
```

**"Wired to orchestration"** → Show code + logs:
```bash
$ grep -A10 "learning_handler.capture_action" services/orchestration/
$ # Make test request, show logs
$ curl -X POST http://localhost:8001/api/chat -d '{"message": "test"}'
$ # Show learning handler was called in logs
```

**"Pattern capture working"** → Show database entry:
```bash
$ # After test action
$ psql -U piper -d piper_db -c "SELECT * FROM learned_patterns LIMIT 5;"
$ # Show pattern was created with correct fields
```

**"Confidence updates"** → Show before/after:
```bash
$ # Query pattern before
$ psql ... -c "SELECT confidence FROM learned_patterns WHERE id='xxx';"
0.50
$ # Record successful outcome
$ # Query pattern after
$ psql ... -c "SELECT confidence FROM learned_patterns WHERE id='xxx';"
0.68
```

**"Tests pass"** → Show pytest output:
```bash
$ pytest tests/learning/test_pattern_capture.py -v
===== 3 passed in 0.15s =====
```

**"Committed changes"** → Show git log:
```bash
$ git log --oneline -1
abc1234 feat(#300): Wire learning handler to orchestration pipeline
```

### Completion Bias Prevention:
- **Never guess! Always verify first!**
- **NO "should work"** - only "here's proof it works"
- **NO assumptions** - only verified facts
- Show actual terminal outputs, not expected outputs

---

## Constraints & Requirements

### MANDATORY Requirements

1. **Infrastructure Verified FIRST**: Phase -1 must complete before any code changes
2. **100% Method Compatibility**: No partial implementations
3. **Check Existing First**: Search for existing learning code before creating
4. **Preserve User Data**: Never delete user configuration
5. **GitHub Tracking**: Update issue #300 with progress
6. **Evidence Required**: Every claim needs terminal proof
7. **Stop Conditions**: Stop immediately if any trigger occurs
8. **Session Log**: Must be .md format, append if exists

### Code Quality Standards

**Testing**:
- Unit tests for each method
- Integration tests for full cycle
- Real database (no mocks for integration)
- Transaction rollback for test isolation

**Architecture**:
- Follow DDD patterns (Pattern-008)
- Async/await properly (Pattern-007)
- No circular dependencies
- Clear layer boundaries

**Performance**:
- <10ms pattern capture
- <5ms confidence update
- Async storage (no user wait)
- Benchmark against targets

---

## 🚨 ANTI-80% COMPLETION SAFEGUARDS

### When Implementing Learning Handler Integration:

**1. Create Verification Table FIRST**:
```
Required Methods      | Status | Evidence
--------------------- | ------ | --------
capture_action()      | [ ]    |
record_outcome()      | [ ]    |
get_suggestions()     | [ ]    |
update_confidence()   | [ ]    |
find_similar_pattern()| [ ]    |

TOTAL: 0/5 = 0% - Starting
```

**2. ZERO AUTHORIZATION to skip methods**:
- Cannot skip "optional" methods
- Cannot rationalize gaps
- Cannot decide what's "core" vs "extra"

**3. Objective Completion Required**:
- Show exact count: "5/5 methods = 100%"
- Not subjective: "looks complete"
- Only acceptable: "X/X = 100% VERIFIED"

**4. STOP if <100%**:
- If any method missing, STOP and report

---

## Implementation Phases

### Phase -1: Infrastructure Verification (15-30 minutes)

**Goal**: Confirm Sprint A5 deliverables exist and match gameplan expectations

**Tasks**:
1. Run verification commands (see Infrastructure Verification section above)
2. Check each expected component
3. Document what exists
4. Compare to gameplan assumptions
5. Report any mismatches

**STOP Conditions**:
- Any Sprint A5 deliverable missing
- Database schema doesn't match
- Orchestration can't support hooks
- Pattern-026 documentation missing

**Evidence Required**:
```bash
# Provide ALL these outputs:
$ ls -la services/learning/
$ grep -r "LearnedPattern" services/
$ cat patterns/pattern-026-cross-feature-learning.md | head -30
$ ls -la services/orchestration/
$ grep "class.*Engine" services/orchestration/*.py
```

**Deliverables**:
- [ ] Verification report with terminal outputs
- [ ] List of confirmed components
- [ ] Any mismatches documented
- [ ] Decision: PROCEED or STOP

---

### Phase 0: Wire Learning Handler (1-2 hours)

**Goal**: Connect Learning Handler to orchestration pipeline for action capture and outcome recording

**Prerequisites**: Phase -1 complete, infrastructure verified

**Implementation Steps**:

**Step 0.1: Locate Orchestration Entry Point** (15 min):
```bash
# Find main request handler
grep -r "process.*request\|handle.*request" services/orchestration/ --include="*.py"

# Identify integration points
# Should be: before execution, after execution
```

**Step 0.2: Add Learning Hooks** (30 min):
```python
# services/orchestration/orchestration_engine.py (or similar)

async def process_request(user_input, user_id, session):
    """Process user request with learning integration"""

    # Existing: Intent classification
    intent = await classify_intent(user_input)

    # NEW: Capture action for learning
    await learning_handler.capture_action(
        user_id=user_id,
        action_type=intent.category,
        context={
            "intent": intent.category,
            "input": user_input,
            "timestamp": datetime.utcnow()
        },
        session=session
    )

    # Existing: Execute action
    result = await execute_intent(intent, user_id, session)

    # NEW: Record outcome
    await learning_handler.record_outcome(
        user_id=user_id,
        action_type=intent.category,
        success=result.success,
        session=session
    )

    # NEW: Get pattern suggestions (for later phases)
    # suggestions = await learning_handler.get_suggestions(...)

    return result
```

**Step 0.3: Verify Integration** (15 min):
```bash
# Check imports work
python -c "from services.orchestration.orchestration_engine import *; print('OK')"

# Syntax check
python -m py_compile services/orchestration/orchestration_engine.py
```

**Step 0.4: Test End-to-End** (30 min):
```bash
# Start server (if not running)
python main.py &

# Make test request
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "create a test issue", "user_id": "test-user"}'

# Check learning handler was called (check logs)
tail -n 50 logs/piper.log | grep -i learning

# Check database for captured pattern
psql -U piper -d piper_db -c "SELECT * FROM learned_patterns WHERE user_id='test-user';"
```

**STOP Conditions**:
- Orchestration errors with learning hooks
- Performance >50ms overhead
- Learning handler not being called
- Database errors on pattern capture

**Evidence Required**:
```bash
# Show integration code
$ grep -A20 "learning_handler.capture_action" services/orchestration/orchestration_engine.py

# Show handler being called
$ curl -X POST ... (request)
$ tail -n 30 logs/piper.log  # Show learning logs

# Show pattern in database
$ psql ... -c "SELECT * FROM learned_patterns;"

# Show performance
$ time curl -X POST ...  # Should be <100ms total
```

**Deliverables**:
- [ ] Learning hooks in orchestration code
- [ ] Syntax validated
- [ ] End-to-end test showing patterns captured
- [ ] Performance within targets
- [ ] Git commit with evidence

---

### Phase 1: Implement Core Learning Cycle (2-3 hours)

**Goal**: Pattern capture, confidence updates, similarity detection working

**Prerequisites**: Phase 0 complete, hooks verified working

**Components to Build**:

**1.1: Pattern Capture** (30-45 min):

Location: `services/learning/learning_handler.py` (or appropriate file)

```python
async def capture_action(
    user_id: UUID,
    action_type: str,
    context: Dict[str, Any],
    session: AsyncSession
):
    """Capture user action for pattern learning"""

    # Extract pattern features
    pattern_data = {
        "action_type": action_type,
        "context": context,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Find similar existing pattern
    similar = await find_similar_pattern(
        user_id=user_id,
        pattern_data=pattern_data,
        similarity_threshold=0.8,
        session=session
    )

    if similar:
        # Update existing pattern
        similar.usage_count += 1
        similar.last_used_at = datetime.utcnow()
    else:
        # Create new pattern
        pattern = LearnedPattern(
            pattern_id=uuid4(),
            user_id=user_id,
            pattern_type=determine_pattern_type(action_type),
            pattern_data=pattern_data,
            confidence=0.5,  # Start neutral
            usage_count=1,
            success_count=0,
            failure_count=0,
            enabled=True
        )
        session.add(pattern)

    await session.commit()
```

**Test 1.1**:
```bash
# Unit test
pytest tests/learning/test_pattern_capture.py::test_first_pattern_created -v

# Integration test
python -c "
from services.learning.learning_handler import capture_action
# ... run capture_action
# ... check database
"
```

**1.2: Outcome Recording** (30-45 min):

```python
async def record_outcome(
    user_id: UUID,
    action_type: str,
    success: bool,
    session: AsyncSession
):
    """Update pattern confidence based on outcome"""

    # Find most recent pattern for this action
    result = await session.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.pattern_data['action_type'].astext == action_type
        )
        .order_by(LearnedPattern.last_used_at.desc())
        .limit(1)
    )
    pattern = result.scalar_one_or_none()

    if not pattern:
        return  # No pattern to update

    # Update counts
    if success:
        pattern.success_count += 1
    else:
        pattern.failure_count += 1

    # Recalculate confidence
    pattern.update_confidence()

    # Disable if too low
    if pattern.confidence < 0.3:
        pattern.enabled = False

    await session.commit()
```

**1.3: Confidence Calculation** (30 min):

Add method to `LearnedPattern` model:

```python
def update_confidence(self):
    """Calculate confidence from success/failure rates"""

    total = self.success_count + self.failure_count
    if total == 0:
        return  # No outcomes yet

    # Success rate (0.0 - 1.0)
    success_rate = self.success_count / total

    # Volume factor (more uses = more confidence, caps at 10)
    volume_factor = min(self.usage_count / 10, 1.0)

    # Weighted: 80% current success, 20% previous confidence
    new_confidence = (success_rate * 0.8 + self.confidence * 0.2)

    # Apply volume factor
    self.confidence = new_confidence * volume_factor

    self.last_updated_at = datetime.utcnow()
```

**1.4: Similarity Detection** (45-60 min):

```python
async def find_similar_pattern(
    user_id: UUID,
    pattern_data: Dict[str, Any],
    similarity_threshold: float,
    session: AsyncSession
) -> Optional[LearnedPattern]:
    """Find existing similar pattern to avoid duplicates"""

    # Get all user's enabled patterns
    result = await session.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.enabled == True
        )
    )

    for pattern in result.scalars():
        # Calculate similarity
        similarity = calculate_similarity(
            pattern.pattern_data,
            pattern_data
        )

        if similarity >= similarity_threshold:
            return pattern

    return None


def calculate_similarity(data1: Dict, data2: Dict) -> float:
    """Calculate similarity between two patterns (0.0 - 1.0)"""

    # Compare action type (most important)
    if data1.get("action_type") != data2.get("action_type"):
        return 0.0  # Different actions = not similar

    # Compare context keys
    context1 = data1.get("context", {})
    context2 = data2.get("context", {})

    # Simple implementation: check key overlap
    keys1 = set(context1.keys())
    keys2 = set(context2.keys())

    if not keys1 or not keys2:
        return 0.8  # Same action, minimal context = fairly similar

    # Jaccard similarity
    intersection = len(keys1 & keys2)
    union = len(keys1 | keys2)

    return (intersection / union) if union > 0 else 0.0
```

**Phase 1 Testing**:

```bash
# Unit tests
pytest tests/learning/test_pattern_capture.py -v
pytest tests/learning/test_confidence.py -v
pytest tests/learning/test_similarity.py -v

# Integration test
pytest tests/learning/test_learning_cycle_integration.py -v
```

**STOP Conditions**:
- Any unit test fails
- Integration test fails
- Pattern capture not working
- Confidence calculation incorrect
- Similarity detection broken
- Performance >10ms per operation

**Evidence Required**:
```bash
# Show implementations exist
$ ls -la services/learning/learning_handler.py
$ wc -l services/learning/learning_handler.py

# Show methods implemented
$ grep "^async def\|^def" services/learning/learning_handler.py

# Method completeness table
Required Methods       | Implemented | Evidence
---------------------- | ----------- | --------
capture_action()       | ✅          | Line 45
record_outcome()       | ✅          | Line 78
update_confidence()    | ✅          | Line 112
find_similar_pattern() | ✅          | Line 145
calculate_similarity() | ✅          | Line 178
TOTAL: 5/5 = 100% COMPLETE

# Show tests pass
$ pytest tests/learning/ -v
===== 8 passed in 0.42s =====

# Show integration works
$ # Make 3 test requests
$ psql ... -c "SELECT pattern_id, usage_count, confidence FROM learned_patterns;"
<show pattern with usage_count=3, confidence increased>

# Show git commit
$ git log --oneline -1
xyz7890 feat(#300): Implement core learning cycle (capture, confidence, similarity)
```

**Deliverables**:
- [ ] Pattern capture implemented
- [ ] Outcome recording implemented
- [ ] Confidence calculation working
- [ ] Similarity detection working
- [ ] Method completeness: 5/5 = 100%
- [ ] All unit tests passing
- [ ] Integration test passing
- [ ] Performance targets met
- [ ] Git commit with evidence

---

## Success Criteria (Phases -1, 0, 1)

- [ ] Infrastructure verified (Phase -1 complete with evidence)
- [ ] Learning Handler wired to orchestration (Phase 0)
- [ ] Real-time pattern capture working (Phase 1)
- [ ] Confidence updates based on outcomes (Phase 1)
- [ ] Pattern similarity detection (no duplicates) (Phase 1)
- [ ] Method completeness: 5/5 = 100%
- [ ] All tests passing (show pytest output)
- [ ] Performance <20ms overhead total
- [ ] GitHub issue #300 updated with progress
- [ ] Evidence provided for each claim
- [ ] Git commits clean (show log)
- [ ] Database contains test patterns (show query)

---

## Cross-Validation Preparation

**For the next agent (Cursor) to verify**:

**What to Check**:
1. Learning Handler integrated into orchestration: `grep "learning_handler" services/orchestration/`
2. Pattern capture working: Make test request, check database
3. Confidence updates working: Record success/failure, check confidence changed
4. Similarity detection working: Create similar patterns, verify merged not duplicated
5. Performance: Time requests, should be <100ms total

**Commands to Run**:
```bash
# Check integration
grep -r "learning_handler" services/orchestration/

# Test pattern capture
curl -X POST http://localhost:8001/api/chat -d '{"message": "test"}'
psql -U piper -d piper_db -c "SELECT * FROM learned_patterns;"

# Test confidence updates
# (requires multiple requests with success/failure outcomes)

# Check performance
time curl -X POST http://localhost:8001/api/chat -d '{"message": "test"}'
```

**Expected Outputs**:
- Pattern in database after request
- Confidence changes with outcomes
- Similar patterns merged (usage_count increments)
- Response time <100ms

**Assumptions Made**:
- (Should be NONE - if any, list here)

---

## Self-Check Before Claiming Complete

Ask yourself:
1. ✅ Did I verify infrastructure in Phase -1 FIRST?
2. ✅ Is my method implementation 100% complete (5/5)?
3. ✅ Did I provide terminal evidence for every claim?
4. ✅ Do all tests pass (unit + integration)?
5. ✅ Is performance within targets (<20ms)?
6. ✅ Can another agent verify my work independently?
7. ✅ Did I update GitHub issue #300 with progress?
8. ✅ Are my git commits clean with evidence?
9. ✅ Did I check what's actually running (ps aux)?
10. ✅ Am I guessing or do I have evidence?

**If uncertain**: Run verification yourself, show actual output, never guess!

---

## STOP Conditions (17 Total)

If ANY occur, STOP and report:

1. Infrastructure doesn't match gameplan
2. Method implementation <100% (must be 5/5)
3. Tests fail (any test)
4. Configuration assumptions needed
5. GitHub issue #300 missing or unassigned
6. Can't provide verification evidence
7. Performance >20ms overhead
8. Database errors on pattern operations
9. Orchestration errors with hooks
10. User data at risk
11. Completion bias detected (claiming without proof)
12. Rationalizing gaps as "minor"
13. Git operations failing
14. Server state unexpected
15. Can't show actual running behavior
16. Similarity detection broken
17. Confidence calculation incorrect

---

## When Tests Fail (YOU DO NOT DECIDE)

**If ANY test fails**:

1. **STOP immediately**
2. **Do NOT decide** if failure is "critical"
3. **Do NOT rationalize**

**Instead, report**:
```
⚠️ STOP - Tests Failing

Failing: [X] tests
Passing: [Y] tests

Exact errors:
[paste error output]

Root cause (if known):
[your diagnosis]

Options:
1. [fix approach]
2. [alternative approach]
3. [skip with approval]

Awaiting PM decision.
```

---

## Deliverables

**Phase -1**:
- Infrastructure verification report with terminal outputs
- List of confirmed components
- Any mismatches documented

**Phase 0**:
- Learning Handler integration code
- End-to-end test evidence
- Performance benchmark
- Git commit

**Phase 1**:
- Complete learning cycle implementation
- Method completeness table (5/5 = 100%)
- Unit test results
- Integration test results
- Database queries showing patterns
- Git commit

**All Phases**:
- Session log with progress
- GitHub issue #300 updated
- Evidence for every claim
- Cross-validation prep notes

---

## Related Documentation

**MUST READ**:
- `gameplan-300-learning-basic-revised.md` - Full gameplan
- `patterns/pattern-026-cross-feature-learning.md` - Architecture
- `BRIEFING-METHODOLOGY.md` - Verification requirements

**Reference**:
- `architectural-guidelines.md` - DDD patterns
- `pattern-007-async-error-handling.md` - Async patterns
- `pattern-001-repository.md` - Repository pattern
- `tdd-pragmatic-approach.md` - Testing guidance

---

## REMINDER: You Are Building A Cathedral

**Foundation Stone #1**: All future learning depends on this
- Build it exceptionally well
- Don't rush to claim complete
- Verify every single claim
- 100% method completeness required
- Evidence for everything

**Time Lord Philosophy**: Quality exists outside time constraints

**Inchworm Protocol**: One solid step at a time
- Phase -1 complete? Evidence?
- Phase 0 complete? Evidence?
- Phase 1 complete? Evidence?

**Never Guess - Always Verify First!**

---

## 🎯 Final Reminder

**This prompt covers ONLY**:
- Phase -1: Infrastructure Verification
- Phase 0: Wire Learning Handler
- Phase 1: Core Learning Cycle

**NOT in scope** (separate prompts later):
- Phase 2: User Controls
- Phase 3: Feedback Loop
- Phase 4: Pattern Application
- Phase 5: Integration Testing
- Phase 6: Manual Testing & Polish

**After completing Phases -1, 0, 1**:
1. Compile evidence package
2. Update GitHub issue #300
3. Report completion to PM
4. STOP and wait for Phase 2-6 prompt

---

**Status**: Ready for Agent Deployment
**Issue**: #300 - CORE-ALPHA-LEARNING-BASIC
**Scope**: Phase -1, 0, 1 (Infrastructure + Wiring + Core Cycle)
**Effort**: 3-6 hours estimated
**Priority**: P2 (Alpha Feature)

---

_"Part of a cathedral, not just a random brick shed"_
_"Quality exists outside of time constraints"_
_"Never guess - always verify first!"_
