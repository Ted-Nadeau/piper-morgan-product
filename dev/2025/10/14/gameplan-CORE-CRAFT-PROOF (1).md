# Gameplan: CORE-CRAFT-PROOF - Documentation & Test Precision

**Date**: October 13, 2025  
**Epic**: CORE-CRAFT-PROOF  
**Context**: Following GAP completion, address 5-10% documentation/test gaps across GREAT epics  
**Duration**: 15-25 hours estimated (accounting for potential discoveries)

## Mission

Achieve 99%+ verified completion across all GREAT epics through systematic documentation updates, test precision improvements, and infrastructure completion. Apply GAP learnings: reconnaissance first, push to 100%, follow the smoke.

## Background

GAP revealed critical patterns:
- Documentation drift: Claimed 89.3% accuracy, actual was 96.55%
- Hidden issues: 2-year library gap, silent CI failures
- Final 5% matters: Production bug found pushing to 100%
- Prevention needed: Systems to catch future drift

## Structure

### Three Stages Approach

**Stage 1: Discovery** (PROOF-0)
- Reconnaissance with Serena
- Find all gaps before planning
- 2-3 hours

**Stage 2: Documentation** (PROOF-1,3,8,9)  
- Fix documentation drift
- Complete ADRs
- Establish sync process
- 8-12 hours

**Stage 3: Precision** (PROOF-2,4,5,6,7)
- Test precision improvements
- CI/CD completion
- Performance validation
- 8-12 hours

## Phase -1: Pre-Reconnaissance Check
**Lead Developer - 15 minutes**

Quick verification before deploying agents:
```bash
# Verify Serena is operational
serena --version

# Check documentation locations
ls -la docs/architecture/
ls -la docs/adrs/
find . -name "GREAT-*" -type f | head -20

# Verify CI/CD status
gh workflow list
gh workflow run list --limit 5

# Check current test count
pytest --collect-only 2>/dev/null | tail -1
```

## PROOF-0: Reconnaissance & Discovery
**Both Agents with Serena - 2-3 hours**

### Systematic Documentation Audit

Using Serena MCP, create comprehensive gap inventory:

```python
# For each GREAT epic
for epic in ["GREAT-1", "GREAT-2", "GREAT-3", "GREAT-4*", "GREAT-5"]:
    # Find all documentation
    mcp__serena__search_project(
        query=f"{epic}",
        file_pattern="*.md"
    )
    
    # Extract all claims
    # Compare to actual code
    # Document discrepancies
```

### Required Discoveries

1. **Documentation Drift Inventory**
   - Claims vs reality for each GREAT epic
   - Line counts claimed vs actual
   - Test counts claimed vs actual
   - File inventories accuracy

2. **ADR Status**
   ```python
   mcp__serena__find_files(
       pattern="ADR-*.md",
       relative_path="docs/adrs/"
   )
   # Check completion status of each
   ```

3. **Test Precision Issues**
   ```python
   # Find permissive test patterns
   mcp__serena__search_project(
       query="assert.*in [200, 404]|assert.*or",
       file_pattern="test_*.py"
   )
   ```

4. **CI/CD Status**
   - Current workflow status (expect 7/9 passing)
   - Nature of 2 failures
   - Fix complexity assessment

### Output: Gap Inventory Report

```markdown
## PROOF Gap Inventory

### Documentation Drift
| Epic | Claim Type | Claimed | Actual | Gap | Priority |
|------|------------|---------|--------|-----|----------|
| GREAT-1 | Test count | 45 | 52 | -7 | High |
| GREAT-1 | Lines | 2,000 | 2,347 | -347 | Low |
...

### ADR Gaps
| ADR | Status | Completion | Action Needed |
|-----|--------|------------|---------------|
| ADR-032 | Outdated | 60% | Update for QueryRouter |
...

### Test Precision Issues
- 23 tests with permissive assertions
- 5 tests checking structure not function
- 12 tests with outdated comments

### CI/CD Gaps
- Test workflow: Needs API mocking
- Architecture: 9 violations to fix

### Estimated Additional Work
- Discovered issues: ~5-8 hours
- Original scope: 9-15 hours
- New total: 14-23 hours
```

## STOP Gate: Reconnaissance Review
**PM + Lead Dev - 30 minutes**

Review PROOF-0 discoveries:
- Any critical issues requiring immediate attention?
- Adjust scope based on findings?
- Proceed with original plan or revise?

If discoveries exceed 30 hours of work, STOP and replan.

## Stage 2: Documentation (PROOF-1,3,8,9)

### PROOF-1: GREAT-1 Documentation
**Duration**: 1-2 hours

```python
# Use Serena to get exact counts
mcp__serena__find_files(
    pattern="*.py",
    relative_path="services/query_router/"
)

# Count actual lines
mcp__serena__count_lines(
    pattern="*.py",
    relative_path="services/query_router/"
)
```

Update:
- architecture.md with current QueryRouter details
- ADR-032 with restoration decisions
- Troubleshooting guide
- Performance metrics

### PROOF-3: GREAT-3 Plugin Polish  
**Duration**: 2-4 hours

