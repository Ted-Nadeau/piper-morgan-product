# Audit models.py for Object Model Alignment

## Context
ADR-045 establishes "Entities experience Moments in Places" as Piper's foundational grammar. However, the working domain models may not reflect this conceptual richness. Developers reference models.py constantly, so any drift here will cause implementation to diverge from vision.

## Scope
**In Scope:**
- `/domain/models.py` and related domain model files
- Mapping existing models to Entity/Place/Moment/Situation concepts
- Identifying Native/Federated/Synthetic ownership patterns
- Checking lifecycle implementation (especially Composting stage)

**Out of Scope:**
- Refactoring code (this is audit only)
- Updating tests
- Modifying database schemas

## Acceptance Criteria
- [ ] Document every model's relationship to object model grammar
- [ ] Identify which models represent Entities vs Places vs Moments
- [ ] Note where Situation-as-container pattern should apply
- [ ] Find lifecycle implementation (or absence)
- [ ] Locate Native/Federated/Synthetic distinctions (or gaps)
- [ ] Create prioritized list of alignment issues
- [ ] Produce remediation plan with effort estimates

## Deliverables
Create `dev/active/audit-models-object-model.md` containing:
1. Current State Analysis (what exists)
2. Gap Analysis (what's missing/misaligned)
3. Remediation Plan (how to fix, priority order)
4. Risk Assessment (what breaks if we don't fix)

## Resources
- ADR-045: `dev/active/ADR-045-object-model.md`
- Object Model Brief v2: `dev/active/object-model-brief-v2.md`
- Current models: `services/domain/models.py` (and related files)
- Morning Standup implementation (reference for consciousness)

## Verification
- Audit document is comprehensive and actionable
- Every domain model is categorized
- Remediation plan has clear priorities
- No speculation - only documented facts

## Notes
This is detective work - we're looking for where reality diverges from vision. The Morning Standup is our "reference implementation" of consciousness - use it as a comparison point.

Remember: We're not judging past decisions, we're mapping current state to future direction.
