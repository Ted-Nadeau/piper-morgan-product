# ADR-036: QueryRouter Resurrection Strategy

**Status**: Accepted
**Date**: September 20, 2025
**Deciders**: Christian Crumlish (PM), Chief Architect

## Context

During our architectural review (September 19, 2025), we discovered QueryRouter (PM-034) is 75% complete but disabled:

```python
# In services/orchestration/engine.py
# TODO: Re-enable QueryRouter after PM-034 completion
# self.query_router = QueryRouter(self.session)  # COMMENTED OUT
```

This single disabled line blocks 80% of MVP features:
- GitHub issue creation through chat
- Complex workflows
- Query operations
- Multi-step operations

The QueryRouter implementation exists, appears well-designed (including A/B testing framework), but was never connected to the OrchestrationEngine. This is the critical wire that needs reconnecting.

## Decision

**Complete PM-034 implementation** rather than redesign or replace QueryRouter.

### Approach

1. **Review existing PM-034 implementation** to understand what's complete
2. **Identify why initialization was disabled** (likely a specific blocker)
3. **Fix the blocker** rather than work around it
4. **Connect QueryRouter to OrchestrationEngine** properly
5. **Connect to existing Intent Classification** (per ADR-032 audit)
6. **Validate with GitHub issue creation** as proof of success

### What We're NOT Doing

- NOT redesigning QueryRouter from scratch
- NOT creating alternative routing mechanisms
- NOT adding workarounds to bypass QueryRouter
- NOT implementing partial solutions

## Consequences

### Positive

1. **Preserves Existing Investment**: 75% complete work is valuable
2. **Faster Path to Functionality**: Completion faster than rewrite
3. **Maintains Architectural Intent**: Original PM-034 design was sound
4. **Unblocks Everything**: This is the keystone - fixes cascade of features
5. **A/B Testing Ready**: Sophisticated framework already in place

### Negative

1. **Inherits Original Design**: Any flaws in PM-034 design persist
2. **Unknown Blockers**: Must discover why it was disabled
3. **Potential Refactoring**: May need updates for current architecture
4. **Documentation Gap**: PM-034 implementation may lack documentation

### Neutral

1. **Learning Opportunity**: Understanding why it failed teaches us about other incomplete work
2. **Pattern Recognition**: Likely follows same 75% pattern seen elsewhere
3. **Testing Required**: Need comprehensive tests to lock in completion

## Implementation Strategy

### Phase 1: Archaeological Discovery (Day 1)
```bash
# Find all QueryRouter references
grep -r "QueryRouter" . --include="*.py"

# Find TODO comments about PM-034
grep -r "PM-034\|TODO.*[Qq]uery" . --include="*.py"

# Check git history for when it was disabled
git log -p --grep="QueryRouter" -- services/orchestration/engine.py
```

### Phase 2: Blocker Identification (Day 2)
- Review PM-034 implementation files
- Identify specific initialization failure
- Check for missing dependencies
- Verify database schema compatibility

### Phase 3: Fix and Connect (Days 3-4)
```python
# Fix initialization in OrchestrationEngine
class OrchestrationEngine:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.query_router = QueryRouter(session)  # RECONNECT!
        self.intent_classifier = IntentClassifier()  # Already works

    async def process_request(self, user_input: str):
        # Connect the full flow
        intent = await self.intent_classifier.classify(user_input)

        if intent.category == IntentCategory.QUERY:
            return await self.query_router.route(intent)  # USE IT!
        # ... rest of routing logic
```

### Phase 4: Validation (Day 5)
- Test GitHub issue creation end-to-end
- Verify performance <500ms
- Run A/B testing framework
- Document what was actually wrong

## Relationship to Other ADRs

### Supersedes/Updates
- **PM-034 Integration Strategy** - Completes the original vision
- **ADR-032** - QueryRouter must respect universal intent classification

### Related To
- **ADR-035 (Inchworm Protocol)** - Must complete 100% before moving on
- **ADR-037 (Test-Driven Locking)** - Tests prevent future disabling

### Enables
- Future ADRs on A/B testing strategies
- Future ADRs on query optimization

## Success Criteria

1. **Functional**: GitHub issue creation works through chat
2. **Performance**: <500ms for issue creation flow
3. **No Workarounds**: Clean implementation without TODOs
4. **Tested**: Integration tests prevent regression
5. **Documented**: Clear explanation of what was wrong and how fixed

## Risk Mitigation

### Risk: Original Blocker Still Exists
**Mitigation**: Time-boxed investigation (2 days max), then escalate to redesign

### Risk: Integration Breaks Other Components
**Mitigation**: Comprehensive test suite before enabling

### Risk: Performance Degradation
**Mitigation**: Benchmark before/after, maintain <500ms target

### Risk: A/B Testing Complexity
**Mitigation**: Start with feature flag off, enable gradually

## Validation Test

```python
# This must work after CORE-GREAT-1
async def test_github_issue_creation():
    """The North Star test - if this works, QueryRouter resurrection succeeded"""

    user_input = "Create a GitHub issue about fixing the login bug"

    # Through the full stack
    result = await orchestration_engine.process_request(user_input)

    # Verify issue created
    assert result.success
    assert result.issue_number
    assert result.issue_url

    # Verify performance
    assert result.processing_time < 500  # milliseconds
```

## The Deeper Pattern

This ADR exemplifies why the Inchworm Protocol exists. PM-034 was a good design that got to 75% completion, hit a blocker, and instead of fixing the blocker, someone commented it out and added a TODO.

This time, we will:
1. Find the blocker
2. Fix the blocker
3. Complete the implementation
4. Lock it with tests
5. Never allow it to be disabled again

## Decision Outcome

By completing PM-034 rather than replacing it, we:
- Honor the original architectural vision
- Build on existing investment
- Demonstrate that incomplete work can be completed
- Prove the Inchworm Protocol works

The QueryRouter resurrection is not just about fixing a component - it's about changing our culture from "work around problems" to "fix problems completely."

---

## References

- PM-034 Original Implementation
- Current State Documentation (September 19, 2025)
- ADR-032 Audit Results (September 20, 2025)
- The Great Refactor Roadmap

## Next Actions

1. CORE-GREAT-1 begins with QueryRouter investigation
2. Document actual blocker when found
3. Update this ADR with specific fix applied
4. Celebrate when GitHub issue creation works! 🐛

---

*"We're not building new things. We're finishing what we started."*
