# Code Agent Prompt: Verify & Close Issue #109 - GitHub Legacy Deprecation

**Date**: October 15, 2025, 5:08 PM
**Sprint**: A2 - Notion & Errors
**Issue**: CORE-INT #109 - GitHub Legacy Integration Deprecation Strategy
**Phase**: Closure Verification
**Duration**: 30-45 minutes
**Agent**: Code Agent

---

## Mission

Systematically verify every checkbox in #109 and gather proof that the GitHub legacy deprecation is complete. Then prepare comprehensive closure documentation.

**Context**: Pre-Inchworm enterprise planning with multi-week timeline. Weeks 1-2 claim to be complete with 100% spatial adoption. Need to verify every claim before closing.

**Philosophy**: "Won't close an issue with a checkbox unchecked until we verify it with proof!"

---

## Issue Overview

**4-Week Timeline**:
- ✅ Week 1: Parallel Operation Infrastructure (claimed complete)
- ✅ Week 2: Legacy Deprecation Warnings (claimed complete)
- 🎯 Week 3: Legacy Disable by Default (ready but not done)
- 🔜 Week 4: Legacy Removal (pending)

**Claims to Verify**:
- 100% spatial adoption
- 0% legacy usage
- 50%+ performance improvement
- All Week 1-2 checkboxes complete

---

## Verification Steps

### Step 1: Verify Feature Flags Exist

**Check configuration files**:
```bash
# Find feature flag definitions
grep -r "USE_SPATIAL_GITHUB\|ALLOW_LEGACY_GITHUB\|GITHUB_DEPRECATION_WARNINGS" . --include="*.py" --include="*.md" --include="*.env*"

# Check config files specifically
cat config/PIPER.user.md | grep -i "github\|spatial" -A 2
cat config/settings.py 2>/dev/null | grep -i "github" || echo "No settings.py"
```

**Document**:
- [ ] USE_SPATIAL_GITHUB flag exists and location
- [ ] ALLOW_LEGACY_GITHUB flag exists and location
- [ ] GITHUB_DEPRECATION_WARNINGS flag exists and location
- [ ] Current values of each flag

---

### Step 2: Verify Spatial Integration Exists

**Check for GitHubSpatialIntelligence**:
```bash
# Find the spatial integration
find services/integrations -name "*spatial*github*" -o -name "*github*spatial*" 2>/dev/null

# Check imports and usage
grep -r "GitHubSpatialIntelligence\|github_spatial" services/ --include="*.py" | head -20

# Verify file exists at claimed location
ls -lh services/integrations/spatial/github_spatial.py 2>/dev/null || echo "File not found at claimed location"
```

**Document**:
- [ ] GitHubSpatialIntelligence class exists
- [ ] File location confirmed
- [ ] Integration is imported and used

---

### Step 3: Verify Legacy Integration Status

**Check for GitHubAgent (legacy)**:
```bash
# Find the legacy integration
ls -lh services/integrations/github/github_agent.py 2>/dev/null || echo "Legacy file not found"

# Check if legacy is still imported anywhere
grep -r "from.*github_agent import\|import.*github_agent" services/ --include="*.py" | grep -v "test" | grep -v "#"

# Check for legacy usage in main code
grep -r "GitHubAgent" services/ --include="*.py" | grep -v "test" | grep -v "#"
```

**Document**:
- [ ] Legacy file exists or deleted?
- [ ] Legacy still imported anywhere?
- [ ] Legacy still used in production code?

---

### Step 4: Verify Router Implementation

**Check for QueryRouter**:
```bash
# Find router that switches between spatial and legacy
grep -r "QueryRouter\|query_router" services/ --include="*.py" -B 2 -A 5

# Check routing logic
grep -r "USE_SPATIAL_GITHUB\|spatial.*legacy\|legacy.*spatial" services/ --include="*.py" -B 2 -A 5
```

**Document**:
- [ ] Router exists and location
- [ ] Router uses feature flags
- [ ] Routing logic favors spatial

---

