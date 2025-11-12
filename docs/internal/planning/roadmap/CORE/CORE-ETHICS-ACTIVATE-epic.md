# CORE-ETHICS-ACTIVATE: Careful Activation of Universal Ethics Middleware

## Context
During CORE-GREAT-2A investigation, we discovered a sophisticated EthicsBoundaryMiddleware system that is 95% complete but temporarily disabled (main.py:169). This provides universal ethical protection for ALL integrations but was disabled for "environment setup" reasons that need investigation.

## Background
- Advanced middleware with adaptive learning, metrics monitoring
- 54KB+ test framework already exists
- Covers GitHub, Slack, Notion, Calendar, QueryRouter, OrchestrationEngine
- Sophisticated boundary detection algorithms implemented
- Only requires uncommenting one line to activate

## Why It Was Disabled
- Unknown - comment says "environment setup"
- Possibly complex dependency chains
- May have integration challenges
- Could affect performance
- Might have been too strict during development

## Acceptance Criteria
- [ ] Investigate why ethics middleware was originally disabled
- [ ] Create comprehensive test plan for activation
- [ ] Test activation in isolated environment first
- [ ] Verify no breaking changes to existing integrations
- [ ] Confirm performance remains acceptable
- [ ] Document any necessary configuration adjustments
- [ ] Successfully activate in production
- [ ] Monitor for unexpected filtering or blocks

## Tasks

### Investigation Phase
- [ ] Review git history for main.py:169 disable reason
- [ ] Check for related issues or ADRs about ethics
- [ ] Identify all dependencies of EthicsBoundaryMiddleware
- [ ] Review the 54KB test suite for clues

### Testing Phase
- [ ] Create isolated test environment
- [ ] Activate middleware in test environment
- [ ] Run integration tests for all services
- [ ] Test edge cases and boundary conditions
- [ ] Performance benchmark with ethics enabled
- [ ] Test adaptive learning features

### Activation Phase
- [ ] Document rollback procedure
- [ ] Activate in staging environment
- [ ] Monitor for 24 hours
- [ ] Address any issues found
- [ ] Activate in production with monitoring
- [ ] Document operational procedures

## Lock Strategy
- Ethics middleware cannot be disabled without approval
- Tests verify ethical boundaries enforced
- Monitoring alerts on ethics bypass attempts
- Configuration locked in production

## Success Validation
```bash
# Middleware is active
grep -v "^#.*EthicsBoundary" main.py

# All tests pass with ethics enabled
pytest tests/ethics/ -v

# Integration tests pass
pytest tests/integrations/ -v --with-ethics

# Performance acceptable
python benchmark_with_ethics.py
```

## Risk Assessment

### High Risk
- Could block legitimate operations if too strict
- May have been disabled for good reason
- Complex dependencies might break

### Medium Risk
- Performance impact unknown
- Adaptive learning might need training
- Configuration might need tuning

### Mitigation
- Careful testing in isolated environment
- Gradual rollout with monitoring
- Clear rollback procedure
- Configuration adjustments ready

## Dependencies
- Complete CORE-GREAT sequence first
- All integrations stable
- Monitoring infrastructure ready

## Estimated Duration
2-3 days of careful testing and activation

## Priority
HIGH - Required for CORE completion before alpha testing

## Related
- Parent: CORE track
- After: CORE-GREAT sequence
- Before: Alpha testing
- Related ADRs: Need to check for ethics-related ADRs

---

**Labels**: core, ethics, activation, careful-testing
