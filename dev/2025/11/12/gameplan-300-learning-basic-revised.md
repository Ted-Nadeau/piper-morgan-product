# Gameplan: CORE-ALPHA-LEARNING-BASIC
## Implement Basic Auto-Learning (Foundation Stone #1)

**Issue**: #300 - CORE-ALPHA-LEARNING-BASIC
**Date**: November 12, 2025
**Author**: Chief Architect (revised from Lead Developer draft)
**Status**: Ready for Agent Implementation
**Estimated Effort**: Medium (1-2 day effort)
**Priority**: P2 (Alpha Feature)

---

## Strategic Context: The Cathedral Foundation

### The Four-Level Roadmap

**Level 1: Basic Auto** ← **THIS GAMEPLAN** 🎯
- Real-time pattern detection from individual users
- Confidence-based suggestions (>0.7)
- User-controlled learning
- **Foundation for all future learning**

**Level 2: Enhanced Auto** ← Post-MVP (if users request)
- Better algorithms, more pattern types
- Evaluate after Level 1 feedback
- **Don't build until demand proven**

**Level 3: Collaborative** ← Enterprise (if user base >50)
- Team pattern sharing
- Wait for critical mass
- **Requires solid Level 1 foundation**

**Level 4: Predictive** ← Probably never
- ML-driven anticipation
- Too risky/costly
- **Skip or partner**

### Why This Matters

**Time Lord Philosophy**: Quality exists outside time constraints - build it right
**Building in Public**: Transparent, user-controlled learning
**Methodology-Driven**: Learns PM best practices, not just automation
**Human-AI Collaboration**: Suggestions, not black-box decisions

**This is not just "make it auto"** - it's **"lay the foundation for the cathedral"**

---

## Problem Statement

**Current**: Learning operates manually with 3-4 week lag
**Goal**: Real-time learning with minutes-to-hours lag
**Value**: Personalization + differentiation vs competitors
**Risk**: Low (mitigatable with confidence thresholds)

---

## What Already Exists (Sprint A5)

### Infrastructure from Sprint A5 ✅
1. **Pattern-026 Architecture**: Documented framework
2. **Database Models**: `LearnedPattern` with confidence tracking
3. **Learning Handler**: Service layer operational
4. **Pattern Types**: 6 types defined
5. **Pattern Sweep**: Standalone tool (continues for codebase patterns)

### What's Missing ❌
1. Learning Handler not wired to orchestration pipeline
2. Real-time confidence updates not implemented
3. User feedback loop doesn't exist
4. Pattern suggestions/application not working
5. User controls not implemented

**Gap**: Infrastructure exists, but not connected to main workflow

---

## Architectural Decisions

### Decision 1: Confidence Thresholds ✅

**Thresholds**:
- **Suggestion**: 0.7 (show to user, let them confirm)
- **Automation**: 0.9 (apply automatically, notify user)
- **Disable**: <0.3 (too low confidence, turn off)

**Rationale**:
- 0.7 is high enough to avoid noise, low enough to learn quickly
- 0.9 ensures high confidence before automation
- 0.3 prevents bad patterns from persisting

**Alternative Rejected**: Single threshold (0.8) - too rigid

---

### Decision 2: Learning Cycle Integration ✅

**Integration Point**: Orchestration Pipeline

```
User Input → Intent → Orchestration → [LEARNING HANDLER] → Execute → [LEARNING HANDLER] → Response
                                        ↑ Capture Action            ↑ Record Outcome
```

**Why Orchestration?**:
- Central flow point (all requests pass through)
- Has user context available
- Can intercept before and after execution

**Alternative Rejected**: Separate learning service - adds latency

---

### Decision 3: Confidence Calculation ✅

**Formula**:
```python
confidence = (success_rate * 0.8 + previous_confidence * 0.2) * volume_factor
```

**Components**:
- Success rate: Recent performance (80% weight)
- Previous confidence: Stability (20% weight)
- Volume factor: More usage = higher confidence (caps at 10 uses)

