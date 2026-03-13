# Issue Template Audit: #408 MUX-VISION-LIFECYCLE-SPEC

## Feature Template Checklist

| Template Section | Present in #408? | Notes |
|------------------|------------------|-------|
| **Header** | | |
| Priority | ❌ Missing | No P0/P1/P2/P3 stated |
| Labels | ⚠️ Partial | Has "UX" label only |
| Milestone | ❌ Missing | No sprint assignment |
| Epic | ✅ Yes | #401 MUX-VISION |
| Related | ⚠️ Partial | Lists #399, #400 but no ADRs |
| **Problem Statement** | | |
| Current State | ⚠️ Implicit | Context section describes gap but not explicitly |
| Impact (Blocks/User/Debt) | ❌ Missing | No impact analysis |
| Strategic Context | ⚠️ Implicit | Part of MUX-VISION sprint noted |
| **Goal** | | |
| Primary Objective | ⚠️ Vague | "Formalize 8-stage lifecycle spec" - but spec for what? |
| Example User Experience | ❌ Missing | No before/after scenario |
| Not In Scope | ✅ Yes | "Out of Scope" section present |
| **What Already Exists** | | |
| Infrastructure ✅ | ✅ Yes | Lists `lifecycle.py`, architecture docs |
| What's Missing ❌ | ⚠️ Partial | Not explicitly called out as "missing" |
| **Requirements** | | |
| Phase 0: Investigation | ❌ Missing | No investigation phase |
| Phases 1-N | ❌ Missing | No phased breakdown |
| Phase Z: Completion | ❌ Missing | No handoff phase |
| **Acceptance Criteria** | | |
| Functionality | ✅ Yes | Documentation Deliverables section |
| Testing | ❌ Missing | No test requirements |
| Quality | ⚠️ Partial | "Quality Gates" section but vague |
| Documentation | ⚠️ Partial | Listed as deliverables |
| **Completion Matrix** | ❌ Missing | No matrix |
| **Testing Strategy** | ❌ Missing | No test scenarios |
| **Success Metrics** | ❌ Missing | No quantitative/qualitative measures |
| **STOP Conditions** | ❌ Missing | No explicit stop conditions |
| **Effort Estimate** | ❌ Missing | No size estimate |
| **Dependencies** | ⚠️ Partial | Listed but not as checkboxes |
| **Related Documentation** | ⚠️ Partial | Resources section exists |

---

## Gap Summary

### Critical Gaps (Must Address)

1. **No phased implementation plan** - Just acceptance criteria categories, no execution phases
2. **No testing strategy** - Experience design still needs tests (unit tests for phrase generation, etc.)
3. **No completion matrix** - Can't verify 100% completion
4. **Phrase tone mismatch not documented** - Issue specifies phrases that differ from existing implementation
5. **No effort estimate** - "Meaty" per PM but no breakdown

### Moderate Gaps (Should Address)

6. **No explicit problem statement** - Why does current implementation need this?
7. **No user impact analysis** - Who benefits and how?
8. **No STOP conditions** - When should work halt?
9. **No success metrics** - How do we know phrases "feel natural"?

### Minor Gaps (Nice to Have)

10. **Priority not stated** - Implied medium-high by parent epic
11. **Milestone not assigned** - V2 sprint implied

---

## Recommendations

### Before Creating Gameplan

1. **Clarify phrase approach** with PM:
   - Replace existing poetic phrases?
   - Add separate `conversation_phrase` property?
   - Both for different contexts?

2. **Add missing sections** to issue:
   - Phased implementation plan
   - Testing strategy
   - Completion matrix
   - Effort estimate

3. **Document the existing infrastructure gap**:
   - Current `experience_phrase` values don't match issue specification
   - This is a design decision, not just implementation

### Issue Should Also Include

- **Success Criteria**: "Transitions feel natural in conversation" - how is this measured? PM review? User testing?
- **Test Scenarios**: Phrase generation should have unit tests even if it's "experience design"

---

## Proposed Issue Updates

Before gameplan, recommend updating #408 with:

1. **Problem Statement** section making explicit why current phrases insufficient
2. **Phased Requirements** with specific deliverables per phase
3. **Testing Strategy** even if minimal (phrase consistency tests)
4. **Completion Matrix** template
5. **Decision: Phrase Approach** - PM to decide replace vs augment

---

## Questions for PM

1. **Phrase tone**: Replace existing or add new property alongside?
2. **Testing depth**: Unit tests for phrase generation, or just PM review?
3. **Integration scope**: Which handlers should use lifecycle phrases first?
4. **Success measurement**: How do we validate "transitions feel natural"?
