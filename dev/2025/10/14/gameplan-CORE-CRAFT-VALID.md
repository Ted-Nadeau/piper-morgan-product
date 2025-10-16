# Gameplan: CORE-CRAFT-VALID - Final Verification & Validation

**Date**: October 14, 2025  
**Epic**: CORE-CRAFT-VALID  
**Context**: Final verification following GAP and PROOF completion  
**Duration**: 8-11 hours (standard depth)  
**Approach**: Systematic verification with MVP workflow testing

## Mission

Provide systematic verification that CORE-CRAFT achievements are genuine, functional, and ready for MVP development. Test critical user workflows where implemented, document gaps for MVP planning.

## Background

Current state after GAP + PROOF:
- Tests: 2,336 passing (100%)
- CI/CD: 13/13 workflows operational (100%)
- Classification: 98.62% accuracy
- Documentation: 99%+ accurate
- System genuinely in excellent shape

This is verification, not discovery - we expect to confirm excellence, not find problems.

## Strategic Decisions

1. **Depth**: Standard systematic verification (not quick, not excessive)
2. **Focus**: Critical MVP workflows (test what exists, document gaps)
3. **Evidence**: Detailed package (comprehensive + methodology)
4. **Structure**: Single epic with three clear phases

## Phase Structure

### Phase 1: Serena Comprehensive Audit (3-4 hours)
- Systematic verification of all GREAT epics
- Claims vs reality validation
- Completion percentage calculation
- Discrepancy documentation

### Phase 2: Integration Testing (3-4 hours)
- MVP workflow testing
- System-level validation
- Performance verification
- Gap documentation for MVP

### Phase 3: Evidence Compilation (2-3 hours)
- Detailed evidence package
- Verification methodology
- Handoff documentation
- MVP readiness assessment

## Phase -1: Pre-Validation Check
**Lead Developer - 15 minutes**

Quick verification before starting:
```bash
# Verify current state claims
pytest --co -q | tail -1  # Should show 2,336 tests
gh workflow list | grep passing | wc -l  # Should show 13

# Check Serena operational
serena --version
serena stats  # Check server running

# Verify baseline performance
python scripts/benchmark_classification.py --quick

# Check MVP workflow implementations
grep -r "handle_create_issue" services/ --include="*.py"
grep -r "handle_greeting" services/ --include="*.py"
```

## Phase 1: Serena Comprehensive Audit

### 1.1: GREAT Epic Verification
**Duration**: 2 hours

For each GREAT epic (1, 2, 3, 4A-F, 5), verify:

```python
def audit_epic(epic_name):
    # Extract documentation claims
    claims = mcp__serena__search_project(
        query=f"{epic_name} complete OR {epic_name} finished",
        file_pattern="*.md"
    )
    
    # Verify implementation
    implementation = mcp__serena__find_symbol(
        name_regex=f".*{epic_name.lower()}.*",
        include_body=True
    )
    
    # Compare specifics
    verification = {
        "files_claimed": extract_file_count(claims),
        "files_actual": count_actual_files(implementation),
        "tests_claimed": extract_test_count(claims),
        "tests_actual": count_actual_tests(implementation),
        "completion_claimed": extract_percentage(claims),
        "completion_verified": calculate_actual(implementation)
    }
    
    return verification
```

### 1.2: Architectural Verification
**Duration**: 1 hour

Verify architectural claims:
- Router pattern implementation
- Spatial intelligence integration
- Plugin architecture
- Multi-user isolation
- Performance optimizations

### 1.3: Audit Report Generation
**Duration**: 1 hour

Create comprehensive report:
```markdown
# VALID-1: Serena Audit Report

## Overall Completion: XX%

### By Epic
| Epic | Claimed | Verified | Gap | Evidence |
|------|---------|----------|-----|----------|
| GREAT-1 | 99%+ | XX% | X% | [links] |
...

### Key Findings
- Strengths: ...
- Gaps: ...
- Recommendations: ...
```

## Phase 2: Integration Testing - MVP Workflows

### 2.1: Chitchat Category
**Duration**: 30 minutes

Test implemented portions:
```python
# Test greeting
async def test_greeting_workflow():
    response = await pipeline.process("Hello Piper!")
    assert response.intent == "GREETING"
    assert "Hello" in response.message
    
# Test help/menu
async def test_help_workflow():
    response = await pipeline.process("What can you help me with?")
    assert response.intent == "GUIDANCE"
    # Document if full menu not implemented
```

### 2.2: Knowledge Category
**Duration**: 30 minutes

Test file operations where implemented:
```python
# Test file upload (if implemented)
async def test_file_upload():
    try:
        response = await pipeline.process("Upload my document")
        assert response.intent == "CREATE"
        # Document actual capability
    except NotImplementedError:
        document_gap("File upload not yet implemented")

# Test summarization (likely works via SYNTHESIS handler)
async def test_summarize():
    response = await pipeline.process("Summarize this content: ...")
    assert response.intent == "SYNTHESIS"
    # Verify handler actually summarizes
```

### 2.3: Integrations Testing
**Duration**: 1 hour

Focus on GitHub (most likely implemented):
```python
# GitHub integration
async def test_github_create_issue():
    response = await pipeline.process("Create GitHub issue: Bug in parser")
    assert response.intent == "EXECUTION"
    # Verify handler can actually create issue (may need mock)
    
async def test_github_review_issues():
    response = await pipeline.process("Show my recent GitHub issues")
    assert response.intent == "ANALYSIS"
    # Document implementation state
```