**Enhancement**: Add time-based decay
```python
effective_confidence = confidence * (0.95 ** days_since_last_use)
```

---

### Decision 4: Pattern Storage Strategy ✅

**Storage**: Per-user patterns only (Level 1 scope)

**Schema**:
```python
class LearnedPattern:
    pattern_id: UUID
    user_id: UUID
    pattern_type: PatternType
    pattern_data: JSON
    confidence: float
    usage_count: int
    success_count: int
    failure_count: int
    enabled: bool
```

**Future-Proof**: Can add team patterns in Level 3 without schema changes

---

### Decision 5: Performance Targets ✅

**Targets**:
- Pattern capture: <10ms
- Confidence update: <5ms
- Pattern suggestion: <1ms (cached)
- Total overhead: <20ms per request

**Mitigation**:
- Async pattern storage (no user wait)
- Cached pattern lookups
- Background confidence calculations

---

### Decision 6: Testing Strategy ✅

**Three-Tier Verification**:
1. **Unit Tests**: Pattern logic in isolation
2. **Integration Tests**: Full cycle with real DB
3. **Manual Tests**: User experience validation

**No Mocks for Integration**: Real database, transaction rollback

---

## Implementation Phases

### Phase -1: Infrastructure Verification
**Effort**: Small (quick checks)

**Verify Sprint A5 Deliverables**:
```bash
# Check Learning Handler exists
ls -la services/learning/

# Check database models
grep -r "LearnedPattern" services/

# Check Pattern-026 documentation
cat patterns/pattern-026-cross-feature-learning.md

# Check orchestration integration points
grep -r "orchestration_engine" services/
```

**Expected**:
- ✅ Learning service directory exists
- ✅ LearnedPattern model defined
- ✅ Pattern-026 documented
- ✅ Orchestration engine accessible

**STOP Conditions**:
- ❌ Sprint A5 deliverables missing
- ❌ Database schema doesn't match expected
- ❌ Orchestration engine doesn't support hooks

**Evidence Required**: Directory listing showing all components present

---

### Phase 0: Wire Learning Handler
**Effort**: Small

**Goal**: Connect Learning Handler to orchestration pipeline

**Implementation**:
```python
# services/orchestration/orchestration_engine.py

async def process_request(user_input, user_id, session):
    """Process with learning integration"""

    # Existing: Intent classification
    intent = await classify_intent(user_input)

    # NEW: Capture action
    await learning_handler.capture_action(
        user_id=user_id,
        action_type=intent.category,
        context={"intent": intent, "input": user_input},
        session=session
    )

    # Existing: Execute
    result = await execute_intent(intent, user_id, session)

    # NEW: Record outcome
    await learning_handler.record_outcome(
        user_id=user_id,
        action_type=intent.category,
        success=result.success,
        session=session
    )

    # NEW: Get suggestions
    suggestions = await learning_handler.get_suggestions(
        user_id=user_id,
        context={"intent": intent},
        session=session
    )

    # Add to response
    if suggestions:
        result.suggestions = suggestions

    return result
```

**STOP Conditions**:
- ❌ Orchestration doesn't support hooks
- ❌ Performance impact >50ms
- ❌ Learning handler causes orchestration errors

**Evidence Required**:
- Logs showing handler called on requests
- Performance benchmark showing <20ms overhead

---

### Phase 1: Implement Core Learning Cycle
**Effort**: Medium

**Components to Build**:

**1. Pattern Capture**:
```python
async def capture_action(user_id, action_type, context, session):
    """Capture user action for pattern learning"""

    # Extract pattern features
    pattern_data = {
        "action_type": action_type,
        "context": context,
        "timestamp": datetime.utcnow()
    }

    # Find or create pattern
    pattern = await find_similar_pattern(
        user_id, pattern_data, similarity_threshold=0.8, session
    )

    if pattern:
        # Update existing
        pattern.usage_count += 1
        pattern.last_used_at = datetime.utcnow()
    else:
        # Create new
        pattern = LearnedPattern(
            user_id=user_id,
            pattern_type=determine_pattern_type(action_type),
            pattern_data=pattern_data,
            confidence=0.5  # Start neutral
        )
        session.add(pattern)

    await session.commit()
```

