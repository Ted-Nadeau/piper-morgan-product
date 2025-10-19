# Architectural Guidance: CORE-ETHICS-ACTIVATE (#197)

**To**: Lead Developer (Sonnet 4.5)
**From**: Chief Architect
**Date**: October 18, 2025, 11:05 AM
**Re**: Careful Activation of Universal Ethics Middleware

---

## Critical Context

This is NOT like the MCP migration. The Ethics middleware affects EVERY interaction in the system. It was disabled for a reason (even if that reason is no longer valid), and activating it incorrectly could break the entire system.

The comment "environment setup" at main.py:169 is suspiciously vague. This suggests the original developer encountered complexity they couldn't quickly resolve.

## Approach: Detective Work First, Activation Second

### Phase -1: Historical Investigation (CRITICAL - 1-2 hours)

**This phase determines everything else. Do NOT skip or rush.**

```python
# Use Serena to investigate:

# 1. Git history for the disable commit
mcp__serena__search_project(
    query="EthicsBoundaryMiddleware disabled OR commented",
    file_pattern="*.md"  # Check commit messages, ADRs, issues
)

# 2. Look for related issues/PRs
mcp__serena__search_project(
    query="ethics boundary environment setup",
    file_pattern="*.md"
)

# 3. Check for configuration dependencies
mcp__serena__find_symbol(
    name_regex="EthicsBoundary.*init",
    include_body=True
)

# 4. Review test failures
mcp__serena__search_project(
    query="SKIP OR xfail OR TODO",
    file_pattern="tests/ethics/*.py"
)
```

**What we're looking for**:
- WHY was it disabled? Performance? Bugs? Config issues?
- WHEN was it disabled? Early development or later?
- WHO disabled it? Can we find their reasoning?
- WHAT broke when it was active?

### Phase 0: Risk Assessment (30 minutes)

Based on Phase -1 findings, categorize the risk:

**LOW RISK indicators**:
- Disabled early in development for convenience
- No actual bugs reported
- Tests pass when enabled
- Simple config issue

**HIGH RISK indicators**:
- Disabled due to production issues
- Complex dependency problems
- Performance degradation noted
- Breaking legitimate operations

**If HIGH RISK**: Create detailed mitigation plan before proceeding.

### Phase 1: Static Analysis (1 hour)

**Before changing ANY code**, understand the system:

```python
# 1. Map all dependencies
mcp__serena__find_references(
    symbol="EthicsBoundaryMiddleware",
    scope="all"
)

# 2. Understand configuration requirements
mcp__serena__find_symbol(
    name_regex="ETHICS.*|BOUNDARY.*",
    scope="config"
)

# 3. Review the test suite
mcp__serena__get_symbols_overview("tests/ethics/")
# Look for:
# - Skipped tests
# - Commented tests
# - Tests with complex setup
# - Performance tests

# 4. Check boundary definitions
mcp__serena__find_symbol(
    name_regex="BoundaryType|BoundaryLevel",
    include_body=True
)
```

**Document findings**:
- Configuration requirements
- Dependency chains
- Test coverage gaps
- Boundary strictness levels

### Phase 2: Isolated Testing (2-3 hours)

**Create a test harness BEFORE touching main.py**:

```python
# tests/test_ethics_activation.py

def test_ethics_activation_isolated():
    """Test ethics in isolation before system-wide activation"""

    # 1. Create minimal app instance
    app = create_test_app()

    # 2. Add ONLY ethics middleware
    ethics = EthicsBoundaryMiddleware()
    app.middleware.append(ethics)

    # 3. Test basic operations
    test_cases = [
        ("Hello", should_pass=True),
        ("Create GitHub issue", should_pass=True),
        ("Delete all data", should_pass=False),  # Should block
        ("Send spam", should_pass=False),  # Should block
    ]

    for input_text, should_pass in test_cases:
        result = app.process(input_text)
        assert (result.blocked is False) == should_pass

def test_ethics_performance_impact():
    """Measure performance impact"""

    app_without = create_test_app()
    app_with = create_test_app()
    app_with.middleware.append(EthicsBoundaryMiddleware())

    # Benchmark both
    time_without = benchmark(app_without, n=1000)
    time_with = benchmark(app_with, n=1000)

    # Accept up to 10% performance impact
    assert time_with < time_without * 1.1

def test_ethics_with_each_integration():
    """Test ethics doesn't break integrations"""

    for service in ['github', 'slack', 'notion', 'calendar']:
        app = create_test_app()
        app.middleware.append(EthicsBoundaryMiddleware())

        # Test service-specific operations
        test_service_operations(app, service)
```

**Run these tests BEFORE any activation**.

### Phase 3: Configuration Preparation (1 hour)

Based on testing, prepare configuration:

```python
# config/ethics_config.py

ETHICS_CONFIG = {
    # Start with permissive settings
    "boundary_strictness": "low",  # low, medium, high
    "learning_enabled": False,  # Disable adaptive learning initially
    "metrics_enabled": True,  # Enable monitoring
    "bypass_list": [],  # Emergency bypass if needed

    # Service-specific settings
    "service_overrides": {
        "github": {"strictness": "medium"},
        "slack": {"strictness": "low"},
        "notion": {"strictness": "medium"},
        "calendar": {"strictness": "low"},
    },

    # Monitoring
    "alert_threshold": 10,  # Alert if >10 blocks per minute
    "log_all_blocks": True,  # Log everything initially
}
```

### Phase 4: Staged Activation (2-3 hours)

**Stage 1: Test Environment** (30 minutes)
```python
# In test environment only
# 1. Uncomment middleware in main.py
# 2. Run ALL integration tests
pytest tests/ -v --tb=short

# 3. Check for any failures
# 4. Review blocked operations log
```

**Stage 2: Feature Flag Activation** (1 hour)
```python
# Instead of hard activation, use feature flag
if settings.ETHICS_ENABLED:  # Default False
    app.add_middleware(EthicsBoundaryMiddleware())

# This allows quick rollback without code changes
```

**Stage 3: Canary Deployment** (1 hour)
- Enable for 10% of requests initially
- Monitor for 1 hour
- Check metrics:
  - Block rate (should be <1%)
  - Performance impact (should be <10%)
  - Error rate (should be 0%)

**Stage 4: Full Activation** (30 minutes)
- Enable for 100% of requests
- Monitor closely for 24 hours
- Have rollback ready

### Phase 5: Validation & Documentation (1 hour)

**Validation Checklist**:
- [ ] All integration tests passing
- [ ] Performance within acceptable limits (<10% impact)
- [ ] Block rate reasonable (<1% for legitimate operations)
- [ ] No increase in error rates
- [ ] Monitoring dashboards operational
- [ ] Rollback procedure tested

**Documentation Required**:
- Configuration guide
- Tuning instructions
- Common issues and solutions
- Rollback procedure
- Monitoring guide

## Success Criteria

The Ethics middleware is successfully activated when:

1. **Functional**: All legitimate operations work normally
2. **Protective**: Harmful operations are blocked
3. **Performant**: <10% performance impact
4. **Monitorable**: Full visibility into decisions
5. **Tunable**: Can adjust strictness without code changes
6. **Reversible**: Can rollback in <1 minute

## Red Flags - STOP if you see these

1. **Mass test failures** when enabled
2. **Performance degradation** >20%
3. **Blocking legitimate operations** frequently
4. **Missing configuration** that can't be resolved
5. **Circular dependencies** in initialization
6. **Memory leaks** or resource exhaustion

If ANY red flag appears, STOP and report back for architectural guidance.

## Time Budget

Total estimated: 6-8 hours (1 day careful work)

- Phase -1: 1-2 hours (investigation)
- Phase 0: 30 minutes (risk assessment)
- Phase 1: 1 hour (static analysis)
- Phase 2: 2-3 hours (isolated testing)
- Phase 3: 1 hour (configuration)
- Phase 4: 2-3 hours (staged activation)
- Phase 5: 1 hour (validation)

This is NOT a race. Take the time needed to do this safely.

## Special Considerations

### Why This Is Different from MCP

**MCP Migration**: Adding/standardizing optional functionality
**Ethics Activation**: Enabling universal enforcement layer

MCP could fail partially and system still works. Ethics failure affects EVERYTHING.

### Rollback Plan

Have this ready BEFORE activation:

```bash
# Instant rollback script
#!/bin/bash

# 1. Disable feature flag
echo "ETHICS_ENABLED=False" > .env.override

# 2. Restart services
systemctl restart piper-api

# 3. Verify disabled
curl http://localhost:8080/health | grep "ethics_enabled.*false"
```

### Monitoring Requirements

Set up BEFORE activation:
- Alert on >10 blocks per minute
- Alert on performance degradation >15%
- Dashboard showing block reasons
- Log aggregation for ethics decisions

## Next Steps

1. **Start with Phase -1** (historical investigation)
2. **Report findings** before proceeding
3. **Get approval** for activation plan based on risk assessment
4. **Execute carefully** with staged approach
5. **Monitor continuously** for 24 hours post-activation

## Questions to Answer First

Before ANY code changes:

1. Why was it originally disabled?
2. What dependencies does it have?
3. What's the default strictness level?
4. How does it handle edge cases?
5. Is there a bypass mechanism for emergencies?

## Remember

This is cathedral work - the foundation of trust in the system. A properly configured ethics layer protects users and the system. An improperly configured one breaks everything.

Take your time. Test thoroughly. Have rollback ready.

Report back after Phase -1 with findings.

---

**Chief Architect**
*October 18, 2025, 11:05 AM*

*"Move carefully when activating universal enforcement."*