Verify and update:
- Plugin test count (claimed 92)
- Developer guide examples
- Performance overhead metrics
- Plugin catalog completeness

### PROOF-8: ADR Completion
**Duration**: 3-4 hours

Complete outstanding ADRs:
- ADR-032: QueryRouter restoration
- ADR-039: Classification accuracy
- 4-6 others from gap inventory

Template for each:
```markdown
# ADR-XXX: [Decision]

## Status
Accepted/Superseded/Deprecated

## Context
[Problem requiring decision]

## Decision
[What we decided]

## Consequences
[Impact of decision]

## Evidence
[Proof it works]
```

### PROOF-9: Documentation Sync Process
**Duration**: 2-3 hours

Establish process to prevent future drift:

1. **Automated Metrics**
   ```python
   # Script to update docs/metrics.md
   def update_metrics():
       test_count = count_tests()
       line_count = count_lines()
       accuracy = measure_accuracy()
       update_markdown(test_count, line_count, accuracy)
   ```

2. **Git Hooks**
   ```bash
   # Pre-commit hook to check doc updates
   if code_changed and not docs_changed:
       warn "Code changed but docs not updated"
   ```

3. **Weekly Audit Process**
   - Monday: Run Serena audit
   - Compare to previous week
   - Update drift log
   - Create issues for gaps

## Stage 3: Precision (PROOF-2,4,5,6,7)

### PROOF-2: GREAT-2 Test Precision
**Duration**: 2-3 hours

Fix permissive patterns:
```python
# Before (permissive)
assert response.status_code in [200, 404]

# After (precise)
assert response.status_code == 200  # Expecting success
```

Tasks:
- Router test count reconciliation
- Spatial intelligence coverage
- ConfigValidator verification

### PROOF-4: GREAT-4C Multi-User
**Duration**: 1-2 hours

Validation testing:
```python
async def test_multi_user_isolation():
    users = [create_user(f"user{i}") for i in range(10)]
    sessions = [create_session(u) for u in users]
    
    # Concurrent operations
    results = await asyncio.gather(*[
        session.execute_intent("STATUS") 
        for session in sessions
    ])
    
    # Verify isolation
    assert_no_data_leakage(results)
```

### PROOF-5: GREAT-4E Test Infrastructure
**Duration**: 2-3 hours

Reconcile claims:
- Test count verification
- 600K req/sec validation
- Execution time metrics
- Operational documentation

### PROOF-6: GREAT-5 Performance
**Duration**: 1 hour

Final precision:
- Benchmark updates
- CI/CD metrics (now operational!)
- Prevention system documentation

### PROOF-7: CI/CD Completion
**Duration**: 3-4 hours

Fix 2 remaining workflows:

**Option A: Mock for CI**
```python
# conftest.py for CI environment
if os.getenv('CI'):
    mock_llm_responses()
```

**Option B: Fix violations**
- Refactor 9 direct adapter imports
- Use router pattern consistently

## Phase Z: Completion Protocol

### Verification with Serena
```python
# Final audit
mcp__serena__audit_documentation(
    verify_claims=True,
    check_drift=True,
    validate_tests=True
)
```

### Evidence Package
1. Before/after documentation diffs
2. Test precision improvements
3. CI/CD green screenshots
4. ADR completion list
5. Sync process documentation

### Handoff
- PROOF complete metrics
- Remaining gaps (if any)
- Ready for VALID phase

## Success Criteria

### Stage Completion Gates

**PROOF-0 Complete**:
- [ ] Gap inventory documented
- [ ] Hidden issues discovered
- [ ] Scope adjusted if needed

**Stage 2 Complete**:
- [ ] Documentation drift eliminated
- [ ] ADRs complete or gaps documented  
- [ ] Sync process established

**Stage 3 Complete**:
- [ ] Tests precise (no permissive patterns)
- [ ] CI/CD 9/9 or documented
- [ ] Performance validated

**PROOF Complete**:
- [ ] 99%+ documentation accuracy
- [ ] Zero undocumented gaps
- [ ] Prevention systems active
- [ ] Evidence package complete

## Risk Mitigation

1. **Hidden Issues** (High probability based on GAP)
   - Mitigation: PROOF-0 reconnaissance
   - Budget: +50% time for discoveries

2. **CI/CD Complexity** (Medium)
   - Mitigation: Timebox to 4 hours
   - Fallback: Document as technical debt

3. **Documentation Structure** (Low)
   - Mitigation: Work with existing structure
   - Defer restructuring to separate epic

## Agent Division

**Both Agents**: PROOF-0 reconnaissance
**Code Agent**: Test precision fixes, CI/CD work
**Cursor Agent**: Documentation updates, ADR completion
**Both Agents**: Final verification

## Timeline

- **Day 1**: PROOF-0 + Stage 2 start (8 hours)
- **Day 2**: Stage 2 complete + Stage 3 start (8 hours)  
- **Day 3**: Stage 3 complete + verification (4-8 hours)

Total: 20-24 hours across 2-3 days

---

*Ready to begin PROOF reconnaissance*