**2. Confidence Calculation**:
```python
def update_confidence(self):
    """Calculate confidence with decay"""

    total = self.success_count + self.failure_count
    if total == 0:
        return

    # Success rate (0.0 - 1.0)
    success_rate = self.success_count / total

    # Volume factor (caps at 10 uses)
    volume_factor = min(self.usage_count / 10, 1.0)

    # Weighted confidence
    new_confidence = (success_rate * 0.8 + self.confidence * 0.2)

    # Apply volume factor
    self.confidence = new_confidence * volume_factor

    # Apply time decay
    days_since_use = (datetime.utcnow() - self.last_used_at).days
    self.confidence *= (0.95 ** days_since_use)

    self.last_updated_at = datetime.utcnow()
```

**3. Similarity Detection**:
```python
def calculate_similarity(pattern1, pattern2) -> float:
    """Compare patterns (0.0 - 1.0)"""

    features = ["action_type", "context", "timing"]
    matches = sum(1 for f in features if pattern1.get(f) == pattern2.get(f))
    return matches / len(features)
```

**Unit Tests Required**:
- Pattern capture creates new patterns
- Similar patterns get merged
- Confidence increases with success
- Confidence decreases with failure
- Time decay works correctly

**STOP Conditions**:
- ❌ Confidence algorithm unstable (oscillates wildly)
- ❌ Pattern capture causes database errors
- ❌ Similarity detection has >10% false positive rate

**Evidence Required**:
- Unit test output showing all tests pass
- Database query showing patterns created

---

### Phase 2: User Controls
**Effort**: Small

**API Endpoints**:
```python
# web/api/routes/learning.py

@router.get("/settings")
async def get_learning_settings(current_user, db):
    """Get user's learning settings"""
    return await learning_service.get_settings(current_user.id, db)

@router.put("/settings")
async def update_learning_settings(settings, current_user, db):
    """Update learning settings"""
    return await learning_service.update_settings(
        current_user.id, settings, db
    )

@router.get("/patterns")
async def get_learned_patterns(current_user, db):
    """View all learned patterns"""
    return await learning_service.get_patterns(current_user.id, db)

@router.delete("/patterns/{pattern_id}")
async def delete_pattern(pattern_id, current_user, db):
    """Remove a learned pattern"""
    await learning_service.delete_pattern(
        pattern_id, current_user.id, db
    )
    return {"success": True}

@router.post("/patterns/{pattern_id}/feedback")
async def provide_feedback(pattern_id, feedback, current_user, db):
    """Confirm or reject pattern"""
    await learning_service.process_feedback(
        pattern_id, current_user.id, feedback.confirmed, db
    )
    return {"success": True}
```

**Web UI Components**:
1. Learning Dashboard - view patterns
2. Pattern Cards - confidence indicators
3. Quick Actions - confirm/reject/disable

**Evidence Required**:
- API endpoint test results
- Screenshot of learning dashboard

---

### Phase 3: Feedback Loop
**Effort**: Small

**Pattern Confirmation Logic**:
```python
async def process_feedback(pattern_id, user_id, confirmed, session):
    """Process user feedback on pattern"""

    pattern = await session.get(LearnedPattern, pattern_id)

    if confirmed:
        # User confirmed - boost confidence
        pattern.success_count += 2  # Weight confirmations
        pattern.confidence = min(pattern.confidence * 1.1, 1.0)
    else:
        # User rejected - reduce confidence
        pattern.failure_count += 2
        pattern.confidence *= 0.5

        # Disable if too low
        if pattern.confidence < 0.3:
            pattern.enabled = False

    await session.commit()
```

