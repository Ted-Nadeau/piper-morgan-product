# Gameplan: CORE-ALPHA-LEARNING-BASIC
## Implement Basic Auto-Learning (Foundation Stone #1)

**Issue**: CORE-ALPHA-LEARNING-BASIC
**Date**: November 12, 2025
**Architect**: Chief Architect (Opus)
**For Review By**: Chief Architect + PM
**Estimated Effort**: 5-10 hours (1-2 days)

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

**Time Lord Philosophy**: Build solid foundation before advancing
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
5. **Pattern Sweep**: Standalone tool (continues running for codebase patterns)

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

**Alternative Considered**: Single threshold (0.8)
- **Rejected**: No distinction between suggestion and automation
- Too rigid for different user preferences

---

### Decision 2: Learning Cycle Integration ✅

**Integration Point**: Orchestration Pipeline

**Flow**:
```
User Input
    ↓
Intent Classification
    ↓
Orchestration Engine
    ↓
Learning Handler (capture action) ← NEW
    ↓
Execute Action
    ↓
Learning Handler (capture outcome + update confidence) ← NEW
    ↓
Check Patterns (suggest or apply) ← NEW
    ↓
Response to User (+ pattern info if applicable)
```

**Why This Point?**:
- After intent classification (we know what user wants)
- Before execution (can capture context)
- After execution (can capture outcome)
- Minimal performance impact (<10ms)

**Alternative Considered**: Separate learning service
- **Rejected**: Adds latency, complicates architecture
- Inline is faster and simpler

---

### Decision 3: User Control Philosophy ✅

**User Always in Control**:
- Can disable learning globally
- Can disable specific patterns
- Can see all learned patterns
- Can delete patterns
- Must confirm before automation (first time)

**Rationale**:
- Aligns with Piper's human-AI collaboration values
- Prevents "creepy factor"
- Builds trust through transparency
- GDPR compliant

**Alternative Considered**: Aggressive auto-learning (no user control)
- **Rejected**: Misaligned with Piper's values
- Risk of user annoyance/distrust

---

### Decision 4: Pattern Storage Strategy ✅

**Storage**: Per-user, in main database

**Schema** (from Sprint A5):
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
    created_at: datetime
    last_used_at: datetime
```

**Why Per-User Only?**:
- Level 1 doesn't need cross-user patterns
- Simpler privacy model
- Faster queries (no aggregation)
- Level 3 can add cross-user later

**Alternative Considered**: Shared pattern pool
- **Rejected**: Premature (Level 3 feature)
- Adds complexity without value yet

---

### Decision 5: Performance Targets ✅

**Targets**:
- Pattern capture: <10ms
- Confidence update: <5ms
- Pattern suggestion: <1ms (cached)
- Total overhead: <20ms per request

**Rationale**:
- User experience: No noticeable delay
- System capacity: 602K req/sec sustained
- Minimal impact: <3% overhead

**Mitigation**:
- Async pattern storage (no user wait)
- Cached pattern lookups
- Background confidence calculations

---

### Decision 6: Testing Strategy ✅

**Three-Tier Verification**:
1. **Unit Tests**: Pattern capture, confidence, similarity
2. **Integration Tests**: Full learning cycle with real DB
3. **Manual Tests**: User experience scenarios

**Why Three Tiers?**:
- Unit: Fast feedback (development)
- Integration: Catch interaction bugs
- Manual: User experience validation

**No Mocks for Integration** (Pattern-006):
- Real database connections
- Transaction rollback for isolation
- Proves actual behavior

---

## Implementation Plan

### Phase -1: Infrastructure Verification (15 minutes)

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

---

### Phase 0: Wire Learning Handler (1 hour)

**Goal**: Connect Learning Handler to orchestration pipeline

**Step 0.1**: Add Learning Hooks to Orchestration (30 min)
```python
# services/orchestration/orchestration_engine.py

