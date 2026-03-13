# Architectural Decision: Ethics Service Layer Refactor

**To**: Lead Developer
**From**: Chief Architect
**Date**: October 18, 2025, 11:55 AM
**Re**: Issue #197 - Ethics Architecture Decision

---

## Decision: APPROVED - Option 1 (Service Layer Refactor)

Both your analysis and Code's independent investigation reached identical conclusions. The evidence is overwhelming that ethics enforcement belongs at the service layer, not as HTTP middleware.

## Key Validation Points

1. **Coverage**: HTTP middleware = 30-40% vs Service layer = 95-100%
2. **DDD Compliance**: Ethics is domain logic per ADR-029 and Pattern-008
3. **Universal Entry Point**: ADR-032 establishes IntentService.process_intent() as the standard
4. **Pattern Consistency**: Follows same approach as logging, metrics, classification

## Implementation Path (Approved)

### Phase 2A: BoundaryEnforcer Refactor (1-2 hours)
- Remove FastAPI Request dependency
- Change signature to accept message/session_id/context
- Update tests for domain objects

### Phase 2B: IntentService Integration (1 hour)
- Add ethics check at start of process_intent()
- Return appropriate IntentProcessingResult on violation
- Add feature flag: `ENABLE_ETHICS_ENFORCEMENT`

### Phase 2C: Clean Up (30 minutes)
- Remove HTTP middleware activation
- Document service-layer enforcement

### Phase 2D: Fix Slack Gap (1 hour)
- Route Slack webhooks through IntentService (Code found they currently bypass)
- Ensure complete coverage

## Critical Requirements

1. **Feature Flag Required**: Must be toggleable without code changes
2. **Test Coverage**: Add multi-channel tests verifying all entry points
3. **No Partial Solutions**: This is Piper Morgan's ethos - A++ quality only
4. **Document Everything**: This is cathedral work

## Time Investment

The additional 2-3 hours for proper architecture is non-negotiable. This is core to our values and must be done correctly.

## Questions Answered

- **Keep middleware?** No - remove to avoid confusion
- **Slack routing?** Yes - must go through IntentService
- **CLI future?** Yes - will use same IntentService path
- **Priority?** Do it right the first time

## Next Steps

1. Proceed with Phase 2A immediately
2. Use Time Lords Protocol - quality determines timeline
3. Test thoroughly across ALL entry points
4. Report completion when universal coverage achieved

---

**This is approved. The architecture must be correct. Ethics must be universal.**

**Chief Architect**
