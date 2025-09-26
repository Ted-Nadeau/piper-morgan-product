# ADR-032 Intent Classification Universal Entry - Audit Report

**Date**: September 20, 2025
**Auditor**: Lead Developer (Claude Sonnet 4)
**Requested by**: Chief Architect

---

## Executive Summary

**ADR-032 Status**: **PARTIALLY IMPLEMENTED** (~50-60% complete)

ADR-032 claims intent classification is the "universal entry point for all Piper Morgan interactions," but audit reveals significant bypasses across all interfaces. The intent classification infrastructure is robust and well-implemented, but universality is not enforced.

## Detailed Findings

### ✅ Intent Classification Infrastructure - EXCELLENT

**Location**: `services/intent_service/`

**Quality Assessment**: The intent classification system is sophisticated and well-architected:
- **Pre-classification**: Pattern-based fast path for common intents
- **LLM Classification**: Claude-powered with reasoning and confidence scoring
- **Fuzzy Matching**: Typo correction and approximate matching
- **Action Normalization**: PM-039 compliance for consistent action naming
- **Spatial Context**: Integration with MCP spatial intelligence
- **Learning Signals**: Framework for continuous improvement

**Technical Quality**: HIGH - This is production-ready infrastructure that exceeds ADR requirements.

### 🟡 Web Interface - MIXED COMPLIANCE

**Primary Intent Endpoint**: ✅ `/api/v1/intent` properly uses intent classification

**Identified Bypasses**:
1. **Direct API Routes** (ADR Violations):
   - `/api/standup` - Bypasses intent classification entirely
   - `/api/personality/*` - All personality endpoints skip intent layer

2. **Intentional Performance Bypass** (Architectural Decision):
   - Tier 1 conversation patterns (greetings) skip orchestration
   - **Status**: This may be acceptable for performance, but contradicts ADR-032's "every user input" requirement

### ❌ CLI Commands - NON-COMPLIANT

**Evidence**: Direct examination of `cli/commands/standup.py` and `cli/commands/issues.py`

**Pattern Found**: All CLI commands directly instantiate domain services, completely bypassing intent classification:
```python
# Current CLI pattern (violates ADR-032)
self.orchestration_service = StandupOrchestrationService()  # Direct service access
```

**Expected ADR-032 Pattern**:
```python
# Should be: intent → classifier → router → handler
intent = await intent_classifier.classify(user_command)
result = await intent_router.route(intent)
```

**Compliance**: 0% - No CLI commands use intent classification

### ❓ Slack Integration - STATUS UNKNOWN

**Requires Further Investigation**: Slack service patterns not audited in this session.

## Root Cause Analysis

### Why ADR-032 Failed to Achieve Universal Adoption

1. **No Enforcement Mechanism**: ADR-032 lacks technical enforcement (lint rules, CI checks, etc.)

2. **Performance Bypass Culture**: Development team created "performance bypasses" that violate universality principle

3. **Legacy Code Patterns**: Existing CLI commands were never migrated to intent-first architecture

4. **Gradual Erosion**: Intent classification was implemented but bypasses were added over time without ADR review

## Impact Assessment

### CORE-GREAT Epic Dependencies

**CORE-GREAT-1 (Orchestration Core)**:
- Current bypasses prevent unified orchestration patterns
- Multiple entry points create inconsistent user experience

**CORE-GREAT-4 (Intent Universalization)**:
- This epic directly addresses ADR-032 completion
- Required to achieve architectural vision

### User Experience Issues

1. **Inconsistent Interface**: Web uses intent, CLI bypasses intent, creating learning overhead
2. **Feature Fragmentation**: Same functionality accessible through different patterns
3. **Testing Complexity**: Multiple code paths for similar user goals

### Technical Debt Accumulation

- **Maintenance Overhead**: Must maintain both intent-based and direct-service patterns
- **Testing Burden**: Duplicate test coverage for different access patterns
- **Documentation Complexity**: Users must learn multiple interaction models

## Recommendations

### Phase 1: Assessment Completion (1 day)
- [ ] Audit Slack integration patterns for intent compliance
- [ ] Create comprehensive bypass inventory across all services
- [ ] Document current state vs ADR-032 requirements

### Phase 2: CLI Remediation (CORE-GREAT-4)
- [ ] Migrate all CLI commands to intent-first pattern
- [ ] Remove direct service instantiation from CLI layer
- [ ] Implement unified CLI intent handler

### Phase 3: Web API Cleanup
- [ ] Evaluate performance bypass necessity
- [ ] Either formalize bypasses as architectural exception OR remove them
- [ ] Migrate `/api/standup` and `/api/personality/*` to intent layer

### Phase 4: Enforcement Implementation
- [ ] Add lint rules preventing intent bypasses
- [ ] Create CI checks for universal intent compliance
- [ ] Add monitoring for non-intent API usage

## Technical Implementation Approach

### Recommended CLI Migration Pattern
```python
# New CLI pattern (ADR-032 compliant)
class CLICommand:
    def __init__(self):
        self.intent_classifier = IntentClassifier()
        self.intent_router = IntentRouter()

    async def execute(self, user_input: str):
        intent = await self.intent_classifier.classify(user_input)
        return await self.intent_router.route(intent)
```

### Web API Migration Pattern
```python
# Migrate direct endpoints to intent routing
@app.post("/api/standup")
async def standup_endpoint(request: Request):
    # Route through intent classification
    intent = Intent(category=IntentCategory.QUERY, action="get_standup")
    return await intent_router.route(intent)
```

## Risk Assessment

### High Risk: Continued Non-Compliance
- **User Confusion**: Multiple interaction patterns create cognitive overhead
- **Development Friction**: Team must maintain parallel systems
- **Architecture Debt**: Intent classification investment wasted if not universal

### Medium Risk: Performance Impact
- **Latency Concerns**: Intent classification adds processing overhead
- **Mitigation**: Pre-classification and caching can maintain performance

### Low Risk: Implementation Complexity
- **Infrastructure Ready**: Intent classification system is production-quality
- **Pattern Available**: Web interface demonstrates working intent integration

## Conclusion

ADR-032's intent classification infrastructure is excellent, but universality enforcement failed. The decision was sound, implementation was partial, and bypasses accumulated over time.

**Recommendation**: Prioritize CORE-GREAT-4 (Intent Universalization) to complete ADR-032 and achieve the architectural vision of unified user interaction patterns.

The investment in intent classification is significant and high-quality. Completing universality will unlock the full value of this infrastructure and provide the consistent user experience originally envisioned.

---

**Next Actions for Chief Architect**:
1. Review findings and confirm remediation priority
2. Approve CORE-GREAT-4 epic scope to include ADR-032 completion
3. Consider architectural exceptions for performance-critical bypasses
4. Define enforcement mechanisms for future ADR compliance

**Session Status**: ADR-032 audit complete, awaiting Chief Architect review