async def process_request(
    user_input: str,
    user_id: UUID,
    session: AsyncSession
):
    """Process user request with learning"""

    # Existing: Intent classification
    intent = await classify_intent(user_input)

    # NEW: Capture user action for learning
    learning_context = {
        "intent": intent.category,
        "input": user_input,
        "timestamp": datetime.utcnow()
    }
    await learning_handler.capture_action(
        user_id=user_id,
        action_type=intent.category,
        context=learning_context,
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

    # NEW: Get pattern suggestions
    suggestions = await learning_handler.get_suggestions(
        user_id=user_id,
        context=learning_context,
        session=session
    )

    # Existing: Return response (+ suggestions)
    return Response(
        content=result.content,
        pattern_suggestions=suggestions
    )
```

**Step 0.2**: Verify Integration (15 min)
```bash
# Run orchestration tests
pytest tests/orchestration/ -v

# Check learning handler called
# Check no performance degradation
```

**Step 0.3**: Test End-to-End (15 min)
```bash
# Start Piper
python main.py

# Perform test action
# Check pattern captured in database
psql -U piper -c "SELECT * FROM learned_patterns;"
```

**Success Criteria**:
- ✅ Learning Handler called before/after execution
- ✅ Patterns captured in database
- ✅ No performance impact (< 10ms overhead)
- ✅ All existing tests still pass

---

### Phase 1: Implement Core Learning Cycle (2-3 hours)

**Goal**: Pattern capture, confidence updates, similarity detection

**Step 1.1**: Pattern Capture (30 min)
```python
# services/learning/learning_handler.py

async def capture_action(
    user_id: UUID,
    action_type: str,
    context: Dict[str, Any],
    session: AsyncSession
):
    """Capture user action for pattern learning"""

    # Extract pattern features
    pattern_data = extract_features(action_type, context)

    # Check for similar patterns
    similar = await find_similar_pattern(
        user_id=user_id,
        pattern_data=pattern_data,
        similarity_threshold=0.8,  # 80% similar
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
            pattern_type=PatternType.USER_WORKFLOW,
            pattern_data=pattern_data,
            confidence=0.5,  # Initial
            usage_count=1,
            enabled=True
        )
        session.add(pattern)

    await session.commit()
```

**Step 1.2**: Outcome Recording (30 min)
```python
async def record_outcome(
    user_id: UUID,
    action_type: str,
    success: bool,
    session: AsyncSession
):
    """Update pattern confidence based on outcome"""

    # Find most recent pattern for this action
    pattern = await get_latest_pattern(user_id, action_type, session)

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

**Step 1.3**: Confidence Algorithm (30 min)
```python
def update_confidence(self):
    """Calculate confidence from success/failure rates"""

    total = self.success_count + self.failure_count
    if total == 0:
        return

    # Success rate (0.0 - 1.0)
    success_rate = self.success_count / total

    # Volume factor (more uses = more confidence)
    # Caps at 10 uses for full confidence
    volume_factor = min(self.usage_count / 10, 1.0)

    # Weighted: 80% current success rate, 20% previous confidence
    # Allows confidence to adjust but not swing wildly
    new_confidence = (success_rate * 0.8 + self.confidence * 0.2)

    # Apply volume factor
    self.confidence = new_confidence * volume_factor

    self.last_updated_at = datetime.utcnow()
```

**Step 1.4**: Similarity Detection (45 min)
```python
async def find_similar_pattern(
    user_id: UUID,
    pattern_data: Dict[str, Any],
    similarity_threshold: float,
    session: AsyncSession
) -> Optional[LearnedPattern]:
    """Find existing similar pattern to avoid duplicates"""

    # Get all user's patterns of same type
    patterns = await session.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.enabled == True
        )
    )

    for pattern in patterns.scalars():
        # Calculate similarity score
        similarity = calculate_similarity(
            pattern.pattern_data,
            pattern_data
        )

        if similarity >= similarity_threshold:
            return pattern

    return None


def calculate_similarity(data1: Dict, data2: Dict) -> float:
    """Calculate similarity between two patterns (0.0 - 1.0)"""

    # Compare key features
    features = ["action_type", "context", "timing", "user_preferences"]
    matches = 0

    for feature in features:
        if data1.get(feature) == data2.get(feature):
            matches += 1

    return matches / len(features)
```

**Step 1.5**: Unit Tests (30 min)
```python
# tests/learning/test_pattern_capture.py

async def test_pattern_capture_creates_new():
    """Test first action creates new pattern"""
    result = await capture_action(user_id, "create_issue", {}, session)

    pattern = await get_pattern(user_id, session)
    assert pattern.usage_count == 1
    assert pattern.confidence == 0.5


async def test_similar_patterns_merged():
    """Test similar actions update existing pattern"""
    await capture_action(user_id, "create_issue", {"after": "standup"}, session)
    await capture_action(user_id, "create_issue", {"after": "standup"}, session)

    patterns = await get_all_patterns(user_id, session)
    assert len(patterns) == 1
    assert patterns[0].usage_count == 2


async def test_confidence_increases_with_success():
    """Test confidence goes up with successful outcomes"""
    pattern = await create_test_pattern(confidence=0.5)

    for _ in range(5):
        await record_outcome(user_id, "create_issue", success=True, session)

    updated = await get_pattern(pattern.pattern_id, session)
    assert updated.confidence > 0.5
```

**Success Criteria**:
- ✅ Patterns captured from user actions
- ✅ Similar patterns merged (no duplicates)
- ✅ Confidence updates with outcomes
- ✅ Low-confidence patterns disabled automatically
- ✅ Unit tests passing

---

### Phase 2: User Controls (1 hour)

**Goal**: User-facing controls for learning system

**Step 2.1**: Settings Model (15 min)
```python
# services/learning/models.py

class LearningSettings(BaseModel):
    """User-configurable learning settings"""

    user_id: UUID
    learning_enabled: bool = True
    suggestion_threshold: float = 0.7
    automation_threshold: float = 0.9
    pattern_visibility: str = "visible"  # visible | suggestions_only | hidden
    feedback_prompts: bool = True
    created_at: datetime
    updated_at: datetime
```

**Step 2.2**: API Endpoints (30 min)
```python
# web/api/routes/learning.py

@router.get("/settings")
async def get_learning_settings(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's learning settings"""
    settings = await learning_service.get_settings(current_user.id, db)
    return settings


@router.put("/settings")
async def update_learning_settings(
    settings: LearningSettings,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update learning settings"""
    updated = await learning_service.update_settings(
        current_user.id,
        settings,
        db
    )
    return updated


@router.get("/patterns")
async def get_learned_patterns(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """View all learned patterns"""
    patterns = await learning_service.get_patterns(current_user.id, db)
    return patterns


@router.delete("/patterns/{pattern_id}")
async def delete_pattern(
    pattern_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Remove a learned pattern"""
    await learning_service.delete_pattern(pattern_id, current_user.id, db)
    return {"success": True}
```

**Step 2.3**: Tests (15 min)
```bash
# Test endpoints
pytest tests/api/test_learning_endpoints.py -v

# Expected: All CRUD operations work
```

**Success Criteria**:
- ✅ Settings endpoints functional
- ✅ Pattern management endpoints functional
- ✅ User can view/delete patterns
- ✅ Settings persist correctly

---

### Phase 3: Feedback Loop (1 hour)

**Goal**: User can confirm/reject pattern suggestions

**Step 3.1**: Pattern Suggestions (30 min)
```python
async def get_suggestions(
    user_id: UUID,
    context: Dict[str, Any],
    session: AsyncSession
) -> List[PatternSuggestion]:
    """Get pattern suggestions above threshold"""

    # Get user's settings
    settings = await get_settings(user_id, session)

    if not settings.learning_enabled:
        return []

    # Find high-confidence patterns
    patterns = await session.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.confidence >= settings.suggestion_threshold,
            LearnedPattern.enabled == True
        )
        .filter(pattern_matches_context(context))
    )

    suggestions = []
    for pattern in patterns.scalars():
        suggestions.append(PatternSuggestion(
            pattern_id=pattern.pattern_id,
            description=describe_pattern(pattern),
            confidence=pattern.confidence,
            action_type="suggestion" if pattern.confidence < settings.automation_threshold else "automatic"
        ))

    return suggestions
```

**Step 3.2**: Pattern Confirmation (30 min)
```python
@router.post("/patterns/{pattern_id}/feedback")
async def provide_feedback(
    pattern_id: UUID,
    feedback: PatternFeedback,  # {confirmed: bool}
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """User confirms or rejects pattern"""

    pattern = await db.get(LearnedPattern, pattern_id)

    if pattern.user_id != current_user.id:
        raise HTTPException(403, "Not your pattern")

    if feedback.confirmed:
        # User confirmed - boost confidence
        pattern.success_count += 2  # Weight confirmations
        pattern.confidence = min(pattern.confidence * 1.1, 1.0)
    else:
        # User rejected - penalize
        pattern.failure_count += 2
        pattern.confidence *= 0.5

        # Disable if too low
        if pattern.confidence < 0.3:
            pattern.enabled = False

    await db.commit()
    return {"success": True, "new_confidence": pattern.confidence}
```

**Success Criteria**:
- ✅ Suggestions appear when confidence >0.7
- ✅ User can confirm patterns (confidence increases)
- ✅ User can reject patterns (confidence decreases)
- ✅ Rejected patterns eventually disable

---

### Phase 4: Pattern Application (1 hour)

**Goal**: High-confidence patterns apply automatically

**Step 4.1**: Automatic Application (45 min)
```python
async def apply_patterns(
    user_id: UUID,
    context: Dict[str, Any],
    session: AsyncSession
) -> List[AppliedPattern]:
    """Apply high-confidence patterns automatically"""

    settings = await get_settings(user_id, session)

    # Only if automation enabled
    if not settings.learning_enabled:
        return []

    # Find patterns above automation threshold
    patterns = await session.execute(
        select(LearnedPattern)
        .where(
            LearnedPattern.user_id == user_id,
            LearnedPattern.confidence >= settings.automation_threshold,
            LearnedPattern.enabled == True
        )
        .filter(pattern_matches_context(context))
    )

    applied = []
    for pattern in patterns.scalars():
        # Execute pattern action
        result = await execute_pattern_action(pattern, context)

        applied.append(AppliedPattern(
            pattern_id=pattern.pattern_id,
            action=pattern.pattern_data["action_type"],
            confidence=pattern.confidence,
            result=result
        ))

        # Update usage
        pattern.usage_count += 1
        pattern.last_used_at = datetime.utcnow()

    await session.commit()
    return applied
```

**Step 4.2**: Tests (15 min)
```python
async def test_automatic_application():
    """Test patterns auto-apply at 0.9+ confidence"""

    # Create high-confidence pattern
    pattern = await create_test_pattern(confidence=0.95)

    # Trigger context
    applied = await apply_patterns(user_id, {"after": "standup"}, session)

    assert len(applied) == 1
    assert applied[0].pattern_id == pattern.pattern_id
```

**Success Criteria**:
- ✅ Patterns >0.9 confidence auto-apply
- ✅ User notified of automatic actions
- ✅ User can disable auto-application
- ✅ Actions logged for audit trail

---

### Phase 5: Integration Testing (1-2 hours)

**Goal**: Verify full learning cycle works end-to-end

**Test Scenario 1: First-Time Learning** (30 min)
```python
@pytest.mark.integration
async def test_first_time_learning_cycle():
    """Test user's first pattern learning experience"""

    # Day 1: User performs action 3 times
    for _ in range(3):
        response = await simulate_action(
            user_id,
            "create_issue",
            {"after": "standup"},
            session
        )

    # Check pattern detected
    patterns = await get_all_patterns(user_id, session)
    assert len(patterns) == 1
    assert patterns[0].usage_count == 3
    assert 0.6 <= patterns[0].confidence <= 0.8

    # Check suggestion appears
    suggestions = await get_suggestions(user_id, {"after": "standup"}, session)
    assert len(suggestions) == 1

    # User confirms pattern
    await provide_feedback(patterns[0].pattern_id, confirmed=True)

    # Check confidence increased
    updated = await get_pattern(patterns[0].pattern_id, session)
    assert updated.confidence > patterns[0].confidence
```

**Test Scenario 2: Pattern Rejection** (30 min)
```python
@pytest.mark.integration
async def test_pattern_rejection():
    """Test user rejecting a pattern"""

    # Create pattern
    pattern = await create_test_pattern(confidence=0.75)

    # User sees suggestion
    suggestions = await get_suggestions(user_id, {}, session)
    assert len(suggestions) == 1

    # User rejects
    await provide_feedback(pattern.pattern_id, confirmed=False)

    # Check confidence dropped
    updated = await get_pattern(pattern.pattern_id, session)
    assert updated.confidence < 0.4

    # Check no longer suggested
    suggestions = await get_suggestions(user_id, {}, session)
    assert len(suggestions) == 0
```

**Test Scenario 3: Automatic Application** (30 min)
```python
@pytest.mark.integration
async def test_automatic_application_flow():
    """Test pattern auto-applies at high confidence"""

    # Build high-confidence pattern through usage
    for i in range(10):
        await simulate_action(user_id, "create_issue", {}, session)
        await record_outcome(user_id, "create_issue", success=True, session)

    # Check confidence reached automation threshold
    pattern = await get_latest_pattern(user_id, "create_issue", session)
    assert pattern.confidence >= 0.9

    # Trigger context, check auto-application
    applied = await apply_patterns(user_id, {}, session)
    assert len(applied) == 1
    assert applied[0].pattern_id == pattern.pattern_id
```

**Success Criteria**:
- ✅ Full cycle works: action → pattern → suggestion → confirmation
- ✅ Pattern rejection prevents future suggestions
- ✅ High confidence triggers auto-application
- ✅ No performance degradation

---

### Phase 6: Manual Testing & Polish (1-2 hours)

**Manual Test Scenarios**:

**Scenario 1: First Pattern Experience**:
1. [ ] Start Piper, perform action 3 times
2. [ ] See "I noticed a pattern" message
3. [ ] See confidence indicator (60-80%)
4. [ ] Click "Yes, that's helpful"
5. [ ] Perform action again, see proactive suggestion
6. [ ] Verify pattern in learning dashboard

**Scenario 2: Pattern Control**:
1. [ ] Open learning dashboard
2. [ ] See all active patterns with confidence bars
3. [ ] Disable specific pattern
4. [ ] Verify it stops appearing
5. [ ] Re-enable pattern
6. [ ] Verify it appears again

**Scenario 3: Automatic Application**:
1. [ ] Build high-confidence pattern (>0.9)
2. [ ] Trigger pattern context
3. [ ] See "I've prepared [action] for you"
4. [ ] One-click execute
5. [ ] Verify action completed

**Polish Items**:
- Clear, friendly messages for pattern suggestions
- Visual confidence indicators
- Smooth UI animations
- Helpful tooltips
- Error handling for edge cases

---

## Testing Summary

### Unit Tests
```bash
# Pattern capture and confidence
pytest tests/learning/test_pattern_capture.py -v
pytest tests/learning/test_confidence.py -v

# Similarity detection
pytest tests/learning/test_similarity.py -v

# Expected: All pass, <3 seconds
```

### Integration Tests
```bash
# Full learning cycle
pytest -m integration tests/learning/ -v

# Expected: 3 tests pass, ~5 seconds
```

### API Tests
```bash
# Learning endpoints
pytest tests/api/test_learning_endpoints.py -v

# Expected: All CRUD operations pass
```

### Manual Tests
- 3 scenarios documented above
- All must pass before claiming complete

---

## Success Criteria (Complete Checklist)

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
- [ ] User can disable learning (global or per-pattern)
- [ ] Friendly, helpful messaging

### Performance ✅
- [ ] Pattern capture: <10ms
- [ ] Confidence update: <5ms
- [ ] Suggestion retrieval: <1ms
- [ ] Total overhead: <20ms per request
- [ ] No degradation in system throughput

### Testing ✅
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Manual scenarios passing
- [ ] No flaky tests
- [ ] Test coverage >80% for learning code

### Documentation ✅
- [ ] User guide: "How Piper learns"
- [ ] API docs: Learning endpoints
- [ ] Developer docs: Architecture
- [ ] Privacy policy updated

---

## Risks & Mitigation

### Risk 1: False Pattern Detection
**Impact**: Medium - Users annoyed by bad suggestions
**Probability**: Medium
**Mitigation**:
- ✅ Confidence thresholds (0.7 for suggestions)
- ✅ User can reject patterns
- ✅ Low-confidence patterns auto-disable
- ✅ Similarity detection prevents duplicates

### Risk 2: Performance Impact
**Impact**: High - System slowdown unacceptable
**Probability**: Low
**Mitigation**:
- ✅ Async pattern storage (no user wait)
- ✅ Cached pattern lookups
- ✅ Performance tests in CI/CD
- ✅ <20ms overhead target

### Risk 3: Privacy Concerns
**Impact**: High - User trust critical
**Probability**: Low
**Mitigation**:
- ✅ Per-user storage only
- ✅ User can export patterns
- ✅ User can delete patterns
- ✅ Transparent UI showing what's learned

### Risk 4: User Annoyance
**Impact**: Medium - Bad UX hurts adoption
**Probability**: Medium
**Mitigation**:
- ✅ User controls (disable globally/per-pattern)
- ✅ Friendly messaging
- ✅ Alpha user feedback
- ✅ Configurable thresholds

---

## Communication Plan

### To PM
- Phase completion updates
- Blockers immediately
- Suggestions for improvements
- Evidence of all claims

### To Chief Architect
- This gameplan for review
- Architectural decisions requiring approval
- Integration points needing coordination
- Performance impact data

### To Agents
- Clear, actionable prompts
- Gameplan context included
- Success criteria explicit
- Evidence requirements stated

---

## Deployment Plan

### Alpha Deployment
1. Deploy to staging first
2. Test with synthetic users
3. Verify performance metrics
4. Deploy to production
5. Monitor alpha user feedback

### Rollback Plan
If issues arise:
1. Disable learning via feature flag
2. Patterns remain in database (no data loss)
3. Re-enable after fixes
4. User data preserved throughout

---

## Next Steps

### For PM Review
1. ✅ Review this gameplan
2. ✅ Approve or request changes
3. ✅ Share with Chief Architect

### For Chief Architect Review
1. ⏸️ Review architectural decisions
2. ⏸️ Approve integration points
3. ⏸️ Confirm performance targets
4. ⏸️ Provide feedback

### After Approval
1. ⏸️ Create agent prompts (Lead Developer)
2. ⏸️ Deploy Code Agent for implementation
3. ⏸️ Deploy Cursor Agent for testing
4. ⏸️ Cross-validation between agents

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

**Status**: Ready for Chief Architect + PM Review
**Author**: Lead Developer
**Date**: November 12, 2025, 5:00 PM PT
**Effort**: 5-10 hours (1-2 days)
**Priority**: P2 (Alpha Feature)

---

_"Part of a cathedral, not just a random brick shed"_
