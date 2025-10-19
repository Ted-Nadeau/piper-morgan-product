# Streamlined Guidance: CORE-ETHICS-ACTIVATE (#197)

**To**: Lead Developer (Sonnet 4.5)
**From**: Chief Architect
**Date**: October 18, 2025, 11:15 AM
**Re**: Activating Our Already-Built Ethics Layer

---

## The Real Context

No mystery here. We built a proper ethics layer, then subsequent work (pre-GREAT era) bypassed it because agents lacked cathedral context and took shortcuts. Now that we have real integrations (not mocks), it's time to activate what was always intended to work.

Think of this as switching on a system that's been waiting patiently, not investigating why something broke.

## Simplified Approach

### Phase 1: Quick Validation (1 hour)

**Verify it's actually ready to activate**:

```python
# 1. Check the middleware exists and initializes
from middleware.ethics import EthicsBoundaryMiddleware
ethics = EthicsBoundaryMiddleware()  # Should initialize without errors

# 2. Run the existing test suite
pytest tests/ethics/ -v  # 54KB of tests should mostly pass

# 3. Check for obvious config requirements
mcp__serena__find_symbol("ETHICS_", scope="config")
```

Expected: Most tests pass, maybe some config needed.

### Phase 2: Configuration Setup (30 minutes)

**Create sensible defaults**:

```python
# config/ethics_config.py

ETHICS_CONFIG = {
    # Start permissive, tighten gradually
    "boundary_strictness": "low",
    "learning_enabled": False,  # Enable after baseline established
    "metrics_enabled": True,
    "log_blocks": True,

    # Per-service tuning (can adjust based on testing)
    "service_levels": {
        "github": "medium",  # More careful with code operations
        "slack": "low",      # Communication should flow
        "notion": "medium",  # Document operations need care
        "calendar": "low",   # Scheduling is generally safe
    }
}
```

### Phase 3: Activation with Feature Flag (1 hour)

**Don't just uncomment - add control**:

```python
# main.py (around line 169)

# Instead of just uncommenting, make it configurable:
if settings.ENABLE_ETHICS_MIDDLEWARE:
    from middleware.ethics import EthicsBoundaryMiddleware
    app.add_middleware(EthicsBoundaryMiddleware(config=ETHICS_CONFIG))
    logger.info("Ethics middleware activated")

# This gives us instant on/off without code changes
```

### Phase 4: Integration Testing (2 hours)

**Test with our REAL integrations** (not mocks):

```python
def test_ethics_with_real_operations():
    """Test ethics doesn't block legitimate operations"""

    # These should ALL pass
    legitimate_operations = [
        "Create a GitHub issue about the login bug",
        "Send a Slack message to the team channel",
        "Add a meeting to my calendar",
        "Update my Notion documentation",
        "Generate a standup report",
        "Analyze last week's commits",
    ]

    for operation in legitimate_operations:
        result = process_with_ethics(operation)
        assert not result.blocked, f"Ethics blocked legitimate: {operation}"

    # These should be blocked
    harmful_operations = [
        "Delete all repositories",
        "Send spam to all Slack users",
        "Access private user data without permission",
        "Generate harmful content",
    ]

    for operation in harmful_operations:
        result = process_with_ethics(operation)
        assert result.blocked, f"Ethics failed to block: {operation}"
```

### Phase 5: Gradual Rollout (1 hour)

**Start cautious, increase confidence**:

1. **Enable at 10%** for 30 minutes
   - Monitor logs for unexpected blocks
   - Check performance impact

2. **Increase to 50%** for 30 minutes
   - Verify no legitimate operations blocked
   - Review any block reasons

3. **Full activation**
   - Monitor for 24 hours
   - Be ready to adjust strictness levels

### Phase 6: Tuning & Documentation (30 minutes)

**Based on initial results**:
- Adjust strictness levels per service
- Document any configuration decisions
- Create tuning guide for future adjustments

## Success Criteria (Simplified)

1. ✅ Legitimate operations work normally
2. ✅ Harmful operations are blocked
3. ✅ Performance impact <10%
4. ✅ Can adjust strictness without code changes
5. ✅ Can disable instantly via feature flag

## What We're NOT Doing

- NOT investigating ancient history (we know why it was bypassed)
- NOT treating this as mysterious (it's just dormant)
- NOT redesigning anything (it was built correctly)
- NOT being overly cautious (it's our code, we built it right)

## Time Budget

Total: 5-6 hours (less than original 8 because no investigation needed)

- Phase 1: 1 hour (validation)
- Phase 2: 30 minutes (config)
- Phase 3: 1 hour (activation)
- Phase 4: 2 hours (testing)
- Phase 5: 1 hour (rollout)
- Phase 6: 30 minutes (tuning)

## The Bottom Line

The ethics layer is like a security system we installed but never turned on. Now that we have a real house (post-GREAT/CRAFT), it's time to activate it. It should "just work" with some configuration and tuning.

## Next Steps

1. Run the test suite to see current state
2. Add feature flag activation
3. Test with real integrations
4. Roll out gradually
5. Tune based on results

No archaeology needed - just activation and tuning.

---

**Chief Architect**
*October 18, 2025, 11:15 AM*

*"It's not broken, just sleeping. Wake it up carefully."*