### Step 5: Check Usage Metrics (100% Spatial Claim)

**Search for usage tracking**:
```bash
# Find any metrics or logging about GitHub integration usage
grep -r "spatial.*github.*usage\|legacy.*github.*usage\|github.*metrics" services/ logs/ --include="*.py" --include="*.log" 2>/dev/null | head -20

# Check for deprecation warnings
grep -r "deprecation.*github\|legacy.*warning" services/ --include="*.py"
```

**Test spatial integration**:
```bash
# Quick test that spatial is working
python -c "
try:
    from services.integrations.spatial.github_spatial import GitHubSpatialIntelligence
    print('✅ GitHubSpatialIntelligence imports successfully')
except Exception as e:
    print(f'❌ Import failed: {e}')
"
```

**Document**:
- [ ] Evidence of usage tracking
- [ ] Deprecation warnings implemented
- [ ] Spatial integration functional

---

### Step 6: Verify Integration Tests

**Check test coverage**:
```bash
# Find integration tests
find tests/ -name "*github*" -o -name "*spatial*" | grep -i integration

# Run GitHub-related integration tests
pytest tests/ -k "github or spatial" --co -q 2>/dev/null | head -20
```

**Document**:
- [ ] Integration tests exist for spatial
- [ ] Integration tests exist for legacy (or removed)
- [ ] Both code paths tested (Week 1 claim)

---

### Step 7: Check Documentation

**Verify migration guides exist**:
```bash
# Find migration documentation
find docs/ -name "*migration*" -o -name "*github*" -o -name "*spatial*" 2>/dev/null

# Check for legacy references in docs
grep -r "github.*legacy\|GitHubAgent\|migration.*spatial" docs/ --include="*.md" | head -20
```

**Document**:
- [ ] Migration guide exists
- [ ] Documentation comprehensive
- [ ] Legacy references handled

---

### Step 8: Verify Performance Claims (50%+ Improvement)

**Look for performance metrics**:
```bash
# Search for performance comparisons
grep -r "performance.*spatial\|spatial.*performance\|50%\|benchmark" docs/ services/ --include="*.md" --include="*.py" | head -20

# Check for timing comparisons
grep -r "timing.*github\|github.*timing\|speed.*improvement" docs/ --include="*.md"
```

**Document**:
- [ ] Performance comparison documented
- [ ] 50%+ improvement claim supported
- [ ] Benchmarks exist

---

### Step 9: Check Rollback Procedures

**Verify emergency rollback documented**:
```bash
# Find rollback documentation
grep -r "rollback\|emergency\|revert.*spatial" docs/ --include="*.md"

# Check if legacy can still be enabled
grep -r "ALLOW_LEGACY_GITHUB.*True" config/ docs/ --include="*.md" --include="*.py"
```

**Document**:
- [ ] Rollback procedures documented
- [ ] Emergency re-enable possible
- [ ] Safety infrastructure exists

---

### Step 10: Verify Week 3-4 Status

**Week 3 Checklist**:
```bash
# Check if ALLOW_LEGACY_GITHUB is False by default
grep -r "ALLOW_LEGACY_GITHUB" config/ --include="*.py" --include="*.md" -A 2

# Check if legacy is disabled
grep -r "ALLOW_LEGACY_GITHUB.*=.*False" config/ --include="*.py"
```

**Week 4 Checklist**:
```bash
# Check if legacy code still exists
ls -lh services/integrations/github/github_agent.py 2>/dev/null && echo "Legacy file still exists" || echo "Legacy file removed"

# Check for TODO or cleanup markers
grep -r "TODO.*legacy\|CLEANUP.*github\|REMOVE.*github" services/ --include="*.py"
```

**Document**:
- [ ] Week 3: Flag status (False by default or not)
- [ ] Week 4: Legacy code present or removed
- [ ] Cleanup markers found

---

## Evidence Compilation

Create: `/tmp/issue-109-closure-verification.md`

