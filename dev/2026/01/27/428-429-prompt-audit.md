# Audit: Subagent Prompts against agent-prompt-template.md

## Audit: #428 ARIA Prompt

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Identity statement | ✅ | "You are a Coding Agent working on Piper Morgan" |
| Mission/objective | ✅ | Clear mission statement with WCAG reference |
| GitHub Issue reference | ✅ | "#428 MUX-IMPLEMENT-ARIA" |
| Context (current/target state) | ✅ | Current state, target state, dependencies |
| Infrastructure verified | ✅ | "Templates exist at templates/components/" |
| Phase 0 verification tasks | ✅ | Component audit with matrix |
| Evidence requirements | ✅ | Before/after diffs, handoff format specified |
| Acceptance criteria | ✅ | 7 checkboxes matching issue |
| STOP conditions | ✅ | 3 conditions specified |
| Handoff format | ✅ | Complete report template |
| Constraints | ✅ | 5 constraints (no JS, no CSS, etc.) |
| Method enumeration (if interface) | N/A | Not implementing interface |
| Test requirements | ⚠️ | No explicit test requirement - ARIA is structural |
| Git commit discipline | ⚠️ | Not explicitly mentioned |

### Action Required
1. ⚠️ Tests: ARIA changes are structural/attribute-only. No unit tests typical for this. Add note that visual regression check is the validation.
2. ⚠️ Git: Add git commit reminder.

**Overall**: Prompt is sufficient. The ⚠️ items are acceptable for this type of work (ARIA attributes don't have unit tests).

---

## Audit: #429 Contrast Prompt

| Template Requirement | Status | Notes |
|---------------------|--------|-------|
| Identity statement | ✅ | "You are a Coding Agent working on Piper Morgan" |
| Mission/objective | ✅ | Clear mission with WCAG requirements |
| GitHub Issue reference | ✅ | "#429 MUX-IMPLEMENT-CONTRAST-TESTS" |
| Context (current/target state) | ✅ | Current state with known failure, target state |
| Infrastructure verified | ✅ | "tokens.css at web/static/css/tokens.css" |
| Phase 0 verification tasks | ✅ | Inventory color combinations |
| Evidence requirements | ✅ | Full table with ratios, handoff format |
| Acceptance criteria | ✅ | 8 checkboxes matching issue |
| STOP conditions | ✅ | 3 conditions specified |
| Handoff format | ✅ | Complete report template |
| Constraints | ✅ | 4 constraints |
| Method enumeration (if interface) | N/A | Not implementing interface |
| Test requirements | ⚠️ | Documentation task, not code - no unit tests |
| Git commit discipline | ⚠️ | Not explicitly mentioned |
| Calculation reference | ✅ | Contrast formula provided |

### Action Required
1. ⚠️ Tests: This is an audit/documentation task. Validation is the contrast ratios themselves.
2. ⚠️ Git: Add git commit reminder.

**Overall**: Prompt is sufficient. Contrast testing is measurement/documentation, not code implementation.

---

## Summary

Both prompts pass audit with minor notes:
- ARIA work (#428) validates via structural inspection, not unit tests
- Contrast work (#429) validates via documented ratios, not unit tests
- Both should include git commit reminders (will add)

**Decision**: Prompts are ready for execution. The ⚠️ items reflect the nature of accessibility work (structural/documentation) rather than missing requirements.
