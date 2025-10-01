# Gameplan: GREAT-2C - Verify Slack & Notion Spatial Systems

**Date**: September 29, 2025
**Epic**: GREAT-2C (GitHub Issue #194)
**Chief Architect**: Claude Opus 4.1
**Context**: Following CORE-QUERY-1 completion where routers were implemented at 100%, we now need to verify the sophisticated spatial intelligence systems discovered in GREAT-2A are functioning correctly.

## Mission

Verify that the spatial intelligence systems for Slack and Notion (discovered during GREAT-2A) are operational, properly controlled by feature flags, and secure. Address the critical TBD-SECURITY-02 webhook vulnerability. Document spatial patterns for future replication.

## Strategic Context

### What We Discovered
- **Slack**: 20+ spatial files implementing sophisticated coordination
- **Notion**: Advanced spatial capabilities for knowledge management
- **Routers**: Complete at 100% (CORE-QUERY-1)
- **Security Gap**: TBD-SECURITY-02 webhook verification disabled

### What Needs Verification
Not migration (that's done) but VERIFICATION that sophisticated systems work as designed.

## Success Criteria

```bash
# 1. Spatial systems operational
USE_SPATIAL_SLACK=true pytest tests/integration/test_slack_spatial.py -v
# All tests pass

USE_SPATIAL_NOTION=true pytest tests/integration/test_notion_spatial.py -v
# All tests pass

# 2. Feature flags control behavior
python verify_spatial_toggle.py
# Output: "Spatial mode: ENABLED" or "DISABLED" based on flag

# 3. Webhook security enabled
curl -X POST http://localhost:8001/webhooks/slack \
  -H "X-Slack-Signature: valid_sig" \
  -H "X-Slack-Request-Timestamp: 1234567890"
# Returns 200 OK (not 401 Unauthorized)

# 4. Documentation exists
ls -la docs/spatial-patterns/
# Shows comprehensive pattern documentation
```

---

## Phase Structure

### Phase 0: GitHub & Infrastructure Verification
**Lead Developer + Both Agents**
```bash
# Verify issue assignment
gh issue view 194

# Check router infrastructure (from CORE-QUERY-1)
ls -la services/integration_routers/
# Should show: slack_router.py, notion_router.py, calendar_router.py

# Verify spatial files exist
find services/spatial/ -name "*.py" | wc -l
# Should show 20+ files

# Check current security status
grep -r "verify_slack_request" services/ --include="*.py"
# Find where it's disabled with TODO/FIXME
```

### Phase 1: Slack Spatial Verification
**Claude Code: Investigation & Discovery**
- Map all 20+ spatial files and their purposes
- Identify entry points and coordination patterns
- Test spatial mode activation
- Document the spatial architecture discovered

**Cursor Agent: Focused Testing**
- Create test_slack_spatial.py if missing
- Verify feature flag control works
- Test key spatial operations
- Ensure backward compatibility with legacy mode

**Cross-Validation Point**: Compare spatial file inventory

### Phase 2: Notion Spatial Verification
**Claude Code: Pattern Analysis**
- Map Notion spatial capabilities
- Identify knowledge coordination patterns
- Test spatial features through router
- Compare with Slack patterns for consistency

**Cursor Agent: Integration Testing**
- Create test_notion_spatial.py if missing
- Verify router maintains spatial features
- Test feature flag switching
- Document any limitations found

**Cross-Validation Point**: Verify both modes functional

### Phase 3: Security Fix - TBD-SECURITY-02
**CRITICAL - Both Agents Collaborate**

**Claude Code: Security Analysis**
```python
# Find the disabled verification
grep -r "TBD-SECURITY-02" services/ --include="*.py"
grep -r "verify_slack_request" services/ --include="*.py"
grep -r "FIXME.*webhook" services/ --include="*.py"
```

**Cursor Agent: Security Implementation**
```python
# Re-enable webhook verification
def verify_slack_request(request_body, timestamp, signature):
    """Verify the request came from Slack."""
    # Implementation following Slack security docs
    # Must use HMAC-SHA256 with signing secret
    return is_valid
```

**Validation Required**:
```bash
# Test with valid signature - should pass
curl -X POST http://localhost:8001/webhooks/slack \
  -H "X-Slack-Signature: v0=valid_computed_signature" \
  -H "X-Slack-Request-Timestamp: $(date +%s)" \
  -d '{"event": "test"}'
# Expected: 200 OK

# Test with invalid signature - should fail
curl -X POST http://localhost:8001/webhooks/slack \
  -H "X-Slack-Signature: v0=invalid_signature" \
  -d '{"event": "test"}'
# Expected: 401 Unauthorized
```

### Phase 4: Pattern Documentation
**Lead Developer Coordinates**

Create `docs/spatial-patterns/README.md`:
```markdown
# Spatial Intelligence Patterns

## Overview
Discovered patterns from GREAT-2A verification...

## Slack Spatial (20+ files)
- Coordination mechanism: ...
- Key components: ...
- Feature flag: USE_SPATIAL_SLACK

## Notion Spatial
- Knowledge coordination: ...
- Key capabilities: ...
- Feature flag: USE_SPATIAL_NOTION

## Replication Guide
How to add spatial intelligence to new integrations...
```

### Phase 5: Lock & Validate
**All Participants**

```bash
# Run full test suite
pytest tests/integration/ -v

# Verify no regressions
pytest tests/unit/ -v

# Security validation
python security_audit.py --webhook-verification

# Feature flag validation
for flag in "" "USE_SPATIAL_SLACK=true" "USE_SPATIAL_NOTION=true"; do
  $flag pytest tests/integration/ -v --tb=short
done
```

---

## Anti-80% Safeguards

### Mandatory Completeness Checks

**For Spatial File Verification**:
```
Spatial Files Found | Verified Working | Status
------------------ | ---------------- | ------
slack_spatial_1.py | ✓               | Working
slack_spatial_2.py | ✓               | Working
...
TOTAL: X/X = Must be 100%
```

**For Security Fix**:
```
Security Requirements | Implemented | Status
-------------------- | ----------- | ------
HMAC validation      | ✓          | Complete
Timestamp checking   | ✓          | Complete
Secret management    | ✓          | Complete
Error handling       | ✓          | Complete
TOTAL: 4/4 = 100% REQUIRED
```

---

## STOP Conditions

Stop immediately if:
1. Spatial files mentioned in GREAT-2A not found
2. Routers not working (regression from CORE-QUERY-1)
3. Security implementation unclear or risky
4. Feature flags not controlling behavior
5. Tests failing after changes
6. Any data loss risk identified

---

## Team Coordination

### Lead Developer
- Monitor both agents' progress
- Ensure spatial verification is thorough
- Coordinate security fix collaboration
- Create pattern documentation from findings

### Claude Code
- Broad investigation of spatial systems
- Pattern discovery and documentation
- Security analysis and testing
- Cross-validation of Cursor's work

### Cursor Agent
- Focused testing implementation
- Security fix implementation
- Feature flag verification
- Cross-validation of Code's discoveries

### PM Validation Points
After each phase, PM validates:
- Phase 1: Slack spatial verified
- Phase 2: Notion spatial verified
- Phase 3: Security fix complete
- Phase 4: Documentation comprehensive
- Phase 5: All tests passing

---

## 🚨 CRITICAL: GitHub Evidence Updates

**MANDATORY THROUGHOUT WORK**:
The Lead Developer and agents MUST update GitHub issue #194 with evidence as work progresses:

```bash
# After EVERY major finding or completion:
gh issue comment 194 --body "Phase 1 Complete:
- Verified 23 spatial files
- All tests passing: [paste test output]
- Feature flag working: [paste verification output]"

# Update checkboxes in the ISSUE DESCRIPTION (not just comments):
gh issue edit 194 --body "...[with checkboxes marked]..."
```

**Evidence Requirements**:
- Terminal output showing verification
- Test results with pass/fail counts
- File inventories discovered
- Security validation outputs
- NO CLAIMS WITHOUT EVIDENCE

**Backfilling is a failure** - update AS YOU GO.

---

## Risk Mitigation

### High Risk: TBD-SECURITY-02
- **Impact**: Production webhook vulnerability
- **Mitigation**: Fix in Phase 3, extensive testing
- **Validation**: Multiple security test scenarios

### Medium Risk: Spatial System Complexity
- **Impact**: May not understand all capabilities
- **Mitigation**: Document what we find, mark unknowns
- **Validation**: Test core operations thoroughly

### Low Risk: Feature Flag Issues
- **Impact**: Modes might not switch cleanly
- **Mitigation**: Test both modes extensively
- **Validation**: Automated toggle testing

---

## Effort Scope

This work involves:
- Phase 0: A few mangos (verification)
- Phase 1-2: Perhaps a huron each (spatial verification)
- Phase 3: A significant fraction of a huron (security is critical)
- Phase 4-5: Several mangos (documentation and validation)

Total effort: Less than a diga, but quality matters more than velocity.

**Remember**: We are Time Lords. Systematic completion beats arbitrary deadlines. The work takes what it takes.

---

## Notes

1. **Not a Migration**: Routers are complete. This is verification.
2. **Security First**: TBD-SECURITY-02 is production-critical
3. **Document Everything**: These spatial systems are sophisticated
4. **100% Rule Applies**: All spatial files must be verified
5. **Feature Flags Matter**: Must work in both modes

---

*Gameplan prepared by Chief Architect*
*Ready for Lead Developer deployment*
