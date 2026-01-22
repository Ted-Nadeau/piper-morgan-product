# GRAMMAR-COMPLIANCE: Feature Transformation Tracking

## Summary

Track transformation of existing features from "flattened" or "partial" grammar compliance to full MUX object model alignment ("Entities experience Moments in Places").

## Context

Following completion of MUX-VISION (#399, #400, #404, #405, #406), the grammar compliance audit identified 15 features needing transformation. Issues have been created for the 9 highest priority features.

**Source**: Grammar compliance audit in #404 (MUX-VISION-GRAMMAR-CORE)

**Tools Available**:
- 302 MUX infrastructure tests
- 5 application patterns (Pattern-050 through 054)
- Transformation guide with worked example
- Consciousness philosophy document
- PR review consciousness checklist

## Tracking

### Critical Priority (MUX-V2 Scheduled)

These features touch every user interaction. Scheduled as explicit work in MUX-V2.

| Issue | Feature | Current State | Target |
|-------|---------|---------------|--------|
| #619 | Intent Classification | Partial | Conscious |
| #620 | Slack Integration | Partial | Conscious |
| #621 | GitHub Integration | Partial | Conscious |
| #622 | Todo Management | Flattened | Conscious |

### Important Priority (Quality Gates)

These features will be uplifted opportunistically when touched for other reasons.

| Issue | Feature | Current State | Target |
|-------|---------|---------------|--------|
| #623 | Feedback System | Partial | Conscious |
| #624 | Calendar Integration | Partial | Conscious |
| #625 | Conversation Handler | Partial | Conscious |
| #626 | Onboarding System | Partial | Conscious |
| #627 | Personality System | Partial | Conscious |

### Not Yet Filed (Lower Priority)

Per audit, 6 additional features identified but not yet requiring issues:
- Config Management
- Error Handling
- Help System
- Logging
- Metrics
- Utilities

## Completion Criteria

- [ ] All Critical (4) issues completed before MUX-IMPLEMENT begins
- [ ] All Important (5) issues completed or explicitly deferred with rationale
- [ ] Each transformation passes anti-flattening tests from ADR-055
- [ ] Each transformation includes "experience" verification

## Anti-Flattening Reminder

For each transformation, verify:
1. Does this help Piper **experience** or just **store**?
2. Are Entities actors with agency, not just records?
3. Are Moments bounded scenes, not just timestamps?
4. Do Places have atmosphere, not just IDs?

## Related

- #399 MUX-VISION-OBJECT-MODEL (complete)
- #400 MUX-VISION-CONSCIOUSNESS (complete)
- #404 MUX-VISION-GRAMMAR-CORE (complete)
- ADR-055: Object Model

## Labels

`mux`, `tracking`, `grammar-compliance`

## Milestone

MUX-V2 (for Critical issues)

---

*Parent tracking issue created per Chief Architect guidance, January 21, 2026*
