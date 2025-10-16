# Gameplan: Sprint A2 - Notion & Errors

**Sprint**: A2  
**Duration**: 2 days  
**Start**: October 15, 2025  
**Context**: CRAFT complete, following established Alpha roadmap  
**Mission**: Complete Notion fixes and error standardization per plan

## Background

CRAFT discovered production handlers exist, but we're following our Alpha plan systematically. No skipping - everything gets verified properly.

Sprint A2 items from the roadmap:
- CORE-NOTN #142 (5h) - API connectivity fix
- CORE-NOTN #136 (1d) - Remove hardcoding  
- CORE-NOTN #165 (1d) - Database API upgrade
- CORE-INT #109 (5h) - Legacy deprecation verification
- MVP-ERROR-STANDARDS (1-2d) - Standardize errors


## Day 1: Notion Focus (Oct 15)

### Phase 1: CORE-NOTN #142 - API Connectivity
**Duration**: 5 hours  
**Issue**: Notion API connectivity problems

Tasks:
- Investigate current Notion integration state
- Verify plugin wrapper from GREAT-3
- Fix API connectivity issues
- Test with actual Notion API (if credentials available)
- Document configuration requirements

### Phase 2: CORE-NOTN #136 - Remove Hardcoding
**Duration**: Remainder of day  
**Issue**: Hardcoded values in Notion integration

Tasks:
- Identify all hardcoded values
- Move to configuration
- Update PIPER.user.md if needed
- Test configuration loading
- Verify no regressions

## Day 2: Notion Completion + Errors (Oct 16)

### Phase 3: CORE-NOTN #165 - Database API Upgrade
**Duration**: 4 hours  
**Issue**: Notion database API needs upgrade

Tasks:
- Review current database integration
- Upgrade to latest Notion API version
- Update database query methods
- Test database operations
- Document breaking changes

### Phase 4: CORE-INT #109 - Legacy Deprecation
**Duration**: 5 hours  
**Issue**: Verify legacy code properly deprecated

Tasks:
- Audit for legacy integration patterns
- Verify all using router pattern
- Remove deprecated code paths
- Update tests
- Document removals

### Phase 5: MVP-ERROR-STANDARDS
**Duration**: Remainder of day (start, continue in A3 if needed)  
**Issue**: Standardize error responses

Tasks:
```python
# Implement standard error format
{
    "error": {
        "code": "INTENT_NOT_FOUND",
        "message": "Unable to classify intent",
        "details": {...}
    }
}
```
- Define error code constants
- Update all endpoints
- Test error scenarios
- Document error codes

## Success Criteria

### Sprint Complete When

**Notion Issues Resolved**:
- [ ] #142: API connectivity working
- [ ] #136: No hardcoded values remain
- [ ] #165: Database API upgraded
- [ ] #109: Legacy code removed

**Error Standards**:
- [ ] MVP-ERROR-STANDARDS implemented
- [ ] All endpoints use standard format
- [ ] Error codes documented

**Quick Fix**:
- [ ] CORE-TEST-CACHE resolved

## Verification Points

### DO NOT SKIP - VERIFY EVERYTHING

Even though CRAFT found handlers exist:
1. **Test each Notion operation** - handler may exist but not be wired
2. **Verify error propagation** - standards must work end-to-end
3. **Check integration points** - plugin to handler connections
4. **Document gaps** - what needs configuration vs code

## Next Sprint Preview: A3 Core Activation

Following the roadmap exactly:
- CORE-MCP-MIGRATION #198 - Model Context Protocol
- CORE-ETHICS-ACTIVATE #197 - Ethics middleware
- CORE-KNOW #99 - Connect knowledge graph
- CORE-KNOW-BOUNDARY #226

No shortcuts - each item gets proper attention.

## Notes on MVP Discovery

While executing A2, we'll note (but not act on):
- Which handlers actually work
- What configuration is needed
- MVP readiness indicators
- Potential accelerations

This information will be valuable but won't change our Alpha plan execution.

## Risk Management

### Low Risk
- TEST-CACHE (isolated issue)
- Hardcoding removal (straightforward)
- Error standards (clear requirements)

### Medium Risk
- Notion API changes (may have evolved)
- Database operations (complex API)
- Legacy deprecation (may touch many files)

### Mitigation
- Test with mocks if no API credentials
- Document all Notion requirements
- Keep legacy code commented until verified

## The Inchworm Way

We're following the plan systematically:
1. Complete A2 items 100%
2. No skipping even if handlers exist
3. Document everything discovered
4. Move to A3 only when A2 complete

The CRAFT discoveries are exciting but don't change our methodical approach. We'll reach MVP when we reach it - quality over speed.

---

*Ready for Sprint A2 - Notion & Errors per the plan*