**In-Chat Suggestions**:
```
Piper: "I've noticed you typically create GitHub issues after standup.
Would you like me to suggest this next time?"

[Yes, that's helpful] [No, don't suggest] [Settings]
```

**STOP Conditions**:
- ❌ Feedback creates infinite loops
- ❌ User rejection rate >50% in testing
- ❌ Confirmation doesn't improve pattern quality

**Evidence Required**:
- Test showing feedback affects confidence
- Screenshot of in-chat suggestion UI

---

### Phase 4: Pattern Application
**Effort**: Small

**Auto-Application Logic**:
```python
async def apply_patterns(user_id, context, session):
    """Apply high-confidence patterns"""

    # Get automation-threshold patterns
    patterns = await session.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.confidence >= 0.9,
            LearnedPattern.enabled == True
        )
    )

    applied = []
    for pattern in patterns.scalars():
        if pattern_matches_context(pattern, context):
            # Apply pattern
            action = prepare_action_from_pattern(pattern)
            applied.append(action)

            # Notify user
            notify_user(f"I've prepared {action.description} based on your pattern")

    return applied
```

**Evidence Required**:
- Demonstration of auto-application at 0.9 confidence
- User notification screenshot

---

### Phase 5: Integration Testing
**Effort**: Small

**Test Full Learning Cycle**:
```python
@pytest.mark.integration
async def test_full_learning_cycle(real_client, real_db):
    """Test complete pattern learning flow"""

    # Day 1: User performs action 3 times
    for i in range(3):
        await simulate_user_action("create_issue_after_standup")

    # Check pattern created
    patterns = await get_user_patterns(user_id)
    assert len(patterns) == 1
    assert 0.5 <= patterns[0].confidence <= 0.7

    # Check suggestion appears
    suggestions = await get_suggestions(user_id, {"after": "standup"})
    assert len(suggestions) == 1

    # User confirms
    await provide_feedback(patterns[0].pattern_id, confirmed=True)

    # Check confidence increased
    updated = await get_pattern(patterns[0].pattern_id)
    assert updated.confidence > patterns[0].confidence

    # After more successes, check auto-application
    for _ in range(5):
        await simulate_successful_action("create_issue_after_standup")

    final = await get_pattern(patterns[0].pattern_id)
    assert final.confidence >= 0.9
```

**Evidence Required**:
- Integration test output showing all scenarios pass
- No performance degradation

---

### Phase 6: Manual Testing & Polish
**Effort**: Small-Medium

**Manual Test Scenarios**:

**Scenario 1: First Pattern Experience**
1. [ ] Perform same action 3 times
2. [ ] See "I noticed a pattern" message
3. [ ] See confidence indicator
4. [ ] Click "Yes, that's helpful"
5. [ ] See proactive suggestion next time

**Scenario 2: Pattern Control**
1. [ ] Open learning dashboard
2. [ ] See patterns with confidence bars
3. [ ] Disable specific pattern
4. [ ] Verify it stops appearing
5. [ ] Re-enable and verify

**Scenario 3: Automatic Application**
1. [ ] Build high-confidence pattern (>0.9)
2. [ ] Trigger pattern context
3. [ ] See "I've prepared [action]"
4. [ ] One-click execute
5. [ ] Verify completion

**Polish Items**:
- Clear, friendly messages
- Visual confidence indicators
- Smooth UI animations
- Error handling

**Evidence Required**:
- Screenshots/video of all 3 scenarios
- User feedback from alpha testers

---

### Phase Z: Completion & Handoff
**Effort**: Small

**Final Verification Checklist**:
- [ ] All unit tests passing (>80% coverage)
- [ ] Integration tests passing (3 scenarios)
- [ ] Manual tests completed (3 scenarios)
- [ ] Performance targets met (<20ms overhead)
- [ ] Documentation updated
- [ ] Evidence package compiled

