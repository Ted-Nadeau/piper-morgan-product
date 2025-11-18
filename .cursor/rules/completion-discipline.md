---
description: Completion discipline
globs:
  - "**/*.py"
  - "**/*.md"
alwaysApply: true
---

# CURSOR COMPLETION REQUIREMENTS

## Rule #1: No exceptions without PM approval
Breaking these rules = session failure. Ask first if uncertain.

## The "Time Lord Alert" escape hatch

If you're uncertain about a decision but uncomfortable expressing it directly, just say: **"Time Lord Alert"** and the PM will pause for discussion. This is your face-saving signal - use it freely.

## Anti-completion-bias protocol

YOU MUST NEVER:
- Declare completion without 100% of acceptance criteria met
- Rationalize gaps as "minor" or "not critical"
- Skip STOP conditions because work is "almost done"
- Defer tasks without explicit PM approval
- Claim "tests pass" without providing terminal output

If you catch yourself thinking "this is good enough" → STOP and escalate immediately.

## Mandatory STOP conditions (17 total)

If ANY of these occur, you MUST stop immediately and escalate to PM - no exceptions:

1. Infrastructure doesn't match gameplan assumptions
2. Method implementation <100% complete
3. Pattern already exists in catalog
4. Tests fail for any reason
5. Configuration assumptions needed
6. GitHub issue missing or unassigned
7. Can't provide verification evidence
8. ADR conflicts with approach
9. Resource not found after searching
10. User data at risk
11. Completion bias detected (claiming without proof)
12. Rationalizing gaps as "minor" or "optional"
13. GitHub tracking not working
14. Single agent seems sufficient (multi-agent is default)
15. Git operations failing
16. Server state unexpected or unclear
17. UI behavior can't be visually confirmed

**CRITICAL**: YOU DO NOT DECIDE which failures are "critical" - the PM decides. Your job is to report the issue, provide options, and wait for PM guidance.

## Context requirements (unchanged)
1. Read CLAUDE.md for methodology
2. Check shared_types.py for ALL enums
3. Use Context7 MCP for latest docs
4. STOP if assumptions needed
5. Don't do Code's assigned work

## Completion protocol (NEW)

### All phases must be 100% complete before moving forward

- Evidence required (terminal output, not claims)
- No deferrals without PM approval
- Update GitHub descriptions (not just comments)
- Session logs must document all decisions

### STOP conditions (immediate escalation)

If ANY occur, STOP and report to PM:
- Tests fail (any failure, don't rationalize)
- Assumptions needed (don't guess)
- Pattern might exist elsewhere (check first)
- Can't verify claims (no evidence available)
- Infrastructure doesn't match expectations

### Test failure reporting

If tests fail:
```
⚠️ STOP - [X] Tests Failing

Errors:
[paste output]

Root cause:
[your analysis]

Options:
1. [approach 1]
2. [approach 2]

Awaiting PM decision.
```

YOU DON'T DECIDE CRITICALITY - PM DOES.

## Anti-patterns to avoid

❌ "Tests mostly pass" (all must pass)
❌ "Core functionality works" (everything must work)
❌ "Minor issue, not blocking" (PM decides priority)
❌ Skipping phases without approval
❌ Deferring work without permission
