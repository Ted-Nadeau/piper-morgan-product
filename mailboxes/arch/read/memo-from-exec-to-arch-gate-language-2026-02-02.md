# Memo: Sprint Gate Issue Language Request

**From**: Chief of Staff (on behalf of PM)
**To**: Chief Architect
**Date**: February 2, 2026
**Re**: Anti-Flattening Gates for MVP Sprints M0-M6

---

## Context

Ship #028's learning pattern ("Conversation ≠ Reality") documented how portfolio onboarding appeared to work conversationally while never actually writing to the database. This is the third manifestation of the 75% Pattern:
- August 2025: Repository stubs
- January 28: #728 projects never saved
- January 30: #734 calendar token leak

The pattern: infrastructure exists, interface defined, final wiring missing. Unit tests with mocked databases hide the gap.

## Request

Please draft **Gate issue language** that can be added to sprints M0 through M6. These gates should ensure sprints cannot be closed without:

1. **Persistence Layer Audit**
   - Verify that user-facing "success" messages correspond to actual database writes
   - E2E test coverage for critical user flows (not just unit tests with mocks)
   - Evidence requirement: specific test names or manual verification log

2. **Anti-Flattening Verification**
   - Check that implementation matches design intent (per Implementation Guide)
   - Verify no "parrot confirmations" or robotic patterns introduced
   - The "Colleague Test" applied to new conversational flows

3. **Multi-Tenancy Sanity Check** (where applicable)
   - User-scoped data is actually user-scoped
   - No hardcoded `user_id="default"` patterns
   - Cross-user data leakage not possible

## Suggested Deliverable

A template Gate issue that can be:
- Added as a child of each sprint epic (M0-M6)
- Cannot be closed without explicit sign-off on each criterion
- References specific evidence (test names, audit logs, verification screenshots)

## Urgency

M0 (Conversational Glue) is ready to start once alpha bugs stabilize. Having the Gate template before M0 closes would operationalize this lesson immediately.

---

*Please advise if you need additional context or would like to discuss scope.*
