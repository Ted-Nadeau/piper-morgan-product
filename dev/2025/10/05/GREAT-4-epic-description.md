# GREAT-4: Intent Classification Universal

## Overview
Transform intent classification from optional feature to mandatory universal entry point for ALL user interactions. No bypasses allowed.

## Context (October 5, 2025)
- Plugin architecture complete (GREAT-3 ✅)
- Layer 3 intent access fixed (#172 ✅)
- Intent system exists but is often bypassed
- Multiple CORE tickets need consolidation (#96, #176, #179)
- ADR-032 defines the vision but implementation incomplete

## Current State
- Intent classifier exists at `services/intent_service/`
- Some endpoints bypass classification entirely
- Missing intent categories (TEMPORAL, STATUS, PRIORITY)
- Generic/undefined responses from intent handlers
- No universal enforcement mechanism

## Scope

### Foundation & Categories
- Add missing intent categories per #96
- Fix pattern loading and classification accuracy
- Establish comprehensive test coverage
- Baseline performance metrics

### Universal Enforcement
- Create intent classification middleware
- Route ALL interactions through classifier
- Remove direct endpoint bypasses
- Implement caching for performance

### Quality & Performance
- Fix generic/undefined responses (#179)
- Optimize processing to <100ms target
- Improve classification accuracy to >80%
- Add context-aware responses

### Validation & Documentation
- Contract tests for universal coverage
- Performance benchmarks
- Update ADR-032 with implementation
- Migration guide for endpoints

## Decomposition

### GREAT-4A: Foundation & Categories (4-6 hours)
- Add TEMPORAL, STATUS, PRIORITY categories
- Fix pattern loading issues
- Create test suite with canonical queries
- Establish baseline metrics

### GREAT-4B: Universal Enforcement (6-8 hours)
- Create intent middleware layer
- Wire all endpoints through classifier
- Remove bypass routes
- Add caching layer

### GREAT-4C: Quality & Performance (4-6 hours)
- Fix undefined/generic responses
- Optimize to <100ms processing
- Improve accuracy to >80%
- Context-aware response generation

### GREAT-4D: Validation & Documentation (2-3 hours)
- 100% endpoint coverage tests
- Performance validation
- Update ADR-032
- Create migration guide

## Acceptance Criteria

Phase 4A:
- [ ] All 3 new categories added and tested
- [ ] Canonical queries classify correctly
- [ ] Pattern loading verified
- [ ] Baseline metrics established

Phase 4B:
- [ ] Intent middleware operational
- [ ] 100% of endpoints use classifier
- [ ] Zero bypass routes remain
- [ ] Caching layer functional

Phase 4C:
- [ ] No undefined responses
- [ ] <100ms processing time
- [ ] >80% accuracy on test set
- [ ] Context-aware responses working

Phase 4D:
- [ ] All tests passing
- [ ] Performance validated
- [ ] Documentation complete
- [ ] Migration guide created

## Lock Strategy
- Middleware tests prevent bypasses
- CI gates enforce intent classification
- Performance tests prevent regression
- Coverage reports show 100%

## Dependencies
- ✅ GREAT-3 (Plugin Architecture complete)
- ✅ #172 (Layer 3 access fixed)

## Success Validation
```bash
# All endpoints go through intent
grep -r "intent_classifier" web/ | wc -l  # Should match endpoint count

# Performance meets targets
python benchmark_intent.py  # <100ms average

# Accuracy validated
pytest tests/intent/accuracy/ -v  # >80% accuracy

# No bypasses possible
pytest tests/intent/enforcement/ -v  # 100% coverage
```

## Issues This Supersedes
When complete, close:
- #96 (CORE-INTENT-CAT) - Categories added in 4A
- #176 (CORE-INTENT-ENFORCE) - Universal enforcement in 4B
- #179 (CORE-INTENT-QUALITY) - Quality fixes in 4C

## Anti-80% Checklist
```
Component | Foundation | Enforce | Quality | Validated | Documented
--------- | ---------- | ------- | ------- | --------- | ----------
Categories| [ ]        | [ ]     | [ ]     | [ ]       | [ ]
Middleware| [ ]        | [ ]     | [ ]     | [ ]       | [ ]
Endpoints | [ ]        | [ ]     | [ ]     | [ ]       | [ ]
Caching   | [ ]        | [ ]     | [ ]     | [ ]       | [ ]
Accuracy  | [ ]        | [ ]     | [ ]     | [ ]       | [ ]
TOTAL: 0/25 checkmarks = 0% (Must reach 100%)
```

## Time Estimate
16-23 hours (2-3 days based on GREAT-3 velocity)