**Evidence Package Assembly**:
```bash
# Compile test results
pytest tests/learning/ -v --cov=services/learning > evidence/tests.txt

# Performance metrics
python scripts/benchmark_learning.py > evidence/performance.txt

# Manual test screenshots
ls -la evidence/screenshots/

# Create summary
echo "## Learning System Evidence" > evidence/SUMMARY.md
echo "- Unit Tests: X/Y passing" >> evidence/SUMMARY.md
echo "- Integration: 3/3 scenarios" >> evidence/SUMMARY.md
echo "- Performance: Xms overhead" >> evidence/SUMMARY.md
echo "- Screenshots: see evidence/screenshots/" >> evidence/SUMMARY.md
```

**Git Commit**:
```bash
git add -A
git commit -m "feat(#300): Implement Basic Auto-Learning

- Real-time pattern detection with 0.7/0.9 thresholds
- User-controlled learning with feedback loop
- Integration with orchestration pipeline
- Performance overhead <20ms
- Three-tier testing complete

Foundation Stone #1 of learning cathedral complete.

Fixes #300"
```

**Handoff to PM**:
- Issue #300 marked complete
- Evidence package in evidence/ directory
- Alpha users ready for testing
- Monitoring dashboard available at /learning

**STOP Conditions**:
- ❌ Any critical test failures
- ❌ Performance >20ms overhead
- ❌ User feedback indicates poor UX

---

## Success Criteria

### Functionality ✅
- [ ] Learning Handler wired to orchestration
- [ ] Real-time pattern capture working
- [ ] Confidence updates based on outcomes
- [ ] Pattern similarity detection (no duplicates)
- [ ] Suggestions appear at >0.7 confidence
- [ ] Automatic application at >0.9 confidence
- [ ] User feedback loop functional

### User Experience ✅
- [ ] Learning dashboard shows patterns
- [ ] Clear confidence indicators
- [ ] One-click pattern confirmation/rejection
- [ ] User can disable learning
- [ ] Friendly, helpful messaging

### Performance ✅
- [ ] Pattern capture: <10ms
- [ ] Confidence update: <5ms
- [ ] Suggestion retrieval: <1ms
- [ ] Total overhead: <20ms
- [ ] No system degradation

### Testing ✅
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Manual scenarios passing
- [ ] No flaky tests
- [ ] >80% code coverage

### Documentation ✅
- [ ] User guide: "How Piper learns"
- [ ] API docs updated
- [ ] Architecture documented
- [ ] Privacy policy updated

---

## Risk Mitigation

### Risk 1: False Pattern Detection
**Impact**: Medium - User annoyance
**Probability**: Medium
**Mitigation**:
- Confidence thresholds (0.7/0.9)
- User rejection mechanism
- Auto-disable at <0.3
- Similarity detection

### Risk 2: Performance Impact
**Impact**: High - System slowdown
**Probability**: Low
**Mitigation**:
- Async pattern storage
- Cached lookups
- Performance tests
- <20ms target

### Risk 3: Privacy Concerns
**Impact**: High - Trust critical
**Probability**: Low
**Mitigation**:
- Per-user storage only
- User can export/delete
- Transparent UI
- Clear documentation

### Risk 4: User Annoyance
**Impact**: Medium - Adoption hurt
**Probability**: Medium
**Mitigation**:
- User controls
- Friendly messaging
- Alpha feedback
- Configurable thresholds

---

## Conclusion

**This Is Foundation Stone #1**:
- All future learning builds on this
- Quality over speed (Time Lord way)
- User-controlled and transparent
- Aligned with Piper's values

**Not Just "Make It Auto"**:
- Part of a cathedral, not a shed
- Strategic progression planned
- Wait for signals before advancing
- Build this foundation exceptionally well

**Expected Outcomes**:
- Real-time personalization (differentiator)
- Faster learning cycle (minutes vs weeks)
- Happy alpha users (quality UX)
- Solid foundation for future levels

---

**Status**: Ready for Agent Implementation
**Effort**: Medium (1-2 days total)
**Priority**: P2 (Alpha Feature)

---

_"Part of a cathedral, not just a random brick shed"_
_"Quality exists outside of time constraints"_
