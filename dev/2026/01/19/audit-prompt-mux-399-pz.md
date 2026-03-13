# Agent Prompt Audit: MUX-399-PZ Verification & Anti-Flattening Tests

**Prompt**: `prompt-mux-399-pz-verification.md`
**Template Version**: v10.2
**Audit Date**: 2026-01-19
**Auditor**: Claude Code (Lead Developer)

---

## Audit Summary

| Section | Template Required | Present | Compliant | Notes |
|---------|------------------|---------|-----------|-------|
| Your Identity | Yes | Yes | ✅ | Verification agent identity |
| Essential Context | Yes | Yes | ✅ | All P0-P4.5 as reference |
| Post-Compaction Protocol | Yes (CRITICAL) | Yes | ✅ | STOP/REPORT/ASK/WAIT |
| Evidence/Handoff Requirements | Yes (CRITICAL) | Yes | ✅ | 7 deliverables tracked |
| Completion Matrix | Yes (NEW) | Yes | ✅ | 0/7 = 0% starting point |
| Handoff Format | Yes | Yes | ✅ | Template provided |
| Infrastructure Verification | Yes (MANDATORY) | Yes | ✅ | 5 verification commands |
| Mission | Yes | Yes | ✅ | Clear scope boundaries |
| Context | Yes | Yes | ✅ | All fields populated |
| Anti-80% Safeguards | Yes (CRITICAL) | Yes | ✅ | Implicit in 7-item matrix |
| Implementation Approach | Yes | Yes | ✅ | TDD with test examples |
| Verification Gates | Recommended | Yes | ✅ | 20+ tests target |
| STOP Conditions | Yes | Yes | ✅ | 5 conditions listed |
| Self-Check | Yes | Yes | ✅ | 8 questions |
| Related Documentation | Yes | Yes | ✅ | P1-P4.5, ADRs linked |

---

## Detailed Compliance Check

### ✅ CRITICAL SECTIONS (All Present)

**1. Post-Compaction Protocol**
- Present: Yes
- Contains: STOP, REPORT, ASK, WAIT
- **Compliant**: ✅

**2. Evidence/Handoff Requirements**
- Acceptance criteria format: ✅ (7 deliverables)
- Evidence requirements listed: ✅
- Handoff format template: ✅
- **Compliant**: ✅

**3. Completion Matrix**
- Present: ✅ (7 deliverables)
- "0/7 = 0%" starting point: ✅
- "Only claim complete when 7/7 = 100%": ✅
- **Compliant**: ✅

**4. Infrastructure Verification**
- "MANDATORY FIRST ACTION": ✅
- Bash commands provided: ✅ (5 commands)
- Expected values specified: ✅ (262 MUX tests)
- STOP protocol: ✅
- **Compliant**: ✅

### ✅ STANDARD SECTIONS (All Present)

**5. Implementation Approach**
- TDD sequence: ✅
- Test code examples: ✅ (comprehensive anti-flattening tests)
- Documentation templates: ✅
- Per-step evidence commands: ✅
- **Compliant**: ✅

**6. Verification Gates**
- Phase 1: 20+ anti-flattening tests
- Phase 2-6: Documentation deliverables
- **Compliant**: ✅

**7. STOP Conditions** (5 conditions)
- Standard conditions: ✅
- Domain-specific: ✅ (anti-flattening reveals issues, grammar broken)
- "When stopped" protocol: ✅
- **Compliant**: ✅

**8. Self-Check** (8 questions)
- Evidence questions: ✅
- Matrix completion: ✅
- Documentation verification: ✅
- **Compliant**: ✅

---

## Anti-Flattening Test Examples Quality

The prompt includes comprehensive test examples covering:

1. **Entity tests**: Identity preservation, agency, memory
2. **Moment tests**: Boundaries, significance, memorability
3. **Place tests**: Atmosphere, affordances, containment
4. **Lifecycle tests**: Composting, story-telling, transformation
5. **Metadata tests**: Knowing about knowing, basis tracking
6. **Ownership tests**: Relationship categories
7. **Design tests**: Experience language verification
8. **Integration tests**: Grammar expressiveness

Each test class has clear pass/fail criteria documented.

---

## Compliance Score

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Critical Sections | 10/10 | 50% | 5.0 |
| Standard Sections | 10/10 | 30% | 3.0 |
| Template Coverage | 10/10 | 15% | 1.5 |
| Best Practices | 10/10 | 5% | 0.5 |

**Total**: 10.0/10

**Assessment**: PASS - READY FOR DEPLOYMENT

---

## Key Strengths

1. **Comprehensive anti-flattening tests** with pass/fail documentation
2. **7 deliverables tracked** covering all verification needs
3. **Experience language** emphasized throughout
4. **Documentation templates** for guide, tests, checkpoint
5. **Sign-off package** structure for PM/CXO review
6. **Final checkpoint template** captures epic journey
7. **Pattern continuity** - follows P1-P4 established patterns

---

## Minor Observations (Not Blocking)

### 1. Human Review Required
Sign-off package requires PM/CXO review - appropriately scoped as async.

### 2. Epic Closure
This is the final issue before epic #399 can close - prompt captures this significance.

---

## Auditor Sign-Off

This agent prompt is **APPROVED for deployment**. It fully implements the critical v10.2 requirements:
- Post-compaction protocol ✅
- Evidence/handoff requirements ✅
- Completion matrix with 7 objective deliverables ✅
- Infrastructure verification ✅
- STOP conditions ✅
- TDD implementation approach with comprehensive tests ✅

The prompt correctly positions PZ as the capstone verification phase for the MUX epic.

*Audit complete: 2026-01-19*