```markdown
# Issue #109 Closure Verification

**Date**: October 15, 2025, 5:XX PM  
**Verified By**: Code Agent  
**Issue**: CORE-INT #109 - GitHub Legacy Integration Deprecation Strategy

---

## Executive Summary

**Status**: [✅ COMPLETE / ⚠️ MOSTLY COMPLETE / ❌ INCOMPLETE]

**Overall Assessment**: [summary of findings]

---

## Week 1: Parallel Operation Infrastructure

### Feature Flags
- [x] USE_SPATIAL_GITHUB implemented
  - Location: [path]
  - Current value: [value]
  - Evidence: [quote from file]

- [x] ALLOW_LEGACY_GITHUB implemented
  - Location: [path]
  - Current value: [value]
  - Evidence: [quote from file]

- [x] Parallel operation working
  - Evidence: [test results, router logic]

- [x] Integration tests exist
  - Location: [paths]
  - Pass rate: [X/Y passing]

- [x] Zero breaking changes
  - Evidence: [how verified]

**Week 1 Status**: [✅ VERIFIED COMPLETE / ⚠️ ISSUES FOUND / ❌ INCOMPLETE]

---

## Week 2: Legacy Deprecation Warnings

### Warning Infrastructure
- [x] Deprecation warnings implemented
  - Location: [path]
  - Evidence: [code snippet]

### Usage Metrics
- [x] Usage tracking exists
  - Spatial usage: [percentage or "100%"]
  - Legacy usage: [percentage or "0%"]
  - Evidence: [logs, metrics, or code]

### Documentation
- [x] Migration guides exist
  - Location: [paths]
  - Comprehensive: [YES/NO]
  - Evidence: [list of docs]

### Performance Comparison
- [x] Performance improvement documented
  - Claimed: 50%+ improvement
  - Evidence: [benchmark location or description]
  - Verified: [YES/NO/PARTIALLY]

**Week 2 Status**: [✅ VERIFIED COMPLETE / ⚠️ ISSUES FOUND / ❌ INCOMPLETE]

---

## Week 3: Legacy Disable by Default

### Feature Flag Status
- [ ] ALLOW_LEGACY_GITHUB=False by default
  - Current value: [True/False]
  - Location: [path]
  - **Status**: [COMPLETE/NOT YET/N/A]

### Emergency Rollback
- [x] Rollback procedures documented
  - Location: [path]
  - Clear: [YES/NO]

### Monitoring
- [x] Enhanced observability
  - Evidence: [logging, metrics]

**Week 3 Status**: [✅ COMPLETE / 🎯 READY TO EXECUTE / ❌ NOT STARTED]

---

## Week 4: Legacy Removal

### Code Removal
- [ ] Legacy GitHub integration deleted
  - File: services/integrations/github/github_agent.py
  - Status: [DELETED/STILL EXISTS]

### Documentation Cleanup
- [ ] Legacy references removed
  - Status: [COMPLETE/IN PROGRESS/NOT STARTED]

### Test Cleanup
- [ ] Legacy test paths removed
  - Status: [COMPLETE/IN PROGRESS/NOT STARTED]

### Final Validation
- [ ] Spatial-only operation validated
  - Status: [COMPLETE/IN PROGRESS/NOT STARTED]

**Week 4 Status**: [✅ COMPLETE / 🔜 READY TO EXECUTE / ❌ NOT STARTED]

---

## Key Findings

### ✅ Verified Complete
[List items fully verified as complete]

### ⚠️ Mostly Complete
[List items mostly complete but with minor gaps]

### ❌ Not Complete
[List items not complete]

### 🎯 Ready to Execute
[List items ready to be executed now]

---

## Spatial vs Legacy Status

**Spatial Integration**:
- Location: [path]
- Status: [ACTIVE/WORKING]
- Usage: [percentage]

**Legacy Integration**:
- Location: [path or "DELETED"]
- Status: [DEPRECATED/REMOVED]
- Usage: [percentage]

**Current Routing**: [Spatial only / Hybrid / Legacy fallback available]

---

## Performance Claims Verification

**Claimed**: 50%+ performance improvement with spatial

**Evidence Found**:
[List evidence: benchmarks, timing comparisons, documentation]

**Verification Status**: [✅ VERIFIED / ⚠️ CLAIMED BUT NOT MEASURED / ❌ NOT VERIFIED]

---

## Migration Completion Evidence

**100% Spatial Adoption Claim**:
- Evidence: [logs, metrics, code analysis]
- Verified: [YES/NO]

**0% Legacy Usage Claim**:
- Evidence: [logs, metrics, code analysis]
- Verified: [YES/NO]

---

## Remaining Work

### Must Complete Before Closing:
- [ ] [Item 1]
- [ ] [Item 2]

### Optional Enhancements:
- [ ] [Item 1]
- [ ] [Item 2]

### Can Be Done After Closing:
- [ ] [Item 1]

---

## Recommendations

### Option 1: Close Now
**If**: [conditions]
**Because**: [rationale]
**Remaining**: [what's left]

### Option 2: Complete Week 3-4 First
**Tasks**: [specific tasks]
**Time**: [estimate]
**Then**: Close with full completion

### Option 3: Close with Follow-up Issues
**Close**: Week 1-2 verified complete
**Create**: New issues for Week 3-4 cleanup
**Rationale**: [why this approach]

---

## Final Assessment

**Can Close #109**: [YES / YES WITH CONDITIONS / NO]

**Rationale**: [detailed explanation of why]

**Next Steps**: [what to do based on findings]

---

## Evidence References

**Files Examined**:
- [list key files checked]

**Tests Run**:
- [list tests executed]

**Metrics Checked**:
- [list metrics examined]

**Documentation Reviewed**:
- [list docs reviewed]

---

**Verification Complete**: [time]  
**Total Time**: [duration]  
**Confidence**: [HIGH/MEDIUM/LOW]
```

