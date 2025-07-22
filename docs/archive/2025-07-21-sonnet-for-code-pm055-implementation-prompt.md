# Claude Code Task: PM-055 Python Version Consistency Implementation

## CRITICAL: REVIEW GITHUB ISSUE #23 FIRST

**MANDATORY FIRST STEPS:**
1. **Read GitHub Issue #23 completely** - including all comments and preparation work
2. **Review Cursor's Implementation Readiness Report** (added Monday 5:29 PM)
3. **Incorporate preparation findings** into your implementation approach
4. **Follow recommended implementation sequence** from preparation analysis

**DO NOT proceed until you have reviewed all GitHub issue content and preparation work.**

---

## CONTEXT
Monday's PM-055 blocker mitigation cleared immediate test compatibility issues. Cursor's comprehensive preparation scouting (GitHub issue #23) provides implementation roadmap, risk assessment, and environment analysis for systematic Python version consistency implementation.

## TASK OBJECTIVE
Implement PM-055 Python version consistency across all environments following Cursor's preparation roadmap and resolving the asyncio.timeout bug root cause.

## PREPARATION WORK INTEGRATION

### From Cursor's Readiness Report (Reference GitHub #23)
**Current State** (per preparation analysis):
- Development: Python 3.9.6 detected
- Target: Python 3.11.x recommended
- Risk Assessment: **LOW** (no version-specific code found)
- Implementation Complexity: **MEDIUM** (environment sync required)

**Recommended Implementation Sequence** (from preparation):
1. Add .python-version file with 3.11.x
2. Update Dockerfile to python:3.11-slim-buster
3. Update CI/CD workflow Python version specification
4. Update documentation and onboarding
5. Full test suite validation under 3.11
6. Rollback plan execution if needed

## IMPLEMENTATION APPROACH

### Phase 1: Version Declaration
**Based on Preparation Recommendations:**

```bash
# 1. Add .python-version file
echo "3.11.9" > .python-version

# 2. Update pyproject.toml (if exists) with python_requires
[project]
requires-python = ">=3.11"
```

### Phase 2: Environment Alignment
**Following Preparation Roadmap:**

```dockerfile
# Update Dockerfile
FROM python:3.11-slim-buster

# Maintain existing build patterns but with 3.11 base
```

```yaml
# Update CI/CD workflows (.github/workflows/)
- uses: actions/setup-python@v4
  with:
    python-version: '3.11'
```

### Phase 3: Validation and Testing
**Per Preparation Risk Assessment:**

```bash
# Critical validation steps from preparation analysis
python3.11 -m pytest tests/ -v
python3.11 -m pytest tests/infrastructure/mcp/ -v  # High risk area identified
python3.11 -m pytest tests/services/analysis/ -v   # AsyncIO compatibility area
```

### Phase 4: Documentation Updates
**Following Preparation Developer Workflow Analysis:**

- README.md: Update Python version requirements
- Developer onboarding: Python 3.11 setup instructions
- Contribution guidelines: Version consistency requirements
- Troubleshooting: Common version mismatch solutions

## SUCCESS CRITERIA FROM PREPARATION

**Per Cursor's Analysis:**
- [ ] All tests pass under Python 3.11 in dev, Docker, and CI
- [ ] No new version-specific bugs introduced
- [ ] Documentation and onboarding updated for 3.11
- [ ] AsyncIO/asyncpg/SQLAlchemy compatibility confirmed (high risk areas)
- [ ] Rollback plan available if critical failures occur

## RISK MITIGATION STRATEGY

**From Preparation Risk Assessment:**
- **High Risk Areas**: AsyncIO/asyncpg/SQLAlchemy patterns
- **Mitigation**: Run comprehensive tests under 3.11 before merging
- **Rollback Plan**: Revert Dockerfile, .python-version, CI config if needed
- **Dependency Strategy**: Pin versions as needed for 3.11 compatibility

## COORDINATION NOTES

### Building on Monday's Work
- **Blocker Mitigation**: Completed by Code (AsyncMock, async fixtures, SQLAlchemy)
- **Preparation Analysis**: Completed by Cursor (environment audit, roadmap)
- **Implementation**: Systematic execution following preparation guidance

### GitHub Issue Integration
- **Document progress** in GitHub issue #23 comments
- **Reference preparation findings** in implementation notes
- **Update status** as each phase completes
- **Note any deviations** from preparation recommendations with rationale

## VERIFICATION APPROACH

### Pre-Implementation Checklist
- [ ] GitHub issue #23 reviewed completely
- [ ] Preparation report findings incorporated
- [ ] Implementation sequence confirmed
- [ ] Risk areas identified and mitigation planned

### Implementation Validation
- [ ] Version consistency across all environments confirmed
- [ ] Test suite passes under Python 3.11
- [ ] High-risk areas (AsyncIO, SQLAlchemy) validated
- [ ] Documentation updated with new requirements

### Success Confirmation
- [ ] AsyncIO.timeout bug root cause resolved
- [ ] Development/production version consistency achieved
- [ ] Team onboarding updated for version requirements
- [ ] Rollback plan tested and available

## EXPECTED DELIVERABLES

1. **Updated Environment Specifications** (.python-version, Dockerfile, CI/CD)
2. **Comprehensive Testing Validation** under Python 3.11
3. **Updated Documentation** (README, onboarding, contribution guidelines)
4. **Implementation Report** documenting how preparation work influenced execution
5. **Success Confirmation** that asyncio.timeout bug root cause is resolved

---

**REMINDER: This implementation builds directly on Cursor's excellent preparation work. Review GitHub issue #23 completely before proceeding to ensure systematic coordination and maximum implementation velocity.**

*[This prompt will be updated if intervening knowledge changes requirements before Wednesday deployment]*