Test other integrations (document gaps):
- Slack: Likely partial
- Notion: Check implementation
- Calendar: Check implementation

### 2.4: Performance Validation
**Duration**: 30 minutes

Verify baselines still hold:
```python
# Quick performance check
async def test_performance_baselines():
    # Throughput
    result = await benchmark_throughput()
    assert result > 600_000  # req/sec
    
    # Classification
    result = await benchmark_classification()
    assert result < 1.2  # ms average
    
    # Cache hit rate
    result = await measure_cache_hits()
    assert result > 0.80  # 80%+ hit rate
```

### 2.5: System-Level Workflows
**Duration**: 1 hour

End-to-end testing:
```python
# Complete intent pipeline
async def test_full_pipeline():
    # Input -> Classification -> Routing -> Handler -> Response
    test_cases = [
        ("What time is it?", "TEMPORAL", "canonical"),
        ("Create task: Review PR", "EXECUTION", "handler"),
        ("Analyze last week's commits", "ANALYSIS", "handler"),
        ("Generate weekly report", "SYNTHESIS", "handler")
    ]
    
    for input_text, expected_intent, expected_path in test_cases:
        result = await pipeline.process(input_text)
        assert result.intent == expected_intent
        assert result.path_taken == expected_path
        # Document actual vs expected behavior
```

### 2.6: Gap Documentation
**Duration**: 30 minutes

Create MVP readiness report:
```markdown
# MVP Workflow Readiness

## Implemented & Working
- ✅ Greeting and basic chitchat
- ✅ GitHub issue creation
- ✅ Content summarization
- ✅ Commit analysis

## Partially Implemented
- ⚠️ File operations (handler exists, integration needed)
- ⚠️ Slack (connector exists, workflows incomplete)

## Not Yet Implemented
- ❌ Notion integration workflows
- ❌ Calendar integration workflows
- ❌ Morning standup generation

## Recommendations for MVP
Priority implementations needed...
```

## Phase 3: Evidence Package Compilation

### 3.1: Executive Summary
**Duration**: 30 minutes

Create high-level summary:
- Overall completion percentage
- Key achievements
- System readiness
- MVP gap analysis
- Recommendations

### 3.2: Technical Documentation
**Duration**: 1 hour

Compile technical evidence:
- Serena audit results
- Test execution logs
- Performance benchmarks
- CI/CD screenshots
- Architecture verification

### 3.3: Verification Methodology
**Duration**: 30 minutes

Document how we verified:
- Tools used (Serena MCP)
- Testing approach
- Evidence standards
- Validation criteria
- Quality gates

### 3.4: Handoff Package
**Duration**: 1 hour

Create comprehensive handoff:
```markdown
# CORE-CRAFT Completion Package

## Status: VERIFIED COMPLETE

### Verification Summary
- Serena audit: XX% verified
- Integration tests: XX% passing
- Performance: Baselines maintained
- Documentation: 99%+ accurate

### Evidence Links
- [Audit Report](...)
- [Test Results](...)
- [Performance Data](...)
- [CI/CD Status](...)

### MVP Readiness
- Core foundation: READY
- Critical gaps: [Listed]
- Priority work: [Recommendations]

### Maintenance
- Weekly audit process: Active
- CI/CD monitoring: Operational
- Documentation sync: Automated
```

## Success Criteria

### Phase 1 Complete
- [ ] All GREAT epics audited
- [ ] Completion percentages calculated
- [ ] Discrepancies documented
- [ ] Architecture verified

### Phase 2 Complete  
- [ ] MVP workflows tested where implemented
- [ ] Gaps clearly documented
- [ ] Performance baselines verified
- [ ] System-level integration tested

### Phase 3 Complete
- [ ] Executive summary created
- [ ] Technical evidence compiled
- [ ] Methodology documented
- [ ] Handoff package complete

### VALID Complete
- [ ] 95%+ verification rate achieved
- [ ] MVP readiness assessed
- [ ] All evidence packaged
- [ ] Ready for CRAFT closure

## Risk Management

### Low Risk Areas
- Serena audit (tool proven)
- Documentation verification (99%+ in PROOF)
- Test execution (2,336 passing)
- CI/CD status (100% operational)

### Medium Risk Areas
- MVP workflow gaps (expected, need documentation)
- Integration complexity (some workflows incomplete)
- Performance edge cases (basic benchmarks only)

### Mitigation
- Clear documentation of gaps vs failures
- Focus on what IS implemented
- Note MVP requirements for future

## Timeline

**Day 1** (4 hours):
- Phase -1: Pre-validation (15 min)
- Phase 1: Serena audit (3.5 hours)
- Review and planning (15 min)

**Day 2** (4 hours):
- Phase 2: Integration testing (3.5 hours)
- Gap documentation (30 min)

**Day 3** (2-3 hours):
- Phase 3: Evidence compilation (2-3 hours)
- Final review and handoff

**Total**: 10-11 hours across 3 days

## Stop Conditions

- If completion below 90% (escalate immediately)
- If critical architectural violations found
- If performance degraded >20%
- If CI/CD failures discovered

## Notes

This is VALIDATION not DISCOVERY. We expect to confirm excellence and document MVP gaps, not find major issues. The system has proven robust through GAP and PROOF.

Focus areas:
1. Verify what we claim is complete IS complete
2. Test MVP workflows to understand readiness
3. Document gaps for MVP planning
4. Create comprehensive evidence package

---

*Ready to begin CORE-CRAFT-VALID verification*