---

## Deliverables

### Verification Complete When:
- [ ] All 10 verification steps executed
- [ ] Evidence documented for each claim
- [ ] Week 1-4 status determined
- [ ] Spatial vs legacy status clear
- [ ] Performance claims assessed
- [ ] Remaining work identified
- [ ] Recommendation provided
- [ ] Closure documentation complete

---

## Success Criteria

**Minimum for Closure**:
- ✅ Weeks 1-2 verified complete
- ✅ Spatial integration working
- ✅ Legacy usage at 0% (or removed)
- ✅ No blocking issues found

**Ideal for Closure**:
- ✅ All above
- ✅ Weeks 3-4 also complete
- ✅ Performance claims verified
- ✅ All checkboxes verified

---

## Time Budget

**Target**: 30-45 minutes

- Feature flag verification: 5 min
- Integration verification: 10 min
- Usage metrics check: 5 min
- Documentation review: 10 min
- Evidence compilation: 10 min
- Recommendations: 5 min

---

## What NOT to Do

- ❌ Don't assume claims are true without evidence
- ❌ Don't skip verification steps
- ❌ Don't recommend closure without proof
- ❌ Don't implement Week 3-4 yet (just verify status)

## What TO Do

- ✅ Verify every checkbox systematically
- ✅ Gather concrete evidence
- ✅ Document gaps clearly
- ✅ Provide clear recommendation
- ✅ Be thorough but efficient

---

## Context

**Why This Matters**:
- Pre-Inchworm enterprise planning
- Multi-week timeline (rigid)
- Claims of completion need verification
- PM wants proof before closing
- "Won't close with unchecked boxes without proof"

**What Comes After**:
- If verified: Close #109 with evidence
- If gaps: Complete remaining work or create follow-ups
- If Week 3-4 needed: Execute and then close

---

**Verification Start**: 5:10 PM  
**Expected Completion**: ~5:40-5:55 PM (30-45 minutes)  
**Status**: Ready to verify systematically

**LET'S VERIFY EVERYTHING!** 🔍

---

*"Trust, but verify. Then close with confidence."*
*- Issue Closure Philosophy*
